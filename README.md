# BitMEX Market Maker

This is a sample market making bot for use with [BitMEX](https://www.bitmex.com).

It is free to use and modify for your own strategies. It provides the following:

* A `BitMEX` object wrapping the REST and WebSocket APIs.
  * All data is realtime and efficiently [fetched via the WebSocket](market_maker/ws/ws_thread.py). This is the fastest way to get market data.
  * Orders may be created, queried, and cancelled via `BitMEX.buy()`, `BitMEX.sell()`, `BitMEX.open_orders()` and the like.
  * Withdrawals may be requested (but they still must be confirmed via email and 2FA).
  * Connection errors and WebSocket reconnection is handled for you.
  * [Permanent API Key](https://testnet.bitmex.com/app/apiKeys) support is included.
* [A scaffolding for building your own trading strategies.](#advanced-usage)
  * Out of the box, a simple market making strategy is implemented that blankets the bid and ask.
  * More complicated strategies are up to the user. Try incorporating [index data](https://testnet.bitmex.com/app/index/.XBT),
    query other markets to catch moves early, or develop your own completely custom strategy.

**Develop on [Testnet](https://testnet.bitmex.com) first!** Testnet trading is completely free and is identical to the live market.

> BitMEX is not responsible for any losses incurred when using this code. This code is intended for sample purposes ONLY - do not
  use this code for real trades unless you fully understand what it does and what its caveats are.

> This is not a sophisticated market making program. It is intended to show the basics of market making while abstracting some
  of the rote work of interacting with the BitMEX API. It does not make smart decisions and will likely lose money.

## Getting Started

1. Create a [Testnet BitMEX Account](https://testnet.bitmex.com) and [deposit some TBTC](https://testnet.bitmex.com/app/deposit).
2. Install: `pip install bitmex-market-maker`. It is strongly recommeded to use a virtualenv.
3. Create a marketmaker project: run `marketmaker setup`
    * This will create `settings.py` and `market_maker/` in the working directory.
    * Modify `settings.py` to tune parameters.
4. Edit settings.py to add your [BitMEX API Key and Secret](https://testnet.bitmex.com/app/apiKeys) and change bot parameters.
    * Note that user/password authentication is not supported.
    * Run with `DRY_RUN=True` to test cost and spread.
5. Run it: `marketmaker [symbol]`
6. Satisfied with your bot's performance? Create a [live API Key](https://www.bitmex.com/app/apiKeys) for your
   BitMEX account, set the `BASE_URL` and start trading!

## Operation Overview

This market maker works on the following principles:

* The market maker tracks the last `bidPrice` and `askPrice` of the quoted instrument to determine where to start quoting.
* Based on parameters set by the user, the bot creates a descriptions of orders it would like to place.
  - If `settings.MAINTAIN_SPREADS` is set, the bot will start inside the current spread and work outwards.
  - Otherwise, spread is determined by interval calculations.
* If the user specifies position limits, these are checked. If the current position is beyond a limit,
  the bot stops quoting that side of the market.
* These order descriptors are compared with what the bot has currently placed in the market.
  - If an existing order can be amended to the desired value, it is amended.
  - Otherwise, a new order is created.
  - Extra orders are canceled.
* The bot then prints details of contracts traded, tickers, and total delta.

## Simplified Output

The following is some of what you can expect when running this bot:

```
2016-01-28 17:29:31,054 - INFO - market_maker - BitMEX Market Maker Version: 1.0
2016-01-28 17:29:31,074 - INFO - ws_thread - Connecting to wss://testnet.bitmex.com/realtime?subscribe=quote:XBT7D,trade:XBT7D,instrument,order:XBT7D,execution:XBT7D,margin,position
2016-01-28 17:29:31,074 - INFO - ws_thread - Authenticating with API Key.
2016-01-28 17:29:31,075 - INFO - ws_thread - Started thread
2016-01-28 17:29:32,079 - INFO - ws_thread - Connected to WS. Waiting for data images, this may take a moment...
2016-01-28 17:29:32,079 - INFO - ws_thread - Got all market data. Starting.
2016-01-28 17:29:32,079 - INFO - market_maker - Using symbol XBT7D.
2016-01-28 17:29:32,079 - INFO - market_maker - Order Manager initializing, connecting to BitMEX. Live run: executing real trades.
2016-01-28 17:29:32,079 - INFO - market_maker - Resetting current position. Cancelling all existing orders.
2016-01-28 17:29:33,460 - INFO - market_maker - XBT7D Ticker: Buy: 388.61, Sell: 389.89
2016-01-28 17:29:33,461 - INFO - market_maker - Start Positions: Buy: 388.62, Sell: 389.88, Mid: 389.25
2016-01-28 17:29:33,461 - INFO - market_maker - Current XBT Balance: 3.443498
2016-01-28 17:29:33,461 - INFO - market_maker - Current Contract Position: -1
2016-01-28 17:29:33,461 - INFO - market_maker - Avg Cost Price: 389.75
2016-01-28 17:29:33,461 - INFO - market_maker - Avg Entry Price: 389.75
2016-01-28 17:29:33,462 - INFO - market_maker - Contracts Traded This Run: 0
2016-01-28 17:29:33,462 - INFO - market_maker - Total Contract Delta: -17.7510 XBT
2016-01-28 17:29:33,462 - INFO - market_maker - Creating 4 orders:
2016-01-28 17:29:33,462 - INFO - market_maker - Sell 100 @ 389.88
2016-01-28 17:29:33,462 - INFO - market_maker - Sell 200 @ 390.27
2016-01-28 17:29:33,463 - INFO - market_maker -  Buy 100 @ 388.62
2016-01-28 17:29:33,463 - INFO - market_maker -  Buy 200 @ 388.23
-----
2016-01-28 17:29:37,366 - INFO - ws_thread - Execution: Sell 1 Contracts of XBT7D at 389.88
2016-01-28 17:29:38,943 - INFO - market_maker - XBT7D Ticker: Buy: 388.62, Sell: 389.88
2016-01-28 17:29:38,943 - INFO - market_maker - Start Positions: Buy: 388.62, Sell: 389.88, Mid: 389.25
2016-01-28 17:29:38,944 - INFO - market_maker - Current XBT Balance: 3.443496
2016-01-28 17:29:38,944 - INFO - market_maker - Current Contract Position: -2
2016-01-28 17:29:38,944 - INFO - market_maker - Avg Cost Price: 389.75
2016-01-28 17:29:38,944 - INFO - market_maker - Avg Entry Price: 389.75
2016-01-28 17:29:38,944 - INFO - market_maker - Contracts Traded This Run: -1
2016-01-28 17:29:38,944 - INFO - market_maker - Total Contract Delta: -17.7510 XBT
2016-01-28 17:29:38,945 - INFO - market_maker - Amending Sell: 99 @ 389.88 to 100 @ 389.88 (+0.00)

```

## Advanced usage

You can implement custom trading strategies using the market maker. `market_maker.OrderManager`
controls placing, updating, and monitoring orders on BitMEX. To implement your own custom
strategy, subclass `market_maker.OrderManager` and override `OrderManager.place_orders()`:

```
from market_maker.market_maker import OrderManager

class CustomOrderManager(OrderManager):
    def place_orders(self) -> None:
        # implement your custom strategy here
```

Your strategy should provide a set of orders. An order is a dict containing price, quantity, and
whether the order is buy or sell. For example:

```
buy_order = {
    'price': 1234.5, # float
    'orderQty': 100, # int
    'side': 'Buy'
}

sell_order = {
    'price': 9876.5, # float
    'orderQty': 100, # int
    'side': 'Sell'
}
```

Call `self.converge_orders()` to submit your orders. `converge_orders()` will create, amend,
and delete orders on BitMEX as necessary to match what you pass in:

```
def place_orders(self) -> None:
    buy_orders = []
    sell_orders = []

    # populate buy and sell orders, e.g.
    buy_orders.append({'price': 998.0, 'orderQty': 100, 'side': "Buy"})
    buy_orders.append({'price': 999.0, 'orderQty': 100, 'side': "Buy"})
    sell_orders.append({'price': 1000.0, 'orderQty': 100, 'side': "Sell"})
    sell_orders.append({'price': 1001.0, 'orderQty': 100, 'side': "Sell"})

    self.converge_orders(buy_orders, sell_orders)
```

To run your strategy, call `run_loop()`:
```
order_manager = CustomOrderManager()
order_manager.run_loop()
```

Your custom strategy will run until you terminate the program with CTRL-C. There is an example
in `custom_strategy.py`.

## Notes on Rate Limiting

By default, the BitMEX API rate limit is 300 requests per 5 minute interval (avg 1/second).

This bot uses the WebSocket to greatly reduce the number of calls sent to the BitMEX API.

If you are quoting multiple contracts and your ratelimit is becoming an obstacle, please
[email support](mailto:support@bitmex.com) with details of your quoting. In the vast majority of cases,
we are able to raise a user's ratelimit without issue.

## Troubleshooting

Common errors we've seen:

* `TypeError: __init__() got an unexpected keyword argument 'json'`
  * This is caused by an outdated version of `requests`. Run `pip install -U requests` to update.


## Compatibility

This module supports Python 3.5 and later.

## See also

BitMEX has a Python [REST client](https://github.com/BitMEX/api-connectors/tree/master/official-http/python-swaggerpy)
and [websocket client.](https://github.com/BitMEX/api-connectors/tree/master/official-ws/python)
