"""
EquiPath Compensation Framework
==============================

Fair compensation and benefit distribution for traditional knowledge contributors.
Extracted from working demonstrations for reusable deployment.
"""

import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class PaymentStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class CompensationType(Enum):
    RESEARCH_FEE = "research_fee"
    ROYALTY_PAYMENT = "royalty_payment"
    MILESTONE_PAYMENT = "milestone_payment"
    COMMUNITY_FUND = "community_fund"

@dataclass
class CompensationRecord:
    """Record of compensation payment to traditional knowledge contributor"""
    payment_id: str
    contribution_id: int
    recipient_id: str
    amount: float
    compensation_type: CompensationType
    payment_method: str  # crypto, bank_transfer, community_fund, etc.
    transaction_reference: str
    timestamp: float
    status: PaymentStatus
    cultural_context: str
    notes: str = ""

@dataclass
class BenefitSharingAgreement:
    """Agreement for sharing benefits from traditional knowledge use"""
    agreement_id: str
    contribution_id: int
    researcher_organization: str
    community_id: str
    base_compensation: float
    royalty_percentage: float
    milestone_payments: Dict[str, float]
    community_fund_percentage: float
    agreement_terms: List[str]
    signed_timestamp: float
    active: bool = True

class CompensationEngine:
    """
    Fair compensation system for traditional knowledge contributors
    
    Features:
    - Multiple payment methods (crypto, traditional banking, community funds)
    - Automatic royalty distribution
    - Milestone-based payments
    - Community benefit sharing
    - Transparent payment tracking
    """
    
    def __init__(self, payment_backend=None):
        self.compensation_records: Dict[str, CompensationRecord] = {}
        self.benefit_agreements: Dict[str, BenefitSharingAgreement] = {}
        self.payment_counter = 0
        
        # Payment backend (could integrate with various payment systems)
        self.payment_backend = payment_backend or self._default_payment_system()
        
    def _default_payment_system(self):
        """Default payment system for demonstration"""
        return {'payments': {}, 'balances': {}}
        
    def create_benefit_sharing_agreement(self, agreement: BenefitSharingAgreement) -> str:
        """Create benefit sharing agreement for traditional knowledge use"""
        self.benefit_agreements[agreement.agreement_id] = agreement
        
        print(f"📋 Benefit Sharing Agreement Created")
        print(f"   Agreement ID: {agreement.agreement_id}")
        print(f"   Community: {agreement.community_id}")
        print(f"   Researcher: {agreement.researcher_organization}")
        print(f"   Base Compensation: ${agreement.base_compensation:,.2f}")
        print(f"   Royalty Rate: {agreement.royalty_percentage}%")
        print(f"   Community Fund: {agreement.community_fund_percentage}%")
        
        return agreement.agreement_id
        
    def process_compensation_payment(self, 
                                   contribution_id: int,
                                   recipient_id: str,
                                   amount: float,
                                   compensation_type: CompensationType,
                                   cultural_context: str,
                                   payment_method: str = "digital_transfer") -> str:
        """
        Process compensation payment to traditional knowledge contributor
        
        Args:
            contribution_id: ID of the knowledge contribution
            recipient_id: ID of the recipient (individual or community)
            amount: Payment amount
            compensation_type: Type of compensation
            cultural_context: Cultural context for the payment
            payment_method: How payment should be made
            
        Returns:
            payment_id: Unique identifier for this payment
        """
        
        self.payment_counter += 1
        payment_id = f"pay_{self.payment_counter}_{int(time.time())}"
        
        # Process payment through backend
        transaction_ref = self._process_payment_backend(
            recipient_id, amount, payment_method
        )
        
        # Create compensation record
        compensation = CompensationRecord(
            payment_id=payment_id,
            contribution_id=contribution_id,
            recipient_id=recipient_id,
            amount=amount,
            compensation_type=compensation_type,
            payment_method=payment_method,
            transaction_reference=transaction_ref,
            timestamp=time.time(),
            status=PaymentStatus.COMPLETED,
            cultural_context=cultural_context,
            notes=f"Compensation for traditional knowledge contribution #{contribution_id}"
        )
        
        self.compensation_records[payment_id] = compensation
        
        print(f"💰 Compensation Payment Processed")
        print(f"   Payment ID: {payment_id}")
        print(f"   Recipient: {recipient_id}")
        print(f"   Amount: ${amount:,.2f}")
        print(f"   Type: {compensation_type.value}")
        print(f"   Method: {payment_method}")
        print(f"   Status: {compensation.status.value}")
        
        return payment_id
        
    def distribute_royalty_payment(self, agreement_id: str, total_revenue: float) -> List[str]:
        """
        Distribute royalty payments based on benefit sharing agreement
        
        Args:
            agreement_id: Benefit sharing agreement ID
            total_revenue: Total revenue to distribute
            
        Returns:
            List of payment IDs for tracking
        """
        
        if agreement_id not in self.benefit_agreements:
            raise ValueError("Invalid agreement ID")
            
        agreement = self.benefit_agreements[agreement_id]
        
        if not agreement.active:
            raise ValueError("Agreement is not active")
            
        # Calculate payments
        royalty_amount = total_revenue * (agreement.royalty_percentage / 100)
        community_fund_amount = royalty_amount * (agreement.community_fund_percentage / 100)
        contributor_amount = royalty_amount - community_fund_amount
        
        payment_ids = []
        
        # Pay individual contributor
        if contributor_amount > 0:
            payment_id = self.process_compensation_payment(
                contribution_id=agreement.contribution_id,
                recipient_id=f"contributor_{agreement.contribution_id}",
                amount=contributor_amount,
                compensation_type=CompensationType.ROYALTY_PAYMENT,
                cultural_context=agreement.community_id,
                payment_method="direct_transfer"
            )
            payment_ids.append(payment_id)
            
        # Pay community fund
        if community_fund_amount > 0:
            payment_id = self.process_compensation_payment(
                contribution_id=agreement.contribution_id,
                recipient_id=agreement.community_id,
                amount=community_fund_amount,
                compensation_type=CompensationType.COMMUNITY_FUND,
                cultural_context=agreement.community_id,
                payment_method="community_fund"
            )
            payment_ids.append(payment_id)
            
        print(f"\n📊 Royalty Distribution Summary")
        print(f"   Total Revenue: ${total_revenue:,.2f}")
        print(f"   Royalty Rate: {agreement.royalty_percentage}%")
        print(f"   Total Royalty: ${royalty_amount:,.2f}")
        print(f"   Contributor Share: ${contributor_amount:,.2f}")
        print(f"   Community Fund: ${community_fund_amount:,.2f}")
        print(f"   Payments Created: {len(payment_ids)}")
        
        return payment_ids
        
    def process_milestone_payment(self, agreement_id: str, milestone_name: str) -> Optional[str]:
        """
        Process milestone-based payment
        
        Args:
            agreement_id: Benefit sharing agreement ID
            milestone_name: Name of the milestone reached
            
        Returns:
            payment_id if payment processed, None if milestone not found
        """
        
        if agreement_id not in self.benefit_agreements:
            raise ValueError("Invalid agreement ID")
            
        agreement = self.benefit_agreements[agreement_id]
        
        if milestone_name not in agreement.milestone_payments:
            return None
            
        milestone_amount = agreement.milestone_payments[milestone_name]
        
        payment_id = self.process_compensation_payment(
            contribution_id=agreement.contribution_id,
            recipient_id=agreement.community_id,
            amount=milestone_amount,
            compensation_type=CompensationType.MILESTONE_PAYMENT,
            cultural_context=agreement.community_id,
            payment_method="milestone_transfer"
        )
        
        print(f"🎯 Milestone Payment Processed")
        print(f"   Milestone: {milestone_name}")
        print(f"   Amount: ${milestone_amount:,.2f}")
        print(f"   Payment ID: {payment_id}")
        
        return payment_id
        
    def get_compensation_history(self, recipient_id: str) -> List[CompensationRecord]:
        """Get compensation history for a recipient"""
        return [record for record in self.compensation_records.values()
                if record.recipient_id == recipient_id]
                
    def get_total_compensation(self, recipient_id: str) -> float:
        """Get total compensation earned by a recipient"""
        history = self.get_compensation_history(recipient_id)
        return sum(record.amount for record in history 
                  if record.status == PaymentStatus.COMPLETED)
                  
    def get_payment_analytics(self) -> Dict:
        """Get analytics on compensation payments"""
        total_payments = len(self.compensation_records)
        total_amount = sum(record.amount for record in self.compensation_records.values()
                          if record.status == PaymentStatus.COMPLETED)
        
        payment_types = {}
        for record in self.compensation_records.values():
            comp_type = record.compensation_type.value
            if comp_type not in payment_types:
                payment_types[comp_type] = {'count': 0, 'amount': 0}
            payment_types[comp_type]['count'] += 1
            payment_types[comp_type]['amount'] += record.amount
            
        return {
            'total_payments': total_payments,
            'total_amount_distributed': total_amount,
            'payment_breakdown': payment_types,
            'active_agreements': len([a for a in self.benefit_agreements.values() if a.active])
        }
        
    def _process_payment_backend(self, recipient_id: str, amount: float, method: str) -> str:
        """Process payment through backend system"""
        # In production: integrate with actual payment systems
        # For demo: simulate payment processing
        transaction_ref = f"txn_{int(time.time())}_{hash(recipient_id) % 10000}"
        
        # Update backend balances
        if recipient_id not in self.payment_backend['balances']:
            self.payment_backend['balances'][recipient_id] = 0
        self.payment_backend['balances'][recipient_id] += amount
        
        # Store payment record
        self.payment_backend['payments'][transaction_ref] = {
            'recipient': recipient_id,
            'amount': amount,
            'method': method,
            'timestamp': time.time()
        }
        
        return transaction_ref

__all__ = ['CompensationEngine', 'BenefitSharingAgreement', 'CompensationRecord', 
           'CompensationType', 'PaymentStatus']
