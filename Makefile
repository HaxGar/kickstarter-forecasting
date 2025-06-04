GIT_USER = 'HaxGar'
PROJECT_NAME = 'kickstarter-forecasting'
DATA_DIR=~/code/${GIT_USER}/${PROJECT_NAME}/data
KAGGLE_URL=https://www.kaggle.com/datasets/kemical/kickstarter-projects/

reset_data_files:
	rm -rf ${DATA_DIR}
	mkdir ${DATA_DIR}
	mkdir ${DATA_DIR}/raw
	mkdir ${DATA_DIR}/processed
	mkdir ${DATA_DIR}/processed/par_commentaire
	mkdir ${DATA_DIR}/processed/ligne_par_projet

	-curl ${KAGGLE_URL}data?select=ks-projects-201801.csv > ${DATA_DIR}/raw/ks-projects-201801.csv
	-curl ${KAGGLE_URL}data?select=Comentarios.csv > ${DATA_DIR}/raw/comments_clean.csv
