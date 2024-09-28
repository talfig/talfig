import requests
import shutil
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

    # Check if request was successful
    if response.status_code != 200:
        print(f"Error fetching {stat}: {response.status_code}, {response.text}")
        stats[stat] = 0  # Set default value on error
        continue

    data = response.json()

    # Handle different response structures
    try:
        if stat == "followers":
            stats[stat] = data["followers"]  # Direct access since it's a dict
        elif stat in ["stars", "forks", "pull_requests", "issues"]:
            stats[stat] = data.get("total_count", 0)  # Access total_count for search results
        elif stat == "commits":
            stats[stat] = len(data.get("items", []))  # Count commits (list of items)
        elif stat in ["repos", "gists"]:
            stats[stat] = len(data)  # Count the number of repos or gists
    except KeyError as e:
        print(f"KeyError fetching {stat}: {e}")
        stats[stat] = 0  # Default value if key is missing

# Copy original file to new file with 'new_' prefix
original_file = "terminal_stats.svg"
new_file = "new_terminal_stats.svg"
shutil.copyfile(original_file, new_file)

# Update SVG content in the new file
with open(new_file, "r") as file:
    svg_content = file.read()

# Replace placeholders in SVG with actual stats
svg_content = svg_content.replace("[Stars]", str(stats["stars"]))
svg_content = svg_content.replace("[Forks]", str(stats["forks"]))
svg_content = svg_content.replace("[Commits]", str(stats["commits"]))
svg_content = svg_content.replace("[Followers]", str(stats["followers"]))
svg_content = svg_content.replace("[Pull Requests]", str(stats["pull_requests"]))
svg_content = svg_content.replace("[Issues]", str(stats["issues"]))
svg_content = svg_content.replace("[Repository]", str(stats["repos"]))
svg_content = svg_content.replace("[Gists]", str(stats["gists"]))

# Write updated content to the new file
with open(new_file, "w") as file:
    file.write(svg_content)
