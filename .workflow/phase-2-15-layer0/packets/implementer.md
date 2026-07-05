# Implementation Packet — phase-2-15-layer0

Implement layer0.py + regions.json per FR-3/FR-4:
- epic_441.md (zero fields) -> no Layer 0 block, empty seeds
- epic_placeholder.md -> assumption seeds for placeholder/invalid fields
- epic_complete.md -> validate FR-3 fields against domain lists in regions.json
- Layer 0 never blocks, never invokes model

Run pytest tests/test_layer0.py -v

Do NOT mark queue complete.
