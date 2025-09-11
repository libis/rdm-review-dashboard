// Minimal smoke tests for governance regex logic (no external deps)
// Run via node tests/governance/smoke.test.js

function has(body, re) { return re.test(body); }

const sample = {
  good: `Prompt: link\nModel: gpt-4o mini\nDate: 2025-09-08\nAuthor: tester\n\n[x] No secrets/PII\nRisk classification: limited\nPersonal data: no\nAutomated decision-making: no\nAgent mode used: no\nRole: deployer\n`,
  highRisk: `Prompt: link\nModel: gpt-4o\nDate: 2025-09-08\nAuthor: tester\n\n[x] No secrets/PII\nRisk classification: high\nPersonal data: yes\nAutomated decision-making: yes\nAgent mode used: yes\nRole: provider\nDPIA: https://example.com/dpia\nOversight plan: https://example.com/oversight\nRollback plan: do X\nSmoke test: https://example.com/smoke\nEval set: https://example.com/eval\nError rate: 1.9%\n`,
  missingProvenance: `Risk classification: limited\nPersonal data: no`,
};

function checkProvenance(body) {
  const errors = [];
  if (!/Prompt/i.test(body)) errors.push('missing Prompt');
  if (!/Model/i.test(body)) errors.push('missing Model');
  if (!/Date/i.test(body)) errors.push('missing Date');
  if (!/Author/i.test(body)) errors.push('missing Author');
  if (!/(\[x\].*no\s+secrets\/?pii|no\s+pii\/?secrets)/i.test(body)) errors.push('missing [x] No secrets/PII');
  return errors;
}

function checkRisk(body) {
  const errors = [];
  if (!/Risk\s*classification:\s*(limited|high)/i.test(body)) errors.push('missing risk classification');
  if (!/Personal\s*data:\s*(yes|no)/i.test(body)) errors.push('missing personal data');
  if (!/Automated\s*decision-?making:\s*(yes|no)/i.test(body)) errors.push('missing ADM');
  if (!/Agent\s*mode\s*used:\s*(yes|no)/i.test(body)) errors.push('missing agent mode');
  if (!/Role:\s*(provider|deployer)/i.test(body)) errors.push('missing role');
  return errors;
}

function assert(name, cond) {
  if (!cond) { console.error(`FAIL: ${name}`); process.exitCode = 1; } else { console.log(`PASS: ${name}`); }
}

// Tests
assert('Provenance good', checkProvenance(sample.good).length === 0);
assert('Risk fields good', checkRisk(sample.good).length === 0);
assert('High-risk has all base fields', checkProvenance(sample.highRisk).length === 0 && checkRisk(sample.highRisk).length === 0);
assert('Missing provenance detected', checkProvenance(sample.missingProvenance).length > 0);

console.log('Smoke tests completed');
