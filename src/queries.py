repositories = """
    {
      search(query: "stars:>100 sort:stars", type: REPOSITORY, first: 50, after: {after}) {
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
            Closed: pullRequests(states: [CLOSED]) {
                totalCount
            }
            Merged: pullRequests(states: [MERGED]) {
                totalCount
            }
          }
        }
      }
    }
    """


pull_requests = """
    {
      repository(owner: "{owner}", name: "{name}") {
        pullRequests(states: [CLOSED, MERGED], first: 100, after: {after}) {
          pageInfo {
            endCursor
            hasNextPage
          }
          nodes {
            id
            title
            state
            createdAt
            closedAt
            changedFiles
            additions
            deletions
            reviews { totalCount }
            body
            participants { totalCount }
            comments { totalCount }
          }
        }
      }
    }
    """