# Judgment Labs Agent Integration & Testing

This repository contains a complete agent implementation integrated with Judgment Labs' evaluation tools, plus systematic testing that identified 8 real issues in their platform.

## **Setup Instructions**

### **Prerequisites**
- Python 3.11+
- OpenAI API key
- Judgment Labs API key and Organization ID

### **Installation**

```bash
# Create virtual environment (REQUIRED - see issues found)
python -m venv judgment_env
judgment_env\Scripts\activate  # Windows
source judgment_env/bin/activate  # Mac/Linux

# Install dependencies
pip install judgeval openai python-dotenv

# Set environment variables
set JUDGMENT_API_KEY=your_api_key_here
set JUDGMENT_ORG_ID=your_org_id_here
set OPENAI_API_KEY=your_openai_key
```

### **Get API Keys**
1. Judgment Labs: https://app.judgmentlabs.ai/register
2. OpenAI: https://platform.openai.com/api-keys

## **Files Overview**

### **Core Agent**
- `research_agent.py` - Main research assistant agent with tracing
- `evaluation_suite.py` - Comprehensive evaluation testing

### **Testing & Utilities**
- `integration_tests.py` - Various integration patterns
- `complete_test.py` - End-to-end testing

## **Running the Agent**

### **Basic Agent Test**
```bash
python research_agent.py
```

**Expected Output:**
- Research reports for 3 topics
- Traces sent to Judgment platform (with warnings about HTTP 500 errors)
- Evaluation results

### **Systematic Testing**
```bash

# Test evaluation suite  
python evaluation_suite.py
```
