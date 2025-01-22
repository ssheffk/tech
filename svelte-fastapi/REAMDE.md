# How to Dockerize a FastAPI Backend and Svelte Frontend Locally with Docker Compose

In this guide, we’ll walk through setting up a **FastAPI** backend and a **Svelte** frontend using **Docker Compose** for seamless local development. We’ll also integrate an external cloud-hosted MongoDB database accessed via a connection URL.

## Project Structure

Here’s the general structure of the project:

```
project-root/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── main.py
├── web/
│   ├── Dockerfile
│   ├── package.json
│   ├── svelte.config.js
│   └── src/
└── docker-compose.yml
```

## Backend: FastAPI

The backend is a FastAPI app with a `Dockerfile` that sets up the environment and runs the app.

### Backend Dockerfile

```dockerfile
# Backend Dockerfile
FROM python:3.11-slim

WORKDIR /

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9001"]
```

### Example `requirements.txt`

Make sure to include the necessary dependencies for your FastAPI app:

```
fastapi
uvicorn
pymongo
```

### Example `main.py`

Here’s a simple example of your FastAPI app:

```python
from fastapi import FastAPI
from pymongo import MongoClient
import os

app = FastAPI()

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client.get_default_database()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
```

## Frontend: Svelte

The frontend is built with Svelte, using the Node.js adapter for deployment.

### Frontend Dockerfile

```dockerfile
# Use a Node.js Alpine image for the builder stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
RUN npm prune --production

# Use another Node.js Alpine image for the final stage
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/build build/
COPY --from=builder /app/node_modules node_modules/
COPY package.json .
EXPOSE 3000
ENV NODE_ENV=production
CMD [ "node", "build/index.js" ]
```

### Svelte Configuration

Your `svelte.config.js` should use the Node.js adapter:

```javascript
import adapter from '@sveltejs/adapter-node';

export default {
  kit: {
    adapter: adapter(),
    prerender: {
      enabled: false,
    },
  },
};
```

## Docker Compose Configuration

Here’s the `docker-compose.yml` file that ties everything together:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: fastapi-backend
    ports:
      - '9001:9001'
    environment:
      - MONGO_URI=your_mongo_connection_string

  frontend:
    build:
      context: ./web
      dockerfile: Dockerfile
    container_name: svelte-frontend
    ports:
      - '3000:3000'
    depends_on:
      - backend
```

## Running the Project Locally

1. **Build the Docker images:**

   ```bash
   docker-compose build
   ```

2. **Start the containers:**

   ```bash
   docker-compose up
   ```

3. **Access the services:**

   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend: [http://localhost:9001](http://localhost:9001)

## Troubleshooting Common Issues

### Issue: Cannot Connect to MongoDB

- **Error**: “Failed to connect to MongoDB server.”
- **Solution**: Ensure your `MONGO_URI` is correct and accessible from your local machine. Use `docker logs fastapi-backend` to debug.

### Issue: Frontend Not Communicating with Backend

- **Error**: “Network Error” or CORS issues.
- **Solution**: Make sure the frontend points to the backend URL (e.g., `http://localhost:9001`). If needed, add CORS middleware to FastAPI:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Conclusion

With this setup, you’ve successfully dockerized a FastAPI backend and Svelte frontend, integrating them locally using Docker Compose. This approach ensures a smooth development workflow and consistent environment across systems.
