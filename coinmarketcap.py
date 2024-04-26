from coinmarketcapapi import CoinMarketCapAPI
import config


class Crypto:
    api_key = config.crypto_token

    def get_price(self, sym):
        #sym = 'BTC'

        cmc = CoinMarketCapAPI(self.api_key)
        rep = cmc.cryptocurrency_quotes_latest(symbol=sym)
        #print(rep.data[sym][0]['quote']['USD']['price'])
        return rep.data[sym][0]['quote']['USD']['price']


if __name__ == '__main__':
    #print(rep.data[sym][0]['tags'])
    print(Crypto().get_price('BTC'))
