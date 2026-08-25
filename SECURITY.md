# Security

## Scope

This repository is a bounded Intelligent Contract, its direct and five-validator tests, and an opt-in StudioNet smoke test. It has no frontend, backend, database, token, payout, upgrade proxy, or privileged secret.

## Trust model

Untrusted API text is delimited as data, output categories are closed, and the consensus check ignores harmless differences in explanatory wording.

The deployer owns the endpoint map; consumer addresses register their own usage and later acknowledge every assessed endpoint.

## Implemented controls

- Concrete immutable GenVM runner hash; no floating `latest` dependency.
- Address normalization, explicit role separation, one-time actions, collection caps, and lifecycle locks.
- Bounded text and strict model-response schemas with `[EXPECTED]` versus `[LLM_ERROR]` failure classes.
- Sorted, delimited untrusted evidence packets and independent validator replay.
- All storage is read before entering nondeterministic callbacks; the final static audit found zero `self`/storage reads inside consensus callbacks.
- No cross-contract calls, fund custody, transfer, automatic purchase, deletion, or off-chain webhook.
- `.env`, caches, artifacts, wallet files, and local deployment material are ignored. Live wallets are encrypted and stored outside the workspace.

## Contract-specific safety properties

- Endpoint definitions cannot change after consumer enrollment begins.
- Only a non-compatible assessed endpoint can use its single revision.
- Completion requires every consumer to acknowledge every final endpoint assessment.

## Residual risks

- It does not execute a migration or prove runtime compatibility.
- Consumer profiles are self-declared and may be incomplete.
- An unresponsive registered consumer can prevent finalization; applications should enroll only active participants.

This contract should not be used to make legal, medical, financial, employment, admission, or physical-safety decisions unless its own policy explicitly supports that domain and an independent professional review is added. This version does not.

## Reporting

Report a vulnerability privately to the repository owner with the contract name, affected method, reproduction, expected invariant, and impact. Do not include private keys or personal data. The owner should reproduce it in a fresh disposable deployment before publishing details.
