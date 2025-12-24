# GitHub MCP Examples

This directory contains demonstration scripts showing how to use the GitHub MCP server.

## Prerequisites

1. Install the MCP Python SDK:
```bash
pip install mcp
```

2. Make sure the GitHub MCP server is installed:
```bash
pip install -e ..
```

3. Set up your GitHub token in a `.env` file:
```
GITHUB_TOKEN=your_github_personal_access_token
```

## Available Demo Scripts

### 1. `demo_client.py` - Complete Demo
Runs through all available tools with pre-configured examples.

**Usage:**
```bash
python examples/demo_client.py
```

**What it does:**
- Lists all available tools
- Searches for Python repositories
- Gets info about python/cpython
- Reads README from microsoft/vscode
- Lists issues from facebook/react
- Gets user info for torvalds
- Lists PRs from nodejs/node

---

### 2. `individual_examples.py` - Individual Tool Examples
Contains separate functions for each tool with multiple examples.

**Usage:**
```bash
# Run all examples
python examples/individual_examples.py

# Run specific example
python examples/individual_examples.py search    # Search repositories
python examples/individual_examples.py repo      # Repository info
python examples/individual_examples.py file      # File contents
python examples/individual_examples.py issues    # List issues
python examples/individual_examples.py user      # User info
python examples/individual_examples.py prs       # Pull requests
```

**Examples included:**
- **Search**: Python repos, ML repos, recent JavaScript repos
- **Repo Info**: vercel/next.js details
- **Files**: README.md, Python files, specific branches
- **Issues**: Open and closed issues
- **Users**: Famous developers (gvanrossum, tj)
- **PRs**: Open and merged pull requests

---

### 3. `interactive_demo.py` - Interactive Explorer
Interactive menu-driven demo where you can test with your own inputs.

**Usage:**
```bash
python examples/interactive_demo.py
```

**Features:**
- Menu-driven interface
- Enter your own parameters
- Formatted, readable output
- Error handling

**Example session:**
```
Select an option (0-6): 1
Enter search query: language:rust stars:>5000
Sort by (stars/forks/updated): stars
Number of results (1-100): 5
```

---

## Example Outputs

### Search Repositories
```json
[
  {
    "name": "python/cpython",
    "description": "The Python programming language",
    "stars": 58432,
    "forks": 29843,
    "language": "Python",
    "url": "https://github.com/python/cpython"
  }
]
```

### Get Repository Info
```json
{
  "name": "vercel/next.js",
  "description": "The React Framework",
  "stars": 120543,
  "forks": 25876,
  "language": "TypeScript",
  "topics": ["react", "nextjs", "framework"],
  "license": "MIT License"
}
```

### List Issues
```json
[
  {
    "number": 12345,
    "title": "Bug: Something is broken",
    "state": "open",
    "user": "octocat",
    "labels": ["bug", "help wanted"],
    "comments": 5
  }
]
```

---

## Customizing Examples

You can easily modify the scripts for your needs:

```python
# Example: Search your own repositories
result = await session.call_tool(
    "search_repositories",
    arguments={
        "query": "user:YOUR_USERNAME language:python",
        "sort": "updated",
        "limit": 10
    }
)

# Example: Check your own repo
result = await session.call_tool(
    "get_repository_info",
    arguments={
        "owner": "YOUR_USERNAME",
        "repo": "YOUR_REPO"
    }
)

# Example: Read your config file
result = await session.call_tool(
    "get_file_contents",
    arguments={
        "owner": "YOUR_USERNAME",
        "repo": "YOUR_REPO",
        "path": "config.json"
    }
)
```

---

## Common Search Queries

Here are some useful search query examples:

```python
# Language specific
"language:python"
"language:javascript"
"language:rust"

# By stars/forks
"stars:>1000"
"forks:>500"
"stars:100..1000"

# By topic
"topic:machine-learning"
"topic:web-framework"
"topic:game-engine"

# Combinations
"language:python stars:>5000 topic:data-science"
"language:go forks:>100"
"language:typescript topic:react"

# By user/org
"user:microsoft language:typescript"
"org:google language:go"

# By date
"created:>2023-01-01"
"pushed:>2024-01-01"

# By size
"size:>10000"  # in KB
```

---

## Troubleshooting

### Error: "GITHUB_TOKEN environment variable is required"
**Solution:** Create a `.env` file with your GitHub token:
```bash
echo "GITHUB_TOKEN=your_token_here" > .env
```

### Error: "404 Not Found"
**Solution:** Check that the repository/user/file path exists and is public.

### Error: Rate limit exceeded
**Solution:** GitHub API has rate limits. Wait a few minutes or use an authenticated token for higher limits.

### Connection errors
**Solution:** Ensure the MCP server is installed and can be run:
```bash
python -m github_mcp.server
```

---

## Creating Your Own Scripts

Basic template:

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def my_custom_demo():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "github_mcp.server"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Your custom tool calls here
            result = await session.call_tool(
                "tool_name",
                arguments={"param": "value"}
            )
            
            print(result.content[0].text)

if __name__ == "__main__":
    asyncio.run(my_custom_demo())
```

---

## Next Steps

1. Try the `interactive_demo.py` to explore the API
2. Modify `individual_examples.py` with your own repositories
3. Create your own custom scripts based on your needs
4. Integrate the MCP server with Claude Desktop for AI-powered GitHub exploration!

---

## Additional Resources

- [GitHub Search Syntax](https://docs.github.com/en/search-github/searching-on-github)
- [MCP Documentation](https://modelcontextprotocol.io)
- [PyGithub Documentation](https://pygithub.readthedocs.io)