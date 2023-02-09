@echo off
git rm -r --cached .

# Add these removals to the Staging Area...
git add .

# ...and commit them!
git commit -m "Clean up ignored files"
pause
