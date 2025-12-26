import json
import os

try:
    from kafka import KafkaProducer
    KAFKA_AVAILABLE = True
    producer = KafkaProducer(
        bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP", "kafka:9092"),
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
except ImportError:
    KAFKA_AVAILABLE = False
    producer = None

def publish_event(key: str, payload: dict) -> None:
    if KAFKA_AVAILABLE and producer:
        producer.send("erp.communication", {"key": key, "payload": payload})
        producer.flush()
    else:
        print(f"Event (Kafka unavailable): {key} - {payload}")
