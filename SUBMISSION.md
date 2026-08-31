Contribution Date: 08/31/2026

Title: API Break Check

Submission status:
HOLD — current-source StudioNet redeployment required before submission.

Notes / Description:
Built a reusable multi-consumer API migration ledger. Validator consensus binds per-consumer impact codes and a protocol-change mask; the contract derives the final compatibility category, permits one bounded revision, and requires every registered consumer to acknowledge the final assessments.

Structured contract behavior:
Validators bind one 0/1/2 impact code per ordered consumer plus a four-bit protocol-change mask. The contract stores both intermediate structures and derives COMPATIBLE, ADAPTATION, or BREAKING deterministically before the revision and acknowledgement stages.

Evidence & Supporting:

GitHub Repository:
https://github.com/Demigodd00/api-break-check

GitHub File:
https://github.com/Demigodd00/api-break-check/blob/main/contracts/api_break_check.py

Current source SHA-256:
2c67ede5e97ae06b99b9d91d49a96df592c2155fd7633fb65df34accef9eceab

GenLayer Studio Contract:
PENDING — deploy the current main-branch source.

GenLayer Explorer Contract:
PENDING — do not reuse the superseded deployment.

Deployment transaction:
PENDING

Successful intelligent transaction:
PENDING

Legacy evidence notice:
The previous deployment at 0xC63a7A9f731354ad8bD8f8b8873E429037eeFbF5 is bound to an older category-only source and is retained only as historical evidence. It must not be submitted as proof of the current implementation.
