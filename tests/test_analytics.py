"""
Tests for analytics module
"""
import unittest
import os
from salespipe.database import Database
from salespipe.models import Lead, Opportunity, Quote, Order
from salespipe.analytics import Analytics


class TestAnalytics(unittest.TestCase):
    """Test Analytics class"""

    def setUp(self):
        """Set up test database with sample data"""
        self.test_db = "test_analytics.db"

        # Remove test db if exists
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

        self.db = Database(self.test_db)
        self.db.create_tables()
        self.analytics = Analytics(self.test_db)

        # Create sample data
        self._create_sample_data()

    def tearDown(self):
        """Clean up test database"""
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def _create_sample_data(self):
        """Create sample data for testing"""
        # Add 5 leads
        lead1 = Lead(None, "AutoCorp", "auto@corp.com", "555-001", "web",
                     location="Germany", industry="automotive", company_size="large")
        lead_id1 = self.db.add_lead(lead1)

        lead2 = Lead(None, "TechCo", "tech@co.com", "555-002", "referral",
                     location="Italy", industry="industrial_components", company_size="medium")
        lead_id2 = self.db.add_lead(lead2)

        lead3 = Lead(None, "FoodPack", "food@pack.com", "555-003", "linkedin",
                     location="France", industry="food_beverage", company_size="large")
        lead_id3 = self.db.add_lead(lead3)

        # Add some leads without opportunities
        self.db.add_lead(Lead(None, "NoOpp1", "no1@test.com", "555-004", "web"))
        self.db.add_lead(Lead(None, "NoOpp2", "no2@test.com", "555-005", "web"))

        # Add 3 opportunities
        opp1 = Opportunity(None, lead_id1, "Robot Cell", 150000, "negotiation", 80)
        opp_id1 = self.db.add_opportunity(opp1)

        opp2 = Opportunity(None, lead_id2, "CNC Machine", 80000, "proposal_development", 60)
        opp_id2 = self.db.add_opportunity(opp2)

        opp3 = Opportunity(None, lead_id3, "Packaging Line", 120000, "qualification", 40)
        opp_id3 = self.db.add_opportunity(opp3)

        # Add 2 quotes
        quote1 = Quote(None, opp_id1, "Q-2024-001", 145000, "2025-01-31", "Net 30", "sent")
        quote_id1 = self.db.add_quote(quote1)

        quote2 = Quote(None, opp_id2, "Q-2024-002", 78000, "2025-02-15", "Net 30", "sent")
        quote_id2 = self.db.add_quote(quote2)

        # Add 2 orders (1 won, 1 lost)
        order1 = Order(None, quote_id1, "won", 142000, "2024-12-20", "Success")
        self.db.add_order(order1)

        order2 = Order(None, quote_id2, "lost", 0, "2024-12-21", "Price too high")
        self.db.add_order(order2)

    def test_conversion_rates(self):
        """Test conversion rate calculation"""
        rates = self.analytics.get_conversion_rates()

        self.assertEqual(rates['total_leads'], 5)
        self.assertEqual(rates['total_opportunities'], 3)
        self.assertEqual(rates['total_quotes'], 2)
        self.assertEqual(rates['total_orders'], 2)
        self.assertEqual(rates['total_won'], 1)

        # Lead to Opportunity: 3/5 = 60%
        self.assertEqual(rates['lead_to_opportunity'], 60.0)

        # Opportunity to Quote: 2/3 = 66.67%
        self.assertAlmostEqual(rates['opportunity_to_quote'], 66.67, places=1)

        # Quote to Order: 2/2 = 100%
        self.assertEqual(rates['quote_to_order'], 100.0)

        # Order Win Rate: 1/2 = 50%
        self.assertEqual(rates['order_win_rate'], 50.0)

        # Overall: 1/5 = 20%
        self.assertEqual(rates['overall_conversion'], 20.0)

    def test_win_rate(self):
        """Test win rate calculation"""
        data = self.analytics.get_win_rate()

        self.assertEqual(data['won_orders'], 1)
        self.assertEqual(data['total_orders'], 2)
        self.assertEqual(data['win_rate'], 50.0)

    def test_pipeline_value(self):
        """Test pipeline value calculation"""
        data = self.analytics.get_pipeline_value()

        # Opportunities: 150k + 80k + 120k = 350k
        self.assertEqual(data['opportunities_value'], 350000.0)

        # Quotes: 145k + 78k = 223k
        self.assertEqual(data['quotes_value'], 223000.0)

        # Won: 142k
        self.assertEqual(data['won_value'], 142000.0)

        # Total Pipeline: 350k + 223k = 573k
        self.assertEqual(data['total_pipeline'], 573000.0)

    def test_performance_by_industry(self):
        """Test performance by industry"""
        data = self.analytics.get_performance_by_industry()

        # Should have 3 industries
        self.assertEqual(len(data), 3)
        self.assertIn('automotive', data)
        self.assertIn('industrial_components', data)
        self.assertIn('food_beverage', data)

        # Automotive: 1 lead, 1 won
        self.assertEqual(data['automotive']['leads'], 1)
        self.assertEqual(data['automotive']['won_orders'], 1)
        self.assertEqual(data['automotive']['win_rate'], 100.0)
        self.assertEqual(data['automotive']['avg_deal_value'], 142000.0)

    def test_performance_by_location(self):
        """Test performance by location"""
        data = self.analytics.get_performance_by_location()

        # Should have 3 locations
        self.assertEqual(len(data), 3)
        self.assertIn('Germany', data)
        self.assertIn('Italy', data)
        self.assertIn('France', data)

        # Germany: 1 lead, 1 won, pipeline 150k
        self.assertEqual(data['Germany']['leads'], 1)
        self.assertEqual(data['Germany']['won_orders'], 1)
        self.assertEqual(data['Germany']['win_rate'], 100.0)
        self.assertEqual(data['Germany']['pipeline_value'], 150000.0)

    def test_empty_database(self):
        """Test analytics with empty database"""
        # Create new empty database
        empty_db = "test_empty.db"
        if os.path.exists(empty_db):
            os.remove(empty_db)

        db = Database(empty_db)
        db.create_tables()
        analytics = Analytics(empty_db)

        rates = analytics.get_conversion_rates()
        self.assertEqual(rates['total_leads'], 0)
        self.assertEqual(rates['overall_conversion'], 0)

        # Clean up
        if os.path.exists(empty_db):
            os.remove(empty_db)


if __name__ == '__main__':
    unittest.main()