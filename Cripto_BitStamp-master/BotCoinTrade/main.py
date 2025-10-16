# Bibliotecas
import time
from threading import Thread
from classBitStamp import BitStamp

# Importando arquivo
from authentication import autenticacao


# Metodo: Conexão
def conexao(url):

    crypto = BitStamp(url)
    crypto.connect()

# Metodo: Principal
def main():

    try:
        url = "wss://ws.bitstamp.net"

        t = Thread(target=conexao, args=(url,))
        t.start()

    except KeyboardInterrupt:
        print("\nInterrupcao do programa detectada. Encerrando...")
        exit(0)

    except Exception as e:
        print(f"Erro inesperado: {e}")


# Execução
if __name__ == '__main__':
    main()
