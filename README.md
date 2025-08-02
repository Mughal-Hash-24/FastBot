# 🤖 FASTBot – University Chat Assistant for FAST-NU Students

FASTBot is a Retrieval-Augmented Generation (RAG) powered conversational AI that helps students at FAST-NU with academic queries related to grading policies, course structure, faculty, and more. It leverages LangChain + Groq's LLaMA 3 via a local Chroma vector database to answer domain-specific questions accurately and efficiently.

## 🎯 Project Goal

To provide FAST-NU students with a personalized assistant that:
- Retrieves relevant information from university documents
- Uses a powerful LLM (LLaMA3-70B) to generate human-like, structured answers
- Offers context-aware responses with source references

## 🧠 How It Works

This project combines **LangChain**, **HuggingFace Embeddings**, **ChromaDB**, and **Groq's LLM** to enable contextual Q&A over academic documents.

### Architecture Overview

1. **Document Ingestion**: Course outlines, policies, and university docs are preprocessed and embedded using `sentence-transformers`
2. **Vector Store Creation**: ChromaDB stores the embeddings locally in `data/vector_store`
3. **Query Handling**: When a user types a question, LangChain:
   - Converts it into a query embedding
   - Searches the Chroma vector store for top `k` relevant chunks
   - Passes those chunks + the query into Groq's `llama3-70b-8192` model
4. **Answer Generation**: Groq LLM generates a concise, structured answer that may include markdown tables, lists, and insights based on context
5. **Frontend Interaction**: A user-friendly HTML page communicates with the FastAPI backend via `/chat`

## 📁 Project Structure

```
📦 FASTBot
┣ 📁 data/
┃ ┗ 📁 vector_store/        # Chroma DB with embedded documents
┣ 📁 logs/                  # Logs directory
┣ 📄 main.py                # FastAPI app + LangChain logic
┣ 📄 .env                   # Contains GROQ_API_KEY (not committed)
┣ 📄 .replit                # Replit-specific run config
┣ 📄 requirements.txt       # All Python dependencies
┗ 📄 README.md              # This file
```

## 🖥️ Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| 🧠 LLM | Groq + llama3-70b-8192 | Text generation |
| 🧠 Framework | LangChain | RAG pipeline |
| 📦 Vector DB | Chroma | Store and retrieve document embeddings |
| 🔤 Embedding | HuggingFace (MiniLM-L6-v2) | Converts text to vectors |
| 🌐 Backend | FastAPI | REST API |
| 🌍 Frontend | HTML/CSS + JavaScript | Simple chat UI |
| 🔐 Secrets | .env file | API Key storage |
| ☁️ Hosting | Replit + Vercel | Backend + Frontend deployment |

## 🚀 Workflow

```
User → [Frontend] → Sends query → [FastAPI Backend]
→ Embeds query → [Chroma Vector Store]
→ Retrieves relevant documents → [LangChain]
→ Adds context + query → [Groq LLM]
→ Generates answer → Returns response → [Frontend]
```

## ⚙️ Local Setup

### Prerequisites
- Python 3.10 or higher
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Mughal-Hash-24/FastBot
   cd FasTBot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Run the server**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

   The server will be available at `http://localhost:8000`

## 🌐 Frontend Integration

Connect your frontend by updating the JavaScript fetch URL:

```javascript
fetch("https://your-backend-url/chat", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ message: userMessage })
})
```

The default frontend uses vanilla HTML + JavaScript and `marked.js` to render markdown-rich responses in a chat-like UI.

## 🚀 Deployment

### Recommended Free Hosting Options

| Platform | Use Case | Notes |
|----------|----------|-------|
| 🆓 **Replit** | Backend Hosting | No credit card required, provides public URL |
| 🆓 **Vercel** | Frontend Hosting | Ideal for static frontend deployment |

### Deployment Steps

1. **Backend (Replit)**:
   - Import your GitHub repository
   - Add `GROQ_API_KEY` to Replit's Secrets panel
   - Run the project

2. **Frontend (Vercel)**:
   - Connect your frontend repository
   - Update API endpoints to point to your Replit backend
   - Deploy

## 🔐 Security Notes

- **Never commit** `.env` files to version control
- Use platform-specific secret management (Replit Secrets, Vercel Environment Variables)
- Ensure API keys are properly secured in production

## 🛠️ API Endpoints

### POST `/chat`
Send a message to the chatbot and receive an AI-generated response.

**Request Body:**
```json
{
  "message": "What is the grading policy for CS courses?"
}
```

**Response:**
```json
{
  "response": "Based on the course documents, the grading policy includes..."
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Ibtasaam Mughal**
- GitHub: [@Mughal-Hash-24](https://github.com/Mughal-Hash-24)
- LinkedIn: [muhammad-ibtasaam-amjad](https://www.linkedin.com/in/muhammad-ibtasaam-amjad/)

## 🙏 Acknowledgments

- FAST-NU for providing the academic context
- Groq for the powerful LLM API
- LangChain community for the excellent RAG framework
- ChromaDB for efficient vector storage

---

Built with ❤️ for FAST-NU students