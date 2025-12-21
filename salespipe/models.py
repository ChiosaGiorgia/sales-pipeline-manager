"""
Data models for Sales Pipeline Manager
"""
from datetime import datetime


class Lead:
    """Represents a sales lead"""

    def __init__(self, lead_id, name, email, phone, source, status="new", created_at=None):
        self.lead_id = lead_id
        self.name = name
        self.email = email
        self.phone = phone
        self.source = source
        self.status = status
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self):
        """Convert lead to dictionary"""
        return {
            'lead_id': self.lead_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'source': self.source,
            'status': self.status,
            'created_at': self.created_at
        }

    def __repr__(self):
        return f"Lead({self.lead_id}, {self.name}, {self.status})"


class Opportunity:
    """Represents a sales opportunity"""

    def __init__(self, opp_id, lead_id, title, value, stage="prospecting",
                 probability=0, expected_close=None, created_at=None):
        self.opp_id = opp_id
        self.lead_id = lead_id
        self.title = title
        self.value = value
        self.stage = stage
        self.probability = probability
        self.expected_close = expected_close
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self):
        """Convert opportunity to dictionary"""
        return {
            'opp_id': self.opp_id,
            'lead_id': self.lead_id,
            'title': self.title,
            'value': self.value,
            'stage': self.stage,
            'probability': self.probability,
            'expected_close': self.expected_close,
            'created_at': self.created_at
        }

    def __repr__(self):
        return f"Opportunity({self.opp_id}, {self.title}, ${self.value}, {self.stage})"

    class Order:
        """Represents a closed deal (won or lost)"""

        def __init__(self, order_id, opp_id, status, close_date, notes=None, created_at=None):
            self.order_id = order_id
            self.opp_id = opp_id
            self.status = status  # 'won' or 'lost'
            self.close_date = close_date
            self.notes = notes
            self.created_at = created_at or datetime.now().isoformat()

        def to_dict(self):
            """Convert order to dictionary"""
            return {
                'order_id': self.order_id,
                'opp_id': self.opp_id,
                'status': self.status,
                'close_date': self.close_date,
                'notes': self.notes,
                'created_at': self.created_at
            }

        def __repr__(self):
            return f"Order({self.order_id}, {self.status}, {self.close_date})"