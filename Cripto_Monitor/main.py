# Bibliotecas
from time import sleep
from json import loads
from requests import get
from colorama import Fore


# Função: Requisicao a API.
def requisicao(url):

    try:
        resp = get(url)
        if resp.status_code == 200:
            return resp.text

        else:
            print(f"{Fore.LIGHTRED_EX}Erro: API não respondeu corretamente!{Fore.RESET}")

    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}Erro na requisição: {e}{Fore.RESET}")

    return None


# Função: Faz o parsing_Json
def parsing_json(resp_html):

    try:
        if resp_html:
            return loads(resp_html)

    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}Erro no Parsing Json: {e}{Fore.RESET}")

    return None


# Função: Organiza os dados da API em dicionário.
def captura_dados(file_json):

    dicionario = dict()

    try:
        if file_json:

            for i in file_json:

                moeda = i["name"]
                preco = i["current_price"]
                dicionario[preco] = moeda

            return dicionario

    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}Erro: {e}{Fore.RESET}")

    return None


# Função: Exibe os dados das criptomoedas
def exibir_dados(dicionario):

    cont = 0
    print(f"{Fore.LIGHTBLUE_EX}{'=-=' * 10} Crypto Moedas {'=-=' * 10}{Fore.RESET}\n")

    for i, j in sorted(dicionario.items(), reverse=True):

        if cont < 3:
            print(f"{Fore.LIGHTGREEN_EX}Moeda: {j}{Fore.RESET}")
            print(f"{Fore.LIGHTYELLOW_EX}Valor: $ {float(i):.2f}{Fore.RESET}\n")
            cont += 1

        # Condicao: Atualiza a cada 3 segundos
        if cont == 3:
            cont = 0
            sleep(3)


# Função para exibir o relatório de dados
def relatorio(url):

    try:
        resp_html = requisicao(url)

        if resp_html:
            file_json = parsing_json(resp_html)

            if file_json:
                dados = captura_dados(file_json)

                if dados:
                    exibir_dados(dados)

    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}Erro na exibição do relatório: {e}{Fore.RESET}")


# Função principal que inicia a execução do programa.
def main():

    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"

    try:
        relatorio(url)

    except KeyboardInterrupt:
        print(f"{Fore.LIGHTCYAN_EX}Execução interrompida pelo usuário!{Fore.RESET}")
        exit(0)

    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}Erro na execução! {e}{Fore.RESET}")


# Execução
if __name__ == '__main__':
    main()