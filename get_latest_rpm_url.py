#!/usr/bin/env python3
"""Fetch the latest CentOS7 bcl-convert RPM URL from Illumina."""
import re
import sys
import urllib.request
import urllib.error

DOWNLOADS_URL = "https://support.illumina.com/sequencing/sequencing_software/bcl-convert/downloads.html"

pattern = re.compile(r'(https?://[^"\s]*bcl-convert-(\d+(?:\.\d+)*)-2\.el7\.x86_64\.rpm)')

try:
    with urllib.request.urlopen(DOWNLOADS_URL) as resp:
        html = resp.read().decode()
except urllib.error.URLError as e:
    sys.exit(f"Failed to fetch the downloads page: {e.reason}")
except urllib.error.HTTPError as e:
    sys.exit(f"HTTP error occurred: {e.code} {e.reason}")

best_version = None
best_url = None

for match in pattern.finditer(html):
    url, version = match.groups()
    ver_tuple = tuple(int(x) for x in version.split('.'))
    if best_version is None or ver_tuple > best_version:
        best_version = ver_tuple
        best_url = url

if not best_url:
    sys.exit("No RPM URL found on page")

print(best_url)
