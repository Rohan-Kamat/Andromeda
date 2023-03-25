source ../venv/bin/activate

python src/andromeda/main.py flush
python src/andromeda/main.py start --n_crawler=4 --n_parser=4
