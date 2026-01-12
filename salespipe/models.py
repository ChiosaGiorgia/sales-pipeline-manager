"""
Data models for Sales Pipeline Manager - P.I.P.E. Industrial Systems
Complete sales funnel: Lead → Opportunity → Quote → Order
"""
from datetime import datetime


class Lead:
    """Represents a sales lead (initial contact)"""

    def __init__(self, lead_id, name, email, phone, source, status="new",
                 location=None, industry=None, company_size=None, created_at=None):
        self.lead_id = lead_id
        self.name = name
        self.email = email
        self.phone = phone
        self.source = source
        self.status = status  # new, contacted, qualified, disqualified
        self.location = location  # Operating markets: Germany, Italy, France, Benelux
        self.industry = industry  # automotive, industrial_components, food_beverage, logistics
        self.company_size = company_size  # small, medium, large
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self):
        """Now converting lead to dictionary"""
        return {
            'lead_id': self.lead_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'source': self.source,
            'status': self.status,
            'location': self.location,
            'industry': self.industry,
            'company_size': self.company_size,
            'created_at': self.created_at
        }

    def __repr__(self):
        return f"Lead({self.lead_id}, {self.name}, {self.status})"


class Opportunity:
    """to represent sales opportunities (qualified interest with estimated value)"""

    def __init__(self, opp_id, lead_id, title, estimated_value, stage="initial_inquiry",
                 probability=0, expected_close=None, created_at=None):
        self.opp_id = opp_id
        self.lead_id = lead_id
        self.title = title
        self.estimated_value = estimated_value  # Estimated commercial value (not final)
        # selling stages: initial_inquiry, qualification, proposal_development,
        # negotiation, order_confirmation, delivery
        self.stage = stage
        self.probability = probability  # 0-100%
        self.expected_close = expected_close
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self):
        """Convert opportunity to dictionary"""
        return {
            'opp_id': self.opp_id,
            'lead_id': self.lead_id,
            'title': self.title,
            'estimated_value': self.estimated_value,
            'stage': self.stage,
            'probability': self.probability,
            'expected_close': self.expected_close,
            'created_at': self.created_at
        }

    def __repr__(self):
        return f"Opportunity({self.opp_id}, {self.title}, Est: €{self.estimated_value}, {self.stage})"


class Quote:
    """Represents a formal quotation (official offer to customer)"""

    def __init__(self, quote_id, opp_id, quote_number, quoted_amount,
                 valid_until, terms=None, status="draft", created_at=None):
        self.quote_id = quote_id
        self.opp_id = opp_id
        self.quote_number = quote_number  # e.g., "Q-2024-001"
        self.quoted_amount = quoted_amount  # Official quoted price
        self.valid_until = valid_until  # Quote expiration date
        self.terms = terms  # Payment terms, delivery conditions, etc.
        self.status = status  # draft, sent, accepted, rejected, expired
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self):
        """Convert quote to dictionary"""
        return {
            'quote_id': self.quote_id,
            'opp_id': self.opp_id,
            'quote_number': self.quote_number,
            'quoted_amount': self.quoted_amount,
            'valid_until': self.valid_until,
            'terms': self.terms,
            'status': self.status,
            'created_at': self.created_at
        }

    def __repr__(self):
        return f"Quote({self.quote_number}, €{self.quoted_amount}, {self.status})"


class Order:
    """Represents a closed deal (final outcome - won or lost)"""

    def __init__(self, order_id, quote_id, status, final_amount, close_date,
                 notes=None, created_at=None):
        self.order_id = order_id
        self.quote_id = quote_id
        self.status = status  # 'won' or 'lost'
        self.final_amount = final_amount  # Actual final amount (may differ from quote)
        self.close_date = close_date
        self.notes = notes
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self):
        """converting now order to dictionary"""
        return {
            'order_id': self.order_id,
            'quote_id': self.quote_id,
            'status': self.status,
            'final_amount': self.final_amount,
            'close_date': self.close_date,
            'notes': self.notes,
            'created_at': self.created_at
        }

    def __repr__(self):
        return f"Order({self.order_id}, {self.status}, €{self.final_amount})"