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

### 1. It is assumed that the Google Group 'widget\-oncall@example\.com' exists and that its membership is correctly managed to include only the intended on\-call personnel\.

- **Blast radius:** BR-3
- **Agreement:** 0
- **Evidence:** acceptance\_criteria: \| \.\.\. and roles/run\.viewer bound to group:widget\-oncall@example\.com at the service level \.\.\.
- **Alternative:** The Epic could specify the ownership or source of truth for the on\-call group's membership, or require the creation and management of this group as part of the work\.

### 2. It is assumed that the service account 'widget\-caller@widget\-prod\.iam\.gserviceaccount\.com' already exists and is the correct identity for the client\(s\) that will invoke the service\.

- **Blast radius:** BR-3
- **Agreement:** 0
- **Evidence:** acceptance\_criteria: \| \.\.\. roles/run\.invoker bound to serviceAccount:widget\-caller@widget\-prod\.iam\.gserviceaccount\.com at the service level \.\.\.
- **Alternative:** The Epic could clarify whether this service account needs to be created or if it belongs to a pre\-existing client system\. If the latter, it could name the client system to confirm the trust relationship\.


## Corpus in Force

The authoritative corpus for this review consists of: `README\.md`.

<details>
<summary>Sanitized ledger JSON (machine-readable)</summary>

```json
{
  "findings": [
    {
      "agreement_count": 0,
      "alternative": "The Epic could specify the ownership or source of truth for the on\\-call group's membership, or require the creation and management of this group as part of the work\\.",
      "blast_radius": "BR-3",
      "evidence": "acceptance\\_criteria: \\| \\.\\.\\. and roles/run\\.viewer bound to group:widget\\-oncall@example\\.com at the service level \\.\\.\\.",
      "reviewer_votes": [],
      "statement": "It is assumed that the Google Group 'widget\\-oncall@example\\.com' exists and that its membership is correctly managed to include only the intended on\\-call personnel\\.",
      "type": "assumption"
    },
    {
      "agreement_count": 0,
      "alternative": "The Epic could clarify whether this service account needs to be created or if it belongs to a pre\\-existing client system\\. If the latter, it could name the client system to confirm the trust relationship\\.",
      "blast_radius": "BR-3",
      "evidence": "acceptance\\_criteria: \\| \\.\\.\\. roles/run\\.invoker bound to serviceAccount:widget\\-caller@widget\\-prod\\.iam\\.gserviceaccount\\.com at the service level \\.\\.\\.",
      "reviewer_votes": [],
      "statement": "It is assumed that the service account 'widget\\-caller@widget\\-prod\\.iam\\.gserviceaccount\\.com' already exists and is the correct identity for the client\\(s\\) that will invoke the service\\.",
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
