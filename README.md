# Sales Pipeline Manager

A command-line sales pipeline management system for P.I.P.E. Industrial Systems, designed to track B2B sales from initial lead through final order.

## Project Overview

**SalesPipe** is a Python-based CRM system built for P.I.P.E. Industrial Systems, a B2B company specializing in industrial machinery and automation solutions across Europe.

### Business Context

P.I.P.E. operates in four key markets:
- Germany (main market)
- Italy (strategic expansion)
- France (growing presence)
- Benelux (Belgium, Netherlands, Luxembourg - emerging market)

### Target Industries

- **Automotive** - Assembly lines, robotic welding
- **Industrial Components** - CNC machining, precision parts
- **Food & Beverage** - Packaging, filling, labeling
- **Logistics** - Warehouse automation, material handling

### Sales Funnel

The system tracks a complete 4-stage sales pipeline:

```
LEAD → OPPORTUNITY → QUOTE → ORDER
```

1. **Lead**: Initial contact or inquiry from potential customer
2. **Opportunity**: Qualified prospect with specific project requirements
3. **Quote**: Formal price proposal with detailed specifications
4. **Order**: Closed deal (won or lost)

## Features

- Complete CRM workflow tracking leads through entire sales cycle
- Company search functionality to view full sales history
- Interactive commands to qualify leads, create quotes, and close orders
- Advanced analytics including conversion rates, win rates, and pipeline value
- Industry and location performance analysis
- CSV import/export for bulk data operations
- SQLite database with persistent storage and foreign key relationships
- Comprehensive automated testing suite with 19+ unit tests

## Requirements

- Python 3.12 or higher
- No external dependencies (uses only Python standard library)

## Installation

### Clone the repository

```bash
git clone https://github.com/ChiosaGiorgia/sales-pipeline-manager.git
cd sales-pipeline-manager
```

### Run the application

```bash
python main.py --help
```

### Populate with sample data (optional)

```bash
python populate_sample_data.py
```

This creates a demonstration dataset with:
- 8 leads across all industries and locations
- 5 opportunities at various stages
- 3 quotes with different statuses
- 3 orders (2 won, 1 lost)

## Why This Project?

### Academic Context

This project was developed as the final assignment for the **Lab of Software Development** course at Ca' Foscari University of Venice (Academic Year 2024-2025). The assignment required building a complete software application that demonstrates:

- Professional software development practices
- Version control with Git and GitHub (branches, issues, pull requests)
- Collaborative development workflow
- Database design and implementation
- Command-line interface design
- Automated testing
- Professional documentation

### Real-World Problem

The project addresses a genuine business challenge faced by **P.I.P.E. Industrial Systems**, a B2B machinery company. Sales teams needed a tool to:

- Track complex sales cycles with multiple stakeholders
- Monitor pipeline value and forecast revenue
- Analyze performance across different industries and geographic markets
- Maintain complete sales history for each customer
- Calculate conversion rates at each funnel stage

Traditional spreadsheets were inadequate for managing the relationships between leads, opportunities, quotes, and orders. This system provides a structured, database-backed solution with built-in analytics.

### Learning Objectives Achieved

Through this project, we gained hands-on experience with:

- **Python standard library**: Building a complete application without external dependencies
- **Database design**: Implementing normalized tables with foreign key relationships
- **CLI design**: Creating intuitive command-line interfaces with argparse
- **Testing**: Writing comprehensive unit tests for data models, database operations, and business logic
- **Git workflow**: Managing branches, resolving conflicts, creating pull requests
- **Team collaboration**: Dividing work across team members with different skill levels
- **Documentation**: Writing professional README files and code documentation

## Quick Start Tutorial

This 5-minute tutorial will walk you through the complete sales cycle using real commands you can copy and paste.

### Step 1: Set Up the System

First, populate the database with sample data:

```bash
python populate_sample_data.py
```

You should see:
```
Populating database with P.I.P.E. sample data...
Adding leads...
  + Lead 1: AutoMech GmbH
  + Lead 2: TechComponents SRL
  ...
Database populated successfully!
```

### Step 2: Explore Existing Data

View all leads in the system:

```bash
python main.py list-leads
```

Search for a specific company to see its complete sales history:

```bash
python main.py company "AutoMech"
```

You'll see the full hierarchy: Lead → Opportunities → Quotes → Orders

### Step 3: Add Your First Lead

Add a new potential customer:

```powershell
python main.py add-lead `
  --name "TestCompany GmbH" `
  --email "contact@testcompany.de" `
  --phone "+49-30-99999" `
  --location "Germany" `
  --industry "automotive" `
  --company-size "medium"
```

Verify it was added:

```bash
python main.py list-leads
```

### Step 4: Qualify the Lead

Convert your lead into a sales opportunity:

```powershell
python main.py add-opportunity `
  --lead-name "TestCompany" `
  --title "Industrial Robot Project" `
  --value 125000 `
  --stage "initial_inquiry" `
  --probability 40
```

Check the company record again:

```bash
python main.py company "TestCompany"
```

You should now see the opportunity linked to the lead!

### Step 5: Create a Quote

Generate a formal quote for the opportunity:

```powershell
python main.py add-quote `
  --opportunity-title "Industrial Robot" `
  --quote-number "Q-2025-TEST-001" `
  --amount 120000 `
  --valid-until "2025-02-28" `
  --terms "40% upfront, 60% on delivery" `
  --status "sent"
```

### Step 6: Close the Deal

Win the order:

```powershell
python main.py add-order `
  --quote-number "Q-2025-TEST-001" `
  --status won `
  --final-amount 118000 `
  --close-date "2025-01-06" `
  --notes "Closed with 1.7% discount"
```

### Step 7: View Analytics

See how your new deal affected the metrics:

```bash
# Overall conversion rates
python main.py analytics --type conversion

# Pipeline value
python main.py analytics --type pipeline

# Performance by industry
python main.py analytics --type industry

# Performance by location
python main.py analytics --type location
```

Congratulations! You've completed a full sales cycle from lead to closed order.

## Try It Yourself: Interactive Examples

Here are some practical scenarios you can try right now. Each example is self-contained and demonstrates a different feature.

### Example 1: Import Multiple Leads from CSV

**Step 1:** Create a file called `my_leads.csv` in the **same folder** where `main.py` is located (the project root directory).

**File location:**
```
sales-pipeline-manager/
├── main.py
├── my_leads.csv          ← Create the file HERE
├── data/
└── salespipe/
```

**Step 2:** Add this content to `my_leads.csv`:

```csv
name,email,phone,source,status,location,industry,company_size
NewCo Italia,info@newco.it,+39-02-12345,trade_show,new,Italy,industrial_components,large
FrenchAuto SA,contact@frenchauto.fr,+33-1-67890,website,contacted,France,automotive,medium
```

**Important notes:**
- Save the file in the **project root directory** (same folder as `main.py`)
- Use **UTF-8 encoding** when saving
- Do NOT add extra spaces before or after commas
- The first line MUST be the header row exactly as shown

**Step 3:** Import the file:

```bash
python main.py import --input my_leads.csv
```

You should see:
```
✓ Imported 2 leads to database
```

**Step 4:** Verify it worked:

```bash
python main.py list-leads
```

**Alternative:** Place the file in the `data/` folder and import with full path:

```bash
python main.py import --input data/my_leads.csv
```

### Example 2: Track a Lost Deal

Sometimes deals don't work out. Here's how to track them:

```powershell
# Add lead
python main.py add-lead `
  --name "LostDeal Corp" `
  --email "sales@lostdeal.com" `
  --industry "logistics" `
  --location "Benelux"

# Create opportunity
python main.py add-opportunity `
  --lead-name "LostDeal" `
  --title "Warehouse System" `
  --value 200000

# Send quote
python main.py add-quote `
  --opportunity-title "Warehouse System" `
  --quote-number "Q-2025-LOST-001" `
  --amount 195000 `
  --valid-until "2025-03-31"

# Mark as lost
python main.py add-order `
  --quote-number "Q-2025-LOST-001" `
  --status lost `
  --final-amount 0 `
  --close-date "2025-01-06" `
  --notes "Lost to competitor - price too high"

# Check win rate (should decrease)
python main.py analytics --type winrate
```

### Example 3: Analyze Industry Performance

Add several leads across different industries, then compare:

```powershell
# Add automotive lead
python main.py add-lead `
  --name "Auto Parts GmbH" `
  --email "info@autoparts.de" `
  --industry "automotive" `
  --location "Germany"

# Add food & beverage lead
python main.py add-lead `
  --name "Food Pack SRL" `
  --email "sales@foodpack.it" `
  --industry "food_beverage" `
  --location "Italy"

# Add logistics lead
python main.py add-lead `
  --name "Logistics Pro BV" `
  --email "contact@logipro.nl" `
  --industry "logistics" `
  --location "Benelux"

# Compare performance
python main.py analytics --type industry
python main.py analytics --type location
```

### Example 4: Export Data for External Analysis

Export all leads to analyze in Excel or another tool:

```bash
python main.py export --output all_leads_backup.csv
```

The exported CSV will contain all lead information and can be re-imported later.

### Example 5: Complete Multi-Stage Deal

Follow a realistic sales process from start to finish:

```powershell
# Week 1: Trade show contact
python main.py add-lead `
  --name "Manufacturing Excellence SRL" `
  --email "purchasing@mfgexcel.it" `
  --phone "+39-06-777888" `
  --source "trade_show" `
  --location "Italy" `
  --industry "industrial_components" `
  --company-size "large"

# Week 2: Discovery meeting - Opportunity
python main.py add-opportunity `
  --lead-name "Manufacturing Excellence" `
  --title "CNC Machining Center Upgrade" `
  --value 250000 `
  --stage "qualification" `
  --probability 50 `
  --expected-close "2025-04-30"

# Week 6: Quote sent
python main.py add-quote `
  --opportunity-title "CNC Machining" `
  --quote-number "Q-2025-MFG-001" `
  --amount 245000 `
  --valid-until "2025-03-31" `
  --terms "30% down payment, 70% on installation" `
  --status "sent"

# Week 8: Negotiation complete - WON
python main.py add-order `
  --quote-number "Q-2025-MFG-001" `
  --status won `
  --final-amount 238000 `
  --close-date "2025-01-06" `
  --notes "Final price after 2.9% discount for volume commitment"

# View complete deal history
python main.py company "Manufacturing Excellence"

# Check updated metrics
python main.py analytics --type conversion
python main.py analytics --type pipeline
```

### Example 6: Find All Deals for a Company

If you're not sure of the exact company name:

```bash
# Partial search works
python main.py company "Auto"

# This will show ALL companies with "Auto" in the name:
# - AutoMech GmbH
# - AutoAssembly FR
# - Precision Auto DE
# - Auto Parts GmbH
```

## Common Commands Reference

Here's a quick reference of the most-used commands:

```bash
# Daily operations
python main.py list-leads                          # See all leads
python main.py company "CompanyName"               # Search company
python main.py add-lead --name "..." --email "..." # Add new lead

# Sales progression
python main.py add-opportunity --lead-name "..." --title "..." --value 100000
python main.py add-quote --opportunity-title "..." --quote-number "..." --amount 95000
python main.py add-order --quote-number "..." --status won --final-amount 93000

# Analytics (run weekly/monthly)
python main.py analytics --type conversion         # Funnel health
python main.py analytics --type winrate           # Closing effectiveness
python main.py analytics --type pipeline          # Revenue forecast
python main.py analytics --type industry          # Best-performing sectors
python main.py analytics --type location          # Geographic performance

# Data management
python main.py import --input file.csv            # Bulk import
python main.py export --output backup.csv         # Backup/export
python populate_sample_data.py                     # Reset to demo data
```

## Usage Guide

### Basic Commands

#### Add a Lead

```powershell
python main.py add-lead `
  --name "AutoMech GmbH" `
  --email "contact@automech.de" `
  --phone "+49-30-12345" `
  --location "Germany" `
  --industry "automotive" `
  --company-size "large"
```

**Parameters:**
- `--name` (required): Company name
- `--email` (required): Contact email
- `--phone`: Contact phone number
- `--source`: Lead source (default: manual)
- `--location`: Geographic location (Germany, Italy, France, Benelux)
- `--industry`: Industry sector (automotive, industrial_components, food_beverage, logistics)
- `--company-size`: Company size (small, medium, large)

#### List All Leads

```bash
python main.py list-leads
```

Displays all leads in tabular format with ID, name, email, status, industry, and location.

#### Search for a Company

View complete sales history including all leads, opportunities, quotes, and orders:

```bash
python main.py company "AutoMech"
```

The system performs partial name matching and displays the full relationship hierarchy for matching companies.

Example output:
```
======================================================================
COMPANY: AutoMech GmbH
======================================================================

LEAD INFO:
  ID: 1
  Email: contact@automech.de
  Status: qualified
  Location: Germany
  Industry: automotive

OPPORTUNITIES:
  [1] Robotic Welding Cell - EUR 150,000.00 (negotiation)
      QUOTES:
        [1] Q-2024-PIPE-001 - EUR 145,000.00 (sent)
            ORDERS:
              [1] WON - EUR 142,000.00
```

### Sales Workflow Commands

#### Qualify Lead to Opportunity

Convert a qualified lead into a sales opportunity:

```powershell
python main.py add-opportunity `
  --lead-name "AutoMech" `
  --title "Robotic Welding Cell" `
  --value 150000 `
  --stage "negotiation" `
  --probability 75 `
  --expected-close "2025-03-31"
```

**Parameters:**
- `--lead-name` (required): Company name (partial match supported)
- `--title` (required): Opportunity title
- `--value` (required): Estimated deal value in EUR
- `--stage`: Current stage (default: initial_inquiry)
- `--probability`: Win probability 0-100 (default: 0)
- `--expected-close`: Expected close date (YYYY-MM-DD format)

**Valid stages:**
- `initial_inquiry` - Customer requests information/quotation
- `qualification` - Technical feasibility evaluation
- `proposal_development` - Customized solution design
- `negotiation` - Pricing and technical details finalization
- `order_confirmation` - Contract signed, production scheduled
- `delivery` - Installation, commissioning, and training

#### Create Quote for Opportunity

Generate a formal quote for an existing opportunity:

```powershell
python main.py add-quote `
  --opportunity-title "Robotic Welding" `
  --quote-number "Q-2025-001" `
  --amount 145000 `
  --valid-until "2025-03-31" `
  --terms "50% upfront, 50% on delivery" `
  --status "sent"
```

**Parameters:**
- `--opportunity-title` (required): Opportunity title (partial match)
- `--quote-number` (required): Unique quote identifier
- `--amount` (required): Quoted amount in EUR
- `--valid-until` (required): Quote expiration date (YYYY-MM-DD)
- `--terms`: Payment terms (default: empty)
- `--status`: Quote status (default: draft)

**Valid statuses:** draft, sent, accepted, rejected

#### Close Quote as Order

Close a quote as either a won or lost order:

```powershell
# Won deal
python main.py add-order `
  --quote-number "Q-2025-001" `
  --status won `
  --final-amount 142000 `
  --close-date "2025-01-05" `
  --notes "Closed with 2% discount for early payment"

# Lost deal
python main.py add-order `
  --quote-number "Q-2025-002" `
  --status lost `
  --final-amount 0 `
  --close-date "2025-01-05" `
  --notes "Lost to competitor on price"
```

**Parameters:**
- `--quote-number` (required): Quote number (partial match)
- `--status` (required): Order outcome (won or lost)
- `--final-amount` (required): Final deal amount in EUR
- `--close-date` (required): Close date (YYYY-MM-DD)
- `--notes`: Additional notes (default: empty)

### Data Management

#### Import Leads from CSV

Import multiple leads from a CSV file:

```bash
python main.py import --input data/sample_leads.csv
```

**CSV format requirements:**
```csv
name,email,phone,source,status,location,industry,company_size
Company Name,email@example.com,+1234567,website,new,Germany,automotive,large
```

**Important:**
- All fields are required
- The CSV must include a header row (first line)
- File must be in UTF-8 encoding
- No extra spaces before or after commas
- Valid values for `location`: Germany, Italy, France, Benelux
- Valid values for `industry`: automotive, industrial_components, food_beverage, logistics
- Valid values for `company_size`: small, medium, large
- Valid values for `status`: new, contacted, qualified, converted, lost

**File location options:**

1. **Project root** (same folder as main.py):
   ```bash
   python main.py import --input my_leads.csv
   ```

2. **data/ folder** (recommended):
   ```bash
   python main.py import --input data/my_leads.csv
   ```

3. **Full path** (any location):
   ```bash
   python main.py import --input C:\Users\YourName\Documents\leads.csv
   ```

**Troubleshooting:**
- If you get "File not found", check the file is in the correct location
- Use `ls` (Mac/Linux) or `dir` (Windows) to see files in current directory
- Make sure you're running the command from the project root directory

#### Export Leads to CSV

Export all leads to a CSV file:

```bash
python main.py export --output my_leads.csv
```

The exported file will contain all lead information in the same format as the import template.

### Analytics & Reports

#### Conversion Rates

Analyze funnel performance across all stages:

```bash
python main.py analytics --type conversion
```

Output includes:
- Total counts at each funnel stage (leads, opportunities, quotes, orders)
- Conversion rates between consecutive stages
- Overall conversion rate from lead to won order
- Order win rate (won/total orders)

Example output:
```
=== CONVERSION RATES ===

Funnel Overview:
  Total Leads:         8
  Total Opportunities: 5
  Total Quotes:        3
  Total Orders:        3
  Won Orders:          2

Conversion Rates:
  Lead → Opportunity:   62.5%
  Opportunity → Quote:  60.0%
  Quote → Order:        100.0%
  Order Win Rate:       66.7%
  Overall (Lead → Won): 25.0%
```

#### Win Rate

Calculate the percentage of closed deals that were won:

```bash
python main.py analytics --type winrate
```

#### Pipeline Value

Display the total value of open opportunities and quotes:

```bash
python main.py analytics --type pipeline
```

Output includes:
- Total value of all open opportunities
- Total value of all pending quotes
- Combined pipeline value
- Total won revenue
- Total closed value (won + lost)

Example output:
```
=== PIPELINE VALUE ===
  Opportunities Value: EUR 555,000.00
  Quotes Value:        EUR 315,000.00
  Total Pipeline:      EUR 870,000.00

  Won Value:           EUR 284,000.00
  Total Closed:        EUR 284,000.00
```

#### Performance by Industry

Analyze sales performance segmented by industry:

```bash
python main.py analytics --type industry
```

Shows lead count, won orders, win rate, and average deal value for each industry sector.

#### Performance by Location

Analyze sales performance segmented by geographic location:

```bash
python main.py analytics --type location
```

Shows lead count, won orders, win rate, and total pipeline value for each market location.

## Database Schema

The system uses SQLite with four normalized tables implementing proper foreign key relationships.

### Table: leads

Primary table for initial customer contacts.

**Columns:**
- `lead_id` INTEGER PRIMARY KEY AUTOINCREMENT
- `name` TEXT NOT NULL
- `email` TEXT NOT NULL
- `phone` TEXT
- `source` TEXT
- `status` TEXT
- `location` TEXT
- `industry` TEXT
- `company_size` TEXT
- `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP

### Table: opportunities

Sales opportunities linked to qualified leads.

**Columns:**
- `opp_id` INTEGER PRIMARY KEY AUTOINCREMENT
- `lead_id` INTEGER NOT NULL (FOREIGN KEY → leads.lead_id)
- `title` TEXT NOT NULL
- `estimated_value` REAL
- `stage` TEXT
- `probability` INTEGER
- `expected_close` TEXT
- `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP

### Table: quotes

Formal price proposals linked to opportunities.

**Columns:**
- `quote_id` INTEGER PRIMARY KEY AUTOINCREMENT
- `opp_id` INTEGER NOT NULL (FOREIGN KEY → opportunities.opp_id)
- `quote_number` TEXT UNIQUE NOT NULL
- `quoted_amount` REAL NOT NULL
- `valid_until` TEXT
- `terms` TEXT
- `status` TEXT
- `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP

### Table: orders

Closed deals (won or lost) linked to quotes.

**Columns:**
- `order_id` INTEGER PRIMARY KEY AUTOINCREMENT
- `quote_id` INTEGER NOT NULL (FOREIGN KEY → quotes.quote_id)
- `status` TEXT NOT NULL
- `final_amount` REAL NOT NULL
- `close_date` TEXT
- `notes` TEXT
- `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP

## Testing

Run the complete test suite using Python's unittest module:

```bash
# Run all tests
python -m unittest discover tests/

# Run specific test file
python -m unittest tests.test_models
python -m unittest tests.test_analytics
python -m unittest tests.test_csv_handler
```

**Test coverage includes:**
- Data model validation (Lead, Opportunity, Quote, Order)
- Database CRUD operations
- Foreign key constraint enforcement
- CSV import/export with all field types
- Analytics calculations (conversion rates, win rates, pipeline values)
- Performance analysis by industry and location
- Edge cases (empty database, zero division, missing data)

The test suite includes 19+ unit tests ensuring system reliability and data integrity.

## Project Structure

```
sales-pipeline-manager/
├── data/
│   └── sample_leads.csv          # Sample data for import
├── docs/
│   └── Lab_of_Software_Project_Development.pdf
├── salespipe/
│   ├── __init__.py
│   ├── models.py                 # Data models (Lead, Opportunity, Quote, Order)
│   ├── database.py               # SQLite operations and queries
│   ├── csv_handler.py            # CSV import/export functionality
│   ├── analytics.py              # Analytics and reporting logic
│   └── cli.py                    # Command-line interface
├── tests/
│   ├── test_models.py            # Model validation tests
│   ├── test_analytics.py         # Analytics calculation tests
│   └── test_csv_handler.py       # CSV operations tests
├── main.py                       # Application entry point
├── populate_sample_data.py       # Sample data generator script
├── README.md                     # This file
├── LICENSE                       # MIT License
└── .gitignore                    # Git ignore rules
```

## Complete Workflow Example

A typical sales cycle from initial contact to closed deal:

```powershell
# Step 1: Add initial lead from trade show contact
python main.py add-lead `
  --name "NewPlant GmbH" `
  --email "contact@newplant.de" `
  --phone "+49-711-12345" `
  --location "Germany" `
  --industry "automotive" `
  --company-size "large"

# Step 2: Qualify lead to opportunity after discovery meeting
python main.py add-opportunity `
  --lead-name "NewPlant" `
  --title "Assembly Line Robot" `
  --value 180000 `
  --stage "proposal_development" `
  --probability 60 `
  --expected-close "2025-04-30"

# Step 3: Send formal quote after technical specifications finalized
python main.py add-quote `
  --opportunity-title "Assembly Line" `
  --quote-number "Q-2025-015" `
  --amount 175000 `
  --valid-until "2025-04-30" `
  --terms "50% upfront, 50% on delivery" `
  --status "sent"

# Step 4: Close the deal after successful negotiation
python main.py add-order `
  --quote-number "Q-2025-015" `
  --status won `
  --final-amount 172000 `
  --close-date "2025-01-20" `
  --notes "Negotiated 1.7% discount for early payment commitment"

# Step 5: View complete sales history for the company
python main.py company "NewPlant"

# Step 6: Review updated analytics
python main.py analytics --type conversion
python main.py analytics --type pipeline
python main.py analytics --type industry
```

## Frequently Asked Questions

### How do I start with an empty database?

The database is created automatically when you run any command for the first time. Simply execute:

```bash
python main.py add-lead --name "First Lead" --email "test@example.com"
```

### How do I reset the database?

Delete the database file and re-populate with sample data:

```bash
rm sales_pipeline.db
python populate_sample_data.py
```

On Windows PowerShell:
```powershell
Remove-Item sales_pipeline.db
python populate_sample_data.py
```

### Can I import existing data?

Yes. Format your data as a CSV file matching the schema in `data/sample_leads.csv`, then import:

```bash
python main.py import --input your_data.csv
```

Ensure all required fields are present: name, email, phone, source, status, location, industry, company_size.

### What happens if I try to add an opportunity for a non-existent lead?

The system performs a partial name search. If no matching lead is found, an error message is displayed:

```
Error: No lead found matching 'CompanyName'
```

You must add the lead first before creating opportunities.

### How do partial name matches work?

All search commands (company, add-opportunity, add-quote, add-order) use SQL LIKE queries with wildcards. This means:
- "Auto" matches "AutoMech GmbH", "AutoAssembly FR", "Precision Auto DE"
- Searches are case-insensitive
- The system displays all matches if multiple companies match the search term

### Can I modify existing records?

The current version supports creating and querying records. To modify a record, you would need to use SQL commands directly on the `sales_pipeline.db` file, or delete and recreate the record.

### Why do I get "File not found" when importing CSV?

The file must be in the correct location relative to where you run the command.

**Check your current location:**
```powershell
# Windows PowerShell
pwd

# Mac/Linux
pwd
```

You should be in the project root directory (where `main.py` is located).

**Option 1:** Place the CSV file in the **same directory as main.py**:
```
sales-pipeline-manager/
├── main.py
├── my_leads.csv          ← Put file here
└── ...
```

Then import:
```bash
python main.py import --input my_leads.csv
```

**Option 2:** Place the CSV in the **data/ folder**:
```
sales-pipeline-manager/
├── main.py
├── data/
│   └── my_leads.csv      ← Put file here
└── ...
```

Then import:
```bash
python main.py import --input data/my_leads.csv
```

**Option 3:** Use the **full file path**:
```bash
python main.py import --input "C:\Users\YourName\Documents\my_leads.csv"
```

**How to check if the file exists:**
```powershell
# Windows PowerShell
dir my_leads.csv
dir data\my_leads.csv

# Mac/Linux
ls my_leads.csv
ls data/my_leads.csv
```

### Why do commands with multiple lines fail in PowerShell?

Windows PowerShell uses backtick (`` ` ``) instead of backslash (`\`) for line continuation.

**Incorrect (Linux/Mac bash format):**
```bash
python main.py add-lead \
  --name "Company"
```

**Correct (PowerShell format):**
```powershell
python main.py add-lead `
  --name "Company"
```

**Alternative (Single line - works everywhere):**
```bash
python main.py add-lead --name "Company" --email "test@example.com"
```

All commands in this README use the PowerShell backtick format for Windows compatibility.

### How do I contribute to this project?

1. Fork the repository on GitHub
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit: `git commit -m "Add feature description"`
4. Push to your fork: `git push origin feature/your-feature-name`
5. Open a Pull Request with a clear description of your changes

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for complete details.

## Development Team

- **Giorgia Chiosa** - Project Lead & Core Development
- **Marta** - Data Management & Documentation
- **Nicola** - Business Context & Quality Assurance

## References

- P.I.P.E. Industrial Systems Business Context: `docs/Lab_of_Software_Project_Development.pdf`
- GitHub Repository: https://github.com/ChiosaGiorgia/sales-pipeline-manager
- Python Standard Library Documentation: https://docs.python.org/3/library/

## Academic Context
--

This project was developed as part of the Lab of Software Development course requirements at Ca' Foscari University of Venice. It demonstrates practical application of:
- Software development methodologies
- Version control with Git and GitHub
- Database design and normalization
- Command-line interface design
- Automated testing practices
- Professional documentation standards

**Course**: Lab of Software Development  
**Institution**: Ca' Foscari University of Venice  
**Academic Year**: 2024-2025
