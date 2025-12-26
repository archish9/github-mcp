import os
import json
import logging
from typing import Any
import mcp.types as types
from mcp.server import Server
import mcp.server.stdio
from github import Github, GithubException
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
        ),
        types.Tool(
            name="create_issue",
            description="Create a new issue in a repository",
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
                    },
                    "title": {
                        "type": "string",
                        "description": "Issue title"
                    },
                    "body": {
                        "type": "string",
                        "description": "Issue body/description"
                    },
                    "labels": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of label names to apply"
                    },
                    "assignees": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of GitHub usernames to assign"
                    },
                    "milestone": {
                        "type": "number",
                        "description": "Milestone number (optional)"
                    }
                },
                "required": ["owner", "repo", "title"]
            }
        ),
        types.Tool(
            name="create_pull_request",
            description="Create a new pull request",
            inputSchema={
                "type": "object",
                "properties": {
                    "owner": {
                        "type": "string",
                        "description": "Repository owner"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name"
                    },
                    "title": {
                        "type": "string",
                        "description": "PR title"
                    },
                    "body": {
                        "type": "string",
                        "description": "PR description"
                    },
                    "head": {
                        "type": "string",
                        "description": "Branch containing changes (e.g., 'feature-branch' or 'owner:feature-branch')"
                    },
                    "base": {
                        "type": "string",
                        "description": "Branch to merge into (default: main/master)",
                        "default": "main"
                    },
                    "draft": {
                        "type": "boolean",
                        "description": "Create as draft PR",
                        "default": False
                    }
                },
                "required": ["owner", "repo", "title", "head"]
            }
        ),
        types.Tool(
            name="add_issue_comment",
            description="Add a comment to an issue",
            inputSchema={
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "issue_number": {
                        "type": "number",
                        "description": "Issue number"
                    },
                    "body": {
                        "type": "string",
                        "description": "Comment text"
                    }
                },
                "required": ["owner", "repo", "issue_number", "body"]
            }
        ),
        types.Tool(
            name="add_pr_comment",
            description="Add a comment to a pull request",
            inputSchema={
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "pr_number": {
                        "type": "number",
                        "description": "Pull request number"
                    },
                    "body": {
                        "type": "string",
                        "description": "Comment text"
                    }
                },
                "required": ["owner", "repo", "pr_number", "body"]
            }
        ),
        types.Tool(
            name="update_issue",
            description="Update an issue (status, labels, assignees, title, body)",
            inputSchema={
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "issue_number": {
                        "type": "number",
                        "description": "Issue number"
                    },
                    "title": {
                        "type": "string",
                        "description": "New title (optional)"
                    },
                    "body": {
                        "type": "string",
                        "description": "New body (optional)"
                    },
                    "state": {
                        "type": "string",
                        "enum": ["open", "closed"],
                        "description": "Issue state"
                    },
                    "labels": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of label names (replaces existing labels)"
                    },
                    "assignees": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of GitHub usernames (replaces existing assignees)"
                    },
                    "milestone": {
                        "type": "number",
                        "description": "Milestone number (use null to remove)"
                    }
                },
                "required": ["owner", "repo", "issue_number"]
            }
        ),
        types.Tool(
            name="update_pull_request",
            description="Update a pull request (title, body, state, labels, assignees)",
            inputSchema={
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "pr_number": {
                        "type": "number",
                        "description": "Pull request number"
                    },
                    "title": {
                        "type": "string",
                        "description": "New title (optional)"
                    },
                    "body": {
                        "type": "string",
                        "description": "New body (optional)"
                    },
                    "state": {
                        "type": "string",
                        "enum": ["open", "closed"],
                        "description": "PR state"
                    },
                    "base": {
                        "type": "string",
                        "description": "Change base branch (optional)"
                    }
                },
                "required": ["owner", "repo", "pr_number"]
            }
        ),
        types.Tool(
            name="close_issue",
            description="Close an issue",
            inputSchema={
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "issue_number": {
                        "type": "number",
                        "description": "Issue number"
                    }
                },
                "required": ["owner", "repo", "issue_number"]
            }
        ),
        types.Tool(
            name="reopen_issue",
            description="Reopen a closed issue",
            inputSchema={
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "issue_number": {
                        "type": "number",
                        "description": "Issue number"
                    }
                },
                "required": ["owner", "repo", "issue_number"]
            }
        ),
        types.Tool(
            name="close_pull_request",
            description="Close a pull request",
            inputSchema={
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "pr_number": {
                        "type": "number",
                        "description": "Pull request number"
                    }
                },
                "required": ["owner", "repo", "pr_number"]
            }
        ),
        types.Tool(
            name="reopen_pull_request",
            description="Reopen a closed pull request",
            inputSchema={
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "pr_number": {
                        "type": "number",
                        "description": "Pull request number"
                    }
                },
                "required": ["owner", "repo", "pr_number"]
            }
        ),
        # Repository Statistics Tools
        types.Tool(
            name="get_contributor_stats",
            description="Get contributor statistics for a repository (commits, additions, deletions per user)",
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
                    },
                    "limit": {
                        "type": "number",
                        "description": "Number of contributors to return (default: 10)",
                        "default": 10
                    }
                },
                "required": ["owner", "repo"]
            }
        ),
        types.Tool(
            name="get_code_frequency",
            description="Get weekly code frequency statistics (additions and deletions over time)",
            inputSchema={
                "type": "object",
                "properties": {
                    "owner": {
                        "type": "string",
                        "description": "Repository owner"
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
            name="get_commit_activity",
            description="Get commit activity for the past year (weekly commit counts)",
            inputSchema={
                "type": "object",
                "properties": {
                    "owner": {
                        "type": "string",
                        "description": "Repository owner"
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
            name="get_language_breakdown",
            description="Get language breakdown for a repository (bytes per language)",
            inputSchema={
                "type": "object",
                "properties": {
                    "owner": {
                        "type": "string",
                        "description": "Repository owner"
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
            name="get_traffic_stats",
            description="Get traffic statistics (views, clones, popular paths). Requires push access to the repository.",
            inputSchema={
                "type": "object",
                "properties": {
                    "owner": {
                        "type": "string",
                        "description": "Repository owner"
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
            name="get_community_health",
            description="Get community health metrics for a repository (code of conduct, contributing guide, issue templates, etc.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "owner": {
                        "type": "string",
                        "description": "Repository owner"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name"
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
        
        elif name == "create_issue":
            owner = arguments.get("owner")
            repo_name = arguments.get("repo")
            title = arguments.get("title")
            body = arguments.get("body", "")
            labels = arguments.get("labels", [])
            assignees = arguments.get("assignees", [])
            milestone = arguments.get("milestone")
            
            # Validate inputs
            if not owner or owner == "YOUR_USERNAME":
                return [types.TextContent(
                    type="text",
                    text=json.dumps({
                        "error": "Invalid owner",
                        "message": "Please provide a valid repository owner (username or organization).",
                        "hint": "Replace 'YOUR_USERNAME' with your actual GitHub username or organization name."
                    }, indent=2)
                )]
            
            if not repo_name or repo_name == "YOUR_REPO":
                return [types.TextContent(
                    type="text",
                    text=json.dumps({
                        "error": "Invalid repository name",
                        "message": "Please provide a valid repository name.",
                        "hint": "Replace 'YOUR_REPO' with your actual repository name."
                    }, indent=2)
                )]
            
            if not title:
                return [types.TextContent(
                    type="text",
                    text=json.dumps({
                        "error": "Missing title",
                        "message": "Issue title is required."
                    }, indent=2)
                )]
            
            logger.info(f"Creating issue in {owner}/{repo_name}: {title}")
            
            try:
                repo = github_client.get_repo(f"{owner}/{repo_name}")
                
                # Check if issues are enabled
                if repo.has_issues is False:
                    return [types.TextContent(
                        type="text",
                        text=json.dumps({
                            "error": "Issues disabled",
                            "message": f"Issues are disabled for repository '{owner}/{repo_name}'.",
                            "suggestions": [
                                "Enable issues in repository settings: Settings → General → Features → Issues",
                                f"Go to: https://github.com/{owner}/{repo_name}/settings"
                            ]
                        }, indent=2)
                    )]
                
                # Create issue
                # Prepare parameters - PyGithub requires empty lists, not None
                issue_params = {
                    "title": title,
                    "body": body
                }
                
                # Only add optional parameters if they have values
                if labels:
                    issue_params["labels"] = labels
                if assignees:
                    issue_params["assignees"] = assignees
                if milestone is not None:
                    issue_params["milestone"] = milestone
                
                issue = repo.create_issue(**issue_params)
                
                logger.info(f"Successfully created issue #{issue.number}")
                
                result = {
                    "number": issue.number,
                    "title": issue.title,
                    "state": issue.state,
                    "url": issue.html_url,
                    "created_at": issue.created_at.isoformat(),
                    "labels": [label.name for label in issue.labels],
                    "assignees": [assignee.login for assignee in issue.assignees]
                }
                
                return [types.TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]
            except GithubException as e:
                error_msg = str(e) or "Unknown GitHub API error"
                status = getattr(e, 'status', None)
                logger.error(f"GitHub API error creating issue (status={status}): {error_msg}")
                
                # Extract additional error details if available
                error_data = {}
                if hasattr(e, 'data') and e.data:
                    error_data = e.data if isinstance(e.data, dict) else {}
                
                # Provide helpful error messages
                if status == 404:
                    return [types.TextContent(
                        type="text",
                        text=json.dumps({
                            "error": "Repository not found",
                            "message": f"Repository '{owner}/{repo_name}' not found or you don't have access.",
                            "details": error_msg,
                            "suggestions": [
                                f"Check that the repository exists: https://github.com/{owner}/{repo_name}",
                                "Verify you have write access to the repository",
                                "Ensure your GitHub token has the 'repo' scope",
                                "Check that owner and repo names are spelled correctly"
                            ],
                            "status": status
                        }, indent=2)
                    )]
                elif status == 403:
                    return [types.TextContent(
                        type="text",
                        text=json.dumps({
                            "error": "Permission denied",
                            "message": "You don't have permission to create issues in this repository.",
                            "details": error_msg,
                            "suggestions": [
                                "Verify you have write access to the repository",
                                "Check that your GitHub token has the 'repo' scope",
                                "For private repos, ensure your token has access",
                                "Verify the token hasn't expired or been revoked"
                            ],
                            "status": status
                        }, indent=2)
                    )]
                elif status == 422:
                    return [types.TextContent(
                        type="text",
                        text=json.dumps({
                            "error": "Validation error",
                            "message": "The request is invalid.",
                            "details": error_msg,
                            "suggestions": [
                                "Check that all labels exist in the repository",
                                "Verify assignee usernames are correct",
                                "Ensure milestone number is valid",
                                "Make sure the repository has issues enabled"
                            ],
                            "status": status
                        }, indent=2)
                    )]
                else:
                    # Generic GitHub API error
                    return [types.TextContent(
                        type="text",
                        text=json.dumps({
                            "error": "GitHub API error",
                            "message": error_msg,
                            "status": status,
                            "details": error_data if error_data else None,
                            "suggestions": [
                                "Check your GitHub token is valid and has correct permissions",
                                "Verify the repository exists and you have access",
                                "Check GitHub API status: https://www.githubstatus.com/",
                                f"Review the error details: {error_msg}"
                            ]
                        }, indent=2)
                    )]
        
        elif name == "create_pull_request":
            owner = arguments.get("owner")
            repo_name = arguments.get("repo")
            title = arguments.get("title")
            body = arguments.get("body", "")
            head = arguments.get("head")
            base = arguments.get("base", "main")
            draft = arguments.get("draft", False)
            
            # Validate inputs
            if not owner or owner == "YOUR_USERNAME":
                return [types.TextContent(
                    type="text",
                    text=json.dumps({
                        "error": "Invalid owner",
                        "message": "Please provide a valid repository owner (username or organization).",
                        "hint": "Replace 'YOUR_USERNAME' with your actual GitHub username or organization name."
                    }, indent=2)
                )]
            
            if not repo_name or repo_name == "YOUR_REPO":
                return [types.TextContent(
                    type="text",
                    text=json.dumps({
                        "error": "Invalid repository name",
                        "message": "Please provide a valid repository name.",
                        "hint": "Replace 'YOUR_REPO' with your actual repository name."
                    }, indent=2)
                )]
            
            if not title:
                return [types.TextContent(
                    type="text",
                    text=json.dumps({
                        "error": "Missing title",
                        "message": "Pull request title is required."
                    }, indent=2)
                )]
            
            if not head:
                return [types.TextContent(
                    type="text",
                    text=json.dumps({
                        "error": "Missing head branch",
                        "message": "Head branch (branch with changes) is required.",
                        "hint": "Specify the branch containing your changes, e.g., 'feature-branch' or 'fork-owner:branch-name'"
                    }, indent=2)
                )]
            
            logger.info(f"Creating pull request in {owner}/{repo_name}: {head} -> {base}")
            
            try:
                repo = github_client.get_repo(f"{owner}/{repo_name}")
                
                # Create PR
                pr = repo.create_pull(
                    title=title,
                    body=body,
                    head=head,
                    base=base,
                    draft=draft
                )
                
                logger.info(f"Successfully created PR #{pr.number}")
                
                result = {
                    "number": pr.number,
                    "title": pr.title,
                    "state": pr.state,
                    "url": pr.html_url,
                    "created_at": pr.created_at.isoformat(),
                    "head": pr.head.ref,
                    "base": pr.base.ref,
                    "draft": pr.draft,
                    "merged": pr.merged
                }
                
                return [types.TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]
            except GithubException as e:
                error_msg = str(e)
                logger.error(f"GitHub API error creating PR: {error_msg}")
                
                # Provide helpful error messages
                if e.status == 404:
                    return [types.TextContent(
                        type="text",
                        text=json.dumps({
                            "error": "Repository or branch not found",
                            "message": f"Repository '{owner}/{repo_name}' or branch '{head}' not found.",
                            "suggestions": [
                                f"Check that the repository exists: https://github.com/{owner}/{repo_name}",
                                f"Verify the branch '{head}' exists in the repository",
                                "For forks, use format: 'fork-owner:branch-name'",
                                "Ensure you have write access to the repository"
                            ]
                        }, indent=2)
                    )]
                elif e.status == 403:
                    return [types.TextContent(
                        type="text",
                        text=json.dumps({
                            "error": "Permission denied",
                            "message": "You don't have permission to create pull requests in this repository.",
                            "suggestions": [
                                "Verify you have write access to the repository",
                                "Check that your GitHub token has the 'repo' scope",
                                "For private repos, ensure your token has access"
                            ]
                        }, indent=2)
                    )]
                elif e.status == 422:
                    # Check for specific validation errors
                    if "No commits between" in error_msg or "head" in error_msg.lower():
                        return [types.TextContent(
                            type="text",
                            text=json.dumps({
                                "error": "Invalid branch configuration",
                                "message": "Cannot create pull request with these branches.",
                                "details": error_msg,
                                "suggestions": [
                                    f"Ensure branch '{head}' has commits that differ from '{base}'",
                                    f"Check that branch '{head}' exists",
                                    f"Verify branch '{base}' exists",
                                    "Make sure you've pushed commits to the head branch"
                                ]
                            }, indent=2)
                        )]
                    else:
                        return [types.TextContent(
                            type="text",
                            text=json.dumps({
                                "error": "Validation error",
                                "message": "The request is invalid.",
                                "details": error_msg,
                                "suggestions": [
                                    "Check that both branches exist",
                                    "Ensure there are differences between branches",
                                    "Verify branch names are correct"
                                ]
                            }, indent=2)
                        )]
                else:
                    return [types.TextContent(
                        type="text",
                        text=json.dumps({
                            "error": "GitHub API error",
                            "message": error_msg,
                            "status": e.status
                        }, indent=2)
                    )]
        
        elif name == "add_issue_comment":
            owner = arguments.get("owner")
            repo_name = arguments.get("repo")
            issue_number = arguments.get("issue_number")
            body = arguments.get("body")
            
            repo = github_client.get_repo(f"{owner}/{repo_name}")
            issue = repo.get_issue(issue_number)
            
            comment = issue.create_comment(body)
            
            result = {
                "id": comment.id,
                "body": comment.body,
                "user": comment.user.login,
                "created_at": comment.created_at.isoformat(),
                "url": comment.html_url
            }
            
            return [types.TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        elif name == "add_pr_comment":
            owner = arguments.get("owner")
            repo_name = arguments.get("repo")
            pr_number = arguments.get("pr_number")
            body = arguments.get("body")
            
            repo = github_client.get_repo(f"{owner}/{repo_name}")
            pr = repo.get_pull(pr_number)
            
            comment = pr.create_issue_comment(body)
            
            result = {
                "id": comment.id,
                "body": comment.body,
                "user": comment.user.login,
                "created_at": comment.created_at.isoformat(),
                "url": comment.html_url
            }
            
            return [types.TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        elif name == "update_issue":
            owner = arguments.get("owner")
            repo_name = arguments.get("repo")
            issue_number = arguments.get("issue_number")
            title = arguments.get("title")
            body = arguments.get("body")
            state = arguments.get("state")
            labels = arguments.get("labels")
            assignees = arguments.get("assignees")
            milestone = arguments.get("milestone")
            
            repo = github_client.get_repo(f"{owner}/{repo_name}")
            issue = repo.get_issue(issue_number)
            
            # Build update parameters
            update_params = {}
            if title is not None:
                update_params["title"] = title
            if body is not None:
                update_params["body"] = body
            if state is not None:
                update_params["state"] = state
            if labels is not None:
                update_params["labels"] = labels
            if assignees is not None:
                update_params["assignees"] = assignees
            if milestone is not None:
                update_params["milestone"] = milestone
            
            # Update issue
            issue.edit(**update_params)
            
            # Refresh to get updated data
            issue = repo.get_issue(issue_number)
            
            result = {
                "number": issue.number,
                "title": issue.title,
                "state": issue.state,
                "url": issue.html_url,
                "updated_at": issue.updated_at.isoformat(),
                "labels": [label.name for label in issue.labels],
                "assignees": [assignee.login for assignee in issue.assignees]
            }
            
            return [types.TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        elif name == "update_pull_request":
            owner = arguments.get("owner")
            repo_name = arguments.get("repo")
            pr_number = arguments.get("pr_number")
            title = arguments.get("title")
            body = arguments.get("body")
            state = arguments.get("state")
            base = arguments.get("base")
            
            repo = github_client.get_repo(f"{owner}/{repo_name}")
            pr = repo.get_pull(pr_number)
            
            # Build update parameters
            update_params = {}
            if title is not None:
                update_params["title"] = title
            if body is not None:
                update_params["body"] = body
            if state is not None:
                update_params["state"] = state
            if base is not None:
                update_params["base"] = base
            
            # Update PR
            pr.edit(**update_params)
            
            # Refresh to get updated data
            pr = repo.get_pull(pr_number)
            
            result = {
                "number": pr.number,
                "title": pr.title,
                "state": pr.state,
                "url": pr.html_url,
                "updated_at": pr.updated_at.isoformat(),
                "head": pr.head.ref,
                "base": pr.base.ref,
                "merged": pr.merged
            }
            
            return [types.TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        elif name == "close_issue":
            owner = arguments.get("owner")
            repo_name = arguments.get("repo")
            issue_number = arguments.get("issue_number")
            
            repo = github_client.get_repo(f"{owner}/{repo_name}")
            issue = repo.get_issue(issue_number)
            issue.edit(state="closed")
            
            result = {
                "number": issue.number,
                "title": issue.title,
                "state": "closed",
                "url": issue.html_url,
                "closed_at": issue.closed_at.isoformat() if issue.closed_at else None
            }
            
            return [types.TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        elif name == "reopen_issue":
            owner = arguments.get("owner")
            repo_name = arguments.get("repo")
            issue_number = arguments.get("issue_number")
            
            repo = github_client.get_repo(f"{owner}/{repo_name}")
            issue = repo.get_issue(issue_number)
            issue.edit(state="open")
            
            result = {
                "number": issue.number,
                "title": issue.title,
                "state": "open",
                "url": issue.html_url
            }
            
            return [types.TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        elif name == "close_pull_request":
            owner = arguments.get("owner")
            repo_name = arguments.get("repo")
            pr_number = arguments.get("pr_number")
            
            repo = github_client.get_repo(f"{owner}/{repo_name}")
            pr = repo.get_pull(pr_number)
            pr.edit(state="closed")
            
            result = {
                "number": pr.number,
                "title": pr.title,
                "state": "closed",
                "url": pr.html_url,
                "closed_at": pr.closed_at.isoformat() if pr.closed_at else None
            }
            
            return [types.TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        elif name == "reopen_pull_request":
            owner = arguments.get("owner")
            repo_name = arguments.get("repo")
            pr_number = arguments.get("pr_number")
            
            repo = github_client.get_repo(f"{owner}/{repo_name}")
            pr = repo.get_pull(pr_number)
            pr.edit(state="open")
            
            result = {
                "number": pr.number,
                "title": pr.title,
                "state": "open",
                "url": pr.html_url
            }
            
            return [types.TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        # Repository Statistics Tools
        elif name == "get_contributor_stats":
            owner = arguments.get("owner")
            repo_name = arguments.get("repo")
            limit = min(arguments.get("limit", 10), 100)
            
            repo = github_client.get_repo(f"{owner}/{repo_name}")
            stats = repo.get_stats_contributors()
            
            # Stats may be None if GitHub is calculating them
            if stats is None:
                return [types.TextContent(
                    type="text",
                    text=json.dumps({
                        "message": "Statistics are being calculated by GitHub. Please try again in a few seconds.",
                        "status": "pending"
                    }, indent=2)
                )]
            
            results = []
            # Sort by total commits (descending) and limit
            sorted_stats = sorted(stats, key=lambda x: x.total, reverse=True)[:limit]
            
            for contributor in sorted_stats:
                total_additions = sum(week.a for week in contributor.weeks)
                total_deletions = sum(week.d for week in contributor.weeks)
                
                results.append({
                    "author": contributor.author.login if contributor.author else "Unknown",
                    "total_commits": contributor.total,
                    "total_additions": total_additions,
                    "total_deletions": total_deletions,
                    "weeks_active": len([w for w in contributor.weeks if w.c > 0])
                })
            
            return [types.TextContent(
                type="text",
                text=json.dumps({
                    "repository": f"{owner}/{repo_name}",
                    "total_contributors": len(stats),
                    "showing": len(results),
                    "contributors": results
                }, indent=2)
            )]
        
        elif name == "get_code_frequency":
            owner = arguments.get("owner")
            repo_name = arguments.get("repo")
            
            repo = github_client.get_repo(f"{owner}/{repo_name}")
            stats = repo.get_stats_code_frequency()
            
            # Stats may be None if GitHub is calculating them
            if stats is None:
                return [types.TextContent(
                    type="text",
                    text=json.dumps({
                        "message": "Statistics are being calculated by GitHub. Please try again in a few seconds.",
                        "status": "pending"
                    }, indent=2)
                )]
            
            # Get last 12 weeks for summary
            from datetime import datetime
            results = []
            for week in stats[-12:]:
                results.append({
                    "week_start": datetime.fromtimestamp(week.week).isoformat(),
                    "additions": week.additions,
                    "deletions": week.deletions
                })
            
            total_additions = sum(w.additions for w in stats)
            total_deletions = sum(w.deletions for w in stats)
            
            return [types.TextContent(
                type="text",
                text=json.dumps({
                    "repository": f"{owner}/{repo_name}",
                    "total_additions": total_additions,
                    "total_deletions": total_deletions,
                    "weeks_tracked": len(stats),
                    "last_12_weeks": results
                }, indent=2)
            )]
        
        elif name == "get_commit_activity":
            owner = arguments.get("owner")
            repo_name = arguments.get("repo")
            
            repo = github_client.get_repo(f"{owner}/{repo_name}")
            stats = repo.get_stats_commit_activity()
            
            # Stats may be None if GitHub is calculating them
            if stats is None:
                return [types.TextContent(
                    type="text",
                    text=json.dumps({
                        "message": "Statistics are being calculated by GitHub. Please try again in a few seconds.",
                        "status": "pending"
                    }, indent=2)
                )]
            
            from datetime import datetime
            results = []
            for week in stats[-12:]:  # Last 12 weeks
                results.append({
                    "week_start": datetime.fromtimestamp(week.week).isoformat(),
                    "total_commits": week.total,
                    "days": week.days  # List of commits per day (Sun-Sat)
                })
            
            total_commits = sum(w.total for w in stats)
            
            return [types.TextContent(
                type="text",
                text=json.dumps({
                    "repository": f"{owner}/{repo_name}",
                    "total_commits_year": total_commits,
                    "weeks_tracked": len(stats),
                    "last_12_weeks": results
                }, indent=2)
            )]
        
        elif name == "get_language_breakdown":
            owner = arguments.get("owner")
            repo_name = arguments.get("repo")
            
            repo = github_client.get_repo(f"{owner}/{repo_name}")
            languages = repo.get_languages()
            
            # Calculate percentages
            total_bytes = sum(languages.values())
            results = []
            
            for lang, bytes_count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
                percentage = (bytes_count / total_bytes * 100) if total_bytes > 0 else 0
                results.append({
                    "language": lang,
                    "bytes": bytes_count,
                    "percentage": round(percentage, 2)
                })
            
            return [types.TextContent(
                type="text",
                text=json.dumps({
                    "repository": f"{owner}/{repo_name}",
                    "total_bytes": total_bytes,
                    "languages": results
                }, indent=2)
            )]
        
        elif name == "get_traffic_stats":
            owner = arguments.get("owner")
            repo_name = arguments.get("repo")
            
            try:
                repo = github_client.get_repo(f"{owner}/{repo_name}")
                
                # Get views
                views = repo.get_views_traffic()
                
                # Get clones
                clones = repo.get_clones_traffic()
                
                # Get top paths
                top_paths = repo.get_top_paths()
                
                # Get top referrers
                top_referrers = repo.get_top_referrers()
                
                paths_list = [{"path": p.path, "title": p.title, "views": p.count, "unique_visitors": p.uniques} for p in top_paths]
                referrers_list = [{"referrer": r.referrer, "views": r.count, "unique_visitors": r.uniques} for r in top_referrers]
                
                return [types.TextContent(
                    type="text",
                    text=json.dumps({
                        "repository": f"{owner}/{repo_name}",
                        "views": {
                            "total": views.get("count", 0),
                            "unique": views.get("uniques", 0)
                        },
                        "clones": {
                            "total": clones.get("count", 0),
                            "unique": clones.get("uniques", 0)
                        },
                        "top_paths": paths_list[:10],
                        "top_referrers": referrers_list[:10]
                    }, indent=2)
                )]
            except GithubException as e:
                if e.status == 403:
                    return [types.TextContent(
                        type="text",
                        text=json.dumps({
                            "error": "Access denied",
                            "message": "Traffic statistics require push access to the repository.",
                            "suggestions": [
                                "Ensure you have push (write) access to this repository",
                                "Use your own repository for traffic statistics",
                                "Check that your token has the 'repo' scope"
                            ]
                        }, indent=2)
                    )]
                raise
        
        elif name == "get_community_health":
            owner = arguments.get("owner")
            repo_name = arguments.get("repo")
            
            repo = github_client.get_repo(f"{owner}/{repo_name}")
            
            # Try to get community profile
            try:
                profile = repo.get_community_profile()
                
                # Extract file info
                def get_file_url(file_info):
                    if file_info and hasattr(file_info, 'url'):
                        return file_info.url
                    elif file_info and isinstance(file_info, dict):
                        return file_info.get('url') or file_info.get('html_url')
                    return None
                
                files = profile.get("files", {})
                
                result = {
                    "repository": f"{owner}/{repo_name}",
                    "health_percentage": profile.get("health_percentage", 0),
                    "description": profile.get("description"),
                    "documentation": profile.get("documentation"),
                    "files": {
                        "code_of_conduct": get_file_url(files.get("code_of_conduct")),
                        "contributing": get_file_url(files.get("contributing")),
                        "issue_template": get_file_url(files.get("issue_template")),
                        "pull_request_template": get_file_url(files.get("pull_request_template")),
                        "license": get_file_url(files.get("license")),
                        "readme": get_file_url(files.get("readme"))
                    },
                    "updated_at": profile.get("updated_at")
                }
                
                return [types.TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]
            except (GithubException, AttributeError) as e:
                # Fallback: gather basic community info manually
                # This handles both API errors and cases where get_community_profile isn't available
                result = {
                    "repository": f"{owner}/{repo_name}",
                    "description": repo.description,
                    "has_issues": repo.has_issues,
                    "has_wiki": repo.has_wiki,
                    "has_downloads": repo.has_downloads,
                    "has_projects": repo.has_projects,
                    "license": repo.license.name if repo.license else None,
                    "homepage": repo.homepage,
                    "default_branch": repo.default_branch,
                    "open_issues_count": repo.open_issues_count,
                    "stargazers_count": repo.stargazers_count,
                    "watchers_count": repo.watchers_count,
                    "forks_count": repo.forks_count,
                    "topics": repo.get_topics(),
                    "url": repo.html_url
                }
                
                return [types.TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
            
    except ValueError as e:
        # Handle missing token error
        logger.error(f"Configuration error: {str(e)}")
        return [types.TextContent(
            type="text",
            text=json.dumps({
                "error": "Configuration Error",
                "message": str(e),
                "suggestions": [
                    "Set GITHUB_TOKEN in your .env file",
                    "Get a token from: https://github.com/settings/tokens",
                    "Ensure the token has the 'repo' or 'public_repo' scope"
                ]
            }, indent=2)
        )]
    except GithubException as e:
        logger.error(f"GitHub API error: {str(e)}")
        return [types.TextContent(
            type="text",
            text=json.dumps({
                "error": "GitHub API Error",
                "message": str(e),
                "status": e.status if hasattr(e, 'status') else None
            }, indent=2)
        )]
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return [types.TextContent(
            type="text",
            text=json.dumps({
                "error": "Unexpected Error",
                "message": str(e),
                "type": type(e).__name__
            }, indent=2)
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

