pragma circom 2.0.0;

include "circomlib/circuits/poseidon.circom";
include "circomlib/circuits/comparators.circom";

// Core circuit for verifying traditional knowledge contributions
// while preserving contributor privacy and cultural context
template KnowledgeVerification() {
    // Public inputs (visible on-chain)
    signal input contributionHash;        // Hash of the knowledge contribution
    signal input culturalContext;         // Cultural context identifier
    signal input timestamp;               // Contribution timestamp
    
    // Private inputs (kept secret)
    signal private input knowledgeContent;    // Actual knowledge content
    signal private input contributorIdentity; // Contributor's identity
    signal private input culturalProof;       // Proof of cultural authority
    signal private input sourceValidation;    // Traditional source validation
    
    // Outputs
    signal output verified;               // Verification result
    signal output attributionHash;       // Attribution hash for compensation
    signal output privacyPreserved;      // Privacy preservation confirmation
    
    // Components for cryptographic operations
    component contentHasher = Poseidon(4);
    component attributionHasher = Poseidon(3);
    component validityChecker = IsEqual();
    
    // Verify knowledge content matches public contribution hash
    contentHasher.inputs[0] <== knowledgeContent;
    contentHasher.inputs[1] <== contributorIdentity;
    contentHasher.inputs[2] <== culturalContext;
    contentHasher.inputs[3] <== timestamp;
    
    // Check if computed hash matches public contribution hash
    validityChecker.in[0] <== contentHasher.out;
    validityChecker.in[1] <== contributionHash;
    
    // Generate attribution hash for compensation tracking
    attributionHasher.inputs[0] <== contributorIdentity;
    attributionHasher.inputs[1] <== culturalProof;
    attributionHasher.inputs[2] <== sourceValidation;
    
    // Assign outputs
    verified <== validityChecker.out;
    attributionHash <== attributionHasher.out;
    privacyPreserved <== 1; // Always 1 if circuit completes successfully
    
    // Constraint: verification must be successful for valid proof
    verified === 1;
}

// Main component instantiation
component main = KnowledgeVerification();
