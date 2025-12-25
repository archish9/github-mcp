"""
GitHub MCP Server - Issues and PRs Demo
This script demonstrates how to create and manage issues and pull requests
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

# Fix encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

async def run_demo():
    """Run demonstrations of Issues and PRs features"""
    
    # Build environment with PYTHONPATH for package discovery
    env = dict(os.environ)
    src_path = str(PROJECT_ROOT / "src")
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] = src_path + os.pathsep + env["PYTHONPATH"]
    else:
        env["PYTHONPATH"] = src_path
    
    # Server parameters
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "github_mcp.server"],
        env=env,
        cwd=str(PROJECT_ROOT)
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("=" * 70)
            print("GitHub MCP Server - Issues and PRs Demo")
            print("=" * 70)
            print()
            print("⚠️  NOTE: This demo requires a repository where you have write access.")
            print("   Replace 'YOUR_USERNAME' and 'YOUR_REPO' with your actual values.")
            print()
            
            # Get user input for repository
            print("Enter repository details:")
            owner = input("  Owner (username or org): ").strip() or "YOUR_USERNAME"
            repo = input("  Repository name: ").strip() or "YOUR_REPO"
            print()
            
            # Demo 1: Create an issue
            print("\n" + "=" * 70)
            print("Demo 1: Create an Issue")
            print("=" * 70)
            print("Creating issue: 'Demo: Test Issue from MCP'")
            try:
                result = await session.call_tool(
                    "create_issue",
                    arguments={
                        "owner": owner,
                        "repo": repo,
                        "title": "Demo: Test Issue from MCP",
                        "body": "This is a test issue created using the GitHub MCP server.\n\n**Features demonstrated:**\n- Issue creation\n- Labels\n- Assignees",
                        "labels": ["documentation", "enhancement"],
                        "assignees": []  # Add your username here if you want
                    }
                )
                issue_data = json.loads(result.content[0].text)
                
                # Check if response is an error
                if isinstance(issue_data, dict) and "error" in issue_data:
                    print(f"❌ Error creating issue: {issue_data.get('message', 'Unknown error')}")
                    if "suggestions" in issue_data:
                        for suggestion in issue_data["suggestions"]:
                            print(f"   - {suggestion}")
                    issue_number = None
                elif "number" in issue_data:
                    print("✅ Issue created successfully!")
                    print(f"Issue #{issue_data['number']}: {issue_data['title']}")
                    print(f"URL: {issue_data['url']}")
                    print(f"State: {issue_data['state']}")
                    print(f"Labels: {', '.join(issue_data.get('labels', []))}")
                    issue_number = issue_data['number']
                else:
                    print("⚠️  Unexpected response format:")
                    print(json.dumps(issue_data, indent=2))
                    issue_number = None
            except KeyError as e:
                print(f"❌ Error accessing issue data: Missing key '{e}'")
                try:
                    issue_data = json.loads(result.content[0].text)
                    print("Response data:")
                    print(json.dumps(issue_data, indent=2))
                except:
                    pass
                issue_number = None
            except Exception as e:
                print(f"❌ Error creating issue: {e}")
                print("   (This is expected if you don't have write access to the repo)")
                issue_number = None
            
            # Demo 2: Add comment to issue
            if issue_number:
                print("\n" + "=" * 70)
                print("Demo 2: Add Comment to Issue")
                print("=" * 70)
                print(f"Adding comment to issue #{issue_number}")
                try:
                    result = await session.call_tool(
                        "add_issue_comment",
                        arguments={
                            "owner": owner,
                            "repo": repo,
                            "issue_number": issue_number,
                            "body": "This is a test comment added via the MCP server! 🚀"
                        }
                    )
                    comment_data = json.loads(result.content[0].text)
                    print("✅ Comment added successfully!")
                    print(f"Comment ID: {comment_data['id']}")
                    print(f"Comment by: {comment_data['user']}")
                    print(f"URL: {comment_data['url']}")
                except Exception as e:
                    print(f"❌ Error adding comment: {e}")
            
            # Demo 3: Update issue
            if issue_number:
                print("\n" + "=" * 70)
                print("Demo 3: Update Issue")
                print("=" * 70)
                print(f"Updating issue #{issue_number}")
                try:
                    result = await session.call_tool(
                        "update_issue",
                        arguments={
                            "owner": owner,
                            "repo": repo,
                            "issue_number": issue_number,
                            "labels": ["documentation", "enhancement", "demo"],
                            "body": "This issue has been updated via the MCP server!\n\n**Updated features:**\n- Modified body\n- Added new label"
                        }
                    )
                    issue_data = json.loads(result.content[0].text)
                    print("✅ Issue updated successfully!")
                    print(f"Labels: {', '.join(issue_data['labels'])}")
                except Exception as e:
                    print(f"❌ Error updating issue: {e}")
            
            # Demo 4: Create Pull Request
            print("\n" + "=" * 70)
            print("Demo 4: Create Pull Request")
            print("=" * 70)
            print("⚠️  NOTE: To create a PR, you need a branch with changes.")
            print("   This demo assumes you have a branch called 'feature-branch'")
            print()
            head_branch = input("  Head branch (branch with changes): ").strip() or "feature-branch"
            base_branch = input("  Base branch (target branch): ").strip() or "main"
            
            try:
                result = await session.call_tool(
                    "create_pull_request",
                    arguments={
                        "owner": owner,
                        "repo": repo,
                        "title": "Demo: Test PR from MCP",
                        "body": "This is a test pull request created using the GitHub MCP server.\n\n**Changes:**\n- Created via MCP\n- Demonstrates PR creation",
                        "head": head_branch,
                        "base": base_branch,
                        "draft": False
                    }
                )
                pr_data = json.loads(result.content[0].text)
                
                # Check if response is an error
                if isinstance(pr_data, dict) and "error" in pr_data:
                    print(f"❌ Error creating PR: {pr_data.get('message', 'Unknown error')}")
                    if "suggestions" in pr_data:
                        print("   Suggestions:")
                        for suggestion in pr_data["suggestions"]:
                            print(f"   - {suggestion}")
                    pr_number = None
                elif "number" in pr_data:
                    print("✅ Pull request created successfully!")
                    print(f"PR #{pr_data['number']}: {pr_data['title']}")
                    print(f"URL: {pr_data['url']}")
                    print(f"State: {pr_data['state']}")
                    print(f"Head: {pr_data['head']} → Base: {pr_data['base']}")
                    pr_number = pr_data['number']
                else:
                    print("⚠️  Unexpected response format:")
                    print(json.dumps(pr_data, indent=2))
                    pr_number = None
            except KeyError as e:
                print(f"❌ Error accessing PR data: Missing key '{e}'")
                print("   Response data:")
                try:
                    pr_data = json.loads(result.content[0].text)
                    print(json.dumps(pr_data, indent=2))
                except:
                    print(result.content[0].text)
                pr_number = None
            except Exception as e:
                print(f"❌ Error creating PR: {e}")
                print("   (This is expected if the branch doesn't exist or you don't have write access)")
                import traceback
                traceback.print_exc()
                pr_number = None
            
            # Demo 5: Add comment to PR
            if pr_number:
                print("\n" + "=" * 70)
                print("Demo 5: Add Comment to Pull Request")
                print("=" * 70)
                print(f"Adding comment to PR #{pr_number}")
                try:
                    result = await session.call_tool(
                        "add_pr_comment",
                        arguments={
                            "owner": owner,
                            "repo": repo,
                            "pr_number": pr_number,
                            "body": "Great work! This PR was created via MCP. 👍"
                        }
                    )
                    comment_data = json.loads(result.content[0].text)
                    print("✅ Comment added successfully!")
                    print(f"Comment ID: {comment_data['id']}")
                    print(f"Comment by: {comment_data['user']}")
                except Exception as e:
                    print(f"❌ Error adding comment: {e}")
            
            # Demo 6: Update PR
            if pr_number:
                print("\n" + "=" * 70)
                print("Demo 6: Update Pull Request")
                print("=" * 70)
                print(f"Updating PR #{pr_number}")
                try:
                    result = await session.call_tool(
                        "update_pull_request",
                        arguments={
                            "owner": owner,
                            "repo": repo,
                            "pr_number": pr_number,
                            "body": "This PR has been updated via the MCP server!\n\n**Updated:**\n- Modified description\n- Ready for review"
                        }
                    )
                    pr_data = json.loads(result.content[0].text)
                    print("✅ PR updated successfully!")
                    print(f"State: {pr_data['state']}")
                except Exception as e:
                    print(f"❌ Error updating PR: {e}")
            
            # Demo 7: Close issue
            if issue_number:
                print("\n" + "=" * 70)
                print("Demo 7: Close Issue")
                print("=" * 70)
                print(f"Closing issue #{issue_number}")
                response = input("  Do you want to close the issue? (y/n): ").strip().lower()
                if response == 'y':
                    try:
                        result = await session.call_tool(
                            "close_issue",
                            arguments={
                                "owner": owner,
                                "repo": repo,
                                "issue_number": issue_number
                            }
                        )
                        issue_data = json.loads(result.content[0].text)
                        print("✅ Issue closed successfully!")
                        print(f"State: {issue_data['state']}")
                        
                        # Demo 8: Reopen issue
                        print("\n" + "=" * 70)
                        print("Demo 8: Reopen Issue")
                        print("=" * 70)
                        response = input("  Do you want to reopen the issue? (y/n): ").strip().lower()
                        if response == 'y':
                            try:
                                result = await session.call_tool(
                                    "reopen_issue",
                                    arguments={
                                        "owner": owner,
                                        "repo": repo,
                                        "issue_number": issue_number
                                    }
                                )
                                issue_data = json.loads(result.content[0].text)
                                print("✅ Issue reopened successfully!")
                                print(f"State: {issue_data['state']}")
                            except Exception as e:
                                print(f"❌ Error reopening issue: {e}")
                    except Exception as e:
                        print(f"❌ Error closing issue: {e}")
                else:
                    print("Skipped closing issue.")
            
            # Demo 9: Close PR
            if pr_number:
                print("\n" + "=" * 70)
                print("Demo 9: Close Pull Request")
                print("=" * 70)
                print(f"Closing PR #{pr_number}")
                response = input("  Do you want to close the PR? (y/n): ").strip().lower()
                if response == 'y':
                    try:
                        result = await session.call_tool(
                            "close_pull_request",
                            arguments={
                                "owner": owner,
                                "repo": repo,
                                "pr_number": pr_number
                            }
                        )
                        pr_data = json.loads(result.content[0].text)
                        print("✅ PR closed successfully!")
                        print(f"State: {pr_data['state']}")
                        
                        # Demo 10: Reopen PR
                        print("\n" + "=" * 70)
                        print("Demo 10: Reopen Pull Request")
                        print("=" * 70)
                        response = input("  Do you want to reopen the PR? (y/n): ").strip().lower()
                        if response == 'y':
                            try:
                                result = await session.call_tool(
                                    "reopen_pull_request",
                                    arguments={
                                        "owner": owner,
                                        "repo": repo,
                                        "pr_number": pr_number
                                    }
                                )
                                pr_data = json.loads(result.content[0].text)
                                print("✅ PR reopened successfully!")
                                print(f"State: {pr_data['state']}")
                            except Exception as e:
                                print(f"❌ Error reopening PR: {e}")
                    except Exception as e:
                        print(f"❌ Error closing PR: {e}")
                else:
                    print("Skipped closing PR.")
            
            print("\n" + "=" * 70)
            print("[OK] Demo completed!")
            print("=" * 70)
            print()
            print("💡 Tip: Check your GitHub repository to see the created issues and PRs!")

if __name__ == "__main__":
    asyncio.run(run_demo())

