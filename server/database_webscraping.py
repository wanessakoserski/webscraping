from server.connection import ServerConnection

class WebscrapingDatabase:
    def __init__(self):
        self.server = ServerConnection('Webscraping')

    
    def create_teste_table(self):
        if not self.server.check_table_exists('Teste'):
            self.server.create_table('Teste', 'ID INT PRIMARY KEY, Nome NVARCHAR(100), Idade INT, Endereco NVARCHAR(255)')
            self.server.insert('Teste', 'ID, Nome, Idade, Endereco', '1, "Nome", 20, "Endereco"')
        else:
            self.server.insert('Teste', 'ID, Nome, Idade, Endereco', "1, 'Nome', 20, 'Endereco'")