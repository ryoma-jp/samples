FROM ubuntu:22.04

# Install necessary packages for Python 3.10
RUN apt update && apt install -y software-properties-common

# Add Deadsnakes PPA and install Python 3.10
RUN add-apt-repository ppa:deadsnakes/ppa && apt update && apt install -y python3.10 python3.10-distutils python3-pip python3.10-dev

# Install necessary packages
RUN apt install -y graphviz-dev git libgl1 vim
COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

# Copy Hailo Dataflow Compiler and Hailo Model Zoo wheel files
COPY ./whl/hailo_dataflow_compiler-3.29.0-py3-none-linux_x86_64.whl /tmp/hailo_dataflow_compiler-3.29.0-py3-none-linux_x86_64.whl
COPY ./whl/hailo_model_zoo-2.13.0-py3-none-any.whl /tmp/hailo_model_zoo-2.13.0-py3-none-any.whl

# Install wheel files (local user)
ARG USER_ID
ARG GROUP_ID
ARG USER_NAME
RUN groupadd -g ${GROUP_ID} ${USER_NAME} && \
    useradd -m -u ${USER_ID} -g ${GROUP_ID} ${USER_NAME}
USER ${USER_NAME}

ENV PATH="${PATH}:/tmp/lib/hailo/bin"
ENV PYTHONPATH="${PYTHONPATH}:/tmp/lib/hailo"
RUN pip3 install --target "/tmp/lib/hailo" /tmp/hailo_dataflow_compiler-3.29.0-py3-none-linux_x86_64.whl /tmp/hailo_model_zoo-2.13.0-py3-none-any.whl

# Download hailo_model_zoo
RUN cd /tmp/ && \
        git clone https://github.com/hailo-ai/hailo_model_zoo.git && \
        cd hailo_model_zoo && \
        git checkout 88365ee4f0d5d2b7a071dcc3bde8db4a81a80009 && \
        ln -s /tmp/hailo_model_zoo/hailo_model_zoo/cfg/postprocess_config /tmp/lib/hailo/hailo_model_zoo/cfg/

