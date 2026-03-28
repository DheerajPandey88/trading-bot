import argparse
import os
from dotenv import load_dotenv

from bot.client import BinanceFuturesClient
from bot.orders import OrderService
from bot.logging_config import setup_logger

def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")

    parser.add_argument("--symbol", required=True, help="Trading symbol (e.g., BTCUSDT)")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"])
    parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT"])
    parser.add_argument("--quantity", required=True, type=float)
    parser.add_argument("--price", type=float, help="Required for LIMIT orders")

    args = parser.parse_args()

    logger = setup_logger()

    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        print("API keys not found. Set them in .env file")
        return

    client = BinanceFuturesClient(api_key, api_secret)
    order_service = OrderService(client, logger)

    try:
        print("\n=== Order Request Summary ===")
        print(f"Symbol   : {args.symbol}")
        print(f"Side     : {args.side}")
        print(f"Type     : {args.type}")
        print(f"Quantity : {args.quantity}")
        if args.type == "LIMIT":
            print(f"Price    : {args.price}")

        response = order_service.place_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price
        )

        print("\n=== Order Response ===")
        print(f"Order ID     : {response.get('orderId')}")
        print(f"Status       : {response.get('status')}")
        print(f"Executed Qty : {response.get('executedQty')}")
        print(f"Avg Price    : {response.get('avgPrice')}")

        print("\n✅ Order placed successfully")

    except Exception as e:
        print(f"\n❌ Order failed: {str(e)}")

if __name__ == "__main__":
    main()