from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
import asyncio
import dotenv
import os
from pathlib import Path
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
import uuid
import argparse
from typing import List


class AgentWithMCP:
    def __init__(self, model_provider="openai"):
        self._client = None
        self._agent = None
        self._mcp_config = {}

        # Set model based on provider
        if model_provider == "openai":
            self._model = init_chat_model(
                "gpt-4o-mini",
                model_provider="openai",
                streamable=True,
            )
        elif model_provider == "google_genai":
            self._model = init_chat_model(
                "gemini-2.0-flash",
                model_provider="google_genai",
                streamable=True,
            )
        else:
            raise ValueError(f"Unsupported model provider: {model_provider}")

        self._memory = MemorySaver()

        thread_id = str(uuid.uuid4())
        self._config = {"configurable": {"thread_id": thread_id}}
        print(f"Thread ID: {thread_id}")
        print(f"Using model provider: {model_provider}")

    def register_mcp_stdio(self, name: str, command: List[str]) -> None:
        self._mcp_config[name] = {
            "command": command[0],
            "args": command[1:],
            "transport": "stdio"
        }

    def register_mcp_streamable_http(self, name: str, url: str) -> None:
        self._mcp_config[name] = {
            "url": url,
            "transport": "streamable_http"
        }

    async def session(self):
        if self._mcp_config == {}:
            raise ValueError("No MCP servers registered")
        if self._client is not None:
            raise ValueError("MCP client already created")
        if self._agent is not None:
            raise ValueError("MCP agent already created")
        if self._model is None:
            raise ValueError("No model specified")
        if self._memory is None:
            raise ValueError("No memory specified")

        self._client = MultiServerMCPClient(self._mcp_config)
        tools = await self._client.get_tools()
        self._agent = create_react_agent(
            self._model,
            tools=tools,
            checkpointer=self._memory,
        )

    async def send_query(self, message: str) -> str:
        if self._agent is None:
            raise RuntimeError(
                "Agent session not active. Call session() first.")

        result = ""

        structured_message = {
            "messages": [HumanMessage(content=message)],
        }

        async for weather_res in self._agent.astream(
            structured_message,
            self._config,
            stream_mode="values",
        ):
            weather_res["messages"][-1].pretty_print()
            result += weather_res["messages"][-1].content

        return result


async def main():
    dotenv.load_dotenv()

    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Weather and Math Agent using MCP"
    )
    parser.add_argument(
        "--provider",
        choices=["openai", "google_genai"],
        default="google_genai",
        help="Model provider to use (openai or google_genai)"
    )
    args = parser.parse_args()

    agent = AgentWithMCP(
        model_provider=args.provider
    )

    current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    math_server_path = \
        str(current_dir.parent / "mcp_servers" / "math" / "math_stdio.py")
    agent.register_mcp_stdio("math", ["uv", "run", math_server_path])
    agent.register_mcp_streamable_http("weather", "http://localhost:8000/mcp")

    await agent.session()
    _ = await agent.send_query("what's (3 + 5) x 12")
    _ = await agent.send_query(
        "I live in Osaka. Do you know where that is?")
    _ = await agent.send_query(
        "What is the weather at my current location?")


if __name__ == "__main__":
    asyncio.run(main())
