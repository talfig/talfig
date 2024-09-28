import requests
import os

# Get GitHub stats
username = "YourGitHubUsername"
token = os.getenv("GITHUB_TOKEN")

headers = {"Authorization": f"token {token}"}
base_url = "https://api.github.com"

stats = {}

# Fetch user profile stats
endpoints = {
    "stars": f"/search/repositories?q=user:{username}+stars:>0",
    "forks": f"/search/repositories?q=user:{username}+forks:>0",
    "commits": f"/search/commits?q=author:{username}",
    "followers": f"/users/{username}",
    "pull_requests": f"/search/issues?q=type:pr+author:{username}",
    "issues": f"/search/issues?q=type:issue+author:{username}",
    "repos": f"/users/{username}/repos",
    "gists": f"/users/{username}/gists",
}

for stat, endpoint in endpoints.items():
    url = base_url + endpoint
    response = requests.get(url, headers=headers)
    data = response.json()

    if stat == "followers":
        stats[stat] = data["followers"]
    elif stat == "stars" or stat == "forks" or stat == "repos" or stat == "gists":
        stats[stat] = data["total_count"]
    elif stat == "commits":
        stats[stat] = len(data["items"])  # Count commits by the user
    elif stat == "pull_requests" or stat == "issues":
        stats[stat] = data["total_count"]

# Update SVG file
with open("terminal_stats.svg", "r") as file:
    svg_content = file.read()

svg_content = svg_content.replace("<number of stars>", str(stats["stars"]))
svg_content = svg_content.replace("<number of forks>", str(stats["forks"]))
svg_content = svg_content.replace("<number of commits>", str(stats["commits"]))
svg_content = svg_content.replace("<number of followers>", str(stats["followers"]))
svg_content = svg_content.replace("<number of pull requests>", str(stats["pull_requests"]))
svg_content = svg_content.replace("<number of issues>", str(stats["issues"]))
svg_content = svg_content.replace("<number of repos>", str(stats["repos"]))
svg_content = svg_content.replace("<number of gists>", str(stats["gists"]))

with open("terminal_stats.svg", "w") as file:
    file.write(svg_content)
