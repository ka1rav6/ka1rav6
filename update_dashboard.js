// scripts/update_dashboard.js
//
// Fetches the user's repos from the GitHub API, builds a small
// "live progress" markdown table, and injects it into README.md
// between the START_SECTION / END_SECTION markers.
//
// Runs with plain Node 20 (built-in fetch, no dependencies needed).

const fs = require("fs");
const path = require("path");

const USERNAME = process.env.GH_USERNAME || "ka1rav6";
const TOKEN = process.env.GH_TOKEN;
const README_PATH = path.join(__dirname, "README.md");

const START_MARKER = "<!--START_SECTION:dashboard-->";
const END_MARKER = "<!--END_SECTION:dashboard-->";

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
  const diffMs = Date.now() - new Date(dateStr).getTime();
  return Math.floor(diffMs / (1000 * 60 * 60 * 24));
}

function statusFor(repo) {
  const d = daysAgo(repo.pushed_at);
  if (d <= 3) return "🟢 active";
  if (d <= 14) return "🟡 warm";
  return "⚪ idle";
}

function buildTable(repos) {
  const filtered = repos
    .filter((r) => !r.fork && !r.archived)
    .sort((a, b) => new Date(b.pushed_at) - new Date(a.pushed_at))
    .slice(0, 8);

  const totalStars = repos.reduce((sum, r) => sum + (r.stargazers_count || 0), 0);
  const totalRepos = repos.filter((r) => !r.fork).length;

  const rows = filtered
    .map((r) => {
      const name = `[${r.name}](${r.html_url})`;
      const lang = r.language || "—";
      const stars = r.stargazers_count ?? 0;
      const updated = `${daysAgo(r.pushed_at)}d ago`;
      return `| ${name} | ${lang} | ${stars}⭐ | ${updated} | ${statusFor(r)} |`;
    })
    .join("\n");

  const timestamp = new Date().toISOString().replace("T", " ").slice(0, 16) + " UTC";

  return `**Last synced:** \`${timestamp}\`  ·  **Repos:** ${totalRepos}  ·  **Total stars:** ${totalStars}

| Project | Language | Stars | Last push | Status |
|---|---|---|---|---|
${rows}`;
}

async function main() {
  const repos = await fetchRepos();
  const table = buildTable(repos);

  const readme = fs.readFileSync(README_PATH, "utf8");
  const startIdx = readme.indexOf(START_MARKER);
  const endIdx = readme.indexOf(END_MARKER);

  if (startIdx === -1 || endIdx === -1) {
    throw new Error("Dashboard markers not found in README.md");
  }

  const before = readme.slice(0, startIdx + START_MARKER.length);
  const after = readme.slice(endIdx);

  const updated = `${before}\n${table}\n${after}`;
  fs.writeFileSync(README_PATH, updated, "utf8");

  console.log("Dashboard section updated.");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
