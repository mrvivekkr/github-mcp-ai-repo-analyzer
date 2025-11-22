from crewai.tools import BaseTool
from repo_analyzer.utils import mcp_tool

class GetOpenIssuesTool(BaseTool):
    name: str = "get_open_issues"
    description: str = "Fetch and provide a list of open issues from a GitHub repository using the MCP server."

    def _run(self, owner: str, repo: str) -> list:
        print(f"Issue Retriever: Getting open issues for {owner}/{repo}")
        result = mcp_tool([
            "tools", "list_issues",
            "--owner", owner,
            "--repo", repo,
            "--state", "open",
            "--perPage", "5",
            "--page", "1"
        ])
        if isinstance(result, list):
            return result
        else:
            print(f"Issue Retriever: Unexpected result: {result}")
            return []

# Create the tool instance to export
get_open_issues = GetOpenIssuesTool()
