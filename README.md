# branch-protections
A Simple Action / Python Script to enforce Branch Protections

### The actions can be scheduled or run manually:

- uses a github app to authenticate (required, PAT cannot update branch protections)
- uses cache for pip
- runs on windows or linux

### The script performs a couple of simple tasks:

- recursively obtains repos via pagination
- requests branch protection rules for each repo
- compare repo rules against default rule set
- if rules do not match, update rules and print details to STDOUT

Not a lot of magic here. We use a response JSON file to validate against the GitHub API reply. If the rule does not match we send the payload JSON file as a `PUT` to bring the repo into compliance.


