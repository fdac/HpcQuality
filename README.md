# Measure Quality of HPC Operational Data

## RQ:
Do HPC VCS has high quality of commits (comparable to that of popular projects on
GH/BB)

## Motivation:

If HPC VCS contains high quality data:
- There could be many lessons to learn about HPC software development.
- Tools could be built to improve HPC dev.

Answering this question and determining what issues HPC VCS data may have would have a
significant impact on HPC development by
a) suggesting better practices of commits
b) shedding light on how HPC code is developed
c) suggesting tools that utilize such data to help HPC SW development

## Approach:
### Discover HPC code
- look at descriptions of existing projects
- pick keywords "numeric", ...
- search over all BB GH repos

### Over the provided and discovered VCS look at stats:
- Number of files
- Number of commits (do not count repeats over files)
- Number of authors
- Number of commit messages (unique)
- Distribution of commits over authors (detect admins)
- Distribution of commits over commit messages (detect low-quality repeating messages)
- How many commit logs contain issue (TRAC or JIRA ID)

```
gunzip -c git.whamcloud.com_fs_lustre-dev.git.delta.gz | cut -d\; -f2 |sort | uniq -c | sort -n
gunzip -c git.whamcloud.com_fs_linux-staging.git.delta.gz | cut -d\; -f2 |sort | uniq -c | sort -n
```

### Measure quality of commits:
- http://robots.thoughtbot.com/5-useful-tips-for-a-better-commit-message
- https://github.com/erlang/otp/wiki/Writing-good-commit-messages
- http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html
- http://ablogaboutcode.com/2011/03/23/proper-git-commit-messages-and-an-elegant-git-history/
- http://stackoverflow.com/questions/15324900/standard-to-follow-when-writing-git-commit-messages
- http://stackoverflow.com/questions/2290016/git-commit-messages-50-72-formatting

