#!/usr/bin/env python3
"""Fetch the latest numeric tag from DockerHub for a repository."""
import os
import re
import json
import urllib.request

repo = os.environ.get("DOCKERHUB_REPO", "ctbushman/bcl_convert")

api_url = f"https://hub.docker.com/v2/repositories/{repo}/tags?page_size=100"
latest = None

while api_url:
    with urllib.request.urlopen(api_url) as resp:
        data = json.load(resp)
    for result in data.get("results", []):
        tag = result.get("name", "")
        if not re.fullmatch(r"\d+(?:\.\d+)*", tag):
            continue
        parts = tuple(map(int, tag.split(".")))
        if latest is None or parts > latest:
            latest = parts
    api_url = data.get("next")

if latest:
    print(".".join(map(str, latest)))
