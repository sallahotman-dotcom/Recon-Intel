import re

def run(shared_data):
    # This module extracts sensitive patterns from identified vulnerabilities
    # Patterns for automated data harvesting
    patterns = {
        "email": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        "api_key": r'AIza[0-9A-Za-z-_]{35}'
    }
    
    shared_data.setdefault('exfiltrated_data', {})
    
    for target, vulnerabilities in shared_data.get('vulnerabilities', {}).items():
        # Scanning target content for potential sensitive data
        print(f"  [!] Scanning for sensitive patterns on: {target}")
        
        # Placeholder for actual request content parsing
        # Example logic:
        # response = shared_data['session'].get(target)
        # matches = re.findall(patterns['email'], response.text)
        
        shared_data['exfiltrated_data'][target] = [
            {"type": "email", "value": "admin@target.com"}
        ]
