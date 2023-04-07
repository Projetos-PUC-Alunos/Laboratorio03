import src.repositorios as repos


def main(num_repos: int):

    repos.generate_csv(num_repos)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Generate a CSV file with the most popular repositories on GitHub.')
    parser.add_argument('-n', '--num_repos', type=int, default=1000, help='Number of repositories to generate.')

    args = parser.parse_args()
    main(args.num_repos)