
# --- build command ---
#   docker build --network=host -f Dockerfile -t jupyter_nb/module_list .
#
# --- for machine learning ---
FROM jupyter/scipy-notebook:latest

USER root

RUN apt update ; \
    apt upgrade -y ; \
    apt install -y graphviz

USER jovyan

RUN pip install pip-licenses==3.5.4 \
		pipdeptree==2.2.1 \
		graphviz==0.20 \
		pydeps==1.10.18 

