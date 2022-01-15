#!/usr/bin/env python

import os
import sys

import requests


def get_repos():
    resp = requests.get(f"{url}/orgs/{org}/repos?per_page=100&page=1", headers=headers)
    payload = resp.json()
    while "next" in resp.links:
        resp = requests.get(resp.links["next"]["url"], headers=headers)
        payload.extend(resp.json())

    repos = []
    for repo in payload:
        if not repo["archived"] and not repo["fork"]:
            repos.append(repo["name"])
    return repos


def get_default_branch(repos):
    default_branch = {}
    for repo in repos:
        resp = requests.get(f"{url}/repos/{org}/{repo}", headers=headers).json()
        default_branch[repo] = resp["default_branch"]
    return default_branch


def get_branch_protections(default_branch):
    branch_protections = {}
    for repo, branch in default_branch.items():
        resp = requests.get(
            f"{url}/repos/{org}/{repo}/branches/{branch}/protection",
            headers=headers,
        ).json()
        branch_protections[repo] = {'branch': branch, 'resp': resp}
    return branch_protections


def cmp_branch_protections(rules):
    protections = {}
    for repo in branch_protections:
        print(rules[repo]['branch'])
        print(rules[repo]['resp'])
        

def set_branch_protections(branch_protections):
    return repo


if __name__ == "__main__":
    if sys.argv[1] == "--help" or sys.argv[1] == "-h":
        print(
            f"""
Usage: {sys.argv[0]} [-h] <org> <token>\n
Update repos into default branch protection state\n
Options:
-h | --help                  this message
"""
        )
        exit()
        
    url = "https://api.github.com"
    token = sys.argv[2]
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    org = sys.argv[1]

    repos = get_repos()
    default_branches = get_default_branch(repos)
    branch_protection = get_branch_protections(default_branches)
    is_protected = cmp_branch_protections(branch_protection)




