import pyodbc


class BD:

    def __init__(self, server, user, senha, nomebd):
        self.nomebd = nomebd
        self.server = server
        self.user = user
        self.senha = senha
        self.nomebd = nomebd
        conne = pyodbc.connect('DRIVER={};SERVER={};PORT=1433;DATABASE={};'
                               'UID={};PWD={}'.format('ODBC Driver 13 for SQL Server', server, nomebd, user, senha))
        self.con = conne
        self.cursor = conne.cursor()
        print("confirme")





