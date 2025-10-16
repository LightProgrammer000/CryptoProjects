"""
# BINANCE
* Documentation: https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams
* Obs.: Individual Symbol Ticker Streams

# Python
* Websocket-client: pip install websocket-client
* Documentation: https://pypi.org/project/websocket-client/

# Moedas
* BTCUSDT:  Bitcoin (BTC) / Tether (USDT)
* ETHUSDT:  Ethereum (ETH) / Tether (USDT)
* BNBUSDT:  Binance Coin (BNB) / Tether (USDT)
* XRPUSDT:  Ripple (XRP) / Tether (USDT)
* ADAUSDT:  Cardano (ADA) / Tether (USDT)
* SOLUSDT:  Solana (SOL) / Tether (USDT)
* DOGEUSDT: Dogecoin (DOGE) / Tether (USDT)
* USDCUSDT: USD Coin (USDC) / Tether (USDT)
"""

# Bibliotecas
import rel
from json import loads
from colorama import Fore
from websocket import WebSocketApp

# Classe
class Binance:

    # Construtor
    def __init__(self, url=None):

        self.url = url
        self.ws= None


    #  Objeto (String)
    def __str__(self):
        return f"{Fore.LIGHTGREEN_EX}Binance Crypto{Fore.RESET}"


    # Funcao: Abertura de conectado
    def on_open(self, ws):
        print(f"{Fore.LIGHTBLUE_EX}Conectado: {Fore.RESET}{self.suporte_url()}{Fore.RESET}")


    # Funcao: Conexao encerrada
    def on_close(self, ws, close_status_code, close_msg):
        print(f"{Fore.LIGHTYELLOW_EX}Conexao fechada para {self.suporte_url()}{Fore.RESET}")


    # Funcao: Erro de conexao
    def on_error(self, ws, error):
        print(f"{Fore.LIGHTRED_EX}Erro {error}na conexao para {self.suporte_url()}{Fore.RESET}")


    # Funcao: Parte principal do programa
    def on_message(self, ws, message):

        try:

            if message:
                data = loads(message)

                # Par Moeda
                par_1 = data["s"][0:-4]
                par_2 = data["s"][-4:]

                # Preco
                pre_atu = data["c"]
                pre_fec = data["p"]

                # Tempo
                max_24h = data["h"]
                min_24h = data["l"]
                vol_24h = data["v"]

                print(f"\n{Fore.LIGHTRED_EX}Atualizacao {Fore.RESET}")
                print(f"{Fore.LIGHTGREEN_EX}Par da Moeda {par_1} <-> {par_2} {Fore.RESET}")
                print(f"{Fore.LIGHTBLUE_EX}Preco Atual: {pre_atu} USDT{Fore.RESET}")
                print(f"{Fore.LIGHTYELLOW_EX}Preco de fechamento anterior: {pre_fec} USDT{Fore.RESET}")
                print(f"{Fore.LIGHTMAGENTA_EX}24h Maximo: {max_24h} USDT{Fore.RESET}")
                print(f"{Fore.LIGHTMAGENTA_EX}24h Minimo: {min_24h} USDT{Fore.RESET}")
                print(f"{Fore.LIGHTMAGENTA_EX}Volume de 24h: {vol_24h} unidades{Fore.RESET}\n")

        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}Erro ao processar os dados {e}{Fore.RESET}")


    # Conexao
    def connect(self):

        print(f"{Fore.LIGHTCYAN_EX}Iniciando conexao...{Fore.RESET}")

        try:
            self.ws = WebSocketApp(self.url,
                                   on_open=self.on_open,
                                   on_message=self.on_message,
                                   on_error=self.on_error,
                                   on_close=self.on_close)

            # Abertura infinita de conexao
            self.ws.run_forever()

            """
            self.ws.run_forever(dispatcher=rel, reconnect=5)
            rel.signal(2, rel.abort)
            rel.dispatch()
            """

        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}Erro ao se conectar {e}{Fore.RESET}")


    # Funcao: Formatacao de URL
    def suporte_url(self):

        url_1 = self.url.split("/")[-1]
        url_2 = url_1.split("@")[0]
        url_fmt = f"{url_2[:3]} - {url_2[3:]}"

        return url_fmt