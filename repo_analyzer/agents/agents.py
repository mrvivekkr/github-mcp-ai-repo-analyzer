from crewai import Agent
from ..tools.directory_scanner import get_repo_files
from ..tools.issue_retriever import get_open_issues
from ..tools.pull_request_lister import get_pull_requests
from ..tools.branch_lister import get_repo_branches

## Repository Structure Analyzer
# repo_structure_auditor = Agent(
#     role = "Repository Structure Auditor",
#     goal = "Analyze the folder and file structure of a GitHub repository and produce a Markdown-based file tree with clickable links.",
#     backstory = (
#         "You are skilled at visualizing repository structures. You help developers by generating clean, readable "
#         "Markdown summaries of files and folders, especially for documentation purposes."
#         ),
#         tools = [get_repo_files],
#         verbose = True        
#     )
repo_structure_auditor = Agent(
    role = "Repository Structure Auditor",
    goal = (
        "Systematically explore and document the complete directory structure "
        "of a GitHub repository, creating a hierarchical tree that accurately "
        "represents the project organization. Prioritize important directories "
        "and provide clear navigation paths."
    ),
    backstory = (
        "You are an expert at analyzing software repository structures. "
        "You understand common project layouts (src/, tests/, docs/, config/, etc.) "
        "and can identify the most important directories. You systematically "
        "traverse directories, going deeper into critical paths while summarizing "
        "less important areas. You create clear, navigable tree structures that "
        "help developers quickly understand project organization."
    ),
    tools = [get_repo_files],  # Add recursive tool
    verbose = True
)

## GitHub Issue Analyst
issue_analyst = Agent(
    role = "GitHub Issue Analyst",
    goal = "Fetch and summarize open GitHub issues, and suggest which issue should be prioritized.",
    backstory = (
        "You are an experienced open-source contributor who can identify, retrieve, and analyze GitHub issues. "
        "You know how to summarize them effectively and highlight the ones that need urgent attention."
    ),
    tools = [get_open_issues],
    verbose = True
)

## Pull Requests Lister
pull_requests_fetcher_reporter = Agent(
    role = "Pull Request Lister",
    goal = "Fetch and provide a list of 5 most recently created pull requests from a GitHub repository with clickable links to each PR.",
    backstory = (
        "You are an expert in retrieving information about GitHub pull requests using the MCP server. "
        "You always include clickable links to each pull request using the html_url field from the PR data. "
        "You format links as [PR #number](url) in Markdown. You concisely summarize pull requests as categories "
        "and provide a comprehensive and readable report with proper links."
    ),
    tools = [get_pull_requests],
    verbose = True
)

## Branch Lister
repo_branch_reporter = Agent(
    role = "Repository Branch Reportor",
    goal = "Fetch and provide a list of 5 branches in a GitHub repository.",
    backstory = "You are an expert in retrieving information about GitHub issues using the MCP server. You also concisely summarize branch as categories and provide a comprehensive and readable report",
    tools = [get_repo_branches],
    verbose = True
)