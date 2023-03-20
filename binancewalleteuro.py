# Import the Client class from the binance.client module to interact with the Binance API
from binance.client import Client


def get_account_balances():
	
	# Create a new client object to interact with the Binance API
	client = Client("<<your_binance_api_key>>", "<<your_binance_secret_key>>")

	# Retrieve the balances of all coins in the user's Binance account
	account_balances = client.get_account()['balances']

	# Get the current price of all tickers from the Binance API
	ticker_info = client.get_all_tickers()

	# Create a dictionary of tickers and their corresponding prices
	ticker_prices = {ticker['symbol']: float(ticker['price']) for ticker in ticker_info}

	# Calculate the USDT value of each coin in the user's account
	coin_values = []
	for coin_balance in account_balances:
		# Get the coin symbol and the free and locked balance of each coin
		coin_symbol = coin_balance['asset']
		unlocked_balance = float(coin_balance['free'])
		locked_balance = float(coin_balance['locked'])

		# If the coin is USDT and the total balance is greater than 1, add it to the list of coins with their EURO values
		if coin_symbol == 'USDT' and unlocked_balance + locked_balance > 1:
			# Calculate EURO value using EURUSDT coin pair
			coin_values.append(('USDT', (unlocked_balance + locked_balance)/ticker_prices.get('EURUSDT')))
		# Otherwise, check if the coin has a USDT trading pair or a BTC trading pair
		elif unlocked_balance + locked_balance > 0.0:
			# Check if the coin has a USDT trading pair
			if (any(coin_symbol + 'USDT' in i for i in ticker_prices)):
				# If it does, calculate its USDT value and add it to the list of coins with their EURO values
				ticker_symbol = coin_symbol + 'USDT'
				ticker_price = ticker_prices.get(ticker_symbol)
				coin_usdt_value = (unlocked_balance + locked_balance) * ticker_price
				if coin_usdt_value > 1:
					# Calculate EURO value using EURUSDT coin pair
					coin_values.append((coin_symbol, coin_usdt_value/ticker_prices.get('EURUSDT')))
			# If the coin does not have a USDT trading pair, check if it has a BTC trading pair
			elif (any(coin_symbol + 'BTC' in i for i in ticker_prices)):
				# If it does, calculate its USDT value and add it to the list of coins with their EURO values
				ticker_symbol = coin_symbol + 'BTC'
				ticker_price = ticker_prices.get(ticker_symbol)
				coin_usdt_value = (unlocked_balance + locked_balance) * ticker_price * ticker_prices.get('BTCUSDT')
				if coin_usdt_value > 1:
					# Calculate EURO value using EURUSDT coin pair
					coin_values.append((coin_symbol, coin_usdt_value/ticker_prices.get('EURUSDT')))

	# Sort the list of coins and their EURO values by EURO value in descending order
	coin_values.sort(key=lambda x: x[1], reverse=True)

	# Return the list of coins and their EURO values
	return coin_values



def main():
	
    # Call the get_accountbalance function to get the list of coins and their EURO values
    coins_euro_value = get_account_balances()

    # Print the list of coins and their EURO values in descending order of EURO value
    for coin, euro_value in coins_euro_value:
        print(f"{coin}: € {euro_value:.2f}")

    # Calculate the grand total EURO value
    grand_euro_total = sum(map(lambda coins_euro_value: coins_euro_value[1], coins_euro_value))

    # Print the grand total EURO value
    print(f"\nGrand Total: € {grand_euro_total:.2f}")

if __name__ == '__main__':
    main()