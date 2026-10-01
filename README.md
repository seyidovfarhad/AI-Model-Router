# AI Router

A backend service that supports three-level routing to minimize language model usage costs for the website of a hypothetical mobile phone, the **Phone X Pro**. Depending on the request, the router directs it to one of three handlers.

# Idea

Real-world systems handle many **repetitive** queries (such as "how do I reset my password" or "where do I pay for my order") and a smaller number of **unique** ones. Routing everything through the most powerful (and slow/expensive) model is wasteful. The project implements three levels of filtering before a request reaches the most resource-intensive model:

1. **Keyword match** — a check to see if one of the keywords is present in the query. If a keyword is found and the query is relatively short, it is likely a **recurring question**. In this case, a pre-prepared answer is returned. Otherwise, `None` is returned.
2. **Vector similarity search** is a method for finding a similar query within a question-and-answer database. If a specific keyword is missing from the question, the embedding model compares the query against all the keys associated with existing answers; if the similarity score **exceeds 0.65**, the value corresponding to that key is likely the answer to the query and is returned. Otherwise, `None` is returned.
3. **Large Language Model** — if the router receives  `None` from all preceding functions, the request is redirected to the language model.

# Retry logic

The response generation function utilizing the language model employs the **OpenRouter API**  provider; consequently, it incorporates **retry logic with exponential backoff** and handles various types of network errors.

# Savings metric

When using paid large language models, such a project minimizes costs. However, since this is a demo project, a **free language model** is used, and the metric for cost savings is **request execution time**.

# Routing logic

The `Router` class used in the `generate()` function can operate in two modes: **optimal and non-optimal**. In the optimal mode, routing logic is executed. In the non-optimal mode, all requests are passed directly to the language model for processing. By default, the `generate()` function operates in the optimal mode. However, even in this case, the request is sent to both the router and the language model; consequently, the response is slow. This setup is intended to display comparative statistics. In a real-world project, the response should be delivered as quickly as possible. Since this project is designed to demonstrate the cost savings achieved through routing, the `generate()` function performs both processing methods to illustrate those savings.



# Installation and Run Instructions

This document provides step-by-step instructions for running the FastAPI application both locally and via Docker.

## 1. Local Setup

### Prerequisites

* Python 3.9 or higher.

### Step-by-Step Guide

1. **Clone the repository and navigate to the project directory**:

```bash
cd <project_name>
```

2. **Create and activate a virtual environment:**

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```



**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
   The `/chat` endpoint (`generate()` function) requires an API key. Set it in your terminal before running the application:

**Linux / macOS:**

```bash
export API_KEY="your_secret_api_key"
```



**Windows (PowerShell):**

```bash
$env:API_KEY="your_secret_api_key"
```

5. **Run the application:**
   
   ```bash
   python main.py
   ```
   
   The application will be accessible locally at: `http://127.0.0.1:8000`
   
   

2. ## Running with Docker
   
   If you prefer running the project inside an isolated container, you can build the Docker image directly on your machine.
   
   

## Prerequisites for Docker

Ensure your project root folder contains a `Dockerfile` and a `requirements.txt` file alongside `main.py`. If you don't have a `Dockerfile` yet, create one with the following contents.

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
```



### Step-by-Step Guide

1. **Build the Docker image:**

Run the following command in the root folder of the project to build the image locally:

```bash
docker build -t fastapi-app .
```

2. **Run the container**:
   
   Pass your API key using the `-e` flag and map port `8000`:
   
   ```bash
   docker run -d -p 8000:8000 -e API_KEY="your_secret_api_key" --name fastapi-container fastapi-app
   ```
   
   Once running, the application will be available at `http://127.0.0.1:8000`, and the interactive API documentation can be found at `http://127.0.0.1:8000/docs`.

# Main Endpoints

* POST /chat` — Handled by the `generate()` function (requires the API key).
* `GET /getComparisonStat` — Handled by the `get_statistics()` function.
