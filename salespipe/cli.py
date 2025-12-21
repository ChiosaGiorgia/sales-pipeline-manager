"""
Command Line Interface for Sales Pipeline Manager
"""
import argparse
from salespipe.database import Database
from salespipe.models import Lead, Opportunity
from salespipe.csv_handler import CSVHandler


class CLI:
    """Command Line Interface handler"""

    def __init__(self):
        self.db = Database()
        self.db.create_tables()

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

        print(f"\n{'ID':<5} {'Name':<20} {'Email':<30} {'Status':<15} {'Industry':<15}")
        print("-" * 90)
        for lead in leads:
            print(f"{lead[0]:<5} {lead[1]:<20} {lead[2]:<30} {lead[5]:<15} {lead[7] or 'N/A':<15}")
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


def create_parser():
    """Create argument parser"""
    parser = argparse.ArgumentParser(
        description="Sales Pipeline Manager - Manage your sales leads and opportunities"
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add lead command
    add_parser = subparsers.add_parser('add-lead', help='Add a new lead')
    add_parser.add_argument('--name', required=True, help='Lead name')
    add_parser.add_argument('--email', required=True, help='Lead email')
    add_parser.add_argument('--phone', default='', help='Lead phone')
    add_parser.add_argument('--source', default='manual', help='Lead source')
    add_parser.add_argument('--location', default=None, help='Lead location (city, country)')
    add_parser.add_argument('--industry', default=None, help='Lead industry (tech, finance, etc.)')
    add_parser.add_argument('--company-size', default=None, help='Company size (small, medium, large)')

    # List leads command
    subparsers.add_parser('list-leads', help='List all leads')

    # Export command
    export_parser = subparsers.add_parser('export', help='Export leads to CSV')
    export_parser.add_argument('--output', default='leads_export.csv', help='Output file')

    # Import command
    import_parser = subparsers.add_parser('import', help='Import leads from CSV')
    import_parser.add_argument('--input', required=True, help='Input CSV file')

    return parser