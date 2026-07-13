import json
import datetime

def run(shared_data):
    # Clean data by removing non-serializable objects
    clean_data = {key: value for key, value in shared_data.items() if key != 'session'}
    
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"report_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(clean_data, f, indent=4)
    
    print(f"[*] Report saved successfully to {filename}")

