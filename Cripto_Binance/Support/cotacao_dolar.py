# Bibliotecas
from json import loads      # Para manipular JSON
from requests import get    # Para fazer requisição HTTP
from colorama import Fore   # Para colorir a saída no terminal

# Função: Realizar a requisição à API
def requisicao():

    url = "https://v6.exchangerate-api.com/v6/31b0cc8e9ccfec29dfbb56df/latest/USD"

    try:
        response = get(url)
        if response:
            return response.text

    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}Erro na requisicao: {e}{Fore.RESET}")

    return None


# Função: Fazer parsing do HTML para JSON
def parsing_html(rep_html):

    try:
        # Converte o HTML para JSON
        return loads(rep_html)

    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}Erro no parsing HTML: {e}{Fore.RESET}")

    return None


# Função: Obter cotação BRL -> USD
def brl_usd():

    try:
        resp = requisicao()

        if resp:
            file_json = parsing_html(resp)

            if file_json:
                dolar_real = float(file_json["conversion_rates"]["BRL"])
                print(f"{Fore.LIGHTBLUE_EX}1 Dolar : {Fore.LIGHTYELLOW_EX}R$ {dolar_real:.2f} reais {Fore.RESET}")

    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}Erro ao obter cotacao do dolar {Fore.RESET}: {e}")


# Função: Exibir todas as cotações
def cotacoes():

    try:
        resp = requisicao()  # Realiza requisição

        if resp:
            file_json = parsing_html(resp)  # Faz o parsing do HTML

            if file_json:
                for moeda, valor in file_json["conversion_rates"].items():
                    print(f"{Fore.LIGHTGREEN_EX}1 Dolar vale: {Fore.LIGHTYELLOW_EX}{valor} {moeda}{Fore.RESET}")

    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}Erro ao obter cotacao do dolar {Fore.RESET}: {e}")


# Função principal: Exibe o menu e controla o fluxo do programa
def main():

    while True:
        try:
            print(f"\n{Fore.LIGHTBLUE_EX}------ MENU ------{Fore.RESET}")
            print(f"{Fore.LIGHTGREEN_EX}# [1] Cotacoes{Fore.RESET}")
            print(f"{Fore.LIGHTCYAN_EX}# [2] BRL -> USD{Fore.RESET}")
            opc = int(input(f"\n{Fore.LIGHTYELLOW_EX}Opc: {Fore.RESET}"))
            print("")

            if opc == 1:

                # Exibe cotações
                cotacoes()

            elif opc == 2:

                # Exibe cotação BRL -> USD
                brl_usd()

            else:
                print("\nOpcao Invalida !")

        except KeyboardInterrupt:
            print("\nPrograma finalizado !")
            exit(0)

        except Exception as e:
            print(f"\nErro inesperado: {e}")


# Execução principal
if __name__ == '__main__':
    main()
