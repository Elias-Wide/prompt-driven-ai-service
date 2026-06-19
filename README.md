# AI Structured Processing Engine

This is an isolated, dynamic AI microservice built with Taskiq, FastAPI, and LangChain. It functions as a prompt-driven processing engine that consumes raw text or voice inputs, enriches them with modular instruction files, and returns strictly structured JSON payloads.

Depending on the startup environment configuration, the service runs either as an asynchronous background worker consuming tasks from a message broker (RabbitMQ) or as a standard web server accepting immediate HTTP requests (FastAPI).

---


### Request Ingestion & Execution Modes
* **HTTP Mode**: When configured via environment variables, the service initializes a FastAPI instance exposing endpoints for low-latency synchronous text and voice processing.
* **Worker Mode**: When HTTP is disabled, the service runs natively as a stateless Taskiq worker, pulling tasks off the RabbitMQ message broker queue.

### Core Processing Layers
* **Speech-to-Text Pipeline**: If the input payload consists of audio data, the system utilizes a dedicated transcription layer to decode speech into a clean text string before routing it further.
* **Text Processing Pipeline**: Clean text strings are directly funneled into the LangChain execution engine layer.

### Dual-Layer Prompt Management
The system utilizes a two-tier hierarchy to construct system instructions dynamically without hardcoded schemas:
1. **Base Meta Prompt**: A static blueprint defining absolute behavioral boundaries, execution context, current timestamp registration, and fallback error handling states.
2. **Contextual Extra Prompts**: To specify tasks, you must place Markdown files (`.md`) inside the designated `prompts/` directory. Each file outlines specific instructions for the target sub-service, describing its operation logic and specifying the exact response JSON layout.

Before execution, the engine fetches the files from memory, builds the pipeline layout, and dynamically binds the meta configuration and the chosen extra file together.

---

## Response Matrix

The processing engine bypasses conversational text responses, strictly enforcing structural JSON objects returning one of two execution paths:
* **200 OK (Success)**: A fully populated JSON map containing key-value data complying exactly with the schema boundaries described in the requested extra prompt file.
* **400 Bad Request (Error)**: If user input is ambiguous, corrupted, or completely out of scope relative to the instructions, a fallback safety mechanism is triggered. The engine immediately aborts processing and outputs a structured error object containing a descriptive explanation message.

---

## Environment Configuration (.env)

The behavior, role distribution, and underlying model allocations of the container instantiation are driven entirely by a flat configuration file.

```ini
APP_MODE=DEV
APP_NAME=AI_SERVICE
APP_LOGGING_MODE=on
APP_ADMIN_EMAIL=admin@example.com
APP_ADMIN_PASSWORD=your_super_secret_password_here

# Toggle flag for container runtime orchestration behavior
# TRUE  -> Initializes FastAPI framework endpoints to handle HTTP traffic
# FALSE -> Disables HTTP and switches execution into a pure Taskiq message queue worker
HTTP_MODE=FALSE

AI_API_KEY=your_ai_api_key_here
AI_TEXT_MODEL=gpt-4o
AI_SPEECH_MODEL=whisper-1
```

