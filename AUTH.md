## First run from venv

```commandline
cd flask_auth_app
python3 -m venv auth
source auth/bin/activate

pip install flask flask-sqlalchemy flask-login

export FLASK_APP=project
export FLASK_DEBUG=1

flask run
```

## Usual run

```commandline
cd flask_auth_app
source auth/bin/activate

export FLASK_APP=project
export FLASK_DEBUG=1

flask run
```

## Addition info

Using the ConfigMap within Python/Flask:

https://www.oreilly.com/library/view/kubernetes-for-developers/9781788834759/6e3697a3-8185-4004-9893-57c2dcfab0a7.xhtml
