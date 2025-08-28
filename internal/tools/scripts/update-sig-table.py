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
yaml_input = "sigs.yaml"
markdown_file = "SIGs.md"

# Define the markers
start_marker = "<!-- sigs -->"
end_marker = "<!-- endsigs -->"

# Read the YAML file
with open(yaml_input, 'r') as file:
    data = yaml.safe_load(file)

# Extract the top and bottom parts of the existing markdown file
with open(markdown_file, 'r') as file:
    content = file.read()
    top_part, bottom_part = content.split(start_marker, 1)[0], content.split(end_marker, 1)[1]

# Generate the markdown content for each SIG group
markdown_content = start_marker + '\n'
markdown_content += "| Name | Owners | Project | Board | Areas | Status | Notes |\n"
markdown_content += "|------|--------|---------|-------|-------|--------|-------|\n"

for sig in data['sigs']:
    name = sig['name']
    project = sig['project']
    board = sig['board']

    owners = ",<br/>".join(
        [
            f"[{owner['name']}](https://github.com/orgs/open-telemetry/teams/{owner['github']})"
            for owner in sig.get('owner', [])
            if owner.get('name') and owner.get('github')
        ]
    )

    labels = ", ".join(
        [f"`{label}`"
         for label in sig.get('labels', [])
         if label]
    )

    areas = ", ".join(
        [f"`{area}`"
         for area in sig.get('areas', [])
         if area]
    )

    # Add a default note for common SIG states
    if sig.get('notes'):
        notes = " ".join(sig['notes'].split())
    elif not sig.get('notes') and 'inactive' in labels:
        notes = "The SIG is inactive. Bugs and bugfixes are welcome. For substantial changes, follow the [new project process](https://github.com/open-telemetry/community/blob/main/project-management.md)"
    elif not sig.get('notes') and 'accepting_contributions' in labels:
        notes = "The SIG is looking for contributions!"

    markdown_content += f"| {name} | {owners} | {project} | {board} | {areas} | {labels} | {notes} |\n"

markdown_content += end_marker

result = top_part + markdown_content + bottom_part

if run_in_check_mode:
    with open(markdown_file, 'r') as file:
        original = file.read()
    if original == result:
        sys.exit(0)
    else:
        print("SIGS.md is outdated. Run make sig-table-generation to update")
        sys.exit(1)
else:
    # Write the updated markdown content to file
    with open(markdown_file, 'w') as file:
        file.write(top_part)
        file.write(markdown_content)
        file.write(bottom_part)

# Inform the user that the markdown file has been updated
print("The markdown file has been updated with the new SIG tables.")
