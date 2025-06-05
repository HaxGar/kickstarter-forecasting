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

preprocess_all_versions:
	python -c 'from kickstarter_predictor.data import load_data; load_data(True,True,True,True)'
	python -c 'from kickstarter_predictor.data import load_data; load_data(True,False,True,True)'
	python -c 'from kickstarter_predictor.data import load_data; load_data(True,False,False,True)'
	python -c 'from kickstarter_predictor.data import load_data; load_data(True,False,False,False)'
	python -c 'from kickstarter_predictor.data import load_data; load_data(True,False,True,False)'
	python -c 'from kickstarter_predictor.data import load_data; load_data(True,True,False,True)'
	python -c 'from kickstarter_predictor.data import load_data; load_data(True,True,False,False)'
	python -c 'from kickstarter_predictor.data import load_data; load_data(True,True,True,False)'

	python -c 'from kickstarter_predictor.data import load_data; load_data(False,True,True,True)'
	python -c 'from kickstarter_predictor.data import load_data; load_data(False,False,True,True)'
	python -c 'from kickstarter_predictor.data import load_data; load_data(False,False,False,True)'
	python -c 'from kickstarter_predictor.data import load_data; load_data(False,False,False,False)'
	python -c 'from kickstarter_predictor.data import load_data; load_data(False,False,True,False)'
	python -c 'from kickstarter_predictor.data import load_data; load_data(False,True,False,True)'
	python -c 'from kickstarter_predictor.data import load_data; load_data(False,True,False,False)'
	python -c 'from kickstarter_predictor.data import load_data; load_data(False,True,True,False)'

install:
	pip install -e .

test:
	@echo ${DATA_DIR}
