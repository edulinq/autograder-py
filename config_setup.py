#!/usr/bin/env python3

import argparse
import sys
from config_manager import ConfigManager, Config

def setup_interactive(manager: ConfigManager):
    """Run interactive configuration setup."""
    print("Configuration Setup")
    print("-" * 30)
    
    while True:
        config = Config(
            user=input("Username: ").strip(),
            password=input("Password: ").strip(),
            server=input("Server URL: ").strip()
        )
        
        course = input("Course (optional, press Enter to skip): ").strip()
        if course:
            config.course = course
        
        assignment = input("Assignment (optional, press Enter to skip): ").strip()
        if assignment:
            config.assignment = assignment
        
        errors = manager.validate(config)
        if not errors:
            break
        
        print("\nConfiguration errors:")
        for error in errors:
            print(f"- {error}")
        print()
    
    manager.save(config)
    print("\nConfiguration saved successfully!")
    show_config(manager)

def update_setting(manager: ConfigManager, setting: str, value: str):
    """Update a single configuration setting."""
    config = manager.load() or Config(user='', password='', server='')
    setattr(config, setting, value)
    
    errors = manager.validate(config)
    if errors:
        print("Validation errors:")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)
    
    manager.save(config)
    masked = '*' * len(value) if setting == 'password' else value
    print(f"Updated {setting} = {masked}")

def show_config(manager: ConfigManager):
    """Display current configuration."""
    config = manager.load()
    if not config:
        print("No configuration found.")
        return
    
    print("\nCurrent Configuration:")
    print("-" * 30)
    print(f"User: {config.user}")
    print(f"Password: {'*' * len(config.password)}")
    print(f"Server: {config.server}")
    if config.course:
        print(f"Course: {config.course}")
    if config.assignment:
        print(f"Assignment: {config.assignment}")

def main():
    parser = argparse.ArgumentParser(description='Configuration Setup')
    parser.add_argument('--config-dir', default='.config',
                      help='Configuration directory (default: .config)')
    parser.add_argument('--interactive', action='store_true',
                      help='Run interactive setup')
    parser.add_argument('--user', help='Set username')
    parser.add_argument('--password', help='Set password')
    parser.add_argument('--server', help='Set server URL')
    parser.add_argument('--course', help='Set course')
    parser.add_argument('--assignment', help='Set assignment')
    parser.add_argument('--show', action='store_true',
                      help='Show current configuration')
    
    args = parser.parse_args()
    manager = ConfigManager(args.config_dir)
    
    if args.interactive:
        setup_interactive(manager)
    elif args.show:
        show_config(manager)
    elif any([args.user, args.password, args.server, args.course, args.assignment]):
        if args.user:
            update_setting(manager, 'user', args.user)
        if args.password:
            update_setting(manager, 'password', args.password)
        if args.server:
            update_setting(manager, 'server', args.server)
        if args.course:
            update_setting(manager, 'course', args.course)
        if args.assignment:
            update_setting(manager, 'assignment', args.assignment)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()