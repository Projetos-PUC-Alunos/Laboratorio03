import pandas as pd
import multiprocessing as mul
import src.queries as queries
from src.utils import query_runner
from datetime import datetime as dt


OUTPUT = 'csvs/PRs.csv'
COLUMNS = [
    'nameWithOwner', 
    'id', 
    'title', 
    'state', 
    'createdAt', 
    'closedAt',
    'changedFiles', 
    'additions', 
    'deletions', 
    'reviews', 
    'body',
    'participants', 
    'comments'
]

# Define uma função que busca pull requests para um repositório específico
def get_pull_requests(nameWithOwner: str):
    
    after = 'null'
    prs = []

    # Divide o nome do proprietário e do repositório
    owner, name = nameWithOwner.split('/')

    print("------------- GERANDO DADOS PARA O ARQUIVO CSV DE PULL REQUESTS PARA CADA REPOSITÓRIO COLETADO -------------------")
    
     # Inicia um loop para buscar todas as páginas de pull requests
    while True:

        # Substitui as variáveis no query com o proprietário, repositório e cursor
        query = queries.pull_requests.replace('{owner}', owner)\
                                     .replace('{name}', name)\
                                     .replace('{after}', after)
        print('__________________', owner, name, after)
        results = query_runner(query)
        # Se o resultado for nulo, pula para a próxima iteração do loop
        if not results: continue

        # Adiciona cada pull request encontrado na lista de pull requests
        for pr in results['data']['repository']['pullRequests']['nodes']:
            prs.append((
                nameWithOwner,
                pr['id'],
                pr['title'],
                pr['state'],
                pr['createdAt'],
                pr['closedAt'],
                pr['changedFiles'],
                pr['additions'],
                pr['deletions'],
                pr['reviews']['totalCount'],
                len(pr['body']),
                pr['participants']['totalCount'],
                pr['comments']['totalCount']
            ))
        after = '"' + results['data']['repository']['pullRequests']['pageInfo']['endCursor'] + '"'
        if not results['data']['repository']['pullRequests']['pageInfo']['hasNextPage']:
            break

    # Converte a lista de pull requests em um DataFrame usando as colunas definidas anteriormente        
    output = pd.DataFrame(prs, columns=COLUMNS)

    # Filtra os pull requests que não possuem revisões
    output = output[output['reviews'] > 0]

    # Calcula o tempo gasto em cada pull request e filtra aqueles com menos de uma hora gasta
    output['hours_spent'] = output.apply(lambda x: (dt.strptime(x['closedAt'], '%Y-%m-%dT%H:%M:%SZ') - dt.strptime(x['createdAt'], '%Y-%m-%dT%H:%M:%SZ')), axis=1)
    output['hours_spent'] = output['hours_spent'].apply(lambda x: x.days * 24 + x.seconds / 3600)

    output = output[output['hours_spent'] >= 1]
    
    return output

# Define uma função que gera o arquivo CSV de saída
def generate_csv(input_path: str):
    print("------------GERANDO CSV----------------")
    line = pd.read_csv(input_path)
    repositories = line['nameWithOwner'].unique().tolist()
    pool = mul.Pool(10)
    results = pool.map(get_pull_requests, repositories)
    output = pd.concat(results)
    output.to_csv(OUTPUT, index=False)
    return OUTPUT