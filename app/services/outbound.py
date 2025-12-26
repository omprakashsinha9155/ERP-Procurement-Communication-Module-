from app.models import CommMessage

def send_message(msg: CommMessage) -> None:
    try:
        if not msg:
            return
        channel = getattr(msg, 'channel', None)
        if not channel:
            return
        if channel == "email":
            _send_email(msg)
        elif channel == "sms":
            _send_sms(msg)
        elif channel == "webhook":
            _send_webhook(msg)
        elif channel == "portal":
            _post_portal_note(msg)
    except Exception as e:
        print(f"Error in send_message: {str(e)}")
        import traceback
        traceback.print_exc()

def _send_email(msg: CommMessage) -> None:
    try:
        if not msg:
            return
        metadata = getattr(msg, 'message_metadata', None)
        if metadata is None:
            metadata = {}
        if not isinstance(metadata, dict):
            metadata = {}
        to_email = metadata.get("to")
        thread_id = getattr(msg, 'thread_id', None)
        body = getattr(msg, 'body', '')
        if not to_email:
            print(f"Email queued for thread {thread_id}")
            return
        print(f"Email would be sent to {to_email}: {body[:50]}...")
    except Exception as e:
        print(f"Error in _send_email: {str(e)}")

def _send_sms(msg: CommMessage) -> None:
    try:
        if not msg:
            return
        metadata = getattr(msg, 'message_metadata', None)
        if metadata is None:
            metadata = {}
        if not isinstance(metadata, dict):
            metadata = {}
        to_number = metadata.get("to")
        thread_id = getattr(msg, 'thread_id', None)
        body = getattr(msg, 'body', '')
        if not to_number:
            print(f"SMS queued for thread {thread_id}")
            return
        print(f"SMS would be sent to {to_number}: {body[:50]}...")
    except Exception as e:
        print(f"Error in _send_sms: {str(e)}")

def _send_webhook(msg: CommMessage) -> None:
    try:
        if not msg:
            return
        metadata = getattr(msg, 'message_metadata', None)
        if metadata is None:
            metadata = {}
        if not isinstance(metadata, dict):
            metadata = {}
        callback_url = metadata.get("callback_url")
        thread_id = getattr(msg, 'thread_id', None)
        if not callback_url:
            print(f"Webhook queued for thread {thread_id}")
            return
        import requests
        message_id = getattr(msg, 'id', None)
        body = getattr(msg, 'body', '')
        requests.post(callback_url, json={
            "event": "comm.message.sent",
            "payload": {
                "thread_id": str(thread_id),
                "message_id": str(message_id),
                "body": body
            }
        }, timeout=5)
    except Exception as e:
        print(f"Error in _send_webhook: {str(e)}")

def _post_portal_note(msg: CommMessage) -> None:
    try:
        if not msg:
            return
        thread_id = getattr(msg, 'thread_id', None)
        body = getattr(msg, 'body', '')
        print(f"Portal note queued for thread {thread_id}: {body[:50]}...")
    except Exception as e:
        print(f"Error in _post_portal_note: {str(e)}")