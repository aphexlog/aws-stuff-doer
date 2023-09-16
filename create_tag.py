# create a tag for the current commit based off of the version in the setup.py file
# usage: python3 create_tag.py

import re
import subprocess

# Read the content of the setup.py file
with open("setup.py", "r", encoding="utf-8") as fh:
    setup_py = fh.read()

# Get the version from the setup.py file
version = re.search(r"version=\"(\d+\.\d+\.\d+)\"", setup_py).group(1)

# Create a tag for the current commit
subprocess.run(
    ["git", "tag", "-a", f"v{version}", "-m", f"v{version}"], check=True
)
subprocess.run(["git", "push", "--tags"], check=True)

print(f"Created tag v{version} and pushed to remote")
