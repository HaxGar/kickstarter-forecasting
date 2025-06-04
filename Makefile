include .env

DATA_DIR=${ROOT}/data
DL_URL=https://files.slack.com/files-pri/T02NE0241-

reset_data_files:
	rm -rf ${DATA_DIR}
	mkdir ${DATA_DIR}
	mkdir ${DATA_DIR}/raw
	mkdir ${DATA_DIR}/processed
	mkdir ${DATA_DIR}/processed/par_commentaire
	mkdir ${DATA_DIR}/processed/par_projet

	-curl ${DL_URL}F09081835UG/download/ks-projects-201801.csv?pub_secret=4522e433b2 > ${DATA_DIR}/raw/ks-projects-201801.csv
	-curl ${DL_URL}F08UWDGPP37/download/comments_clean.csv?pub_secret=fedb7864a9 > ${DATA_DIR}/raw/comments_clean.csv

reset_processed_data_files:
	rm -rf ${DATA_DIR}/processed
	mkdir ${DATA_DIR}/processed
	mkdir ${DATA_DIR}/processed/par_commentaire
	mkdir ${DATA_DIR}/processed/par_projet

test :
	@echo ${DATA_DIR}
