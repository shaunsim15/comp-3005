from fitness_club import create_app # import create_app function from __init__.py. We put __init__.py inside of fitness_club folder to make fitness_club a python package

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) # This lets you run a flask application. debug=True means webserver will be automatically rerun whenever we change any of our python code
