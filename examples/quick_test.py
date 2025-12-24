"""
Quick test script for GitHub MCP Server
Verifies that the server is working correctly with a simple test
Works on Windows, Linux, and Mac
"""

import asyncio
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

# Fix encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Server configuration - works on Windows, Linux, and Mac
SERVER_PARAMS = StdioServerParameters(
    command=sys.executable,  # Use same Python as this script (important for venv!)
    args=["-m", "github_mcp.server"],
    env=dict(os.environ),  # Inherit environment variables (now includes .env)
    cwd=str(PROJECT_ROOT)  # Set working directory so .env is found
)


async def quick_test():
    """Run a quick test to verify the server is working"""
    print("[*] Connecting to GitHub MCP Server...")
    
    try:
        async with stdio_client(SERVER_PARAMS) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("[OK] Connected to server!")
                
                # Test 1: List available tools
                print("\n[*] Available tools:")
                tools = await session.list_tools()
                for tool in tools.tools:
                    print(f"    - {tool.name}")
                
                # Test 2: Simple search
                print("\n[*] Testing search_repositories...")
                result = await session.call_tool(
                    "search_repositories",
                    arguments={
                        "query": "mcp",
                        "sort": "stars",
                        "limit": 3
                    }
                )
                print("[OK] Search completed successfully!")
                
                # Test 3: Get user info
                print("\n[*] Testing get_user_info...")
                result = await session.call_tool(
                    "get_user_info",
                    arguments={"username": "octocat"}
                )
                print("[OK] User info retrieved successfully!")
                
                print("\n" + "=" * 50)
                print("[OK] All tests passed! Server is working correctly.")
                print("=" * 50)
                return True
                
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        print("\nPossible causes:")
        print("  1. GITHUB_TOKEN not set in .env file")
        print("  2. Invalid or expired GitHub token")
        print("  3. Network connection issues")
        return False


if __name__ == "__main__":
    success = asyncio.run(quick_test())
    exit(0 if success else 1)
