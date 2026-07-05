# [EPIC] Complete regional widget deployment

## Objective

Deploy the widget service with full governance metadata so Layer 0 emits no assumption seeds.

## Target

`services/widget/`

region: us-central1
security_posture: private-service-connect
quota_budget: 5000_vcpu_hours
acceptance_criteria: |
  - 99.9% uptime over 30 days
  - All RBAC scopes documented and enforced at project and service level
  - No open BR-3 assumptions in the final ledger

status:ai-agent-active
