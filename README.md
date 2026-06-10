# AI Structured Processing Engine (Taskiq Worker)

This is an isolated, event-driven AI microservice built with **Taskiq** and **LangChain**. It functions as a prompt-driven processing engine that consumes raw text or voice inputs from a message broker (**RabbitMQ**), dynamically fetches its active system instructions from a lightweight management server (**PocketBase**), and returns strictly structured JSON payloads back to the requesting backend.

By leveraging an event-driven architecture, this service eliminates the overhead of HTTP web servers (like FastAPI), running purely as an asynchronous background worker optimized for AI and speech-to-text processing.

## 🚀 Tech Stack & Core Systems

- **Taskiq & taskiq-aio-pika** – Modern, pure-asynchronous (`asyncio`-first) task queue framework for Python.
- **RabbitMQ** – High-performance message broker managing asynchronous service-to-service communication.
- **PocketBase (SQLite)** – Embedded configuration system providing a Web Admin UI to store, version, and edit system prompts in real-time without service redeployment.
- **LangChain & Groq API** – High-speed LLM integration using `with_structured_output` for zero-shot intent parsing and strict schema extraction.
- **Whisper (STT)** – Automated audio-to-text pipeline for handling voice command files.
- **Pure Worker Architecture** – Completely stateless; contains no public HTTP endpoints, operating entirely through message queues.

---

## 🛠 Architectural Data Flow

