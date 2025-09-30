# AI Model Deployment Workshop

Deploy your first AI model to the cloud in under 10 minutes using serverless infrastructure!

## Overview

This workshop teaches you how to deploy machine learning models using Modal, a serverless platform that handles all the infrastructure complexity. You'll build a sentiment analysis API that can analyze emotions in text and deploy it to production.

**What you'll learn:**
- Serverless vs traditional deployment
- How to deploy ML models to the cloud
- Creating production-ready APIs
- Monitoring and scaling deployments

**What you'll build:**
A live sentiment analysis API that:
- Analyzes emotions in text (positive, negative, neutral)
- Scales automatically from 0 to thousands of users
- Costs nothing when not in use
- Can be shared via URL immediately

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- A free Modal account (we'll create this during setup)
- Basic Python knowledge

## Setup Instructions

### 1. Clone or Download This Repository

```bash
git clone <your-repo-url>
cd model_deployment
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**If you get version errors**, run this instead:
```bash
pip install modal python-dotenv requests
pip install transformers torch --upgrade
pip install pillow fastapi pydantic
```

### 3. Run Modal Setup

```bash
python3 modal_setup.py
```

This will:
- Check if Modal is installed
- Open your browser to create a free Modal account
- Authenticate your computer with Modal
- Verify everything is working

**Important:** Follow the browser prompts to:
1. Sign up for Modal (completely free)
2. Authorize your computer
3. Return to the terminal

## Quick Start

### Deploy Your First Model

```bash
modal deploy sentiment_api.py
```

This command will:
1. Build a container image with your ML model
2. Deploy it to Modal's cloud infrastructure
3. Give you a public URL to use your API

**Expected output:**
```
✓ Created objects.
├── Created mount /home/you/model_deployment/sentiment_api.py
├── Created image im-...
└── Created sentiment-analyzer => https://your-username--sentiment-analyzer.modal.run
✓ App deployed!
```

Save that URL - that's your live API!

## Using Your Deployed API

### Test with curl

```bash
# Analyze positive sentiment
curl -X POST "https://your-username--sentiment-analyzer.modal.run/sentiment" \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this workshop!"}'

# Analyze negative sentiment  
curl -X POST "https://your-username--sentiment-analyzer.modal.run/sentiment" \
  -H "Content-Type: application/json" \
  -d '{"text": "This is terrible"}'

# Check API health
curl "https://your-username--sentiment-analyzer.modal.run/health"
```

### Test with Python

```python
import requests

# Your API URL from deployment
API_URL = "https://your-username--sentiment-analyzer.modal.run"

# Analyze sentiment
response = requests.post(
    f"{API_URL}/sentiment",
    json={"text": "Machine learning is fascinating!"}
)

result = response.json()
print(f"Sentiment: {result['label']}")
print(f"Confidence: {result['confidence']}")
print(f"Emoji: {result['emoji']}")
```

### Test with JavaScript

```javascript
// Your API URL from deployment
const API_URL = "https://your-username--sentiment-analyzer.modal.run";

// Analyze sentiment
fetch(`${API_URL}/sentiment`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    text: "This workshop is amazing!"
  })
})
.then(response => response.json())
.then(data => {
  console.log('Sentiment:', data.label);
  console.log('Confidence:', data.confidence);
});
```

## Understanding the Code

### sentiment_api.py Structure

```python
# 1. Define your Modal app
app = modal.App("sentiment-analyzer")

# 2. Specify what packages your model needs
image = modal.Image.debian_slim().pip_install([
    "transformers", "torch", "fastapi"
])

# 3. Create your ML function
@app.function(image=image)
def analyze_sentiment(text: str):
    # Load model and analyze text
    # This runs in Modal's cloud
    pass

# 4. Create web endpoints
@app.function()
@modal.asgi_app()
def fastapi_app():
    # FastAPI routes for HTTP access
    pass
```

### How Serverless Works

**Traditional Server:**
- Always running (24/7)
- You pay even when nobody uses it
- Fixed capacity - can crash if too many users

**Serverless (Modal):**
- Only runs when someone makes a request
- Pay only for compute time used (by the second)
- Automatically scales from 0 to 1000s of containers
- Costs $0 when not in use

### Cost Example

**Traditional server:** $50/month always running
**Serverless:** 
- 1000 requests/day = ~$0.50/month
- 10,000 requests/day = ~$5/month  
- 100,000 requests/day = ~$50/month

You only pay for what you use!

## Monitoring Your Deployment

### View in Modal Dashboard

1. Go to https://modal.com/apps
2. Find your `sentiment-analyzer` app
3. Click to see:
   - Request count
   - Response times
   - Error rates
   - Costs
   - Logs

### Check API Health

```bash
curl "https://your-username--sentiment-analyzer.modal.run/health"
```

Should return:
```json
{
  "status": "healthy",
  "service": "sentiment-analyzer",
  "model": "Twitter RoBERTa",
  "message": "Ready to analyze sentiment!"
}
```

## Common Issues & Solutions

### Issue: "modal: command not found"

**Solution:**
```bash
pip install modal --upgrade
# If still not found, add to PATH or use:
python -m modal setup
```

### Issue: "Could not find a version that satisfies the requirement torch==2.1.0"

**Solution:** You have Python 3.12+, use newer versions:
```bash
pip install torch>=2.5.0 transformers>=4.36.0
```

### Issue: "ExecutionError: Function has not been hydrated"

**Solution:** Don't try to test locally. Just deploy directly:
```bash
modal deploy sentiment_api.py
```

### Issue: Authentication fails

**Solution:**
```bash
# Try manual setup
modal token set --token-id YOUR_ID --token-secret YOUR_SECRET

# Or re-authenticate
modal setup
```

### Issue: Deployment is slow

**First deployment:** Takes 2-5 minutes (building container image)  
**Subsequent deployments:** Takes 30 seconds (uses cached image)

This is normal! Modal is building a container with all your dependencies.

## Next Steps

### Make It Your Own

1. **Change the model:**
   - Replace `"cardiffnlp/twitter-roberta-base-sentiment-latest"` with any Hugging Face model
   - Try: `"distilbert-base-uncased-finetuned-sst-2-english"` for faster inference

2. **Add features:**
   - Save results to a database
   - Add rate limiting
   - Return confidence scores for all categories

3. **Customize responses:**
   - Add more emoji mappings
   - Return explanations
   - Add multi-language support

### Build More Projects

**Image Classification:**
- Deploy a vision model
- Classify uploaded photos
- Use GPU for faster inference

**Text Generation:**
- Deploy GPT-2 or similar
- Build a writing assistant
- Create a chatbot

**Question Answering:**
- Deploy BERT for Q&A
- Build a knowledge base search
- Extract information from documents

## Resources

### Modal Documentation
- [Modal Docs](https://modal.com/docs)
- [Modal Examples](https://modal.com/docs/examples)
- [API Reference](https://modal.com/docs/reference)

### ML Model Resources
- [Hugging Face Models](https://huggingface.co/models)
- [Transformers Documentation](https://huggingface.co/docs/transformers)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

### Learning More
- [Serverless ML Blog](https://modal.com/blog)
- [ML Deployment Best Practices](https://developers.google.com/machine-learning/guides)
- [Production ML Guide](https://madewithml.com/)

## Workshop Concepts Review

### Key Terms

**Serverless:** Cloud computing model where you don't manage servers - just deploy code and it runs

**Container:** Packaged software with all dependencies - ensures your code runs the same everywhere

**API (Application Programming Interface):** Way for programs to communicate over the internet

**Inference:** Running a trained ML model to make predictions (vs training the model)

**Cold Start:** Time to spin up a new container from zero - first request is slower

**Scaling:** Automatically adding more compute resources when traffic increases

### Deployment Types Comparison

| Type | Best For | Cost | Complexity |
|------|----------|------|------------|
| **Serverless** | APIs, demos, sporadic use | Pay per use | Low |
| **Containers** | Production apps, always-on | Moderate | Medium |
| **VPS/Server** | Maximum control | High (always paying) | High |

**For ML models:** Serverless is ideal because:
- ML inference is usually sporadic (not constant)
- Models can be expensive to run continuously
- Automatic scaling handles traffic spikes
- No infrastructure management needed

## Add This to Your Resume

```
Deployed production machine learning models using serverless architecture
• Built and deployed sentiment analysis API using Modal and Transformers
• Implemented RESTful endpoints with FastAPI for model inference
• Configured auto-scaling infrastructure handling 1000+ concurrent requests
• Reduced deployment time from hours to minutes using containerization
```

## Credits

Created by ACM AI for the Fall 2025 workshop series.

Based on:
- Modal documentation and examples
- Hugging Face Transformers library  
- FastAPI framework

---

**Ready to deploy?** Run `modal deploy sentiment_api.py` and share your API URL with the world!