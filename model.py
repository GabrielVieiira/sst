import sqlite3

class Database:
    def __init__(self, db_name='dados_sst.db'):
        self.db_name = db_name

    def connect(self):
        try:
            return sqlite3.connect(self.db_name)
        except sqlite3.Error as e:
            print(f'Erro ao conectar ao banco de dados: {e}')
            return None

    def execute_query(self, query, params=None):
        try:
            with self.connect() as conn:
                if conn is None:
                    raise sqlite3.Error('Falha na conexão com o banco de dados.')
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f'Erro ao executar a consulta: {e}')
            return None
        
    def get_cargos(self,):
        query = 'SELECT * FROM cargos'
        try:
            with self.connect() as conn:
                if conn is None:
                    raise sqlite3.Error('Falha na conexão com o banco de dados.')
                cursor = conn.cursor()
                cursor.execute(query)
                response = cursor.fetchall()
                cargos = [(row[0], row[1]) for row in response]
                return cargos
        except sqlite3.Error as e:
            print(f'Erro ao executar a consulta: {e}')
            return None
        
    def get_exame(self,):
        query = 'SELECT * FROM exames'
        try:
            with self.connect() as conn:
                if conn is None:
                    raise sqlite3.Error('Falha na conexão com o banco de dados.')
                cursor = conn.cursor()
                cursor.execute(query)
                response = cursor.fetchall()
                exames = [row[1] for row in response]
                return exames
        except sqlite3.Error as e:
            print(f'Erro ao executar a consulta: {e}')
            return None
        
    def get_epi(self,):
        query = 'SELECT * FROM epis'
        try:
            with self.connect() as conn:
                if conn is None:
                    raise sqlite3.Error('Falha na conexão com o banco de dados.')
                cursor = conn.cursor()
                cursor.execute(query)
                response = cursor.fetchall()
                epis = [row[1] for row in response]
                return epis
        except sqlite3.Error as e:
            print(f'Erro ao executar a consulta: {e}')
            return None
        
    def get_integracao(self,):
        query = 'SELECT * FROM integracoes'
        try:
            with self.connect() as conn:
                if conn is None:
                    raise sqlite3.Error('Falha na conexão com o banco de dados.')
                cursor = conn.cursor()
                cursor.execute(query)
                response = cursor.fetchall()
                integracoes = [row[1] for row in response]
                return integracoes
        except sqlite3.Error as e:
            print(f'Erro ao executar a consulta: {e}')
            return None
        
    def get_exames_por_cargo(self, cargo_id):
        query = '''
        SELECT exame_id FROM cargo_exame WHERE cargo_id = ?
        '''
        try:
            with self.connect() as conn:
                if conn is None:
                    raise sqlite3.Error('Falha na conexão com o banco de dados.')
                cursor = conn.cursor()
                cursor.execute(query, (cargo_id,))
                response = cursor.fetchall()
                exames_ids = [row[0] for row in response]
                return exames_ids
        except sqlite3.Error as e:
            print(f'Erro ao executar a consulta: {e}')
            return None
        
    def get_epis_por_cargo(self, cargo_id):
        query = '''
        SELECT epi_id FROM cargo_epi WHERE cargo_id = ?
        '''
        try:
            with self.connect() as conn:
                if conn is None:
                    raise sqlite3.Error('Falha na conexão com o banco de dados.')
                cursor = conn.cursor()
                cursor.execute(query, (cargo_id,))
                response = cursor.fetchall()
                epis_ids = [row[0] for row in response]
                return epis_ids
        except sqlite3.Error as e:
            print(f'Erro ao executar a consulta: {e}')
            return None
        
    def get_integracoes_por_cargo(self, cargo_id):
        query = '''
        SELECT integracao_id FROM cargo_integracao WHERE cargo_id = ?
        '''
        try:
            with self.connect() as conn:
                if conn is None:
                    raise sqlite3.Error('Falha na conexão com o banco de dados.')
                cursor = conn.cursor()
                cursor.execute(query, (cargo_id,))
                response = cursor.fetchall()
                integracoes_ids = [row[0] for row in response]
                return integracoes_ids
        except sqlite3.Error as e:
            print(f'Erro ao executar a consulta: {e}')
            return None