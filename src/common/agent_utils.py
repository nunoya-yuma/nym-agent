from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
import uuid
from typing import List
from contextlib import asynccontextmanager, AsyncExitStack


class BasicAgent:
    def __init__(
            self,
            model_provider: str,
            model_name: str = "",
            mcp_config: dict = None,
            tools: List[any] = None
    ):
        self._client = None
        self._agent = None
        self._tools = tools
        self._model = self._select_model(model_provider, model_name)
        self._mcp_config = mcp_config
        self._memory = MemorySaver()

        thread_id = str(uuid.uuid4())
        self._config = {"configurable": {"thread_id": thread_id}}
        print(f"Thread ID: {thread_id}")
        print(f"Using model provider: {model_provider}")

    @asynccontextmanager
    async def session(self):
        if self._client is not None:
            raise ValueError("MCP client already created")
        if self._agent is not None:
            raise ValueError("Agent is already created")
        if self._model is None:
            raise ValueError("No model specified")
        if self._memory is None:
            raise ValueError("No memory specified")

        self._client = MultiServerMCPClient(self._mcp_config)
        async with AsyncExitStack() as stack:
            for server_name in self._mcp_config.keys():
                session = await stack.enter_async_context(
                    self._client.session(server_name)
                )
                tools = await load_mcp_tools(session)
                self._tools.extend(tools)

            self._agent = create_react_agent(
                self._model,
                tools=self._tools,
                checkpointer=self._memory,
            )
            yield

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

    @staticmethod
    def _select_model(model_provider: str, model_name: str = ""):
        selected_model = None
        if model_name:
            selected_model = init_chat_model(
                model_name,
                model_provider=model_provider,
            )
        elif model_provider == "openai":
            selected_model = init_chat_model(
                "gpt-4o-mini",
                model_provider="openai",
            )
        elif model_provider == "google_genai":
            selected_model = init_chat_model(
                "gemini-2.0-flash",
                model_provider="google_genai",
                model_kwargs={"streamable": True},
            )
        else:
            raise ValueError(f"Unsupported model provider: {model_provider}")

        return selected_model
