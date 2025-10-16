# Bibliotecas
from colorama import Fore
from threading import Thread

# Importacao de arquivo
from classBinance import Binance


# Funcao: Conexao
def conexao(url):

    try:
        crypto = Binance(url)
        crypto.connect()

    except KeyboardInterrupt:
        exit(0)

    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}Erro na conexao: {e}{Fore.RESET}")


# Funcao: Principal
def main():

    try:
        url = "wss://stream.binance.com:9443/ws/btcusdt@ticker"

        for i in range(1):
            t = Thread(target=conexao, args=(url, ))
            t.start()

    except KeyboardInterrupt:
        exit(0)

    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}Erro na conexao: {e}{Fore.RESET}")


# Execucao
if __name__ == '__main__':
    main()