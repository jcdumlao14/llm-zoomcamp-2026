# Setup Guide: AI Orchestration with Kestra

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installing Docker](#installing-docker)
3. [Starting Kestra](#starting-kestra)
4. [Creating API Keys](#creating-api-keys)
5. [Importing Flows](#importing-flows)
6. [Verification](#verification)
7. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements

- **CPU**: 2 cores (4 cores recommended)
- **RAM**: 4 GB (8 GB recommended)
- **Disk**: 10 GB available space
- **OS**: Linux, macOS, or Windows with Docker

### Required Software

- **Docker Desktop** (20.10+)
- **Docker Compose** (2.0+)
- **Git**
- **Text Editor** (VS Code recommended)
- **Web Browser** (Chrome, Firefox, Safari, or Edge)

---

## Installing Docker

### macOS

1. Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop)
2. Open the `.dmg` file and drag Docker to Applications
3. Launch Docker from Applications
4. Verify installation:

```bash
docker --version
docker-compose --version
```

### Linux (Ubuntu/Debian)

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Verify installation
docker --version
docker-compose --version
```

### Windows

1. Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop)
2. Run the installer and follow prompts
3. Restart your computer
4. Verify installation:

```bash
docker --version
docker-compose --version
```

---

## Starting Kestra

### Option 1: Using Docker Compose (Recommended)

Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  kestra:
    image: kestra/kestra:latest
    container_name: kestra
    ports:
      - "8080:8080"
      - "8081:8081"
    environment:
      KESTRA_CONFIGURATION: |
        server:
          ssl: false
        kestra:
          repository:
            type: memory
          datastore:
            type: memory
          queue:
            type: memory
          cache:
            type: memory
    command: server standalone
```

Start Kestra:

```bash
docker-compose up
```

### Option 2: Using Docker Run Directly

```bash
docker run -d \
  -p 8080:8080 \
  --name kestra \
  kestra/kestra:latest \
  server standalone
```

### Verification

1. Open your browser: `http://localhost:8080`
2. You should see the Kestra dashboard
3. Check the logs:

```bash
docker logs kestra
```

---

## Creating API Keys

### Obtaining a Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com)
2. Click **"Get API Key"** in the left menu
3. Select **"Create API key in new project"**
4. Copy the generated API key
5. Keep it secure (don't share it)

### Storing API Key in Kestra

#### Method 1: Secrets UI (Recommended)

1. In Kestra dashboard, navigate to **Settings**
2. Find **"Secrets"** section
3. Click **"Add Secret"**
4. Enter:
   - **Key**: `GEMINI_API_KEY`
   - **Value**: `<your-api-key>`
5. Click **"Save"**

#### Method 2: Environment Variables

```bash
export GEMINI_API_KEY=<your-api-key>
docker-compose up
```

#### Method 3: Configuration File

Add to `docker-compose.yml`:

```yaml
services:
  kestra:
    environment:
      KESTRA_SECRETS_GEMINI_API_KEY: '<your-api-key>'
```

---

## Importing Flows

### Manual Import via UI

1. Navigate to your namespace in Kestra
2. Click **"Create Flow"** → **"Edit as YAML"**
3. Copy the contents of a YAML file from `flows/` directory
4. Paste into the editor
5. Click **"Save"**
6. Click **"Deploy"**

### Example: Importing the First Flow

1. Open [1_chat_without_rag.yaml](../flows/1_chat_without_rag.yaml)
2. Copy the entire contents
3. In Kestra UI, create a new flow
4. Paste the YAML
5. Click **"Save and Deploy"**
6. Click **"Execute"** to test

### Batch Import

For importing multiple flows:

```bash
# Create a script to import flows
for file in flows/*.yaml; do
  echo "Importing $file..."
  # Use Kestra API or CLI to import
done
```

---

## Verification

### Check Kestra Status

1. Visit `http://localhost:8080`
2. Dashboard should be accessible
3. Navigate to **Namespaces** to verify setup

### Test API Connection

Create a test flow:

```yaml
id: test_gemini_connection
namespace: homework
description: Test Gemini API connectivity

tasks:
  - id: test_request
    type: io.kestra.plugin.core.http.Request
    uri: https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent
    method: POST
    headers:
      Content-Type: application/json
    body: |
      {
        "contents": [
          {
            "parts": [
              {
                "text": "Say 'Hello, Kestra!'"
              }
            ]
          }
        ]
      }
    auth:
      type: BASIC
      username: "{{ secret('GEMINI_API_KEY') }}"

  - id: log_result
    type: io.kestra.plugin.core.log.Log
    message: "{{ outputs.test_request.body }}"
```

Run this flow and check the logs for a successful response.

---

## Troubleshooting

### Docker Issues

**Problem**: Docker daemon is not running

```bash
# Solution: Start Docker
# macOS: Open Docker Desktop from Applications
# Linux: systemctl start docker
# Windows: Open Docker Desktop from Start menu
```

**Problem**: Port 8080 is already in use

```bash
# Solution: Use a different port
docker run -d -p 8081:8080 kestra/kestra:latest server standalone
# Then access: http://localhost:8081
```

### Kestra Issues

**Problem**: Cannot access Kestra dashboard

```bash
# Solution: Check if container is running
docker ps | grep kestra

# If not running, start it
docker-compose up
```

**Problem**: API key not working

1. Verify API key is correct (no extra spaces)
2. Ensure API key has proper permissions
3. Check if API is enabled in Google Console
4. Verify the secret name matches in the flow

### Network Issues

**Problem**: Kestra cannot reach Gemini API

```bash
# Solution: Check internet connection
ping google.com

# Verify firewall allows HTTPS
curl https://generativelanguage.googleapis.com -v
```

### Memory Issues

**Problem**: Docker container keeps crashing

```yaml
# Increase memory in docker-compose.yml
services:
  kestra:
    deploy:
      resources:
        limits:
          memory: 2G
```

---

## Next Steps

1. ✅ Start Kestra: `docker-compose up`
2. ✅ Access dashboard: `http://localhost:8080`
3. ✅ Create API key
4. ✅ Store API key as secret
5. ✅ Import first flow
6. ✅ Run a test execution
7. 📖 Read [ai-copilot.md](ai-copilot.md) for next lesson

---

**Last Updated**: July 3, 2026
