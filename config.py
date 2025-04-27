import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = str(os.getenv("ADMIN_CHAT_ID", "714948319"))  # Convert to string
BACKEND_URL = "https://web-production-34229.up.railway.app/api/orders/"  # Ensure trailing slash
MEDIA_URL = "https://web-production-34229.up.railway.app"

# Notification settings (default: enabled)
NOTIFICATIONS_ENABLED = True
NOTIFICATION_SOUND = True