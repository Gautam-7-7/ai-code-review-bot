import os
import requests
from openai import OpenAI

def main():
    # Read secrets
    github_token = os.getenv("GITHUB_TOKEN")
    openai_key = os.getenv("OPENAI_API_KEY")
    repo = os.getenv("GITHUB_REPOSITORY")       # owner/repo
    pr_number = os.getenv("PR_NUMBER")          # set in workflow

    if not github_token or not openai_key:
        print("❌ Missing secrets")
        return

    print(f"✅ Running review for PR #{pr_number} in {repo}")

    # Step 1: Get PR diff
    diff_url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
    headers = {"Authorization": f"token {github_token}"}
    resp = requests.get(diff_url, headers=headers)

    if resp.status_code != 200:
        print("❌ Failed to fetch PR files:", resp.text)
        return

    files = resp.json()
    changes = "\n\n".join(
        [f"File: {f['filename']}\nPatch:\n{f.get('patch', '')}" for f in files]
    )

    # Step 2: Ask GPT for a code review
    client = OpenAI(api_key=openai_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful code reviewer."},
            {"role": "user", "content": f"Review this code diff:\n{changes}"}
        ]
    )

    review = response.choices[0].message.content
    print("AI Review:", review)

    # Step 3: Post comment back to PR
    comment_url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    data = {"body": f"🤖 AI Code Review:\n\n{review}"}
    comment_resp = requests.post(comment_url, headers=headers, json=data)

    if comment_resp.status_code == 201:
        print("✅ Review posted to PR")
    else:
        print("❌ Failed to post review:", comment_resp.text)

if __name__ == "__main__":
    main()
