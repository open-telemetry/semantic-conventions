function isAreaActive(area) {
    return area.status.includes('accepting_contributions') || area.status.includes('active');
}

function getActiveAreasWithCodeOwners(areas) {
    const areaOwnersMap = new Map();
    areas.filter(a => isAreaActive(a)).forEach((area) => {
        area.labels.forEach((l) => {
            const labelWithoutPrefix = l.slice('area:'.length);
            // use all areas as map key
            if (!areaOwnersMap.has(labelWithoutPrefix)) {
                areaOwnersMap.set(labelWithoutPrefix, new Set());
            }
            // add all owners - an area can be owned by multiple teams
            // as well as a team own many areas.
            area.owner.forEach((owner) => {
                areaOwnersMap.get(labelWithoutPrefix).add(owner.github);
            });
        });
    });
    return areaOwnersMap;
}

module.exports = {
    isAreaActive: isAreaActive,
    getActiveAreasWithCodeOwners: getActiveAreasWithCodeOwners
};
