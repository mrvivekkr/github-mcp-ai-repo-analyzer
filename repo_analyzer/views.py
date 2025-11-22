import os
import markdown
from django.shortcuts import render
from .crews.crew import build_crew
from django.conf import settings

OPENAI_API_KEY = settings.OPENAI_API_KEY  # or load from environment

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GENERATED_DOCS_DIR = os.path.join(BASE_DIR, 'generated_docs')


# Create your views here.
def documentation_interface(request):
    return render(request, 'repo_analyzer/documentation_interface.html')

def generate_documentation(request):
    if request.method == 'POST':
        repo_url = request.POST.get('repo_url', '')
        if repo_url:
            try:
                owner, repo_name = extract_owner_repo(repo_url)
                if owner and repo_name:
                    if not OPENAI_API_KEY:
                        error = "Error: OPENAI_API_KEY is not set in Django settings."
                        return render(request, 'repo_analyzer/documentation_interface.html', {'error': error})

                    # llm = ChatOpenAI(api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo-16k")
                    crew = build_crew(owner, repo_name)
                    crew.kickoff()

                    output_files = [
                        os.path.join(GENERATED_DOCS_DIR, "repo_structure.md"),
                        os.path.join(GENERATED_DOCS_DIR, "report_issues.md"),
                        os.path.join(GENERATED_DOCS_DIR, "pull_requests.md"),
                        os.path.join(GENERATED_DOCS_DIR, "branches.md"),
                    ]
                    final_output_path = os.path.join(GENERATED_DOCS_DIR, "summary.md")
                    combined_markdown_path = combine_markdown_files(output_files, final_output_path, owner, repo_name)

                    if combined_markdown_path:
                        html_content = convert_markdown_to_html(combined_markdown_path)
                        if html_content:
                            return render(request, 'repo_analyzer/documentation_display.html', {
                                'documentation': html_content
                            })
                        else:
                            error = "Failed to convert combined Markdown to HTML."
                            return render(request, 'repo_analyzer/documentation_interface.html', {'error': error})
                    else:
                        error = "Failed to combine the documentation files."
                        return render(request, 'repo_analyzer/documentation_interface.html', {'error': error})
                else:
                    error = "Invalid GitHub repository URL."
                    return render(request, 'repo_analyzer/documentation_interface.html', {'error': error})

            except ValueError as e:
                error = str(e)
                return render(request, 'repo_analyzer/documentation_interface.html', {'error': error})

    return render(request, 'repo_analyzer/documentation_interface.html')


def extract_owner_repo(repo_url: str):
    import re
    match = re.match(r"https?://github\.com/([^/]+)/([^/]+)", repo_url)
    if match:
        return match.group(1), match.group(2)
    return None, None


def combine_markdown_files(file_paths, output_path, owner, repo_name):
    combined_content = f"# Summary for {owner}/{repo_name}\n\n"
    for file_path in file_paths:
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
                markdown_content = ""
                # Handle code fences for markdown content
                if lines and lines[0].strip() == "``````":
                    markdown_content = "".join(lines[1:-1]).strip()
                else:
                    markdown_content = "".join(lines).strip()
                combined_content += f"\n\n---\n\n" + markdown_content
        except FileNotFoundError:
            print(f"Warning: File not found: {file_path}")
    try:
        with open(output_path, "w") as f:
            f.write(combined_content.strip())
        print(f"Combined output saved to {output_path}")
        return output_path
    except Exception as e:
        print(f"Error saving combined markdown: {e}")
        return None

# The utility function to change markdown to HTML
def convert_markdown_to_html(markdown_file_path):
    try:
        with open(markdown_file_path, "r") as f:
            markdown_text = f.read()
            html_content = markdown.markdown(markdown_text, extensions=['extra'])
            return html_content
    except FileNotFoundError:
        print(f"Error: Markdown file not found at {markdown_file_path}")
        return None
    except Exception as e:
        print(f"Error converting Markdown to HTML: {e}")
        return None