import os
import requests
from openai import OpenAI

# Load environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REPO = os.getenv("GITHUB_REPOSITORY")
PR_NUMBER = os.getenv("PR_NUMBER")

client = OpenAI(api_key=OPENAI_API_KEY)

def get_pr_diff():
    """Fetch PR diff from GitHub API"""
    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    pr_data = response.json()
    diff_url = pr_data["diff_url"]
    return requests.get(diff_url, headers=headers).text

def review_code(diff):
    """Send diff to GPT for review"""
    prompt = f"Review the following GitHub Pull Request diff and suggest improvements:\n\n{diff}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a senior software engineer reviewing code."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def post_review(comment):
    """Post review as a comment on PR"""
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    requests.post(url, json={"body": comment}, headers=headers)

if __name__ == "__main__":
    diff = get_pr_diff()
    review = review_code(diff)
    post_review(review)
