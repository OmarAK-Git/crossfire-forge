# [EPIC] Complete regional widget deployment

## Objective

Deploy the widget service with full governance metadata and explicit access-control bindings.

## Target

`services/widget/`

region: us-central1
security_posture: private-service-connect
quota_budget: 5000_vcpu_hours
acceptance_criteria: |
  - 99.9% uptime over 30 days
  - Access control documented and enforced: roles/run.invoker bound to serviceAccount:widget-caller@widget-prod.iam.gserviceaccount.com at the service level, and roles/run.viewer bound to group:widget-oncall@example.com at the service level (least privilege; no project-level grants)
  - No public access: neither allUsers nor allAuthenticatedUsers is bound to any role, and ingress is restricted to internal traffic through the private-service-connect endpoint

status:ai-agent-active
