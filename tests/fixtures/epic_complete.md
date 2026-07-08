# [EPIC] Complete regional widget deployment

## Objective

Deploy the widget service with full governance metadata and explicit access-control bindings.

## Target

`services/widget/`

region: us-central1
security_posture: private-service-connect
quota_budget: 5000_vcpu_hours
acceptance_criteria: |
  - 99.9% uptime over 30 days, measured as the fraction of successful synthetic probes (HTTP 200 on /healthz at 60-second intervals) in the existing widget-prod Cloud Monitoring workspace; min-instances is set to 1 to remove cold-start gaps
  - Access control documented and enforced: roles/run.invoker bound to serviceAccount:widget-caller@widget-prod.iam.gserviceaccount.com at the service level, and roles/run.viewer bound to group:widget-oncall@example.com at the service level (least privilege; no project-level grants; service-level bindings are the finest granularity Cloud Run offers, and read-only access covers the on-call runbook, which escalates writes to the deploy pipeline). Both principals already exist in the widget-prod IAM inventory.
  - No public access: neither allUsers nor allAuthenticatedUsers is bound to any role, and ingress is restricted to internal traffic through the existing psc-widget private-service-connect endpoint (service attachment provisioned in the shared VPC), which is the sole ingress path for all internal consumers; egress is routed through the shared VPC connector with no public internet route

## Deployment context

- us-central1 is pinned by the widget data-residency requirement; this service tier is single-region by policy, with no multi-region failover in scope.
- The quota budget applies per calendar month and covers service compute only; it was sized from the 2026-Q2 load test (peak 5.8 vCPU sustained) plus 20% headroom, and is enforced as a hard limit with alerting at 80% in the widget-prod quota dashboard.

status:ai-agent-active
