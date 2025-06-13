include .env

DATA_DIR=${ROOT}/data
DL_URL=https://files.slack.com/files-pri/T02NE0241-

clean_folders:
	rm -rf ${DATA_DIR}/processed
	mkdir ${DATA_DIR}/processed
	mkdir ${DATA_DIR}/processed/par_commentaire
	mkdir ${DATA_DIR}/processed/par_projet

do_cleaned_data:
	python -c 'from kickstarter_predictor.data import load_data; load_data();'

do_live_data:
	python -c 'from kickstarter_predictor.data import load_data; load_data(live=True);'

reset_data: clean_folders do_cleaned_data do_live_data

download_raw_data_files:
	rm -rf ${DATA_DIR}/raw
	mkdir ${DATA_DIR}/raw
	-curl ${DL_URL}F09081835UG/download/ks-projects-201801.csv?pub_secret=4522e433b2 > ${DATA_DIR}/raw/ks-projects-201801.csv
	-curl ${DL_URL}F08UWDGPP37/download/comments_clean.csv?pub_secret=fedb7864a9 > ${DATA_DIR}/raw/comments_clean.csv

install:
	pip install -e .


docker_build:
	docker compose build

gcp_push:
	docker compose push

gcp_allow:
	gcloud compute firewall-rules create allow-fastapi   --allow tcp:80   --source-ranges 0.0.0.0/0   --description "Allow FastAPI on port 80"

gcp_instance_ip:
	gcloud compute instances describe kickstarter-instance-api --format='get(networkInterfaces[0].accessConfigs[0].natIP)'

gcp_deploy:
	gcloud compute instances create-with-container kickstarter-instance-api 									\
	--zone=europe-west1-b 																						\
	--machine-type=e2-small																						\
	--container-image=europe-west1-docker.pkg.dev/solar-imprint-456810-d6/kickstarter/kickstarter-anatole-fix 	\
	--tags=http-server 																							\
	--container-restart-policy=always																			\
	--container-env ROOT=/kickstarter

instance_ssh:
	gcloud compute ssh kickstarter-instance-api

cloud:
	make docker_build
	make gcp_push
	make gcp_deploy

test:
	@echo ${DATA_DIR}
