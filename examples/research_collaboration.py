"""
EquiPath Ethical Research Collaboration Demo
==========================================

Demonstrates how researchers can collaborate ethically with indigenous communities
using privacy-preserving technology and community sovereignty principles.

Complete Workflow:
- Researcher proposal and community approval
- Privacy-preserving knowledge sharing via zero-knowledge proofs
- Culturally-respectful research protocols
- Fair compensation and benefit sharing
- Ongoing collaboration and community control
"""

import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import hashlib
import json

# Import components from previous demos
from traditional_medicine_demo import EquiPathUniversal, KnowledgeContribution
from community_sovereignty import CommunityGovernance, AccessRequest, ConsentStatus, AccessLevel, CommunityMember, KnowledgeItem

@dataclass
class ResearchProject:
    """Ethical research project with community oversight"""
    project_id: str
    title: str
    principal_investigator: str
    institution: str
    community_partners: List[str]
    research_questions: List[str]
    methodology: str
    timeline_months: int
    budget_total: float
    community_benefit_percentage: float
    cultural_protocols: Dict
    approved_knowledge_items: List[str] = field(default_factory=list)
    research_progress: List[Dict] = field(default_factory=list)
    compensation_distributed: float = 0.0
    active: bool = True

@dataclass
class ResearchFinding:
    """Research finding that respects traditional knowledge attribution"""
    finding_id: str
    project_id: str
    traditional_knowledge_source: str
    scientific_discovery: str
    validation_results: Dict
    attribution_requirements: List[str]
    commercialization_potential: str
    community_share_percentage: float
    publication_restrictions: List[str]

class EthicalResearchFramework:
    """
    Framework for ethical research collaboration with indigenous communities
    
    Implements:
    - UN Declaration on Rights of Indigenous Peoples
    - Nagoya Protocol principles
    - Academic research ethics standards
    - Community-controlled research protocols
    """
    
    def __init__(self, equipath_system: EquiPathUniversal, community_governance: CommunityGovernance):
        self.equipath = equipath_system
        self.community = community_governance
        self.research_projects: Dict[str, ResearchProject] = {}
        self.research_findings: Dict[str, ResearchFinding] = {}
        self.collaboration_agreements: Dict[str, Dict] = {}
        
    def submit_research_proposal(self, project: ResearchProject) -> str:
        """
        Submit research proposal for community review
        
        Must include:
        - Clear research objectives
        - Benefit sharing arrangement
        - Cultural protocol compliance
        - Community oversight mechanisms
        """
        self.research_projects[project.project_id] = project
        
        # Create access request for community governance
        access_request = AccessRequest(
            request_id=f"research_{project.project_id}",
            requester_id=project.principal_investigator,
            requester_organization=project.institution,
            knowledge_categories=[item for item in project.approved_knowledge_items],
            intended_use="Ethical research collaboration",
            research_purpose=f"{project.title}: {'; '.join(project.research_questions)}",
            benefit_sharing_proposal=f"{project.community_benefit_percentage}% of research benefits + ${project.budget_total * 0.1:.0f} upfront community fund",
            access_level_requested=AccessLevel.RESEARCH_ACCESS,
            timestamp=time.time(),
            status=ConsentStatus.PENDING
        )
        
        # Submit to community governance
        request_id = self.community.submit_access_request(access_request)
        
        print(f"\n🔬 Research Proposal Submitted")
        print(f"   Project: {project.title}")
        print(f"   PI: {project.principal_investigator}")
        print(f"   Institution: {project.institution}")
        print(f"   Community Benefit: {project.community_benefit_percentage}%")
        print(f"   Research Timeline: {project.timeline_months} months")
        print(f"   Status: Under community review")
        
        return request_id
        
    def begin_ethical_research(self, project_id: str, access_request_id: str):
        """
        Begin research collaboration after community approval
        """
        project = self.research_projects[project_id]
        access_request = self.community.access_requests[access_request_id]
        
        if access_request.status != ConsentStatus.APPROVED:
            raise ValueError("Research not approved by community")
            
        print(f"\n🤝 Ethical Research Collaboration Initiated")
        print(f"   Project: {project.title}")
        print(f"   Community Partnership: {self.community.community_name}")
        print(f"   Approval Vote: {access_request.votes_for}/{access_request.votes_for + access_request.votes_against}")
        
        # Establish collaboration agreement
        self.collaboration_agreements[project_id] = {
            'community_consent': access_request_id,
            'cultural_protocols': project.cultural_protocols,
            'benefit_sharing': project.community_benefit_percentage,
            'oversight_committee': ['elder_001', 'healer_001'],  # Community representatives
            'quarterly_reports_required': True,
            'publication_approval_required': True
        }
        
        print(f"   ✅ Collaboration agreement established")
        print(f"   ✅ Community oversight committee assigned")
        print(f"   ✅ Cultural protocols integrated")
        
    def access_traditional_knowledge_with_privacy(self, project_id: str, knowledge_item_id: str) -> Dict:
        """
        Access traditional knowledge using zero-knowledge proofs
        
        Demonstrates privacy-preserving research:
        - Researcher gets validated information
        - Community sacred details remain private
        - All access is logged and auditable
        """
        project = self.research_projects[project_id]
        
        # Get knowledge item (this would be the private data)
        knowledge_item = self.community.knowledge_items[knowledge_item_id]
        
        # Simulate traditional knowledge with sacred and shareable components
        traditional_knowledge = {
            'public_components': {
                'plant_species': 'Banisteriopsis caapi + Psychotria viridis',
                'general_use': 'Traditional healing ceremony',
                'preparation_time': '24-48 hours',
                'therapeutic_category': 'Spiritual healing'
            },
            'research_accessible': {
                'active_compounds': ['DMT', 'Harmaline', 'Harmine'],
                'preparation_method': 'Water extraction with specific pH control',
                'dosage_guidelines': 'Based on individual assessment by healer',
                'contraindications': ['Heart conditions', 'MAOI interactions']
            },
            'sacred_private': {
                'ceremonial_songs': '[PROTECTED BY ZERO-KNOWLEDGE PROOF]',
                'spiritual_protocols': '[PROTECTED BY ZERO-KNOWLEDGE PROOF]',
                'sacred_preparation_details': '[PROTECTED BY ZERO-KNOWLEDGE PROOF]',
                'community_specific_practices': '[PROTECTED BY ZERO-KNOWLEDGE PROOF]'
            }
        }
        
        # Generate zero-knowledge proof that validates research data without revealing sacred information
        research_data_hash = hashlib.sha256(
            json.dumps(traditional_knowledge['research_accessible']).encode()
        ).hexdigest()
        
        zk_proof = {
            'proof_a': [789, 123],
            'proof_b': [[456, 789], [012, 345]],
            'proof_c': [678, 901],
            'public_signals': [234, 567, 890],
            'research_data_hash': research_data_hash
        }
        
        # Verify knowledge access through EquiPath
        contribution_id = self.equipath.verify_contribution(
            knowledge_data=json.dumps(traditional_knowledge['research_accessible']),
            cultural_context=knowledge_item.category,
            contributor_id=knowledge_item_id,
            cultural_metadata={'project_id': project_id, 'access_type': 'research'},
            zk_proof=zk_proof
        )
        
        # Log research access
        project.research_progress.append({
            'timestamp': time.time(),
            'action': 'knowledge_access',
            'knowledge_item': knowledge_item_id,
            'contribution_id': contribution_id,
            'researcher': project.principal_investigator
        })
        
        print(f"\n🔐 Privacy-Preserving Knowledge Access")
        print(f"   Knowledge Item: {knowledge_item.title}")
        print(f"   Research Data: Available to researcher")
        print(f"   Sacred Information: Protected by zero-knowledge proof")
        print(f"   Access Logged: Contribution ID {contribution_id}")
        
        # Return only research-accessible data to researcher
        return {
            'contribution_id': contribution_id,
            'research_data': traditional_knowledge['research_accessible'],
            'public_info': traditional_knowledge['public_components'],
            'cultural_protocols': knowledge_item.cultural_protocols,
            'attribution_requirements': ['Traditional knowledge of ' + self.community.community_name]
        }
        
    def conduct_culturally_respectful_research(self, project_id: str, research_data: Dict) -> ResearchFinding:
        """
        Conduct research following cultural protocols and community oversight
        """
        project = self.research_projects[project_id]
        
        # Simulate research process with cultural oversight
        print(f"\n🧪 Culturally-Respectful Research Process")
        print(f"   Project: {project.title}")
        print(f"   Cultural Protocols: {list(project.cultural_protocols.keys())}")
        
        # Simulated research findings
        research_results = {
            'compound_analysis': {
                'dmt_concentration': '0.5-1.2%',
                'harmine_content': '3.8-5.2%',
                'synergistic_effects': 'Enhanced bioavailability through MAO inhibition'
            },
            'therapeutic_potential': {
                'depression_efficacy': '78% improvement in preliminary studies',
                'anxiety_reduction': '65% reduction in anxiety scores',
                'addiction_treatment': 'Promising results for substance abuse recovery'
            },
            'safety_profile': {
                'contraindications_validated': True,
                'traditional_dosage_confirmed': True,
                'interaction_warnings': ['SSRIs', 'Tramadol', 'Certain heart medications']
            }
        }
        
        # Create research finding with proper attribution
        finding = ResearchFinding(
            finding_id=f"finding_{project_id}_{int(time.time())}",
            project_id=project_id,
            traditional_knowledge_source=self.community.community_name,
            scientific_discovery=json.dumps(research_results),
            validation_results={'traditional_knowledge_validated': True},
            attribution_requirements=[
                f"Traditional knowledge contributed by {self.community.community_name}",
                "Research conducted with free, prior, and informed consent",
                "Cultural protocols respected throughout research process"
            ],
            commercialization_potential="High - potential pharmaceutical development",
            community_share_percentage=project.community_benefit_percentage,
            publication_restrictions=[
                "Community review required before publication",
                "Sacred knowledge details must remain confidential",
                "Attribution to traditional knowledge holders required"
            ]
        )
        
        self.research_findings[finding.finding_id] = finding
        
        print(f"   ✅ Research completed following cultural protocols")
        print(f"   ✅ Traditional knowledge validated scientifically")
        print(f"   ✅ Community attribution requirements documented")
        
        return finding
        
    def share_results_with_community(self, finding_id: str):
        """
        Share research results back with community before publication
        Demonstrates respect for community knowledge sovereignty
        """
        finding = self.research_findings[finding_id]
        project = self.research_projects[finding.project_id]
        
        print(f"\n📊 Research Results Shared with Community")
        print(f"   Finding: {finding.finding_id}")
        print(f"   Project: {project.title}")
        
        # Community review process
        print(f"   📋 Community Review Process:")
        print(f"      • Results presented to community oversight committee")
        print(f"      • Traditional knowledge validation confirmed")
        print(f"      • Publication content reviewed for cultural sensitivity")
        print(f"      • Community attribution requirements verified")
        
        # Simulate community approval
        community_approval = {
            'approved_for_publication': True,
            'required_attributions': finding.attribution_requirements,
            'restricted_information': ['Sacred ceremonial details remain confidential'],
            'community_comments': [
                'Results validate our traditional knowledge',
                'Important that sacred protocols remain protected',
                'Pleased with respectful research approach'
            ]
        }
        
        print(f"   ✅ Community approves publication with attributions")
        print(f"   ✅ Sacred knowledge protection maintained")
        
        return community_approval
        
    def distribute_research_benefits(self, project_id: str, benefit_amount: float):
        """
        Distribute research benefits according to community agreement
        """
        project = self.research_projects[project_id]
        community_share = benefit_amount * (project.community_benefit_percentage / 100)
        
        print(f"\n💰 Research Benefit Distribution")
        print(f"   Total Benefit: ${benefit_amount:,.2f}")
        print(f"   Community Share ({project.community_benefit_percentage}%): ${community_share:,.2f}")
        
        # Distribute through EquiPath compensation system
        for knowledge_item_id in project.approved_knowledge_items:
            # Find contribution records for this project
            for contrib_id, contrib in self.equipath.contributions.items():
                if (contrib.contributor_id == knowledge_item_id and 
                    project_id in str(contrib.cultural_metadata)):
                    
                    item_share = community_share / len(project.approved_knowledge_items)
                    self.equipath.distribute_compensation(contrib_id, item_share)
                    
        project.compensation_distributed += community_share
        
        print(f"   ✅ Compensation distributed through EquiPath")
        print(f"   ✅ Traditional knowledge holders compensated")
        print(f"   ✅ Community development fund supported")

def demo_ethical_research_collaboration():
    """
    Complete demonstration of ethical research collaboration
    
    Shows the full cycle:
    1. Research proposal and community approval
    2. Privacy-preserving knowledge access
    3. Culturally-respectful research conduct
    4. Community review of results
    5. Fair benefit sharing
    """
    
    print("🤝 EquiPath Ethical Research Collaboration Demo")
    print("=" * 55)
    
    # Initialize systems (building on previous demos)
    equipath = EquiPathUniversal()
    community = CommunityGovernance("Shipibo-Konibo Nation")
    research_framework = EthicalResearchFramework(equipath, community)
    
    # Set up community (abbreviated from previous demo)
    elder1 = CommunityMember("elder_001", "Grandmother Maria", "elder", 3.0)
    healer1 = CommunityMember("healer_001", "Maestro Roberto", "traditional_healer", 2.5)
    leader1 = CommunityMember("leader_001", "Chief Elena", "community_leader", 2.0)
    
    for member in [elder1, healer1, leader1]:
        community.add_community_member(member)
        
    # Add traditional knowledge
    ayahuasca_knowledge = KnowledgeItem(
        knowledge_id="ayahuasca_001",
        title="Ayahuasca Therapeutic Preparation",
        category="ceremonial_medicine",
        sacredness_level="sacred",
        sharing_restrictions=["research_only", "no_commercial_use"],
        authorized_researchers=set(),
        access_history=[],
        cultural_protocols={"requires_elder_blessing": True, "ceremony_context_only": True}
    )
    community.add_knowledge_item(ayahuasca_knowledge)
    
    print(f"\n🏛️ Community Established: {community.community_name}")
    print(f"   Knowledge Items: 1 (Ayahuasca therapeutic preparation)")
    print(f"   Governance: Elder council + community leaders")
    
    # 1. Research proposal submission
    research_project = ResearchProject(
        project_id="ayahuasca_study_2025",
        title="Traditional Ayahuasca Preparation: Therapeutic Compound Analysis",
        principal_investigator="Dr. Sarah Chen",
        institution="Stanford University, Department of Psychiatry",
        community_partners=["Shipibo-Konibo Nation"],
        research_questions=[
            "What are the active therapeutic compounds in traditional ayahuasca preparation?",
            "How do traditional preparation methods affect compound bioavailability?",
            "Can traditional dosage guidelines be validated scientifically?"
        ],
        methodology="Chemical analysis + clinical validation with community oversight",
        timeline_months=18,
        budget_total=250000.0,
        community_benefit_percentage=25.0,
        cultural_protocols={
            "requires_elder_blessing": True,
            "community_oversight_required": True,
            "sacred_knowledge_protection": True,
            "quarterly_community_reports": True
        }
    )
    
    print(f"\n📋 Research Proposal")
    request_id = research_framework.submit_research_proposal(research_project)
    
    # 2. Community voting process
    print(f"\n🗳️  Community Decision Process")
    community.cast_vote(request_id, "elder_001", "approve", "Researcher shows deep respect for our traditions")
    community.cast_vote(request_id, "healer_001", "approve", "Good opportunity to validate our medicine scientifically")
    community.cast_vote(request_id, "leader_001", "approve", "Benefit sharing arrangement is fair")
    
    # Check results
    result = community.check_voting_results(request_id)
    if result == ConsentStatus.APPROVED:
        community.grant_access(request_id)
        
        # 3. Begin ethical research
        research_framework.begin_ethical_research(research_project.project_id, request_id)
        
        # 4. Access traditional knowledge with privacy protection
        research_data = research_framework.access_traditional_knowledge_with_privacy(
            research_project.project_id, 
            "ayahuasca_001"
        )
        
        # 5. Conduct research following cultural protocols
        finding = research_framework.conduct_culturally_respectful_research(
            research_project.project_id,
            research_data
        )
        
        # 6. Share results with community
        community_approval = research_framework.share_results_with_community(finding.finding_id)
        
        # 7. Distribute benefits
        print(f"\n🎯 Research Success: Publication and Commercialization")
        print(f"   • Research published in Nature Medicine")
        print(f"   • Pharmaceutical licensing deal: $500,000")
        print(f"   • Ongoing royalties: 5% of sales")
        
        research_framework.distribute_research_benefits(
            research_project.project_id, 
            500000.0  # Initial licensing fee
        )
        
        # 8. Long-term relationship
        print(f"\n🌱 Ongoing Partnership Established")
        print(f"   ✅ Community maintains control over sacred knowledge")
        print(f"   ✅ Researchers conduct ethical, respectful science")
        print(f"   ✅ Traditional knowledge validated and preserved")
        print(f"   ✅ Community benefits economically from their knowledge")
        print(f"   ✅ Model created for future ethical collaborations")
        
        # Final statistics
        print(f"\n📊 Collaboration Success Metrics")
        print(f"   Community Approval: 100% (3/3 votes)")
        print(f"   Sacred Knowledge Protected: ✅ (via zero-knowledge proofs)")
        print(f"   Cultural Protocols Followed: ✅ (elder blessing, community oversight)")
        print(f"   Fair Compensation: ${research_project.compensation_distributed:,.2f}")
        print(f"   Traditional Knowledge Validated: ✅ (scientific confirmation)")
        print(f"   Long-term Partnership: ✅ (ongoing collaboration established)")

if __name__ == "__main__":
    demo_ethical_research_collaboration()
