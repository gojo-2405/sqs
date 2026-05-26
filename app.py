from flask import Flask, request, jsonify
import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

sqs = boto3.client(
    "sqs",
    region_name="us-east-1"
)

QUEUE_URL = os.getenv("QUEUE_URL")

@app.route("/order", methods=["POST"])
def create_order():

    data = request.json

    message = {
        "type": data.get("type"),
        "order_id": data.get("order_id"),
        "amount": data.get("amount"),
        "user": data.get("user")
    }

    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(message)
    )

    return jsonify({
        "message": "Message sent to SQS",
        "data": message
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
