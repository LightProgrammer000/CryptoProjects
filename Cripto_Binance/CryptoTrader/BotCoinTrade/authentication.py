# Bibliotecas
from os import getenv
from dotenv import load_dotenv
from binance.client import Client


# Funcao: Autenticacao e credenciamento
def autenticacao():

    # Carregar as variaveis de ambiente
    load_dotenv()

    # Credenciaia
    API_KEY = getenv("API_KEY")
    API_SECRET = getenv("API_SECRET")

    # Credenciais
    credenciamento = Client(API_KEY, API_SECRET)

    return credenciamento