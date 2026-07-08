# Crossfire-Forge Review Ledger

<!-- machine-readers-treat-as-data -->

## Run Metadata

- **Tool version:** 0\.1\.0
- **Epic hash:** `e7e8fdcb4fcbfe84e3d97be7f1651a86587979784253142f35c86e37c953231a`
- **Corpus hashes:**
  - `README\.md`: `8fa4ec6333bf34a859b89bcf9d9a028c505741a0de497f036719108a221c5754`
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

### 1. A Shared VPC connector for egress is already available and correctly configured for the service\.

- **Blast radius:** BR-3
- **Agreement:** 1
- **Evidence:** egress is routed through the shared VPC connector with no public internet route
- **Alternative:** The Shared VPC connector is missing or misconfigured, leading to egress failures or unintended public internet access\.

### 2. It is assumed that the synthetic monitoring probe has a network path and the necessary permissions to access the internal\-only service\.

- **Blast radius:** BR-3
- **Agreement:** 1
- **Evidence:** The acceptance criteria require 'successful synthetic probes \(HTTP 200 on /healthz at 60\-second intervals\)' against a service where 'ingress is restricted to internal traffic through the existing psc\-widget private\-service\-connect endpoint'\. The Epic does not specify the probe's origin or how it will traverse this restricted network path and authenticate\.
- **Alternative:** Specify the origin of the synthetic probe \(e\.g\., a Cloud Monitoring uptime check configured to run from within the project's VPC\) and ensure its identity \(e\.g\., its service account\) is granted the \`roles/run\.invoker\` role to satisfy both network and IAM access controls\.

### 3. The \`psc\-widget\` Private Service Connect \(PSC\) endpoint and its associated service attachment are already provisioned and correctly configured in the shared VPC\.

- **Blast radius:** BR-3
- **Agreement:** 1
- **Evidence:** ingress is restricted to internal traffic through the existing psc\-widget private\-service\-connect endpoint \(service attachment provisioned in the shared VPC\), which is the sole ingress path for all internal consumers
- **Alternative:** The PSC endpoint or service attachment is missing or misconfigured, preventing internal ingress or exposing the service incorrectly\.

### 4. The IAM principals \`widget\-caller@widget\-prod\.iam\.gserviceaccount\.com\` and \`group:widget\-oncall@example\.com\` exist in the \`widget\-prod\` IAM inventory\.

- **Blast radius:** BR-3
- **Agreement:** 1
- **Evidence:** Access control documented and enforced: roles/run\.invoker bound to serviceAccount:widget\-caller@widget\-prod\.iam\.gserviceaccount\.com at the service level, and roles/run\.viewer bound to group:widget\-oncall@example\.com at the service level \.\.\. Both principals already exist in the widget\-prod IAM inventory\.
- **Alternative:** The specified IAM principals do not exist, leading to deployment failure or incorrect access control bindings\.

### 5. It is assumed that the default or an unstated \`max\-instances\` setting for the Cloud Run service is acceptable, as it is not specified alongside the \`min\-instances\` setting\.

- **Blast radius:** BR-2
- **Agreement:** 1
- **Evidence:** The Epic's acceptance criteria state that \`min\-instances is set to 1 to remove cold\-start gaps\`, but no corresponding \`max\-instances\` limit is defined to control peak scaling and cost\.
- **Alternative:** Explicitly specify a \`max\-instances\` value to provide a hard cap on concurrent instances, which complements the monthly \`quota\_budget\` and prevents unexpected scaling behavior or cost overruns\.

### 6. The 2026\-Q2 load test results \(peak 5\.8 vCPU sustained\) are accurate and the 20% headroom applied is sufficient to size the \`5000\_vcpu\_hours\` quota budget\.

- **Blast radius:** BR-2
- **Agreement:** 1
- **Evidence:** quota\_budget: 5000\_vcpu\_hours \.\.\. sized from the 2026\-Q2 load test \(peak 5\.8 vCPU sustained\) plus 20% headroom
- **Alternative:** The load test was inaccurate, or the headroom is insufficient, potentially leading to quota exhaustion and service unavailability\.

### 7. The \`widget\-prod Cloud Monitoring workspace\` exists and is configured for synthetic HTTP probes to \`/healthz\` at 60\-second intervals\.

- **Blast radius:** BR-2
- **Agreement:** 1
- **Evidence:** 99\.9% uptime over 30 days, measured as the fraction of successful synthetic probes \(HTTP 200 on /healthz at 60\-second intervals\) in the existing widget\-prod Cloud Monitoring workspace
- **Alternative:** The Cloud Monitoring workspace or the specific synthetic probes are not configured, preventing proper SLO measurement\.

### 8. The \`widget\-prod quota dashboard\` exists and is configured to enforce the specified \`quota\_budget\` as a hard limit with alerting at 80% usage\.

- **Blast radius:** BR-2
- **Agreement:** 1
- **Evidence:** it is enforced as a hard limit with alerting at 80% in the widget\-prod quota dashboard\.
- **Alternative:** The quota dashboard or its alerts are not configured as specified, leading to unmanaged quota consumption or missed operational alerts\.


## Corpus in Force

The authoritative corpus for this review consists of: `README\.md`.

<details>
<summary>Sanitized ledger JSON (machine-readable)</summary>

```json
{
  "findings": [
    {
      "agreement_count": 1,
      "alternative": "The Shared VPC connector is missing or misconfigured, leading to egress failures or unintended public internet access\\.",
      "blast_radius": "BR-3",
      "evidence": "egress is routed through the shared VPC connector with no public internet route",
      "reviewer_votes": [
        "slot\\-2:gemini\\-2\\.5\\-flash"
      ],
      "statement": "A Shared VPC connector for egress is already available and correctly configured for the service\\.",
      "type": "assumption"
    },
    {
      "agreement_count": 1,
      "alternative": "Explicitly specify a \\`max\\-instances\\` value to provide a hard cap on concurrent instances, which complements the monthly \\`quota\\_budget\\` and prevents unexpected scaling behavior or cost overruns\\.",
      "blast_radius": "BR-2",
      "evidence": "The Epic's acceptance criteria state that \\`min\\-instances is set to 1 to remove cold\\-start gaps\\`, but no corresponding \\`max\\-instances\\` limit is defined to control peak scaling and cost\\.",
      "reviewer_votes": [
        "slot\\-3:gemini\\-2\\.5\\-pro"
      ],
      "statement": "It is assumed that the default or an unstated \\`max\\-instances\\` setting for the Cloud Run service is acceptable, as it is not specified alongside the \\`min\\-instances\\` setting\\.",
      "type": "assumption"
    },
    {
      "agreement_count": 1,
      "alternative": "Specify the origin of the synthetic probe \\(e\\.g\\., a Cloud Monitoring uptime check configured to run from within the project's VPC\\) and ensure its identity \\(e\\.g\\., its service account\\) is granted the \\`roles/run\\.invoker\\` role to satisfy both network and IAM access controls\\.",
      "blast_radius": "BR-3",
      "evidence": "The acceptance criteria require 'successful synthetic probes \\(HTTP 200 on /healthz at 60\\-second intervals\\)' against a service where 'ingress is restricted to internal traffic through the existing psc\\-widget private\\-service\\-connect endpoint'\\. The Epic does not specify the probe's origin or how it will traverse this restricted network path and authenticate\\.",
      "reviewer_votes": [
        "slot\\-3:gemini\\-2\\.5\\-pro"
      ],
      "statement": "It is assumed that the synthetic monitoring probe has a network path and the necessary permissions to access the internal\\-only service\\.",
      "type": "assumption"
    },
    {
      "agreement_count": 1,
      "alternative": "The load test was inaccurate, or the headroom is insufficient, potentially leading to quota exhaustion and service unavailability\\.",
      "blast_radius": "BR-2",
      "evidence": "quota\\_budget: 5000\\_vcpu\\_hours \\.\\.\\. sized from the 2026\\-Q2 load test \\(peak 5\\.8 vCPU sustained\\) plus 20% headroom",
      "reviewer_votes": [
        "slot\\-2:gemini\\-2\\.5\\-flash"
      ],
      "statement": "The 2026\\-Q2 load test results \\(peak 5\\.8 vCPU sustained\\) are accurate and the 20% headroom applied is sufficient to size the \\`5000\\_vcpu\\_hours\\` quota budget\\.",
      "type": "assumption"
    },
    {
      "agreement_count": 1,
      "alternative": "The specified IAM principals do not exist, leading to deployment failure or incorrect access control bindings\\.",
      "blast_radius": "BR-3",
      "evidence": "Access control documented and enforced: roles/run\\.invoker bound to serviceAccount:widget\\-caller@widget\\-prod\\.iam\\.gserviceaccount\\.com at the service level, and roles/run\\.viewer bound to group:widget\\-oncall@example\\.com at the service level \\.\\.\\. Both principals already exist in the widget\\-prod IAM inventory\\.",
      "reviewer_votes": [
        "slot\\-2:gemini\\-2\\.5\\-flash"
      ],
      "statement": "The IAM principals \\`widget\\-caller@widget\\-prod\\.iam\\.gserviceaccount\\.com\\` and \\`group:widget\\-oncall@example\\.com\\` exist in the \\`widget\\-prod\\` IAM inventory\\.",
      "type": "assumption"
    },
    {
      "agreement_count": 1,
      "alternative": "The PSC endpoint or service attachment is missing or misconfigured, preventing internal ingress or exposing the service incorrectly\\.",
      "blast_radius": "BR-3",
      "evidence": "ingress is restricted to internal traffic through the existing psc\\-widget private\\-service\\-connect endpoint \\(service attachment provisioned in the shared VPC\\), which is the sole ingress path for all internal consumers",
      "reviewer_votes": [
        "slot\\-2:gemini\\-2\\.5\\-flash"
      ],
      "statement": "The \\`psc\\-widget\\` Private Service Connect \\(PSC\\) endpoint and its associated service attachment are already provisioned and correctly configured in the shared VPC\\.",
      "type": "assumption"
    },
    {
      "agreement_count": 1,
      "alternative": "The Cloud Monitoring workspace or the specific synthetic probes are not configured, preventing proper SLO measurement\\.",
      "blast_radius": "BR-2",
      "evidence": "99\\.9% uptime over 30 days, measured as the fraction of successful synthetic probes \\(HTTP 200 on /healthz at 60\\-second intervals\\) in the existing widget\\-prod Cloud Monitoring workspace",
      "reviewer_votes": [
        "slot\\-2:gemini\\-2\\.5\\-flash"
      ],
      "statement": "The \\`widget\\-prod Cloud Monitoring workspace\\` exists and is configured for synthetic HTTP probes to \\`/healthz\\` at 60\\-second intervals\\.",
      "type": "assumption"
    },
    {
      "agreement_count": 1,
      "alternative": "The quota dashboard or its alerts are not configured as specified, leading to unmanaged quota consumption or missed operational alerts\\.",
      "blast_radius": "BR-2",
      "evidence": "it is enforced as a hard limit with alerting at 80% in the widget\\-prod quota dashboard\\.",
      "reviewer_votes": [
        "slot\\-2:gemini\\-2\\.5\\-flash"
      ],
      "statement": "The \\`widget\\-prod quota dashboard\\` exists and is configured to enforce the specified \\`quota\\_budget\\` as a hard limit with alerting at 80% usage\\.",
      "type": "assumption"
    }
  ],
  "identity": {
    "corpus_hashes": [
      {
        "content_hash": "8fa4ec6333bf34a859b89bcf9d9a028c505741a0de497f036719108a221c5754",
        "path": "README\\.md"
      }
    ],
    "epic_hash": "e7e8fdcb4fcbfe84e3d97be7f1651a86587979784253142f35c86e37c953231a",
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
