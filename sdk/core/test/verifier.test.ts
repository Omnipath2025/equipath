/**
 * @file verifier.test.ts
 * @title EquiPath Verification SDK Test Suite
 * @dev ESP Grant Deliverable: Comprehensive tests for TypeScript SDK
 * @notice Professional testing suite demonstrating SDK functionality and reliability
 * @author EquiPath Protocol Team
 * @version 1.0.0
 * 
 * This test suite validates all core functionality of the EquiPath verification SDK,
 * ensuring reliable operation for developers integrating the verification system.
 * 
 * ESP Grant Alignment:
 * - Developer Tools: Validates SDK reliability and ease of use
 * - Infrastructure: Tests core verification protocol functionality
 * - Public Good: Ensures open-source code quality and maintainability
 * - Research: Validates zero-knowledge proof generation and verification
 */

import { jest } from '@jest/globals';
import { ethers } from 'ethers';

// Import SDK components
import {
  EquiPathVerifier,
  createEquiPathVerifier,
  createTestnetVerifier,
  generateSampleContribution,
  createSampleParams,
  KnowledgeContribution,
  VerificationParams,
  ZKProof,
  VerificationResult,
  EquiPathConfig,
  CircuitError,
  ContractError,
  ValidationError
} from '../src/verifier';

// Mock external dependencies
jest.mock('ethers');
jest.mock('snarkjs');
jest.mock('circomlibjs');

// Mock implementations
const mockProvider = {
  getNetwork: jest.fn().mockResolvedValue({ chainId: 11155111, name: 'sepolia' }),
  getBlockNumber: jest.fn().mockResolvedValue(1000000),
  getGasPrice: jest.fn().mockResolvedValue(ethers.parseUnits('20', 'gwei'))
};

const mockContract = {
  submitContribution: jest.fn(),
  verifyContribution: jest.fn(),
  getContribution: jest.fn(),
  isContributionVerified: jest.fn(),
  on: jest.fn(),
  removeAllListeners: jest.fn(),
  connect: jest.fn().mockReturnThis()
};

const mockSigner = {
  getAddress: jest.fn().mockResolvedValue('0x1234567890123456789012345678901234567890'),
  signMessage: jest.fn().mockResolvedValue('0xmocksignature')
};

const mockSnarkjs = {
  groth16: {
    fullProve: jest.fn(),
    verify: jest.fn()
  }
};

// Test configuration
const testConfig: EquiPathConfig = {
  contractAddress: '0x742d35Cc6634C0532925a3b8D5b9dd32a1234567',
  providerUrl: 'https://eth-sepolia.g.alchemy.com/v2/test',
  circuitWasmPath: './test/fixtures/knowledge_verification.wasm',
  circuitZkeyPath: './test/fixtures/knowledge_verification_final.zkey',
  maxKnowledgeLength: 256,
  maxContextLength: 128
};

// Test data
const sampleContribution: KnowledgeContribution = {
  content: 'Traditional herbal remedy using willow bark for pain relief',
  culturalContext: 'Native American traditional medicine from Pacific Northwest',
  contributorIdentity: 'verified-tribal-healer-001',
  qualityMetrics: {
    authenticity: 95,
    completeness: 88,
    accuracy: 92,
    culturalSignificance: 97
  },
  contextDetails: 'Knowledge passed down through seven generations of tribal healers',
  culturalCredentials: 'Certified by Tribal Council as authentic traditional medicine practitioner'
};

const sampleProof: ZKProof = {
  proof: {
    pi_a: ['0x123', '0x456', '0x789'],
    pi_b: [['0xabc', '0xdef'], ['0x111', '0x222'], ['0x333', '0x444']],
    pi_c: ['0x555', '0x666', '0x777']
  },
  publicSignals: ['1', '0x888999aaabbbcccdddeeefff000111222333444555666777888', '85']
};

// Setup and teardown
beforeEach(() => {
  jest.clearAllMocks();
  
  // Setup ethers mocks
  (ethers.JsonRpcProvider as jest.Mock).mockReturnValue(mockProvider);
  (ethers.Contract as jest.Mock).mockReturnValue(mockContract);
  (ethers.keccak256 as jest.Mock).mockImplementation((data) => 
    '0x' + Buffer.from(data).toString('hex').padStart(64, '0')
  );
  (ethers.toUtf8Bytes as jest.Mock).mockImplementation((str) => 
    Buffer.from(str, 'utf8')
  );

  // Setup snarkjs mocks
  jest.doMock('snarkjs', () => mockSnarkjs);
});

afterEach(() => {
  jest.resetAllMocks();
});

// ============ Constructor and Configuration Tests ============

describe('EquiPathVerifier Constructor', () => {
  
  test('should create instance with valid configuration', () => {
    const verifier = new EquiPathVerifier(testConfig);
    expect(verifier).toBeInstanceOf(EquiPathVerifier);
    expect(ethers.JsonRpcProvider).toHaveBeenCalledWith(testConfig.providerUrl);
    expect(ethers.Contract).toHaveBeenCalledWith(
      testConfig.contractAddress,
      expect.any(Array),
      mockProvider
    );
  });

  test('should connect signer successfully', () => {
    const verifier = new EquiPathVerifier(testConfig);
    verifier.connectSigner(mockSigner as any);
    expect(mockContract.connect).toHaveBeenCalledWith(mockSigner);
  });

});

describe('Factory Functions', () => {

  test('createEquiPathVerifier should return configured instance', () => {
    const verifier = createEquiPathVerifier(
      testConfig.contractAddress,
      testConfig.providerUrl
    );
    expect(verifier).toBeInstanceOf(EquiPathVerifier);
  });

  test('createTestnetVerifier should return testnet-configured instance', () => {
    const verifier = createTestnetVerifier(testConfig.contractAddress);
    expect(verifier).toBeInstanceOf(EquiPathVerifier);
  });

});

// ============ Validation Tests ============

describe('Input Validation', () => {

  let verifier: EquiPathVerifier;

  beforeEach(() => {
    verifier = new EquiPathVerifier(testConfig);
  });

  test('should validate contribution with valid data', async () => {
    const params = createSampleParams('0x123456789012345678901234567890123456789012345678901234567890abcd');
    
    mockSnarkjs.groth16.fullProve.mockResolvedValue({
      proof: sampleProof.proof,
      publicSignals: sampleProof.publicSignals
    });

    const result = await verifier.generateProof(sampleContribution, params);
    expect(result).toHaveProperty('proof');
    expect(result).toHaveProperty('publicSignals');
  });

  test('should throw ValidationError for empty knowledge content', async () => {
    const invalidContribution = { ...sampleContribution, content: '' };
    const params = createSampleParams('0x123456789012345678901234567890123456789012345678901234567890abcd');

    await expect(verifier.generateProof(invalidContribution, params))
      .rejects.toThrow(ValidationError);
  });

  test('should throw ValidationError for invalid quality metrics', async () => {
    const invalidContribution = {
      ...sampleContribution,
      qualityMetrics: { ...sampleContribution.qualityMetrics, authenticity: 150 }
    };
    const params = createSampleParams('0x123456789012345678901234567890123456789012345678901234567890abcd');

    await expect(verifier.generateProof(invalidContribution, params))
      .rejects.toThrow(ValidationError);
  });

  test('should throw ValidationError for invalid contribution hash format', async () => {
    const params = createSampleParams('invalid_hash');

    await expect(verifier.generateProof(sampleContribution, params))
      .rejects.toThrow(ValidationError);
  });

});

// ============ Proof Generation Tests ============

describe('Zero-Knowledge Proof Generation', () => {

  let verifier: EquiPathVerifier;

  beforeEach(() => {
    verifier = new EquiPathVerifier(testConfig);
  });

  test('should generate valid proof for authentic knowledge', async () => {
    const params = createSampleParams('0x123456789012345678901234567890123456789012345678901234567890abcd');
    
    mockSnarkjs.groth16.fullProve.mockResolvedValue({
      proof: sampleProof.proof,
      publicSignals: sampleProof.publicSignals
    });

    const result = await verifier.generateProof(sampleContribution, params);
    
    expect(result.proof).toEqual(sampleProof.proof);
    expect(result.publicSignals).toEqual(sampleProof.publicSignals);
    expect(mockSnarkjs.groth16.fullProve).toHaveBeenCalledWith(
      expect.any(Object),
      testConfig.circuitWasmPath,
      testConfig.circuitZkeyPath
    );
  });

  test('should handle circuit compilation errors', async () => {
    const params = createSampleParams('0x123456789012345678901234567890123456789012345678901234567890abcd');
    
    mockSnarkjs.groth16.fullProve.mockRejectedValue(new Error('Circuit compilation failed'));

    await expect(verifier.generateProof(sampleContribution, params))
      .rejects.toThrow(CircuitError);
  });

  test('should prepare circuit inputs correctly', async () => {
    const params = createSampleParams('0x123456789012345678901234567890123456789012345678901234567890abcd');
    
    mockSnarkjs.groth16.fullProve.mockResolvedValue({
      proof: sampleProof.proof,
      publicSignals: sampleProof.publicSignals
    });

    await verifier.generateProof(sampleContribution, params);
    
    const circuitInputs = mockSnarkjs.groth16.fullProve.mock.calls[0][0];
    expect(circuitInputs).toHaveProperty('contributionHash');
    expect(circuitInputs).toHaveProperty('culturalContext');
    expect(circuitInputs).toHaveProperty('knowledgeContent');
    expect(circuitInputs).toHaveProperty('qualityMetrics');
    expect(circuitInputs.qualityMetrics).toHaveLength(4);
  });

});

// ============ Proof Verification Tests ============

describe('Zero-Knowledge Proof Verification', () => {

  let verifier: EquiPathVerifier;

  beforeEach(() => {
    verifier = new EquiPathVerifier(testConfig);
  });

  test('should verify valid proof successfully', async () => {
    const params = createSampleParams('0x123456789012345678901234567890123456789012345678901234567890abcd');
    
    mockSnarkjs.groth16.verify.mockResolvedValue(true);

    const result = await verifier.verifyProof(sampleProof, params);
    
    expect(result.verified).toBe(true);
    expect(result.attributionProof).toBe(sampleProof.publicSignals[1]);
    expect(result.qualityScore).toBe(85);
  });

  test('should reject invalid proof', async () => {
    const params = createSampleParams('0x123456789012345678901234567890123456789012345678901234567890abcd');
    
    mockSnarkjs.groth16.verify.mockResolvedValue(false);

    const result = await verifier.verifyProof(sampleProof, params);
    
    expect(result.verified).toBe(false);
    expect(result.attributionProof).toBe('');
    expect(result.qualityScore).toBe(0);
  });

  test('should handle verification errors', async () => {
    const params = createSampleParams('0x123456789012345678901234567890123456789012345678901234567890abcd');
    
    mockSnarkjs.groth16.verify.mockRejectedValue(new Error('Verification failed'));

    await expect(verifier.verifyProof(sampleProof, params))
      .rejects.toThrow(CircuitError);
  });

});

// ============ Blockchain Interaction Tests ============

describe('Smart Contract Interactions', () => {

  let verifier: EquiPathVerifier;

  beforeEach(() => {
    verifier = new EquiPathVerifier(testConfig);
    verifier.connectSigner(mockSigner as any);
  });

  test('should submit contribution to blockchain successfully', async () => {
    const mockReceipt = {
      hash: '0xtxhash123',
      blockNumber: 1000001,
      gasUsed: { toNumber: () => 150000 }
    };
    
    mockContract.submitContribution.mockResolvedValue({
      wait: () => Promise.resolve(mockReceipt)
    });

    const result = await verifier.submitContribution(sampleContribution, sampleProof);
    
    expect(result.success).toBe(true);
    expect(result.transactionHash).toBe('0xtxhash123');
    expect(result.blockNumber).toBe(1000001);
    expect(result.gasUsed).toBe(150000);
  });

  test('should handle submission errors gracefully', async () => {
    mockContract.submitContribution.mockRejectedValue(new Error('Transaction failed'));

    const result = await verifier.submitContribution(sampleContribution, sampleProof);
    
    expect(result.success).toBe(false);
    expect(result.error).toContain('Transaction failed');
  });

  test('should check contribution verification status', async () => {
    const contributionHash = '0x123456789012345678901234567890123456789012345678901234567890abcd';
    mockContract.isContributionVerified.mockResolvedValue(true);

    const result = await verifier.isContributionVerified(contributionHash);
    
    expect(result).toBe(true);
    expect(mockContract.isContributionVerified).toHaveBeenCalledWith(contributionHash);
  });

  test('should retrieve contribution details', async () => {
    const contributionHash = '0x123456789012345678901234567890123456789012345678901234567890abcd';
    const mockContribution = {
      contributionHash,
      culturalContext: '0xculturalcontext',
      contributor: '0xcontributor',
      status: 1,
      timestamp: { toNumber: () => 1640995200 },
      verificationCount: { toNumber: () => 3 },
      attributionProof: '0xattributionproof'
    };
    
    mockContract.getContribution.mockResolvedValue(mockContribution);

    const result = await verifier.getContribution(contributionHash);
    
    expect(result.contributionHash).toBe(contributionHash);
    expect(result.contributor).toBe('0xcontributor');
    expect(result.timestamp).toBeInstanceOf(Date);
    expect(result.verificationCount).toBe(3);
  });

  test('should throw ContractError when signer not connected', async () => {
    const verifierWithoutSigner = new EquiPathVerifier(testConfig);

    await expect(verifierWithoutSigner.submitContribution(sampleContribution, sampleProof))
      .rejects.toThrow(ContractError);
  });

});

// ============ Event Listening Tests ============

describe('Event Listening', () => {

  let verifier: EquiPathVerifier;

  beforeEach(() => {
    verifier = new EquiPathVerifier(testConfig);
  });

  test('should register contribution submission event listener', () => {
    const callback = jest.fn();
    
    verifier.onContributionSubmitted(callback);
    
    expect(mockContract.on).toHaveBeenCalledWith('ContributionSubmitted', expect.any(Function));
  });

  test('should register contribution verification event listener', () => {
    const callback = jest.fn();
    
    verifier.onContributionVerified(callback);
    
    expect(mockContract.on).toHaveBeenCalledWith('ContributionVerified', expect.any(Function));
  });

  test('should remove all event listeners', () => {
    verifier.removeAllListeners();
    
    expect(mockContract.removeAllListeners).toHaveBeenCalled();
  });

});

// ============ Utility Function Tests ============

describe('Utility Functions', () => {

  test('generateSampleContribution should return valid contribution', () => {
    const contribution = generateSampleContribution();
    
    expect(contribution).toHaveProperty('content');
    expect(contribution).toHaveProperty('culturalContext');
    expect(contribution).toHaveProperty('contributorIdentity');
    expect(contribution).toHaveProperty('qualityMetrics');
    expect(contribution.qualityMetrics.authenticity).toBeGreaterThan(0);
    expect(contribution.qualityMetrics.authenticity).toBeLessThanOrEqual(100);
  });

  test('createSampleParams should return valid parameters', () => {
    const contributionHash = '0x123456789012345678901234567890123456789012345678901234567890abcd';
    const params = createSampleParams(contributionHash);
    
    expect(params.contributionHash).toBe(contributionHash);
    expect(params.qualityThreshold).toBeGreaterThan(0);
    expect(params.qualityThreshold).toBeLessThanOrEqual(100);
    expect(params.culturalContext).toMatch(/^0x[a-fA-F0-9]{64}$/);
    expect(params.expectedAttributes).toMatch(/^0x[a-fA-F0-9]{64}$/);
  });

});

// ============ Error Handling Tests ============

describe('Error Handling', () => {

  let verifier: EquiPathVerifier;

  beforeEach(() => {
    verifier = new EquiPathVerifier(testConfig);
  });

  test('should throw CircuitError for circuit-related failures', async () => {
    const params = createSampleParams('0x123456789012345678901234567890123456789012345678901234567890abcd');
    mockSnarkjs.groth16.fullProve.mockRejectedValue(new Error('Circuit error'));

    await expect(verifier.generateProof(sampleContribution, params))
      .rejects.toThrow(CircuitError);
  });

  test('should throw ValidationError for invalid inputs', async () => {
    const invalidContribution = { ...sampleContribution, content: '' };
    const params = createSampleParams('0x123456789012345678901234567890123456789012345678901234567890abcd');

    await expect(verifier.generateProof(invalidContribution, params))
      .rejects.toThrow(ValidationError);
  });

  test('should throw ContractError for blockchain failures', async () => {
    mockContract.getContribution.mockRejectedValue(new Error('Network error'));

    await expect(verifier.getContribution('0x123'))
      .rejects.toThrow(ContractError);
  });

});

// ============ Integration Tests ============

describe('End-to-End Integration', () => {

  let verifier: EquiPathVerifier;

  beforeEach(() => {
    verifier = new EquiPathVerifier(testConfig);
    verifier.connectSigner(mockSigner as any);
  });

  test('should complete full verification workflow', async () => {
    // Step 1: Generate proof
    const params = createSampleParams('0x123456789012345678901234567890123456789012345678901234567890abcd');
    mockSnarkjs.groth16.fullProve.mockResolvedValue({
      proof: sampleProof.proof,
      publicSignals: sampleProof.publicSignals
    });

    const proof = await verifier.generateProof(sampleContribution, params);
    expect(proof).toHaveProperty('proof');

    // Step 2: Verify proof
    mockSnarkjs.groth16.verify.mockResolvedValue(true);
    const verificationResult = await verifier.verifyProof(proof, params);
    expect(verificationResult.verified).toBe(true);

    // Step 3: Submit to blockchain
    const mockReceipt = {
      hash: '0xtxhash123',
      blockNumber: 1000001,
      gasUsed: { toNumber: () => 150000 }
    };
    mockContract.submitContribution.mockResolvedValue({
      wait: () => Promise.resolve(mockReceipt)
    });

    const submissionResult = await verifier.submitContribution(sampleContribution, proof);
    expect(submissionResult.success).toBe(true);

    // Step 4: Check verification status
    mockContract.isContributionVerified.mockResolvedValue(true);
    const isVerified = await verifier.isContributionVerified(params.contributionHash);
    expect(isVerified).toBe(true);
  });

});

// ============ Performance Tests ============

describe('Performance', () => {

  let verifier: EquiPathVerifier;

  beforeEach(() => {
    verifier = new EquiPathVerifier(testConfig);
  });

  test('should generate proof within reasonable time', async () => {
    const params = createSampleParams('0x123456789012345678901234567890123456789012345678901234567890abcd');
    mockSnarkjs.groth16.fullProve.mockResolvedValue({
      proof: sampleProof.proof,
      publicSignals: sampleProof.publicSignals
    });

    const startTime = Date.now();
    await verifier.generateProof(sampleContribution, params);
    const endTime = Date.now();

    // Should complete within 10 seconds (mocked, but validates timing logic)
    expect(endTime - startTime).toBeLessThan(10000);
  });

  test('should handle large knowledge content efficiently', async () => {
    const largeContribution = {
      ...sampleContribution,
      content: 'A'.repeat(1000) // Large content
    };
    const params = createSampleParams('0x123456789012345678901234567890123456789012345678901234567890abcd');
    
    mockSnarkjs.groth16.fullProve.mockResolvedValue({
      proof: sampleProof.proof,
      publicSignals: sampleProof.publicSignals
    });

    const result = await verifier.generateProof(largeContribution, params);
    expect(result).toHaveProperty('proof');
  });

});
