dicionario = {

    'data':
        {'id': 409935133,
         'timestamp': '1743279246',
         'amount': 0.00059322,
         'amount_str': '0.00059322',
         'price': 82600,
         'price_str': '82600',
         'type': 1,
         'microtimestamp': '1743279246241000',
         'buy_order_id': 1861403571625990,
         'sell_order_id': 1861403736403968
         },

    'channel': 'live_trades_btcusd',
    'event': 'trade'
    }

print(dicionario["data"]["price"])

