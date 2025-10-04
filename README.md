# LeetCode Daily Automation & AI Code Analysis

## Overview
This repository contains my **LeetCode solutions**, automatically submitted daily through my **Turbotic AI-powered automation pipeline**. Each solution includes:
- Problem metadata (title, language, runtime, memory, submission URL)
- **AI-assisted code analysis** using Azure OpenAI
- Daily commits for consistent tracking
This project ensures **consistent DSA practice**, provides **verifiable proof of work**, and improves problem-solving skills through AI analysis.

## Features
- **Automated Daily Commits** – Solutions solved on LeetCode are automatically committed to this repository.
- **AI-Powered Code Analysis** – Each solution is analyzed for:
  - Code summary
  - Time and space complexity
  - Strengths and weaknesses
  - Suggestions for improvement
- **Daily Email Summary** – Summary of solved problems and links to GitHub commits.
- **Consistent DSA Practice** – Encourages daily problem-solving and progress tracking.

## Tech Stack
- **Node.js** – Automation scripting
- **LeetCode-query** – Fetch submissions
- **Azure OpenAI** – AI-powered analysis
- **GitHub API (Octokit)** – Automated commits
- **SendGrid** – Daily email summaries
- **Moment.js** – Date handling

## Automation Script
All automation logic is implemented in **`main.js`**, including:
- Fetching submissions from LeetCode
- Analyzing code with Azure OpenAI
- Committing annotated solutions to GitHub
- Sending daily summary emails

## Motivation
During college, I solved many LeetCode problems but had little proof of consistent work for placements. This automation:
- Submits solutions to GitHub automatically
- Provides AI-assisted insights for each solution
- Sends daily email reminders to track progress
It bridges the gap between **practice and proof**, while enhancing **DSA skills** for placement preparation.

## How to Use
Clone the repository:
```bash
git clone https://github.com/<your-username>/<repo-name>.git
code in main.js
---


