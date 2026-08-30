// update_dashboard.js
//
// Fetches the public repos from the GitHub API, builds the "live" section of
// the profile README (headline stats, language mix, most recently touched
// projects) and injects it between the START_SECTION / END_SECTION markers.
//
// Runs on plain Node 20+ (built-in fetch, no dependencies).

const fs = require("fs");
const path = require("path");

const USERNAME = process.env.GH_USERNAME || "ka1rav6";
const TOKEN = process.env.GH_TOKEN;
const README_PATH = path.join(__dirname, "README.md");

const START_MARKER = "<!--START_SECTION:dashboard-->";
const END_MARKER = "<!--END_SECTION:dashboard-->";

// Housekeeping repos — real, but not worth a slot in the showcase.
const HIDDEN = new Set([
  USERNAME,             // this repo
  "githubworkshop",
  "bbs-iiitd-induction",
  "mom-projects",
]);

const RECENT_COUNT = 6;
const LANG_COUNT = 6;
const BAR_WIDTH = 22;

async function fetchRepos() {
  const res = await fetch(
    `https://api.github.com/users/${USERNAME}/repos?per_page=100&sort=pushed`,
    {
      headers: {
        Accept: "application/vnd.github+json",
        ...(TOKEN ? { Authorization: `Bearer ${TOKEN}` } : {}),
      },
    }
  );
  if (!res.ok) {
    throw new Error(`GitHub API error: ${res.status} ${await res.text()}`);
  }
  return res.json();
}

function daysAgo(dateStr) {
  return Math.floor((Date.now() - new Date(dateStr).getTime()) / 86400000);
}

function ago(dateStr) {
  const d = daysAgo(dateStr);
  if (d === 0) return "today";
  if (d === 1) return "yesterday";
  if (d < 30) return `${d}d ago`;
  return `${Math.floor(d / 30)}mo ago`;
}

function statusFor(repo) {
  const d = daysAgo(repo.pushed_at);
  if (d <= 3) return "`building`";
  if (d <= 21) return "`warm`";
  return "`resting`";
}

function languageBars(repos) {
  const counts = new Map();
  for (const r of repos) {
    if (!r.language) continue;
    counts.set(r.language, (counts.get(r.language) || 0) + 1);
  }
  const ranked = [...counts.entries()].sort((a, b) => b[1] - a[1]).slice(0, LANG_COUNT);
  if (!ranked.length) return "";

  const max = ranked[0][1];
  const pad = Math.max(...ranked.map(([name]) => name.length));

  return ranked
    .map(([name, n]) => {
      const filled = Math.max(1, Math.round((n / max) * BAR_WIDTH));
      const bar = "█".repeat(filled) + "░".repeat(BAR_WIDTH - filled);
      const label = n === 1 ? "1 repo" : `${n} repos`;
      return `${name.padEnd(pad)}  ${bar}  ${label}`;
    })
    .join("\n");
}

function buildSection(repos) {
  const own = repos.filter((r) => !r.fork && !r.archived);
  // Only repos that can explain themselves get a row.
  const showcase = own.filter((r) => !HIDDEN.has(r.name) && r.description);

  const stars = own.reduce((sum, r) => sum + (r.stargazers_count || 0), 0);
  const oldest = own.reduce(
    (min, r) => (new Date(r.created_at) < new Date(min) ? r.created_at : min),
    own[0]?.created_at || new Date().toISOString()
  );
  const since = new Date(oldest).toLocaleDateString("en-GB", {
    month: "short",
    year: "numeric",
  });
  const synced = new Date().toISOString().replace("T", " ").slice(0, 16) + " UTC";

  const rows = showcase
    .sort((a, b) => new Date(b.pushed_at) - new Date(a.pushed_at))
    .slice(0, RECENT_COUNT)
    .map((r) => {
      const desc = (r.description || "").split(/(?<=\.)\s|—/)[0].trim().slice(0, 84);
      return `| [\`${r.name}\`](${r.html_url}) | ${r.language || "—"} | ${desc || "—"} | ${ago(
        r.pushed_at
      )} | ${statusFor(r)} |`;
    })
    .join("\n");

  return `\`${own.length} public repos\` · \`${stars} stars\` · \`shipping since ${since}\` · \`synced ${synced}\`

**most recently touched**

| repo | lang | what | last push | state |
|---|---|---|---|---|
${rows}

**where the time goes** <sub>(primary language, public repos)</sub>

\`\`\`
${languageBars(own)}
\`\`\``;
}

async function main() {
  const repos = await fetchRepos();
  const section = buildSection(repos);

  const readme = fs.readFileSync(README_PATH, "utf8");
  const startIdx = readme.indexOf(START_MARKER);
  const endIdx = readme.indexOf(END_MARKER);

  if (startIdx === -1 || endIdx === -1) {
    throw new Error("Dashboard markers not found in README.md");
  }

  const before = readme.slice(0, startIdx + START_MARKER.length);
  const after = readme.slice(endIdx);

  fs.writeFileSync(README_PATH, `${before}\n${section}\n${after}`, "utf8");
  console.log("Dashboard section updated.");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
