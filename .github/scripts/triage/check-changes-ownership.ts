import * as utils from './utils.ts';
import { Octokit } from "@octokit/action";

const octokit = new Octokit();

const [owner, repo] = process.env.GITHUB_REPOSITORY!.split("/");
const prNumber: number = +process.env.PR_NUMBER!;
const changes: string[] = process.env.CHANGED_FILES!.split(',');

/**
 * Checks if the PR already has the 'triage:accepted:ready' or 'triage:accepted:ready-with-sig' label, meaning the triage checks should be skipped.
 * Also checks if the PR title starts with '[chore]' which indicates a maintenance PR that should skip checks.
 * @returns true if the PR has the 'triage:accepted:ready' or 'triage:accepted:ready-with-sig' label or title starts with '[chore]', false otherwise.
 */
async function shouldSkipCheck() {
    const result = await octokit.request("GET /repos/{owner}/{repo}/issues/{issue_number}", {
        owner: owner,
        repo: repo,
        issue_number: prNumber
    });

    const hasAcceptedLabel = result.data.labels?.some(l =>
        l.name === "triage:accepted:ready" || l.name === "triage:accepted:ready-with-sig"
    ) ?? false;
    const isChore = result.data.title.toLowerCase().startsWith('[chore]');

    return hasAcceptedLabel || isChore;
}

function getCommentText(changesWithoutOwners: string[]): string {
    return `
This PR contains changes to area(s) that do not have an active SIG/project and will be auto-closed:

- ${changesWithoutOwners.join('\n- ')}

Such changes may be rejected or put on hold until a new SIG/project is established.

Please refer to the [Semantic Convention Areas](https://github.com/open-telemetry/semantic-conventions/blob/main/AREAS.md)
document to see the current active SIGs and also to learn how to kick start a new one.`;
}

async function changesInInactiveAreas(): Promise<boolean> {
    // skips enforcing the triage process if the PR has the 'triage:accepted:ready' label on it
    // this means maintainers/approvers decided to bypass it for good reasons.
    if (await shouldSkipCheck()) {
        return false;
    }

    const areas = utils.getAllAreasMetadata();
    const areaOwnersMap = utils.getActiveAreasWithCodeOwners(areas);

    // extract only the name after model/ which is the actual area name
    const changedAreas = changes.map(folder => folder.split('/')[1]);

    let changesWithoutOwners: string[] = [];
    changedAreas.forEach(ca => {
        if (!areaOwnersMap.has(ca)) {
            changesWithoutOwners.push(ca);
        }
    });

    if (changesWithoutOwners.length > 0) {
        await octokit.request("POST /repos/{owner}/{repo}/issues/{issue_number}/labels", {
            owner: owner,
            repo: repo,
            issue_number: prNumber,
            labels: ['triage:rejected:declined']
        });
        await octokit.request("POST /repos/{owner}/{repo}/issues/{issue_number}/comments", {
            owner: owner,
            repo: repo,
            issue_number: prNumber,
            body: getCommentText(changesWithoutOwners)
        });
        await octokit.request("PATCH /repos/{owner}/{repo}/issues/{issue_number}", {
            owner: owner,
            repo: repo,
            issue_number: prNumber,
            state: 'closed',
            state_reason: 'not_planned'
        });

        return true
    }

    return false;
}

(async () => {
    const result = await changesInInactiveAreas();
    if (result) {
        process.exit(1);
    }
})();
