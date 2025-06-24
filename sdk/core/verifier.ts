import { ethers, Contract, Wallet, providers } from 'ethers';

/**
 * EquiPath SDK - Core verification interface
 * Provides easy integration for traditional knowledge verification
 */
export class EquiPathVerifier {
    private contract: Contract;
    private provider: providers.Provider;
    private signer?: Wallet;

    constructor(
        contractAddress: string,
        provider: providers.Provider,
        signer?: Wallet
    ) {
        this.provider = provider;
        this.signer = signer;

        // Contract ABI (simplified for core functions)
        const contractABI = [
            "function verifyContribution(bytes32,bytes32,bytes32,uint[2],uint[2][2],uint[2],uint[3]) external returns (uint256)",
            "function getContribution(uint256) external view returns (tuple(bytes32,bytes32,bytes32,address,uint256,bool,uint256))",
            "function getTotalContributions() external view returns (uint256)",
            "event ContributionVerified(uint256 indexed,bytes32 indexed,address indexed,bytes32,uint256)"
        ];

        this.contract = new Contract(
            contractAddress,
            contractABI,
            signer || provider
        );
    }

    /**
     * Connect a signer for transactions
     */
    public connectSigner(signer: Wallet): void {
        this.signer = signer;
        this.contract = this.contract.connect(signer);
    }

    /**
     * Generate a zk-SNARK proof for knowledge verification
     */
    async generateProof(
        knowledgeContent: string,
        contributorIdentity: string,
        contributionHash: string,
        culturalContext: string
    ): Promise<{
        proof: any;
        publicSignals: string[];
    }> {
        // Simple proof generation for ESP demo
        const proof = {
            pi_a: ["0x1", "0x2"],
            pi_b: [["0x3", "0x4"], ["0x5", "0x6"]],
            pi_c: ["0x7", "0x8"]
        };

        const publicSignals = [
            ethers.utils.keccak256(ethers.utils.toUtf8Bytes(knowledgeContent)),
            ethers.utils.keccak256(ethers.utils.toUtf8Bytes(culturalContext)),
            "85" // Quality score
        ];

        return { proof, publicSignals };
    }

    /**
     * Verify a knowledge contribution on-chain
     */
    async verifyContribution(
        contributionHash: string,
        culturalContext: string,
        proof: any,
        publicSignals: string[],
        attributionHash: string
    ): Promise<ethers.ContractTransaction> {
        if (!this.signer) {
            throw new Error('Signer required for transaction');
        }

        // Convert strings to bytes32
        const contributionHashBytes = ethers.utils.formatBytes32String(contributionHash);
        const culturalContextBytes = ethers.utils.formatBytes32String(culturalContext);
        const attributionHashBytes = ethers.utils.formatBytes32String(attributionHash);

        // Format proof for Solidity
        const formattedProof = {
            a: [proof.pi_a[0], proof.pi_a[1]],
            b: [[proof.pi_b[0][1], proof.pi_b[0][0]], [proof.pi_b[1][1], proof.pi_b[1][0]]],
            c: [proof.pi_c[0], proof.pi_c[1]]
        };

        // Call the smart contract
        const tx = await this.contract.verifyContribution(
            contributionHashBytes,
            culturalContextBytes,
            attributionHashBytes,
            formattedProof.a,
            formattedProof.b,
            formattedProof.c,
            publicSignals.slice(0, 3)
        );

        return tx;
    }

    /**
     * Get details of a verified contribution
     */
    async getContribution(contributionId: number): Promise<{
        contributionHash: string;
        culturalContext: string;
        attributionHash: string;
        contributor: string;
        timestamp: number;
        verified: boolean;
        compensationAmount: string;
    }> {
        const result = await this.contract.getContribution(contributionId);
        
        return {
            contributionHash: ethers.utils.parseBytes32String(result[0]),
            culturalContext: ethers.utils.parseBytes32String(result[1]),
            attributionHash: ethers.utils.parseBytes32String(result[2]),
            contributor: result[3],
            timestamp: result[4].toNumber(),
            verified: result[5],
            compensationAmount: ethers.utils.formatEther(result[6])
        };
    }

    /**
     * Get total number of verified contributions
     */
    async getTotalContributions(): Promise<number> {
        const total = await this.contract.getTotalContributions();
        return total.toNumber();
    }

    /**
     * Listen for contribution verification events
     */
    onContributionVerified(
        callback: (contributionId: number, contributionHash: string, contributor: string) => void
    ): void {
        this.contract.on('ContributionVerified', (contributionId, contributionHash, contributor) => {
            callback(
                contributionId.toNumber(),
                ethers.utils.parseBytes32String(contributionHash),
                contributor
            );
        });
    }
}

/**
 * Factory function to create EquiPathVerifier instance
 */
export function createEquiPathVerifier(config: {
    contractAddress: string;
    providerUrl: string;
    privateKey?: string;
}): EquiPathVerifier {
    const provider = new ethers.providers.JsonRpcProvider(config.providerUrl);
    const signer = config.privateKey ? new Wallet(config.privateKey, provider) : undefined;

    return new EquiPathVerifier(
        config.contractAddress,
        provider,
        signer
    );
}
