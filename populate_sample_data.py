"""
Populate database with P.I.P.E. sample data for testing
"""
from salespipe.database import Database
from salespipe.models import Lead, Opportunity, Quote, Order


def populate_database():
    """Add complete sample data to database"""
    db = Database()
    db.create_tables()

    print("Populating database with P.I.P.E. sample data...\n")

    # ===== LEADS =====
    print("Adding leads...")

    leads_data = [
        ("AutoMech GmbH", "contact@automech.de", "+49-30-12345", "trade_show",
         "Germany", "automotive", "large"),
        ("TechComponents SRL", "info@techcomp.it", "+39-02-98765", "referral",
         "Italy", "industrial_components", "medium"),
        ("BeveragePack SA", "sales@bevpack.fr", "+33-1-55443", "linkedin",
         "France", "food_beverage", "large"),
        ("LogiFlow BV", "contact@logiflow.nl", "+31-20-77889", "website",
         "Benelux", "logistics", "medium"),
        ("Precision Auto DE", "info@precisionauto.de", "+49-89-33221", "cold_call",
         "Germany", "automotive", "large"),
        ("FoodTech Italia", "sales@foodtech.it", "+39-06-44556", "referral",
         "Italy", "food_beverage", "medium"),
        ("AutoAssembly FR", "contact@autoassembly.fr", "+33-4-66778", "website",
         "France", "automotive", "medium"),
        ("Industrial Parts BE", "info@indparts.be", "+32-2-99887", "linkedin",
         "Benelux", "industrial_components", "small"),
    ]

    lead_ids = []
    for name, email, phone, source, location, industry, size in leads_data:
        lead = Lead(None, name, email, phone, source, "new", location, industry, size)
        lead_id = db.add_lead(lead)
        lead_ids.append(lead_id)
        print(f"  + Lead {lead_id}: {name}")

    # ===== OPPORTUNITIES =====
    print("\nAdding opportunities...")

    opportunities_data = [
        (lead_ids[0], "Robotic Welding Cell", 150000, "negotiation", 75, "2025-02-28"),
        (lead_ids[1], "CNC Machining Center", 85000, "proposal_development", 60, "2025-03-15"),
        (lead_ids[2], "Automated Packaging Line", 200000, "qualification", 50, "2025-04-30"),
        (lead_ids[3], "Warehouse Robotics System", 120000, "initial_inquiry", 30, "2025-05-15"),
        (lead_ids[4], "Assembly Line Robot", 95000, "negotiation", 70, "2025-02-15"),
    ]

    opp_ids = []
    for lead_id, title, value, stage, prob, close_date in opportunities_data:
        opp = Opportunity(None, lead_id, title, value, stage, prob, close_date)
        opp_id = db.add_opportunity(opp)
        opp_ids.append(opp_id)
        print(f"  + Opportunity {opp_id}: {title} (EUR {value:,})")

    # ===== QUOTES =====
    print("\nAdding quotes...")

    quotes_data = [
        (opp_ids[0], "Q-2024-PIPE-001", 145000, "2025-01-31", "50% upfront, 50% on delivery", "sent"),
        (opp_ids[1], "Q-2024-PIPE-002", 82000, "2025-02-28", "Net 30 days", "sent"),
        (opp_ids[4], "Q-2024-PIPE-003", 92000, "2025-01-15", "Net 45 days", "accepted"),
    ]

    quote_ids = []
    for opp_id, quote_num, amount, valid, terms, status in quotes_data:
        quote = Quote(None, opp_id, quote_num, amount, valid, terms, status)
        quote_id = db.add_quote(quote)
        quote_ids.append(quote_id)
        print(f"  + Quote {quote_id}: {quote_num} (EUR {amount:,})")

    # ===== ORDERS =====
    print("\nAdding orders...")

    orders_data = [
        (quote_ids[0], "won", 142000, "2024-12-20", "Closed with 2% discount. Installation scheduled for March."),
        (quote_ids[1], "lost", 0, "2024-12-21", "Lost to competitor - price too high"),
        (quote_ids[2], "won", 90000, "2024-12-22", "Won! Customer negotiated 2.2% discount. Delivery in February."),
    ]

    for quote_id, status, amount, close_date, notes in orders_data:
        order = Order(None, quote_id, status, amount, close_date, notes)
        order_id = db.add_order(order)
        print(f"  + Order {order_id}: {status.upper()} (EUR {amount:,})")

    print("\n" + "=" * 60)
    print("SUCCESS: Sample data populated!")
    print("=" * 60)
    print(f"\nSummary:")
    print(f"  Leads:         {len(lead_ids)}")
    print(f"  Opportunities: {len(opp_ids)}")
    print(f"  Quotes:        {len(quote_ids)}")
    print(f"  Orders:        {len(orders_data)} (2 won, 1 lost)")
    print(f"\nDatabase ready for testing!")


if __name__ == '__main__':
    populate_database()