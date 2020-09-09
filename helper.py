from github import Github
import sys
import os

ME = os.environ.get("GITHUB_HELPER_ME")
args = sys.argv
primary_arg = None
secondary_arg = None

if len(args) >= 2:
  primary_arg = args[1]

g = Github(os.environ.get('GITHUB_HELPER_KEY'))
user = g.get_user()

repo_name = os.environ.get('GITHUB_HELPER_REPO')
repo = g.get_repo(repo_name)

if primary_arg is None:
  issues = repo.get_issues(assignee=ME, state='open')
  for i in issues:
    issue_id = i.number
    print("%s\t%s" % (i.number, i.title))

if primary_arg in ('create', 'add'):
  task_name = ' '.join(args[2:])
  issue = repo.create_issue(title=task_name,assignee=ME)
  url = 'https://github.com/%s/issues/%s' % (repo_name, issue.number)
  msg = "Created issue %s" % url
  print(msg)

if primary_arg == 'url':
  issue_id = args[2]
  issue = repo.get_issue(number=int(issue_id))
  url = 'https://github.com/%s/issues/%s' % (repo_name, issue.number)
  msg = "Issue @ %s" % url
  print(msg)

if primary_arg == 'list':
  state = args[2]
  if state:
    issues = repo.get_issues(assignee=ME, state=state)
  else:
    issues = repo.get_issues(assignee=ME)
  for issue in issues:
    if state:
      output = '%s\t%s\t%s' % (issue.number, issue.closed_at, issue.title)
    else:
      output = '%s\t%s' % (issue.number, issue.title)
    print(output)

if primary_arg == 'close':
  issue_id = args[2]
  comment = None
  if len(args) >= 3:
    comment = ' '.join(args[3:])
  issue = repo.get_issue(number=int(issue_id))
  issue.edit(state='closed')
  if comment is not None:
    issue.create_comment(body=comment)
  url = 'https://github.com/%s/issues/%s' % (repo_name, issue.number)
  msg = "closed issue %s" % url
  print(msg)

if primary_arg == 'comment':
  issue_id = args[2]
  comment = ' '.join(args[3:])
  issue = repo.get_issue(number=int(issue_id))
  issue.create_comment(body=comment)
  url = 'https://github.com/%s/issues/%s' % (repo_name, issue.number)
  msg = "commented issue %s" % url
  print(msg)
