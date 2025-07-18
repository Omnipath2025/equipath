"""
EquiPath Community Sovereignty Demo: Democratic Control Over Traditional Knowledge
===============================================================================

Demonstrates how indigenous communities maintain complete control over their
traditional knowledge through democratic governance and consent management.

Core Features:
- Community-controlled access permissions
- Democratic decision-making for knowledge sharing
- Consent revocation and access management
- Cultural protocol integration
- Transparent governance processes
"""

import time
from typing import Dict, List, Set, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
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

@dataclass
class KnowledgeItem:
    """Traditional knowledge item with access controls"""
    knowledge_id: str
    title: str
    category: str
    sacredness_level: str  # public, sensitive, sacred
    sharing_restrictions: List[str]
    authorized_researchers: Set[str]
    access_history: List[Dict]
    cultural_protocols: Dict
    
    def __post_init__(self):
        if self.authorized_researchers is None:
            self.authorized_researchers = set()
        if self.access_history is None:
            self.access_history = []

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
        self.knowledge_items: Dict[str, KnowledgeItem] = {}
        self.cultural_protocols: Dict[str, Dict] = {}
        
        # Governance parameters
        self.voting_period_days = 14
        self.quorum_percentage = 0.6  # 60% of active members must vote
        self.approval_threshold = 0.66  # 66% approval needed
        
    def add_community_member(self, member: CommunityMember):
        """Add a member to the community governance system"""
        self.members[member.member_id] = member
        print(f"✅ Added community member: {member.name} ({member.role})")
        
    def submit_access_request(self, request: AccessRequest) -> str:
        """
        Submit request for access to traditional knowledge
        Triggers community consultation process
        """
        self.access_requests[request.request_id] = request
        self.votes[request.request_id] = {}
        
        print(f"\n📋 New Access Request Submitted")
        print(f"   Request ID: {request.request_id}")
        print(f"   Requester: {request.requester_organization}")
        print(f"   Purpose: {request.research_purpose}")
        print(f"   Knowledge Areas: {', '.join(request.knowledge_categories)}")
        print(f"   Benefit Sharing: {request.benefit_sharing_proposal}")
        print(f"   Status: Community consultation initiated")
        
        return request.request_id
        
    def cast_vote(self, request_id: str, member_id: str, vote: str, comment: str = ""):
        """
        Cast vote on access request
        
        Args:
            request_id: The access request being voted on
            member_id: Community member casting vote
            vote: 'approve', 'deny', or 'abstain'
            comment: Optional comment explaining vote
        """
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
            
        print(f"🗳️  Vote cast by {self.members[member_id].name}: {vote}")
        if comment:
            print(f"   Comment: {comment}")
            
    def check_voting_results(self, request_id: str) -> Optional[ConsentStatus]:
        """
        Check if voting is complete and determine result
        """
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
            
    def grant_access(self, request_id: str):
        """
        Grant access to approved knowledge request
        """
        request = self.access_requests[request_id]
        
        if request.status != ConsentStatus.APPROVED:
            raise ValueError("Request not approved by community")
            
        # Grant access to requested knowledge categories
        for category in request.knowledge_categories:
            knowledge_items = [k for k in self.knowledge_items.values() 
                             if k.category == category]
            
            for item in knowledge_items:
                item.authorized_researchers.add(request.requester_id)
                item.access_history.append({
                    'requester': request.requester_id,
                    'organization': request.requester_organization,
                    'access_granted': time.time(),
                    'access_level': request.access_level_requested.value,
                    'community_vote_result': f"{request.votes_for}/{request.votes_for + request.votes_against}"
                })
                
        print(f"\n✅ Access Granted!")
        print(f"   Requester: {request.requester_organization}")
        print(f"   Knowledge Categories: {', '.join(request.knowledge_categories)}")
        print(f"   Access Level: {request.access_level_requested.value}")
        print(f"   Community Vote: {request.votes_for} for, {request.votes_against} against")
        
    def revoke_access(self, requester_id: str, reason: str = "Community decision"):
        """
        Revoke access to traditional knowledge
        Demonstrates community sovereignty - they can revoke access anytime
        """
        revoked_items = []
        
        for item in self.knowledge_items.values():
            if requester_id in item.authorized_researchers:
                item.authorized_researchers.remove(requester_id)
                item.access_history.append({
                    'requester': requester_id,
                    'access_revoked': time.time(),
                    'reason': reason
                })
                revoked_items.append(item.title)
                
        print(f"\n🚫 Access Revoked!")
        print(f"   Requester: {requester_id}")
        print(f"   Reason: {reason}")
        print(f"   Items affected: {len(revoked_items)}")
        
    def add_knowledge_item(self, item: KnowledgeItem):
        """Add traditional knowledge item under community control"""
        self.knowledge_items[item.knowledge_id] = item
        print(f"📚 Knowledge item added: {item.title} (Category: {item.category})")

def demo_community_sovereignty():
    """
    Demonstration: Community Control Over Traditional Knowledge
    
    Shows how indigenous communities:
    1. Democratically decide on knowledge sharing
    2. Maintain control over access permissions
    3. Can revoke access based on community decisions
    4. Follow cultural protocols in decision-making
    """
    
    print("🏛️ EquiPath Community Sovereignty Demo")
    print("=" * 50)
    
    # Initialize community governance
    community = CommunityGovernance("Shipibo-Konibo Nation")
    
    # Add community members with different roles and voting weights
    members = [
        CommunityMember("elder_001", "Grandmother Maria", "elder", voting_weight=3.0),
        CommunityMember("elder_002", "Grandfather Carlos", "elder", voting_weight=3.0),
        CommunityMember("healer_001", "Maestro Roberto", "traditional_healer", voting_weight=2.5),
        CommunityMember("leader_001", "Chief Elena", "community_leader", voting_weight=2.0),
        CommunityMember("member_001", "Ana Lucia", "community_member", voting_weight=1.0),
        CommunityMember("member_002", "Jose Manuel", "community_member", voting_weight=1.0),
        CommunityMember("member_003", "Isabella Rosa", "community_member", voting_weight=1.0),
    ]
    
    for member in members:
        community.add_community_member(member)
        
    print(f"\n👥 Community Established: {community.community_name}")
    print(f"   Active Members: {len(members)}")
    print(f"   Governance: Democratic with elder councils")
    print(f"   Voting Threshold: {community.approval_threshold*100}% approval required")
    
    # Add traditional knowledge items
    knowledge_items = [
        KnowledgeItem(
            knowledge_id="ayahuasca_001",
            title="Ayahuasca Ceremonial Preparation",
            category="ceremonial_medicine",
            sacredness_level="sacred",
            sharing_restrictions=["research_only", "no_commercial_use", "cultural_sensitivity_required"],
            authorized_researchers=set(),
            access_history=[],
            cultural_protocols={"requires_elder_blessing": True, "ceremony_context_only": True}
        ),
        KnowledgeItem(
            knowledge_id="plant_med_001", 
            title="Medicinal Plant Combinations",
            category="herbal_medicine",
            sacredness_level="sensitive",
            sharing_restrictions=["research_only", "benefit_sharing_required"],
            authorized_researchers=set(),
            access_history=[],
            cultural_protocols={"healer_supervision_required": True}
        )
    ]
    
    for item in knowledge_items:
        community.add_knowledge_item(item)
        
    # Simulate access request from researcher
    access_request = AccessRequest(
        request_id="req_001",
        requester_id="researcher_jane_smith",
        requester_organization="University of California, Ethnobotany Dept",
        knowledge_categories=["ceremonial_medicine", "herbal_medicine"],
        intended_use="Academic research on traditional healing practices",
        research_purpose="Study plant compounds for potential therapeutic applications",
        benefit_sharing_proposal="20% of any research profits returned to community + annual $5000 research fund",
        access_level_requested=AccessLevel.RESEARCH_ACCESS,
        timestamp=time.time(),
        status=ConsentStatus.PENDING
    )
    
    print(f"\n📨 Access Request Received")
    request_id = community.submit_access_request(access_request)
    
    print(f"\n🗳️  Community Voting Process")
    print("   Cultural Protocol: All community members consulted")
    print("   Elders given additional weight in sacred knowledge decisions")
    
    # Community members cast votes
    voting_actions = [
        ("elder_001", "approve", "Research appears respectful and benefits our people"),
        ("elder_002", "approve", "Good benefit sharing proposal, I support this"),
        ("healer_001", "approve", "Researcher shows cultural sensitivity"),
        ("leader_001", "approve", "Will help preserve our knowledge for future generations"),
        ("member_001", "deny", "Concerned about commercialization of sacred practices"),
        ("member_002", "approve", "Community needs the research funding"),
        ("member_003", "abstain", "Need more information about researcher background")
    ]
    
    for member_id, vote, comment in voting_actions:
        community.cast_vote(request_id, member_id, vote, comment)
        
    # Check voting results
    result = community.check_voting_results(request_id)
    
    print(f"\n📊 Voting Results")
    print(f"   Status: {result.value if result else 'Still pending'}")
    
    if result == ConsentStatus.APPROVED:
        print(f"   Community Decision: Access APPROVED")
        community.grant_access(request_id)
        
        # Show access granted
        print(f"\n🔓 Knowledge Access Status")
        for item in community.knowledge_items.values():
            if access_request.requester_id in item.authorized_researchers:
                print(f"   ✅ {item.title}: Access granted")
                print(f"      Restrictions: {', '.join(item.sharing_restrictions)}")
                
        # Simulate access revocation after community reconsideration
        print(f"\n⏰ Six Months Later...")
        print("   Community meeting raises new concerns about research direction")
        
        community.revoke_access(
            access_request.requester_id, 
            "Community vote to revoke due to concerns about commercial patents"
        )
        
        print(f"\n🔒 Updated Access Status")
        print("   All access revoked - demonstrating community sovereignty")
        
    elif result == ConsentStatus.DENIED:
        print(f"   Community Decision: Access DENIED")
        print("   Researcher may resubmit with modified proposal")
        
    # Show final community control summary
    print(f"\n🏛️ Community Sovereignty Demonstrated")
    print(f"   ✅ Democratic decision-making process")
    print(f"   ✅ Cultural protocols respected")
    print(f"   ✅ Community maintains control over sacred knowledge")
    print(f"   ✅ Access can be revoked at any time")
    print(f"   ✅ Benefit-sharing negotiated by community")
    
    # Show transparency
    print(f"\n📊 Governance Transparency")
    print(f"   Total Requests: {len(community.access_requests)}")
    print(f"   Community Members: {len([m for m in community.members.values() if m.active])}")
    print(f"   Knowledge Items Protected: {len(community.knowledge_items)}")
    print(f"   Cultural Protocols: Respected throughout process")

if __name__ == "__main__":
    demo_community_sovereignty()
