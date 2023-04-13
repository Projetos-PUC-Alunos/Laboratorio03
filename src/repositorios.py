import pandas as pd

import src.queries as queries
from src.utils import query_runner

OUTPUT = 'csvs/repositories.csv'

def generate_csv(num_repos: int):
    after = 'null'
    
    # Cria um DataFrame vazio com as colunas desejadas
    df = pd.DataFrame(columns=['nameWithOwner', 'url', 'createdAt', 'stargazers', 'pullRequests'])
    
    while len(df) < num_repos:
        print("------------- GERANDO DADOS PARA O ARQUIVO CSV PARA REPOSITÓRIOS -------------------")
        
        # Substitui o valor de {after} na query e executa a consulta
        query = queries.repositories.replace('{after}', after)
        results = query_runner(query)
        
        # Itera sobre os repositórios retornados na consulta
        for repo in results['data']['search']['nodes']:
            # Calcula o total de pull requests do repositório
            pull_requests = repo['Closed']['totalCount'] + repo['Merged']['totalCount']  

            # Aplica um filtro para incluir apenas repositórios com quantidade de pull requests entre 100 e 500
            if pull_requests < 100: continue  

            df = pd.concat([df, pd.DataFrame({
                'nameWithOwner': [repo['nameWithOwner']],
                'url': [repo['url']],
                'createdAt': [repo['createdAt']],
                'stargazers': [repo['stargazers']['totalCount']],
                'pullRequests': [pull_requests]
            })])
        
        # Atualiza o cursor para a próxima página, se houver
        after = '"' + results['data']['search']['pageInfo']['endCursor'] + '"'
        
        if not results['data']['search']['pageInfo']['hasNextPage']:
            break
    
    # Escreve o DataFrame em um arquivo CSV e retorna o caminho do arquivo gerado
    df.to_csv(OUTPUT, index=False)
    return OUTPUT
