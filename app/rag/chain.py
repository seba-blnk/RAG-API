from langchain_google_genai import ChatGoogleGenerativeAI
from app.rag.vectorstore import collection
from app.rag.embeddings import embeddings
from app.config import GOOGLE_API_KEY

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key= GOOGLE_API_KEY,
    temperature=0.3
)

def ask(question: str) -> dict:
    """Search relevant chunks and generate answer using RAG"""

    #1. Convert the quersion to a vector and search similar chunks.
    question_vector = embeddings.embed_query(question)

    results = collection.query(
        query_embeddings=[question_vector],
        n_results=3
    )

    #2. Extract the text from the results
    documents = results["documents"][0]

    if not documents:
        return{
            "answer": "No relevant documents found.",
            "context": []
        }
    
    #3. Build the prompt with context
    content_text = "\n\n".join(documents)

    prompt =f"""Answer the question based ONLY on the following context.
    If the context doesn't contain enough information, say so.

    Context:
    {content_text}

    Question:
    {question}"""

    #4. Send to the LLM and return
    response = llm.invoke(prompt)

    return{
        "answer": response.content,
        "context": documents
    }