"""
SQLite database management for Sales Pipeline Manager
"""
import sqlite3
from pathlib import Path


class Database:
    """Manages SQLite database operations"""

    def __init__(self, db_path="sales_pipeline.db"):
        """Initialize database connection"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect(self):
        """Connect to database"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON")

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def create_tables(self):
        """Create database tables if they don't exist"""
        self.connect()

        # Create leads table
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS leads
                            (
                                lead_id
                                INTEGER
                                PRIMARY
                                KEY
                                AUTOINCREMENT,
                                name
                                TEXT
                                NOT
                                NULL,
                                email
                                TEXT
                                NOT
                                NULL,
                                phone
                                TEXT,
                                source
                                TEXT,
                                status
                                TEXT
                                DEFAULT
                                'new',
                                location
                                TEXT,
                                industry
                                TEXT,
                                company_size
                                TEXT,
                                created_at
                                TEXT
                                NOT
                                NULL
                            )
                            ''')

        # Create opportunities table
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS opportunities
                            (
                                opp_id
                                INTEGER
                                PRIMARY
                                KEY
                                AUTOINCREMENT,
                                lead_id
                                INTEGER
                                NOT
                                NULL,
                                title
                                TEXT
                                NOT
                                NULL,
                                estimated_value
                                REAL
                                NOT
                                NULL,
                                stage
                                TEXT
                                DEFAULT
                                'initial_inquiry',
                                probability
                                INTEGER
                                DEFAULT
                                0,
                                expected_close
                                TEXT,
                                created_at
                                TEXT
                                NOT
                                NULL,
                                FOREIGN
                                KEY
                            (
                                lead_id
                            ) REFERENCES leads
                            (
                                lead_id
                            )
                                )
                            ''')

        # Create quotes table
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS quotes
                            (
                                quote_id
                                INTEGER
                                PRIMARY
                                KEY
                                AUTOINCREMENT,
                                opp_id
                                INTEGER
                                NOT
                                NULL,
                                quote_number
                                TEXT
                                NOT
                                NULL
                                UNIQUE,
                                quoted_amount
                                REAL
                                NOT
                                NULL,
                                valid_until
                                TEXT,
                                terms
                                TEXT,
                                status
                                TEXT
                                DEFAULT
                                'draft',
                                created_at
                                TEXT
                                NOT
                                NULL,
                                FOREIGN
                                KEY
                            (
                                opp_id
                            ) REFERENCES opportunities
                            (
                                opp_id
                            )
                                )
                            ''')

        # Create orders table
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS orders
                            (
                                order_id
                                INTEGER
                                PRIMARY
                                KEY
                                AUTOINCREMENT,
                                quote_id
                                INTEGER
                                NOT
                                NULL,
                                status
                                TEXT
                                NOT
                                NULL,
                                final_amount
                                REAL
                                NOT
                                NULL,
                                close_date
                                TEXT
                                NOT
                                NULL,
                                notes
                                TEXT,
                                created_at
                                TEXT
                                NOT
                                NULL,
                                FOREIGN
                                KEY
                            (
                                quote_id
                            ) REFERENCES quotes
                            (
                                quote_id
                            )
                                )
                            ''')

        self.conn.commit()
        self.close()

    def add_lead(self, lead):
        """Add a lead to database"""
        self.connect()
        self.cursor.execute('''
                            INSERT INTO leads (name, email, phone, source, status, location, industry, company_size,
                                               created_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (lead.name, lead.email, lead.phone, lead.source,
                                  lead.status, lead.location, lead.industry, lead.company_size, lead.created_at))
        self.conn.commit()
        lead_id = self.cursor.lastrowid
        self.close()
        return lead_id

    def get_all_leads(self):
        """Get all leads from database"""
        self.connect()
        self.cursor.execute('SELECT * FROM leads')
        rows = self.cursor.fetchall()
        self.close()
        return rows

    def add_opportunity(self, opp):
        """Add an opportunity to database"""
        self.connect()
        self.cursor.execute('''
                            INSERT INTO opportunities (lead_id, title, estimated_value, stage,
                                                       probability, expected_close, created_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                            ''', (opp.lead_id, opp.title, opp.estimated_value, opp.stage,
                                  opp.probability, opp.expected_close, opp.created_at))
        self.conn.commit()
        opp_id = self.cursor.lastrowid
        self.close()
        return opp_id

    def get_all_opportunities(self):
        """Get all opportunities from database"""
        self.connect()
        self.cursor.execute('SELECT * FROM opportunities')
        rows = self.cursor.fetchall()
        self.close()
        return rows

    def add_quote(self, quote):
        """Add a quote to database"""
        self.connect()
        self.cursor.execute('''
                            INSERT INTO quotes (opp_id, quote_number, quoted_amount, valid_until, terms, status,
                                                created_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                            ''', (quote.opp_id, quote.quote_number, quote.quoted_amount,
                                  quote.valid_until, quote.terms, quote.status, quote.created_at))
        self.conn.commit()
        quote_id = self.cursor.lastrowid
        self.close()
        return quote_id

    def get_all_quotes(self):
        """Get all quotes from database"""
        self.connect()
        self.cursor.execute('SELECT * FROM quotes')
        rows = self.cursor.fetchall()
        self.close()
        return rows

    def add_order(self, order):
        """Add an order to database"""
        self.connect()
        self.cursor.execute('''
                            INSERT INTO orders (quote_id, status, final_amount, close_date, notes, created_at)
                            VALUES (?, ?, ?, ?, ?, ?)
                            ''', (order.quote_id, order.status, order.final_amount,
                                  order.close_date, order.notes, order.created_at))
        self.conn.commit()
        order_id = self.cursor.lastrowid
        self.close()
        return order_id

    def get_all_orders(self):
        """Get all orders from database"""
        self.connect()
        self.cursor.execute('SELECT * FROM orders')
        rows = self.cursor.fetchall()
        self.close()
        return rows