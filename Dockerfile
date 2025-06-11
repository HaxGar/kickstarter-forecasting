#FROM
FROM python:3.12.9-slim
WORKDIR /kickstarter

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python3 -m nltk.downloader punkt
RUN python3 -m nltk.downloader wordnet
RUN python3 -m nltk.downloader stopwords
RUN python3 -m nltk.downloader punkt_tab

#ADD
ADD kickstarter_predictor ./kickstarter_predictor
ADD apps ./apps

COPY pyproject.toml .
ADD models ./models
ADD data/processed/live_commentaires.parquet ./data/processed/live_commentaires.parquet
RUN pip install -e .


#CMD
CMD ["fastapi", "run", "apps/API.py", "--host", "0.0.0.0", "--port", "8080"]
