from crewai.tools import BaseTool
from repo_analyzer.utils import mcp_tool

class ListBranchesTool(BaseTool):
    name: str = "get_repo_branches"
    description: str = "Fetch and provide a list of 5 branches of the GitHub repository using the MCP server."

    def _run(self, owner: str, repo: str) -> list:
        print(f"Branch Lister: Get the branches of {owner}/{repo}")
        result = mcp_tool([
            "tools", "list_branches",
            "--owner", owner,
            "--repo", repo,
            "--perPage", "5",
            "--page", "1"
        ])
        if isinstance(result, list):
            return result
        else:
            print(f"Branch Lister: Unexpected result: {result}")
            return []

# Create the tool instance to export
get_repo_branches = ListBranchesTool()
