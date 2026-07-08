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

### 1. The epic assumes the "existing psc\-widget private\-service\-connect endpoint" and "shared VPC connector with no public internet route" are fully configured, audited, and compliant with all network security policies, including ingress source restrictions and egress blocking\.

- **Blast radius:** BR-3
- **Agreement:** 1
- **Evidence:** Ingress is restricted to internal traffic through the existing psc\-widget private\-service\-connect endpoint \(service attachment provisioned in the shared VPC\), which is the sole ingress path for all internal consumers; egress is routed through the shared VPC connector with no public internet route
- **Alternative:** Reference specific network policies, firewall rules, or audit reports that confirm the correct and secure configuration of the PSC endpoint \(e\.g\., explicitly whitelist source VPCs/subnets\) and the enforcement of no public internet egress \(e\.g\., via NAT or firewall rules\)\.

### 2. A single minimum instance \(\`min\-instances: 1\`\) is assumed to be sufficient to meet the 99\.9% uptime SLO, which may not hold true during single\-instance failures or underlying infrastructure events within the region\.

- **Blast radius:** BR-2
- **Agreement:** 1
- **Evidence:** The epic specifies a \`99\.9% uptime\` requirement but configures \`min\-instances is set to 1\` to address cold starts, not for high availability\.
- **Alternative:** Consider setting \`min\-instances\` to 2 or more to provide resilience against single\-instance failure and improve the likelihood of meeting the uptime SLO\.

### 3. The acceptance criteria assume that the \`widget\-prod Cloud Monitoring workspace\` and its synthetic probes are fully adequate for measuring 99\.9% uptime, and that setting \`min\-instances = 1\` completely resolves cold\-start gaps under all traffic conditions\.

- **Blast radius:** BR-2
- **Agreement:** 1
- **Evidence:** 99\.9% uptime over 30 days, measured as the fraction of successful synthetic probes \(HTTP 200 on /healthz at 60\-second intervals\) in the existing widget\-prod Cloud Monitoring workspace; min\-instances is set to 1 to remove cold\-start gaps
- **Alternative:** Specify the configuration details of the synthetic probes \(e\.g\., source regions, probe frequency, expected response times\) to ensure they accurately reflect user experience\. Clarify the definition of "cold\-start gaps" and provide a strategy for ensuring \`min\-instances = 1\` is effective under various load profiles, or specify a non\-zero acceptable latency for "warm\-up" if not completely eliminated\.

### 4. The epic assumes that Cloud Run's service\-level access control granularity is sufficient for all current and future access requirements, and that the on\-call runbook's escalation process for writes through the deploy pipeline is robust and timely enough for all operational needs\.

- **Blast radius:** BR-2
- **Agreement:** 1
- **Evidence:** service\-level bindings are the finest granularity Cloud Run offers, and read\-only access covers the on\-call runbook, which escalates writes to the deploy pipeline\.
- **Alternative:** Explicitly acknowledge the limitations of service\-level granularity and document any future requirements that might necessitate finer\-grained control \(e\.g\., specific API paths or data operations\)\. Document the expected response time and process for on\-call escalation to the deploy pipeline for write operations, ensuring it meets business and operational recovery objectives\.

### 5. The epic assumes that the business risk associated with a single\-region deployment \(due to the "single\-region by policy, with no multi\-region failover in scope"\) is fully understood, accepted, and documented by relevant stakeholders\.

- **Blast radius:** BR-2
- **Agreement:** 1
- **Evidence:** us\-central1 is pinned by the widget data\-residency requirement; this service tier is single\-region by policy, with no multi\-region failover in scope\.
- **Alternative:** Explicitly state the maximum acceptable downtime and data loss \(RTO/RPO\) for the widget service in the event of a regional outage\. Reference the official business continuity or disaster recovery documentation where this single\-region strategy and its associated risks have been formally approved\.

### 6. The epic assumes the 2026\-Q2 load test accurately predicts future peak loads, that 20% headroom is sufficient, and that a "hard limit with alerting at 80%" provides adequate time for intervention without affecting service availability\.

- **Blast radius:** BR-2
- **Agreement:** 1
- **Evidence:** quota\_budget: 5000\_vcpu\_hours, was sized from the 2026\-Q2 load test \(peak 5\.8 vCPU sustained\) plus 20% headroom, and is enforced as a hard limit with alerting at 80% in the widget\-prod quota dashboard\.
- **Alternative:** Detail the scope and methodology of the 2026\-Q2 load test and justify the 20% headroom based on anticipated growth or spike patterns\. Specify the operational runbook or automated response for 80% quota alerts, including escalation paths and acceptable timeframes for resolution, and explicitly state the business impact if the hard limit is reached\.


## Corpus in Force

The authoritative corpus for this review consists of: `README\.md`.

<details>
<summary>Sanitized ledger JSON (machine-readable)</summary>

```json
{
  "findings": [
    {
      "agreement_count": 1,
      "alternative": "Consider setting \\`min\\-instances\\` to 2 or more to provide resilience against single\\-instance failure and improve the likelihood of meeting the uptime SLO\\.",
      "blast_radius": "BR-2",
      "evidence": "The epic specifies a \\`99\\.9% uptime\\` requirement but configures \\`min\\-instances is set to 1\\` to address cold starts, not for high availability\\.",
      "reviewer_votes": [
        "slot\\-3:gemini\\-2\\.5\\-pro"
      ],
      "statement": "A single minimum instance \\(\\`min\\-instances: 1\\`\\) is assumed to be sufficient to meet the 99\\.9% uptime SLO, which may not hold true during single\\-instance failures or underlying infrastructure events within the region\\.",
      "type": "assumption"
    },
    {
      "agreement_count": 1,
      "alternative": "Specify the configuration details of the synthetic probes \\(e\\.g\\., source regions, probe frequency, expected response times\\) to ensure they accurately reflect user experience\\. Clarify the definition of \"cold\\-start gaps\" and provide a strategy for ensuring \\`min\\-instances = 1\\` is effective under various load profiles, or specify a non\\-zero acceptable latency for \"warm\\-up\" if not completely eliminated\\.",
      "blast_radius": "BR-2",
      "evidence": "99\\.9% uptime over 30 days, measured as the fraction of successful synthetic probes \\(HTTP 200 on /healthz at 60\\-second intervals\\) in the existing widget\\-prod Cloud Monitoring workspace; min\\-instances is set to 1 to remove cold\\-start gaps",
      "reviewer_votes": [
        "slot\\-1:gemini\\-2\\.5\\-flash"
      ],
      "statement": "The acceptance criteria assume that the \\`widget\\-prod Cloud Monitoring workspace\\` and its synthetic probes are fully adequate for measuring 99\\.9% uptime, and that setting \\`min\\-instances = 1\\` completely resolves cold\\-start gaps under all traffic conditions\\.",
      "type": "assumption"
    },
    {
      "agreement_count": 1,
      "alternative": "Explicitly acknowledge the limitations of service\\-level granularity and document any future requirements that might necessitate finer\\-grained control \\(e\\.g\\., specific API paths or data operations\\)\\. Document the expected response time and process for on\\-call escalation to the deploy pipeline for write operations, ensuring it meets business and operational recovery objectives\\.",
      "blast_radius": "BR-2",
      "evidence": "service\\-level bindings are the finest granularity Cloud Run offers, and read\\-only access covers the on\\-call runbook, which escalates writes to the deploy pipeline\\.",
      "reviewer_votes": [
        "slot\\-1:gemini\\-2\\.5\\-flash"
      ],
      "statement": "The epic assumes that Cloud Run's service\\-level access control granularity is sufficient for all current and future access requirements, and that the on\\-call runbook's escalation process for writes through the deploy pipeline is robust and timely enough for all operational needs\\.",
      "type": "assumption"
    },
    {
      "agreement_count": 1,
      "alternative": "Explicitly state the maximum acceptable downtime and data loss \\(RTO/RPO\\) for the widget service in the event of a regional outage\\. Reference the official business continuity or disaster recovery documentation where this single\\-region strategy and its associated risks have been formally approved\\.",
      "blast_radius": "BR-2",
      "evidence": "us\\-central1 is pinned by the widget data\\-residency requirement; this service tier is single\\-region by policy, with no multi\\-region failover in scope\\.",
      "reviewer_votes": [
        "slot\\-1:gemini\\-2\\.5\\-flash"
      ],
      "statement": "The epic assumes that the business risk associated with a single\\-region deployment \\(due to the \"single\\-region by policy, with no multi\\-region failover in scope\"\\) is fully understood, accepted, and documented by relevant stakeholders\\.",
      "type": "assumption"
    },
    {
      "agreement_count": 1,
      "alternative": "Reference specific network policies, firewall rules, or audit reports that confirm the correct and secure configuration of the PSC endpoint \\(e\\.g\\., explicitly whitelist source VPCs/subnets\\) and the enforcement of no public internet egress \\(e\\.g\\., via NAT or firewall rules\\)\\.",
      "blast_radius": "BR-3",
      "evidence": "Ingress is restricted to internal traffic through the existing psc\\-widget private\\-service\\-connect endpoint \\(service attachment provisioned in the shared VPC\\), which is the sole ingress path for all internal consumers; egress is routed through the shared VPC connector with no public internet route",
      "reviewer_votes": [
        "slot\\-1:gemini\\-2\\.5\\-flash"
      ],
      "statement": "The epic assumes the \"existing psc\\-widget private\\-service\\-connect endpoint\" and \"shared VPC connector with no public internet route\" are fully configured, audited, and compliant with all network security policies, including ingress source restrictions and egress blocking\\.",
      "type": "assumption"
    },
    {
      "agreement_count": 1,
      "alternative": "Detail the scope and methodology of the 2026\\-Q2 load test and justify the 20% headroom based on anticipated growth or spike patterns\\. Specify the operational runbook or automated response for 80% quota alerts, including escalation paths and acceptable timeframes for resolution, and explicitly state the business impact if the hard limit is reached\\.",
      "blast_radius": "BR-2",
      "evidence": "quota\\_budget: 5000\\_vcpu\\_hours, was sized from the 2026\\-Q2 load test \\(peak 5\\.8 vCPU sustained\\) plus 20% headroom, and is enforced as a hard limit with alerting at 80% in the widget\\-prod quota dashboard\\.",
      "reviewer_votes": [
        "slot\\-1:gemini\\-2\\.5\\-flash"
      ],
      "statement": "The epic assumes the 2026\\-Q2 load test accurately predicts future peak loads, that 20% headroom is sufficient, and that a \"hard limit with alerting at 80%\" provides adequate time for intervention without affecting service availability\\.",
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
