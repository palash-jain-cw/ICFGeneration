import re
import subprocess


def fix_markdown_for_streamlit(markdown):
    # Match tables and add a horizontal rule after them
    fixed_markdown = re.sub(
        r"((?:^\|.*?\|\n)+)",  # Match the entire table block
        r"\1\n\n---\n\n",  # Add a horizontal rule after the table
        markdown,
        flags=re.MULTILINE,
    )
    return fixed_markdown


def get_git_branch():
    try:
        return (
            subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"])
            .decode()
            .strip()
        )
    except Exception:
        return "unknown"
