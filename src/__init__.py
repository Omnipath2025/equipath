"""
EquiPath: Universal Traditional Knowledge Protection Platform
===========================================================

Privacy-preserving, community-controlled platform for protecting traditional knowledge
through zero-knowledge proofs, democratic governance, and fair compensation.

Universal Implementation - Works with any database, platform, or deployment environment.
"""

__version__ = "1.0.0"
__author__ = "Cloak & Quill Research"
__license__ = "MIT"

# Import core components
from .zkp_engine import ZKProofValidator
from .community_control import (
    CommunityGovernance, 
    CommunityMember, 
    AccessRequest, 
    ConsentStatus, 
    AccessLevel
)
from .attribution_system import (
    AttributionTracker, 
    ProvenanceChain, 
    KnowledgeContribution
)
from .compensation_framework import (
    CompensationEngine, 
    BenefitSharingAgreement, 
    CompensationRecord, 
    CompensationType, 
    PaymentStatus
)

class EquiPathPlatform:
    """
    Complete EquiPath Platform
    
    Unified interface for all traditional knowledge protection features:
    - Zero-knowledge proof privacy protection
    - Community democratic governance
    - Cryptographic attribution tracking
    - Fair compensation distribution
    """
    
    def __init__(self, community_name: str = "Default Community"):
        """Initialize complete EquiPath platform"""
        
        # Initialize all subsystems
        self.zkp_validator = ZKProofValidator()
        self.community_governance = CommunityGovernance(community_name)
        self.attribution_tracker = AttributionTracker()
        self.compensation_engine = CompensationEngine()
        self.provenance_chain = ProvenanceChain()
        
        print(f"🛡️ EquiPath Platform Initialized")
        print(f"   Community: {community_name}")
        print(f"   Privacy: Zero-knowledge proof protection")
        print(f"   Governance: Democratic community control")
        print(f"   Attribution: Cryptographic tracking")
        print(f"   Compensation: Fair benefit distribution")
        
    def get_platform_status(self) -> dict:
        """Get overall platform status and statistics"""
        return {
            'community_name': self.community_governance.community_name,
            'active_members': len([m for m in self.community_governance.members.values() if m.active]),
            'total_contributions': len(self.attribution_tracker.contributions),
            'pending_access_requests': len([r for r in self.community_governance.access_requests.values() 
                                          if r.status == ConsentStatus.PENDING]),
            'total_compensation_distributed': sum(r.amount for r in self.compensation_engine.compensation_records.values()),
            'platform_version': __version__
        }

# Export all main components
__all__ = [
    # Core Platform
    'EquiPathPlatform',
    
    # Zero-Knowledge Proofs
    'ZKProofValidator',
    
    # Community Control
    'CommunityGovernance',
    'CommunityMember', 
    'AccessRequest',
    'ConsentStatus',
    'AccessLevel',
    
    # Attribution System
    'AttributionTracker',
    'ProvenanceChain', 
    'KnowledgeContribution',
    
    # Compensation Framework
    'CompensationEngine',
    'BenefitSharingAgreement',
    'CompensationRecord',
    'CompensationType',
    'PaymentStatus',
    
    # Metadata
    '__version__',
    '__author__',
    '__license__'
]

# Platform information
PLATFORM_INFO = {
    'name': 'EquiPath',
    'description': 'Universal Traditional Knowledge Protection Platform',
    'version': __version__,
    'author': __author__,
    'license': __license__,
    'supports': [
        'Zero-knowledge proof privacy protection',
        'Democratic community governance', 
        'Cryptographic attribution tracking',
        'Fair compensation distribution',
        'Universal platform deployment'
    ],
    'compatible_with': [
        'Any database system',
        'Any blockchain platform', 
        'Any payment system',
        'Any web/mobile application',
        'Any cloud or on-premise deployment'
    ]
}
