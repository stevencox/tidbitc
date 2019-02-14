# tidbitc

**tidbitc** compiles a yaml definition file into a translator tidbit. 

The config file looks like this:
```
header:
  name: workflow-5
  theme: ananke
  title: What phenotypes are associated with chemical exposure in a cohort?
body:
  - name: Question
    text: |
      This is the biomedical question.
      ![Overview](/thumbnail_JD.jpg)
  - name: Background
    issue_id: 36
    text: |
      ![Background](/thumbnail_JD.jpg)
```

## Install

Install the Hugo website generator. (On OS X, `brew install hugo`).

## Run

python gentidbit.py <config-file>

