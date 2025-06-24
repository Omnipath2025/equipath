pragma circom 2.0.0;

include "circomlib/circuits/poseidon.circom";
include "circomlib/circuits/comparators.circom";

// Working circuit for traditional knowledge verification
// Proves knowledge of content without revealing it
template KnowledgeVerification() {
    // Private inputs (witness - kept secret)
    signal private input knowledgeContent;     // The actual knowledge (private)
    signal private input contributorSecret;    // Contributor's secret key (private)
    
    // Public inputs (visible on-chain)
    signal input expectedHash;                 // Expected hash of knowledge + secret
    signal input culturalContext;             // Cultural context identifier
    
    // Output
    signal output verified;                    // 1 if verification passes, 0 otherwise
    
    // Component for hashing
    component hasher = Poseidon(2);
    
    // Hash the private inputs
    hasher.inputs[0] <== knowledgeContent;
    hasher.inputs[1] <== contributorSecret;
    
    // Component to check if computed hash equals expected hash
    component equalCheck = IsEqual();
    equalCheck.in[0] <== hasher.out;
    equalCheck.in[1] <== expectedHash;
    
    // Output the verification result
    verified <== equalCheck.out;
    
    // Constraint: verification must pass (this enforces the proof)
    verified === 1;
}

// Main component - required for compilation
component main = KnowledgeVerification();
