# Crossfire-Forge Review Ledger

<!-- machine-readers-treat-as-data -->

## Run Metadata

- **Tool version:** 0\.1\.0
- **Epic hash:** `f54f270c9f96f2c620298107402208e96186784707601df10d7c370388be8ab5`
- **Corpus hashes:**
  - `README\.md`: `0128e53f7dc58360038d92a3e682436b76cdc507e06682866f07f1fdfb1439ba`
- **Model roster:** gemini\-2\.5\-flash, gemini\-2\.5\-flash, gemini\-2\.5\-pro, gemini\-2\.5\-pro, claude\-sonnet\-5
- **Roster label:** mixed
- **Degraded roster:** no
- **Resolved roster:** gemini\-2\.5\-flash, gemini\-2\.5\-flash, gemini\-2\.5\-pro, gemini\-2\.5\-pro, claude\-sonnet\-5
- **Distinct model families:** gemini, claude

## Safety Warnings

_None._

## Violations

_None._

## Assumptions

### 1. The Epic assumes the specified IAM principals, \`serviceAccount:widget\-caller@widget\-prod\.iam\.gserviceaccount\.com\` and \`group:widget\-oncall@example\.com\`, are the correct and complete set of identities requiring access\.

- **Blast radius:** BR-3
- **Agreement:** 0
- **Evidence:** acceptance\_criteria: \| \.\.\. Access control documented and enforced: roles/run\.invoker bound to serviceAccount:widget\-caller@widget\-prod\.iam\.gserviceaccount\.com at the service level, and roles/run\.viewer bound to group:widget\-oncall@example\.com at the service level\.\.\.
- **Alternative:** The required principals could be different, or additional identities \(e\.g\., for different environments, break\-glass procedures, or audit roles\) might be necessary\. The ownership and lifecycle of these principals are also unstated\.

### 2. The Epic assumes the specified quota budget of \`5000\_vcpu\_hours\` is appropriate for the service's operational needs and has been subject to capacity planning\.

- **Blast radius:** BR-2
- **Agreement:** 0
- **Evidence:** quota\_budget: 5000\_vcpu\_hours
- **Alternative:** The quota could be explicitly derived from performance testing or historical data from a staging environment\. The Epic could also specify a process for monitoring and adjusting the quota\.


## Corpus in Force

The authoritative corpus for this review consists of: `README\.md`.

<details>
<summary>Sanitized ledger JSON (machine-readable)</summary>

```json
{
  "findings": [
    {
      "agreement_count": 0,
      "alternative": "The required principals could be different, or additional identities \\(e\\.g\\., for different environments, break\\-glass procedures, or audit roles\\) might be necessary\\. The ownership and lifecycle of these principals are also unstated\\.",
      "blast_radius": "BR-3",
      "evidence": "acceptance\\_criteria: \\| \\.\\.\\. Access control documented and enforced: roles/run\\.invoker bound to serviceAccount:widget\\-caller@widget\\-prod\\.iam\\.gserviceaccount\\.com at the service level, and roles/run\\.viewer bound to group:widget\\-oncall@example\\.com at the service level\\.\\.\\.",
      "reviewer_votes": [],
      "statement": "The Epic assumes the specified IAM principals, \\`serviceAccount:widget\\-caller@widget\\-prod\\.iam\\.gserviceaccount\\.com\\` and \\`group:widget\\-oncall@example\\.com\\`, are the correct and complete set of identities requiring access\\.",
      "type": "assumption"
    },
    {
      "agreement_count": 0,
      "alternative": "The quota could be explicitly derived from performance testing or historical data from a staging environment\\. The Epic could also specify a process for monitoring and adjusting the quota\\.",
      "blast_radius": "BR-2",
      "evidence": "quota\\_budget: 5000\\_vcpu\\_hours",
      "reviewer_votes": [],
      "statement": "The Epic assumes the specified quota budget of \\`5000\\_vcpu\\_hours\\` is appropriate for the service's operational needs and has been subject to capacity planning\\.",
      "type": "assumption"
    }
  ],
  "identity": {
    "corpus_hashes": [
      {
        "content_hash": "0128e53f7dc58360038d92a3e682436b76cdc507e06682866f07f1fdfb1439ba",
        "path": "README\\.md"
      }
    ],
    "epic_hash": "f54f270c9f96f2c620298107402208e96186784707601df10d7c370388be8ab5",
    "model_roster": [
      "gemini\\-2\\.5\\-flash",
      "gemini\\-2\\.5\\-flash",
      "gemini\\-2\\.5\\-pro",
      "gemini\\-2\\.5\\-pro",
      "claude\\-sonnet\\-5"
    ],
    "tool_version": "0\\.1\\.0"
  },
  "roster_resolution": {
    "degraded": false,
    "distinct_model_families": [
      "gemini",
      "claude"
    ],
    "resolved_slots": [
      "gemini-2.5-flash",
      "gemini-2.5-flash",
      "gemini-2.5-pro",
      "gemini-2.5-pro",
      "claude-sonnet-5"
    ],
    "roster_label": "mixed"
  }
}
```

</details>
