import requests
import os

# Get GitHub stats
username = "talfig"
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

    # Handle different response structures
    if stat == "followers":
        stats[stat] = data.get("followers", 0)  # Direct access since it's a dict
    elif stat in ["stars", "forks", "pull_requests", "issues"]:
        stats[stat] = data.get("total_count", 0)  # Access total_count for search results or default to 0
    elif stat == "commits":
        stats[stat] = len(data.get("items", []))  # Count commits (list of items), default to empty list
    elif stat in ["repos", "gists"]:
        stats[stat] = len(data) if isinstance(data, list) else 0  # Count repos or gists if response is a list

# Update SVG file
with open("terminal_stats.svg", "r") as file:
    svg_content = file.read()

# Replace placeholders in SVG with actual stats
svg_content = svg_content.replace("[Stars]", str(stats.get("stars", 0)))
svg_content = svg_content.replace("[Forks]", str(stats.get("forks", 0)))
svg_content = svg_content.replace("[Commits]", str(stats.get("commits", 0)))
svg_content = svg_content.replace("[Followers]", str(stats.get("followers", 0)))
svg_content = svg_content.replace("[Pull Requests]", str(stats.get("pull_requests", 0)))
svg_content = svg_content.replace("[Issues]", str(stats.get("issues", 0)))
svg_content = svg_content.replace("[Repository]", str(stats.get("repos", 0)))
svg_content = svg_content.replace("[Gists]", str(stats.get("gists", 0)))

with open("terminal_stats.svg", "w") as file:
    file.write(svg_content)
