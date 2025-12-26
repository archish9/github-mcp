"""
Individual examples for Branch Management tools

Run a specific example:
    python examples/branch_management/individual_examples.py list
    python examples/branch_management/individual_examples.py protection
    python examples/branch_management/individual_examples.py compare
    python examples/branch_management/individual_examples.py create
    python examples/branch_management/individual_examples.py delete
    python examples/branch_management/individual_examples.py merge

Run all examples:
    python examples/branch_management/individual_examples.py
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()
load_dotenv(PROJECT_ROOT / ".env")

def get_server_env():
    env = dict(os.environ)
    src_path = str(PROJECT_ROOT / "src")
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] = src_path + os.pathsep + env["PYTHONPATH"]
    else:
        env["PYTHONPATH"] = src_path
    return env

SERVER_PARAMS = StdioServerParameters(
    command=sys.executable,
    args=["-m", "github_mcp.server"],
    env=get_server_env(),
    cwd=str(PROJECT_ROOT)
)

def print_result(result, title="Result"):
    """Pretty print JSON result"""
    print(f"\n{title}:")
    print("-" * 70)
    try:
        text = result.content[0].text
        data = json.loads(text)
        if isinstance(data, dict) and "error" in data:
            print("ERROR:")
            print(f"   {data.get('message', data.get('error'))}")
        else:
            print(json.dumps(data, indent=2))
    except:
        print(result.content[0].text)
    print()


async def example_list_branches():
    """Example: List all branches in a repository"""
    try:
        async with stdio_client(SERVER_PARAMS) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print("=" * 70)
                print("Example: List Branches")
                print("=" * 70)
                
                # List all branches
                print("\n1. Listing branches in facebook/react...")
                result = await session.call_tool(
                    "list_branches",
                    arguments={
                        "owner": "facebook",
                        "repo": "react"
                    }
                )
                print_result(result, "All Branches")
                
                # List only protected branches
                print("\n2. Listing protected branches in microsoft/vscode...")
                result = await session.call_tool(
                    "list_branches",
                    arguments={
                        "owner": "microsoft",
                        "repo": "vscode",
                        "protected_only": True
                    }
                )
                print_result(result, "Protected Branches")
                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


async def example_get_branch_protection():
    """Example: Get branch protection rules"""
    try:
        async with stdio_client(SERVER_PARAMS) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print("=" * 70)
                print("Example: Get Branch Protection")
                print("=" * 70)
                
                # Get protection for main branch
                print("\n1. Getting protection rules for microsoft/vscode main branch...")
                result = await session.call_tool(
                    "get_branch_protection",
                    arguments={
                        "owner": "microsoft",
                        "repo": "vscode",
                        "branch": "main"
                    }
                )
                print_result(result, "Branch Protection")
                
                # Get protection for default branch
                print("\n2. Getting protection for vercel/next.js default branch...")
                result = await session.call_tool(
                    "get_branch_protection",
                    arguments={
                        "owner": "vercel",
                        "repo": "next.js"
                    }
                )
                print_result(result, "Branch Protection")
                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


async def example_compare_branches():
    """Example: Compare two branches"""
    try:
        async with stdio_client(SERVER_PARAMS) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print("=" * 70)
                print("Example: Compare Branches")
                print("=" * 70)
                
                # Compare main to a recent commit
                print("\n1. Comparing HEAD~5 to HEAD in microsoft/vscode...")
                result = await session.call_tool(
                    "compare_branches",
                    arguments={
                        "owner": "microsoft",
                        "repo": "vscode",
                        "base": "HEAD~5",
                        "head": "HEAD"
                    }
                )
                print_result(result, "Branch Comparison")
                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


async def example_create_branch():
    """Example: Create a new branch (requires write access)"""
    owner = os.getenv("GITHUB_REPO_OWNER")
    repo = os.getenv("GITHUB_REPO_NAME")
    
    if not owner or not repo:
        print("=" * 70)
        print("Example: Create Branch")
        print("=" * 70)
        print("\nNote: This example requires write access to a repository.")
        print("Set GITHUB_REPO_OWNER and GITHUB_REPO_NAME in your .env file.")
        print("\nExample usage (in code):")
        print('  await session.call_tool("create_branch", arguments={')
        print('      "owner": "your-username",')
        print('      "repo": "your-repo",')
        print('      "branch_name": "feature/new-feature",')
        print('      "from_branch": "main"')
        print("  })")
        return
    
    try:
        async with stdio_client(SERVER_PARAMS) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print("=" * 70)
                print("Example: Create Branch")
                print("=" * 70)
                
                branch_name = f"test-branch-{int(__import__('time').time())}"
                
                print(f"\nCreating branch '{branch_name}' in {owner}/{repo}...")
                result = await session.call_tool(
                    "create_branch",
                    arguments={
                        "owner": owner,
                        "repo": repo,
                        "branch_name": branch_name
                    }
                )
                print_result(result, "Branch Created")
                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


async def example_delete_branch():
    """Example: Delete a branch (requires write access)"""
    print("=" * 70)
    print("Example: Delete Branch")
    print("=" * 70)
    print("\nNote: This example requires write access to a repository.")
    print("Set GITHUB_REPO_OWNER and GITHUB_REPO_NAME in your .env file.")
    print("\nExample usage (in code):")
    print('  await session.call_tool("delete_branch", arguments={')
    print('      "owner": "your-username",')
    print('      "repo": "your-repo",')
    print('      "branch_name": "feature/old-feature"')
    print("  })")


async def example_merge_branches():
    """Example: Merge branches (requires write access)"""
    print("=" * 70)
    print("Example: Merge Branches")
    print("=" * 70)
    print("\nNote: This example requires write access to a repository.")
    print("Set GITHUB_REPO_OWNER and GITHUB_REPO_NAME in your .env file.")
    print("\nExample usage (in code):")
    print('  await session.call_tool("merge_branches", arguments={')
    print('      "owner": "your-username",')
    print('      "repo": "your-repo",')
    print('      "base": "main",')
    print('      "head": "feature/my-feature",')
    print('      "commit_message": "Merge feature branch"')
    print("  })")


async def run_all_examples():
    """Run all examples"""
    examples = [
        ("List Branches", example_list_branches),
        ("Get Branch Protection", example_get_branch_protection),
        ("Compare Branches", example_compare_branches),
        ("Create Branch", example_create_branch),
        ("Delete Branch", example_delete_branch),
        ("Merge Branches", example_merge_branches),
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
        await asyncio.sleep(1)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        example_name = sys.argv[1].lower()
        examples = {
            "list": example_list_branches,
            "protection": example_get_branch_protection,
            "compare": example_compare_branches,
            "create": example_create_branch,
            "delete": example_delete_branch,
            "merge": example_merge_branches,
        }
        
        if example_name in examples:
            print(f"Running example: {example_name}")
            asyncio.run(examples[example_name]())
        else:
            print(f"Unknown example: {example_name}")
            print(f"Available: {', '.join(examples.keys())}")
    else:
        asyncio.run(run_all_examples())
