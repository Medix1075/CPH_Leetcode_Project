import requests
import json
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


def get_problem_info(titleSlug):
    data = {
        "operationName": "questionData",
        "variables": {"titleSlug": titleSlug},
        "query": """
        query questionData($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionId
                questionFrontendId
                title
                titleSlug
                content
                difficulty
                likes
                dislikes
                similarQuestions
                topicTags {
                    name
                    slug
                    translatedName
                }
                codeSnippets {
                    lang
                    langSlug
                    code
                }
                stats
                hints
                solution {
                    id
                    canSeeDetail
                }
                status
                sampleTestCase
                metaData
                judgerAvailable
                judgeType
                mysqlSchemas
                enableRunCode
                exampleTestcases
            }
        }
        """
    }

    url = "https://leetcode.com/graphql"
    
    try:
        response = requests.post(url=url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raises an exception for bad status codes
        
        r_json = response.json()
        if 'data' in r_json and 'question' in r_json['data']:
            return r_json['data']['question']
        else:
            print("Problem details not found in the API response.")
            return None
    except Exception as e:
        print(f"Error fetching problem details: {e}")
        return None


