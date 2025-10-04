==========================================================
LeetCode to GitHub Automation
==========================================================

Automatically sync your daily LeetCode submissions to a 
GitHub repository.

----------------------------------------------------------
SETUP
----------------------------------------------------------

# Environment Variables (must be set in your workspace)

LEETCODE_USERNAME   = Your LeetCode username
LEETCODE_SESSION    = Your LeetCode session token (for API access)
LEETCODE_CSRFTOKEN  = Your LeetCode CSRF token (for API access)
GITHUB_TOKEN        = A GitHub personal access token with repo write permissions
GITHUB_REPO         = Target GitHub repository (owner/repo OR full URL OR SSH format)
GITHUB_BRANCH       = Branch to commit to (default: main)

# Permissions
- GITHUB_TOKEN must allow pushing commits to the specified repo + branch

# LeetCode
- You must have at least one submission for today (UTC)

----------------------------------------------------------
DEPENDENCIES
----------------------------------------------------------

Install required npm packages:
    npm install leetcode-query moment octokit

Built-in (no install needed):
    fs
    path

Packages:
- leetcode-query : Fetch LeetCode submissions and code
- moment         : UTC date/time handling
- octokit        : GitHub API for commits
- fs             : File system operations
- path           : File path handling

----------------------------------------------------------
HOW IT WORKS
----------------------------------------------------------

1. Fetch today's (UTC) submissions from LeetCode
2. Save each distinct submission as a file
3. Commit all files to the target GitHub repo + branch 
   in a single commit

----------------------------------------------------------
EXAMPLE
----------------------------------------------------------

# .env file

LEETCODE_USERNAME=johndoe
LEETCODE_SESSION=abcd1234
LEETCODE_CSRFTOKEN=wxyz5678
GITHUB_TOKEN=ghp_1234567890
GITHUB_REPO=johndoe/leetcode-solutions
GITHUB_BRANCH=main


# Run automation

npm start

==========================================================
----------------------------------------------------------
CODE IN main.js
----------------------------------------------------------
