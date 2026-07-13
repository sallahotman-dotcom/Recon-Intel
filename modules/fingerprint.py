import requests
import os

def run(shared_data):
    target_file = 'targets.txt'
    if not os.path.exists(target_file):
        return

    with open(target_file, 'r') as f:
        targets = [line.strip() for line in f if line.strip()]

    shared_data['fingerprinting'] = {}

    for target in targets:
        try:
            url = target if target.startswith('http') else f"http://{target}"
            response = requests.get(url, timeout=5)
            shared_data['fingerprinting'][url] = {
                "server": response.headers.get('Server', 'Unknown'),
                "powered_by": response.headers.get('X-Powered-By', 'None')
            }
        except Exception as e:
            shared_data['fingerprinting'][target] = {"error": str(e)}
