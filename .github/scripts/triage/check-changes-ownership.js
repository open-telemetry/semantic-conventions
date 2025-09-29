const utils = require('./utils')

async function changesInInactiveAreas(core, context, github, areas, changedAreas) {
    let changesWithoutOwners = [];
    const areaOwnersMap = utils.getActiveAreasWithCodeOwners(areas);

    changedAreas.forEach(ca => {
        if (!areaOwnersMap.has(ca)) {
            changesWithoutOwners.push(ca);
        }
    });

    if (changesWithoutOwners.length > 0) {
        core.setFailed(`The pull request PR contains changes to areas that are not active:\n${changesWithoutOwners.join('\n')}`)
        await github.rest.issues.addLabels({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              labels: ['triage:rejected:declined']
            })
        await github.rest.pulls.createReviewComment({
            owner: context.repo.owner,
            repo: context.repo.repo,
            pull_number: context.issue.number,
            commit_id: context.sha,
            body: 'PR contains changes to areas that are not active'
        });
    }

    return changesWithoutOwners;
}

const findChangesInInactiveAreas = async (core, context, github, areas, changedAreas) => {
    await changesInInactiveAreas(core, context, github, areas, JSON.parse(changedAreas));
}

module.exports = findChangesInInactiveAreas;
