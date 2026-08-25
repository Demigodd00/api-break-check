# API Break Check

Reviews each proposed API endpoint change against frozen interface text and the actual usage profiles registered by its consumers.

## Why it is an Intelligent Contract

Classify an endpoint as COMPATIBLE, ADAPTATION, or BREAKING and produce a bounded migration note. Validators must independently agree on the category; wording is advisory. GenLayer's validator consensus turns that semantic judgment into shared contract state. Enrollment, authorization, the one-revision limit, acknowledgement counting, and completion are ordinary deterministic state transitions.

## Reusable deployment model

Deploy once per API migration campaign. A deployment can hold up to twelve endpoints and ten consumers; deploy the same source again for another API or release.

One completed deployment is an auditable record and is not reset or silently repurposed. Reuse means deploying the same reviewed source with new constructor data.

## Roles and workflow

The deployer owns the endpoint map; consumer addresses register their own usage and later acknowledge every assessed endpoint.

State path: `DESIGNING → ENROLLING → REVIEWING → ACKNOWLEDGING → COMPLETE`

## Evidence boundary

API name, migration policy, old and proposed endpoint contracts, and registered consumer usage profiles stored by the contract.

The authoritative material is the stored old/new endpoint text, migration policy, and consumer usage. No live documentation site is fetched, so a reviewer can replay the exact packet that validators saw.

## Core invariants

- Endpoint definitions cannot change after consumer enrollment begins.
- Only a non-compatible assessed endpoint can use its single revision.
- Completion requires every consumer to acknowledge every final endpoint assessment.

## Public interface

Write methods: `acknowledge_endpoint, add_endpoint, assess_endpoint, finalize_migration_map, open_acknowledgements, open_consumer_registry, register_consumer, revise_proposed_contract, start_endpoint_reviews`

View methods: `get_endpoint, get_policy, get_state`

`get_policy` exposes the machine-readable operating boundary and confirms that this contract never custodies funds.

## Verification

Pinned GenVM runner: `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`

```powershell
python -m pip install -r requirements.txt
genvm-lint check contracts/api_break_check.py
genvm-lint typecheck contracts/api_break_check.py
pytest tests/direct -q
python tests/run_glsim.py --port 4000 --validators 5 --no-browser
gltest tests/integration/test_glsim_consensus.py --network localnet -q
```

The StudioNet smoke test is opt-in and requires three disposable owner-specific test accounts. It reads state using `LATEST_FINAL` and asserts successful finalized execution.

## Final StudioNet proof

- Contract: https://explorer-studio.genlayer.com/address/0xC63a7A9f731354ad8bD8f8b8873E429037eeFbF5
- Studio import: https://studio.genlayer.com/?import-contract=0xC63a7A9f731354ad8bD8f8b8873E429037eeFbF5
- Deployment transaction: https://explorer-studio.genlayer.com/tx/0xbfe37b81ad64a1cce6ff09c99d6d2f1acf70873253edd973ea63ba8622248f35
- Intelligent transaction: https://explorer-studio.genlayer.com/tx/0x61f51a1b4dd49695faa1968c49f8f040e71c07deb5dff933414427f8e8a46ff6
- Observed final-state sample: `"COMPATIBLE"`
- Audited source SHA-256: `bd0342080186e6ca272d35f57d1d14b6cd2e720dd05d96bcf3d579acba5e0f72`

## Limitations

- It does not execute a migration or prove runtime compatibility.
- Consumer profiles are self-declared and may be incomplete.
- An unresponsive registered consumer can prevent finalization; applications should enroll only active participants.

## Repository map

- `contracts/api_break_check.py` — Intelligent Contract source
- `tests/direct` — fast leader/validator and lifecycle tests
- `tests/integration/test_glsim_consensus.py` — five-validator simulator flow
- `tests/integration/test_studionet_smoke.py` — live opt-in proof
- `deployments/studionet.json` — source-bound public deployment evidence
- `ARCHITECTURE.md`, `SOURCE_POLICY.md`, `SECURITY.md`, `AUDIT.md` — review material

License: MIT.
