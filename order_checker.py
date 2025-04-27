import asyncio
import requests
from handlers import send_order_to_admin
from config import BACKEND_URL, NOTIFICATIONS_ENABLED
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def check_orders_loop(bot):
    sent_orders = set()
    logger.info("Starting order monitoring loop")

    while True:
        try:
            if NOTIFICATIONS_ENABLED:
                logger.info("Checking for new orders...")
                response = requests.get(f"{BACKEND_URL}?status=pending")
                response.raise_for_status()

                orders = response.json()
                for order in orders:
                    if order["id"] not in sent_orders:
                        order_data = {
                            'id': order['id'],
                            'name': order['name'],
                            'created_at': order['created_at'],
                            'phone': order['phone'],
                            'product': order['product'],
                            'quantity': order['quantity'],
                            'receipt': order['receipt']
                        }
                        await send_order_to_admin(bot, order_data)
                        sent_orders.add(order['id'])
                        logger.info(f"Sent notification for new order #{order['id']}")
            else:
                logger.info("Notifications are disabled, skipping order check")
                
        except requests.RequestException as e:
            logger.error(f"Error getting orders: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in order checker: {e}")

        # Check every 10 seconds
        await asyncio.sleep(10)