import requests

def run(shared_data):
    vuln_patterns = {
        "/.env": "Sensitive Config",
        "/config.php.bak": "Backup File",
        "/sql-dump.sql": "Database Leak"
    }
    
    targets = shared_data.get('fingerprinting', {}).keys()
    shared_data.setdefault('vulnerabilities', {})
    
    for target in targets:
        shared_data['vulnerabilities'].setdefault(target, [])
        for path, description in vuln_patterns.items():
            url = f"{target.rstrip('/')}{path}"
            try:
                response = requests.get(url, timeout=3)
                if response.status_code == 200:
                    shared_data['vulnerabilities'][target].append({"url": url, "type": description})
            except:
                continue
