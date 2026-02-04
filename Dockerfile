# 🔌 Active Skill: @docker-expert
# Defines the specific image for AWS Lambda with Python 3.12
FROM public.ecr.aws/lambda/python:3.12 AS builder

# Install build tools and dependencies
# We need these to compile HDF5 and NetCDF from source
# m4 and libcurl-devel are required for netcdf-c configure
RUN dnf update -y && \
    dnf install -y \
    gcc \
    gcc-c++ \
    make \
    m4 \
    libcurl-devel \
    tar \
    gzip \
    wget \
    openssl-devel \
    zlib-devel \
    diffutils \
    libxml2-devel \
    && dnf clean all

# Versions
ENV HDF5_VERSION=1.14.3
ENV NETCDF_VERSION=4.9.2

# Compile HDF5
WORKDIR /tmp
RUN wget https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.14/hdf5-${HDF5_VERSION}/src/hdf5-${HDF5_VERSION}.tar.gz && \
    tar -xBzf hdf5-${HDF5_VERSION}.tar.gz && \
    cd hdf5-${HDF5_VERSION} && \
    ./configure --prefix=/usr/local --enable-hl && \
    make -j$(nproc) && \
    make install

# Compile NetCDF
WORKDIR /tmp
RUN wget https://downloads.unidata.ucar.edu/netcdf-c/${NETCDF_VERSION}/netcdf-c-${NETCDF_VERSION}.tar.gz && \
    tar -xzf netcdf-c-${NETCDF_VERSION}.tar.gz && \
    cd netcdf-c-${NETCDF_VERSION} && \
    CPPFLAGS="-I/usr/local/include" LDFLAGS="-L/usr/local/lib" ./configure --prefix=/usr/local --disable-dap && \
    make -j$(nproc) && \
    make install

# Install uv for fast package management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy requirements file
COPY api_requirements.txt .

# Install dependencies into a specific directory leveraging uv
# We point HDF5_DIR and NETCDF4_DIR to /usr/local so pip builds the wheels correctly linked
ENV UV_CACHE_DIR=/tmp/.uv-cache
ENV HDF5_DIR=/usr/local
ENV NETCDF4_DIR=/usr/local
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

RUN uv pip install \
    --system \
    --target /var/task \
    --no-cache \
    -r api_requirements.txt

# ==========================================
# Final Stage
# ==========================================
FROM public.ecr.aws/lambda/python:3.12

# Copy the specific libraries we need from builder
# We copy everything from /usr/local/lib to ensure all deps are there
COPY --from=builder /usr/local/lib/libhdf5.so* /usr/lib64/
COPY --from=builder /usr/local/lib/libhdf5_hl.so* /usr/lib64/
COPY --from=builder /usr/local/lib/libnetcdf.so* /usr/lib64/

# Copy the installed python dependencies
COPY --from=builder /var/task /var/task

# Copy application code
COPY app/ ${LAMBDA_TASK_ROOT}/app

# Set the CMD to your handler
CMD ["app.main.handler"]
