# Laboratorio03

## SCRIPT DOS REPOSITORIOS

```
search(query: "stars:>100 sort:stars", type: REPOSITORY, first: 250, after: {after}) {
        pageInfo {
          hasNextPage
          endCursor
        }
        nodes {
          ... on Repository {
            nameWithOwner
            url
            createdAt
            stargazers {
              totalCount
            }
            prClosed: pullRequests(states: [CLOSED]) {
                totalCount
            }
            prMerged: pullRequests(states: [MERGED]) {
                totalCount
            }
          }
        }
      }
    }
```
