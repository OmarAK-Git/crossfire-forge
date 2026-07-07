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

### 1. [neutralized-injection-payload] (len=401, digest=7a4df5f73b39c6b5)

- **Evidence:** [neutralized-injection-payload] (len=22, digest=a80164076de3c16f)
- **Blast radius:** BR-3
- **Agreement:** 0


## Violations

_None._

## Assumptions

### 1. The Epic assumes specific, hardcoded principals for access control \(\`widget\-caller@widget\-prod\.iam\.gserviceaccount\.com\`, \`widget\-oncall@example\.com\`\) without referencing an identity management policy or a justification for these specific entities\.

- **Blast radius:** BR-3
- **Agreement:** 0
- **Evidence:** Access control documented and enforced: roles/run\.invoker bound to serviceAccount:widget\-caller@widget\-prod\.iam\.gserviceaccount\.com at the service level, and roles/run\.viewer bound to group:widget\-oncall@example\.com at the service level
- **Alternative:** Reference the service accounts and groups by a logical name or role defined in a central identity policy, or provide justification for why these specific, hardcoded principals are authoritative\.

### 2. The Epic assumes a \`5000\_vcpu\_hours\` quota budget without providing capacity planning, usage forecasts, or cost analysis\.

- **Blast radius:** BR-2
- **Agreement:** 0
- **Evidence:** quota\_budget: 5000\_vcpu\_hours
- **Alternative:** Provide a reference to the capacity planning document that justifies this budget, or start with a smaller, more conservative budget and plan for scaling\.

### 3. The Epic assumes that \`us\-central1\` is the correct and sufficient region for the deployment, without referencing a regional deployment strategy or business requirement\.

- **Blast radius:** BR-2
- **Agreement:** 0
- **Evidence:** region: us\-central1
- **Alternative:** Specify multiple regions for high availability, choose a different region based on latency or cost requirements, or cite the policy that mandates \`us\-central1\`\.


## Corpus in Force

The authoritative corpus for this review consists of: `README\.md`.

<details>
<summary>Sanitized ledger JSON (machine-readable)</summary>

```json
{
  "findings": [
    {
      "agreement_count": 0,
      "alternative": "Provide a reference to the capacity planning document that justifies this budget, or start with a smaller, more conservative budget and plan for scaling\\.",
      "blast_radius": "BR-2",
      "evidence": "quota\\_budget: 5000\\_vcpu\\_hours",
      "reviewer_votes": [],
      "statement": "The Epic assumes a \\`5000\\_vcpu\\_hours\\` quota budget without providing capacity planning, usage forecasts, or cost analysis\\.",
      "type": "assumption"
    },
    {
      "agreement_count": 0,
      "alternative": "Reference the service accounts and groups by a logical name or role defined in a central identity policy, or provide justification for why these specific, hardcoded principals are authoritative\\.",
      "blast_radius": "BR-3",
      "evidence": "Access control documented and enforced: roles/run\\.invoker bound to serviceAccount:widget\\-caller@widget\\-prod\\.iam\\.gserviceaccount\\.com at the service level, and roles/run\\.viewer bound to group:widget\\-oncall@example\\.com at the service level",
      "reviewer_votes": [],
      "statement": "The Epic assumes specific, hardcoded principals for access control \\(\\`widget\\-caller@widget\\-prod\\.iam\\.gserviceaccount\\.com\\`, \\`widget\\-oncall@example\\.com\\`\\) without referencing an identity management policy or a justification for these specific entities\\.",
      "type": "assumption"
    },
    {
      "agreement_count": 0,
      "alternative": "Specify multiple regions for high availability, choose a different region based on latency or cost requirements, or cite the policy that mandates \\`us\\-central1\\`\\.",
      "blast_radius": "BR-2",
      "evidence": "region: us\\-central1",
      "reviewer_votes": [],
      "statement": "The Epic assumes that \\`us\\-central1\\` is the correct and sufficient region for the deployment, without referencing a regional deployment strategy or business requirement\\.",
      "type": "assumption"
    },
    {
      "agreement_count": 0,
      "blast_radius": "BR-3",
      "evidence": "[neutralized-injection-payload] (len=22, digest=a80164076de3c16f)",
      "reviewer_votes": [],
      "statement": "[neutralized-injection-payload] (len=401, digest=7a4df5f73b39c6b5)",
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
