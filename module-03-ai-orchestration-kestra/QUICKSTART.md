# Quick Start Guide

Get up and running with Module 3 in 5 minutes!

## Prerequisites

- Docker Desktop installed
- Git installed
- Gemini API key from [Google AI Studio](https://aistudio.google.com)

## 5-Minute Setup

### Step 1: Start Kestra (1 min)

```bash
cd module-03-ai-orchestration-kestra
docker-compose up
```

Open: `http://localhost:8080`

### Step 2: Add API Key (1 min)

In Kestra UI:
1. Settings → Secrets
2. Add Secret: `GEMINI_API_KEY` = `your-key`
3. Save

### Step 3: Import First Flow (1 min)

1. Click "Create Flow" → "Edit as YAML"
2. Copy contents of `flows/1_chat_without_rag.yaml`
3. Paste into editor
4. Click "Save"

### Step 4: Run Flow (1 min)

1. Click "Execute"
2. View logs
3. See the response!

### Step 5: View Documentation (1 min)

Read through:
- `docs/module-notes.md` - Overview
- `docs/setup-guide.md` - Detailed setup
- `docs/rag.md` - RAG concepts

## Homework Sequence

### Q1: Compare Tools
- **Time**: 20 minutes
- **Files**: ChatGPT vs Kestra AI Copilot
- **Output**: `docs/homework-answers.md` (Q1 section)

### Q2: RAG Comparison
- **Time**: 30 minutes
- **Run**: `1_chat_without_rag.yaml` + `2_chat_with_rag.yaml`
- **Output**: `docs/homework-answers.md` (Q2 section)

### Q3: Token Usage (Short)
- **Time**: 15 minutes
- **Run**: `4_simple_agent.yaml` with `summary_length: short`
- **Record**: Token counts in `docs/homework-answers.md`

### Q4: Token Usage (Long)
- **Time**: 15 minutes
- **Run**: `4_simple_agent.yaml` with `summary_length: long`
- **Compare**: Against Q3 results

### Q5: Context Modification
- **Time**: 20 minutes
- **Modify**: Flow to use 3 sentences instead of 1
- **Measure**: Token impact

### Q6: Best Practices
- **Time**: 30 minutes
- **Summarize**: Production practices from docs
- **Document**: In `docs/homework-answers.md`

**Total Time**: ~2-3 hours for full homework

## Common Commands

### Start Kestra
```bash
docker-compose up
```

### Stop Kestra
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f kestra
```

### Restart Everything
```bash
docker-compose down
docker-compose up
```

### Access Kestra UI
```
http://localhost:8080
```

## File Locations

| Item | Location |
|------|----------|
| Flows | `flows/*.yaml` |
| Documentation | `docs/*.md` |
| Homework Answers | `docs/homework-answers.md` |
| Screenshots (Q1) | `screenshots/q1/` |
| Screenshots (Q2) | `screenshots/q2/` |
| Screenshots (Q3) | `screenshots/q3/` |
| Screenshots (Q4) | `screenshots/q4/` |
| Screenshots (Q5) | `screenshots/q5/` |
| Screenshots (Q6) | `screenshots/q6/` |
| Config Example | `configs/example.env` |
| Secrets Guide | `configs/secrets-example.md` |

## Documentation Map

```
docs/
├── module-notes.md           # Start here (overview)
├── setup-guide.md            # Detailed setup instructions
├── ai-copilot.md             # Q1: Copilot comparison
├── rag.md                    # Q2: RAG concepts
├── agents.md                 # Q3-Q4: Agent patterns
├── multi-agent.md            # Advanced multi-agent systems
├── best-practices.md         # Q6: Production practices
└── homework-answers.md       # Submit answers here
```

## Troubleshooting

### Kestra won't start
```bash
# Check if port 8080 is in use
lsof -i :8080

# If in use, either:
# 1. Stop the other service
# 2. Use a different port in docker-compose.yml
```

### API key not working
```bash
# Verify it's stored correctly
# In Kestra Settings → Secrets, check GEMINI_API_KEY exists

# Test with a simple flow
# Check if the API key hasn't expired or been revoked
```

### Flow won't execute
```bash
# Check the error message in the logs
# Common issues:
# - Invalid YAML syntax
# - Secret not found (verify name)
# - API error (check internet connection)
```

## Next Steps After Homework

1. **Explore**: Try modifying the flows
2. **Build**: Create your own workflows
3. **Optimize**: Reduce token costs
4. **Deploy**: Move to production
5. **Scale**: Handle more queries

## Resources

- [Kestra Docs](https://kestra.io/docs)
- [Gemini API Docs](https://ai.google.dev)
- [RAG Guide](docs/rag.md)
- [Best Practices](docs/best-practices.md)

---

**Last Updated**: July 3, 2026  
**Estimated Total Time**: 2-3 hours
