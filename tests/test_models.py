"""
Tests for database operations
"""
import unittest
import os
from salespipe.database import Database
from salespipe.models import Lead, Opportunity, Quote, Order


class TestDatabase(unittest.TestCase):
    """Test Database class"""

    def setUp(self):
        """Set up test database before each test"""
        self.test_db = "test_pipeline.db"
        # Remove test db if exists
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

        self.db = Database(self.test_db)
        self.db.create_tables()

    def tearDown(self):
        """Clean up test database after each test"""
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_create_tables(self):
        """Test database tables creation"""
        self.db.connect()

        # Check leads table exists
        self.db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='leads'")
        self.assertIsNotNone(self.db.cursor.fetchone())

        # Check opportunities table exists
        self.db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='opportunities'")
        self.assertIsNotNone(self.db.cursor.fetchone())

        # Check quotes table exists
        self.db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='quotes'")
        self.assertIsNotNone(self.db.cursor.fetchone())

        # Check orders table exists
        self.db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders'")
        self.assertIsNotNone(self.db.cursor.fetchone())

        self.db.close()

    def test_add_and_get_lead(self):
        """Test adding and retrieving a lead"""
        lead = Lead(
            lead_id=None,
            name="Test Company",
            email="test@company.com",
            phone="555-0001",
            source="website",
            location="Germany",
            industry="automotive",
            company_size="large"
        )

        lead_id = self.db.add_lead(lead)
        self.assertIsNotNone(lead_id)
        self.assertGreater(lead_id, 0)

        # Retrieve leads
        leads = self.db.get_all_leads()
        self.assertEqual(len(leads), 1)
        self.assertEqual(leads[0][1], "Test Company")
        self.assertEqual(leads[0][6], "Germany")
        self.assertEqual(leads[0][7], "automotive")

    def test_add_and_get_opportunity(self):
        """Test adding and retrieving an opportunity"""
        # First add a lead
        lead = Lead(None, "Test Co", "test@co.com", "555", "web")
        lead_id = self.db.add_lead(lead)

        # Add opportunity
        opp = Opportunity(
            opp_id=None,
            lead_id=lead_id,
            title="Big Deal",
            estimated_value=50000.00,
            stage="qualification"
        )

        opp_id = self.db.add_opportunity(opp)
        self.assertIsNotNone(opp_id)

        # Retrieve opportunities
        opps = self.db.get_all_opportunities()
        self.assertEqual(len(opps), 1)
        self.assertEqual(opps[0][2], "Big Deal")
        self.assertEqual(opps[0][3], 50000.00)

    def test_add_and_get_quote(self):
        """Test adding and retrieving a quote"""
        # Add lead and opportunity first
        lead = Lead(None, "Test", "t@t.com", "555", "web")
        lead_id = self.db.add_lead(lead)

        opp = Opportunity(None, lead_id, "Deal", 30000, "proposal_development")
        opp_id = self.db.add_opportunity(opp)

        # Add quote
        quote = Quote(
            quote_id=None,
            opp_id=opp_id,
            quote_number="Q-2024-001",
            quoted_amount=28000.00,
            valid_until="2025-01-31",
            terms="Net 30 days",
            status="sent"
        )

        quote_id = self.db.add_quote(quote)
        self.assertIsNotNone(quote_id)

        # Retrieve quotes
        quotes = self.db.get_all_quotes()
        self.assertEqual(len(quotes), 1)
        self.assertEqual(quotes[0][2], "Q-2024-001")
        self.assertEqual(quotes[0][3], 28000.00)
        self.assertEqual(quotes[0][6], "sent")

    def test_add_and_get_order(self):
        """Test adding and retrieving an order"""
        # Add lead, opportunity, and quote first
        lead = Lead(None, "Test", "t@t.com", "555", "web")
        lead_id = self.db.add_lead(lead)

        opp = Opportunity(None, lead_id, "Deal", 25000, "negotiation")
        opp_id = self.db.add_opportunity(opp)

        quote = Quote(None, opp_id, "Q-001", 24000, "2025-01-31", "Net 30")
        quote_id = self.db.add_quote(quote)

        # Add order
        order = Order(
            order_id=None,
            quote_id=quote_id,
            status="won",
            final_amount=23500.00,
            close_date="2024-12-20",
            notes="Successful deal with 2% discount"
        )

        order_id = self.db.add_order(order)
        self.assertIsNotNone(order_id)

        # Retrieve orders
        orders = self.db.get_all_orders()
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0][2], "won")
        self.assertEqual(orders[0][3], 23500.00)

    def test_complete_sales_funnel(self):
        """Test complete sales funnel: Lead -> Opp -> Quote -> Order"""
        # Create lead
        lead = Lead(None, "P.I.P.E. Client", "client@pipe.com", "555-1234",
                    "trade_show", location="Germany", industry="automotive",
                    company_size="large")
        lead_id = self.db.add_lead(lead)

        # Create opportunity
        opp = Opportunity(None, lead_id, "Robotic Cell Project", 150000.00,
                          "proposal_development", 60)
        opp_id = self.db.add_opportunity(opp)

        # Create quote
        quote = Quote(None, opp_id, "Q-2024-PIPE-001", 145000.00,
                      "2025-02-28", "50% upfront, 50% on delivery", "sent")
        quote_id = self.db.add_quote(quote)

        # Create order
        order = Order(None, quote_id, "won", 142000.00, "2024-12-20",
                      "Final negotiation: 3% discount")
        order_id = self.db.add_order(order)

        # Verify complete funnel
        self.assertGreater(lead_id, 0)
        self.assertGreater(opp_id, 0)
        self.assertGreater(quote_id, 0)
        self.assertGreater(order_id, 0)

        # Verify data consistency
        leads = self.db.get_all_leads()
        opps = self.db.get_all_opportunities()
        quotes = self.db.get_all_quotes()
        orders = self.db.get_all_orders()

        self.assertEqual(len(leads), 1)
        self.assertEqual(len(opps), 1)
        self.assertEqual(len(quotes), 1)
        self.assertEqual(len(orders), 1)

    def test_multiple_leads(self):
        """Test adding multiple leads"""
        for i in range(5):
            lead = Lead(None, f"Company{i}", f"email{i}@test.com",
                        f"555-000{i}", "web")
            self.db.add_lead(lead)

        leads = self.db.get_all_leads()
        self.assertEqual(len(leads), 5)


if __name__ == '__main__':
    unittest.main()