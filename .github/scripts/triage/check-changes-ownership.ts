import * as utils from './utils.ts';
import { Octokit } from "@octokit/action";

const octokit = new Octokit();

export function shouldSkipCheckForPullRequest(pr: { labels?: Array<{ name?: string }>, title: string }) {
    const hasAcceptedLabel = pr.labels?.some(l =>
        l.name === "triage:accepted:ready" ||
        l.name === "triage:accepted:ready-with-sig"
    ) ?? false;
    const hasDependenciesLabel = pr.labels?.some(l => l.name === "dependencies") ?? false;
    const isChore = pr.title.toLowerCase().startsWith('[chore]');

    return hasAcceptedLabel || hasDependenciesLabel || isChore;
}

/**
 * Checks if the PR already has the 'triage:accepted:ready' or 'triage:accepted:ready-with-sig' label, meaning the triage checks should be skipped.
 * Also checks if the PR has the 'dependencies' label or its title starts with '[chore]', which indicate PRs that should skip checks.
 * @returns true if the PR should skip the ownership check, false otherwise.
 */
async function shouldSkipCheck() {
    const [owner, repo] = process.env.GITHUB_REPOSITORY!.split("/");
    const prNumber: number = +process.env.PR_NUMBER!;
    const result = await octokit.request("GET /repos/{owner}/{repo}/issues/{issue_number}", {
        owner: owner,
        repo: repo,
        issue_number: prNumber
    });

    return shouldSkipCheckForPullRequest({
        labels: result.data.labels,
        title: result.data.title,
    });
}

function getCommentText(changesWithoutOwners: string[]): string {
    return `👋 Thanks for your contribution!

This PR modifies file(s) in area(s) that do not currently have an active SIG/project:

- ${changesWithoutOwners.join('\n- ')}

Per the [area ownership process](https://github.com/open-telemetry/semantic-conventions/blob/main/AREAS.md),
changes to these areas need an active SIG/project, so this PR has been automatically
closed and labeled \`triage:rejected:declined\`.

This does not mean your change is unwelcome:

- **For substantial changes or new conventions**: Consider starting a new SIG/project.
  See the [Project Management](https://github.com/open-telemetry/community/blob/main/project-management.md) guide.
- **If you believe this was closed in error**: Please reach out in the
  \`#otel-semantic-conventions\` channel on the [CNCF Slack](https://slack.cncf.io/).

Thanks again for taking the time to contribute! 🙏`;
}

async function changesInInactiveAreas(): Promise<boolean> {
    const [owner, repo] = process.env.GITHUB_REPOSITORY!.split("/");
    const prNumber: number = +process.env.PR_NUMBER!;
    const changes: string[] = process.env.CHANGED_FILES!.split(',');

    // skips enforcing the triage process if the PR has an accepted/dependencies label
    // or if it is a maintenance chore PR.
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

if (process.argv[1]?.endsWith('check-changes-ownership.ts')) {
    (async () => {
        const result = await changesInInactiveAreas();
        if (result) {
            process.exit(1);
        }
    })();
}
