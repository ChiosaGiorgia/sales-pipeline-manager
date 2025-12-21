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

    # If no command is provided, show help
    if not args.command:
        parser.print_help()
        return

    # Create CLI instance
    cli = CLI()

    # Execute the appropriate command
    if args.command == 'add-lead':
        cli.add_lead(args)
    elif args.command == 'list-leads':
        cli.list_leads(args)
    elif args.command == 'export':
        cli.export_leads(args)
    elif args.command == 'import':
        cli.import_leads(args)
    else:
        print(f"Unknown command: {args.command}")
        parser.print_help()


if __name__ == "__main__":
    main()