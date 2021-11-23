# metis-ai-services

## Local Development Setup

1. install python

2. clone or download the repo

3. install virtualenvwrapper

```bash
pip3 install virtualenvwrapper;
...
export WORKON_HOME=~/Envs
mkdir -p $WORKON_HOME
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv metisaiapi
```

4. install project packages

```bash
pip3 install -e
pip3 install -e .[dev]
```

5. run the server

```bash
flask run
```
