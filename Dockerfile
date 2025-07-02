# syntax=docker/dockerfile:1

FROM debian:bullseye-slim
ARG BCLCONVERT_VERSION
ARG RPM_FILENAME="bcl-convert-${BCLCONVERT_VERSION}-2.el7.x86_64.rpm"

LABEL org.opencontainers.image.description="Docker image containing bcl-convert"
LABEL org.opencontainers.image.version="$BCLCONVERT_VERSION"
LABEL org.opencontainers.image.documentation="https://github.com/Ulthran/bcl_convert/README.md"
LABEL org.opencontainers.image.source="https://github.com/Ulthran/bcl_convert"
LABEL org.opencontainers.image.vendor="Penn-CHOP Microbiome Program"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       procps rpm2cpio cpio \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN ln -s /bin/hostname /usr/bin/hostname

# Add and extract the RPM package
ADD ${RPM_FILENAME} bcl-convert.rpm

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN rpm2cpio bcl-convert.rpm | cpio -idmv && rm bcl-convert.rpm

# Clean up logs and link log dir to tmp
RUN rm -rf /var/log/bcl-convert && ln -sfT /tmp /var/log/bcl-convert

# Export bin dir for easy access
ENV PATH="/bcl-convert-${BCLCONVERT_VERSION}/bin:$PATH"
