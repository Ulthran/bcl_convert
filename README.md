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

## Usage

### Docker

With the image built as `bcl_convert`, you can invoke the `bcl-convert`
binary directly:

```bash
docker run --rm -v "$PWD":/data bcl_convert bcl-convert --help
```

### Singularity/Apptainer

You can create a Singularity/Apptainer image from the Docker build:

```bash
apptainer build bcl_convert.sif docker-archive://bcl_convert:latest
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
