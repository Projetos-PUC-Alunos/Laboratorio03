import requests
from time import sleep

MAX_QUERY_ATTEMPTS = 10
GITHUB_INDEX = 0
GITHUB_TOKEN = [
    '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',
    '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',
    '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',
    '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',
    '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',
    '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',
    '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',
    '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',
    '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',
    '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',
    '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',
    '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',
    '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',
    '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',
    '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',
    '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A',
    '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',
    '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',
    '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',
    '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'
    ]

def query_runner(query: str, attemp=1) -> dict:
    print("**********EXECUTANDO QUERY_RUNNER**************")
    url = 'https://api.github.com/graphql'
    global GITHUB_INDEX
    token = GITHUB_TOKEN[GITHUB_INDEX]
    headers = {'Authorization': 'Bearer {}'.format(token)}
    try:
        response = requests.post(url, json={'query': query}, headers=headers)
        remaing_requests = response.headers.get('x-ratelimit-remaining')
        ("Response: ", response.status_code, " -> ", response.json(), "\n") if not remaing_requests else None

        if not remaing_requests and response.status_code in (403, 502):
            sleep(60)
            return query_runner(query, attemp)

        if remaing_requests <= '1':
            print('Renovando token...')
            GITHUB_INDEX = (GITHUB_INDEX + 1) % len(GITHUB_TOKEN)
            return query_runner(query, attemp)

        elif response.status_code == 200:
            print('RODANDO...................')
            return response.json()

        elif response.status_code == 502 and attemp <= MAX_QUERY_ATTEMPTS:
            print('DEU ERROR E TENTA DE NOVO...................')
            return query_runner(query, attemp + 1)
        
        elif response.status_code == 502 and attemp > MAX_QUERY_ATTEMPTS:
            print('DEU ERROR E ESTOUROU, TERMINAR...................')
            exit(1)

        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))

    except Exception:
        return query_runner(query, attemp)