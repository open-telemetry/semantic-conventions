const gulp = require("gulp");
const through2 = require("through2");
const markdownlint = require("markdownlint");
const yaml = require("js-yaml");
const fs = require("fs");

let numFilesProcessed = 0,
  numFilesWithIssues = 0;

function markdownLintFile(file, encoding, callback) {
  const config = yaml.load(fs.readFileSync("./.markdownlint.yaml", "utf8"));
  const options = {
    files: [file.path],
    config: config,
  };

  markdownlint(options, function (err, result) {
    if (err) {
      console.error("ERROR occurred while running markdownlint: ", err);
      return callback(err);
    }

    const _resultString = (result || "").toString();
    // Result is a string with lines of the form:
    //
    //   <file-path>:\s*<line-number>: <ID-and-message>
    //
    // Strip out any whitespace between the filepath and line number
    // so that tools can jump directly to the line.
    const resultString = _resultString
      .split("\n")
      .map((line) => line.replace(/^([^:]+):\s*(\d+):(.*)/, "$1:$2:$3"))
      .join("\n");
    if (resultString) {
      console.log(resultString);
      numFilesWithIssues++;
      // Don't report an error yet so that other files can be checked:
      // callback(new Error('...'));
    }
    numFilesProcessed++;
    callback(null, file);
  });
}

function lintMarkdown() {
  const markdownFiles = ["**/*.md", "!**/node_modules/**", "!**/.github/**"];

  return gulp
    .src(markdownFiles)
    .pipe(through2.obj(markdownLintFile))
    .on("end", () => {
      const fileOrFiles = "file" + (numFilesProcessed == 1 ? "" : "s");
      const msg = `Processed ${numFilesProcessed} ${fileOrFiles}, ${numFilesWithIssues} had issues.`;
      if (numFilesWithIssues > 0) {
        throw new Error(msg);
      } else {
        console.log(msg);
      }
    });
}

lintMarkdown.description = `Run markdownlint on all '*.md' files.`;

gulp.task("lint-md", lintMarkdown);
