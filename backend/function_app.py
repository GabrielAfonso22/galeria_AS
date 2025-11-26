import logging
import os
import json
import azure.functions as func
import pyodbc 

# Cria a instância da Function App
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Define o endpoint HTTP
@app.route(route="GetObrasFunction", auth_level=func.AuthLevel.ANONYMOUS)
def GetObrasFunction(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # 1. Tenta obter a string de conexão da variável de ambiente
    try:
        # A chave de ambiente está em 'Values' no local.settings.json
        connection_string = os.environ["DbConnectionString"]
    except KeyError:
        return func.HttpResponse(
             "DbConnectionString não configurada. Verifique App Settings no Azure ou local.settings.json",
             status_code=500
        )

    obras = []
    conn = None 
    cursor = None
    try:
        # 2. Conectar ao DB (Azure SQL)
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        
        # 3. Executar a Query
        query = "SELECT Nome, Artista, Descricao, URLImagem FROM Obras;"
        cursor.execute(query)
        
        # 4. Formatar o Resultado para JSON
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            obra = dict(zip(columns, row))
            # Tratamento de string 
            for key, value in obra.items():
                if isinstance(value, str):
                    obra[key] = value.strip()
            obras.append(obra)

    except pyodbc.Error as ex:
        logging.error(f"Erro do pyodbc/SQL Server: {ex}")
        # Em caso de erro de DB, retorna o erro
        return func.HttpResponse(
             f"Erro interno do servidor ao carregar dados do SQL: {ex}",
             status_code=500
        )
    finally:
        # 5. Fechar conexões (muito importante!)
        if cursor: cursor.close()
        if conn: conn.close()

    # 6. Retornar JSON com cabeçalhos CORS
    headers = {
        "Content-type": "application/json",
        "Access-Control-Allow-Origin": "*", # Permite que o frontend acesse.
        "Access-Control-Allow-Methods": "GET",
        "Access-Control-Allow-Headers": "Content-Type"
    }

    return func.HttpResponse(
        json.dumps(obras, ensure_ascii=False),
        mimetype="application/json",
        status_code=200,
        headers=headers
    )