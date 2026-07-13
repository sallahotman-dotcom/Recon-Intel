import dns.resolver

def run(shared_data):
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = ['8.8.8.8']
    
    subdomains = ["dev", "admin", "api", "test"]
    targets = list(shared_data.get('fingerprinting', {}).keys())
    
    for domain in targets:
        clean_domain = domain.replace("http://", "").replace("https://", "").rstrip('/')
        for sub in subdomains:
            target = f"{sub}.{clean_domain}"
            try:
                resolver.resolve(target, 'A')
                shared_data['fingerprinting'][f"http://{target}"] = {'tech': 'Unknown'}
                print(f"  [+] Found: {target}")
            except Exception:
                continue
