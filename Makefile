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

install:
	pip install -e .

test:
	@echo ${DATA_DIR}
