"""
Analytics module for P.I.P.E. Sales Pipeline
Provides conversion rates, win rates, and performance metrics
"""
from salespipe.database import Database


class Analytics:
    """Analytics calculator for sales pipeline"""

    def __init__(self, db_path="sales_pipeline.db"):
        self.db = Database(db_path)

    def get_conversion_rates(self):
        """
        Calculate conversion rates for each stage of the funnel
        Returns dict with conversion rates
        """
        self.db.connect()

        # Count leads
        self.db.cursor.execute("SELECT COUNT(*) FROM leads")
        total_leads = self.db.cursor.fetchone()[0]

        # Count opportunities
        self.db.cursor.execute("SELECT COUNT(*) FROM opportunities")
        total_opps = self.db.cursor.fetchone()[0]

        # Count quotes
        self.db.cursor.execute("SELECT COUNT(*) FROM quotes")
        total_quotes = self.db.cursor.fetchone()[0]

        # Count orders (won)
        self.db.cursor.execute("SELECT COUNT(*) FROM orders WHERE status='won'")
        total_won = self.db.cursor.fetchone()[0]

        # Count all orders
        self.db.cursor.execute("SELECT COUNT(*) FROM orders")
        total_orders = self.db.cursor.fetchone()[0]

        self.db.close()

        # Calculate conversion rates
        lead_to_opp = (total_opps / total_leads * 100) if total_leads > 0 else 0
        opp_to_quote = (total_quotes / total_opps * 100) if total_opps > 0 else 0
        quote_to_order = (total_orders / total_quotes * 100) if total_quotes > 0 else 0
        order_win_rate = (total_won / total_orders * 100) if total_orders > 0 else 0
        lead_to_won = (total_won / total_leads * 100) if total_leads > 0 else 0

        return {
            'total_leads': total_leads,
            'total_opportunities': total_opps,
            'total_quotes': total_quotes,
            'total_orders': total_orders,
            'total_won': total_won,
            'lead_to_opportunity': round(lead_to_opp, 2),
            'opportunity_to_quote': round(opp_to_quote, 2),
            'quote_to_order': round(quote_to_order, 2),
            'order_win_rate': round(order_win_rate, 2),
            'overall_conversion': round(lead_to_won, 2)
        }

    def get_win_rate(self):
        """
        Calculate overall win rate (won orders / total orders)
        """
        self.db.connect()

        self.db.cursor.execute("SELECT COUNT(*) FROM orders WHERE status='won'")
        won_orders = self.db.cursor.fetchone()[0]

        self.db.cursor.execute("SELECT COUNT(*) FROM orders")
        total_orders = self.db.cursor.fetchone()[0]

        self.db.close()

        win_rate = (won_orders / total_orders * 100) if total_orders > 0 else 0

        return {
            'won_orders': won_orders,
            'total_orders': total_orders,
            'win_rate': round(win_rate, 2)
        }

    def get_pipeline_value(self):
        """
        Calculate total pipeline value from opportunities and quotes
        """
        self.db.connect()

        # Sum of estimated values from opportunities
        self.db.cursor.execute("SELECT SUM(estimated_value) FROM opportunities")
        opp_value = self.db.cursor.fetchone()[0] or 0

        # Sum of quoted amounts
        self.db.cursor.execute("SELECT SUM(quoted_amount) FROM quotes")
        quote_value = self.db.cursor.fetchone()[0] or 0

        # Sum of won orders
        self.db.cursor.execute("SELECT SUM(final_amount) FROM orders WHERE status='won'")
        won_value = self.db.cursor.fetchone()[0] or 0

        # Sum of all orders (won + lost)
        self.db.cursor.execute("SELECT SUM(final_amount) FROM orders")
        total_closed_value = self.db.cursor.fetchone()[0] or 0

        self.db.close()

        return {
            'opportunities_value': round(opp_value, 2),
            'quotes_value': round(quote_value, 2),
            'won_value': round(won_value, 2),
            'total_closed_value': round(total_closed_value, 2),
            'total_pipeline': round(opp_value + quote_value, 2)
        }

    def get_performance_by_industry(self):
        """
        Calculate performance metrics by industry
        """
        self.db.connect()

        # Get all industries
        self.db.cursor.execute("SELECT DISTINCT industry FROM leads WHERE industry IS NOT NULL")
        industries = [row[0] for row in self.db.cursor.fetchall()]

        results = {}

        for industry in industries:
            # Count leads per industry
            self.db.cursor.execute("SELECT COUNT(*) FROM leads WHERE industry=?", (industry,))
            leads_count = self.db.cursor.fetchone()[0]

            # Count won orders per industry (via lead_id chain)
            self.db.cursor.execute("""
                                   SELECT COUNT(*)
                                   FROM orders o
                                            JOIN quotes q ON o.quote_id = q.quote_id
                                            JOIN opportunities opp ON q.opp_id = opp.opp_id
                                            JOIN leads l ON opp.lead_id = l.lead_id
                                   WHERE l.industry = ?
                                     AND o.status = 'won'
                                   """, (industry,))
            won_count = self.db.cursor.fetchone()[0]

            # Average deal value per industry
            self.db.cursor.execute("""
                                   SELECT AVG(o.final_amount)
                                   FROM orders o
                                            JOIN quotes q ON o.quote_id = q.quote_id
                                            JOIN opportunities opp ON q.opp_id = opp.opp_id
                                            JOIN leads l ON opp.lead_id = l.lead_id
                                   WHERE l.industry = ?
                                     AND o.status = 'won'
                                   """, (industry,))
            avg_value = self.db.cursor.fetchone()[0] or 0

            win_rate = (won_count / leads_count * 100) if leads_count > 0 else 0

            results[industry] = {
                'leads': leads_count,
                'won_orders': won_count,
                'win_rate': round(win_rate, 2),
                'avg_deal_value': round(avg_value, 2)
            }

        self.db.close()
        return results

    def get_performance_by_location(self):
        """
        Calculate performance metrics by geography location
        """
        self.db.connect()

        # Get all locations
        self.db.cursor.execute("SELECT DISTINCT location FROM leads WHERE location IS NOT NULL")
        locations = [row[0] for row in self.db.cursor.fetchall()]

        results = {}

        for location in locations:
            # Count leads per location
            self.db.cursor.execute("SELECT COUNT(*) FROM leads WHERE location=?", (location,))
            leads_count = self.db.cursor.fetchone()[0]

            # Count won orders per location
            self.db.cursor.execute("""
                                   SELECT COUNT(*)
                                   FROM orders o
                                            JOIN quotes q ON o.quote_id = q.quote_id
                                            JOIN opportunities opp ON q.opp_id = opp.opp_id
                                            JOIN leads l ON opp.lead_id = l.lead_id
                                   WHERE l.location = ?
                                     AND o.status = 'won'
                                   """, (location,))
            won_count = self.db.cursor.fetchone()[0]

            # Pipeline value per location
            self.db.cursor.execute("""
                                   SELECT SUM(opp.estimated_value)
                                   FROM opportunities opp
                                            JOIN leads l ON opp.lead_id = l.lead_id
                                   WHERE l.location = ?
                                   """, (location,))
            pipeline_value = self.db.cursor.fetchone()[0] or 0

            win_rate = (won_count / leads_count * 100) if leads_count > 0 else 0

            results[location] = {
                'leads': leads_count,
                'won_orders': won_count,
                'win_rate': round(win_rate, 2),
                'pipeline_value': round(pipeline_value, 2)
            }

        self.db.close()
        return results