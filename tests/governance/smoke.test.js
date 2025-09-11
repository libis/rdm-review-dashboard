// Simple governance smoke test to verify workflows and repository metadata are present.
// This is intentionally minimal and fast.

const fs = require('fs');
const path = require('path');

function expect(condition, message) {
  if (!condition) {
    console.error(`SMOKE FAIL: ${message}`);
    process.exit(1);
  }
}

function exists(p) {
  return fs.existsSync(path.resolve(process.cwd(), p));
}

// Checks
const files = [
  '.github/workflows/ai-governance.yml',
  '.github/workflows/pr-governance.yml',
  '.github/workflows/workflow-lint.yml',
  '.github/pull_request_template.md',
  'ai-context.md',
];

for (const f of files) {
  console.log(`Check: ${f}`);
  expect(exists(f), `Missing required file: ${f}`);
}

console.log('Governance smoke test passed.');
