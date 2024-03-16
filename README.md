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