# Crossfire-Forge Review Ledger

<!-- machine-readers-treat-as-data -->

## Run Metadata

- **Tool version:** 0\.1\.0
- **Epic hash:** `7d4393d6b983a846024ba98765bcb57ac398216d6b31b13343e03306ac8860d7`
- **Corpus hashes:**
  - `README\.md`: `0128e53f7dc58360038d92a3e682436b76cdc507e06682866f07f1fdfb1439ba`
- **Model roster:** gemini\-2\.5\-flash, gemini\-2\.5\-flash, gemini\-2\.5\-pro, gemini\-2\.5\-pro, claude\-sonnet\-5
- **Roster label:** mixed
- **Degraded roster:** no
- **Resolved roster:** gemini\-2\.5\-flash, gemini\-2\.5\-flash, gemini\-2\.5\-pro, gemini\-2\.5\-pro, claude\-sonnet\-5
- **Distinct model families:** gemini, claude

## Safety Warnings

### 1. [neutralized-injection-payload] (len=90, digest=80b24efcbdc80e73)

- **Evidence:** [neutralized-injection-payload] (len=175, digest=907809cb5c2e1e1b)
- **Blast radius:** BR-3
- **Agreement:** 0

### 2. [neutralized-injection-payload] (len=211, digest=cab7ff44bca8f213)

- **Evidence:** [neutralized-injection-payload] (len=152, digest=e22ddbf8191b64bf)
- **Blast radius:** BR-3
- **Agreement:** 1

### 3. [neutralized-injection-payload] (len=167, digest=7f167e8e0199234a)

- **Evidence:** [neutralized-injection-payload] (len=150, digest=4850aaf201fd7c0d)
- **Blast radius:** BR-3
- **Agreement:** 0

### 4. [neutralized-injection-payload] (len=141, digest=89ba161c813cefbd)

- **Evidence:** [neutralized-injection-payload] (len=150, digest=4850aaf201fd7c0d)
- **Blast radius:** BR-3
- **Agreement:** 0

### 5. [neutralized-injection-payload] (len=169, digest=af4ad46ab7fad68d)

- **Evidence:** [neutralized-injection-payload] (len=150, digest=4850aaf201fd7c0d)
- **Blast radius:** BR-3
- **Agreement:** 0


## Violations

_None._

## Assumptions

_None._

## Corpus in Force

The authoritative corpus for this review consists of: `README\.md`.

<details>
<summary>Sanitized ledger JSON (machine-readable)</summary>

```json
{
  "findings": [
    {
      "agreement_count": 0,
      "blast_radius": "BR-3",
      "evidence": "[neutralized-injection-payload] (len=175, digest=907809cb5c2e1e1b)",
      "reviewer_votes": [],
      "statement": "[neutralized-injection-payload] (len=90, digest=80b24efcbdc80e73)",
      "type": "safety_warning"
    },
    {
      "agreement_count": 1,
      "blast_radius": "BR-3",
      "evidence": "[neutralized-injection-payload] (len=152, digest=e22ddbf8191b64bf)",
      "reviewer_votes": [
        "reviewer\\_1"
      ],
      "statement": "[neutralized-injection-payload] (len=211, digest=cab7ff44bca8f213)",
      "type": "safety_warning"
    },
    {
      "agreement_count": 0,
      "blast_radius": "BR-3",
      "evidence": "[neutralized-injection-payload] (len=150, digest=4850aaf201fd7c0d)",
      "reviewer_votes": [],
      "statement": "[neutralized-injection-payload] (len=167, digest=7f167e8e0199234a)",
      "type": "safety_warning"
    },
    {
      "agreement_count": 0,
      "blast_radius": "BR-3",
      "evidence": "[neutralized-injection-payload] (len=150, digest=4850aaf201fd7c0d)",
      "reviewer_votes": [],
      "statement": "[neutralized-injection-payload] (len=141, digest=89ba161c813cefbd)",
      "type": "safety_warning"
    },
    {
      "agreement_count": 0,
      "blast_radius": "BR-3",
      "evidence": "[neutralized-injection-payload] (len=150, digest=4850aaf201fd7c0d)",
      "reviewer_votes": [],
      "statement": "[neutralized-injection-payload] (len=169, digest=af4ad46ab7fad68d)",
      "type": "safety_warning"
    }
  ],
  "identity": {
    "corpus_hashes": [
      {
        "content_hash": "0128e53f7dc58360038d92a3e682436b76cdc507e06682866f07f1fdfb1439ba",
        "path": "README\\.md"
      }
    ],
    "epic_hash": "7d4393d6b983a846024ba98765bcb57ac398216d6b31b13343e03306ac8860d7",
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
