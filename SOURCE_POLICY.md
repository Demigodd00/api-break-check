# Source Policy

## Authoritative source collection

The authoritative material is the stored old/new endpoint text, migration policy, and consumer usage. No live documentation site is fetched, so a reviewer can replay the exact packet that validators saw.

Concretely, the validator evidence consists of: api name, migration policy, old and proposed endpoint contracts, and registered consumer usage profiles stored by the contract.

## No autonomous retrieval

This contract performs no HTTP request, web search, URL rendering, oracle lookup, or hidden enrichment. A URL or source label inside user text remains untrusted text; validators are not asked to open it. This prevents mutable pages, blocked domains, and different search results from changing consensus.

## Collection responsibility

The deployer and participants must provide complete, lawfully usable, non-secret material. On-chain storage proves which bytes were considered after normalization; it does not prove authorship, completeness, ownership, or real-world truth.

## Normalization and limits

Text inputs normalize CRLF/CR to LF, trim surrounding whitespace, and enforce field-specific minimum and maximum lengths. Collection sizes are capped. Structured model output uses closed categories or fixed-order binary masks and fails closed on extra, missing, malformed, or out-of-range values.

## Prompt-injection boundary

Every evidence packet is serialized as sorted JSON and surrounded by named START/END delimiters. The prompt states that the packet is data, never instructions. A validator independently replays the assessment before any result is stored.

## Interpretation boundary

It does not execute a migration or prove runtime compatibility. Consumer profiles are self-declared and may be incomplete. Applications must show these limits next to results and use a fresh deployment when the underlying source set or policy changes.
