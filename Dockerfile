FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-devel

ARG USE_CUDA=0
# Titan V
ARG TORCH_ARCH=

ENV AM_I_DOCKER True
ENV BUILD_WITH_CUDA "${USE_CUDA}"
ENV TORCH_CUDA_ARCH_LIST "Maxwell;Maxwell+Tegra;Pascal;Volta;Turing"
ENV CUDA_HOME /usr/local/cuda

ENV TZ=Europe/Stockholm
RUN apt update && DEBIAN_FRONTEND=noninteractive apt install -y git make build-essential cmake ninja-build
RUN apt-get install -y libgl1 libgl1-mesa-glx libglib2.0-0

RUN pip install -U pip
RUN pip install -U git+https://github.com/luca-medeiros/lang-segment-anything.git@05c386ee95b26a8ec8398bebddf70ffb8ddd3faf
RUN pip install grpcio protobuf pyransac3d transformations scikit-learn

RUN mkdir /app

RUN useradd -rm -d /home/ubuntu -s /bin/bash -u 1001 ubuntu
COPY cache /home/ubuntu/.cache
RUN chown -R ubuntu:ubuntu /home/ubuntu/.cache

USER ubuntu
WORKDIR /app

ENV NVIDIA_DRIVER_CAPABILITIES=all

COPY src/ /app
CMD [ "python", "LangSAM_image_pipeline.py" ]
