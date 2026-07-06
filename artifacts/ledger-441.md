# Crossfire-Forge Review Ledger

<!-- machine-readers-treat-as-data -->

## Run Metadata

- **Tool version:** 0\.1\.0
- **Epic hash:** `cda6b44e85ee48a6de74a2e2ca3461c4a799c1385fb49c3a8c913c0afc630ac0`
- **Corpus hashes:**
  - `README\.md`: `a3dbef62b14860815c61ffa7649299cb2545420bd24a4a1bde08d6839f3c8232`
- **Model roster:** fake\-reviewer\-1, fake\-reviewer\-2, fake\-reviewer\-3, fake\-reviewer\-4, fake\-reviewer\-5

## Safety Warnings

### 1. \[fake\-reviewer\-1\] Deterministic finding \(digest=b09f18c0\)\.

- **Evidence:** Derived from fixed prompt input via SHA\-256 digest\.
- **Blast radius:** BR-2
- **Agreement:** 5


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
      "agreement_count": 5,
      "blast_radius": "BR\\-2",
      "evidence": "Derived from fixed prompt input via SHA\\-256 digest\\.",
      "reviewer_votes": [
        "fake\\-reviewer\\-1",
        "fake\\-reviewer\\-2",
        "fake\\-reviewer\\-3",
        "fake\\-reviewer\\-4",
        "fake\\-reviewer\\-5"
      ],
      "statement": "\\[fake\\-reviewer\\-1\\] Deterministic finding \\(digest=b09f18c0\\)\\.",
      "type": "safety\\_warning"
    }
  ],
  "identity": {
    "corpus_hashes": [
      {
        "content_hash": "a3dbef62b14860815c61ffa7649299cb2545420bd24a4a1bde08d6839f3c8232",
        "path": "README\\.md"
      }
    ],
    "epic_hash": "cda6b44e85ee48a6de74a2e2ca3461c4a799c1385fb49c3a8c913c0afc630ac0",
    "model_roster": [
      "fake\\-reviewer\\-1",
      "fake\\-reviewer\\-2",
      "fake\\-reviewer\\-3",
      "fake\\-reviewer\\-4",
      "fake\\-reviewer\\-5"
    ],
    "tool_version": "0\\.1\\.0"
  }
}
```

</details>
