

# Chainlit Chatbot with OpenAI Agents
A simple Chainlit-based chatbot project using openai-agents.


### 📁 Getting Started

### 1️⃣ Install UV 
First, install UV (if not already installed):
```bash
pip install uv
```

Check version:
```bash
uv --version
```


### 2️⃣ Create and Initialize the Project
```bash
uv init vs-code-example-Gemini-with-auth
cd vs-code-example-Gemini-with-auth
```



### 3️⃣ Install Dependencies
```bash
uv add chainlit google-generativeai python-dotenv
```

### 4️⃣ Activate UV Virtual Environment (Windows)
```bash
.venv\Scripts\activate

```

### 5️⃣ Try Chainlit Hello
```bash
chainlit hello
```


### 6️⃣ Create .env file
* GEMINI_API_KEY=your_gemini_api_key
* OAUTH_GITHUB_CLIENT_ID=your_github_client_id
* OAUTH_GITHUB_CLIENT_SECRET=your_github_client_secret
* CHAINLIT_AUTH_SECRET=your_chainlit_auth_secret


1. Get Google Gemini API key from here
2. Get GitHub OAuth Client ID and Client Secret from here

**Generate chainlit auth secret with the following command:**
```bash
chainlit create-secret
```

