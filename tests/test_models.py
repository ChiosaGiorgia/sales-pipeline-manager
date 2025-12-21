"""
Tests for data models
"""
import unittest
from salespipe.models import Lead, Opportunity


class TestLead(unittest.TestCase):
    """Test Lead model"""

    def test_lead_creation(self):
        """Test creating a lead"""
        lead = Lead(
            lead_id=1,
            name="Test User",
            email="test@example.com",
            phone="555-1234",
            source="test"
        )
        self.assertEqual(lead.name, "Test User")
        self.assertEqual(lead.email, "test@example.com")
        self.assertEqual(lead.status, "new")

    def test_lead_to_dict(self):
        """Test lead to dictionary conversion"""
        lead = Lead(1, "Test", "test@example.com", "555-1234", "web")
        data = lead.to_dict()
        self.assertIn('lead_id', data)
        self.assertIn('name', data)
        self.assertEqual(data['email'], "test@example.com")


class TestOpportunity(unittest.TestCase):
    """Test Opportunity model"""

    def test_opportunity_creation(self):
        """Test creating an opportunity"""
        opp = Opportunity(
            opp_id=1,
            lead_id=1,
            title="Big Sale",
            value=10000.00
        )
        self.assertEqual(opp.title, "Big Sale")
        self.assertEqual(opp.value, 10000.00)
        self.assertEqual(opp.stage, "prospecting")


if __name__ == '__main__':
    unittest.main()