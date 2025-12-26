from kafka import KafkaConsumer
import json
from app.services.templates import render_template
from app.services.outbound import send_message

consumer = KafkaConsumer(
    "erp.procurement",
    bootstrap_servers="kafka:9092",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    group_id="comm-module"
)

for msg in consumer:
    event = msg.value
    key = event.get("key")
    payload = event.get("payload")

    if key == "rfq.created":
        thread_id = create_thread_for(payload["rfq_id"], "RFQ", supplier_id=payload["supplier_id"])
        message_body = render_template("rfq_created", payload)
        outbound = build_message(thread_id, "system", None, message_body, "email",
                                 metadata={"to": payload["supplier_email"]})
        send_message(outbound)

    elif key == "po.approved":
        thread_id = get_or_create_thread("PO", payload["po_id"], payload["supplier_id"])
        message_body = render_template("po_approved", payload)
        outbound = build_message(thread_id, "system", None, message_body, "email",
                                 metadata={"to": payload["supplier_email"]})
        send_message(outbound)

    elif key == "grn.delayed":
        create_alert(thread_id=get_thread("PO", payload["po_id"]),
                     type="delay", level="warning",
                     message=f"Delivery delay for PO {payload['po_id']}",
                     target_user_id=payload["buyer_id"])
