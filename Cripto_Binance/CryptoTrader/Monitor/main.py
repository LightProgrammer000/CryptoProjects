# Bibliotecas
from threading import Thread

# Importando a classe
from class_Binance import Binance

# Conexao
def conexao(url):

    try:
        a = Binance(url)
        a.connect()

    except Exception as e:
        print(f"Conexao nao completada: {e}")


# Funcao: Principal
def main():

    # Lista de Threads
    lista_threads = list()

    try:
        ws_urls = [
            "wss://stream.binance.com:9443/ws/btcusdt@ticker",  # BTC/USDT
            "wss://stream.binance.com:9443/ws/ethusdt@ticker",  # ETH/USDT
            "wss://stream.binance.com:9443/ws/xrpusdt@ticker",  # XRP/USDT
            "wss://stream.binance.com:9443/ws/adausdt@ticker",  # ADA/USDT
            "wss://stream.binance.com:9443/ws/solusdt@ticker",  # SOL/USDT
            "wss://stream.binance.com:9443/ws/dogeusdt@ticker"  # DOGE/USDT
        ]

        for i in ws_urls:
            t = Thread(target=conexao, args=(i, ))
            lista_threads.append(t)

        for i in lista_threads:
            i.start()

        for i in lista_threads:
            i.join()

    except KeyboardInterrupt:
        exit(0)

    except Exception as e:
        print(f"Erro inesperado: {e}")


# Execucao
if __name__ == '__main__':
    main()