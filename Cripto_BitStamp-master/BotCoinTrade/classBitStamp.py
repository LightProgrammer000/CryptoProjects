# Bibliotecas
from json import loads
from colorama import Fore
from websocket import WebSocketApp
from authentication import autenticacao

# Classe
class BitStamp:

    # Construtor
    def __init__(self, url):

        self.url = url
        self.ws = None

        # Autenticação com as credenciais
        self.auth = autenticacao()


    # Objeto (String)
    def __str__(self):
        return f"{Fore.LIGHTYELLOW_EX}BitCoin{Fore.RESET}"


    # Metodo: Parte principal do programa
    def on_message(self, ws, message):

        try:
            data = loads(message)

            if data:

                # Extracao dos dados
                preco = data["data"]["price"]
                preco_float = float(preco)

                print(f"\n{Fore.LIGHTWHITE_EX}{self} (preço): {preco} USDT{Fore.RESET}")

                # Condicao: Logica para comprar e vender BTC
                if preco_float > 10_000:

                    # Exemplo: Vender 0 BTC (ajuste conforme necessário)
                    self.vender(0)

                elif preco_float < 8_100:

                    # Exemplo: Comprar 0.01 BTC (ajuste conforme necessário)
                    self.comprar(0)

        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}Erro ao processar compra/venda: {e}{Fore.RESET}")


    # Metodo: Erro de conexao
    def on_error(self, ws, error):
        print(f"{Fore.LIGHTRED_EX}Erro na conexão: {error}{Fore.RESET}")


    # Metodo: Conexao fechada
    def on_close(self, ws, close_status_code, close_msg):
        print(f"{Fore.LIGHTYELLOW_EX}Conexão fechada!{Fore.RESET}")


    # Metodo: Conexao aberta
    def on_open(self, ws):
        print(f"{Fore.LIGHTBLUE_EX}Conexão iniciada!{Fore.RESET}")

        # Assinando o canal de live trades para BTC/USD
        live_trades_btcusd = """
        {
            "event": "bts:subscribe",
            "data": {
                "channel": "live_trades_btcusd"
            }
        }
        """

        # Enviando dados com o WebSocket
        self.ws.send(live_trades_btcusd)


    # Metodo: Conexao
    def connect(self):

        self.ws = WebSocketApp(self.url,
                               on_open=self.on_open,
                               on_message=self.on_message,
                               on_error=self.on_error,
                               on_close=self.on_close)
        self.ws.run_forever()


    """"""""""""""""""""""""
    """ METODOS SUPORTE """
    """"""""""""""""""""""""

    # Metodo: Comprar BTC mediante quantidade estabelecida
    def comprar(self, quantidade):

        try:
            if quantidade <= 0:
                print(f"{Fore.LIGHTRED_EX}Quantidade inválida para comprar!{Fore.RESET}")
                return

            print(f"{Fore.LIGHTBLUE_EX}Comprando {quantidade} BTC...{Fore.RESET}")

            # Chama a API para realizar a compra de mercado
            self.auth.buy_market_order(quantity=quantidade)
            print(f"{Fore.LIGHTGREEN_EX}Compra realizada com sucesso!{Fore.RESET}")

        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}Erro ao tentar comprar: {e}{Fore.RESET}")


    # Metodo: Vender BTC mediante quantidade estabelecida
    def vender(self, quantidade):

        try:
            if quantidade <= 0:
                print(f"{Fore.LIGHTRED_EX}Quantidade inválida para vender!{Fore.RESET}")
                return

            print(f"{Fore.LIGHTCYAN_EX}Vendendo {quantidade} BTC...{Fore.RESET}")

            # Chama a API para realizar a venda de mercado
            self.auth.sell_market_order(quantity=quantidade)
            print(f"{Fore.LIGHTGREEN_EX}Venda realizada com sucesso!{Fore.RESET}")

        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}Erro ao tentar vender: {e}{Fore.RESET}")