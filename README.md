# trolog

## Installation

```
git clone https://github.com/jbshep/trolog
cd trolog
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

## Run

`python -m trolog <command>`

## Tests

```
pytest tests
pytest --cov=trolog tests
coverage report -m
```

## Run Checks (Tests and PEP8)

```
./check-all.sh
```

May have to `chmod u+x check-all.sh` first.
