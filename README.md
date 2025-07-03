# bcl_convert
[![DockerHub](https://img.shields.io/docker/pulls/ctbushman/bcl_convert)](https://hub.docker.com/repository/docker/ctbushman/bcl_convert)

Illumina BCL Convert software containerized for cross platform use.

## Usage

Pre-built container images are published on Docker Hub under
`ctbushman/bcl_convert`. You can use the `latest` tag or select a specific
version.

### Docker

Run the tool directly from the Docker Hub image:

```bash
docker run --rm -v "$PWD":/data ctbushman/bcl_convert bcl-convert --help
```

### Singularity/Apptainer

You can create a Singularity/Apptainer image from the Docker Hub image:

```bash
apptainer build bcl_convert.sif docker://ctbushman/bcl_convert:latest
```

Run the tool inside the container just as you would under Docker:

```bash
apptainer run -B "$PWD":/data bcl_convert.sif bcl-convert --help
```

### Running on Slurm with Apptainer

When using a Slurm cluster, you can launch jobs with Apptainer by binding
your working directory and specifying the container image:

```bash
srun --container-image=bcl_convert.sif --container-workdir=$PWD \
     bcl-convert --help
```

## Building

This repository contains a helper script, `get_latest_rpm_url.py`, which
scrapes Illumina's download page to locate the newest CentOS7 RPM.

```bash
python3 get_latest_rpm_url.py
```

Download that RPM into the repository and build the Docker image using the
corresponding version number:

```bash
# Download the RPM
curl -LO "$(python3 get_latest_rpm_url.py)"

# Extract the version from the file name
VERSION=$(ls bcl-convert-*-2.el7.x86_64.rpm | sed -n 's/.*bcl-convert-\(.*\)-2.el7.x86_64.rpm/\1/p')

docker build --build-arg BCLCONVERT_VERSION="$VERSION" -t bcl_convert .
```

The Dockerfile expects the RPM to be present in the build context.
