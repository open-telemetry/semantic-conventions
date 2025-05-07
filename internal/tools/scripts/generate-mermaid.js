const fs = require("fs");
const path = require("path");
const yaml = require("js-yaml");

function extractEntitiesAndRelationships(baseDir) {
  const entities = [];

  function processFile(filePath) {
    const fileContent = fs.readFileSync(filePath, "utf8");
    const data = yaml.load(fileContent);

    if (data.groups) {
      data.groups.forEach((group) => {
        if (group.type === "resource" || group.type === "entity") {
          entities.push(group);
        }
      });
    }
  }

  function walkDirectory(dir) {
    const files = fs.readdirSync(dir);
    files.forEach((file) => {
      const fullPath = path.join(dir, file);
      if (fs.statSync(fullPath).isDirectory()) {
        walkDirectory(fullPath);
      } else if (file === "resources.yaml") {
        processFile(fullPath);
      }
    });
  }

  walkDirectory(baseDir);
  return entities;
}

// The word "namespace" is reserved and I don't know how to quote it
function sanitize(name) {
  return name.replace("namespace", "namespacⱸ");
}

function generateMermaidDiagram(entities) {
  console.log("classDiagram");
  for (const entity of entities) {
    const name = sanitize(entity.name);
    for (const attr of entity.attributes) {
      console.log(`  ${name} : attribute ${attr.ref}`);
    }
    for (const attr of entity.descriptive_attributes ?? []) {
      console.log(`  ${name} : descriptive_attribute ${attr.ref}`);
    }
    for (const relationship of entity.relationships ?? []) {
      for ([relationshipType, relatedEntityType] of Object.entries(
        relationship,
      )) {
        console.log(
          `  ${name} --> ${sanitize(relatedEntityType)}: ${relationshipType}`,
        );
      }
    }
  }
}

generateMermaidDiagram(
  extractEntitiesAndRelationships(path.join(__dirname, "../../..", "model")),
);
