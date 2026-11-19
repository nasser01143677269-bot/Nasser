import os
import logging
from flask import Flask, request, jsonify

# إعداد سجل الأحداث
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("NasserBot")

app = Flask(__name__)

# بيانات الإعدادات (هنحطها في Environment Variables على Railway لاحقاً)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "PUT_TELEGRAM_TOKEN_HERE")
MIKROTIK_HOST = os.getenv("MIKROTIK_HOST", "PUT_MIKROTIK_IP_HERE")
MIKROTIK_USER = os.getenv("MIKROTIK_USER", "admin")
MIKROTIK_PASS = os.getenv("MIKROTIK_PASS", "PUT_MIKROTIK_PASS_HERE")


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "service": "MikroTik & Telegram Bridge",
        "mikrotik_configured": MIKROTIK_HOST != "PUT_MIKROTIK_IP_HERE",
        "telegram_configured": TELEGRAM_BOT_TOKEN != "PUT_TELEGRAM_TOKEN_HERE"
    }), 200


@app.route("/health", methods=["GET"])
def health():
    return "OK", 200


@app.route("/telegram/webhook", methods=["POST"])
def telegram_webhook():
    data = request.get_json(silent=True) or {}
    logger.info(f"Received Telegram update: {data}")

    message = data.get("message") or {}
    chat_id = (message.get("chat") or {}).get("id")
    text = (message.get("text") or "").strip()

    if not chat_id:
        return jsonify({"ok": True}), 200

    # مثال سريع لأمر /status
    if text == "/status":
        reply = f"البوت شغال تمام ✅\nسيرفر الميكروتيك المضبوط: {MIKROTIK_HOST}"
        logger.info(f"Reply to {chat_id}: {reply}")

    return jsonify({"ok": True}), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    logger.info(f"Starting server on port {port}...")
    app.run(host="0.0.0.0", port=port)
