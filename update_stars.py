import requests

# Replace 'talfig' with your GitHub username
username = 'talfig'
api_url = f'https://api.github.com/users/{username}/repos'

response = requests.get(api_url)
repos = response.json()

total_stars = sum(repo['stargazers_count'] for repo in repos)

# Update the SVG file
svg_file_path = 'path/to/your/svgfile.svg'

with open(svg_file_path, 'r') as file:
    svg_content = file.read()

# Replace the placeholder [TOTAL_STARS] in the SVG with the actual total stars
updated_svg_content = svg_content.replace('[TOTAL_STARS]', str(total_stars))

# Write the updated SVG content back to the file
with open(svg_file_path, 'w') as file:
    file.write(updated_svg_content)

print(f"Updated SVG with {total_stars} stars")
