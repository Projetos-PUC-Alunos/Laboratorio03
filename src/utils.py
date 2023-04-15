import requests
from time import sleep
from random import randint

MAX_QUERY_ATTEMPTS = 10
GITHUB_INDEX = 0
GITHUB_TOKEN = [
    '',
    '',
    ]

def query_runner(query: str, attemp=1) -> dict:
    
    url = 'https://api.github.com/graphql'
    global GITHUB_INDEX
    token = GITHUB_TOKEN[GITHUB_INDEX]
    headers = {'Authorization': 'Bearer {}'.format(token)}
    try:
        sleep(randint(1, 30))
        response = requests.post(url, json={'query': query}, headers=headers)
        remaing_requests = response.headers.get('x-ratelimit-remaining')
        ("Response: ", response.status_code, " -> ", response.json(), "\n") if not remaing_requests else None

        if not remaing_requests and response.status_code in (403, 502):
            sleep(60)
            return query_runner(query, attemp)

        if remaing_requests <= '1':
            GITHUB_INDEX = (GITHUB_INDEX + 1) % len(GITHUB_TOKEN)
            return query_runner(query, attemp)

        elif response.status_code == 200:
            return response.json()

        elif response.status_code == 502 and attemp <= MAX_QUERY_ATTEMPTS:
            return query_runner(query, attemp + 1)
        
        elif response.status_code == 502 and attemp > MAX_QUERY_ATTEMPTS:
            exit(1)

        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))

    except Exception:
        return query_runner(query, attemp)