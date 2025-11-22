from crewai import Task
from ..agents.agents import repo_structure_auditor
from ..agents.agents import issue_analyst
from ..agents.agents import pull_requests_fetcher_reporter
from ..agents.agents import repo_branch_reporter
from ..tools.directory_scanner import get_repo_files
from ..tools.issue_retriever import get_open_issues
from ..tools.pull_request_lister import get_pull_requests
from ..tools.branch_lister import get_repo_branches

# Analyze Repository
def analyze_repo_structure_task(owner: str, repo: str):
    return [
        Task(
            description = (
                f"Systematically explore the {owner}/{repo} repository structure using "
                "a breadth-first approach:\n"
                "1. Start with root directory to identify main folders\n"
                "2. Prioritize these directories (explore fully):\n"
                "   - src/, lib/, app/, source/ (source code)\n"
                "   - tests/, test/, __tests__/ (test files)\n"
                "   - docs/, documentation/ (documentation)\n"
                "   - config/, configuration/ (configuration files)\n"
                "3. For each important directory, explore up to 3-4 levels deep\n"
                "4. For less important directories, summarize at 1-2 levels\n"
                "5. Exclude: .git/, node_modules/, __pycache__/, .venv/, dist/, build/\n"
                "6. Include important config files: package.json, requirements.txt, etc.\n"
                "7. Use proper tree indentation (2-4 spaces per level)\n"
                "8. For each file, include: [filename](github_url)\n"
                "9. For directories, use: directory_name/ (no link)\n"
                "10. Group related files together\n"
                "\n"
                "Generate a complete, hierarchical Markdown tree structure."
            ),
            # expected_output = (
            #     "A well-formatted Markdown directory tree with:\n"
            #     "- Proper indentation showing hierarchy (use 2 spaces per level)\n"
            #     "- Directory names ending with '/' (e.g., src/)\n"
            #     "- File names as clickable links: [filename](github_url)\n"
            #     "- Important directories explored 3-4 levels deep\n"
            #     "- Less important directories summarized at 1-2 levels\n"
            #     "- Clear section headers for major directory groups\n"
            #     "- File counts for summarized directories (e.g., 'config/ (15 files)')\n"
            #     "- Example format:\n"
            #     "  ```\n"
            #     "  project/\n"
            #     "    src/\n"
            #     "      main/\n"
            #     "        java/\n"
            #     "          [App.java](url)\n"
            #     "    tests/ (25 files)\n"
            #     "  ```"
            # ),
            expected_output=(
                "A Markdown code block tree with:\n"
                "- Up to 3 levels deep, 2 spaces per indent\n"
                "- Directory names ending with '/'\n"
                "- File names as clickable links\n"
                "- Directories deeper than level 3 shown as 'folder/ (N files)'"
            ),
            agent = repo_structure_auditor,
            tools = [get_repo_files],
            output_file = "/generated_docs/repo_structure.md",
            create_directory = True,
            verbose = True
        )
    ]

def get_issue_tasks(owner: str, repo: str):
    fetch_issue_task = Task(
        description = (
            f"Fetch open issues for the {owner}/{repo} repository and summarize them in Markdown.\n"
            "Format each issue as a bulleted list item: `- [Title](URL): short category or summary`.\n"
            "Example:\n"
            "- [Fix broken tool integration](https://github.com/owner/repo/issues/42): Bug\n"
            "- [Refactor API](https://github.com/owner/repo/issues/43): Enhancement\n"
            "Add priorities/recommendations as a summary paragraph at the end."
        ),
        expected_output = (
            "A Markdown heading:\n"
            "## Open Issues Summary for {owner}/{repo}\n"
            "Followed by a bulleted list of issues (`- [Title](URL): category/summary`)."
        ),
        agent = issue_analyst,
        tools = [get_open_issues],
        output_file = "/generated_docs/report_issues.md",
        create_directory = True,
        verbose = True
    )
    return [fetch_issue_task]

def list_pull_requests_tasks(owner: str, repo: str):
    fetch_pull_request_task = Task(
        description = f"Fetch a list of 5 most recently created pull requests for the {owner}/{repo} repository using the 'get_pull_requests' tool. Analyze the provided lists to identify key themes, active discussions, and potential areas of focus.",
        expected_output = f"A Markdown-formatted summary of the repository's pull requests. Provide a concise and categorical summary of the requests and your feedback for it.",
        agent = pull_requests_fetcher_reporter,
        tools = [get_pull_requests],
        output_file = "/generated_docs/pull_requests.md",
        create_directory = True,
        verbose = True
    )
    return [fetch_pull_request_task] 


def list_branches_tasks(owner: str, repo: str):
    lsit_branches_task = Task(
        description = (
            f"List 5 branches for the {owner}/{repo} repository. Output each branch as a bullet:\n"
            "`- `branch-name`: summary or focus of this branch`\n"
            "Example:\n"
            "- `main`: production/default branch\n"
            "- `feature/auth`: adds authentication module\n"
            "Begin section with a Markdown heading:\n"
            "## Branches Summary for {owner}/{repo} Repository"
        ),
        expected_output = (
            "Markdown heading: ## Branches Summary for {owner}/{repo} Repository\n"
            "Bulleted list: - `branch-name`: short description\n"
            "Brief insights if needed."
        ),agent = repo_branch_reporter,
        tools = [get_repo_branches],
        output_file = "/generated_docs/branches.md",
        create_directory = True,
        verbose = True
    )
    return [lsit_branches_task]