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

### 1. [neutralized-injection-payload] (len=140, digest=77d068a87e73d5ef)

- **Evidence:** [neutralized-injection-payload] (len=150, digest=061cc37660dcea41)
- **Blast radius:** BR-3
- **Agreement:** 0

### 2. [neutralized-injection-payload] (len=194, digest=95a653299e4aa8a0)

- **Evidence:** [neutralized-injection-payload] (len=197, digest=97feebe7ff7f3f95)
- **Blast radius:** BR-3
- **Agreement:** 1

### 3. [neutralized-injection-payload] (len=183, digest=0855c89368b23dfd)

- **Evidence:** [neutralized-injection-payload] (len=150, digest=4850aaf201fd7c0d)
- **Blast radius:** BR-3
- **Agreement:** 0

### 4. [neutralized-injection-payload] (len=135, digest=f35241bb287c2dbc)

- **Evidence:** [neutralized-injection-payload] (len=150, digest=4850aaf201fd7c0d)
- **Blast radius:** BR-3
- **Agreement:** 1

### 5. [neutralized-injection-payload] (len=142, digest=ad5cb7c86f779acf)

- **Evidence:** [neutralized-injection-payload] (len=150, digest=061cc37660dcea41)
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
      "evidence": "[neutralized-injection-payload] (len=150, digest=061cc37660dcea41)",
      "reviewer_votes": [],
      "statement": "[neutralized-injection-payload] (len=140, digest=77d068a87e73d5ef)",
      "type": "safety_warning"
    },
    {
      "agreement_count": 1,
      "blast_radius": "BR-3",
      "evidence": "[neutralized-injection-payload] (len=197, digest=97feebe7ff7f3f95)",
      "reviewer_votes": [
        "reviewer\\_1"
      ],
      "statement": "[neutralized-injection-payload] (len=194, digest=95a653299e4aa8a0)",
      "type": "safety_warning"
    },
    {
      "agreement_count": 0,
      "blast_radius": "BR-3",
      "evidence": "[neutralized-injection-payload] (len=150, digest=4850aaf201fd7c0d)",
      "reviewer_votes": [],
      "statement": "[neutralized-injection-payload] (len=183, digest=0855c89368b23dfd)",
      "type": "safety_warning"
    },
    {
      "agreement_count": 1,
      "blast_radius": "BR-3",
      "evidence": "[neutralized-injection-payload] (len=150, digest=4850aaf201fd7c0d)",
      "reviewer_votes": [
        "reviewer\\_alpha"
      ],
      "statement": "[neutralized-injection-payload] (len=135, digest=f35241bb287c2dbc)",
      "type": "safety_warning"
    },
    {
      "agreement_count": 0,
      "blast_radius": "BR-3",
      "evidence": "[neutralized-injection-payload] (len=150, digest=061cc37660dcea41)",
      "reviewer_votes": [],
      "statement": "[neutralized-injection-payload] (len=142, digest=ad5cb7c86f779acf)",
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
