import { readFileSync } from 'fs'
import { parse } from 'yaml'

export interface Owner {
    name: string
    github: string
}

export interface Area {
    name: string
    owner?: Owner[]
    project: string
    board: string
    labels: string[]
    status: string[]
}

export function isAreaActive(area: Area): boolean {
    return area.status.includes('accepting_contributions') || area.status.includes('active');
}

export function getActiveAreasWithCodeOwners(areas: Area[]): Map<string, Set<string>>{
    const areaOwnersMap = new Map<string, Set<string>>();
    areas.filter(a => isAreaActive(a)).forEach((area) => {
        area.labels.forEach((l) => {
            const labelWithoutPrefix = l.slice('area:'.length);
            // use all areas as map key
            if (!areaOwnersMap.has(labelWithoutPrefix)) {
                areaOwnersMap.set(labelWithoutPrefix, new Set<string>());
            }
            // add all owners - an area can be owned by multiple teams
            // as well as a team own many areas.
            area.owner?.forEach((owner) => {
                areaOwnersMap.get(labelWithoutPrefix)!.add(owner.github);
            });
        });
    });
    return areaOwnersMap;
}

export function getAllAreasMetadata(): Area[] {
    const fileContent = readFileSync('./areas.yaml', 'utf8')
    const data = parse(fileContent)
    return data.areas;
}
