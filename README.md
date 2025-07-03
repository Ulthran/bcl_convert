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

Download that RPM (has to be done manually because Illumina requires you to login and verify you're a customer)
and build the Docker image using the corresponding version number:

```bash
# Extract the version from the file name
VERSION=$(ls bcl-convert-*-2.el7.x86_64.rpm | sed -n 's/.*bcl-convert-\(.*\)-2.el7.x86_64.rpm/\1/p')
# OR just do it manually e.g.
VERSION=4.4.4

# Set your DockerHub channel (mine is ctbushman)
DOCKERHUB_USERNAME=ctbushman

# This will require having Docker installed and the daemon running
docker build --build-arg BCLCONVERT_VERSION="$VERSION" -t $DOCKERHUB_USERNAME/bcl_convert:$VERSION .
```

The Dockerfile expects the RPM to be present in the build context.

Then push the image to DockerHub (this will require write access to the DockerHub channel you're trying to push to):

```bash
docker push $DOCKERHUB_USERNAME/bcl_convert:$VERSION
docker tag $DOCKERHUB_USERNAME/bcl_convert:$VERSION $DOCKERHUB_USERNAME/bcl_convert:latest
docker push $DOCKERHUB_USERNAME/bcl_convert:latest
```
