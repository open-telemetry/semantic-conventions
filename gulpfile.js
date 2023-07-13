const gulp = require("gulp");
const through2 = require("through2");
const markdownlint = require("markdownlint");
const yaml = require("js-yaml");
const fs = require("fs");

const markdownFiles = ["**/*.md", "!**/node_modules/**", "!**/.github/**"];
const config = yaml.load(fs.readFileSync("./.markdownlint.yaml", "utf8"));

let fileCounter = 0;

function markdownLintFile(file, encoding, callback) {
  const options = {
    files: [file.path],
    config: config,
  };

  markdownlint(options, function (err, result) {
    const _resultString = (result || "").toString();
    // Result is of the form:
    // "<file-path>:\s*<line-number>: <ID-and-message"
    // Strip out the whitespace between the file-path and line number
    // so that tools can jump directly to the line.
    const resultString = _resultString.replace(
      /([^:]+):\s*(\d+):(.*)/,
      "$1:$2:$3",
    );
    if (resultString) console.log(resultString);
    fileCounter++;
    callback(null, file);
  });
}

function lintMarkdown() {
  return (
    gulp
      .src(markdownFiles)
      .pipe(through2.obj(markdownLintFile))
      .on("end", () => {
        console.log(`Processed ${fileCounter} file${fileCounter == 1 ? '' : 's'}.`);
      })
  );
}

gulp.task("lint-md", lintMarkdown);
