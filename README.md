# bcl_convert
Illumina BCL Convert software containerized for cross platform use

## Building

This repository contains a helper script, `get_latest_rpm_url.py`, which
scrapes Illumina's download page and prints the URL of the latest CentOS7 RPM.

```bash
python3 get_latest_rpm_url.py
```

Download that RPM into the repository and build the image by passing the
corresponding version number to the Docker build:

```bash
# Download the RPM
curl -LO "$(python3 get_latest_rpm_url.py)"

# Extract the version from the file name
VERSION=$(ls bcl-convert-*-2.el7.x86_64.rpm | sed -n 's/.*bcl-convert-\(.*\)-2.el7.x86_64.rpm/\1/p')

docker build --build-arg BCLCONVERT_VERSION="$VERSION" -t bcl_convert .
```

The Dockerfile expects the RPM to be present in the build context.
