/**
 * @file verifier.ts
 * @title EquiPath Verification SDK
 * @dev ESP Grant Deliverable: Core TypeScript SDK for traditional knowledge verification
 * @notice Developer tools for integrating privacy-preserving knowledge verification
 * @author EquiPath Protocol Team
 * @version 1.0.0
 * 
 * This SDK provides developers with easy-to-use interfaces for integrating
 * EquiPath's zero-knowledge verification system into their applications.
 * 
 * ESP Grant Alignment:
 * - Developer Tools: Simple APIs for knowledge verification integration
 * - Infrastructure: Reusable components for Ethereum dApp development  
 * - Public Good: Open-source SDK with comprehensive documentation
 * - Research: Practical implementation of zk-SNARK verification protocols
 */

import { ethers } from 'ethers';
import * as snarkjs from 'snarkjs';
import { poseidon } from 'circomlibjs';

// ============ Type Definitions ============

/**
 * @dev Knowledge contribution interface
 */
export interface KnowledgeContribution {
  content: string;
  culturalContext: string;
  contributorIdentity: string;
  qualityMetrics: QualityMetrics;
  contextDetails: string;
  culturalCredentials: string;
}

/**
 * @dev Quality metrics for knowledge evaluation
 */
export interface QualityMetrics {
  authenticity: number;      // 0-100: How authentic is the knowledge
  completeness: number;      // 0-100: How complete is the information
  accuracy: number;          // 0-100: How accurate is the knowledge
  culturalSignificance: number; // 0-100: Cultural importance level
}

/**
 * @dev Verification parameters
 */
export interface VerificationParams {
  contributionHash: string;
  culturalContext: string;
  qualityThreshold: number;
  expectedAttributes: string;
}

/**
 * @dev Zero-knowledge proof structure
 */
export interface ZKProof {
  proof: {
    pi_a: string[];
    pi_b: string[][];
    pi_c: string[];
  };
  publicSignals: string[];
}

/**
 * @dev Verification result
 */
export interface VerificationResult {
  verified: boolean;
  attributionProof: string;
  qualityScore: number;
  transactionHash?: string;
  gasUsed?: number;
}

/**
 * @dev SDK configuration
 */
export interface EquiPathConfig {
  contractAddress: string;
  providerUrl: string;
  circuitWasmPath: string;
  circuitZkeyPath: string;
  maxKnowledgeLength: number;
  maxContextLength: number;
}

/**
 * @dev Contract interaction result
 */
export interface ContractResult {
  success: boolean;
  transactionHash: string;
  blockNumber: number;
  gasUsed: number;
  error?: string;
}

// ============ Error Classes ============

export class EquiPathError extends Error {
  constructor(message: string, public code: string) {
    super(message);
    this.name = 'EquiPathError';
  }
}

export class CircuitError extends EquiPathError {
  constructor(message: string) {
    super(message, 'CIRCUIT_ERROR');
  }
}

export class ContractError extends EquiPathError {
  constructor(message: string) {
    super(message, 'CONTRACT_ERROR');
  }
}

export class ValidationError extends EquiPathError {
  constructor(message: string) {
    super(message, 'VALIDATION_ERROR');
  }
}

// ============ Main SDK Class ============

/**
 * @class EquiPathVerifier
 * @dev Main SDK class for EquiPath verification system
 */
export class EquiPathVerifier {
  private config: EquiPathConfig;
  private provider: ethers.Provider;
  private contract: ethers.Contract;
  private signer?: ethers.Signer;

  // Contract ABI (simplified for ESP demonstration)
  private readonly contractABI = [
    "function submitContribution(bytes32 contributionHash, bytes32 culturalContext, bytes32 attributionProof) external returns (bool)",
    "function verifyContribution(bytes32 contributionHash, bytes32 verificationProof, bool isValid) external returns (bool)",
    "function getContribution(bytes32 contributionHash) external view returns (tuple(bytes32 contributionHash, bytes32 culturalContext, address contributor, uint8 status, uint256 timestamp, uint256 verificationCount, bytes32 attributionProof))",
    "function isContributionVerified(bytes32 contributionHash) external view returns (bool)",
    "event ContributionSubmitted(bytes32 indexed contributionHash, address indexed contributor, bytes32 culturalContext, uint256 timestamp)",
    "event ContributionVerified(bytes32 indexed contributionHash, address indexed verifier, uint8 status, uint256 verificationCount)"
  ];

  /**
   * @dev Constructor
   * @param config SDK configuration parameters
   */
  constructor(config: EquiPathConfig) {
    this.config = config;
    this.provider = new ethers.JsonRpcProvider(config.providerUrl);
    this.contract = new ethers.Contract(
      config.contractAddress,
      this.contractABI,
      this.provider
    );
  }

  /**
   * @dev Connect wallet signer for transaction execution
   * @param signer Ethereum signer (wallet)
   */
  public connectSigner(signer: ethers.Signer): void {
    this.signer = signer;
    this.contract = this.contract.connect(signer);
  }

  // ============ Core Verification Functions ============

  /**
   * @dev Generate zero-knowledge proof for knowledge contribution
   * @param contribution Knowledge contribution data
   * @param params Verification parameters
   * @returns ZK proof object
   */
  public async generateProof(
    contribution: KnowledgeContribution,
    params: VerificationParams
  ): Promise<ZKProof> {
    try {
      // Validate inputs
      this.validateContribution(contribution);
      this.validateParams(params);

      // Prepare circuit inputs
      const circuitInputs = await this.prepareCircuitInputs(contribution, params);

      // Generate zero-knowledge proof
      const { proof, publicSignals } = await snarkjs.groth16.fullProve(
        circuitInputs,
        this.config.circuitWasmPath,
        this.config.circuitZkeyPath
      );

      return {
        proof: {
          pi_a: proof.pi_a,
          pi_b: proof.pi_b,
          pi_c: proof.pi_c
        },
        publicSignals
      };

    } catch (error) {
      throw new CircuitError(`Failed to generate proof: ${error.message}`);
    }
  }

  /**
   * @dev Verify zero-knowledge proof
   * @param proof ZK proof to verify
   * @param params Verification parameters
   * @returns Verification result
   */
  public async verifyProof(
    proof: ZKProof,
    params: VerificationParams
  ): Promise<VerificationResult> {
    try {
      // Load verification key (in production, this would be cached)
      const vKey = await this.loadVerificationKey();

      // Verify the proof cryptographically
      const isValidProof = await snarkjs.groth16.verify(
        vKey,
        proof.publicSignals,
        proof.proof
      );

      if (!isValidProof) {
        return {
          verified: false,
          attributionProof: '',
          qualityScore: 0
        };
      }

      // Extract results from public signals
      const verified = proof.publicSignals[0] === '1';
      const attributionProof = proof.publicSignals[1];
      const qualityScore = parseInt(proof.publicSignals[2]);

      return {
        verified,
        attributionProof,
        qualityScore
      };

    } catch (error) {
      throw new CircuitError(`Failed to verify proof: ${error.message}`);
    }
  }

  /**
   * @dev Submit contribution to blockchain
   * @param contribution Knowledge contribution
   * @param proof Generated ZK proof
   * @returns Contract interaction result
   */
  public async submitContribution(
    contribution: KnowledgeContribution,
    proof: ZKProof
  ): Promise<ContractResult> {
    try {
      if (!this.signer) {
        throw new ContractError('Signer not connected. Call connectSigner() first.');
      }

      // Generate contribution hash
      const contributionHash = await this.generateContributionHash(contribution);
      
      // Generate cultural context hash
      const culturalContextHash = await this.generateCulturalContextHash(
        contribution.culturalContext,
        contribution.contextDetails
      );

      // Submit to smart contract
      const tx = await this.contract.submitContribution(
        contributionHash,
        culturalContextHash,
        proof.publicSignals[1] // Attribution proof
      );

      const receipt = await tx.wait();

      return {
        success: true,
        transactionHash: receipt.hash,
        blockNumber: receipt.blockNumber,
        gasUsed: receipt.gasUsed.toNumber()
      };

    } catch (error) {
      return {
        success: false,
        transactionHash: '',
        blockNumber: 0,
        gasUsed: 0,
        error: error.message
      };
    }
  }

  /**
   * @dev Check if contribution is verified on-chain
   * @param contributionHash Hash of the contribution
   * @returns Boolean verification status
   */
  public async isContributionVerified(contributionHash: string): Promise<boolean> {
    try {
      return await this.contract.isContributionVerified(contributionHash);
    } catch (error) {
      throw new ContractError(`Failed to check verification status: ${error.message}`);
    }
  }

  /**
   * @dev Get contribution details from blockchain
   * @param contributionHash Hash of the contribution
   * @returns Contribution details
   */
  public async getContribution(contributionHash: string): Promise<any> {
    try {
      const contribution = await this.contract.getContribution(contributionHash);
      
      return {
        contributionHash: contribution.contributionHash,
        culturalContext: contribution.culturalContext,
        contributor: contribution.contributor,
        status: contribution.status,
        timestamp: new Date(contribution.timestamp.toNumber() * 1000),
        verificationCount: contribution.verificationCount.toNumber(),
        attributionProof: contribution.attributionProof
      };

    } catch (error) {
      throw new ContractError(`Failed to get contribution: ${error.message}`);
    }
  }

  // ============ Helper Functions ============

  /**
   * @dev Validate knowledge contribution data
   * @param contribution Contribution to validate
   */
  private validateContribution(contribution: KnowledgeContribution): void {
    if (!contribution.content || contribution.content.length === 0) {
      throw new ValidationError('Knowledge content cannot be empty');
    }

    if (!contribution.culturalContext || contribution.culturalContext.length === 0) {
      throw new ValidationError('Cultural context cannot be empty');
    }

    if (!contribution.contributorIdentity || contribution.contributorIdentity.length === 0) {
      throw new ValidationError('Contributor identity cannot be empty');
    }

    // Validate quality metrics
    const metrics = contribution.qualityMetrics;
    if (metrics.authenticity < 0 || metrics.authenticity > 100) {
      throw new ValidationError('Authenticity score must be between 0 and 100');
    }
    if (metrics.completeness < 0 || metrics.completeness > 100) {
      throw new ValidationError('Completeness score must be between 0 and 100');
    }
    if (metrics.accuracy < 0 || metrics.accuracy > 100) {
      throw new ValidationError('Accuracy score must be between 0 and 100');
    }
    if (metrics.culturalSignificance < 0 || metrics.culturalSignificance > 100) {
      throw new ValidationError('Cultural significance score must be between 0 and 100');
    }
  }

  /**
   * @dev Validate verification parameters
   * @param params Parameters to validate  
   */
  private validateParams(params: VerificationParams): void {
    if (!params.contributionHash || params.contributionHash.length !== 66) {
      throw new ValidationError('Invalid contribution hash format');
    }

    if (!params.culturalContext || params.culturalContext.length !== 66) {
      throw new ValidationError('Invalid cultural context hash format');
    }

    if (params.qualityThreshold < 0 || params.qualityThreshold > 100) {
      throw new ValidationError('Quality threshold must be between 0 and 100');
    }
  }

  /**
   * @dev Prepare inputs for circuit computation
   * @param contribution Knowledge contribution
   * @param params Verification parameters
   * @returns Circuit inputs object
   */
  private async prepareCircuitInputs(
    contribution: KnowledgeContribution,
    params: VerificationParams
  ): Promise<any> {
    // Convert strings to field elements for circuit
    const knowledgeContent = this.stringToFieldArray(
      contribution.content,
      this.config.maxKnowledgeLength
    );

    const contextDetails = this.stringToFieldArray(
      contribution.contextDetails,
      this.config.maxContextLength
    );

    const contributorIdentity = this.stringToField(contribution.contributorIdentity);
    const culturalCredentials = this.stringToField(contribution.culturalCredentials);

    return {
      // Public inputs
      contributionHash: params.contributionHash,
      culturalContext: params.culturalContext,
      qualityThreshold: params.qualityThreshold,
      expectedAttributes: params.expectedAttributes,

      // Private inputs
      knowledgeContent,
      contributorIdentity,
      contextDetails,
      qualityMetrics: [
        contribution.qualityMetrics.authenticity,
        contribution.qualityMetrics.completeness,
        contribution.qualityMetrics.accuracy,
        contribution.qualityMetrics.culturalSignificance
      ],
      culturalCredentials
    };
  }

  /**
   * @dev Generate cryptographic hash of contribution
   * @param contribution Knowledge contribution
   * @returns Contribution hash
   */
  private async generateContributionHash(contribution: KnowledgeContribution): Promise<string> {
    const combined = contribution.content + contribution.contributorIdentity;
    return ethers.keccak256(ethers.toUtf8Bytes(combined));
  }

  /**
   * @dev Generate cultural context hash
   * @param context Public cultural context
   * @param details Private context details
   * @returns Cultural context hash
   */
  private async generateCulturalContextHash(
    context: string,
    details: string
  ): Promise<string> {
    const combined = context + details;
    return ethers.keccak256(ethers.toUtf8Bytes(combined));
  }

  /**
   * @dev Convert string to field element array for circuits
   * @param str Input string
   * @param maxLength Maximum array length
   * @returns Field element array
   */
  private stringToFieldArray(str: string, maxLength: number): string[] {
    const bytes = ethers.toUtf8Bytes(str);
    const result: string[] = [];

    for (let i = 0; i < maxLength; i++) {
      if (i < bytes.length) {
        result.push(bytes[i].toString());
      } else {
        result.push('0');
      }
    }

    return result;
  }

  /**
   * @dev Convert string to single field element
   * @param str Input string
   * @returns Field element as string
   */
  private stringToField(str: string): string {
    return ethers.keccak256(ethers.toUtf8Bytes(str));
  }

  /**
   * @dev Load verification key for proof verification
   * @returns Verification key object
   */
  private async loadVerificationKey(): Promise<any> {
    // In production, this would load from a file or cache
    // For ESP demonstration, return mock verification key structure
    return {
      protocol: "groth16",
      curve: "bn128",
      nPublic: 4,
      vk_alpha_1: ["0", "0", "0"],
      vk_beta_2: [["0", "0"], ["0", "0"], ["0", "0"]],
      vk_gamma_2: [["0", "0"], ["0", "0"], ["0", "0"]],
      vk_delta_2: [["0", "0"], ["0", "0"], ["0", "0"]],
      vk_alphabeta_12: [[["0", "0"], ["0", "0"]], [["0", "0"], ["0", "0"]]],
      IC: [["0", "0", "0"], ["0", "0", "0"], ["0", "0", "0"], ["0", "0", "0"], ["0", "0", "0"]]
    };
  }

  // ============ Event Listening ============

  /**
   * @dev Listen for contribution submission events
   * @param callback Function to call when event is detected
   */
  public onContributionSubmitted(
    callback: (contributionHash: string, contributor: string, timestamp: Date) => void
  ): void {
    this.contract.on('ContributionSubmitted', (contributionHash, contributor, culturalContext, timestamp) => {
      callback(contributionHash, contributor, new Date(timestamp.toNumber() * 1000));
    });
  }

  /**
   * @dev Listen for contribution verification events
   * @param callback Function to call when event is detected
   */
  public onContributionVerified(
    callback: (contributionHash: string, verifier: string, status: number) => void
  ): void {
    this.contract.on('ContributionVerified', (contributionHash, verifier, status, verificationCount) => {
      callback(contributionHash, verifier, status);
    });
  }

  /**
   * @dev Stop listening to contract events
   */
  public removeAllListeners(): void {
    this.contract.removeAllListeners();
  }
}

// ============ Factory Functions ============

/**
 * @dev Create EquiPathVerifier instance with default configuration
 * @param contractAddress Smart contract address
 * @param providerUrl Ethereum provider URL
 * @returns Configured EquiPathVerifier instance
 */
export function createEquiPathVerifier(
  contractAddress: string,
  providerUrl: string
): EquiPathVerifier {
  const config: EquiPathConfig = {
    contractAddress,
    providerUrl,
    circuitWasmPath: './circuits/knowledge_verification.wasm',
    circuitZkeyPath: './circuits/knowledge_verification_final.zkey',
    maxKnowledgeLength: 256,
    maxContextLength: 128
  };

  return new EquiPathVerifier(config);
}

/**
 * @dev Create EquiPathVerifier instance for testnet
 * @param contractAddress Smart contract address on testnet
 * @returns Testnet-configured EquiPathVerifier instance
 */
export function createTestnetVerifier(contractAddress: string): EquiPathVerifier {
  return createEquiPathVerifier(
    contractAddress,
    'https://eth-sepolia.g.alchemy.com/v2/demo'
  );
}

// ============ Utility Functions ============

/**
 * @dev Generate sample knowledge contribution for testing
 * @returns Sample contribution object
 */
export function generateSampleContribution(): KnowledgeContribution {
  return {
    content: 'Traditional herbal remedy for common ailments using locally sourced plants',
    culturalContext: 'Indigenous knowledge from Pacific Northwest traditional medicine',
    contributorIdentity: 'verified-traditional-healer-001',
    qualityMetrics: {
      authenticity: 95,
      completeness: 87,
      accuracy: 92,
      culturalSignificance: 98
    },
    contextDetails: 'Passed down through five generations of traditional healers',
    culturalCredentials: 'Certified by tribal council as authentic traditional healer'
  };
}

/**
 * @dev Create verification parameters for testing
 * @param contributionHash Hash of the contribution
 * @returns Sample verification parameters
 */
export function createSampleParams(contributionHash: string): VerificationParams {
  return {
    contributionHash,
    culturalContext: ethers.keccak256(ethers.toUtf8Bytes('traditional-medicine-pacific-northwest')),
    qualityThreshold: 80,
    expectedAttributes: ethers.keccak256(ethers.toUtf8Bytes('herbal-remedy-traditional'))
  };
}

// Export all types and classes
export default EquiPathVerifier;
