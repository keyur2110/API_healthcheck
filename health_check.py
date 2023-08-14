import requests
import time
import yaml

def load_endpoints_from_file(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

def check_health(endpoint):
    try:
        start_time = time.time()

        headers = endpoint.get("headers", {})
        response = requests.request(
            method=endpoint.get("method", "GET"),
            url=endpoint["url"],
            headers=headers,
            data=endpoint.get("body"),
        )

        end_time = time.time()

        if 200 <= response.status_code < 300 and (end_time - start_time) * 1000 < 500:
            return "UP"
        else:
            return "DOWN"
    except requests.exceptions.RequestException:
        return "DOWN"

if __name__ == "__main__":
    file_path = "endpoints.yaml"
    data = load_endpoints_from_file(file_path)
    endpoints = data.get("endpoints", [])

    test_interval = 15
    
    try:
        while True:
            print(f"Testing endpoints at {time.strftime('%Y-%m-%d %H:%M:%S')}:")

            for endpoint in endpoints:
                status = check_health(endpoint)
                availability = 100 if status == "UP" else 0
                print(f"{endpoint['name']} has {availability}% availability percentage")
            
            print("=" * 40)
            
            time.sleep(test_interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")


