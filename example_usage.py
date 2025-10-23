#!/usr/bin/env python3

import sys
from config_manager import ConfigManager

def main():
    # Initialize config manager with relative path
    manager = ConfigManager('.config')
    
    # Check if configuration exists and is valid
    config = manager.load()
    if not config or not manager.is_valid():
        print("Configuration is missing or invalid.")
        print("Please run config_setup.py to configure your settings.")
        print("\nExample commands:")
        print("  ./config_setup.py --interactive")
        print("  ./config_setup.py --user username --password pass123 --server https://example.com")
        sys.exit(1)
    
    # Use the configuration
    print(f"Connected to {config.server} as {config.user}")
    if config.course:
        print(f"Current course: {config.course}")
    if config.assignment:
        print(f"Current assignment: {config.assignment}")

if __name__ == '__main__':
    main()