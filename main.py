from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/notify', methods=['POST'])
def send_notification():
    notification = request.json
    # Here you can add logic to send notifications (e.g., email, SMS)
    return jsonify(notification), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)