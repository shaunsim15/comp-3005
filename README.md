# fitness_club app

### Virtual Env Setup

https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/
1) On Windows Command Prompt, run:
```
pip install virtualenv
python -m venv 3005-virtual-env
cd 3005-virtual-env   
cd Scripts
activate.bat
```

2) Then, run "pip list" to confirm youre in a new virtual env. Should only show 2 libs:
Package    Version
---------- -------
pip        22.3   
setuptools 65.5.0 

3) WHEN IN VIRTUAL ENV, you can either run "pip install" statements one by one, or more efficiently, run:

pip install -r requirements.txt

4) To generate a requirements.txt based off the current virtualenv, run "pip freeze > requirements.txt"

5) To exit virtual env, run "deactivate"

### How to run Project
1) In PGAdmin, create a database called "fitness_club_project" to match the db_name in `__init__.py`
2) Ensure your postgresql username is "postgres" and password is "56789", to match what is in `__init__.py`
3) Otherwise, follow this [YT Video](https://www.youtube.com/watch?v=GjLR_qnwFUs) and run the following in PGAdmin's QueryTool: `ALTER USER postgres WITH PASSWORD '56789';`
4) Run `python run.py` whilst in the comp-3005 root directory to launch the app (should be running on http://127.0.0.1:5000 or similar)