// rules/heading-title-sync.js
const matter = require("gray-matter");

module.exports = function(context, options = {}) {
  const { Syntax, RuleError, report, fixer, getSource } = context;

  return {
    [Syntax.Document](node) {
      const fullText = getSource(node);

      // Parse front matter safely
      const parsed = matter(fullText);
      const yamlNode = Object.keys(parsed.data).length > 0 ? parsed.data : undefined;
      const body = parsed.content || "";

      const frontMatterTitle = yamlNode ? yamlNode.title : undefined;
      const h1Match = body.match(/^#\s+(.*)$/m);
      const h1Title = h1Match ? h1Match[1].trim() : null;

      // -----------------------------------
      // CASE 1: No YAML front matter at all
      // -----------------------------------
      if (!yamlNode) {
        const yamlBlock = matter.stringify(body, {
          title: h1Title
        });

        report(
          node,
          new RuleError("Missing YAML front matter", {
            //fix: fixer.insertTextBeforeRange([0, 0], yamlBlock)
          })
        );
        return;
      }

      // -----------------------------------
      // CASE 2: YAML exists but no title
      // -----------------------------------
      if (!frontMatterTitle) {
        const yamlBlock = matter.stringify("", {
          ... yamlNode,
          title: h1Title
        });
        report(
          node,
          new RuleError("Missing title in YAML front matter", {
            //fix: fixer.replaceText(yamlNode, yamlBlock)
          })
        );
        return;
      }

      // -----------------------------------
      // CASE 3: YAML title exists but H1 missing
      // -----------------------------------
      if (!h1Title) {
        const h1 = `\n# ${frontMatterTitle}\n\n`;
        const yamlBlock = matter.stringify(h1, {
          ... yamlNode,
          title: h1Title
        });
        report(
          node,
          new RuleError("Missing H1 heading", {
            //fix: fixer.replaceText(yamlNode, yamlBlock)
          })
        );
        return;
      }

      // -----------------------------------
      // CASE 4: Both exist but differ → update YAML ONLY
      // -----------------------------------
      if (frontMatterTitle !== h1Title) {
        const updated = matter.stringify(body, {
          ...yamlNode,
          title: h1Title
        });

        report(
          node,
          new RuleError(
            `YAML title (“${frontMatterTitle}”) does not match H1 (“${h1Title}”)`,
            {
              //fix: fixer.replaceText(yamlNode, updated)
            }
          )
        );
      }
    }
  };
};
