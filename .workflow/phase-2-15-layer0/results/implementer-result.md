# Implementer Result — phase-2-15-layer0

## Summary

Implemented Layer 0 full parser per FR-3/FR-4: optional FR-3 field extraction, placeholder and domain validation against `regions.json`, and non-blocking assumption seed generation for Layer 1.

## Files Changed

| File | Change |
|------|--------|
| `crossfire_forge/regions.json` | Domain lists for `regions`, `security_posture`, and `quota_budget_patterns` (regex) |
| `crossfire_forge/layer0.py` | `parse_layer0(epic_text) -> Layer0Result` with optional parsed fields and `seeds` list |
| `tests/test_layer0.py` | Fixture-driven tests for `epic_441.md`, `epic_placeholder.md`, and `epic_complete.md` |

## Behavior

- **FR-3 fields:** `region`, `security_posture`, `quota_budget`, `acceptance_criteria` — all optional.
- **Zero-field epic (`epic_441.md`):** No Layer 0 block detected → empty seeds, all parsed fields `None`.
- **Placeholder epic (`epic_placeholder.md`):** One seed per bad field (`{field} has placeholder value`).
- **Complete epic (`epic_complete.md`):** Valid fields parsed (`us-central1` in regions list); no seeds.
- **Partial block:** When any FR-3 field is present, missing siblings emit `{field} unspecified` seeds.
- **Domain invalid:** Values outside `regions.json` lists/patterns emit `{field} has invalid value` seeds.
- **Placeholder detection:** `TODO`, `TBD`, `___`, `placeholder`, `<TBD>`, empty/whitespace, and related patterns.
- **Non-blocking:** `parse_layer0` never raises; malformed input returns empty `Layer0Result`. No model calls.

## Deviations

None — plan executed as specified.

## Verification

```text
pytest tests/test_layer0.py -v
============================= 14 passed in 0.05s ==============================
```
