# Creating a Private GitHub Repository

## Using `gh` CLI
```bash
gh repo create <repo-name> --private --description "Description here" --clone
```
* `--private` makes the repo private.
* Omit `--public` (default is public if not specified).

## Using Git + cURL (API)
1. Create the repo via API:
```bash
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user/repos \
  -d '{
    "name": "<repo-name>",
    "description": "Description here",
    "private": true,
    "auto_init": true
  }'
```
2. Clone it:
```bash
git clone https://github.com/<username>/<repo-name>.git
```

## Making an Existing Repo Private
```bash
# Via gh
gh repo edit <username>/<repo-name> --private

# Via cURL (PATCH)
curl -s -X PATCH \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/<username>/<repo-name> \
  -d '{"private": true}'
```