# fitness_club app

### 0. Cloning the repo

1) Run `git clone https://github.com/shaunsim15/comp-3005.git` in your terminal and cd into the project root directory

### 1. Virtual Env Setup (Optional, but recommended)
<details>
<summary>
Click to view detailed instructions
</summary>

The below instructions are Windows-specific and based on guidance from [FreeCodeCamp](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/). Similar instructions for different OSes can be found on their website.


1) In Windows Command Prompt, navigate to the root directory of the project folder, and run these commands, one at a time:
```
pip install virtualenv
python -m venv 3005-virtual-env
cd 3005-virtual-env   
cd Scripts
activate.bat
```

2) Then, run "pip list" to confirm you're in a new virtual environment. There should only be 2 libraries that are part of this virtual environment:

```
Package    Version
---------- -------
pip        22.3   
setuptools 65.5.0 

```
3) Once you're in the virtual environment, run:

`pip install -r requirements.txt`

4) If you want to regenerate a `requirements.txt` after having installed more libraries in the current virtual environment, you can run "pip freeze > requirements.txt".

5) To exit the virtual environment, run "deactivate" in the Command line

</details>

### 2. How to run Project

1) In PGAdmin, create a database called "fitness_club_project" to match the db_name in `__init__.py`
![image](https://github.com/shaunsim15/comp-3005/assets/61551217/f5531693-f68e-49f8-be87-c59b9a3ff8b2)
![image](https://github.com/shaunsim15/comp-3005/assets/61551217/30a6615b-8fbf-4e41-bcc3-fd9c69dfdeeb)


2) Ensure your postgresql username is "postgres" and password is "56789", to match what is in `__init__.py`. Alternatively, edit [these lines](https://github.com/shaunsim15/comp-3005/blob/main/fitness_club/__init__.py#L21-L22) of `__init__.py` to match your postgres username and password.
3) To change your postgres password, follow this [Youtube Video](https://www.youtube.com/watch?v=GjLR_qnwFUs) and run the following in PGAdmin's QueryTool: `ALTER USER postgres WITH PASSWORD '56789';`. 
4) If you haven't already done so when setting up the virtual environment, run `pip install -r requirements.txt` to install all dependencies. If you're getting errors at this stage and didn't set up a virtual environment, try setting up a virtual environment
5) Run `python run.py` whilst in the comp-3005 root directory to launch the app (should be running on http://127.0.0.1:5000 or similar)

### 3. Locations of key project deliverables

- The Report can be found [here](https://github.com/shaunsim15/comp-3005/blob/main/Team_2_fitness_club_project_report.pdf)
- The ERD can be found [here](https://github.com/shaunsim15/comp-3005/blob/main/Team_2_ERD.pdf)
- The Schema can be found [here](https://github.com/shaunsim15/comp-3005/blob/main/Team_2_Schema.pdf)
- The DDL and DML can be found [here](https://github.com/shaunsim15/comp-3005/tree/main/fitness_club/SQL)
- The demo video can be found [here](https://youtu.be/J2ayfwEC7Hw?si=ehkjzXtGyfjGzpF_)
