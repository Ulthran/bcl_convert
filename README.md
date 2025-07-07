# bcl_convert
[![DockerHub](https://img.shields.io/docker/pulls/ctbushman/bcl_convert)](https://hub.docker.com/repository/docker/ctbushman/bcl_convert)

Illumina BCL Convert software containerized for cross-platform use with Docker
and Singularity/Apptainer, enabling Mac, Windows and Linux workflows.

> **Note**
> bcl-convert is a commercial tool from Illumina. The container images provided
> here are community maintained and are not provided nor supported by Illumina.

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
# You may need to load the module for apptainer/singularity (something like `module load singularity`)
# If you have singularity instead of apptainer, replace the command in the below examples
apptainer build bcl_convert.sif docker://ctbushman/bcl_convert:latest
```

Run the tool inside the container just as you would under Docker:

```bash
apptainer run -B "$PWD":/data bcl_convert.sif bcl-convert --help
```

### Running on Slurm with Apptainer

When using a Slurm cluster, you can launch jobs with Apptainer by binding
your working directory and specifying the container image. Create the below
script and save it as something like `basecall.sh` (be sure to replace 
elements like `--partition=defq` or `--account=hpcusers` with values specific 
to your HPC:

```bash
#!/bin/bash
#SBATCH --job-name=basecall
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=24:00:00
#SBATCH --partition=defq
#SBATCH --account=hpcusers

module load singularity

singularity exec --bind $2:/data $1 bcl-convert --bcl-input-directory /data/ --output-directory /data/Data/Intensities/BaseCalls/
```

Then submit the script to your cluster:

```bash
sbatch basecall.sh /path/to/bcl_convert.sif /path/to/sequencing/dir/
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

## Search keywords

For easier discovery by users looking for a portable BCL Convert solution,
below are some terms associated with this project:

- cross platform BCL Convert
- bcl-convert Docker container
- Apptainer or Singularity BCL Convert
- HPC and Slurm BCL Convert
- Windows, macOS and Linux BCL Convert container
