FROM continuumio/miniconda3

ADD ./requirements.txt ./requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN conda install -c conda-forge opencv

RUN apt-get update && apt-get install -y libgl1-mesa-glx

ADD . /usr/src/app
WORKDIR /usr/src/app

EXPOSE 4000

ENTRYPOINT [ "python", "index.py" ]
