# EquiPath Protocol - API Reference

This document provides the technical API reference for the EquiPath core protocol. It is intended for developers who wish to integrate privacy-preserving knowledge verification into their applications using the EquiPath smart contracts and TypeScript SDK.

This reference covers the low-level smart contract interface and the higher-level SDK functions. For a conceptual overview, please see the `architecture-overview.md`.

---

## 1. Core Concepts

Before using the API, it's important to understand these fundamental concepts:

-   **`contributionHash` (bytes32):** A cryptographic hash representing the knowledge contribution. It acts as a unique, privacy-preserving identifier without revealing the content itself.
-   **`culturalContext` (bytes32):** A hash or identifier representing the cultural context of the knowledge. This allows for categorization and respect for specific traditions without exposing sensitive details on-chain.
-   **`zk-SNARK Proof`:** A zero-knowledge proof generated off-chain that proves a contributor possesses the original knowledge corresponding to the `contributionHash` without revealing the knowledge. This is the core of the privacy mechanism.

---

## 2. Smart Contract API (`EquiPathVerifier.sol`)

This is the primary on-chain component of the EquiPath protocol. All interactions ultimately call functions on this contract.

**Address:** `[Deployed Contract Address]` (To be filled upon deployment)

### Functions

#### `verifyContribution()`

Verifies a knowledge contribution by validating a zk-SNARK proof on-chain. This is the primary function for registering a new, verified contribution.

