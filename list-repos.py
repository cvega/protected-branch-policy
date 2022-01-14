#!/usr/bin/env python

import os
import requests
import sys


def list_repos(org):
    resp = requests.get(f"{url}/orgs/{org}/repos?per_page=100&page=1", headers=headers)
    repos = resp.json()
    while "next" in resp.links.keys():
        resp = requests.get(resp.links["next"]["url"], headers=headers)
        repos.extend(resp.json())

    with open(f"{org}.txt", mode="w") as file:
        for repo in repos:
            if not repo["archived"] and not repo["fork"]:
                file.write(f'{repo["full_name"]}\n')

                
if __name__ == "__main__":
    if sys.argv[1] == "--help" or sys.argv[1] == "-h":
        print(
            f"""
        Usage: {sys.argv[0]} ][-h] <org>\n
        List repos that are not forks or archived and write to a file (<org>.txt)\n
        Options:
        -h | --help                  this message
        """
        )
        exit()
    url = "api.github.com"
    token = os.getenv("GITHUB_TOKEN")
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    list_repos(sys.argv[1])
