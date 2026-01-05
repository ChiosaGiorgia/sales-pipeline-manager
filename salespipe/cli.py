"""
Command Line Interface for Sales Pipeline Manager
"""
import argparse
from salespipe.database import Database
from salespipe.models import Lead, Opportunity, Quote, Order
from salespipe.csv_handler import CSVHandler
from salespipe.analytics import Analytics


class CLI:
    """Command Line Interface handler"""

    def __init__(self):
        self.db = Database()
        self.db.create_tables()
        self.analytics = Analytics()

    def add_lead(self, args):
        """Add a new lead"""
        lead = Lead(
            lead_id=None,
            name=args.name,
            email=args.email,
            phone=args.phone,
            source=args.source,
            status="new",
            location=args.location,
            industry=args.industry,
            company_size=args.company_size
        )
        lead_id = self.db.add_lead(lead)
        print(f"✓ Lead added successfully! ID: {lead_id}")

    def list_leads(self, args):
        """List all leads"""
        leads = self.db.get_all_leads()
        if not leads:
            print("No leads found.")
            return

        print(f"\n{'ID':<5} {'Name':<20} {'Email':<30} {'Status':<15} {'Industry':<20} {'Location':<15}")
        print("-" * 110)
        for lead in leads:
            print(
                f"{lead[0]:<5} {lead[1]:<20} {lead[2]:<30} {lead[5]:<15} {lead[7] or 'N/A':<20} {lead[6] or 'N/A':<15}")
        print(f"\nTotal: {len(leads)} leads")

    def export_leads(self, args):
        """Export leads to CSV"""
        leads = self.db.get_all_leads()
        CSVHandler.export_leads_to_csv(leads, args.output)

    def import_leads(self, args):
        """Import leads from CSV"""
        leads = CSVHandler.import_leads_from_csv(args.input)
        for lead in leads:
            self.db.add_lead(lead)
        print(f"✓ Imported {len(leads)} leads to database")

    def show_analytics(self, args):
        """Show analytics based on type"""
        if args.type == 'conversion':
            self._show_conversion_rates()
        elif args.type == 'winrate':
            self._show_win_rate()
        elif args.type == 'pipeline':
            self._show_pipeline_value()
        elif args.type == 'industry':
            self._show_industry_performance()
        elif args.type == 'location':
            self._show_location_performance()
        else:
            print("Unknown analytics type. Use: conversion, winrate, pipeline, industry, or location")

    def _show_conversion_rates(self):
        """Display conversion rates"""
        rates = self.analytics.get_conversion_rates()

        print("\n=== CONVERSION RATES ===")
        print(f"\nFunnel Overview:")
        print(f"  Total Leads:         {rates['total_leads']}")
        print(f"  Total Opportunities: {rates['total_opportunities']}")
        print(f"  Total Quotes:        {rates['total_quotes']}")
        print(f"  Total Orders:        {rates['total_orders']}")
        print(f"  Won Orders:          {rates['total_won']}")

        print(f"\nConversion Rates:")
        print(f"  Lead → Opportunity:   {rates['lead_to_opportunity']}%")
        print(f"  Opportunity → Quote:  {rates['opportunity_to_quote']}%")
        print(f"  Quote → Order:        {rates['quote_to_order']}%")
        print(f"  Order Win Rate:       {rates['order_win_rate']}%")
        print(f"  Overall (Lead → Won): {rates['overall_conversion']}%")

    def _show_win_rate(self):
        """Display win rate"""
        data = self.analytics.get_win_rate()

        print("\n=== WIN RATE ===")
        print(f"  Won Orders:   {data['won_orders']}")
        print(f"  Total Orders: {data['total_orders']}")
        print(f"  Win Rate:     {data['win_rate']}%")

    def _show_pipeline_value(self):
        """Display pipeline value"""
        data = self.analytics.get_pipeline_value()

        print("\n=== PIPELINE VALUE ===")
        print(f"  Opportunities Value: €{data['opportunities_value']:,.2f}")
        print(f"  Quotes Value:        €{data['quotes_value']:,.2f}")
        print(f"  Total Pipeline:      €{data['total_pipeline']:,.2f}")
        print(f"\n  Won Value:           €{data['won_value']:,.2f}")
        print(f"  Total Closed:        €{data['total_closed_value']:,.2f}")

    def _show_industry_performance(self):
        """Display performance by industry"""
        data = self.analytics.get_performance_by_industry()

        if not data:
            print("\nNo industry data available.")
            return

        print("\n=== PERFORMANCE BY INDUSTRY ===")
        print(f"\n{'Industry':<25} {'Leads':<10} {'Won':<10} {'Win Rate':<12} {'Avg Deal':<15}")
        print("-" * 75)

        for industry, metrics in data.items():
            print(f"{industry:<25} {metrics['leads']:<10} {metrics['won_orders']:<10} "
                  f"{metrics['win_rate']:<11}% €{metrics['avg_deal_value']:>12,.2f}")

    def _show_location_performance(self):
        """Display performance by location"""
        data = self.analytics.get_performance_by_location()

        if not data:
            print("\nNo location data available.")
            return

        print("\n=== PERFORMANCE BY LOCATION ===")
        print(f"\n{'Location':<20} {'Leads':<10} {'Won':<10} {'Win Rate':<12} {'Pipeline':<15}")
        print("-" * 70)

        for location, metrics in data.items():
            print(f"{location:<20} {metrics['leads']:<10} {metrics['won_orders']:<10} "
                  f"{metrics['win_rate']:<11}% €{metrics['pipeline_value']:>12,.2f}")

    def show_company(self, args):
        """Show all records for a company and provide interactive options"""
        company_name = args.name

        # Search for leads with this company name
        self.db.connect()
        self.db.cursor.execute(
            "SELECT * FROM leads WHERE name LIKE ?",
            (f"%{company_name}%",)
        )
        leads = self.db.cursor.fetchall()
        self.db.close()

        if not leads:
            print(f"\nNo company found matching '{company_name}'")
            return

        # Show all data for each matching lead
        for lead in leads:
            lead_id = lead[0]
            lead_name = lead[1]

            print(f"\n{'=' * 70}")
            print(f"COMPANY: {lead_name}")
            print(f"{'=' * 70}")

            # Show lead info
            print(f"\nLEAD INFO:")
            print(f"  ID: {lead[0]}")
            print(f"  Email: {lead[2]}")
            print(f"  Phone: {lead[3]}")
            print(f"  Status: {lead[5]}")
            print(f"  Location: {lead[6] or 'N/A'}")
            print(f"  Industry: {lead[7] or 'N/A'}")
            print(f"  Company Size: {lead[8] or 'N/A'}")

            # Get opportunities for this lead
            self.db.connect()
            self.db.cursor.execute(
                "SELECT * FROM opportunities WHERE lead_id=?",
                (lead_id,)
            )
            opportunities = self.db.cursor.fetchall()
            self.db.close()

            if opportunities:
                print(f"\nOPPORTUNITIES:")
                for opp in opportunities:
                    print(f"  [{opp[0]}] {opp[2]} - EUR {opp[3]:,.2f} ({opp[4]})")

                    # Get quotes for this opportunity
                    self.db.connect()
                    self.db.cursor.execute(
                        "SELECT * FROM quotes WHERE opp_id=?",
                        (opp[0],)
                    )
                    quotes = self.db.cursor.fetchall()
                    self.db.close()

                    if quotes:
                        print(f"      QUOTES:")
                        for quote in quotes:
                            print(f"        [{quote[0]}] {quote[2]} - EUR {quote[3]:,.2f} ({quote[6]})")

                            # Get orders for this quote
                            self.db.connect()
                            self.db.cursor.execute(
                                "SELECT * FROM orders WHERE quote_id=?",
                                (quote[0],)
                            )
                            orders = self.db.cursor.fetchall()
                            self.db.close()

                            if orders:
                                print(f"            ORDERS:")
                                for order in orders:
                                    status_symbol = "WON" if order[2] == "won" else "LOST"
                                    print(f"              [{order[0]}] {status_symbol} - EUR {order[3]:,.2f}")
            else:
                print(f"\nOPPORTUNITIES: None")

            print(f"\n{'=' * 70}\n")

    def add_opportunity_cmd(self, args):
        """Add an opportunity for an existing lead"""
        # Find lead by name
        self.db.connect()
        self.db.cursor.execute(
            "SELECT lead_id, name FROM leads WHERE name LIKE ?",
            (f"%{args.lead_name}%",)
        )
        lead = self.db.cursor.fetchone()
        self.db.close()

        if not lead:
            print(f"Error: No lead found matching '{args.lead_name}'")
            return

        lead_id, lead_name = lead

        # Create opportunity
        opp = Opportunity(
            opp_id=None,
            lead_id=lead_id,
            title=args.title,
            estimated_value=args.value,
            stage=args.stage or "initial_inquiry",
            probability=args.probability or 0,
            expected_close=args.expected_close
        )

        opp_id = self.db.add_opportunity(opp)
        print(f"\nOpportunity created successfully!")
        print(f"  Company: {lead_name}")
        print(f"  Opportunity ID: {opp_id}")
        print(f"  Title: {args.title}")
        print(f"  Value: EUR {args.value:,.2f}")
        print(f"  Stage: {opp.stage}")

    def add_quote_cmd(self, args):
        """Add a quote for an existing opportunity"""
        # Find opportunity by title
        self.db.connect()
        self.db.cursor.execute(
            "SELECT opp_id, title, lead_id FROM opportunities WHERE title LIKE ?",
            (f"%{args.opportunity_title}%",)
        )
        opp = self.db.cursor.fetchone()

        if not opp:
            self.db.close()
            print(f"Error: No opportunity found matching '{args.opportunity_title}'")
            return

        opp_id, opp_title, lead_id = opp

        # Get company name
        self.db.cursor.execute("SELECT name FROM leads WHERE lead_id=?", (lead_id,))
        company_name = self.db.cursor.fetchone()[0]
        self.db.close()

        # Create quote
        quote = Quote(
            quote_id=None,
            opp_id=opp_id,
            quote_number=args.quote_number,
            quoted_amount=args.amount,
            valid_until=args.valid_until,
            terms=args.terms,
            status=args.status or "draft"
        )

        quote_id = self.db.add_quote(quote)
        print(f"\nQuote created successfully!")
        print(f"  Company: {company_name}")
        print(f"  Opportunity: {opp_title}")
        print(f"  Quote ID: {quote_id}")
        print(f"  Quote Number: {args.quote_number}")
        print(f"  Amount: EUR {args.amount:,.2f}")
        print(f"  Status: {quote.status}")

    def add_order_cmd(self, args):
        """Add an order (close a quote)"""
        # Find quote by number
        self.db.connect()
        self.db.cursor.execute(
            "SELECT quote_id, quote_number, opp_id, quoted_amount FROM quotes WHERE quote_number LIKE ?",
            (f"%{args.quote_number}%",)
        )
        quote = self.db.cursor.fetchone()

        if not quote:
            self.db.close()
            print(f"Error: No quote found matching '{args.quote_number}'")
            return

        quote_id, quote_number, opp_id, quoted_amount = quote

        # Get opportunity and company info
        self.db.cursor.execute(
            "SELECT o.title, l.name FROM opportunities o JOIN leads l ON o.lead_id = l.lead_id WHERE o.opp_id=?",
            (opp_id,)
        )
        opp_info = self.db.cursor.fetchone()
        opp_title, company_name = opp_info
        self.db.close()

        # Create order
        order = Order(
            order_id=None,
            quote_id=quote_id,
            status=args.status,
            final_amount=args.final_amount,
            close_date=args.close_date,
            notes=args.notes
        )

        order_id = self.db.add_order(order)

        status_symbol = "WON" if args.status == "won" else "LOST"
        print(f"\nOrder created successfully!")
        print(f"  Company: {company_name}")
        print(f"  Opportunity: {opp_title}")
        print(f"  Quote: {quote_number}")
        print(f"  Order ID: {order_id}")
        print(f"  Status: {status_symbol}")
        print(f"  Final Amount: EUR {args.final_amount:,.2f}")


def create_parser():
    """
    Create argument parser

    P.I.P.E. Sales Process Stages:
    1. initial_inquiry - Customer requests information/quotation
    2. qualification - Technical feasibility evaluation
    3. proposal_development - Customized solution design
    4. negotiation - Pricing and technical details finalization
    5. order_confirmation - Contract signed, production scheduled
    6. delivery - Installation, commissioning, training
    """
    parser = argparse.ArgumentParser(
        description="Sales Pipeline Manager - P.I.P.E. Industrial Systems",
        epilog="Track your sales funnel: Lead → Opportunity → Quote → Order"
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add lead command
    add_parser = subparsers.add_parser('add-lead', help='Add a new lead')
    add_parser.add_argument('--name', required=True, help='Lead name')
    add_parser.add_argument('--email', required=True, help='Lead email')
    add_parser.add_argument('--phone', default='', help='Lead phone')
    add_parser.add_argument('--source', default='manual', help='Lead source')
    add_parser.add_argument('--location', default=None, help='Location (Germany, Italy, France, Benelux)')
    add_parser.add_argument('--industry', default=None,
                            help='Industry (automotive, industrial_components, food_beverage, logistics)')
    add_parser.add_argument('--company-size', default=None, help='Company size (small, medium, large)')

    # List leads command
    subparsers.add_parser('list-leads', help='List all leads')

    # Export command
    export_parser = subparsers.add_parser('export', help='Export leads to CSV')
    export_parser.add_argument('--output', default='leads_export.csv', help='Output file')

    # Import command
    import_parser = subparsers.add_parser('import', help='Import leads from CSV')
    import_parser.add_argument('--input', required=True, help='Input CSV file')

    # Analytics command
    analytics_parser = subparsers.add_parser('analytics', help='Show analytics and reports')
    analytics_parser.add_argument('--type', required=True,
                                  choices=['conversion', 'winrate', 'pipeline', 'industry', 'location'],
                                  help='Type of analytics to display')

    # Company search command
    company_parser = subparsers.add_parser('company', help='View all records for a company')
    company_parser.add_argument('name', help='Company name (partial match)')

    # Add opportunity command
    add_opp_parser = subparsers.add_parser('add-opportunity', help='Create opportunity for a lead')
    add_opp_parser.add_argument('--lead-name', required=True, help='Lead/Company name')
    add_opp_parser.add_argument('--title', required=True, help='Opportunity title')
    add_opp_parser.add_argument('--value', type=float, required=True, help='Estimated value')
    add_opp_parser.add_argument('--stage', default='initial_inquiry',
                                help='Stage (initial_inquiry, qualification, proposal_development, negotiation, order_confirmation, delivery)')
    add_opp_parser.add_argument('--probability', type=int, default=0, help='Probability 0-100')
    add_opp_parser.add_argument('--expected-close', help='Expected close date (YYYY-MM-DD)')

    # Add quote command
    add_quote_parser = subparsers.add_parser('add-quote', help='Create quote for opportunity')
    add_quote_parser.add_argument('--opportunity-title', required=True, help='Opportunity title')
    add_quote_parser.add_argument('--quote-number', required=True, help='Quote number (e.g., Q-2025-001)')
    add_quote_parser.add_argument('--amount', type=float, required=True, help='Quoted amount')
    add_quote_parser.add_argument('--valid-until', required=True, help='Valid until date (YYYY-MM-DD)')
    add_quote_parser.add_argument('--terms', default='', help='Payment terms')
    add_quote_parser.add_argument('--status', default='draft', help='Status (draft, sent, accepted, rejected)')

    # Add order command
    add_order_parser = subparsers.add_parser('add-order', help='Create order (close quote)')
    add_order_parser.add_argument('--quote-number', required=True, help='Quote number')
    add_order_parser.add_argument('--status', required=True, choices=['won', 'lost'], help='Order status')
    add_order_parser.add_argument('--final-amount', type=float, required=True, help='Final amount')
    add_order_parser.add_argument('--close-date', required=True, help='Close date (YYYY-MM-DD)')
    add_order_parser.add_argument('--notes', default='', help='Notes')

    return parser