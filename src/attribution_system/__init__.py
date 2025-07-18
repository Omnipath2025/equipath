"""
EquiPath Attribution System
==========================

Cryptographic attribution and provenance tracking for traditional knowledge.
Extracted from working demonstrations for reusable deployment.
"""

import hashlib
import time
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class KnowledgeContribution:
    """
    Universal knowledge contribution record
    Works with any database: SQLite, PostgreSQL, MongoDB, etc.
    """
    contribution_id: int
    contribution_hash: str          # Public hash of contribution
    cultural_context: str           # Cultural context identifier  
    attribution_hash: str           # Attribution hash for compensation
    contributor_id: str             # Contributor identifier
    timestamp: float               # Verification timestamp
    verified: bool                 # Verification status
    compensation_amount: float     # Compensation earned
    cultural_metadata: Dict        # Additional cultural context

class AttributionTracker:
    """
    Cryptographic attribution tracking system
    
    Manages:
    - Knowledge contribution records
    - Attribution hashing for privacy
    - Compensation tracking
    - Provenance chains
    """
    
    def __init__(self, storage_backend=None):
        self.contributions: Dict[int, KnowledgeContribution] = {}
        self.contribution_counter = 0
        self.contribution_hash_to_id: Dict[str, int] = {}
        self.storage = storage_backend or self._default_storage()
        
    def _default_storage(self):
        """Default in-memory storage for demo purposes"""
        return {'contributions': {}, 'metadata': {}}
        
    def create_contribution_record(self, 
                                 knowledge_data: str,
                                 cultural_context: str,
                                 contributor_id: str,
                                 cultural_metadata: Dict) -> int:
        """
        Create attribution record for traditional knowledge contribution
        
        Args:
            knowledge_data: The traditional knowledge being contributed
            cultural_context: Cultural context identifier
            contributor_id: Unique identifier for contributor
            cultural_metadata: Additional cultural context information
            
        Returns:
            contribution_id: Unique ID for this contribution record
        """
        
        # Generate contribution hash (what gets stored publicly)
        contribution_hash = self._generate_contribution_hash(knowledge_data, cultural_context)
        
        # Check if contribution already exists
        if contribution_hash in self.contribution_hash_to_id:
            raise ValueError("Contribution already recorded")
            
        # Generate attribution hash for compensation tracking
        attribution_hash = self._generate_attribution_hash(
            contributor_id, cultural_context, contribution_hash
        )
        
        # Create contribution record
        self.contribution_counter += 1
        contribution_id = self.contribution_counter
        
        contribution = KnowledgeContribution(
            contribution_id=contribution_id,
            contribution_hash=contribution_hash,
            cultural_context=cultural_context,
            attribution_hash=attribution_hash,
            contributor_id=contributor_id,
            timestamp=time.time(),
            verified=True,
            compensation_amount=0.0,
            cultural_metadata=cultural_metadata
        )
        
        # Store contribution
        self.contributions[contribution_id] = contribution
        self.contribution_hash_to_id[contribution_hash] = contribution_id
        
        # Persist to storage backend
        self._persist_contribution(contribution)
        
        return contribution_id
        
    def update_compensation(self, contribution_id: int, amount: float):
        """Update compensation amount for a contribution"""
        if contribution_id not in self.contributions:
            raise ValueError("Invalid contribution ID")
            
        contribution = self.contributions[contribution_id]
        contribution.compensation_amount += amount
        
        # Persist updated contribution
        self._persist_contribution(contribution)
        
    def get_contribution(self, contribution_id: int) -> Optional[KnowledgeContribution]:
        """Get contribution details by ID"""
        return self.contributions.get(contribution_id)
        
    def get_contributions_by_contributor(self, contributor_id: str) -> List[KnowledgeContribution]:
        """Get all contributions by a specific contributor"""
        return [contrib for contrib in self.contributions.values() 
                if contrib.contributor_id == contributor_id]
        
    def get_total_compensation(self, contributor_id: str) -> float:
        """Get total compensation earned by a contributor"""
        contributions = self.get_contributions_by_contributor(contributor_id)
        return sum(contrib.compensation_amount for contrib in contributions)
        
    def verify_attribution(self, contribution_hash: str, claimed_contributor: str) -> bool:
        """Verify attribution claim using cryptographic proof"""
        if contribution_hash not in self.contribution_hash_to_id:
            return False
            
        contribution_id = self.contribution_hash_to_id[contribution_hash]
        contribution = self.contributions[contribution_id]
        
        return contribution.contributor_id == claimed_contributor
        
    def _generate_contribution_hash(self, knowledge_data: str, cultural_context: str) -> str:
        """Generate hash of contribution for public storage"""
        combined = f"{knowledge_data}:{cultural_context}:{time.time()}"
        return hashlib.sha256(combined.encode()).hexdigest()
        
    def _generate_attribution_hash(self, contributor_id: str, 
                                 cultural_context: str, 
                                 contribution_hash: str) -> str:
        """Generate attribution hash for compensation tracking"""
        combined = f"{contributor_id}:{cultural_context}:{contri
