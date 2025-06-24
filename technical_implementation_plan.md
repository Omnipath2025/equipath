# EquiPath Technical Implementation Plan

## Overview

This document details the implementation of EquiPath's **open-source components** funded by the Ethereum Foundation Small Grant. These components provide public infrastructure for privacy-preserving knowledge verification.

## Architecture Separation

### ✅ Open Source (This Repository)
Components funded by the grant and released under MIT License:

1. **zk-SNARK Circuits** (Circom)
   - Contribution verification circuits
   - Attribute proof circuits
   - Eligibility verification circuits

2. **Smart Contracts** (Solidity)
   - Proof verification contracts
   - Basic registry contracts
   - Standard interfaces

3. **Client Library** (TypeScript)
   - Proof generation SDK
   - Basic integration tools
   - Documentation and examples

### ❌ Not Included (Proprietary)
Components NOT funded by grant and NOT in this repository:

- OmniPath integration orchestration
- AI-driven compensation algorithms
- Justice-equity calculation engines
- Enterprise compliance features
- Cross-path workflow automation

## Technical Implementation

### 1. zk-SNARK Circuit Design

```javascript
// circuits/contribution_verifier.circom
pragma circom 2.0.0;

template ContributionVerifier() {
    // Public inputs
    signal input contribution_hash;
    signal input attribute_commitment;
    
    // Private inputs
    signal private input knowledge_content;
    signal private input contributor_secret;
    signal private input attributes[10];
    
    // Verification logic
    component hasher = Poseidon(2);
    hasher.inputs[0] <== knowledge_content;
    hasher.inputs[1] <== contributor_secret;
    
    // Constrain hash matches
    contribution_hash === hasher.out;
    
    // Verify attributes without revealing
    component attr_verifier = AttributeVerifier();
    attr_verifier.attributes <== attributes;
    attr_verifier.commitment <== attribute_commitment;
}

component main = ContributionVerifier();
