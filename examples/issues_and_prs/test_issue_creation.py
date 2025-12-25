"""
Quick test script to debug issue creation
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

# Build environment
env = dict(os.environ)
src_path = str(PROJECT_ROOT / "src")
if "PYTHONPATH" in env:
    env["PYTHONPATH"] = src_path + os.pathsep + env["PYTHONPATH"]
else:
    env["PYTHONPATH"] = src_path

SERVER_PARAMS = StdioServerParameters(
    command=sys.executable,
    args=["-m", "github_mcp.server"],
    env=env,
    cwd=str(PROJECT_ROOT)
)

async def test_create_issue():
    """Test creating an issue with full debugging"""
    owner = os.getenv("GITHUB_REPO_OWNER", "archish9")
    repo = os.getenv("GITHUB_REPO_NAME", "github-mcp-testing")
    
    print("=" * 70)
    print("Testing Issue Creation")
    print("=" * 70)
    print(f"Repository: {owner}/{repo}")
    print(f"Token set: {'Yes' if os.getenv('GITHUB_TOKEN') else 'No'}")
    print()
    
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("Attempting to create issue...")
            print(f"Arguments:")
            args = {
                "owner": owner,
                "repo": repo,
                "title": "Test Issue from MCP",
                "body": "This is a test issue created via MCP server."
            }
            print(json.dumps(args, indent=2))
            print()
            
            try:
                result = await session.call_tool("create_issue", arguments=args)
                
                print("Response received:")
                print(f"  Content type: {type(result)}")
                print(f"  Has content: {hasattr(result, 'content')}")
                
                if hasattr(result, 'content') and result.content:
                    print(f"  Content length: {len(result.content)}")
                    print(f"  First content type: {type(result.content[0])}")
                    
                    if hasattr(result.content[0], 'text'):
                        text = result.content[0].text
                        print(f"  Text length: {len(text)}")
                        print(f"  Text preview: {text[:200]}...")
                        print()
                        print("Full response:")
                        print("-" * 70)
                        print(text)
                        print("-" * 70)
                        
                        # Try to parse as JSON
                        try:
                            data = json.loads(text)
                            print("\nParsed JSON:")
                            print(json.dumps(data, indent=2))
                        except json.JSONDecodeError as e:
                            print(f"\nNot valid JSON: {e}")
                    else:
                        print("  No 'text' attribute in content")
                else:
                    print("  No content in response")
                    
            except Exception as e:
                print(f"\n❌ Exception occurred: {type(e).__name__}: {e}")
                import traceback
                traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_create_issue())

