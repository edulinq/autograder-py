#!/usr/bin/env python3

import configparser
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, List
from urllib.parse import urlparse

@dataclass
class Config:
    user: str
    password: str
    server: str
    course: Optional[str] = None
    assignment: Optional[str] = None

class ConfigManager:
    def __init__(self, config_dir: str = '.config'):
        self.config_dir = config_dir
        self.config_file = os.path.join(config_dir, 'config.ini')
        os.makedirs(config_dir, exist_ok=True)
    
    def load(self) -> Optional[Config]:
        """Load configuration from file."""
        if not os.path.exists(self.config_file):
            return None
        
        parser = configparser.ConfigParser()
        parser.read(self.config_file)
        
        if 'settings' not in parser:
            return None
        
        settings = parser['settings']
        return Config(
            user=settings.get('user', ''),
            password=settings.get('password', ''),
            server=settings.get('server', ''),
            course=settings.get('course', None),
            assignment=settings.get('assignment', None)
        )
    
    def save(self, config: Config):
        """Save configuration to file."""
        parser = configparser.ConfigParser()
        parser['settings'] = {
            'user': config.user,
            'password': config.password,
            'server': config.server
        }
        if config.course:
            parser['settings']['course'] = config.course
        if config.assignment:
            parser['settings']['assignment'] = config.assignment
        
        with open(self.config_file, 'w') as f:
            parser.write(f)
    
    def validate(self, config: Config) -> List[str]:
        """Validate configuration values."""
        errors = []
        
        if not config.user or not re.match(r'^[a-zA-Z0-9_-]+$', config.user):
            errors.append("Invalid username. Use only letters, numbers, underscores, and hyphens.")
        
        if not config.password or len(config.password) < 6:
            errors.append("Password must be at least 6 characters long.")
        
        try:
            result = urlparse(config.server)
            if not all([result.scheme, result.netloc]):
                raise ValueError()
        except:
            errors.append("Invalid server URL. Must include protocol (http:// or https://)")
        
        return errors
    
    def is_valid(self) -> bool:
        """Check if current configuration is valid."""
        config = self.load()
        if not config:
            return False
        return len(self.validate(config)) == 0