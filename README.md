# ERP Procurement Communication Module

A FastAPI-based communication module for managing multi-channel communication between ERP systems and suppliers.

## Overview

This is an **ERP Procurement Communication Module** built with FastAPI. It manages communication between ERP systems and suppliers through multiple channels (Email, SMS, Webhook, Portal, Chat).

## Features
### Core Functionality


1. **Communication Threads Management**
   - Create communication threads for procurement objects (RFQ, PO, GRN, etc.)
   - Track thread status (open/closed)
   - Maintain thread-based conversation history

2. **Multi-Channel Messaging**
   - **Email**: Send email notifications to suppliers
   - **SMS**: SMS alerts support
   - **Webhook**: Send webhook events to external systems
   - **Portal**: Post notes to supplier portal
   - **Chat**: Chat messages support

3. **Event-Driven Architecture**
   - Consume Kafka events (RFQ created, PO approved, GRN delayed, etc.)
   - Automatically send notifications to suppliers based on events
   - Template-based message generation using Jinja2

4. **REST API Endpoints**
   - `POST /threads/` - Create communication threads
   - `POST /messages/` - Create and send messages
   - `GET /alerts/` - List alerts
   - `GET /channels/` - Get available communication channels
   - `POST /webhooks/emit/{message_id}` - Emit webhook events

## Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL database
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ERP_communication
   ```

2. **Create virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   
   Create PostgreSQL database:
   ```sql
   CREATE DATABASE ERP_Communication;
   ```
   
   Update database credentials in `app/db.py`:
   ```python
   DB_USER = "postgres"
   DB_PASSWORD = "your_password"
   DB_HOST = "localhost"
   DB_PORT = "5432"
   DB_NAME = "ERP_Communication"
   ```

5. **Initialize Database**
   ```bash
   python init_db.py
   ```

6. **Run the Application**
   ```bash
   python run.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

7. **Access API Documentation**
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
ERP_communication/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── db.py                # Database connection configuration
│   ├── models.py            # SQLAlchemy models
│   ├── routers/             # API route handlers
│   │   ├── threads.py       # Thread management endpoints
│   │   ├── messages.py     # Message creation/sending endpoints
│   │   ├── alerts.py        # Alerts management endpoints
│   │   ├── channels.py      # Channel listing endpoints
│   │   └── webhooks.py     # Webhook event endpoints
│   ├── services/            # Business logic services
│   │   ├── outbound.py     # Message sending (email/SMS/webhook/portal)
│   │   ├── templates.py    # Jinja2 template rendering
│   │   └── events.py       # Kafka event publishing (optional)
│   └── workers/            # Background workers
│       └── consumer.py     # Kafka consumer for procurement events
├── init_db.py              # Database initialization script
├── run.py                  # Application runner script
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore file
├── LICENSE                # MIT License
└── README.md              # This file
```

## Database Schema

### Table: comm_threads
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| object_type | String | Type of object (RFQ, PO, etc.) |
| object_id | String | Object identifier |
| supplier_id | UUID | Supplier reference (nullable) |
| subject | Text | Thread subject (nullable) |
| status | String | Thread status (default: "open") |
| created_by | UUID | Creator user ID (nullable) |
| created_at | TIMESTAMP | Creation timestamp |

### Table: comm_messages
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| thread_id | UUID | Foreign key to comm_threads |
| sender_type | String | system/user/supplier |
| sender_id | String | Sender identifier (nullable) |
| body | Text | Message content |
| direction | String | outbound/inbound |
| channel | String | email/sms/webhook/portal/chat |
| status | String | queued/sent/failed (default: "queued") |
| metadata | JSONB | Additional metadata (JSON) |
| created_at | TIMESTAMP | Creation timestamp |

## API Usage Examples

### Create a Communication Thread

```bash
POST http://localhost:8000/threads/
Content-Type: application/json

{
  "object_type": "PO",
  "object_id": "PO-12345",
  "supplier_id": "550e8400-e29b-41d4-a716-446655440000",
  "subject": "Purchase Order Communication",
  "created_by": "550e8400-e29b-41d4-a716-446655440001"
}
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440002"
}
```

### Send a Message

```bash
POST http://localhost:8000/messages/

Content-Type: application/json

{
  "thread_id": ""bc3c9d1c-6c9a-4056-b4aa-c676e1a81e1d"",
  "sender_type": "system",
  "sender_id": null,
  "body": "Your Purchase Order PO-12345 has been approved and will be processed soon.",
  "channel": "email"
}
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440003",
  "status": "sent"
}
```

### Get Available Channels

```bash
GET http://localhost:8000/channels/
```

**Response:**
```json
{
  "channels": ["email", "sms", "webhook", "portal", "chat"]
}
```

## Configuration

### Database Configuration

Update database settings in `app/db.py`:

```python
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "your_password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "ERP_Communication")
```

### Environment Variables

You can also use environment variables:

```bash
# Windows PowerShell
$env:DB_USER="postgres"
$env:DB_PASSWORD="your_password"
$env:DB_HOST="localhost"
$env:DB_PORT="5432"
$env:DB_NAME="ERP_Communication"

# Linux/Mac
export DB_USER="postgres"
export DB_PASSWORD="your_password"
export DB_HOST="localhost"
export DB_PORT="5432"
export DB_NAME="ERP_Communication"
```

### Kafka Configuration (Optional)

Kafka integration is optional. If Kafka is not available, the server will run without it. To enable Kafka, update `app/services/events.py` with your Kafka configuration.

## Troubleshooting

### Database Connection Error
- Verify PostgreSQL service is running
- Check database credentials in `app/db.py`
- Ensure database `ERP_Communication` exists

### Module Not Found Error
```bash
pip install -r requirements.txt
```

### Port Already in Use
- Stop the process using port 8000, or
- Use a different port:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

## Important Notes

1. **Kafka Integration**: Optional. Server runs without Kafka if not configured.

2. **Email/SMS Providers**: Configure actual providers for production:
   - Email: SMTP server configuration in `app/services/outbound.py`
   - SMS: SMS provider API configuration

3. **Templates**: Create `templates/` folder for Jinja2 templates:
   - `templates/rfq_created.txt`
   - `templates/po_approved.txt`
   - etc.

4. **Database**: PostgreSQL is required. SQLite or other databases are not supported.

## Development

### Adding New Features

1. Add new router in `app/routers/`
2. Register router in `app/main.py`
3. Add required services in `app/services/`
4. Update database models if needed

### Code Structure
- **Routers**: Define API endpoints
- **Services**: Handle business logic
- **Models**: Define database models
- **Workers**: Handle background tasks

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions:
1. Check the README carefully
2. Review error messages
3. Verify database connection
4. Ensure dependencies are properly installed

---

**Happy Coding!**
