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

        # Create leads table with new fields
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                lead_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                source TEXT,
                status TEXT DEFAULT 'new',
                location TEXT,
                industry TEXT,
                company_size TEXT,
                created_at TEXT NOT NULL
            )
        ''')

        # Create opportunities table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS opportunities (
                opp_id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                value REAL NOT NULL,
                stage TEXT DEFAULT 'prospecting',
                probability INTEGER DEFAULT 0,
                expected_close TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (lead_id) REFERENCES leads(lead_id)
            )
        ''')

        # Create orders table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                opp_id INTEGER NOT NULL,
                status TEXT NOT NULL,
                close_date TEXT NOT NULL,
                notes TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (opp_id) REFERENCES opportunities(opp_id)
            )
        ''')

        self.conn.commit()
        self.close()

    def add_lead(self, lead):
        """Add a lead to database"""
        self.connect()
        self.cursor.execute('''
            INSERT INTO leads (name, email, phone, source, status, location, industry, company_size, created_at)
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
            INSERT INTO opportunities (lead_id, title, value, stage, 
                                      probability, expected_close, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (opp.lead_id, opp.title, opp.value, opp.stage,
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

    def add_order(self, order):
        """Add an order to database"""
        self.connect()
        self.cursor.execute('''
            INSERT INTO orders (opp_id, status, close_date, notes, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (order.opp_id, order.status, order.close_date, order.notes, order.created_at))
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