import asyncio
import dotenv
import os
from pathlib import Path
import argparse

from src.common import agent_utils


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

    agent = agent_utils.BasicAgent(
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
