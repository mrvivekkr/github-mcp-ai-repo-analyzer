# GitHub MCP AI Repo Analyzer

This project is a Django-based repo documentation generator powered by agentic AI, integrating the GitHub MCP server toolkit. It summarizes the structure, open issues, pull requests, and branches of any GitHub repository, producing clear Markdown and HTML outputs.

---

## Overview

Analyze public or private GitHub repositories and produce concise documentation using AI and MCP CLI tools. Agent workflows fetch and summarize data using OpenAI and present results in your browser.

---

## Sample Output

See example documentation generated for the GitHub MCP Server repo:

- [Sample HTML Report](./sample_reports/Generated-GitHub-Documentation.html)

These files illustrate how this tool visualizes repository structure, open issues, pull requests, and more.

---

## Quickstart

1. **Build MCP Server and CLI Tools**
```
git clone https://github.com/github/github-mcp-server.git
cd github-mcp-server
go build -o github-mcp-server ./cmd/github-mcp-server
go build -o mcpcurl ./cmd/mcpcurl
```

Copy both binaries into your Django project root:
```
cp github-mcp-server mcpcurl /path/to/your/project/
```


2. **Set up Environment Variables**
- Create a `.env` file in your project root:
  ```
  OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  ```

3. **Install Python Dependencies**
pip install -r requirements.txt


4. **Apply Migrations and Run**
python manage.py migrate
python manage.py runserver

- Access [http://localhost:8000](http://localhost:8000) in your browser.

---

## Features

- Repository structure summary with clickable tree.
- Issue and pull request fetching and summarization.
- Branch listing.
- AI-powered Markdown and HTML documentation.

---

## Troubleshooting

- For empty results or "401 Bad credentials", check your GitHub token:
- Must be correct, not expired, and have `repo` and `user` scopes.
- For binary errors, rebuild `mcpcurl` and `github-mcp-server` for your OS.
- Make sure your `.env` values match those loaded in the shell.

---

## References

- [github-mcp-server](https://github.com/github/github-mcp-server)
- [OpenAI API Docs](https://platform.openai.com/docs/api-reference)
- [Django Docs](https://docs.djangoproject.com/en/5.2/)

