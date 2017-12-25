#!flask/bin/python
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import pyodbc
import DataHandler
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/projects/', methods=['POST', 'GET'])
def projects():
    if request.method == 'GET':
        projects_html = dh.renderAllProjectHtml()
        return render_template('index.html', tr=projects_html)


@app.route('/projects/addproject', methods=['GET', 'POST', 'UPDATE'])
def addProject():
    if request.method == 'GET':
        return render_template('addproject.html')
    elif request.method == 'POST':
        dh.addProject(request.form['project-name'],request.form['project-description'],request.form['project-progress'],request.form['checkpoints'])
        return redirect(url_for('projects'))

@app.route('/projects/<string:project_id>')
def project(project_id):
    project_html = dh.displayProjectHtml(project_id)
    project_name = dh.getNameFromId(project_id)
    return render_template('project.html', project=project_html, name=project_name)


if __name__ == '__main__':
    connection = pyodbc.connect('Trusted_Connection=yes', driver='{SQL Server}', server='PATRICKS-XPS',
                                database='Website')
    dh = DataHandler.DataHandler(connection)
    app.run(host='localhost', port=80, debug=True)
