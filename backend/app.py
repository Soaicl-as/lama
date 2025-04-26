from flask import Flask, render_template, request, jsonify
from instagram import InstagramBot
from utils import send_messages
from config import Config
import threading

app = Flask(__name__)
bot = InstagramBot()

@app.route("/")
def index():
    return render_template("frontend/index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    result = bot.login(username, password)
    if result == "2FA":
        return jsonify({"2FA": True})
    elif result:
        return jsonify({"success": True})
    else:
        return jsonify({"error": "Invalid credentials"})

@app.route("/2fa", methods=["POST"])
def two_factor_auth():
    code = request.form["code"]
    bot.login_with_2fa(code)
    return jsonify({"success": True})

@app.route("/target", methods=["POST"])
def target():
    target_username = request.form["target_username"]
    target_list = request.form["target_list"]
    Config.TARGET_USERNAME = target_username
    Config.TARGET_LIST = target_list
    return jsonify({"success": True})

@app.route("/message", methods=["POST"])
def message():
    message = request.form["message"]
    num_recipients = int(request.form["num_recipients"])
    delay_min = int(request.form["delay_min"])
    delay_max = int(request.form["delay_max"])
    Config.MESSAGE = message
    Config.NUM_RECIPIENTS = num_recipients
    Config.DELAY_MIN = delay_min
    Config.DELAY_MAX = delay_max
    return jsonify({"success": True})

@app.route("/start", methods=["POST"])
def start():
    target_list = bot.get_target_list(Config.TARGET_USERNAME, Config.TARGET_LIST)
    recipient_usernames = [profile.username for profile in target_list[:Config.NUM_RECIPIENTS]]
    threading.Thread(target=send_messages, args=(bot, recipient_usernames, Config.MESSAGE, Config.DELAY_MIN, Config.DELAY_MAX)).start()
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)
