#Download base image ubuntu 20.04
FROM ubuntu:20.04

# LABEL about the custom image
LABEL maintainer="mars.frolova@gmail.com"

# Disable Prompt During Packages Installation
ARG DEBIAN_FRONTEND=noninteractive

# Update Ubuntu Software repository
RUN apt update

# Install packages from ubuntu repository
#RUN apt install -y autoconf automake ca-certificates cmake curl g++ gcc git libbz2-dev \
#        libc6-dev libcurl4-gnutls-dev libfreetype6 wget libgsl-dev liblzma-dev \
#        libncurses5-dev libperl-dev libreadline-dev libssl-dev libz-dev make \
#        unzip zlib1g-dev && \
#    rm -rf /var/lib/apt/lists/* && \
#    apt clean


# Install packages from ubuntu repository
RUN apt-get update && \
        apt-get install -y autoconf automake ca-certificates cmake curl g++ gcc git libbz2-dev \
        libc6-dev libcurl4-gnutls-dev libfreetype6 wget libgsl-dev liblzma-dev \
        libncurses5-dev libperl-dev libreadline-dev libssl-dev libz-dev make \
        pkg-config unzip zlib1g-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean
 

# Define software versions
ENV SAMTOOLS_VERSION=1.18
ENV BCFTOOLS_VERSION=1.18
ENV VCFTOOLS_VERSION=0.1.16
ENV HTSLIB_VERSION=1.18

# Установка samtools + htslib + libdeflate
# Официальный сайт: http://www.htslib.org/
# Последний релиз: https://github.com/samtools/samtools/releases/latest

# Set the base soft directory
ENV SOFT="/soft"

# Download and build htslib
WORKDIR $SOFT
RUN wget https://github.com/samtools/htslib/releases/download/$HTSLIB_VERSION/htslib-$HTSLIB_VERSION.tar.bz2 && \
    tar -xjf htslib-$HTSLIB_VERSION.tar.bz2 && \
    rm htslib-$HTSLIB_VERSION.tar.bz2 && \
    cd htslib-$HTSLIB_VERSION && \
    autoheader && \
    autoconf && \
    ./configure --prefix=$SOFT/htslib-$HTSLIB_VERSION && \
    make && \
    make install



# Install samtools
WORKDIR $SOFT
RUN wget https://github.com/samtools/samtools/releases/download/$SAMTOOLS_VERSION/samtools-$SAMTOOLS_VERSION.tar.bz2 && \
    tar -xjf samtools-$SAMTOOLS_VERSION.tar.bz2 && \
    rm samtools-$SAMTOOLS_VERSION.tar.bz2 && \
    cd samtools-$SAMTOOLS_VERSION && \
    ./configure --prefix=$SOFT/samtools-$SAMTOOLS_VERSION && \
    make && \
    make install

# Install bcftools
WORKDIR $SOFT
RUN wget https://github.com/samtools/bcftools/releases/download/$BCFTOOLS_VERSION/bcftools-$BCFTOOLS_VERSION.tar.bz2 && \
    tar -xjf bcftools-$BCFTOOLS_VERSION.tar.bz2 && \
    rm bcftools-$BCFTOOLS_VERSION.tar.bz2 && \
    cd bcftools-$BCFTOOLS_VERSION && \
    ./configure --prefix=$SOFT/bcftools-$BCFTOOLS_VERSION --enable-libgsl --with-htslib=$SOFT/htslib-$HTSLIB_VERSION && \
    make && \
    make install

# Install vcftools
WORKDIR $SOFT
RUN wget https://github.com/vcftools/vcftools/releases/download/v$VCFTOOLS_VERSION/vcftools-$VCFTOOLS_VERSION.tar.gz && \
    tar -xf vcftools-$VCFTOOLS_VERSION.tar.gz && \
    rm vcftools-$VCFTOOLS_VERSION.tar.gz && \
    cd vcftools-$VCFTOOLS_VERSION && \
#    ./autogen.sh && \
    ./configure --prefix=$SOFT/vcftools-$VCFTOOLS_VERSION && \
    make && \
    make install

# Install vcftools
WORKDIR $SOFT
#RUN wget https://github.com/vcftools/vcftools/releases/download/v$VCFTOOLS_VERSION/vcftools-$VCFTOOLS_VERSION.tar.gz \
#    && tar -xf vcftools-$VCFTOOLS_VERSION.tar.gz \
#    && rm vcftools-$VCFTOOLS_VERSION.tar.gz \
#    && cd vcftools-$VCFTOOLS_VERSION \
#    && ./autogen.sh \
#    && ./configure --prefix=$SOFT/vcftools-$VCFTOOLS_VERSION \
#    && make \
#    && make install

# Set environment variables
ENV PATH="$SOFT/htslib-$HTSLIB_VERSION/bin:$SOFT/samtools-$SAMTOOLS_VERSION/bin:$SOFT/bcftools-$BCFTOOLS_VERSION/bin:$SOFT/vcftools-$VCFTOOLS_VERSION/bin:${PATH}"

# Clean up
RUN apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR $SOFT
# Default command
#CMD ["/bin/bash"]
