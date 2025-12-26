"""
Individual examples for Repository Statistics tools
Copy and modify these examples for your own use

Run a specific example:
    python examples/repo_statistics/individual_examples.py contributors
    python examples/repo_statistics/individual_examples.py code_frequency
    python examples/repo_statistics/individual_examples.py commit_activity
    python examples/repo_statistics/individual_examples.py languages
    python examples/repo_statistics/individual_examples.py traffic
    python examples/repo_statistics/individual_examples.py community

Run all examples:
    python examples/repo_statistics/individual_examples.py
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
    command=sys.executable,  # Use same Python as this script
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
        
        # Check for error responses
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


async def example_get_contributor_stats():
    """Example: Get contributor statistics for a repository"""
    try:
        async with stdio_client(SERVER_PARAMS) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print("=" * 70)
                print("Example: Contributor Statistics")
                print("=" * 70)
                
                # Example: Get top contributors for a popular repo
                print("\n1. Getting top 5 contributors for python/cpython...")
                result = await session.call_tool(
                    "get_contributor_stats",
                    arguments={
                        "owner": "python",
                        "repo": "cpython",
                        "limit": 5
                    }
                )
                print_result(result, "Contributor Stats")
                
                # Example 2: More contributors from another repo
                print("\n2. Getting top 10 contributors for vercel/next.js...")
                result = await session.call_tool(
                    "get_contributor_stats",
                    arguments={
                        "owner": "vercel",
                        "repo": "next.js",
                        "limit": 10
                    }
                )
                print_result(result, "Contributor Stats")
                
    except Exception as e:
        print(f"Error running example: {e}")
        import traceback
        traceback.print_exc()


async def example_get_code_frequency():
    """Example: Get code frequency (additions/deletions over time)"""
    try:
        async with stdio_client(SERVER_PARAMS) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print("=" * 70)
                print("Example: Code Frequency")
                print("=" * 70)
                
                # Example: Get code frequency for a repo
                print("\n1. Getting code frequency for facebook/react...")
                result = await session.call_tool(
                    "get_code_frequency",
                    arguments={
                        "owner": "facebook",
                        "repo": "react"
                    }
                )
                print_result(result, "Code Frequency")
                
    except Exception as e:
        print(f"Error running example: {e}")
        import traceback
        traceback.print_exc()


async def example_get_commit_activity():
    """Example: Get commit activity by week"""
    try:
        async with stdio_client(SERVER_PARAMS) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print("=" * 70)
                print("Example: Commit Activity")
                print("=" * 70)
                
                # Example: Get commit activity for a repo
                print("\n1. Getting commit activity for microsoft/vscode...")
                result = await session.call_tool(
                    "get_commit_activity",
                    arguments={
                        "owner": "microsoft",
                        "repo": "vscode"
                    }
                )
                print_result(result, "Commit Activity")
                
    except Exception as e:
        print(f"Error running example: {e}")
        import traceback
        traceback.print_exc()


async def example_get_language_breakdown():
    """Example: Get language breakdown for a repository"""
    try:
        async with stdio_client(SERVER_PARAMS) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print("=" * 70)
                print("Example: Language Breakdown")
                print("=" * 70)
                
                # Example 1: Language breakdown for a multi-language repo
                print("\n1. Getting language breakdown for tensorflow/tensorflow...")
                result = await session.call_tool(
                    "get_language_breakdown",
                    arguments={
                        "owner": "tensorflow",
                        "repo": "tensorflow"
                    }
                )
                print_result(result, "Language Breakdown")
                
                # Example 2: Another repo
                print("\n2. Getting language breakdown for rust-lang/rust...")
                result = await session.call_tool(
                    "get_language_breakdown",
                    arguments={
                        "owner": "rust-lang",
                        "repo": "rust"
                    }
                )
                print_result(result, "Language Breakdown")
                
    except Exception as e:
        print(f"Error running example: {e}")
        import traceback
        traceback.print_exc()


async def example_get_traffic_stats():
    """Example: Get traffic statistics (requires push access)"""
    # Get default repo from environment
    owner = os.getenv("GITHUB_REPO_OWNER")
    repo = os.getenv("GITHUB_REPO_NAME")
    
    if not owner or not repo:
        print("=" * 70)
        print("Example: Traffic Statistics")
        print("=" * 70)
        print("\nNote: Traffic stats require push access to the repository.")
        print("Set GITHUB_REPO_OWNER and GITHUB_REPO_NAME in your .env file")
        print("to test with your own repository.")
        print("\nExample .env:")
        print("  GITHUB_REPO_OWNER=your-username")
        print("  GITHUB_REPO_NAME=your-repo")
        return
    
    try:
        async with stdio_client(SERVER_PARAMS) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print("=" * 70)
                print("Example: Traffic Statistics")
                print("=" * 70)
                print(f"\nNote: Using repository {owner}/{repo} from environment")
                print("(Traffic stats require push access to the repository)\n")
                
                result = await session.call_tool(
                    "get_traffic_stats",
                    arguments={
                        "owner": owner,
                        "repo": repo
                    }
                )
                print_result(result, "Traffic Stats")
                
    except Exception as e:
        print(f"Error running example: {e}")
        import traceback
        traceback.print_exc()


async def example_get_community_health():
    """Example: Get community health metrics"""
    try:
        async with stdio_client(SERVER_PARAMS) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print("=" * 70)
                print("Example: Community Health")
                print("=" * 70)
                
                # Example 1: Well-established project
                print("\n1. Getting community health for microsoft/vscode...")
                result = await session.call_tool(
                    "get_community_health",
                    arguments={
                        "owner": "microsoft",
                        "repo": "vscode"
                    }
                )
                print_result(result, "Community Health")
                
                # Example 2: Another project
                print("\n2. Getting community health for facebook/react...")
                result = await session.call_tool(
                    "get_community_health",
                    arguments={
                        "owner": "facebook",
                        "repo": "react"
                    }
                )
                print_result(result, "Community Health")
                
    except Exception as e:
        print(f"Error running example: {e}")
        import traceback
        traceback.print_exc()


async def run_all_examples():
    """Run all examples"""
    examples = [
        ("Contributor Statistics", example_get_contributor_stats),
        ("Code Frequency", example_get_code_frequency),
        ("Commit Activity", example_get_commit_activity),
        ("Language Breakdown", example_get_language_breakdown),
        ("Traffic Statistics", example_get_traffic_stats),
        ("Community Health", example_get_community_health),
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
        # Run specific example
        example_name = sys.argv[1].lower()
        examples = {
            "contributors": example_get_contributor_stats,
            "code_frequency": example_get_code_frequency,
            "commit_activity": example_get_commit_activity,
            "languages": example_get_language_breakdown,
            "traffic": example_get_traffic_stats,
            "community": example_get_community_health,
        }
        
        if example_name in examples:
            print(f"Running example: {example_name}")
            asyncio.run(examples[example_name]())
        else:
            print(f"Unknown example: {example_name}")
            print(f"Available: {', '.join(examples.keys())}")
    else:
        # Run all examples
        asyncio.run(run_all_examples())
