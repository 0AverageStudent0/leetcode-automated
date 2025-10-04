const { LeetCode, Credential } = require('leetcode-query');
const moment = require('moment');
const fs = require('fs');
const path = require('path');
const { Octokit } = require('octokit');

// Map LeetCode language to file extension
function getFileExtension(lang) {
    const map = {
        'python3': 'py',
        'java': 'java',
        'cpp': 'cpp',
        'c': 'c',
        'csharp': 'cs',
        'javascript': 'js',
        'typescript': 'ts',
        'ruby': 'rb',
        'swift': 'swift',
        'go': 'go',
        'kotlin': 'kt',
        'rust': 'rs',
        'scala': 'scala',
        'mysql': 'sql',
        'bash': 'sh',
        'php': 'php',
        'racket': 'rkt',
        'erlang': 'erl',
        'elixir': 'ex',
        'dart': 'dart',
        'perl': 'pl',
        'haskell': 'hs',
        'lua': 'lua',
        'shell': 'sh',
        'plaintext': 'txt',
    };
    return map[lang] || 'txt';
}

// Map file extension to comment prefix
function getCommentPrefix(ext) {
    if (["js", "ts", "cpp", "c", "java", "kt", "go", "swift", "scala", "rs", "php", "dart", "pl", "hs", "lua", "rkt", "erl", "ex"].includes(ext)) return "//";
    if (["py", "sh", "txt"].includes(ext)) return "#";
    if (ext === "sql") return "--";
    return "#";
}

function parseRepo(repoString) {
    // Accepts: owner/repo OR https://github.com/owner/repo OR git@github.com:owner/repo.git
    let owner, repo;
    if (repoString.startsWith('http')) {
        // https://github.com/owner/repo or similar
        const parts = repoString.replace(/\.git$/, '').split('/');
        owner = parts[parts.length - 2];
        repo = parts[parts.length - 1];
    } else if (repoString.startsWith('git@')) {
        // git@github.com:owner/repo.git
        const match = repoString.match(/:(.+)\/(.+)\.git$/);
        if (match) {
            owner = match[1];
            repo = match[2];
        }
    } else {
        // owner/repo
        [owner, repo] = repoString.replace(/\.git$/, '').split('/');
    }
    if (!owner || !repo) throw new Error('Could not parse owner/repo from GITHUB_REPO');
    return [owner, repo];
}

async function main() {
    try {
        const username = process.env.LEETCODE_USERNAME;
        const session = process.env.LEETCODE_SESSION;
        const csrfToken = process.env.LEETCODE_CSRFTOKEN;
        const githubToken = process.env.GITHUB_TOKEN;
        const githubRepo = process.env.GITHUB_REPO;
        const githubBranch = process.env.GITHUB_BRANCH || 'main';
        if (!username || !session || !csrfToken) {
            throw new Error('Missing LEETCODE_USERNAME, LEETCODE_SESSION, or LEETCODE_CSRFTOKEN environment variables');
        }
        if (!githubToken || !githubRepo) {
            throw new Error('Missing GITHUB_TOKEN or GITHUB_REPO environment variables');
        }

        // Setup credential
        const credential = new Credential();
        await credential.init(session, csrfToken);
        const leetcode = new LeetCode(credential);

        // Get recent 30 submissions (timeout 30s)
        let submissions;
        try {
            submissions = await Promise.race([
                leetcode.submissions({ limit: 30, offset: 0 }),
                new Promise((_, reject) => setTimeout(() => reject(new Error('LeetCode submissions API timed out after 30s')), 30000))
            ]);
        } catch (apiErr) {
            process.exit(1);
        }
        if (!submissions || submissions.length === 0) {
            console.log('No submissions found');
            return;
        }

        // Filter submissions made today (UTC)
        const todayStart = moment.utc().startOf('day');
        const todayEnd = moment.utc().endOf('day');
        const todaysSubmissions = submissions.filter(submission => {
            const subTime = moment.unix(Math.floor(submission.timestamp / 1000)).utc();
            return subTime.isBetween(todayStart, todayEnd, null, '[]');
        });

        // Make them distinct by last submitted (by titleSlug)
        const distinctMap = new Map();
        for (const submission of todaysSubmissions) {
            if (!distinctMap.has(submission.titleSlug) || distinctMap.get(submission.titleSlug).timestamp < submission.timestamp) {
                distinctMap.set(submission.titleSlug, submission);
            }
        }
        const distinctSubmissions = Array.from(distinctMap.values())
            .sort((a, b) => b.timestamp - a.timestamp); // Sort by latest first

        if (distinctSubmissions.length === 0) {
            console.log('No distinct LeetCode submissions found for today (UTC day)');
            return;
        }

        // Fetch code for each distinct submission in parallel
        console.log('Saving each distinct LeetCode submission made today (UTC) to a file...');
        const detailsArr = await Promise.all(distinctSubmissions.map(sub =>
            leetcode.submission(sub.id).catch(() => ({ code: '[Error fetching code]' }))
        ));

        const savedFiles = [];
        distinctSubmissions.forEach((submission, idx) => {
            const code = detailsArr[idx].code || '[Code not found]';
            // Prepare file name: <problem name>.<ext>
            const problemName = submission.titleSlug.replace(/[^a-zA-Z0-9\-]/g, '');
            const ext = getFileExtension(submission.lang);
            const fileName = `${problemName}.${ext}`;
            // Prepare file content: details as comments, code as code
            const commentPrefix = getCommentPrefix(ext);
            const detailsComment = [
                `${commentPrefix} Problem Title: ${submission.title}`,
                `${commentPrefix} Language: ${submission.lang}`,
                `${commentPrefix} Status: ${submission.statusDisplay}`,
                `${commentPrefix} Runtime: ${submission.runtime}`,
                `${commentPrefix} Memory: ${submission.memory}`,
                `${commentPrefix} Submission URL: https://leetcode.com${submission.url}`,
                '',
            ].join('\n');
            const fileContent = `${detailsComment}\n${code}`;
            fs.writeFileSync(fileName, fileContent, 'utf8');
            savedFiles.push(fileName);
            console.log(`Saved: ${fileName}`);
        });

        // Cat all the files just created
        console.log('\n--- Contents of all generated files ---');
        for (const file of savedFiles) {
            console.log(`\n===== ${file} =====`);
            const content = fs.readFileSync(path.join(process.cwd(), file), 'utf8');
            console.log(content);
        }
        console.log('\n--- End of files ---');

        // Commit all files to GitHub in a single commit
        console.log('Committing files to GitHub...');
        const octokit = new Octokit({ auth: githubToken });
        const [owner, repo] = parseRepo(githubRepo);
        // Get latest commit SHA and tree SHA
        const { data: refData } = await octokit.rest.git.getRef({
            owner,
            repo,
            ref: `heads/${githubBranch}`
        });
        const latestCommitSha = refData.object.sha;
        const { data: commitData } = await octokit.rest.git.getCommit({
            owner,
            repo,
            commit_sha: latestCommitSha
        });
        const baseTreeSha = commitData.tree.sha;
        // Create blobs for each file
        const blobs = await Promise.all(savedFiles.map(async file => {
            const content = fs.readFileSync(path.join(process.cwd(), file), 'utf8');
            const blob = await octokit.rest.git.createBlob({
                owner,
                repo,
                content,
                encoding: 'utf-8'
            });
            return { file, sha: blob.data.sha };
        }));
        // Create a new tree
        const tree = blobs.map(({ file, sha }) => ({
            path: file,
            mode: '100644',
            type: 'blob',
            sha
        }));
        const { data: newTree } = await octokit.rest.git.createTree({
            owner,
            repo,
            tree,
            base_tree: baseTreeSha
        });
        // Create a new commit
        const commitMessage = "Add today's LeetCode submissions";
        const { data: newCommit } = await octokit.rest.git.createCommit({
            owner,
            repo,
            message: commitMessage,
            tree: newTree.sha,
            parents: [latestCommitSha]
        });
        // Update the branch reference
        await octokit.rest.git.updateRef({
            owner,
            repo,
            ref: `heads/${githubBranch}`,
            sha: newCommit.sha
        });
        console.log('Files committed to GitHub successfully.');
    } catch (e) {
        console.error(e);
        process.exit(1);
    }
}

main();

process.on('unhandledRejection', () => {
    process.exit(1);
});
