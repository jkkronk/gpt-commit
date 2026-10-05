import argparse
import openai
import subprocess
import re
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field

class CodeChange:
    file_changed = Field(..., description="The name of the file that was changed.")
    lines_changed = Field(..., description="The lines that were changed in the file.")
    content = Field(..., description="The content of the change or the review of the change.")

    def __init__(self, file_changed, lines_changed, content):
        self.file_changed = file_changed
        self.lines_changed = lines_changed
        self.content = content

    def __repr__(self):
        return f"File Changed: {self.file_changed}, Lines Changed: {self.lines_changed}, Content: {self.content}"


class reviewList(BaseModel):
    review: list[CodeChange] = Field(..., description="A list of suggestions reflecting the change.")

def fetch_code_diff(branch_to_compare_with):
    git_diff_command = ["git", "diff", "HEAD...", branch_to_compare_with]

    try:
        result = subprocess.run(git_diff_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print("Error while executing git diff:", e.stderr)
        return []

    diffs = result.stdout.split('\ndiff --git')
    code_changes = []

    for diff in diffs:
        if diff:
            # Parse file name
            file_match = re.search(r'a/(.*) b/', diff)
            file_changed = file_match.group(1) if file_match else "Unknown File"

            # Parse changed lines
            lines_match = re.findall(r'@@ \-(\d+,\d+) \+(\d+,\d+) @@', diff)
            lines_changed = ', '.join(['-'.join(lines) for lines in lines_match])

            # Construct a CodeChange object
            code_changes.append(CodeChange(file_changed, lines_changed, diff))

    return code_changes

def review_code(branch_to_compare_with):
    # Fetch the code differences between the two branches
    code_diff = fetch_code_diff(branch_to_compare_with)

    # OpenAI API setup
    openai.api_key = 'YOUR_OPENAI_API_KEY'

    # Prepare the prompt for GPT-4
    prompt = f"Review the following code changes:" \
             f"\n\n{code_diff}"

    # Sending request to OpenAI GPT-4
    client = instructor.patch(OpenAI())
    reviews: reviewList = client.chat.completions.create(
        model="gpt-4",
        response_model=reviewList,
        messages=[
            {"role": "user", "content": prompt},
        ],
        max_retries=2,
    )

    return reviews

def main():
    parser = argparse.ArgumentParser(description='Merge Request Code Review using GPT-4')
    parser.add_argument('branch', type=str, help='The name of the branch to merge into')

    args = parser.parse_args()

    review = review_code(args.branch)

    print("Code Review:\n", review)

    ## TODO: Add logic to write in the terminal review line per review line and ask for approval


if __name__ == "__main__":
    main()
