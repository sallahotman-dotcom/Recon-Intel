import requests

def run(shared_data):
    # Payloads represent common attack vectors
    attack_vectors = {
        "/.env": "Info Disclosure",
        "/admin/config.php": "Unauthorized Access",
        "/wp-login.php": "CMS Login Page",
        "/?id=1'": "Possible SQL Injection",
    }
    
    for target in shared_data['fingerprinting'].keys():
        shared_data['vulnerabilities'].setdefault(target, [])
        for path, v_type in attack_vectors.items():
            try:
                # Use a proper session for speed and bypass basic WAF
                resp = requests.get(f"{target.rstrip('/')}{path}", timeout=3)
                if resp.status_code == 200:
                    # Score the finding based on impact
                    shared_data['vulnerabilities'][target].append({
                        "url": f"{target}{path}",
                        "type": v_type,
                        "risk": "HIGH" if ".env" in path else "MEDIUM"
                    })
            except:
                pass
