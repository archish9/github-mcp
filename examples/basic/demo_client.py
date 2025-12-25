"""
GitHub MCP Server Demo Client
This script demonstrates how to interact with the GitHub MCP server
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
# File is in examples/basic/, so we need to go up 3 levels
PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()

# Load environment variables from .env file
load_dotenv(PROJECT_ROOT / ".env")

# Fix encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

async def run_demo():
    """Run demonstrations of all GitHub MCP tools"""
    
    # Build environment with PYTHONPATH for package discovery
    env = dict(os.environ)
    src_path = str(PROJECT_ROOT / "src")
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] = src_path + os.pathsep + env["PYTHONPATH"]
    else:
        env["PYTHONPATH"] = src_path
    
    # Server parameters - works on Windows, Linux, and Mac
    server_params = StdioServerParameters(
        command=sys.executable,  # Use same Python as this script (important for venv!)
        args=["-m", "github_mcp.server"],
        env=env,  # Inherit environment variables with PYTHONPATH
        cwd=str(PROJECT_ROOT)  # Set working directory so .env is found
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()
            
            print("=" * 70)
            print("GitHub MCP Server - Demo Client")
            print("=" * 70)
            print()
            
            # List available tools
            print("[*] Available Tools:")
            print("-" * 70)
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"  - {tool.name}")
                print(f"    {tool.description}")
            print()
            
            # Demo 1: Search repositories
            print("\n" + "=" * 70)
            print("Demo 1: Search Repositories")
            print("=" * 70)
            result = await session.call_tool(
                "search_repositories",
                arguments={
                    "query": "language:python stars:>5000",
                    "sort": "stars",
                    "limit": 5
                }
            )
            print("Query: 'language:python stars:>5000'")
            print("Results:")
            print(result.content[0].text)
            
            # Demo 2: Get repository info
            print("\n" + "=" * 70)
            print("Demo 2: Get Repository Information")
            print("=" * 70)
            result = await session.call_tool(
                "get_repository_info",
                arguments={
                    "owner": "python",
                    "repo": "cpython"
                }
            )
            print("Repository: python/cpython")
            print("Information:")
            print(result.content[0].text)
            
            # Demo 3: Get file contents
            print("\n" + "=" * 70)
            print("Demo 3: Get File Contents")
            print("=" * 70)
            result = await session.call_tool(
                "get_file_contents",
                arguments={
                    "owner": "microsoft",
                    "repo": "vscode",
                    "path": "README.md",
                    "branch": "main"
                }
            )
            print("File: microsoft/vscode/README.md")
            print("Contents (first 500 chars):")
            content = result.content[0].text[:500]
            print(content + "...\n")
            
            # Demo 4: List issues
            print("\n" + "=" * 70)
            print("Demo 4: List Repository Issues")
            print("=" * 70)
            result = await session.call_tool(
                "list_issues",
                arguments={
                    "owner": "facebook",
                    "repo": "react",
                    "state": "open",
                    "limit": 3
                }
            )
            print("Repository: facebook/react")
            print("Open Issues (3 most recent):")
            print(result.content[0].text)
            
            # Demo 5: Get user info
            print("\n" + "=" * 70)
            print("Demo 5: Get User Information")
            print("=" * 70)
            result = await session.call_tool(
                "get_user_info",
                arguments={
                    "username": "torvalds"
                }
            )
            print("Username: torvalds")
            print("User Information:")
            print(result.content[0].text)
            
            # Demo 6: List pull requests
            print("\n" + "=" * 70)
            print("Demo 6: List Pull Requests")
            print("=" * 70)
            result = await session.call_tool(
                "list_pull_requests",
                arguments={
                    "owner": "nodejs",
                    "repo": "node",
                    "state": "open",
                    "limit": 3
                }
            )
            print("Repository: nodejs/node")
            print("Open Pull Requests (3 most recent):")
            print(result.content[0].text)
            
            print("\n" + "=" * 70)
            print("[OK] Demo completed successfully!")
            print("=" * 70)

if __name__ == "__main__":
    asyncio.run(run_demo())