import src.repositorios as repos
import src.PRs as prs


def Aplicacao(num_repos: int):

     # repos_filename = repos.generate_csv(num_repos)

    # prs.generate_csv(repos_filename)
    prs.generate_csv('./csvs/repositories-ord.csv')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Gerando um arquivo CSV com os repositórios mais populares no GitHub.')
    parser.add_argument('-n', '--num_repos', type=int, default=1)

    args = parser.parse_args()
    Aplicacao(args.num_repos)