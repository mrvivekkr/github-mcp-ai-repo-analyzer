from crewai.tools import BaseTool
from repo_analyzer.utils import mcp_tool

class ListPullRequestsTool(BaseTool):
    name: str = "get_pull_requests"
    description: str = "Fetch and provide a list of 5 most recently updated pull requests from a GitHub repository using the MCP server."

    def _run(self, owner: str, repo: str) -> list:
        print(f"Pull Requests Lister: Get the pull requests for {owner}/{repo}")
        result = mcp_tool([
            "tools", "list_pull_requests",
            "--owner", owner,
            "--repo", repo,
            "--sort", "updated",
            "--direction", "desc",
            "--perPage", "5",
            "--page", "1"
        ])
        if isinstance(result, list):
            return result
        else:
            print(f"Pull Request Lister: Unexpected result: {result}")
            return []

# Create the tool instance to export
get_pull_requests = ListPullRequestsTool()
