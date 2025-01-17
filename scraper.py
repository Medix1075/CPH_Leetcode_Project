import requests
import json

# Function to execute a GraphQL query to fetch problem details
def get_problem_details(problem_slug):
    url = "https://leetcode.com/graphql"
    headers = {
        "Content-Type": "application/json",
    }
    query = {
        "query": """
        {
          question(slug: "%s") {
            title
            titleSlug
            content
            difficulty
            tags {
              name
            }
            exampleTestCases {
              input
              output
            }
          }
        }
        """ % problem_slug,
    }

    # Send POST request to GraphQL endpoint
    response = requests.post(url, headers=headers, data=json.dumps(query))

    # Check if response is valid
    if response.status_code == 200:
        data = response.json()
        problem_data = data.get("data", {}).get("question", {})
        return problem_data
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

# Example usage: Extracting details of a problem (e.g., "two-sum")
problem_slug = "Count Beautiful Splits in an Array"
details = get_problem_details(problem_slug)

if details:
    print(f"Title: {details['title']}")
    print(f"Difficulty: {details['difficulty']}")
    print(f"Description: {details['content']}")
    print(f"Tags: {', '.join(tag['name'] for tag in details['tags'])}")
    print("Example Test Cases:")
    for test_case in details["exampleTestCases"]:
        print(f"Input: {test_case['input']}, Output: {test_case['output']}")
else:
    print("Problem details not found.")
