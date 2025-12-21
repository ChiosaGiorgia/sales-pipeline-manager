"""
Command Line Interface for Sales Pipeline Manager
"""
import argparse
from salespipe.database import Database
from salespipe.models import Lead, Opportunity
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
            print(f"{lead[0]:<5} {lead[1]:<20} {lead[2]:<30} {lead[5]:<15} {lead[7] or 'N/A':<20} {lead[6] or 'N/A':<15}")
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
    add_parser.add_argument('--industry', default=None, help='Industry (automotive, industrial_components, food_beverage, logistics)')
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

    return parser