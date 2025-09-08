import pika
import json
import joblib
import pandas as pd

from preprocessor.encode import EncodeHighCardFeatures
from feature_engine.encoding import RareLabelEncoder, WoEEncoder
from preprocessor.transformer import DataFrameWrapper
from preprocessor.transformer import CatWoeTransformer, WoeTransformer

PIPELINE_PATH = "models/pipeline.joblib"
pipeline = joblib.load(PIPELINE_PATH)
mapping_dict = joblib.load("models/mapping_dict.joblib")
def predict(features):
    
    y_hat = pipeline.predict_proba(pd.DataFrame([features]))[:,1][0]
    return f'{y_hat:.2f}'

def callback(ch, method, props, body):

    data = json.loads(body)
    print(data)
    prediction = predict(data)
    
    print(f"{prediction}")

    ch.basic_publish(
        exchange="",
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=str(prediction),
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    credentials = pika.PlainCredentials("guest", "guest")  # or your custom user
    connection = pika.BlockingConnection(
        pika.ConnectionParameters("localhost", 5672, "/", credentials)
    )
    channel = connection.channel()

    channel.queue_declare(queue="ml_queue")

    channel.basic_consume(queue="ml_queue", on_message_callback=callback, auto_ack=True)

    print("[*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    main()