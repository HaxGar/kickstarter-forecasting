FROM python:3.12.9-slim

# Installation de Firefox dans le container
RUN apt-get update && apt-get install wget gnupg -y
RUN wget -q -O - https://packages.mozilla.org/apt/repo-signing-key.gpg | apt-key add - \
    && echo "deb https://packages.mozilla.org/apt mozilla main" | tee -a /etc/apt/sources.list.d/mozilla.list \
    && apt-get update \
    && apt-get install -y firefox

# Équivalent de "mkdir kickstarter && cd kickstarter"
WORKDIR /kickstarter

# On installe d'abord le requirements.txt pour faire l'installation des dépendences
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Ensuite les datasets nltk qui sont lourds
RUN python3 -m nltk.downloader punkt
RUN python3 -m nltk.downloader wordnet
RUN python3 -m nltk.downloader stopwords
RUN python3 -m nltk.downloader punkt_tab

# On rajoute le projet Kickstarter (et tous les autres dossiers)
ADD kickstarter_predictor ./kickstarter_predictor
ADD apps ./apps
ADD models ./models
ADD data/processed/live_commentaires.parquet ./data/processed/live_commentaires.parquet

# Une fois que tout est en place, on installe le projet
COPY pyproject.toml .
RUN pip install -e .

EXPOSE 80

# Commande qui sera lancée au démarrage du container
CMD ["fastapi", "run", "apps/API.py", "--host", "0.0.0.0", "--port", "80"]