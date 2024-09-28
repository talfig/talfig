import requests
import shutil
import os

# Get GitHub stats
username = "talfig"
token = os.getenv("GITHUB_TOKEN")

headers = {"Authorization": f"token {token}"}
base_url = "https://api.github.com"

stats = {}

# Fetch repositories to calculate stars, forks, and commits
repos_url = f"{base_url}/users/{username}/repos"
repos_response = requests.get(repos_url, headers=headers)
repos = repos_response.json()

# Initialize counts
total_stars = 0
total_forks = 0
total_commits = 0

for repo in repos:
    total_stars += repo.get("stargazers_count", 0)
    total_forks += repo.get("forks_count", 0)
    
    # Fetch commits for each repository
    commits_url = f"{base_url}/repos/{username}/{repo['name']}/commits"
    commits_response = requests.get(commits_url, headers=headers)
    commits = commits_response.json()
    total_commits += len(commits)

# Fetch followers count
followers_url = f"{base_url}/users/{username}"
followers_response = requests.get(followers_url, headers=headers)
followers = followers_response.json().get("followers", 0)

# Fetch pull requests and issues count
pull_requests_url = f"{base_url}/search/issues?q=type:pr+author:{username}"
pull_requests_response = requests.get(pull_requests_url, headers=headers)
total_pull_requests = pull_requests_response.json().get("total_count", 0)

issues_url = f"{base_url}/search/issues?q=type:issue+author:{username}"
issues_response = requests.get(issues_url, headers=headers)
total_issues = issues_response.json().get("total_count", 0)

# Fetch gists count
gists_url = f"{base_url}/users/{username}/gists"
gists_response = requests.get(gists_url, headers=headers)
total_gists = len(gists_response.json())

# Store stats
stats["stars"] = total_stars
stats["forks"] = total_forks
stats["commits"] = total_commits
stats["followers"] = followers
stats["pull_requests"] = total_pull_requests
stats["issues"] = total_issues
stats["repos"] = len(repos)
stats["gists"] = total_gists

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
