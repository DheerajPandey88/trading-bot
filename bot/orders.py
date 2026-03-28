from bot.validators import (
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price
)

class OrderService:
    def __init__(self, client, logger):
        self.client = client
        self.logger = logger

    def place_order(self, symbol, side, order_type, quantity, price=None):
        try:
            # Validation
            validate_side(side)
            validate_order_type(order_type)
            validate_quantity(quantity)
            validate_price(price, order_type)

            order_params = {
                "symbol": symbol,
                "side": side,
                "type": order_type,
                "quantity": quantity
            }

            if order_type == "LIMIT":
                order_params["price"] = price
                order_params["timeInForce"] = "GTC"

            self.logger.info(f"Request: {order_params}")

            response = self.client.place_order(**order_params)

            self.logger.info(f"Response: {response}")

            return response

        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
            raise