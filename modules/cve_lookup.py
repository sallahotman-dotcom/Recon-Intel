import requests

def run(shared_data):
    print("  -> Searching for known CVEs for detected technologies...")
    
    for target, info in shared_data.get('fingerprinting', {}).items():
        tech_stack = info.get('tech_stack', {})
        
        shared_data.setdefault('vulnerabilities', {}).setdefault(target, [])
        
        # Check for vulnerable technology patterns
        if "PHP" in str(tech_stack):
            shared_data['vulnerabilities'][target].append({
                "url": target,
                "type": "Outdated Software Detected",
                "risk": "MEDIUM",
                "advice": "Verify if the server version is patched against recent CVEs."
            })

