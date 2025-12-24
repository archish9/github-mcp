import os
import json
from typing import Any
import mcp.types as types
from mcp.server import Server
import mcp.server.stdio
from github import Github, GithubException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Lazy initialization of GitHub client
_github_client = None

def get_github_client():
    """Get or create GitHub client, checking for token."""
    global _github_client
    if _github_client is None:
        GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
        if not GITHUB_TOKEN:
            raise ValueError(
                "GITHUB_TOKEN environment variable is required. "
                "Please set it in your .env file or environment variables. "
                "Get a token from: https://github.com/settings/tokens"
            )
        _github_client = Github(GITHUB_TOKEN)
    return _github_client

# Create MCP server
server = Server("github-mcp")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available GitHub tools."""
    return [
        types.Tool(
            name="search_repositories",
            description="Search for GitHub repositories",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (e.g., 'language:python stars:>1000')"
                    },
                    "sort": {
                        "type": "string",
                        "description": "Sort by: stars, forks, updated",
                        "enum": ["stars", "forks", "updated"]
                    },
                    "limit": {
                        "type": "number",
                        "description": "Number of results (max 100)",
                        "default": 10
                    }
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="get_repository_info",
            description="Get detailed information about a repository",
            inputSchema={
                "type": "object",
                "properties": {
                    "owner": {
                        "type": "string",
                        "description": "Repository owner (username or organization)"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name"
                    }
                },
                "required": ["owner", "repo"]
            }
        ),
        types.Tool(
            name="get_file_contents",
            description="Get contents of a file from a repository",
            inputSchema={
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "path": {
                        "type": "string",
                        "description": "Path to the file in the repository"
                    },
                    "branch": {
                        "type": "string",
                        "description": "Branch name (default: main/master)",
                        "default": "main"
                    }
                },
                "required": ["owner", "repo", "path"]
            }
        ),
        types.Tool(
            name="list_issues",
            description="List issues for a repository",
            inputSchema={
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "state": {
                        "type": "string",
                        "enum": ["open", "closed", "all"],
                        "default": "open"
                    },
                    "limit": {
                        "type": "number",
                        "default": 10
                    }
                },
                "required": ["owner", "repo"]
            }
        ),
        types.Tool(
            name="get_user_info",
            description="Get information about a GitHub user",
            inputSchema={
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "GitHub username"
                    }
                },
                "required": ["username"]
            }
        ),
        types.Tool(
            name="list_pull_requests",
            description="List pull requests for a repository",
            inputSchema={
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "state": {
                        "type": "string",
                        "enum": ["open", "closed", "all"],
                        "default": "open"
                    },
                    "limit": {
                        "type": "number",
                        "default": 10
                    }
                },
                "required": ["owner", "repo"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution requests."""
    
    try:
        # Get GitHub client (will check for token)
        github_client = get_github_client()
        
        if name == "search_repositories":
            query = arguments.get("query")
            sort = arguments.get("sort", "stars")
            limit = min(arguments.get("limit", 10), 100)
            
            repos = github_client.search_repositories(query=query, sort=sort)
            results = []
            
            for repo in repos[:limit]:
                results.append({
                    "name": repo.full_name,
                    "description": repo.description,
                    "stars": repo.stargazers_count,
                    "forks": repo.forks_count,
                    "language": repo.language,
                    "url": repo.html_url,
                    "updated_at": repo.updated_at.isoformat()
                })
            
            return [types.TextContent(
                type="text",
                text=json.dumps(results, indent=2)
            )]
        
        elif name == "get_repository_info":
            owner = arguments.get("owner")
            repo_name = arguments.get("repo")
            
            repo = github_client.get_repo(f"{owner}/{repo_name}")
            
            info = {
                "name": repo.full_name,
                "description": repo.description,
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "watchers": repo.watchers_count,
                "language": repo.language,
                "open_issues": repo.open_issues_count,
                "default_branch": repo.default_branch,
                "created_at": repo.created_at.isoformat(),
                "updated_at": repo.updated_at.isoformat(),
                "homepage": repo.homepage,
                "topics": repo.get_topics(),
                "license": repo.license.name if repo.license else None,
                "url": repo.html_url
            }
            
            return [types.TextContent(
                type="text",
                text=json.dumps(info, indent=2)
            )]
        
        elif name == "get_file_contents":
            owner = arguments.get("owner")
            repo_name = arguments.get("repo")
            path = arguments.get("path")
            branch = arguments.get("branch", "main")
            
            repo = github_client.get_repo(f"{owner}/{repo_name}")
            
            try:
                file_content = repo.get_contents(path, ref=branch)
                content = file_content.decoded_content.decode('utf-8')
                
                return [types.TextContent(
                    type="text",
                    text=content
                )]
            except GithubException:
                # Try master branch if main doesn't exist
                file_content = repo.get_contents(path, ref="master")
                content = file_content.decoded_content.decode('utf-8')
                
                return [types.TextContent(
                    type="text",
                    text=content
                )]
        
        elif name == "list_issues":
            owner = arguments.get("owner")
            repo_name = arguments.get("repo")
            state = arguments.get("state", "open")
            limit = min(arguments.get("limit", 10), 100)
            
            repo = github_client.get_repo(f"{owner}/{repo_name}")
            issues = repo.get_issues(state=state)
            
            results = []
            for issue in issues[:limit]:
                if not issue.pull_request:  # Exclude PRs
                    results.append({
                        "number": issue.number,
                        "title": issue.title,
                        "state": issue.state,
                        "created_at": issue.created_at.isoformat(),
                        "updated_at": issue.updated_at.isoformat(),
                        "user": issue.user.login,
                        "labels": [label.name for label in issue.labels],
                        "comments": issue.comments,
                        "url": issue.html_url
                    })
            
            return [types.TextContent(
                type="text",
                text=json.dumps(results, indent=2)
            )]
        
        elif name == "get_user_info":
            username = arguments.get("username")
            user = github_client.get_user(username)
            
            info = {
                "login": user.login,
                "name": user.name,
                "bio": user.bio,
                "company": user.company,
                "location": user.location,
                "email": user.email,
                "public_repos": user.public_repos,
                "followers": user.followers,
                "following": user.following,
                "created_at": user.created_at.isoformat(),
                "url": user.html_url
            }
            
            return [types.TextContent(
                type="text",
                text=json.dumps(info, indent=2)
            )]
        
        elif name == "list_pull_requests":
            owner = arguments.get("owner")
            repo_name = arguments.get("repo")
            state = arguments.get("state", "open")
            limit = min(arguments.get("limit", 10), 100)
            
            repo = github_client.get_repo(f"{owner}/{repo_name}")
            prs = repo.get_pulls(state=state)
            
            results = []
            for pr in prs[:limit]:
                results.append({
                    "number": pr.number,
                    "title": pr.title,
                    "state": pr.state,
                    "created_at": pr.created_at.isoformat(),
                    "updated_at": pr.updated_at.isoformat(),
                    "user": pr.user.login,
                    "merged": pr.merged,
                    "url": pr.html_url
                })
            
            return [types.TextContent(
                type="text",
                text=json.dumps(results, indent=2)
            )]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
            
    except ValueError as e:
        # Handle missing token error
        return [types.TextContent(
            type="text",
            text=f"Configuration Error: {str(e)}"
        )]
    except GithubException as e:
        return [types.TextContent(
            type="text",
            text=f"GitHub API Error: {str(e)}"
        )]
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]

async def main():
    """Main entry point for the MCP server."""
    try:
        # Run the server using stdin/stdout streams
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            # Create initialization options using the server's method
            init_options = server.create_initialization_options()
            await server.run(
                read_stream,
                write_stream,
                init_options,
            )
    except Exception as e:
        # Print error to stderr so it's visible
        import sys
        print(f"Server error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        raise

if __name__ == "__main__":
    import asyncio
    import sys
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

