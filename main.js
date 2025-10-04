import { LeetCode, Credential } from 'leetcode-query';
import moment from 'moment';
import fs from 'fs';
import path from 'path';
import { Octokit } from 'octokit';
import ModelClient, { isUnexpected } from "@azure-rest/ai-inference";
import { AzureKeyCredential } from "@azure/core-auth";
import sgMail from '@sendgrid/mail';

function getFileExtension(lang) {
    const map = {
        'python3': 'py', 'java': 'java', 'cpp': 'cpp', 'c': 'c', 'csharp': 'cs', 'javascript': 'js', 'typescript': 'ts', 'ruby': 'rb', 'swift': 'swift', 'go': 'go', 'kotlin': 'kt', 'rust': 'rs', 'scala': 'scala', 'mysql': 'sql', 'bash': 'sh', 'php': 'php', 'racket': 'rkt', 'erlang': 'erl', 'elixir': 'ex', 'dart': 'dart', 'perl': 'pl', 'h': 'hs', 'lua': 'lua', 'shell': 'sh', 'plaintext': 'txt',
    };
    return map[lang] || 'txt';
}

function getCommentPrefix(ext) {
    if (["js", "ts", "cpp", "java", "kt", "go", "swift", "scala", "rs", "php", "dart", "pl", "hs", "lua", "kt", "erl", "ex"].includes(ext)) return "//";
    if (["py", "sh", "txt"].includes(ext)) return "#";
    if (ext === "sql") return "--";
    return "#";
}

function parseRepo(repoString) {
    let owner, repo;
    if (repoString.startsWith('http')) {
        const parts = repoString.replace(/\.git$/, '').split('/');
        owner = parts[parts.length - 2];
        repo = parts[parts.length - 1];
    } else if (repoString.startsWith('git@')) {
        const match = repoString.match(/:(.+)\/(.+)\.git$/);
        if (match) {
            owner = match[1];
            repo = match[2];
        }
    } else {
        [owner, repo] = repoString.replace(/\.git$/, '').split('/');
    }
    if (!owner || !repo) throw new Error('Could not parse owner/repo from GITHUB_REPO');
    return [owner, repo];
}

async function analyzeCodeWithAzureOpenAI(code, problemTitle, lang) {
    const endpoint = process.env.AZURE_OPENAI_ENDPOINT;
    const apiKey = process.env.AZURE_OPENAI_API_KEY;
    const model = process.env.AZURE_OPENAI_MODEL || "gpt-4o";
    if (!endpoint || !apiKey) return '[Azure OpenAI endpoint or API key missing]';
    const client = ModelClient(endpoint, new AzureKeyCredential(apiKey));
    const prompt = `Analyze the following LeetCode solution code for the problem titled "${problemTitle}" written in ${lang}. For your analysis, provide:\n- A brief summary of the code\n- The time complexity\n- The space complexity\n- Strengths\n- Weaknesses\n- Suggestions for improvement\n\nCode:\n${code}`;
    try {
        const response = await client.path("/chat/completions").post({
            body: {
                messages: [
                    { role: "system", content: "You are a helpful AI code reviewer. Always include time and space complexity in your analysis." },
                    { role: "user", content: prompt }
                ],
                temperature: 1,
                top_p: 1,
                model: model
            }
        });
        if (isUnexpected(response)) {
            console.error('Azure OpenAI API error:', {
                status: response.status,
                body: response.body,
                headers: response.headers
            });
            return `[Azure OpenAI error: ${response.body.error?.message || 'Unknown error'} | Status: ${response.status} | Body: ${JSON.stringify(response.body)}]`;
        }
        return response.body.choices[0].message.content;
    } catch (e) {
        console.error('Azure OpenAI request failed:', e);
        return `[Azure OpenAI request failed: ${e.message} | Error: ${JSON.stringify(e)}]`;
    }
}

async function sendSummaryEmail({
    to,
    from,
    submissions,
    githubRepo,
    githubBranch,
    commitDate
}) {
    sgMail.setApiKey(process.env.SENDGRID_API_KEY);
    const subject = `LeetCode Daily Summary for ${commitDate}`;
    let html = `<h2>LeetCode Problems Solved on ${commitDate}</h2>`;
    if (submissions.length === 0) {
        html += `<p>No problems solved today.</p>`;
    } else {
        html += `<ul>`;
        for (const sub of submissions) {
            html += `<li><b>${sub.title}</b> (${sub.lang})<br>
            <a href="https://leetcode.com${sub.url}">View Submission</a></li>`;
        }
        html += `</ul>`;
        html += `<p>All solutions have been committed to <a href="https://github.com/${githubRepo}/tree/${githubBranch}">${githubRepo}</a> with full analysis.</p>`;
    }
    html += `<p>If you face any error in the automation, please check the logs or contact support.</p>`;
    const text = `LeetCode Problems Solved on ${commitDate}\n${submissions.map(sub => `- ${sub.title} (${sub.lang})`).join('\n')}
All solutions have been committed to ${githubRepo} (${githubBranch}) with full analysis.
If you face any error in the automation, please check the logs or contact support.`;
    const msg = {
        to,
        from,
        subject,
        text,
        html
    };
    try {
        await sgMail.send(msg);
        console.log('Summary email sent successfully.');
    } catch (e) {
        console.error('Error sending summary email:', e);
    }
}

async function main() {
    try {
        const username = process.env.LEETCODE_USERNAME;
        const session = process.env.LEETCODE_SESSION;
        const csrfToken = process.env.LEETCODE_CSRFTOKEN;
        const githubToken = process.env.GITHUB_TOKEN;
        const githubRepo = process.env.GITHUB_REPO;
        const githubBranch = process.env.GITHUB_BRANCH || 'main';
        const sendgridApiKey = process.env.SENDGRID_API_KEY;
        const mailTo = process.env.MAIL_TO;
        const mailFrom = process.env.MAIL_FROM;
        if (!username || !session || !csrfToken) {
            throw new Error('Missing LEETCODE_USERNAME, LEETCODE_SESSION, or LEETCODE_CSRFTOKEN environment variables');
        }
        if (!githubToken || !githubRepo) {
            throw new Error('Missing GITHUB_TOKEN or GITHUB_REPO environment variables');
        }
        if (!process.env.AZURE_OPENAI_ENDPOINT || !process.env.AZURE_OPENAI_API_KEY) {
            throw new Error('Missing AZURE_OPENAI_ENDPOINT or AZURE_OPENAI_API_KEY environment variable');
        }
        if (!sendgridApiKey || !mailTo || !mailFrom) {
            throw new Error('Missing SENDGRID_API_KEY, MAIL_TO, or MAIL_FROM environment variable');
        }

        const credential = new Credential();
        await credential.init(session, csrfToken);
        const leetcode = new LeetCode(credential);

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

        const todayStart = moment.utc().startOf('day');
        const todayEnd = moment.utc().endOf('day');
        const todaysSubmissions = submissions.filter(submission => {
            const subTime = moment.unix(Math.floor(submission.timestamp / 1000)).utc();
            return subTime.isBetween(todayStart, todayEnd, null, '[]');
        });

        const distinctMap = new Map();
        for (const submission of todaysSubmissions) {
            if (!distinctMap.has(submission.titleSlug) || distinctMap.get(submission.titleSlug).timestamp < submission.timestamp) {
                distinctMap.set(submission.titleSlug, submission);
            }
        }
        const distinctSubmissions = Array.from(distinctMap.values())
            .sort((a, b) => b.timestamp - a.timestamp);

        if (distinctSubmissions.length === 0) {
            console.log('No distinct LeetCode submissions found for today (UTC day)');
            return;
        }

        console.log(`Found ${distinctSubmissions.length} distinct LeetCode submissions for today (UTC).`);
        const detailsArr = await Promise.all(distinctSubmissions.map(sub =>
            leetcode.submission(sub.id).catch(() => ({ code: '[Error fetching code]' }))
        ));

        const savedFiles = [];
        for (let idx = 0; idx < distinctSubmissions.length; idx++) {
            const submission = distinctSubmissions[idx];
            const code = detailsArr[idx].code || '[Code not found]';
            const problemName = submission.titleSlug.replace(/[^a-zA-Z0-9\-]/g, '');
            const ext = getFileExtension(submission.lang);
            const fileName = `${problemName}.${ext}`;
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
            console.log(`Analyzing code for '${submission.title}'...`);
            const analysis = await analyzeCodeWithAzureOpenAI(code, submission.title, submission.lang);
            const fileContent = `${detailsComment}\n${code}\n\n${commentPrefix} Azure OpenAI Analysis\n'''\n${analysis}\n'''`;
            fs.writeFileSync(fileName, fileContent, 'utf8');
            savedFiles.push(fileName);
            console.log(`Saved file: ${fileName}`);
        }

        console.log(`All files saved. Total: ${savedFiles.length}`);

        console.log('Committing files to GitHub...');
        const octokit = new Octokit({ auth: githubToken });
        const [owner, repo] = parseRepo(githubRepo);
        const { data: refData } = await octokit.rest.git.getRef({ owner, repo, ref: `heads/${githubBranch}` });
        const latestCommitSha = refData.object.sha;
        const { data: commitData } = await octokit.rest.git.getCommit({ owner, repo, commit_sha: latestCommitSha });
        const baseTreeSha = commitData.tree.sha;
        const blobs = await Promise.all(savedFiles.map(async file => {
            const content = fs.readFileSync(path.join(process.cwd(), file), 'utf8');
            const blob = await octokit.rest.git.createBlob({ owner, repo, content, encoding: 'utf-8' });
            return { file, sha: blob.data.sha };
        }));
        const tree = blobs.map(({ file, sha }) => ({ path: file, mode: '100644', type: 'blob', sha }));
        const { data: newTree } = await octokit.rest.git.createTree({ owner, repo, tree, base_tree: baseTreeSha });
        const commitMessage = moment.utc().format('YYYY-MM-DD');
        const { data: newCommit } = await octokit.rest.git.createCommit({ owner, repo, message: commitMessage, tree: newTree.sha, parents: [latestCommitSha] });
        await octokit.rest.git.updateRef({ owner, repo, ref: `heads/${githubBranch}`, sha: newCommit.sha });
        console.log('Files committed to GitHub successfully.');

        // Send summary email
        await sendSummaryEmail({
            to: mailTo,
            from: mailFrom,
            submissions: distinctSubmissions,
            githubRepo,
            githubBranch,
            commitDate: commitMessage
        });
    } catch (e) {
        console.error(e);
        process.exit(1);
    }
}

main();

process.on('unhandledRejection', () => {
    process.exit(1);
});
