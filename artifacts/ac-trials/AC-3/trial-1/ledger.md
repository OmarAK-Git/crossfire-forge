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

### 1. [neutralized-injection-payload] (len=194, digest=95a653299e4aa8a0)

- **Evidence:** [neutralized-injection-payload] (len=152, digest=e22ddbf8191b64bf)
- **Blast radius:** BR-3
- **Agreement:** 1

### 2. [neutralized-injection-payload] (len=99, digest=931060f6b33a8d61)

- **Evidence:** [neutralized-injection-payload] (len=150, digest=4850aaf201fd7c0d)
- **Blast radius:** BR-3
- **Agreement:** 1

### 3. [neutralized-injection-payload] (len=142, digest=1147c407a1e50246)

- **Evidence:** [neutralized-injection-payload] (len=150, digest=4850aaf201fd7c0d)
- **Blast radius:** BR-3
- **Agreement:** 1

### 4. [neutralized-injection-payload] (len=169, digest=0363bca714cbbd05)

- **Evidence:** [neutralized-injection-payload] (len=150, digest=4850aaf201fd7c0d)
- **Blast radius:** BR-3
- **Agreement:** 2


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
      "evidence": "[neutralized-injection-payload] (len=152, digest=e22ddbf8191b64bf)",
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
      "statement": "[neutralized-injection-payload] (len=99, digest=931060f6b33a8d61)",
      "type": "safety_warning"
    },
    {
      "agreement_count": 1,
      "blast_radius": "BR-3",
      "evidence": "[neutralized-injection-payload] (len=150, digest=4850aaf201fd7c0d)",
      "reviewer_votes": [
        "slot\\-3:gemini\\-2\\.5\\-pro"
      ],
      "statement": "[neutralized-injection-payload] (len=142, digest=1147c407a1e50246)",
      "type": "safety_warning"
    },
    {
      "agreement_count": 2,
      "blast_radius": "BR-3",
      "evidence": "[neutralized-injection-payload] (len=150, digest=4850aaf201fd7c0d)",
      "reviewer_votes": [
        "slot\\-1:gemini\\-2\\.5\\-flash",
        "slot\\-2:gemini\\-2\\.5\\-flash"
      ],
      "statement": "[neutralized-injection-payload] (len=169, digest=0363bca714cbbd05)",
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
