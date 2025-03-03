import requests

# Replace with your actual Supabase URL and table name
url = 'https://vndclryqjcrarvhtpfrf.supabase.co/rest/v1/users?select=*'

# Define headers with the correct API key and Authorization Bearer token
headers = {
    "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZuZGNscnlxamNyYXJ2aHRwZnJmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk3NDgwMDUsImV4cCI6MjA1NTMyNDAwNX0.LWu2AU3iJHZNCyHBw_1j-nh4yZBLop7PKShrr599OqU",  # Replace with your actual API key
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZuZGNscnlxamNyYXJ2aHRwZnJmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk3NDgwMDUsImV4cCI6MjA1NTMyNDAwNX0.LWu2AU3iJHZNCyHBw_1j-nh4yZBLop7PKShrr599OqU"  # Replace with your actual auth token
}

# Make the GET request to Supabase API
response = requests.get(url, headers=headers)

# Print status and response for debugging
print("Status Code:", response.status_code)
#print("Response Text:", response.text)

# If response status is OK (200), parse and print JSON
if response.status_code == 200:
    print(response.json())
else:
    print("Error: Could not fetch data.")
