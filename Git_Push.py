import subprocess
from datetime import datetime

current_date = datetime.now().date()

        # Add changes to the staging area
subprocess.run(["git", "add", "."])

# Create a commit with a message
subprocess.run(["git", "commit", "-m", str(current_date)])

# Push the commit to the remote repository
subprocess.run(["git", "push"])