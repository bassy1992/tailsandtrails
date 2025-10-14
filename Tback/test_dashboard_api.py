import requests
import json

# Test token
token = "52def62fbfe219db9083a2165e2be6a209fbe2b2"
headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json',
}

base_url = 'http://localhost:8000/api/dashboard'

# Test overview endpoint
print("Testing overview endpoint...")
try:
    response = requests.get(f'{base_url}/overview/', headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("Overview data:", json.dumps(data, indent=2))
    else:
        print("Error:", response.text)
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*50 + "\n")

# Test bookings endpoint
print("Testing bookings endpoint...")
try:
    response = requests.get(f'{base_url}/bookings/', headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Found {len(data)} bookings")
        for booking in data[:2]:  # Show first 2
            print(f"- {booking['destination']} ({booking['type']}) - {booking['status']}")
    else:
        print("Error:", response.text)
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*50 + "\n")

# Test activity endpoint
print("Testing activity endpoint...")
try:
    response = requests.get(f'{base_url}/activity/', headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Found {len(data)} activities")
        for activity in data[:3]:  # Show first 3
            print(f"- {activity['title']} ({activity['status']})")
    else:
        print("Error:", response.text)
except Exception as e:
    print(f"Error: {e}")