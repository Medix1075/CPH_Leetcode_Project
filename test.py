import requests
import json

url = "https://leetcode.com/graphql"
headers = {
    "accept": "*/*",
    "accept-language": "en",
    "content-type": "application/json",
    "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin"
}
query = """
query {
    question() {
        title
        content
        questionId
    }
}
"""
response = requests.post(url, json={'query': query}, headers=headers)

try:
    response = requests.post(url, json={'query': query}, headers=headers, timeout=30)  # Set timeout to 30 seconds
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
except requests.exceptions.Timeout:
    print("The request timed out.")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
