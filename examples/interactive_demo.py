"""
Interactive GitHub MCP Demo
Allows you to test different tools interactively
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

# Fix encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Build environment with PYTHONPATH for package discovery
def get_server_env():
    env = dict(os.environ)
    src_path = str(PROJECT_ROOT / "src")
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] = src_path + os.pathsep + env["PYTHONPATH"]
    else:
        env["PYTHONPATH"] = src_path
    return env

# Server configuration - works on Windows, Linux, and Mac
SERVER_PARAMS = StdioServerParameters(
    command=sys.executable,  # Use same Python as this script (important for venv!)
    args=["-m", "github_mcp.server"],
    env=get_server_env(),  # Inherit environment variables with PYTHONPATH
    cwd=str(PROJECT_ROOT)  # Set working directory so .env is found
)

def print_menu():
    """Print the interactive menu"""
    print("\n" + "="*70)
    print("GitHub MCP Server - Interactive Demo")
    print("="*70)
    print("1. Search Repositories")
    print("2. Get Repository Info")
    print("3. Get File Contents")
    print("4. List Issues")
    print("5. Get User Info")
    print("6. List Pull Requests")
    print("0. Exit")
    print("="*70)

async def interactive_search_repos(session):
    """Interactive repository search"""
    print("\n--- Search Repositories ---")
    query = input("Enter search query (e.g., 'language:python stars:>1000'): ")
    sort = input("Sort by (stars/forks/updated) [stars]: ").strip() or "stars"
    limit = input("Number of results (1-100) [10]: ").strip() or "10"
    
    result = await session.call_tool(
        "search_repositories",
        arguments={
            "query": query,
            "sort": sort,
            "limit": int(limit)
        }
    )
    
    print("\n--- Results ---")
    data = json.loads(result.content[0].text)
    for i, repo in enumerate(data, 1):
        print(f"\n{i}. {repo['name']}")
        print(f"   [*] {repo['stars']} stars | {repo['forks']} forks")
        print(f"   [i] {repo['description']}")
        print(f"   [>] {repo['url']}")

async def interactive_repo_info(session):
    """Interactive repository info"""
    print("\n--- Get Repository Info ---")
    owner = input("Enter repository owner: ")
    repo = input("Enter repository name: ")
    
    result = await session.call_tool(
        "get_repository_info",
        arguments={
            "owner": owner,
            "repo": repo
        }
    )
    
    print("\n--- Repository Information ---")
    data = json.loads(result.content[0].text)
    print(f"Name: {data['name']}")
    print(f"Description: {data['description']}")
    print(f"[*] Stars: {data['stars']}")
    print(f"[*] Forks: {data['forks']}")
    print(f"[*] Watchers: {data['watchers']}")
    print(f"Language: {data['language']}")
    print(f"Open Issues: {data['open_issues']}")
    print(f"License: {data['license']}")
    print(f"Topics: {', '.join(data['topics'])}")
    print(f"[>] URL: {data['url']}")

async def interactive_file_contents(session):
    """Interactive file contents"""
    print("\n--- Get File Contents ---")
    owner = input("Enter repository owner: ")
    repo = input("Enter repository name: ")
    path = input("Enter file path (e.g., README.md): ")
    branch = input("Enter branch [main]: ").strip() or "main"
    
    result = await session.call_tool(
        "get_file_contents",
        arguments={
            "owner": owner,
            "repo": repo,
            "path": path,
            "branch": branch
        }
    )
    
    print("\n--- File Contents ---")
    content = result.content[0].text
    print(content[:1000])  # Show first 1000 characters
    if len(content) > 1000:
        print(f"\n... ({len(content) - 1000} more characters)")
        show_more = input("\nShow full content? (y/n): ").lower()
        if show_more == 'y':
            print(content)

async def interactive_list_issues(session):
    """Interactive issue listing"""
    print("\n--- List Issues ---")
    owner = input("Enter repository owner: ")
    repo = input("Enter repository name: ")
    state = input("State (open/closed/all) [open]: ").strip() or "open"
    limit = input("Number of issues (1-100) [10]: ").strip() or "10"
    
    result = await session.call_tool(
        "list_issues",
        arguments={
            "owner": owner,
            "repo": repo,
            "state": state,
            "limit": int(limit)
        }
    )
    
    print(f"\n--- {state.capitalize()} Issues ---")
    data = json.loads(result.content[0].text)
    for i, issue in enumerate(data, 1):
        print(f"\n{i}. #{issue['number']}: {issue['title']}")
        print(f"   [@] {issue['user']} | {issue['comments']} comments")
        print(f"   [#] Labels: {', '.join(issue['labels'])}")
        print(f"   [>] {issue['url']}")

async def interactive_user_info(session):
    """Interactive user info"""
    print("\n--- Get User Info ---")
    username = input("Enter GitHub username: ")
    
    result = await session.call_tool(
        "get_user_info",
        arguments={
            "username": username
        }
    )
    
    print("\n--- User Information ---")
    data = json.loads(result.content[0].text)
    print(f"Username: {data['login']}")
    print(f"Name: {data['name']}")
    print(f"Bio: {data['bio']}")
    print(f"Company: {data['company']}")
    print(f"Location: {data['location']}")
    print(f"[#] Public Repos: {data['public_repos']}")
    print(f"[@] Followers: {data['followers']}")
    print(f"Following: {data['following']}")
    print(f"[>] Profile: {data['url']}")

async def interactive_list_prs(session):
    """Interactive PR listing"""
    print("\n--- List Pull Requests ---")
    owner = input("Enter repository owner: ")
    repo = input("Enter repository name: ")
    state = input("State (open/closed/all) [open]: ").strip() or "open"
    limit = input("Number of PRs (1-100) [10]: ").strip() or "10"
    
    result = await session.call_tool(
        "list_pull_requests",
        arguments={
            "owner": owner,
            "repo": repo,
            "state": state,
            "limit": int(limit)
        }
    )
    
    print(f"\n--- {state.capitalize()} Pull Requests ---")
    data = json.loads(result.content[0].text)
    for i, pr in enumerate(data, 1):
        merged_status = "[OK] Merged" if pr['merged'] else "[..] Not merged"
        print(f"\n{i}. #{pr['number']}: {pr['title']}")
        print(f"   [@] {pr['user']} | {merged_status}")
        print(f"   [>] {pr['url']}")

async def main():
    """Main interactive loop"""
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("\n[OK] Connected to GitHub MCP Server!")
            
            while True:
                print_menu()
                choice = input("\nSelect an option (0-6): ").strip()
                
                try:
                    if choice == "0":
                        print("\n[*] Goodbye!")
                        break
                    elif choice == "1":
                        await interactive_search_repos(session)
                    elif choice == "2":
                        await interactive_repo_info(session)
                    elif choice == "3":
                        await interactive_file_contents(session)
                    elif choice == "4":
                        await interactive_list_issues(session)
                    elif choice == "5":
                        await interactive_user_info(session)
                    elif choice == "6":
                        await interactive_list_prs(session)
                    else:
                        print("[!] Invalid option. Please try again.")
                    
                    input("\nPress Enter to continue...")
                    
                except Exception as e:
                    print(f"\n[!] Error: {e}")
                    input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n[*] Interrupted. Goodbye!")