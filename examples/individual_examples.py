"""
Individual examples for each GitHub MCP tool
Copy and modify these examples for your own use
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
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

# Load environment variables from .env file
load_dotenv(PROJECT_ROOT / ".env")

# Server configuration
SERVER_PARAMS = StdioServerParameters(
    command=sys.executable,  # Use same Python as this script (important for venv!)
    args=["-m", "github_mcp.server"],
    env=dict(os.environ),  # Inherit environment variables (now includes .env)
    cwd=str(PROJECT_ROOT)  # Set working directory so .env is found
)

async def example_search_repositories():
    """Example: Search for repositories"""
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Example 1: Search Python repos with many stars
            result = await session.call_tool(
                "search_repositories",
                arguments={
                    "query": "language:python stars:>10000",
                    "sort": "stars",
                    "limit": 5
                }
            )
            print("Python repos with >10k stars:")
            print(result.content[0].text)
            print("\n" + "="*50 + "\n")
            
            # Example 2: Search for machine learning repos
            result = await session.call_tool(
                "search_repositories",
                arguments={
                    "query": "machine learning language:python",
                    "sort": "stars",
                    "limit": 5
                }
            )
            print("Machine Learning repos:")
            print(result.content[0].text)
            print("\n" + "="*50 + "\n")
            
            # Example 3: Recently updated JavaScript repos
            result = await session.call_tool(
                "search_repositories",
                arguments={
                    "query": "language:javascript",
                    "sort": "updated",
                    "limit": 5
                }
            )
            print("Recently updated JavaScript repos:")
            print(result.content[0].text)

async def example_get_repository_info():
    """Example: Get detailed repository information"""
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Example: Get info about a popular repo
            result = await session.call_tool(
                "get_repository_info",
                arguments={
                    "owner": "vercel",
                    "repo": "next.js"
                }
            )
            print("Repository Info for vercel/next.js:")
            print(result.content[0].text)

async def example_get_file_contents():
    """Example: Read file contents from a repository"""
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Example 1: Read README
            result = await session.call_tool(
                "get_file_contents",
                arguments={
                    "owner": "fastapi",
                    "repo": "fastapi",
                    "path": "README.md"
                }
            )
            print("FastAPI README.md:")
            print(result.content[0].text[:500])  # First 500 chars
            print("\n" + "="*50 + "\n")
            
            # Example 2: Read a Python file
            result = await session.call_tool(
                "get_file_contents",
                arguments={
                    "owner": "pallets",
                    "repo": "flask",
                    "path": "src/flask/__init__.py"
                }
            )
            print("Flask __init__.py:")
            print(result.content[0].text[:500])  # First 500 chars
            print("\n" + "="*50 + "\n")
            
            # Example 3: Read from specific branch
            result = await session.call_tool(
                "get_file_contents",
                arguments={
                    "owner": "django",
                    "repo": "django",
                    "path": "setup.py",
                    "branch": "main"
                }
            )
            print("Django setup.py (main branch):")
            print(result.content[0].text[:500])  # First 500 chars

async def example_list_issues():
    """Example: List repository issues"""
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Example 1: Open issues
            result = await session.call_tool(
                "list_issues",
                arguments={
                    "owner": "vuejs",
                    "repo": "vue",
                    "state": "open",
                    "limit": 5
                }
            )
            print("Open issues in vuejs/vue:")
            print(result.content[0].text)
            print("\n" + "="*50 + "\n")
            
            # Example 2: Closed issues
            result = await session.call_tool(
                "list_issues",
                arguments={
                    "owner": "vuejs",
                    "repo": "vue",
                    "state": "closed",
                    "limit": 3
                }
            )
            print("Recently closed issues in vuejs/vue:")
            print(result.content[0].text)

async def example_get_user_info():
    """Example: Get GitHub user information"""
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Example 1: Famous developer
            result = await session.call_tool(
                "get_user_info",
                arguments={
                    "username": "gvanrossum"  # Python creator
                }
            )
            print("User info for Guido van Rossum:")
            print(result.content[0].text)
            print("\n" + "="*50 + "\n")
            
            # Example 2: Another user
            result = await session.call_tool(
                "get_user_info",
                arguments={
                    "username": "tj"  # TJ Holowaychuk
                }
            )
            print("User info for TJ Holowaychuk:")
            print(result.content[0].text)

async def example_list_pull_requests():
    """Example: List pull requests"""
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Example 1: Open PRs
            result = await session.call_tool(
                "list_pull_requests",
                arguments={
                    "owner": "rust-lang",
                    "repo": "rust",
                    "state": "open",
                    "limit": 5
                }
            )
            print("Open PRs in rust-lang/rust:")
            print(result.content[0].text)
            print("\n" + "="*50 + "\n")
            
            # Example 2: All PRs (including merged)
            result = await session.call_tool(
                "list_pull_requests",
                arguments={
                    "owner": "microsoft",
                    "repo": "TypeScript",
                    "state": "all",
                    "limit": 5
                }
            )
            print("Recent PRs in microsoft/TypeScript:")
            print(result.content[0].text)

async def run_all_examples():
    """Run all examples"""
    examples = [
        ("Search Repositories", example_search_repositories),
        ("Get Repository Info", example_get_repository_info),
        ("Get File Contents", example_get_file_contents),
        ("List Issues", example_list_issues),
        ("Get User Info", example_get_user_info),
        ("List Pull Requests", example_list_pull_requests),
    ]
    
    for name, example_func in examples:
        print("\n" + "="*70)
        print(f"EXAMPLE: {name}")
        print("="*70 + "\n")
        try:
            await example_func()
        except Exception as e:
            print(f"Error: {e}")
        print("\n")
        await asyncio.sleep(1)  # Rate limiting

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Run specific example
        example_name = sys.argv[1]
        examples = {
            "search": example_search_repositories,
            "repo": example_get_repository_info,
            "file": example_get_file_contents,
            "issues": example_list_issues,
            "user": example_get_user_info,
            "prs": example_list_pull_requests,
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