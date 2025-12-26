"""
Interactive demo for Repository Statistics tools
Run this script and follow the menu prompts to explore the tools interactively.

Usage:
    python examples/repo_statistics/interactive_demo.py
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()

# Load environment variables
load_dotenv(PROJECT_ROOT / ".env")

# Build environment with PYTHONPATH
def get_server_env():
    env = dict(os.environ)
    src_path = str(PROJECT_ROOT / "src")
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] = src_path + os.pathsep + env["PYTHONPATH"]
    else:
        env["PYTHONPATH"] = src_path
    return env

# Server configuration
SERVER_PARAMS = StdioServerParameters(
    command=sys.executable,
    args=["-m", "github_mcp.server"],
    env=get_server_env(),
    cwd=str(PROJECT_ROOT)
)


def print_result(result):
    """Pretty print JSON result"""
    try:
        text = result.content[0].text
        data = json.loads(text)
        
        if isinstance(data, dict) and "error" in data:
            print("\n[ERROR]")
            print(f"  {data.get('message', data.get('error'))}")
            if "suggestions" in data:
                print("\n  Suggestions:")
                for s in data["suggestions"]:
                    print(f"    - {s}")
        else:
            print("\n[RESULT]")
            print(json.dumps(data, indent=2))
    except json.JSONDecodeError:
        print(result.content[0].text)
    except Exception as e:
        print(f"Error: {e}")


def print_menu():
    """Print the menu options"""
    print("\n" + "=" * 60)
    print("GitHub MCP - Repository Statistics Demo")
    print("=" * 60)
    print("\nSelect an option:")
    print("  1. Get Contributor Statistics")
    print("  2. Get Code Frequency")
    print("  3. Get Commit Activity")
    print("  4. Get Language Breakdown")
    print("  5. Get Traffic Statistics (requires push access)")
    print("  6. Get Community Health")
    print("  0. Exit")
    print()


async def get_contributor_stats(session):
    """Interactive contributor stats"""
    owner = input("Repository owner: ").strip()
    repo = input("Repository name: ").strip()
    limit = input("Number of contributors to show (default: 10): ").strip()
    limit = int(limit) if limit else 10
    
    print("\nFetching contributor statistics...")
    result = await session.call_tool(
        "get_contributor_stats",
        arguments={"owner": owner, "repo": repo, "limit": limit}
    )
    print_result(result)


async def get_code_frequency(session):
    """Interactive code frequency"""
    owner = input("Repository owner: ").strip()
    repo = input("Repository name: ").strip()
    
    print("\nFetching code frequency...")
    result = await session.call_tool(
        "get_code_frequency",
        arguments={"owner": owner, "repo": repo}
    )
    print_result(result)


async def get_commit_activity(session):
    """Interactive commit activity"""
    owner = input("Repository owner: ").strip()
    repo = input("Repository name: ").strip()
    
    print("\nFetching commit activity...")
    result = await session.call_tool(
        "get_commit_activity",
        arguments={"owner": owner, "repo": repo}
    )
    print_result(result)


async def get_language_breakdown(session):
    """Interactive language breakdown"""
    owner = input("Repository owner: ").strip()
    repo = input("Repository name: ").strip()
    
    print("\nFetching language breakdown...")
    result = await session.call_tool(
        "get_language_breakdown",
        arguments={"owner": owner, "repo": repo}
    )
    print_result(result)


async def get_traffic_stats(session):
    """Interactive traffic stats"""
    print("\n[NOTE] Traffic statistics require push access to the repository.")
    print("Use your own repository for this feature.\n")
    
    owner = input("Repository owner (your username): ").strip()
    repo = input("Repository name (your repo): ").strip()
    
    print("\nFetching traffic statistics...")
    result = await session.call_tool(
        "get_traffic_stats",
        arguments={"owner": owner, "repo": repo}
    )
    print_result(result)


async def get_community_health(session):
    """Interactive community health"""
    owner = input("Repository owner: ").strip()
    repo = input("Repository name: ").strip()
    
    print("\nFetching community health metrics...")
    result = await session.call_tool(
        "get_community_health",
        arguments={"owner": owner, "repo": repo}
    )
    print_result(result)


async def main():
    """Main interactive loop"""
    print("Connecting to GitHub MCP server...")
    
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("Connected!")
            
            while True:
                print_menu()
                
                try:
                    choice = input("Select an option (0-6): ").strip()
                    
                    if choice == "0":
                        print("\nGoodbye!")
                        break
                    elif choice == "1":
                        await get_contributor_stats(session)
                    elif choice == "2":
                        await get_code_frequency(session)
                    elif choice == "3":
                        await get_commit_activity(session)
                    elif choice == "4":
                        await get_language_breakdown(session)
                    elif choice == "5":
                        await get_traffic_stats(session)
                    elif choice == "6":
                        await get_community_health(session)
                    else:
                        print("Invalid option. Please try again.")
                        
                except KeyboardInterrupt:
                    print("\n\nGoodbye!")
                    break
                except Exception as e:
                    print(f"\nError: {e}")
                    import traceback
                    traceback.print_exc()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")
