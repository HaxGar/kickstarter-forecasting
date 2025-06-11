#FROM
FROM python:3.12.9-alpine
#COPY
COPY kickstarter_predictor /kickstarter_predictor
COPY apps /apps
COPY pyproject.toml /pyproject.toml
COPY Makefile /Makefile
COPY models /models
COPY data/processed/live_commentaires.parquet /data/processed/live_commentaires.parquet
#RUN
RUN pip install --upgrade pip
RUN pip install -U scikit-learn
RUN pip install -e .
#CMD
CMD fastapi dev apps/API.py  --host 0.0.0.0 --port
