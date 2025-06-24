pragma circom 2.0.0;

include "circomlib/circuits/poseidon.circom";
include "circomlib/circuits/comparators.circom";

// Working circuit for ESP demonstration
template KnowledgeVerification() {
    // Public inputs
    signal input expectedHash;
    signal input culturalContext;
    
    // Private inputs  
    signal private input knowledgeContent;
    signal private input contributorSecret;
    
    // Output
    signal output verified;
    
    // Hash the private inputs
    component hasher = Poseidon(2);
    hasher.inputs[0] <== knowledgeContent;
    hasher.inputs[1] <== contributorSecret;
    
    // Check if hash matches expected
    component equalCheck = IsEqual();
    equalCheck.in[0] <== hasher.out;
    equalCheck.in[1] <== expectedHash;
    
    // Output verification result
    verified <== equalCheck.out;
    
    // Constraint: must verify
    verified === 1;
}

component main = KnowledgeVerification();
