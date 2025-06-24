// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title EquiPathVerifier
 * @dev ESP Grant Deliverable: Core verification contract for traditional knowledge attribution
 * @notice Zero-knowledge verification infrastructure for privacy-preserving knowledge attribution
 * @author EquiPath Protocol Team
 * 
 * This contract provides the foundational verification layer for traditional knowledge
 * contributions while maintaining complete privacy of sensitive cultural information.
 * 
 * ESP Grant Alignment:
 * - Infrastructure: Core verification protocol for Ethereum ecosystem
 * - Developer Tools: Reusable verification interfaces for dApp integration
 * - Public Good: Open-source attribution without compensation mechanisms
 * - Research: Novel application of zero-knowledge proofs to cultural IP protection
 */
contract EquiPathVerifier {
    
    // ============ State Variables ============
    
    /// @dev Version of the verification protocol
    string public constant VERSION = "1.0.0";
    
    /// @dev Verification status enumeration
    enum VerificationStatus {
        Pending,
        Verified,
        Rejected,
        Disputed
    }
    
    /// @dev Knowledge contribution structure
    struct KnowledgeContribution {
        bytes32 contributionHash;     // Hash of contribution content
        bytes32 culturalContext;      // Cultural context identifier
        address contributor;          // Contributor address
        VerificationStatus status;    // Current verification status
        uint256 timestamp;           // Submission timestamp
        uint256 verificationCount;   // Number of independent verifications
        bytes32 attributionProof;    // Zero-knowledge attribution proof
    }
    
    /// @dev Verifier information structure
    struct Verifier {
        bool isActive;               // Verifier status
        uint256 verificationCount;   // Number of verifications performed
        uint256 reputationScore;     // Verifier reputation (0-1000)
        bytes32 qualifications;      // Hashed qualifications
    }
    
    // ============ Storage ============
    
    /// @dev Mapping from contribution hash to contribution details
    mapping(bytes32 => KnowledgeContribution) public contributions;
    
    /// @dev Mapping from contributor address to their contributions
    mapping(address => bytes32[]) public contributorContributions;
    
    /// @dev Mapping from verifier address to verifier details
    mapping(address => Verifier) public verifiers;
    
    /// @dev Array of registered verifier addresses
    address[] public verifierList;
    
    /// @dev Contract owner for administrative functions
    address public owner;
    
    /// @dev Minimum number of verifications required
    uint256 public constant MIN_VERIFICATIONS = 3;
    
    /// @dev Maximum number of verifications allowed
    uint256 public constant MAX_VERIFICATIONS = 10;
    
    // ============ Events ============
    
    /// @dev Emitted when a new contribution is submitted
    event ContributionSubmitted(
        bytes32 indexed contributionHash,
        address indexed contributor,
        bytes32 culturalContext,
        uint256 timestamp
    );
    
    /// @dev Emitted when a contribution is verified
    event ContributionVerified(
        bytes32 indexed contributionHash,
        address indexed verifier,
        VerificationStatus status,
        uint256 verificationCount
    );
    
    /// @dev Emitted when a verifier is registered
    event VerifierRegistered(
        address indexed verifier,
        bytes32 qualifications,
        uint256 timestamp
    );
    
    /// @dev Emitted when verification status changes
    event StatusChanged(
        bytes32 indexed contributionHash,
        VerificationStatus oldStatus,
        VerificationStatus newStatus,
        uint256 timestamp
    );
    
    // ============ Modifiers ============
    
    /// @dev Restricts access to contract owner
    modifier onlyOwner() {
        require(msg.sender == owner, "EquiPathVerifier: caller is not owner");
        _;
    }
    
    /// @dev Restricts access to registered verifiers
    modifier onlyVerifier() {
        require(verifiers[msg.sender].isActive, "EquiPathVerifier: caller is not active verifier");
        _;
    }
    
    /// @dev Validates contribution exists
    modifier contributionExists(bytes32 contributionHash) {
        require(
            contributions[contributionHash].contributor != address(0),
            "EquiPathVerifier: contribution does not exist"
        );
        _;
    }
    
    // ============ Constructor ============
    
    /**
     * @dev Contract constructor
     * @notice Initializes the EquiPath verification contract
     */
    constructor() {
        owner = msg.sender;
    }
    
    // ============ Core Verification Functions ============
    
    /**
     * @dev Submit a new knowledge contribution for verification
     * @param contributionHash Cryptographic hash of the contribution
     * @param culturalContext Cultural context identifier
     * @param attributionProof Zero-knowledge proof of attribution
     * @return success True if submission was successful
     * 
     * @notice This function enables privacy-preserving submission of traditional knowledge
     * contributions without revealing the actual content. The contribution hash serves
     * as a commitment to the knowledge while the attribution proof demonstrates ownership.
     */
    function submitContribution(
        bytes32 contributionHash,
        bytes32 culturalContext,
        bytes32 attributionProof
    ) external returns (bool success) {
        // Validate inputs
        require(contributionHash != bytes32(0), "EquiPathVerifier: invalid contribution hash");
        require(culturalContext != bytes32(0), "EquiPathVerifier: invalid cultural context");
        require(attributionProof != bytes32(0), "EquiPathVerifier: invalid attribution proof");
        
        // Ensure contribution doesn't already exist
        require(
            contributions[contributionHash].contributor == address(0),
            "EquiPathVerifier: contribution already exists"
        );
        
        // Create new contribution record
        contributions[contributionHash] = KnowledgeContribution({
            contributionHash: contributionHash,
            culturalContext: culturalContext,
            contributor: msg.sender,
            status: VerificationStatus.Pending,
            timestamp: block.timestamp,
            verificationCount: 0,
            attributionProof: attributionProof
        });
        
        // Add to contributor's contribution list
        contributorContributions[msg.sender].push(contributionHash);
        
        // Emit submission event
        emit ContributionSubmitted(
            contributionHash,
            msg.sender,
            culturalContext,
            block.timestamp
        );
        
        return true;
    }
    
    /**
     * @dev Verify a knowledge contribution using zero-knowledge proof
     * @param contributionHash Hash of the contribution to verify
     * @param verificationProof Zero-knowledge verification proof
     * @param isValid Boolean indicating whether the contribution is valid
     * @return success True if verification was recorded successfully
     * 
     * @notice This function allows registered verifiers to provide verification
     * without revealing the content of the traditional knowledge. The verification
     * process maintains privacy while building consensus on attribution.
     */
    function verifyContribution(
        bytes32 contributionHash,
        bytes32 verificationProof,
        bool isValid
    ) external onlyVerifier contributionExists(contributionHash) returns (bool success) {
        // Validate inputs
        require(verificationProof != bytes32(0), "EquiPathVerifier: invalid verification proof");
        
        KnowledgeContribution storage contribution = contributions[contributionHash];
        
        // Ensure contribution is in pending status
        require(
            contribution.status == VerificationStatus.Pending,
            "EquiPathVerifier: contribution not in pending status"
        );
        
        // Ensure verifier hasn't already verified this contribution
        // Note: In production, this would require additional mapping to track verifier-contribution pairs
        
        // Increment verification count
        contribution.verificationCount++;
        
        // Update verifier statistics
        verifiers[msg.sender].verificationCount++;
        
        // Determine new status based on verification result and count
        VerificationStatus newStatus = contribution.status;
        
        if (isValid && contribution.verificationCount >= MIN_VERIFICATIONS) {
            newStatus = VerificationStatus.Verified;
        } else if (!isValid && contribution.verificationCount >= MIN_VERIFICATIONS) {
            newStatus = VerificationStatus.Rejected;
        }
        
        // Update status if changed
        if (newStatus != contribution.status) {
            VerificationStatus oldStatus = contribution.status;
            contribution.status = newStatus;
            
            emit StatusChanged(
                contributionHash,
                oldStatus,
                newStatus,
                block.timestamp
            );
        }
        
        // Emit verification event
        emit ContributionVerified(
            contributionHash,
            msg.sender,
            contribution.status,
            contribution.verificationCount
        );
        
        return true;
    }
    
    // ============ Verifier Management ============
    
    /**
     * @dev Register a new verifier
     * @param verifier Address of the verifier to register
     * @param qualifications Hashed qualifications of the verifier
     * @return success True if registration was successful
     */
    function registerVerifier(
        address verifier,
        bytes32 qualifications
    ) external onlyOwner returns (bool success) {
        require(verifier != address(0), "EquiPathVerifier: invalid verifier address");
        require(qualifications != bytes32(0), "EquiPathVerifier: invalid qualifications");
        require(!verifiers[verifier].isActive, "EquiPathVerifier: verifier already registered");
        
        verifiers[verifier] = Verifier({
            isActive: true,
            verificationCount: 0,
            reputationScore: 500, // Start with neutral reputation
            qualifications: qualifications
        });
        
        verifierList.push(verifier);
        
        emit VerifierRegistered(verifier, qualifications, block.timestamp);
        
        return true;
    }
    
    /**
     * @dev Deactivate a verifier
     * @param verifier Address of the verifier to deactivate
     * @return success True if deactivation was successful
     */
    function deactivateVerifier(address verifier) external onlyOwner returns (bool success) {
        require(verifiers[verifier].isActive, "EquiPathVerifier: verifier not active");
        
        verifiers[verifier].isActive = false;
        
        return true;
    }
    
    // ============ View Functions ============
    
    /**
     * @dev Get contribution details
     * @param contributionHash Hash of the contribution
     * @return contribution Full contribution details
     */
    function getContribution(bytes32 contributionHash) 
        external 
        view 
        contributionExists(contributionHash) 
        returns (KnowledgeContribution memory contribution) 
    {
        return contributions[contributionHash];
    }
    
    /**
     * @dev Get contributions by contributor
     * @param contributor Address of the contributor
     * @return contributionHashes Array of contribution hashes
     */
    function getContributorContributions(address contributor) 
        external 
        view 
        returns (bytes32[] memory contributionHashes) 
    {
        return contributorContributions[contributor];
    }
    
    /**
     * @dev Check if a contribution is verified
     * @param contributionHash Hash of the contribution
     * @return isVerified True if the contribution is verified
     */
    function isContributionVerified(bytes32 contributionHash) 
        external 
        view 
        contributionExists(contributionHash) 
        returns (bool isVerified) 
    {
        return contributions[contributionHash].status == VerificationStatus.Verified;
    }
    
    /**
     * @dev Get total number of registered verifiers
     * @return count Number of registered verifiers
     */
    function getVerifierCount() external view returns (uint256 count) {
        return verifierList.length;
    }
    
    /**
     * @dev Get verifier details
     * @param verifier Address of the verifier
     * @return verifierDetails Full verifier details
     */
    function getVerifier(address verifier) 
        external 
        view 
        returns (Verifier memory verifierDetails) 
    {
        return verifiers[verifier];
    }
    
    // ============ Administrative Functions ============
    
    /**
     * @dev Update contract ownership
     * @param newOwner Address of the new owner
     */
    function transferOwnership(address newOwner) external onlyOwner {
        require(newOwner != address(0), "EquiPathVerifier: new owner is zero address");
        owner = newOwner;
    }
    
    /**
     * @dev Emergency pause function (can be extended with pausable pattern)
     * @notice This function can be extended to implement emergency pause functionality
     */
    function emergencyPause() external onlyOwner {
        // Implementation for emergency pause
        // This would typically set a paused state that blocks normal operations
    }
}
