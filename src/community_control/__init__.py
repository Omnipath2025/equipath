"""
EquiPath Community Control System
================================

Democratic governance and consent management for traditional knowledge.
Extracted from community_sovereignty.py for reusable deployment.
"""

import time
from typing import Dict, List, Set, Optional
from dataclasses import dataclass
from enum import Enum

class ConsentStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    REVOKED = "revoked"

class AccessLevel(Enum):
    NONE = "none"
    BASIC_INFO = "basic_info"
    RESEARCH_ACCESS = "research_access"
    FULL_ACCESS = "full_access"

@dataclass
class CommunityMember:
    """Community member with voting rights"""
    member_id: str
    name: str
    role: str  # elder, healer, community_leader, member
    voting_weight: float  # elders might have more weight
    active: bool = True

@dataclass
class AccessRequest:
    """Request for access to traditional knowledge"""
    request_id: str
    requester_id: str
    requester_organization: str
    knowledge_categories: List[str]
    intended_use: str
    research_purpose: str
    benefit_sharing_proposal: str
    access_level_requested: AccessLevel
    timestamp: float
    status: ConsentStatus
    votes_for: int = 0
    votes_against: int = 0
    community_comments: List[str] = None
    
    def __post_init__(self):
        if self.community_comments is None:
            self.community_comments = []

class CommunityGovernance:
    """
    Democratic governance system for traditional knowledge sharing decisions
    
    Implements UN Declaration on Rights of Indigenous Peoples principles:
    - Free, Prior, and Informed Consent (FPIC)
    - Community self-determination
    - Cultural protocol respect
    """
    
    def __init__(self, community_name: str):
        self.community_name = community_name
        self.members: Dict[str, CommunityMember] = {}
        self.access_requests: Dict[str, AccessRequest] = {}
        self.votes: Dict[str, Dict[str, str]] = {}  # request_id -> {member_id: vote}
        
        # Governance parameters
        self.voting_period_days = 14
        self.quorum_percentage = 0.6  # 60% of active members must vote
        self.approval_threshold = 0.66  # 66% approval needed
        
    def add_community_member(self, member: CommunityMember):
        """Add a member to the community governance system"""
        self.members[member.member_id] = member
        
    def submit_access_request(self, request: AccessRequest) -> str:
        """Submit request for access to traditional knowledge"""
        self.access_requests[request.request_id] = request
        self.votes[request.request_id] = {}
        return request.request_id
        
    def cast_vote(self, request_id: str, member_id: str, vote: str, comment: str = ""):
        """Cast vote on access request"""
        if request_id not in self.access_requests:
            raise ValueError("Invalid request ID")
            
        if member_id not in self.members:
            raise ValueError("Invalid member ID")
            
        if not self.members[member_id].active:
            raise ValueError("Member not active")
            
        request = self.access_requests[request_id]
        if request.status != ConsentStatus.PENDING:
            raise ValueError("Voting period has ended")
            
        # Record vote
        self.votes[request_id][member_id] = vote
        
        if comment:
            request.community_comments.append(f"{self.members[member_id].name}: {comment}")
            
    def check_voting_results(self, request_id: str) -> Optional[ConsentStatus]:
        """Check if voting is complete and determine result"""
        if request_id not in self.access_requests:
            return None
            
        request = self.access_requests[request_id]
        votes = self.votes[request_id]
        
        # Count active members
        active_members = [m for m in self.members.values() if m.active]
        total_voting_weight = sum(m.voting_weight for m in active_members)
        
        # Count votes with weights
        votes_cast_weight = 0
        weighted_approve = 0
        weighted_deny = 0
        
        for member_id, vote in votes.items():
            member = self.members[member_id]
            votes_cast_weight += member.voting_weight
            
            if vote == 'approve':
                weighted_approve += member.voting_weight
            elif vote == 'deny':
                weighted_deny += member.voting_weight
                
        # Check if quorum reached
        if votes_cast_weight < (total_voting_weight * self.quorum_percentage):
            return None  # Still waiting for quorum
            
        # Calculate approval percentage
        total_decisive_votes = weighted_approve + weighted_deny
        if total_decisive_votes == 0:
            return ConsentStatus.DENIED  # All abstained = denial
            
        approval_percentage = weighted_approve / total_decisive_votes
        
        # Determine result
        if approval_percentage >= self.approval_threshold:
            request.status = ConsentStatus.APPROVED
            request.votes_for = int(weighted_approve)
            request.votes_against = int(weighted_deny)
            return ConsentStatus.APPROVED
        else:
            request.status = ConsentStatus.DENIED
            request.votes_for = int(weighted_approve)
            request.votes_against = int(weighted_deny)
            return ConsentStatus.DENIED

__all__ = ['CommunityGovernance', 'CommunityMember', 'AccessRequest', 'ConsentStatus', 'AccessLevel']
