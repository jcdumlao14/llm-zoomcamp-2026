# AI Copilot: Automating Workflow Generation

## Table of Contents

1. [Overview](#overview)
2. [What is AI Copilot](#what-is-ai-copilot)
3. [How It Works](#how-it-works)
4. [Prompt Engineering](#prompt-engineering)
5. [Best Practices](#best-practices)
6. [Comparison with ChatGPT](#comparison-with-chatgpt)
7. [Advanced Techniques](#advanced-techniques)

---

## Overview

Kestra's **AI Copilot** feature enables users to generate workflows using natural language prompts. Instead of manually writing YAML, you can describe what you want to accomplish, and AI generates the corresponding Kestra workflow.

This reduces development time and helps developers who are unfamiliar with Kestra syntax.

---

## What is AI Copilot

**Definition**: An AI-powered assistant that generates code (in this case, Kestra YAML) from natural language descriptions.

**Key Features**:

- 🤖 Natural language interface
- ⚡ Fast workflow generation
- 📝 Syntax validation
- 🔧 Integration with Kestra editor
- 🎯 Context-aware suggestions

**Benefits**:

- Faster workflow creation
- Lower barrier to entry
- Reduced syntax errors
- Learning by example
- Improved productivity

---

## How It Works

### Step 1: Access AI Copilot

In the Kestra Dashboard:

1. Click **"Create Flow"**
2. Select **"Generate with AI"** (or similar option)
3. Enter your prompt in the text field

### Step 2: Write Your Prompt

Describe the workflow you want to create. Be specific and detailed.

**Good Prompt**:
```
Create a workflow that:
1. Calls the Gemini API with a question
2. Extracts the response
3. Logs the result
4. Uses the GEMINI_API_KEY secret
```

**Vague Prompt** (avoid):
```
Make a chat flow
```

### Step 3: Generate

Click **"Generate"** and AI creates a YAML workflow based on your description.

### Step 4: Review and Refine

1. Review the generated YAML
2. Make any necessary adjustments
3. Test the flow
4. Deploy if satisfied

---

## Prompt Engineering

### Effective Prompts

**Structure**:

```
Create a Kestra workflow that:
1. [Task 1]: [Details about task 1]
2. [Task 2]: [Details about task 2]
3. [Task 3]: [Details about task 3]

Configuration:
- Use [API/Service]: [API details]
- Input: [Expected input format]
- Output: [Expected output format]
```

**Example**:

```
Create a Kestra workflow that:
1. Accepts a search query as input
2. Calls the Gemini API to answer the question
3. Extracts the response text
4. Logs the response with token usage information

Configuration:
- Use Gemini API with secret GEMINI_API_KEY
- Input: STRING type named 'query'
- Output: STRING type with the API response
- Set temperature to 0.7 and max tokens to 500
```

### Tips for Better Results

1. **Be Specific**: Use exact API names, parameter names
2. **Use Lists**: Number steps for clarity
3. **Include Context**: Mention APIs, services, or tools
4. **Specify Configuration**: Temperature, tokens, authentication
5. **Define I/O**: Clearly state inputs and outputs
6. **Use Task Names**: Suggest task IDs for clarity

### Poor vs Good Prompts

**Poor**:
```
Make a workflow that processes data and calls an API
```

**Good**:
```
Create a Kestra workflow that:
1. Reads a CSV file from a URL
2. Extracts the 'question' column
3. Sends each question to Gemini API
4. Logs the responses
Use GEMINI_API_KEY secret for authentication
```

---

## Best Practices

### 1. Start Simple

Begin with basic workflows and gradually add complexity.

```
First: Create a simple HTTP request flow
Then: Add error handling and logging
Finally: Add conditional logic and retries
```

### 2. Use Examples

Reference existing flows or patterns in your prompts.

```
Similar to the 1_chat_without_rag.yaml flow, create a flow that:
- Does [additional requirement]
- With [additional feature]
```

### 3. Iterate

Don't expect perfection on the first generation.

- Generate initial flow
- Test and identify issues
- Ask AI to fix specific problems
- Refine incrementally

### 4. Validate Generated Code

Always review generated workflows for:
- Correct API endpoints
- Proper authentication
- Accurate parameter names
- Valid task types
- Correct variable syntax

### 5. Add Comments

Enhance readability with descriptions.

```yaml
description: >
  Workflow that retrieves data from an API,
  processes it, and stores results in a database.
```

---

## Comparison with ChatGPT

### AI Copilot vs ChatGPT

| Aspect | AI Copilot | ChatGPT |
|--------|-----------|---------|
| **Integration** | Built into Kestra | Standalone web interface |
| **Context** | Aware of Kestra syntax | General knowledge |
| **Output** | Direct YAML insertion | Copy-paste to Kestra |
| **Validation** | Real-time Kestra validation | Manual validation required |
| **Learning Curve** | Quick for Kestra users | Requires YAML knowledge |
| **Speed** | Instant in Kestra | Browser-dependent latency |
| **Customization** | Kestra-specific | Generic code generation |

### When to Use Each

**Use AI Copilot for**:
- Quick Kestra workflow generation
- Staying in the Kestra UI
- Leveraging Kestra-specific context
- Testing workflows immediately

**Use ChatGPT for**:
- Learning Kestra fundamentals
- Complex algorithm explanation
- Troubleshooting non-Kestra issues
- Generating Python/other code

### Hybrid Approach

1. **Plan** with ChatGPT: Outline workflow architecture
2. **Generate** with AI Copilot: Create YAML from plan
3. **Refine** with ChatGPT: Fix issues or add complexity
4. **Test** in Kestra: Validate and deploy

---

## Advanced Techniques

### Technique 1: Template-Based Generation

Provide a template to guide AI output:

```
Using this template structure:
id: [meaningful-name]
namespace: homework
tasks:
  - id: [task-name]
    type: [kestra-plugin]

Create a flow that [your requirement]
```

### Technique 2: Multi-Step Refinement

Start broad, then narrow down:

**First Prompt**:
```
Generate a RAG workflow in Kestra
```

**Follow-up Prompt**:
```
Modify the previous workflow to:
- Use vector embeddings for search
- Retrieve top 3 documents
- Pass them to Gemini as context
```

### Technique 3: Error-Driven Refinement

If generated code has errors:

```
The previous flow failed with this error: [error message]
Fix the flow to resolve this issue.
```

### Technique 4: Performance Optimization

Ask for optimization after initial generation:

```
Optimize the previous flow for:
- Lower token usage
- Faster execution
- Parallel task execution
```

---

## Homework Question 1: Copilot vs ChatGPT

### Comparison Task

1. **In Kestra AI Copilot**, generate:
   ```
   Create a Kestra workflow that calls Gemini API 
   and returns a formatted response
   ```

2. **In ChatGPT**, ask:
   ```
   How would you create a Kestra workflow that 
   calls Gemini API and returns a formatted response?
   ```

3. **Compare**:
   - Code quality
   - Syntax accuracy
   - Completeness
   - Integration readiness
   - Learning value

4. **Document observations** in `docs/homework-answers.md`

---

## Resources

- [Kestra AI Copilot Documentation](https://kestra.io/docs)
- [Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [ChatGPT for Code Generation](https://chat.openai.com)

---

**Last Updated**: July 3, 2026
