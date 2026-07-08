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

### 1. The Epic assumes that the \`roles/run\.viewer\` role provides sufficient permissions for the on\-call group to perform all necessary incident response and operational tasks\.

- **Blast radius:** BR-3
- **Agreement:** 1
- **Evidence:** acceptance\_criteria: \.\.\. and roles/run\.viewer bound to group:widget\-oncall@example\.com at the service level \(least privilege; no project\-level grants\)
- **Alternative:** Verify with the on\-call team that \`roles/run\.viewer\` permissions are sufficient for their operational needs \(e\.g\., debugging, viewing logs, checking status\)\. If additional permissions are required, consider creating a custom role that grants only the necessary extra permissions to maintain least privilege\.

### 2. The Epic assumes that the required network infrastructure, such as a producer VPC and a correctly configured Service Attachment, is already in place to support the \`private\-service\-connect\` security posture\.

- **Blast radius:** BR-3
- **Agreement:** 1
- **Evidence:** The Epic specifies \`security\_posture: private\-service\-connect\` without defining or referencing the specific underlying network resources or service attachment, creating ambiguity about which network boundary the service will be exposed on\.
- **Alternative:** The Epic could explicitly reference the target VPC network and Service Attachment to ensure the service is connected to the intended network boundary\.

### 3. The Epic assumes a quota management system exists to monitor and enforce the specified \`quota\_budget\`\.

- **Blast radius:** BR-2
- **Agreement:** 1
- **Evidence:** The Epic specifies \`quota\_budget: 5000\_vcpu\_hours\` without defining the mechanism for its enforcement or the consequences of exceeding it\.
- **Alternative:** The Epic could reference the specific quota project, alerting policies, or other mechanisms responsible for enforcing the budget\.

### 4. The Epic assumes that a monitoring and observability system capable of accurately measuring and reporting the '99\.9% uptime over 30 days' SLA for the widget service is either already in place or will be provisioned\.

- **Blast radius:** BR-2
- **Agreement:** 1
- **Evidence:** acceptance\_criteria: '\- 99\.9% uptime over 30 days'
- **Alternative:** Explicitly state the monitoring system to be used and who is responsible for its configuration for this service, or acknowledge that such a system needs to be established\.

### 5. The Epic assumes that the necessary Private Service Connect \(PSC\) infrastructure, including VPC networks and service attachments, is already established or will be provisioned as a prerequisite for deploying the widget service\.

- **Blast radius:** BR-2
- **Agreement:** 1
- **Evidence:** security\_posture: private\-service\-connect, acceptance\_criteria: 'ingress is restricted to internal traffic through the private\-service\-connect endpoint'
- **Alternative:** Define the responsibility and timeline for provisioning the PSC infrastructure or confirm its pre\-existence\.

### 6. The Epic assumes that the specified IAM service account \(\`widget\-caller@widget\-prod\.iam\.gserviceaccount\.com\`\) and IAM group \(\`widget\-oncall@example\.com\`\) either already exist or will be provisioned as a prerequisite for the service deployment\.

- **Blast radius:** BR-2
- **Agreement:** 1
- **Evidence:** acceptance\_criteria: 'Access control documented and enforced: roles/run\.invoker bound to serviceAccount:widget\-caller@widget\-prod\.iam\.gserviceaccount\.com at the service level, and roles/run\.viewer bound to group:widget\-oncall@example\.com at the service level'
- **Alternative:** Explicitly state the responsibility and process for creating or verifying the existence of these IAM principals\.

### 7. The Epic specifies a \`quota\_budget\` of \`5000\_vcpu\_hours\` without referencing any capacity planning, load testing, or cost analysis to justify this specific value\.

- **Blast radius:** BR-2
- **Agreement:** 1
- **Evidence:** quota\_budget: 5000\_vcpu\_hours
- **Alternative:** Base the quota budget on data from load testing, historical usage from similar services, or a formal capacity planning exercise\. This ensures the budget is sufficient to avoid service disruption while preventing resource over\-allocation\.


## Corpus in Force

The authoritative corpus for this review consists of: `README\.md`.

<details>
<summary>Sanitized ledger JSON (machine-readable)</summary>

```json
{
  "findings": [
    {
      "agreement_count": 1,
      "alternative": "The Epic could reference the specific quota project, alerting policies, or other mechanisms responsible for enforcing the budget\\.",
      "blast_radius": "BR-2",
      "evidence": "The Epic specifies \\`quota\\_budget: 5000\\_vcpu\\_hours\\` without defining the mechanism for its enforcement or the consequences of exceeding it\\.",
      "reviewer_votes": [
        "slot\\-4:gemini\\-2\\.5\\-pro"
      ],
      "statement": "The Epic assumes a quota management system exists to monitor and enforce the specified \\`quota\\_budget\\`\\.",
      "type": "assumption"
    },
    {
      "agreement_count": 1,
      "alternative": "Explicitly state the monitoring system to be used and who is responsible for its configuration for this service, or acknowledge that such a system needs to be established\\.",
      "blast_radius": "BR-2",
      "evidence": "acceptance\\_criteria: '\\- 99\\.9% uptime over 30 days'",
      "reviewer_votes": [
        "slot\\-1:gemini\\-2\\.5\\-flash"
      ],
      "statement": "The Epic assumes that a monitoring and observability system capable of accurately measuring and reporting the '99\\.9% uptime over 30 days' SLA for the widget service is either already in place or will be provisioned\\.",
      "type": "assumption"
    },
    {
      "agreement_count": 1,
      "alternative": "Verify with the on\\-call team that \\`roles/run\\.viewer\\` permissions are sufficient for their operational needs \\(e\\.g\\., debugging, viewing logs, checking status\\)\\. If additional permissions are required, consider creating a custom role that grants only the necessary extra permissions to maintain least privilege\\.",
      "blast_radius": "BR-3",
      "evidence": "acceptance\\_criteria: \\.\\.\\. and roles/run\\.viewer bound to group:widget\\-oncall@example\\.com at the service level \\(least privilege; no project\\-level grants\\)",
      "reviewer_votes": [
        "slot\\-3:gemini\\-2\\.5\\-pro"
      ],
      "statement": "The Epic assumes that the \\`roles/run\\.viewer\\` role provides sufficient permissions for the on\\-call group to perform all necessary incident response and operational tasks\\.",
      "type": "assumption"
    },
    {
      "agreement_count": 1,
      "alternative": "Define the responsibility and timeline for provisioning the PSC infrastructure or confirm its pre\\-existence\\.",
      "blast_radius": "BR-2",
      "evidence": "security\\_posture: private\\-service\\-connect, acceptance\\_criteria: 'ingress is restricted to internal traffic through the private\\-service\\-connect endpoint'",
      "reviewer_votes": [
        "slot\\-1:gemini\\-2\\.5\\-flash"
      ],
      "statement": "The Epic assumes that the necessary Private Service Connect \\(PSC\\) infrastructure, including VPC networks and service attachments, is already established or will be provisioned as a prerequisite for deploying the widget service\\.",
      "type": "assumption"
    },
    {
      "agreement_count": 1,
      "alternative": "The Epic could explicitly reference the target VPC network and Service Attachment to ensure the service is connected to the intended network boundary\\.",
      "blast_radius": "BR-3",
      "evidence": "The Epic specifies \\`security\\_posture: private\\-service\\-connect\\` without defining or referencing the specific underlying network resources or service attachment, creating ambiguity about which network boundary the service will be exposed on\\.",
      "reviewer_votes": [
        "slot\\-4:gemini\\-2\\.5\\-pro"
      ],
      "statement": "The Epic assumes that the required network infrastructure, such as a producer VPC and a correctly configured Service Attachment, is already in place to support the \\`private\\-service\\-connect\\` security posture\\.",
      "type": "assumption"
    },
    {
      "agreement_count": 1,
      "alternative": "Explicitly state the responsibility and process for creating or verifying the existence of these IAM principals\\.",
      "blast_radius": "BR-2",
      "evidence": "acceptance\\_criteria: 'Access control documented and enforced: roles/run\\.invoker bound to serviceAccount:widget\\-caller@widget\\-prod\\.iam\\.gserviceaccount\\.com at the service level, and roles/run\\.viewer bound to group:widget\\-oncall@example\\.com at the service level'",
      "reviewer_votes": [
        "slot\\-1:gemini\\-2\\.5\\-flash"
      ],
      "statement": "The Epic assumes that the specified IAM service account \\(\\`widget\\-caller@widget\\-prod\\.iam\\.gserviceaccount\\.com\\`\\) and IAM group \\(\\`widget\\-oncall@example\\.com\\`\\) either already exist or will be provisioned as a prerequisite for the service deployment\\.",
      "type": "assumption"
    },
    {
      "agreement_count": 1,
      "alternative": "Base the quota budget on data from load testing, historical usage from similar services, or a formal capacity planning exercise\\. This ensures the budget is sufficient to avoid service disruption while preventing resource over\\-allocation\\.",
      "blast_radius": "BR-2",
      "evidence": "quota\\_budget: 5000\\_vcpu\\_hours",
      "reviewer_votes": [
        "slot\\-3:gemini\\-2\\.5\\-pro"
      ],
      "statement": "The Epic specifies a \\`quota\\_budget\\` of \\`5000\\_vcpu\\_hours\\` without referencing any capacity planning, load testing, or cost analysis to justify this specific value\\.",
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
