import * as utils from './utils.ts';
import { Octokit } from "@octokit/action";

const octokit = new Octokit();

const [owner, repo] = process.env.GITHUB_REPOSITORY!.split("/");
const prNumber: number = +process.env.PR_NUMBER!;
const changes : string[] = process.env.CHANGED_FILES!.split(',');

function getCommentText(changesWithoutOwners: string[]): string {
    return `
This PR contains changes to area(s) that do not have an active SIG/project:

- ${changesWithoutOwners.join('\n- ')}

Such changes may be rejected or put on hold until a new SIG/project is stablished.

Please refer to the [Semantic Convention Areas](./https://github.com/open-telemetry/semantic-conventions/blob/main/AREAS.md)
document to see the current active SIGs and also to learn how to kick start a new one.

If there's no interaction to this PR, it will be auto-closed.`;
}

async function changesInInactiveAreas(): Promise<boolean> {
    const areas = utils.getAllAreasMetadata();

    let changesWithoutOwners: string[] = [];
    const areaOwnersMap = utils.getActiveAreasWithCodeOwners(areas);

    // extract only the name after model/ which is the actual area name
    const changedAreas = changes.map(folder => folder.split('/')[1]);

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
