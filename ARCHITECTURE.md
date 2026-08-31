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

For each endpoint, validators independently bind two structured results: one `0/1/2` impact code per ordered consumer and a four-bit protocol-change mask. The validator must reproduce both complete vectors; migration-note wording remains advisory.

The leader callback validates vector lengths, the closed code alphabet, the mask, and note bounds. A validator reruns the same semantic operation and rejects disagreement in any independently bound component. The contract—not the model—derives BREAKING when any consumer has code `2`, ADAPTATION when none has `2` but at least one has `1`, and COMPATIBLE otherwise.

## Deterministic boundary

Category derivation, enrollment, authorization, the one-revision loop, acknowledgement counting, and completion are ordinary deterministic state transitions.

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
