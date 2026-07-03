<<<<<<< HEAD

=======
# AI Orchestration with Kestra – Module 3 Homework

## Overview

This repository contains the practical exercises and homework completed for **Module 3: AI Orchestration with Kestra** from the LLM Zoomcamp 2026 course.

This repository demonstrates:

- **AI Workflows**: Building orchestrated workflows with Kestra
- **AI Copilot**: Generating workflows using AI assistance
- **Context Engineering**: Structuring prompts and context for LLMs
- **Retrieval-Augmented Generation (RAG)**: Enhancing AI responses with external data
- **AI Agents**: Creating autonomous agents that reason and act
- **Multi-Agent Systems**: Coordinating multiple specialized agents
- **Production Best Practices**: Observability, security, compliance, and cost optimization

---

## Learning Objectives

- ✅ Understand AI orchestration principles
- ✅ Build Kestra workflows from scratch
- ✅ Learn context engineering techniques
- ✅ Generate workflows using AI Copilot
- ✅ Build RAG pipelines for grounded responses
- ✅ Execute AI agents with reasoning capabilities
- ✅ Build multi-agent workflows with specialized roles
- ✅ Learn production best practices for AI systems

---

## Technologies Used

- **Kestra**: Workflow orchestration platform
- **Docker & Docker Compose**: Containerization and local deployment
- **Gemini API**: Google's generative AI models
- **YAML**: Workflow configuration language
- **AI Copilot**: Workflow generation assistance
- **RAG**: Retrieval-Augmented Generation techniques
- **Git & GitHub**: Version control and collaboration

---

## Prerequisites

Before running the workflows, ensure you have:

- **Docker Desktop**: For running Kestra locally
- **Git**: For version control
- **Gemini API Key**: From [Google AI Studio](https://aistudio.google.com)
- **Kestra**: Installed and running (via Docker)
- **Internet Connection**: For API calls and model access

---

## Installation

### Step 1: Clone Repository

```bash
git clone <repository_url>
```

### Step 2: Open Folder

```bash
cd module-03-ai-orchestration-kestra
```

### Step 3: Start Kestra

```bash
docker compose up
```

Kestra will start on your local machine. The Docker Compose file is assumed to be in the parent directory or can be created with:

```bash
# If no docker-compose.yml exists, create one:
docker run --rm -it -p 8080:8080 kestra/kestra server standalone
```

### Step 4: Open Browser

Navigate to:

```
http://localhost:8080
```

You should see the Kestra dashboard.

### Step 5: Configure Gemini API Key

1. Obtain your API key from [Google AI Studio](https://aistudio.google.com)
2. In the Kestra UI, navigate to **Settings → Secrets**
3. Create a new secret named `GEMINI_API_KEY` with your API key value
4. Alternatively, add it to your `.env` file (see `configs/example.env`)

---

## Importing Flows

All workflow YAML files in the `flows/` folder should be imported into Kestra:

1. In the Kestra dashboard, go to **Namespaces**
2. Select your namespace
3. Click **Create Flow** → **Edit as YAML**
4. Copy the contents of each YAML file and paste it into the editor
5. Click **Save**

The flows are:

- `1_chat_without_rag.yaml` - Simple chat without retrieval
- `2_chat_with_rag.yaml` - Chat augmented with RAG
- `3_*.yaml` - Advanced flows (context engineering, multi-agent)
- `4_simple_agent.yaml` - Basic AI agent with tools
- `additional_flows.yaml` - Extra workflows for exploration

---

## Running the Homework

### Question 1: Compare ChatGPT vs AI Copilot

**Objective**: Compare ChatGPT with Kestra's AI Copilot for workflow generation.

**Steps**:

1. Open Kestra Dashboard (http://localhost:8080)
2. Navigate to **Create Flow → Generate with AI Copilot**
3. Describe a simple workflow prompt, e.g., "Create a workflow that calls Gemini API and logs the response"
4. Compare the output with equivalent workflows in ChatGPT
5. Record observations about:
   - Code quality
   - Completeness
   - YAML syntax accuracy
   - Integration with Kestra

**Where to store results**: `screenshots/q1/` and `docs/homework-answers.md`

---

### Question 2: Compare Chat Without RAG vs With RAG

**Objective**: Understand the difference between responses with and without RAG.

**Steps**:

1. Import and run `1_chat_without_rag.yaml`:
   - Execute the flow
   - Record the execution logs
   - Note the response quality and token usage

2. Import and run `2_chat_with_rag.yaml`:
   - Execute the flow
   - Record the execution logs
   - Compare the response quality vs non-RAG version

**Analysis**:

- Compare output accuracy
- Compare token usage
- Note differences in response grounding
- Observe retrieval quality

**Where to store results**: `screenshots/q2/` and `docs/homework-answers.md`

---

### Question 3: Measure Token Usage (Short Summary)

**Objective**: Measure output token usage with `summary_length = short`.

**Steps**:

1. Import `4_simple_agent.yaml`
2. Configure the agent with:
   - `summary_length = short`
   - Run a test query
3. Record:
   - Output tokens used
   - Response length
   - Execution time

**Where to store results**: `screenshots/q3/` and `docs/homework-answers.md`

---

### Question 4: Compare Token Usage (Long Summary)

**Objective**: Compare token usage when increasing summary length to `long`.

**Steps**:

1. Run `4_simple_agent.yaml` again with:
   - `summary_length = long`
2. Record:
   - Output tokens used
   - Response length
   - Execution time
3. Compare with Question 3 results

**Analysis**:

- How much did output tokens increase?
- What's the token cost difference?
- Is the extra detail worth the cost?

**Where to store results**: `screenshots/q4/` and `docs/homework-answers.md`

---

### Question 5: Modify Context and Measure Impact

**Objective**: Modify system prompts to understand token cost impacts.

**Steps**:

1. Modify `4_simple_agent.yaml`:
   - Change `english_brevity` constraint from:
     ```
     Exactly 1 sentence
     ```
   - To:
     ```
     Exactly 3 sentences
     ```
2. Save the changes
3. Run the flow again
4. Record:
   - Output tokens used
   - Response length
   - Execution time

**Analysis**:

- How much did token usage increase?
- Was the increase proportional to the content expansion?
- What's the token cost per additional sentence?

**Where to store results**: `screenshots/q5/` and `docs/homework-answers.md`

---

### Question 6: Production Best Practices

**Objective**: Summarize production best practices for AI workflows.

**Topics to cover**:

- Observability and monitoring
- Deterministic workflows
- Error handling and retries
- Compliance and governance
- Security and secrets management
- Token cost optimization
- Rate limiting and throttling
- Caching strategies
- Version control for workflows

**Where to store results**: `docs/homework-answers.md`

---

## Homework Results

Track completion of all homework questions:

| Question | Completed | Notes |
|----------|-----------|-------|
| Q1 | ⬜ | Compare ChatGPT vs Copilot |
| Q2 | ⬜ | Compare RAG vs Non-RAG |
| Q3 | ⬜ | Token usage (short) |
| Q4 | ⬜ | Token usage (long) |
| Q5 | ⬜ | Context modification impact |
| Q6 | ⬜ | Best practices summary |

**Legend**: ⬜ = Not started, 🟨 = In progress, ✅ = Completed

---

## Screenshots

Screenshots and execution results are organized by question:

```
screenshots/
├── setup/          # Kestra setup and configuration screenshots
├── q1/             # AI Copilot comparison screenshots
├── q2/             # RAG vs Non-RAG comparison
├── q3/             # Token usage (short summary)
├── q4/             # Token usage (long summary)
├── q5/             # Context modification results
└── q6/             # Best practices documentation
```

Include:
- Kestra dashboard screenshots
- Flow execution logs
- Token usage metrics
- Response comparisons

---

## Notes

Lesson summaries and reference materials are stored in `docs/`:

- **`setup-guide.md`**: Installation and configuration guide
- **`ai-copilot.md`**: AI Copilot usage and prompt engineering
- **`rag.md`**: Retrieval-Augmented Generation concepts
- **`agents.md`**: AI agents and autonomous reasoning
- **`multi-agent.md`**: Multi-agent system architecture
- **`best-practices.md`**: Production deployment best practices
- **`homework-answers.md`**: Complete homework answers and results

---

## Repository Structure

```
module-03-ai-orchestration-kestra/
│
├── README.md                          # This file
│
├── flows/                             # Kestra YAML workflows
│   ├── 1_chat_without_rag.yaml
│   ├── 2_chat_with_rag.yaml
│   ├── 3_context_engineering.yaml
│   ├── 4_simple_agent.yaml
│   └── additional_flows.yaml
│
├── docs/                              # Documentation and notes
│   ├── module-notes.md
│   ├── setup-guide.md
│   ├── ai-copilot.md
│   ├── rag.md
│   ├── agents.md
│   ├── multi-agent.md
│   ├── best-practices.md
│   └── homework-answers.md
│
├── screenshots/                       # Execution results and screenshots
│   ├── setup/
│   ├── q1/
│   ├── q2/
│   ├── q3/
│   ├── q4/
│   ├── q5/
│   └── q6/
│
├── assets/                            # Static assets and diagrams
│   └── architecture.png
│
├── configs/                           # Configuration examples
│   ├── example.env
│   └── secrets-example.md
│
└── LICENSE
```

---

## Future Improvements

Potential enhancements for advanced learning:

- 🔹 **More AI Agents**: Build specialized agents for different domains
- 🔹 **Larger RAG Datasets**: Work with more comprehensive document collections
- 🔹 **Cloud Deployment**: Deploy to Google Cloud Run or AWS Lambda
- 🔹 **Observability Dashboards**: Set up monitoring with Prometheus/Grafana
- 🔹 **Workflow Monitoring**: Implement alerting for workflow failures
- 🔹 **CI/CD Automation**: Automate workflow testing and deployment
- 🔹 **Performance Optimization**: Profile and optimize token usage
- 🔹 **Advanced RAG**: Implement hybrid search and re-ranking strategies

---

## Contributing

Feel free to modify flows, add notes, and experiment with different configurations. All changes should be documented in the relevant sections.

---

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

## Resources

- [Kestra Documentation](https://kestra.io/docs)
- [Google Gemini API](https://ai.google.dev)
- [RAG Best Practices](https://python.langchain.com/docs/use_cases/question_answering)
- [AI Agents Guide](https://arxiv.org/abs/2401.02704)

---

**Last Updated**: July 3, 2026  
**Course**: LLM Zoomcamp 2026 – Module 3  
**Author**: [Your Name]
>>>>>>> 2b54948 (Module 3 setup with official Kestra flows)
