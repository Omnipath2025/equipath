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

function verifyContribution(
bytes32 contributionHash,
bytes32 culturalContext,
uint256 memory a,
uint256 memory b,
uint256 memory c,
uint256 memory input
) public returns (bool)


-   **@param `contributionHash` (bytes32):** The public hash of the contribution.
-   **@param `culturalContext` (bytes32):** The public identifier for the cultural context.
-   **@param `a`, `b`, `c` (uint256 arrays):** The core components of the Groth16 zk-SNARK proof.
-   **@param `input` (uint256 array):** The public inputs used for proof verification (must match the `contributionHash` and `culturalContext`).
-   **@returns (bool):** Returns `true` if the verification is successful.
-   **Emits:** `ContributionVerified` event upon successful verification.

**Ethers.js Example:**
const { ethers } = require("hardhat");
const verifierContract = await ethers.getContractAt("EquiPathVerifier", contractAddress);

// Assume proof and publicSignals are generated off-chain
const tx = await verifierContract.verifyContribution(
publicSignals, // contributionHash
publicSignals, // culturalContext
proof.pi_a,
proof.pi_b,
proof.pi_c,
publicSignals
);
await tx.wait();

#### `isVerified()`

A public view function to check if a contribution has already been successfully verified.

function isVerified(bytes32 contributionHash) public view returns (bool)


-   **@param `contributionHash` (bytes32):** The hash of the contribution to check.
-   **@returns (bool):** Returns `true` if the contribution exists and is marked as verified.

**Ethers.js Example:**
const isContributionVerified = await verifierContract.isVerified(contributionHash);
console.log('Is verified:', isContributionVerified);

#### `getContribution()`

A public view function to retrieve the details of a stored contribution.

function getContribution(bytes32 contributionHash) public view returns (KnowledgeContribution memory)

-   **@param `contributionHash` (bytes32):** The hash of the contribution to retrieve.
-   **@returns (KnowledgeContribution):** A struct containing the contribution's details (`contributionHash`, `culturalContext`, `verified`, `timestamp`, `contributor` address).

**Ethers.js Example:**
const contributionDetails = await verifierContract.getContribution(contributionHash);
console.log('Contributor:', contributionDetails.contributor);
console.log('Timestamp:', new Date(contributionDetails.timestamp * 1000));


### Events

#### `ContributionVerified`

Emitted when a contribution is successfully verified via the `verifyContribution` function.

event ContributionVerified(
bytes32 indexed contributionHash,
address indexed contributor,
uint256 timestamp
);

-   **@param `contributionHash` (bytes32):** The hash of the verified contribution.
-   **@param `contributor` (address):** The address of the account that submitted the verification proof.
-   **@param `timestamp` (uint256):** The block timestamp of the verification.

---

## 3. TypeScript SDK

The EquiPath SDK provides a high-level, developer-friendly interface for interacting with the protocol, abstracting away the complexities of direct smart contract calls.

### Setup
import { EquiPathSDK } from 'equipath-sdk';
import { ethers } from 'ethers';

// Connect to a provider (e.g., MetaMask, Infura, Alchemy)
const provider = new ethers.providers.Web3Provider(window.ethereum);
const signer = provider.getSigner();

const sdk = new EquiPathSDK(signer, {
verifierContractAddress: '0x...'
});

### SDK Methods

#### `sdk.verify()`

A wrapper for the `verifyContribution` smart contract function. It takes the proof and public signals and handles the transaction submission.

async verify(proof: ZKProof, publicSignals: string[]): Promise<ethers.ContractTransaction>

-   **@param `proof` (ZKProof):** An object containing the `pi_a`, `pi_b`, and `pi_c` components of the proof.
-   **@param `publicSignals` (string[]):** An array of public signals, including the `contributionHash` and `culturalContext`.
-   **@returns (Promise<ethers.ContractTransaction>):** A promise that resolves to the transaction object.

**Example:**
// Assume myProof and myPublicSignals are generated
try {
const tx = await sdk.verify(myProof, myPublicSignals);
const receipt = await tx.wait();
console.log('Transaction successful:', receipt.transactionHash);
} catch (error) {
console.error('Verification failed:', error);
}

#### `sdk.isContributionVerified()`

A wrapper for the `isVerified` smart contract function.
async isContributionVerified(contributionHash: string): Promise<boolean>

-   **@param `contributionHash` (string):** The `bytes32` hash as a hex string.
-   **@returns (Promise<boolean>):** A promise that resolves to `true` or `false`.

**Example:**
const isVerified = await sdk.isContributionVerified('0x...');
console.log(isVerified); // true or false

---

## 4. Error Handling

When interacting with the smart contract, transactions may revert with specific error messages. Your application should handle these gracefully.

-   **`Invalid contribution hash`**: Thrown if `contributionHash` is zero.
-   **`Invalid proof input`**: Thrown if the proof data is malformed.
-   **Generic Reverts**: Standard transaction failures (e.g., `invalid proof`, `out of gas`) may also occur.


