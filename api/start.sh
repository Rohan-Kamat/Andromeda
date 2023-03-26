rm -rf dist/

python setup.py bdist_wheel

cd dist
pip install andromeda_api-0.0.0-py3-none-any.whl
cd ..

waitress-serve --call 'api:run'
