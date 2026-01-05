#!/usr/bin/env python3
"""
Sales Pipeline Manager - Main Entry Point
"""
import sys
from salespipe.cli import CLI, create_parser


def main():
    """Main entry point for the application"""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    cli = CLI()

    # Route commands to appropriate handlers
    if args.command == 'add-lead':
        cli.add_lead(args)
    elif args.command == 'list-leads':
        cli.list_leads(args)
    elif args.command == 'export':
        cli.export_leads(args)
    elif args.command == 'import':
        cli.import_leads(args)
    elif args.command == 'analytics':
        cli.show_analytics(args)
    elif args.command == 'company':
        cli.show_company(args)
    elif args.command == 'add-opportunity':
        cli.add_opportunity_cmd(args)
    elif args.command == 'add-quote':
        cli.add_quote_cmd(args)
    elif args.command == 'add-order':
        cli.add_order_cmd(args)
    else:
        print(f"Unknown command: {args.command}")
        parser.print_help()


if __name__ == '__main__':
    main()