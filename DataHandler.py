import pyodbc
import uuid
import datetime

class DataHandler:

    def __init__(self, conn):
        self.dbconn = conn
        self.projects_dict = {}


    def renderAllProjectHtml(self):
        html = ''
        cur = self.dbconn.cursor()
        cur.execute('select * from PROJECT')
        tbl = cur.fetchall()
        for x in tbl:
            project_date = self.formatDate(x[2])
            self.projects_dict[x[1]] = [project_date, str(x[3]), x[0]]
        for key in self.projects_dict.keys():
            html += '<tr class=\"project\">' + \
                    self.createProjectNameAndDateColumnHtml(key, self.projects_dict[key][0], self.projects_dict[key][2])  + \
                    self.createProjectProgressAndInfoHtml(self.projects_dict[key][1], self.projects_dict[key][2]) + \
                    self.createProjectEditLinkHtml(self.projects_dict[key][2]) + '</tr>'
                    #self.createProjectDataHtml(self.projects_dict[key][2], cur)

        return html

    def addProject(self, name, description, progress, checkpoints):
        cur = self.dbconn.cursor()
        query = "insert into dbo.PROJECT(ID, NAME, DT_CREATED, PROGRESS) VALUES (?,?,?,?)"
        cur.execute(query,  uuid.uuid4(), name, datetime.datetime.now(), progress)
        self.dbconn.commit()

    def displayProjectHtml(self, id):
        cur = self.dbconn.cursor()
        cur.execute('select * from PROJECT WHERE ID = ?',id)
        proj = cur.fetchone()
        html = '<form action=\"{{ url_for(\'updateProject\') }}\" method=\"POST\"><label>Project Name:</label> \
               <input name="project-name" value=\"{}\"><br /><label>Project Description:</label> \
               <input name=\"project-description\" value=\"\"> <br /><label>Project Progess:</label><input name = \
               \"project-progress\" value=\"{}\"><br /><label>Project Checkpoints:</label><textarea \
               name=\"checkpoints\"></textarea> <br /><button type=\"submit\">Save</button></form>'.format(proj[1],str(proj[3]))
        return html

    def getNameFromId(self, id):
        cur = self.dbconn.cursor()
        cur.execute('select * from PROJECT WHERE ID = ?', id)
        proj = cur.fetchone()
        return proj[1]

    def formatDate(self, date):
        return date.strftime('%Y-%m-%d')

    def createProjectNameAndDateColumnHtml(self, name, date, id):
        html = '<td class=\"name-date\"><a class=\"project-name\" href=\"/projects/' + id + '\">' + name + '<a><br />'
        html += '<label class=\"project-date\">Date Created: </label><a class=\"project-date\">' + date + '</a><br />'
        html+= '<label class=\"project-date\">Projected Completion: </label><a class=\"project-date\">' + date + '</a></td>'
        return html

    def createProjectProgressAndInfoHtml(self, progress, id):
        html = '<td class=\"progess\">'
        html += '<div class=\"progress-value\">' + progress + '</div>'
        cur = self.dbconn.cursor()
        cur.execute('SELECT * FROM dbo.[CHECKPOINT] WHERE PROJECT_ID = ?', id)
        checkpoints = cur.fetchall()
        count = len(checkpoints)
        for checkpoint in checkpoints:
            html += '<div class=\"vl\" style=\"left:' + str(checkpoint[3]) +'%;top:' + str(count*2.5) + 'em\"></div>'
            count -= 1
        html += '<progress value=\"' + progress + '\" max=\"100\"></progress>'
        html += '<br />'
        html += '<ul>'
        html += '<li>Goals: </li>'
        html += '<li>Design Notes: </li>'
        html += '<li>Reference Material: </li>'
        html += '<li>Materials: </li>'
        html += '<li>etc... </li>'
        html += '</ul>'
        html += '</td>'
        return html

    def createProjectEditLinkHtml(self, id):
        return '<td class=\"edit\"> <a href=\"/projects/' + id + '\">Edit</a></td>'

    def createProjectDataHtml(self, id, cur):
        cur = self.dbconn.cursor()
        cur.execute('SELECT * FROM dbo.[CHECKPOINT] WHERE PROJECT_ID = ?', id)
        checkpoints = cur.fetchall()
        html = '<tr class=\"info-row\" colspan=\"4\">'
        html += '<td class=\"project-description\" colspan=\"2\"><p> Description of Project </p></td>'
        html += '<td class=\"project-checkpoints\" colspan=\"2\"><p>'
        for checkpoint in checkpoints:
            html += checkpoint[1] + ': ' + str(checkpoint[3]) + '\\n'
        html += '</p></td>'
        return html