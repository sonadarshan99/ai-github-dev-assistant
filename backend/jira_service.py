from jira import JIRA

jira = JIRA(
    server="https://sonadarshan99.atlassian.net",
    basic_auth=("email","api_token")
)

def create_issue(title, description):

    issue = jira.create_issue(
        project={"key":"AI"},
        summary=title,
        description=description,
        issuetype={"name":"Task"}
    )

    return issue.key