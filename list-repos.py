#!/usr/bin/env python

import os
import sys

import requests


def get_repos():
    resp = requests.get(f"{url}/orgs/{org}/repos?per_page=100&page=1", headers=headers)
    repos = resp.json()
    while "next" in resp.links.keys():
        resp = requests.get(resp.links["next"]["url"], headers=headers)
        repos.extend(resp.json())

    with open(f"{org}.txt", mode="w") as file:
        for repo in repos:
            if not repo["archived"] and not repo["fork"]:
                file.write(f'{repo["name"]}\n')


def get_default_branch():
    repos = []
    with open(f"{org}.txt") as file:
        while repo := file.readline().rstrip():
            resp = requests.get(f"{url}/repos/{org}/{repo}", headers=headers).json()
            repos.append(f'{repo},{resp["default_branch"]}')

    with open(f"{org}-default-branch.txt", mode="w") as file:
        for repo in repos:
            file.write(f"{repo}\n")


def get_branch_protections():
    with open(f"{org}-default-branch.txt", mode="r") as file:
        while repo := file.readline().rstrip():
            repo = repo.split(",")
            resp = requests.get(
                f"{url}/repos/{org}/{repo[0]}/branches/{repo[1]}/protection",
                headers=headers,
            ).json()
            print(resp)


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

    get_repos()
    get_default_branch()
    get_branch_protections()
