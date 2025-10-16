"""
# BINANCE
* Documentation: https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams
* Obs.: Individual Symbol Ticker Streams

# Python
* Websocket-client: pip install websocket-client
* Documentation: https://pypi.org/project/websocket-client/
"""

# Bibliotecas
from time import time
from json import loads
from requests import get
from colorama import Fore
from websocket import WebSocketApp

# Importando arquivo
from authentication import autenticacao

# Classe Binance
class Binance:

    # Construtor
    def __init__(self, url=None):

        self.url = url  # URL da websocket
        self.ws = None  # WebSocket

        # Calculo da SMA
        self.short_window = 15  # Janela curta para o SMA (15 minutos)
        self.long_windows = 60  # Janela longa para o SMA (60 minutos)

        # Lista de preços históricos
        self.prices = []

        # Variáveis de controle
        self.last_trade_time = 0        # Tempo da última negociação
        self.trade_cooldown = 60 * 10   # Intervalo de negociação: 10 minutos
        self.preco_compra = 0           # Preço de compra
        self.preco_venda = 0            # Preço de venda


    # Objeto (String)
    def __str__(self):
        return f"{Fore.LIGHTYELLOW_EX}BinanceCoin{Fore.RESET}"


    # Metodo: Função principal
    def on_message(self, ws, message):

        try:
            # Parsing JSON
            data = loads(message)

            # Caso exista capturar dados
            if data:

                # Dados
                simbolo = data["s"]
                preco_atual = data["c"]

                # Preço atual do ativo
                preco_atual_float = float(preco_atual)
                self.prices.append(preco_atual_float) # Adiciona o preço à lista

                """ Limitar número de preços (evitar uso excessivo de memória) """
                if len(self.prices) > self.long_windows:
                    self.prices.pop(0)

                print(f"\n{Fore.LIGHTWHITE_EX}{simbolo} (preço atual): {preco_atual} USDT{Fore.RESET}")

                """ Lógica: Compra e Venda com base no lucro de 20% """
                if len(self.prices) >= self.short_window:

                    # Curto prazo
                    sma_short = sum(self.prices[-self.short_window:]) / self.short_window

                    # Longo prazo
                    sma_long = sum(self.prices) / len(self.prices)

                    # Condição: Verifica o tempo de CoolDown para negociações
                    current_time = time()
                    if current_time - self.last_trade_time < self.trade_cooldown:

                        print(f"{Fore.LIGHTMAGENTA_EX}Aguardando o tempo para realizar outra negociação{Fore.RESET}")
                        return

                    # Condição (compra): Preço atual abaixo das médias móveis
                    if preco_atual_float < sma_short and preco_atual_float < sma_long:

                        print(f"\n{Fore.LIGHTBLUE_EX}Preço baixo: Comprando BTC{Fore.RESET}")
                        self.comprar_btc(50)  # Aqui você compra BTC com 50 reais

                    # Condição (venda): Preço atual acima das médias móveis e atingir o lucro desejado
                    if self.preco_compra != 0 and preco_atual_float >= self.preco_compra * 1.20:

                        print(f"\n{Fore.LIGHTGREEN_EX}Preço alto: Vendendo BTC com lucro de 20%{Fore.RESET}")
                        self.vender_btc(self.calcular_quantidade_btc())

        except Exception as e:
            print(f"Erro na captura dos dados: {e}")


    # Metodo: Erro na conexão WebSocket
    def on_error(self, ws, error):
        print(f"{Fore.LIGHTRED_EX}Erro na conexão: {error}{Fore.RESET}")


    # Metodo: Conexão WebSocket fechada
    def on_close(self, ws, close_status_code, close_msg):
        print(f"{Fore.LIGHTRED_EX}Conexão encerrada!{Fore.RESET}")


    # Metodo: Conexão WebSocket aberta
    def on_open(self, ws):
        print(f"{Fore.LIGHTBLUE_EX}Conectado a Binance para o par {Fore.LIGHTGREEN_EX}{self.url_formatada()}{Fore.RESET}\n")


    # Metodo: Conexão
    def connect(self):
        self.ws = WebSocketApp(self.url,
                               on_open=self.on_open,
                               on_message=self.on_message,
                               on_error=self.on_error,
                               on_close=self.on_close)

        self.ws.run_forever()


    """"""""""""""""""""""""
    """ MÉTODOS ALICERCE """
    """"""""""""""""""""""""

    # Metodo: Realização da compra de BitCoin
    def comprar_btc(self, valor_reais):

        # Obtem o preço atual do BTC
        preco_btc_usdt = self.obter_preco_btc()

        # Proteção
        if preco_btc_usdt == 0:
            print(f"{Fore.LIGHTRED_EX}Erro ao obter preço do BTC{Fore.RESET}")
            return

        # Converte REAL -> USDT
        cotacao_dolar = self.obter_cotacao_dolar()

        # Proteção
        if cotacao_dolar == 0:
            print(f"{Fore.LIGHTRED_EX}Erro ao obter preço do Dólar{Fore.RESET}")
            return

        # Converter REAL -> DOLAR
        valor_usdt = valor_reais / cotacao_dolar

        # Cálculo da quantidade de BTC que pode ser comprado
        quantidade_btc = valor_usdt / preco_btc_usdt
        print(f"\nComprando {quantidade_btc} BTC por {valor_reais} reais (equivalente a {valor_usdt} USDT)")

        # Condição: Verificação do saldo
        if self.verificar_saldo(ativo="USDT", valor_necessario=valor_reais):

            try:
                ordem = autenticacao().order_market_buy(symbol="BTCUSDT", quantity=quantidade_btc)

                # Atualização do tempo da última negociação
                print(f"{Fore.LIGHTGREEN_EX}Compra realizada: {ordem}{Fore.RESET}")
                self.last_trade_time = time()

                # Armazenar o preço de compra
                self.preco_compra = preco_btc_usdt

            except Exception as e:
                print(f"{Fore.LIGHTRED_EX}Erro ao realizar compra: {e}{Fore.RESET}")

        else:
            print(f"{Fore.LIGHTRED_EX}Saldo insuficiente para realizar a compra{Fore.RESET}")


    # Metodo: Realização da venda de BitCoin
    def vender_btc(self, valor_btc):

        # Condição: Verificação do saldo
        if self.verificar_saldo(ativo="BTC", valor_necessario=valor_btc):

            try:
                ordem = autenticacao().order_market_sell(symbol="BTCUSDT", quantity=valor_btc)

                # Atualização do tempo da última negociação
                print(f"{Fore.LIGHTGREEN_EX}Venda realizada: {ordem}{Fore.RESET}")
                self.last_trade_time = time()

                # Resetando o preço de compra após a venda
                self.preco_compra = 0

            except Exception as e:
                print(f"{Fore.LIGHTRED_EX}Erro ao realizar a venda: {e}{Fore.RESET}")

        else:
            print(f"{Fore.LIGHTRED_EX}Saldo insuficiente de BTC para vender {valor_btc} BTC{Fore.RESET}")


    """"""""""""""""""""""""
    """ MÉTODOS SUPORTE """
    """"""""""""""""""""""""

    # Função: Obter o preço atual do BTC em USDT
    def obter_preco_btc(self):
        try:
            ticker = autenticacao().get_symbol_ticker(symbol="BTCUSDT")
            ticker_fmt = float(ticker)

            return ticker_fmt

        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}Erro ao obter o preço do BTC: {e}{Fore.RESET}")

        return 0


    # Função: Obter a cotação atual do dólar (BRL/USD)
    def obter_cotacao_dolar(self):

        url = "https://v6.exchangerate-api.com/v6/31b0cc8e9ccfec29dfbb56df/latest/USD"

        try:
            resp = get(url)

            if resp:
                file_json = loads(resp.text)

                if file_json:
                    dolar = file_json["conversion_rates"]["BRL"]

                    return dolar

        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}Erro ao obter a cotação do dólar: {e}{Fore.RESET}")

        return 0


    # Função: Verificar saldo na Binance
    def verificar_saldo(self, ativo, valor_necessario):

        try:
            # Saldo disponível
            saldo = autenticacao().get_asset_balance(ativo)
            saldo_disponivel = float(saldo["free"])

            return saldo_disponivel if saldo_disponivel >= valor_necessario else False

        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}Erro ao verificar saldo: {e}{Fore.RESET}")

        return False


    # Função: Calcular quantidade de BTC comprada
    def calcular_quantidade_btc(self):

        saldo_btc = autenticacao().get_asset_balance("BTC")
        return float(saldo_btc["free"])


    # Função: Formatação de URL
    def url_formatada(self):

        url_1 = self.url.split("/")[-1]
        url_2 = url_1.split("@")[0]
        url_fmt = f"{url_2[:3]} - {url_2[3:]}"

        return url_fmt