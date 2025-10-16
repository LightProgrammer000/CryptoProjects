from time import time

url = "wss://stream.binance.com:9443/ws/btcusdt@ticker"
url_1 = url.split("/")[-1]
url_2 = url_1.split("@")[0]
final = f"{url_2[:3]} - {url_2[3:]}"

print(final)
print(time())