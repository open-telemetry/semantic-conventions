#!/usr/bin/env python3
import subprocess
import sys

# in the Makefile we use a unmodified python container to run this script, so we need to install pyyaml if it's not already installed
if (len(sys.argv) > 1) and (sys.argv[1] == "--install"):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyyaml', '--root-user-action=ignore'])
    sys.argv = sys.argv[1:]

import yaml

# Do not safe the file but verify that it is different from the original one.
run_in_check_mode = (len(sys.argv) > 1) and (sys.argv[1] == "--check")

# Define the YAML input file and the markdown file to be updated
yaml_input = "areas.yaml"
markdown_file = "AREAS.md"

# Define the markers
start_marker = "<!-- areas -->"
end_marker = "<!-- endareas -->"

# Read the YAML file
with open(yaml_input, 'r') as file:
    data = yaml.safe_load(file)

# Extract the top and bottom parts of the existing markdown file
with open(markdown_file, 'r') as file:
    content = file.read()
    top_part, bottom_part = content.split(start_marker, 1)[0], content.split(end_marker, 1)[1]

# Generate the markdown content for each AREA group
markdown_content = start_marker + '\n'
markdown_content += "| Name | Owners | Project | Board | Labels | Status | Notes |\n"
markdown_content += "|------|--------|---------|-------|-------|--------|-------|\n"

for area in data['areas']:
    name = area['name']
    project = area['project']
    board = area['board']

    owners = ",<br/>".join(
        [
            f"[{owner['name']}](https://github.com/orgs/open-telemetry/teams/{owner['github']})"
            for owner in area.get('owner', [])
            if owner.get('name') and owner.get('github')
        ]
    )

    labels = ", ".join(
        [f"`{label}`"
         for label in area.get('labels', [])
         if label]
    )

    status = ", ".join(
        [f"`{s}`"
         for s in area.get('status', [])
         if s]
    )

    # Add a default note for common states
    if area.get('notes'):
        notes = " ".join(area['notes'].split())
    elif not area.get('notes') and 'inactive' in status:
        notes = "The SIG is inactive. Bugs and bugfixes are welcome. For substantial changes, follow the [new project process](https://github.com/open-telemetry/community/blob/main/project-management.md)"
    elif not area.get('notes') and 'accepting_contributions' in status:
        notes = "The SIG is looking for contributions!"

    markdown_content += f"| {name} | {owners} | {project} | {board} | {labels} | {status} | {notes} |\n"

markdown_content += end_marker

result = top_part + markdown_content + bottom_part

if run_in_check_mode:
    with open(markdown_file, 'r') as file:
        original = file.read()
    if original == result:
        sys.exit(0)
    else:
        print("AREAS.md is outdated. Run make areas-table-generation to update")
        sys.exit(1)
else:
    # Write the updated markdown content to file
    with open(markdown_file, 'w') as file:
        file.write(top_part)
        file.write(markdown_content)
        file.write(bottom_part)

# Inform the user that the markdown file has been updated
print("The markdown file has been updated with the new area tables.")
