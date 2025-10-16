# Bibliotecas
from os import getenv
from dotenv import load_dotenv
from bitstamp.client import Trading

def autenticacao():

    # Carregar as variaveis de ambiente
    load_dotenv()

    # Crendenciais
    USERNAME = getenv("USERNAME")
    KEY = getenv("KEY")
    SECRET = getenv("SECRET")

    # Montando autenticacao
    credencial = Trading(USERNAME, KEY, SECRET)

    return credencial
