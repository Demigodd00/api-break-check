# Structured Judgment Update Audit

Audit date: 2026-08-31

Audited source: `contracts/api_break_check.py`

Source SHA-256: `2c67ede5e97ae06b99b9d91d49a96df592c2155fd7633fb65df34accef9eceab`

## Outcome

The category-only judgment identified in the prior review has been removed. Validators bind one 0/1/2 impact code per ordered consumer plus a four-bit protocol-change mask. The contract stores both intermediate structures and derives COMPATIBLE, ADAPTATION, or BREAKING deterministically before the revision and acknowledgement stages.

The current source passed local and GitHub verification. It is not ready to submit with the previous StudioNet links: that deployment is bound to the superseded source and must be replaced by a deployment of the current hash.

## Verification matrix

| Check | Result |
| --- | --- |
| Concrete GenVM runner pin | Pass |
| `genvm-lint check` | Pass |
| `genvm-lint typecheck` | Pass in GitHub CI |
| Hardened direct tests | Pass — 3 tests |
| Independent validator replay over intermediate results | Pass |
| Five-validator GLSim integration | Pass |
| Deterministic final-outcome derivation | Pass |
| Structured intermediate result stored on-chain | Pass |
| Meaningful reusable lifecycle after judgment | Pass |
| Current-source StudioNet deployment and intelligent write | Pending redeployment |
| Previous deployment | Superseded; do not submit as current proof |
| Fund custody and cross-contract calls | None |

## Rejection issue addressed

The model no longer returns a final category for one equality check. Consensus binds independently replayed intermediate findings, the contract derives the final outcome by explicit rules, and that outcome controls later contract-specific state transitions.

## Required before submission

1. Deploy the current `contracts/api_break_check.py` source.
2. Execute and finalize a representative intelligent write.
3. Record the new contract address, transaction hashes, observed intermediate fields, and source hash.
4. Replace the pending fields in `SUBMISSION.md`, `README.md`, and `deployments/studionet.json`.

Legacy deployment address: `0xC63a7A9f731354ad8bD8f8b8873E429037eeFbF5`.
