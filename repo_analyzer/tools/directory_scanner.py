from crewai.tools import BaseTool
from repo_analyzer.utils import mcp_tool

class ListRepoFilesTool(BaseTool):
    name: str = "get_repo_files"
    description: str = "List files and folders at a given path in a GitHub repository."

    def _run(self, owner: str, repo: str, path: str = "/"):
        if not path or str(path).strip() == "":
            path = "/"
        result = mcp_tool([
            "tools", "get_file_contents",
            "--owner", owner,
            "--repo", repo,
            "--path", path
        ])
        return result if isinstance(result, list) else []


# Create instance to export
get_repo_files = ListRepoFilesTool()
