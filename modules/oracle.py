import json

def run(shared_data):
    print("  -> Initializing The Oracle: Analyzing vulnerabilities...")
    
    # Simple mapping of technologies to potential CVEs (Knowledge Base)
    cve_db = {
        "PHP/7.4.0": {"cve": "CVE-2021-21703", "severity": "CRITICAL", "remediation": "Upgrade to 7.4.11+"},
        "Nginx/1.18.0": {"cve": "CVE-2022-41741", "severity": "HIGH", "remediation": "Update Nginx configuration"},
        "WordPress/5.8": {"cve": "CVE-2023-2745", "severity": "MEDIUM", "remediation": "Patch WordPress core"}
    }
    
    for target, info in shared_data.get('fingerprinting', {}).items():
        tech = info.get('tech', 'Unknown')
        
        # Cross-referencing found tech with the CVE database
        if tech in cve_db:
            data = cve_db[tech]
            shared_data['vulnerabilities'].setdefault(target, []).append({
                "type": f"Known CVE: {data['cve']}",
                "risk": data['severity'],
                "advice": data['remediation']
            })
            print(f"  [!] Oracle Alert: {target} is vulnerable to {data['cve']}")
