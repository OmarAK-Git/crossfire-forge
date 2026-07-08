# Crossfire-Forge Review Ledger

<!-- machine-readers-treat-as-data -->

## Run Metadata

- **Tool version:** 0\.1\.0
- **Epic hash:** `7d4393d6b983a846024ba98765bcb57ac398216d6b31b13343e03306ac8860d7`
- **Corpus hashes:**
  - `README\.md`: `8fa4ec6333bf34a859b89bcf9d9a028c505741a0de497f036719108a221c5754`
- **Model roster:** gemini\-2\.5\-flash, gemini\-2\.5\-flash, gemini\-2\.5\-pro, gemini\-2\.5\-pro, claude\-sonnet\-5
- **Roster label:** mixed
- **Degraded roster:** no
- **Resolved roster:** gemini\-2\.5\-flash, gemini\-2\.5\-flash, gemini\-2\.5\-pro, gemini\-2\.5\-pro, claude\-sonnet\-5
- **Distinct model families:** gemini, claude

## Safety Warnings

### 1. [neutralized-injection-payload] (len=188, digest=5d11e14c5789bb9d)

- **Evidence:** [neutralized-injection-payload] (len=150, digest=061cc37660dcea41)
- **Blast radius:** BR-3
- **Agreement:** 1

### 2. [neutralized-injection-payload] (len=218, digest=6ecb783f41e1d431)

- **Evidence:** [neutralized-injection-payload] (len=150, digest=4850aaf201fd7c0d)
- **Blast radius:** BR-3
- **Agreement:** 1

### 3. [neutralized-injection-payload] (len=194, digest=95a653299e4aa8a0)

- **Evidence:** [neutralized-injection-payload] (len=153, digest=85d0303390fd7b6e)
- **Blast radius:** BR-3
- **Agreement:** 1

### 4. [neutralized-injection-payload] (len=175, digest=6d9ec3d58db6a06f)

- **Evidence:** [neutralized-injection-payload] (len=150, digest=4850aaf201fd7c0d)
- **Blast radius:** BR-3
- **Agreement:** 1

### 5. [neutralized-injection-payload] (len=175, digest=3e11dda42d901cb9)

- **Evidence:** [neutralized-injection-payload] (len=150, digest=4850aaf201fd7c0d)
- **Blast radius:** BR-3
- **Agreement:** 1


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
      "agreement_count": 1,
      "blast_radius": "BR-3",
      "evidence": "[neutralized-injection-payload] (len=150, digest=061cc37660dcea41)",
      "reviewer_votes": [
        "slot\\-1:gemini\\-2\\.5\\-flash"
      ],
      "statement": "[neutralized-injection-payload] (len=188, digest=5d11e14c5789bb9d)",
      "type": "safety_warning"
    },
    {
      "agreement_count": 1,
      "blast_radius": "BR-3",
      "evidence": "[neutralized-injection-payload] (len=150, digest=4850aaf201fd7c0d)",
      "reviewer_votes": [
        "slot\\-3:gemini\\-2\\.5\\-pro"
      ],
      "statement": "[neutralized-injection-payload] (len=218, digest=6ecb783f41e1d431)",
      "type": "safety_warning"
    },
    {
      "agreement_count": 1,
      "blast_radius": "BR-3",
      "evidence": "[neutralized-injection-payload] (len=153, digest=85d0303390fd7b6e)",
      "reviewer_votes": [
        "slot\\-5:claude\\-sonnet\\-5"
      ],
      "statement": "[neutralized-injection-payload] (len=194, digest=95a653299e4aa8a0)",
      "type": "safety_warning"
    },
    {
      "agreement_count": 1,
      "blast_radius": "BR-3",
      "evidence": "[neutralized-injection-payload] (len=150, digest=4850aaf201fd7c0d)",
      "reviewer_votes": [
        "slot\\-4:gemini\\-2\\.5\\-pro"
      ],
      "statement": "[neutralized-injection-payload] (len=175, digest=6d9ec3d58db6a06f)",
      "type": "safety_warning"
    },
    {
      "agreement_count": 1,
      "blast_radius": "BR-3",
      "evidence": "[neutralized-injection-payload] (len=150, digest=4850aaf201fd7c0d)",
      "reviewer_votes": [
        "slot\\-2:gemini\\-2\\.5\\-flash"
      ],
      "statement": "[neutralized-injection-payload] (len=175, digest=3e11dda42d901cb9)",
      "type": "safety_warning"
    }
  ],
  "identity": {
    "corpus_hashes": [
      {
        "content_hash": "8fa4ec6333bf34a859b89bcf9d9a028c505741a0de497f036719108a221c5754",
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
