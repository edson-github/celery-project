# Celery Project

A FastAPI application with Celery integration for asynchronous task processing. This project demonstrates how to use Celery with Redis as a message broker to handle background tasks in a web application.

## Features

- **FastAPI Web Framework**: Modern, fast web framework for building APIs
- **Celery Task Queue**: Asynchronous task processing with Redis as broker
- **Task Status Tracking**: Monitor task execution status and results
- **Simple Math Operations**: Example task for basic arithmetic
- **Long-Running Tasks**: Simulated long-running task with 10-second delay

## Project Structure

```
celery-project/
├── main.py              # FastAPI application with endpoints
├── tasks.py             # Celery task definitions
├── celeryconfig.py      # Celery configuration
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

## Prerequisites

- Python 3.8+
- Redis server
- pip (Python package manager)

## Installation

1. **Clone the repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd celery-project
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install and start Redis**:
   
   **On macOS (using Homebrew)**:
   ```bash
   brew install redis
   brew services start redis
   ```
   
   **On Ubuntu/Debian**:
   ```bash
   sudo apt-get install redis-server
   sudo systemctl start redis-server
   ```
   
   **On Windows**:
   Download and install Redis from [redis.io](https://redis.io/download)

## Dependencies

The project requires the following Python packages:

```
fastapi
uvicorn
celery
redis
```

## Configuration

The Celery configuration is defined in `celeryconfig.py`:

- **Broker**: Redis at `localhost:6379/0`
- **Result Backend**: Redis at `localhost:6379/0`
- **Serializer**: JSON
- **Timezone**: America/Sao_Paulo
- **UTC**: Enabled

## Running the Application

### 1. Start the Celery Worker

In a terminal, start the Celery worker:

```bash
celery -A tasks worker --loglevel=info
```

### 2. Start the FastAPI Server

In another terminal, start the FastAPI application:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Health Check
- **GET** `/`
- **Response**: `{"Hello": "World"}`

### 2. Addition Task
- **GET** `/somar/?a={number}&b={number}`
- **Parameters**:
  - `a`: First number (integer)
  - `b`: Second number (integer)
- **Response**: `{"task_id": "task-uuid"}`

**Example**:
```bash
curl "http://localhost:8000/somar/?a=5&b=3"
```

### 3. Task Status
- **GET** `/status/{task_id}`
- **Parameters**:
  - `task_id`: Task UUID returned from task creation
- **Response**: 
  ```json
  {
    "task_id": "task-uuid",
    "status": "PENDING|SUCCESS|FAILURE",
    "result": "task_result_or_error"
  }
  ```

**Example**:
```bash
curl "http://localhost:8000/status/task-uuid-here"
```

### 4. Long-Running Task
- **GET** `/tarefa-lenta/`
- **Response**: `{"task_id": "task-uuid"}`

**Example**:
```bash
curl "http://localhost:8000/tarefa-lenta/"
```

## Task Types

### 1. Addition Task (`soma`)
- **Purpose**: Performs basic arithmetic addition
- **Input**: Two numbers (x, y)
- **Output**: Sum of the numbers
- **Execution Time**: Immediate

### 2. Long-Running Task (`tarefa_lenta`)
- **Purpose**: Simulates a time-consuming operation
- **Input**: None
- **Output**: Success message
- **Execution Time**: 10 seconds

## Usage Examples

### Complete Workflow Example

1. **Start a task**:
   ```bash
   curl "http://localhost:8000/somar/?a=10&b=20"
   ```
   Response: `{"task_id": "abc123-def456-ghi789"}`

2. **Check task status**:
   ```bash
   curl "http://localhost:8000/status/abc123-def456-ghi789"
   ```
   Response: `{"task_id": "abc123-def456-ghi789", "status": "SUCCESS", "result": 30}`

### Long-Running Task Example

1. **Start long task**:
   ```bash
   curl "http://localhost:8000/tarefa-lenta/"
   ```
   Response: `{"task_id": "xyz789-abc123-def456"}`

2. **Monitor progress**:
   ```bash
   curl "http://localhost:8000/status/xyz789-abc123-def456"
   ```
   Response (immediately): `{"task_id": "xyz789-abc123-def456", "status": "PENDING", "result": null}`

3. **Check after completion**:
   ```bash
   curl "http://localhost:8000/status/xyz789-abc123-def456"
   ```
   Response: `{"task_id": "xyz789-abc123-def456", "status": "SUCCESS", "result": "Tarefa concluída após 10 segundos"}`

## Development

### Adding New Tasks

1. **Define the task in `tasks.py`**:
   ```python
   @celery.task
   def minha_nova_tarefa(parametro):
       # Task logic here
       return resultado
   ```

2. **Add endpoint in `main.py`**:
   ```python
   @app.get("/minha-tarefa/")
   def executar_minha_tarefa(parametro: str):
       tarefa = minha_nova_tarefa.delay(parametro)
       return {"task_id": tarefa.id}
   ```

### Configuration Options

Modify `celeryconfig.py` to change:
- Redis connection settings
- Task serialization format
- Timezone settings
- Task routing and queues

## Troubleshooting

### Common Issues

1. **Redis Connection Error**:
   - Ensure Redis is running: `redis-cli ping`
   - Check Redis port and configuration

2. **Celery Worker Not Starting**:
   - Verify Redis is accessible
   - Check Celery configuration
   - Ensure all dependencies are installed

3. **Tasks Not Executing**:
   - Confirm Celery worker is running
   - Check task imports and registration
   - Verify broker connection

### Debug Mode

Enable debug logging:
```bash
celery -A tasks worker --loglevel=debug
```

## Production Considerations

- Use a production-grade Redis instance
- Configure Celery with proper concurrency settings
- Implement proper error handling and monitoring
- Use environment variables for configuration
- Set up task result expiration
- Configure task routing for different queues

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For issues and questions:
- Check the troubleshooting section
- Review Celery and FastAPI documentation
- Open an issue in the repository
