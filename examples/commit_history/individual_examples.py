"""
Individual examples for Commit History tools
Copy and modify these examples for your own use

Run a specific example:
    python examples/commit_history/individual_examples.py list
    python examples/commit_history/individual_examples.py details
    python examples/commit_history/individual_examples.py search
    python examples/commit_history/individual_examples.py compare
    python examples/commit_history/individual_examples.py stats

Run all examples:
    python examples/commit_history/individual_examples.py
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Get project root (parent of examples directory)
PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()

# Load environment variables from .env file
load_dotenv(PROJECT_ROOT / ".env")

# Build environment with PYTHONPATH for package discovery
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

def print_result(result, title="Result"):
    """Pretty print JSON result with error handling"""
    print(f"\n{title}:")
    print("-" * 70)
    try:
        text = result.content[0].text
        data = json.loads(text)
        
        if isinstance(data, dict) and "error" in data:
            print("ERROR:")
            error_msg = data.get('message') or data.get('error') or 'Unknown error'
            print(f"   {error_msg}")
            if "suggestions" in data:
                print("\nSuggestions:")
                for suggestion in data["suggestions"]:
                    print(f"   - {suggestion}")
        else:
            print(json.dumps(data, indent=2))
    except json.JSONDecodeError:
        print(result.content[0].text)
    except Exception as e:
        print(f"Error parsing result: {e}")
    print()


async def example_list_commits():
    """Example: List recent commits from a repository"""
    try:
        async with stdio_client(SERVER_PARAMS) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print("=" * 70)
                print("Example: List Commits")
                print("=" * 70)
                
                # Example 1: List recent commits from a popular repo
                print("\n1. Getting last 5 commits from microsoft/vscode...")
                result = await session.call_tool(
                    "list_commits",
                    arguments={
                        "owner": "microsoft",
                        "repo": "vscode",
                        "limit": 5
                    }
                )
                print_result(result, "Recent Commits")
                
                # Example 2: List commits from a specific branch
                print("\n2. Getting commits from facebook/react main branch...")
                result = await session.call_tool(
                    "list_commits",
                    arguments={
                        "owner": "facebook",
                        "repo": "react",
                        "branch": "main",
                        "limit": 5
                    }
                )
                print_result(result, "Branch Commits")
                
    except Exception as e:
        print(f"Error running example: {e}")
        import traceback
        traceback.print_exc()


async def example_get_commit_details():
    """Example: Get details about a specific commit"""
    try:
        async with stdio_client(SERVER_PARAMS) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print("=" * 70)
                print("Example: Get Commit Details")
                print("=" * 70)
                
                # First, get a recent commit SHA
                print("\n1. First, getting a recent commit from vercel/next.js...")
                result = await session.call_tool(
                    "list_commits",
                    arguments={
                        "owner": "vercel",
                        "repo": "next.js",
                        "limit": 1
                    }
                )
                
                # Parse the result to get SHA
                data = json.loads(result.content[0].text)
                if data.get("commits"):
                    sha = data["commits"][0]["sha"]
                    print(f"   Found commit: {sha[:7]}")
                    
                    # Now get details
                    print(f"\n2. Getting details for commit {sha[:7]}...")
                    result = await session.call_tool(
                        "get_commit_details",
                        arguments={
                            "owner": "vercel",
                            "repo": "next.js",
                            "sha": sha,
                            "include_patch": False
                        }
                    )
                    print_result(result, "Commit Details")
                else:
                    print("   No commits found")
                
    except Exception as e:
        print(f"Error running example: {e}")
        import traceback
        traceback.print_exc()


async def example_search_commits():
    """Example: Search commits by author or date"""
    try:
        async with stdio_client(SERVER_PARAMS) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print("=" * 70)
                print("Example: Search Commits")
                print("=" * 70)
                
                # Example 1: Search by date range
                print("\n1. Searching commits from last week in python/cpython...")
                from datetime import datetime, timedelta
                since_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
                
                result = await session.call_tool(
                    "search_commits",
                    arguments={
                        "owner": "python",
                        "repo": "cpython",
                        "since": since_date,
                        "limit": 5
                    }
                )
                print_result(result, "Recent Commits")
                
                # Example 2: Search by file path
                print("\n2. Searching commits that modified README in vercel/next.js...")
                result = await session.call_tool(
                    "search_commits",
                    arguments={
                        "owner": "vercel",
                        "repo": "next.js",
                        "path": "README.md",
                        "limit": 5
                    }
                )
                print_result(result, "README Commits")
                
    except Exception as e:
        print(f"Error running example: {e}")
        import traceback
        traceback.print_exc()


async def example_compare_commits():
    """Example: Compare branches or commits"""
    try:
        async with stdio_client(SERVER_PARAMS) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print("=" * 70)
                print("Example: Compare Commits/Branches")
                print("=" * 70)
                
                # Compare two recent commits
                print("\n1. Comparing HEAD~5 to HEAD in microsoft/vscode...")
                result = await session.call_tool(
                    "compare_commits",
                    arguments={
                        "owner": "microsoft",
                        "repo": "vscode",
                        "base": "HEAD~5",
                        "head": "HEAD"
                    }
                )
                print_result(result, "Comparison")
                
    except Exception as e:
        print(f"Error running example: {e}")
        import traceback
        traceback.print_exc()


async def example_get_commit_stats():
    """Example: Get commit statistics"""
    try:
        async with stdio_client(SERVER_PARAMS) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print("=" * 70)
                print("Example: Commit Statistics")
                print("=" * 70)
                
                # Get stats for last 30 days
                print("\n1. Getting commit stats for last 30 days in facebook/react...")
                result = await session.call_tool(
                    "get_commit_stats",
                    arguments={
                        "owner": "facebook",
                        "repo": "react",
                        "days": 30
                    }
                )
                print_result(result, "Commit Stats (30 days)")
                
                # Get stats for last 7 days
                print("\n2. Getting commit stats for last 7 days in vercel/next.js...")
                result = await session.call_tool(
                    "get_commit_stats",
                    arguments={
                        "owner": "vercel",
                        "repo": "next.js",
                        "days": 7
                    }
                )
                print_result(result, "Commit Stats (7 days)")
                
    except Exception as e:
        print(f"Error running example: {e}")
        import traceback
        traceback.print_exc()


async def run_all_examples():
    """Run all examples"""
    examples = [
        ("List Commits", example_list_commits),
        ("Get Commit Details", example_get_commit_details),
        ("Search Commits", example_search_commits),
        ("Compare Commits", example_compare_commits),
        ("Commit Statistics", example_get_commit_stats),
    ]
    
    for name, example_func in examples:
        print("\n" + "=" * 70)
        print(f"EXAMPLE: {name}")
        print("=" * 70 + "\n")
        try:
            await example_func()
        except Exception as e:
            print(f"Error: {e}")
        print("\n")
        await asyncio.sleep(1)  # Rate limiting


if __name__ == "__main__":
    if len(sys.argv) > 1:
        example_name = sys.argv[1].lower()
        examples = {
            "list": example_list_commits,
            "details": example_get_commit_details,
            "search": example_search_commits,
            "compare": example_compare_commits,
            "stats": example_get_commit_stats,
        }
        
        if example_name in examples:
            print(f"Running example: {example_name}")
            asyncio.run(examples[example_name]())
        else:
            print(f"Unknown example: {example_name}")
            print(f"Available: {', '.join(examples.keys())}")
    else:
        asyncio.run(run_all_examples())
