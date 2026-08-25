# Architecture

## Deployment boundary

Deploy once per API migration campaign. A deployment can hold up to twelve endpoints and ten consumers; deploy the same source again for another API or release.

The constructor establishes the deployment's subject and policy. Later calls add only the bounded records allowed by the state machine; a completed instance cannot be reopened.

## Participants

The deployer owns the endpoint map; consumer addresses register their own usage and later acknowledge every assessed endpoint.

Addresses are normalized before authorization comparisons. Role checks and phase gates execute before any semantic assessment.

## State machine

`DESIGNING → ENROLLING → REVIEWING → ACKNOWLEDGING → COMPLETE`

The phase value is the primary lifecycle lock. Every write either advances that path, performs a documented single-use loop, or fails with an `[EXPECTED]` user error.

## Evidence assembly

API name, migration policy, old and proposed endpoint contracts, and registered consumer usage profiles stored by the contract.

Before consensus, the contract normalizes bounded text, reads all required storage, constructs a sorted JSON packet, and places it between explicit data delimiters. The nested nondeterministic callbacks use captured plain values and do not read contract storage.

## Consensus boundary

Classify an endpoint as COMPATIBLE, ADAPTATION, or BREAKING and produce a bounded migration note. Validators must independently agree on the category; wording is advisory.

The leader callback validates JSON shape, field types, closed categories, masks, and length bounds. A validator reruns the same semantic operation and rejects disagreement. Where an explanatory label can vary harmlessly, consensus binds the stable decision field while still checking that the leader's advisory text is well formed.

## Deterministic boundary

Enrollment, authorization, the one-revision limit, acknowledgement counting, and completion are ordinary deterministic state transitions.

Important invariants:

- Endpoint definitions cannot change after consumer enrollment begins.
- Only a non-compatible assessed endpoint can use its single revision.
- Completion requires every consumer to acknowledge every final endpoint assessment.

No method sends value, pays rewards, escrows assets, deletes external data, or calls another contract.

## Failure model

- Invalid caller input or lifecycle use raises `[EXPECTED]` and leaves state unchanged.
- Malformed or out-of-policy model output raises `[LLM_ERROR]` and leaves the record assessable.
- Validator disagreement cannot commit an assessment.
- StudioNet proof reads explicitly target `LATEST_FINAL`, avoiding stale pre-final state.
