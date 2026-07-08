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

### 1. The access control configuration relies on the pre\-existence and correct lifecycle management of the \`widget\-caller\` service account and the \`widget\-oncall\` group outside of this deployment's scope\.

- **Blast radius:** BR-3
- **Agreement:** 1
- **Evidence:** Both principals already exist in the widget\-prod IAM inventory\.
- **Alternative:** The deployment process could be enhanced to verify the existence of these principals, or even create/manage them, to make the service's deployment more self\-contained and less prone to external dependency failures\.

### 2. The Epic assumes that the 'shared VPC connector with no public internet route' is correctly provisioned and configured to reliably prevent any public internet egress for the service\.

- **Blast radius:** BR-3
- **Agreement:** 1
- **Evidence:** egress is routed through the shared VPC connector with no public internet route
- **Alternative:** Explicitly include a verification step or a task to provision and configure the shared VPC connector, ensuring strict adherence to the 'no public internet route' requirement\.

### 3. The Epic assumes the \`psc\-widget\` Private Service Connect endpoint and its underlying service attachment in the shared VPC are already provisioned, correctly configured for the new service's ingress, and fully operational\.

- **Blast radius:** BR-3
- **Agreement:** 1
- **Evidence:** ingress is restricted to internal traffic through the existing psc\-widget private\-service\-connect endpoint \(service attachment provisioned in the shared VPC\), which is the sole ingress path for all internal consumers
- **Alternative:** Explicitly include a verification step or a task to provision and configure the Private Service Connect endpoint and its service attachment as part of this Epic, ensuring it's ready before deployment\.

### 4. The grant of read\-only access to the on\-call group assumes that the documented escalation path via the deployment pipeline is sufficient for all operational incidents, and that direct write access is never required for emergency remediation\.

- **Blast radius:** BR-3
- **Agreement:** 1
- **Evidence:** read\-only access covers the on\-call runbook, which escalates writes to the deploy pipeline
- **Alternative:** Provide a break\-glass mechanism for the on\-call group to gain temporary, audited write access to the service for emergencies where the standard deployment pipeline is too slow or is part of the failure\.

### 5. The service's networking and security posture are dependent on an existing Private Service Connect endpoint in a shared VPC, which is managed outside the scope of this service's deployment\.

- **Blast radius:** BR-3
- **Agreement:** 1
- **Evidence:** ingress is restricted to internal traffic through the existing psc\-widget private\-service\-connect endpoint \(service attachment provisioned in the shared VPC\)
- **Alternative:** The deployment process could include a step to verify the existence and correct configuration of the specified PSC endpoint to prevent deployment failures or traffic black\-holing due to a misconfigured or missing dependency\.

### 6. The Epic assumes that the '2026\-Q2 load test' accurately predicts future production load, the '20% headroom' is sufficient for growth and spikes, and the 'widget\-prod quota dashboard' with 80% alerting is effective at preventing quota\-related outages\.

- **Blast radius:** BR-2
- **Agreement:** 1
- **Evidence:** The quota budget\.\.\. was sized from the 2026\-Q2 load test \(peak 5\.8 vCPU sustained\) plus 20% headroom, and is enforced as a hard limit with alerting at 80% in the widget\-prod quota dashboard\.
- **Alternative:** Mandate a review of the load test methodology and results for current relevance, and explicitly confirm the configuration and monitoring of the quota dashboard's alerting\.

### 7. The Epic assumes that the 'existing widget\-prod Cloud Monitoring workspace' is properly configured, accessible for the new service to report metrics, and capable of hosting the described synthetic probes\.

- **Blast radius:** BR-2
- **Agreement:** 1
- **Evidence:** 99\.9% uptime over 30 days, measured as the fraction of successful synthetic probes \(HTTP 200 on /healthz at 60\-second intervals\) in the existing widget\-prod Cloud Monitoring workspace
- **Alternative:** Explicitly include a task to verify the Cloud Monitoring workspace's readiness, confirm the service's permissions to publish metrics, and ensure synthetic probes can be created within it\.

### 8. The Epic assumes that the operational process where 'read\-only access covers the on\-call runbook, which escalates writes to the deploy pipeline' is a fully defined, reliable, and efficient mechanism for handling incidents requiring write access\.

- **Blast radius:** BR-2
- **Agreement:** 1
- **Evidence:** read\-only access covers the on\-call runbook, which escalates writes to the deploy pipeline
- **Alternative:** Mandate documentation or a review of the on\-call runbook and the deploy pipeline's escalation process to confirm it covers all necessary write operations and provides an acceptable Mean Time To Recovery \(MTTR\) for incidents\.

### 9. The Epic specifies setting \`min\-instances\` to 1 to meet the uptime SLO by avoiding cold starts, which assumes the continuous cost of an idle instance is an acceptable trade\-off against potential latency or availability dips during traffic scale\-up from zero\.

- **Blast radius:** BR-2
- **Agreement:** 1
- **Evidence:** min\-instances is set to 1 to remove cold\-start gaps
- **Alternative:** Set \`min\-instances\` to 0 to minimize costs during idle periods, accepting the risk of cold\-start latency which could affect the uptime metric for initial requests after a lull\.


## Corpus in Force

The authoritative corpus for this review consists of: `README\.md`.

<details>
<summary>Sanitized ledger JSON (machine-readable)</summary>

```json
{
  "findings": [
    {
      "agreement_count": 1,
      "alternative": "Mandate a review of the load test methodology and results for current relevance, and explicitly confirm the configuration and monitoring of the quota dashboard's alerting\\.",
      "blast_radius": "BR-2",
      "evidence": "The quota budget\\.\\.\\. was sized from the 2026\\-Q2 load test \\(peak 5\\.8 vCPU sustained\\) plus 20% headroom, and is enforced as a hard limit with alerting at 80% in the widget\\-prod quota dashboard\\.",
      "reviewer_votes": [
        "slot\\-1:gemini\\-2\\.5\\-flash"
      ],
      "statement": "The Epic assumes that the '2026\\-Q2 load test' accurately predicts future production load, the '20% headroom' is sufficient for growth and spikes, and the 'widget\\-prod quota dashboard' with 80% alerting is effective at preventing quota\\-related outages\\.",
      "type": "assumption"
    },
    {
      "agreement_count": 1,
      "alternative": "Explicitly include a task to verify the Cloud Monitoring workspace's readiness, confirm the service's permissions to publish metrics, and ensure synthetic probes can be created within it\\.",
      "blast_radius": "BR-2",
      "evidence": "99\\.9% uptime over 30 days, measured as the fraction of successful synthetic probes \\(HTTP 200 on /healthz at 60\\-second intervals\\) in the existing widget\\-prod Cloud Monitoring workspace",
      "reviewer_votes": [
        "slot\\-1:gemini\\-2\\.5\\-flash"
      ],
      "statement": "The Epic assumes that the 'existing widget\\-prod Cloud Monitoring workspace' is properly configured, accessible for the new service to report metrics, and capable of hosting the described synthetic probes\\.",
      "type": "assumption"
    },
    {
      "agreement_count": 1,
      "alternative": "Explicitly include a verification step or a task to provision and configure the shared VPC connector, ensuring strict adherence to the 'no public internet route' requirement\\.",
      "blast_radius": "BR-3",
      "evidence": "egress is routed through the shared VPC connector with no public internet route",
      "reviewer_votes": [
        "slot\\-1:gemini\\-2\\.5\\-flash"
      ],
      "statement": "The Epic assumes that the 'shared VPC connector with no public internet route' is correctly provisioned and configured to reliably prevent any public internet egress for the service\\.",
      "type": "assumption"
    },
    {
      "agreement_count": 1,
      "alternative": "Mandate documentation or a review of the on\\-call runbook and the deploy pipeline's escalation process to confirm it covers all necessary write operations and provides an acceptable Mean Time To Recovery \\(MTTR\\) for incidents\\.",
      "blast_radius": "BR-2",
      "evidence": "read\\-only access covers the on\\-call runbook, which escalates writes to the deploy pipeline",
      "reviewer_votes": [
        "slot\\-1:gemini\\-2\\.5\\-flash"
      ],
      "statement": "The Epic assumes that the operational process where 'read\\-only access covers the on\\-call runbook, which escalates writes to the deploy pipeline' is a fully defined, reliable, and efficient mechanism for handling incidents requiring write access\\.",
      "type": "assumption"
    },
    {
      "agreement_count": 1,
      "alternative": "Explicitly include a verification step or a task to provision and configure the Private Service Connect endpoint and its service attachment as part of this Epic, ensuring it's ready before deployment\\.",
      "blast_radius": "BR-3",
      "evidence": "ingress is restricted to internal traffic through the existing psc\\-widget private\\-service\\-connect endpoint \\(service attachment provisioned in the shared VPC\\), which is the sole ingress path for all internal consumers",
      "reviewer_votes": [
        "slot\\-1:gemini\\-2\\.5\\-flash"
      ],
      "statement": "The Epic assumes the \\`psc\\-widget\\` Private Service Connect endpoint and its underlying service attachment in the shared VPC are already provisioned, correctly configured for the new service's ingress, and fully operational\\.",
      "type": "assumption"
    },
    {
      "agreement_count": 1,
      "alternative": "Set \\`min\\-instances\\` to 0 to minimize costs during idle periods, accepting the risk of cold\\-start latency which could affect the uptime metric for initial requests after a lull\\.",
      "blast_radius": "BR-2",
      "evidence": "min\\-instances is set to 1 to remove cold\\-start gaps",
      "reviewer_votes": [
        "slot\\-4:gemini\\-2\\.5\\-pro"
      ],
      "statement": "The Epic specifies setting \\`min\\-instances\\` to 1 to meet the uptime SLO by avoiding cold starts, which assumes the continuous cost of an idle instance is an acceptable trade\\-off against potential latency or availability dips during traffic scale\\-up from zero\\.",
      "type": "assumption"
    },
    {
      "agreement_count": 1,
      "alternative": "The deployment process could be enhanced to verify the existence of these principals, or even create/manage them, to make the service's deployment more self\\-contained and less prone to external dependency failures\\.",
      "blast_radius": "BR-3",
      "evidence": "Both principals already exist in the widget\\-prod IAM inventory\\.",
      "reviewer_votes": [
        "slot\\-4:gemini\\-2\\.5\\-pro"
      ],
      "statement": "The access control configuration relies on the pre\\-existence and correct lifecycle management of the \\`widget\\-caller\\` service account and the \\`widget\\-oncall\\` group outside of this deployment's scope\\.",
      "type": "assumption"
    },
    {
      "agreement_count": 1,
      "alternative": "Provide a break\\-glass mechanism for the on\\-call group to gain temporary, audited write access to the service for emergencies where the standard deployment pipeline is too slow or is part of the failure\\.",
      "blast_radius": "BR-3",
      "evidence": "read\\-only access covers the on\\-call runbook, which escalates writes to the deploy pipeline",
      "reviewer_votes": [
        "slot\\-3:gemini\\-2\\.5\\-pro"
      ],
      "statement": "The grant of read\\-only access to the on\\-call group assumes that the documented escalation path via the deployment pipeline is sufficient for all operational incidents, and that direct write access is never required for emergency remediation\\.",
      "type": "assumption"
    },
    {
      "agreement_count": 1,
      "alternative": "The deployment process could include a step to verify the existence and correct configuration of the specified PSC endpoint to prevent deployment failures or traffic black\\-holing due to a misconfigured or missing dependency\\.",
      "blast_radius": "BR-3",
      "evidence": "ingress is restricted to internal traffic through the existing psc\\-widget private\\-service\\-connect endpoint \\(service attachment provisioned in the shared VPC\\)",
      "reviewer_votes": [
        "slot\\-4:gemini\\-2\\.5\\-pro"
      ],
      "statement": "The service's networking and security posture are dependent on an existing Private Service Connect endpoint in a shared VPC, which is managed outside the scope of this service's deployment\\.",
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
