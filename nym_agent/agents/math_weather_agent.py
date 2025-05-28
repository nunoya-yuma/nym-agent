import asyncio
import dotenv
import os
from pathlib import Path
import argparse
import logging

from langchain_community.tools.tavily_search import TavilySearchResults

from nym_agent.common import agent_utils


logger = logging.getLogger("nym_agent")


async def main():
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s[%(levelname)s] %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.info("Starting Math and Weather Agent...")
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

    current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    math_server_path = \
        str(current_dir.parent / "mcp_servers" / "math" / "math_stdio.py")
    mcp_config = {
        "math": {
            "command": "python",
            "args": [math_server_path],
            "transport": "stdio",
        },
        "weather": {
            "url": "http://localhost:8000/mcp",
            "transport": "streamable_http",
        }
    }

    search = TavilySearchResults(max_results=2)
    tools = [search]

    agent = agent_utils.BasicAgent(
        model_provider=args.provider,
        mcp_config=mcp_config,
        tools=tools,
    )
    async with agent.session():
        logger.info("Agent session started.")
        _ = await agent.send_query("what's (3 + 5) x 12")
        _ = await agent.send_query(
            "I live in Osaka. Do you know where that is?"
            " (No need to search the web.)")
        _ = await agent.send_query(
            "What is the weather at my current location?")
        _ = await agent.send_query(
            "Research one of today's Japanese news"
            " and tell me about it in Japanese.")


if __name__ == "__main__":
    asyncio.run(main())
