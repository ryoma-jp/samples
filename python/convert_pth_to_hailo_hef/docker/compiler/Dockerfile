FROM ubuntu:22.04

# Install necessary packages for Python 3.10
RUN apt update && apt install -y software-properties-common

# Add Deadsnakes PPA and install Python 3.10
RUN add-apt-repository ppa:deadsnakes/ppa && apt update && apt install -y python3.10 python3.10-distutils python3-pip python3.10-dev

# Install necessary packages
RUN apt install -y graphviz-dev
COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

# Copy Hailo Dataflow Compiler and Hailo Model Zoo wheel files
COPY ./whl/hailo_dataflow_compiler-3.29.0-py3-none-linux_x86_64.whl /tmp/hailo_dataflow_compiler-3.29.0-py3-none-linux_x86_64.whl
COPY ./whl/hailo_model_zoo-2.13.0-py3-none-any.whl /tmp/hailo_model_zoo-2.13.0-py3-none-any.whl

# Install wheel files
RUN pip3 install /tmp/hailo_dataflow_compiler-3.29.0-py3-none-linux_x86_64.whl /tmp/hailo_model_zoo-2.13.0-py3-none-any.whl
