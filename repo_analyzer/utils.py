
import subprocess
import json
import os
from django.conf import settings

def mcp_tool(command_args: list[str]) -> dict or list or str or None:
    """
    Executes mcpcurl with the given command arguments and returns the JSON response.
    """
    mcpcurl_path = os.path.join(os.getcwd(), 'mcpcurl')  # Assuming mcpcurl is in the project root
    github_mcp_server_path = os.path.join(os.getcwd(), '..', 'github-mcp-server', 'github-mcp-server')
    base_command = [
        mcpcurl_path,
        f'--stdio-server-cmd={github_mcp_server_path} --toolsets all stdio'
    ]

    full_command = base_command + command_args
    env = {'GITHUB_PERSONAL_ACCESS_TOKEN': settings.GITHUB_PERSONAL_ACCESS_TOKEN}

    print(f"mcp_tool executing command: {full_command}")  # Debug log

    try:
        process = subprocess.Popen(full_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, env=env, text=True)
        stdout, stderr = process.communicate(timeout=20)
        if stderr:
            print(f"mcpcurl stderr: {stderr}")  # Debug log

        if stdout:
            try:
                return json.loads(stdout)
            except json.JSONDecodeError:
                print(f"mcpcurl stdout is not valid JSON: {stdout}")
                return stdout.strip()
        else:
            return None

    except FileNotFoundError:
        print(f"Error: mcpcurl not found at {mcpcurl_path}")
        return None
    except subprocess.TimeoutExpired:
        print("Error: Timeout communicating with mcpcurl.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while running mcpcurl: {e}")
        return None

