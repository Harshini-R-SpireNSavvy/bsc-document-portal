import os
import chromadb
from groq import Groq
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import PyPDF2
from docx import Document
import pandas as pd

load_dotenv()

_groq_api_key = os.getenv("GROQ_API_KEY")
if not _groq_api_key:
    client = None
else:
    client = Groq(api_key=_groq_api_key)

# Free local embedding model
print("Loading embedding model...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
print("Embedding model ready!")

# Setup ChromaDB
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="documents")

# Conversation memory
conversation_history = []
MAX_HISTORY = 10


def load_documents(folder_path: str) -> list[dict]:
    """Read all .txt, .pdf, .docx and .xlsx files from a folder."""
    documents = []

    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        content = ""

        # TXT files
        if filename.endswith(".txt"):
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            print(f"[OK] Read TXT: {filename}")

        # PDF files
        elif filename.endswith(".pdf"):
            try:
                with open(filepath, "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        text = page.extract_text()
                        if text:
                            content += text + "\n"
                print(f"[OK] Read PDF: {filename}")
            except Exception as e:
                print(f"[ERROR] Error reading PDF {filename}: {e}")
                continue

        # DOCX files
        elif filename.endswith(".docx"):
            try:
                doc = Document(filepath)
                for para in doc.paragraphs:
                    if para.text.strip():
                        content += para.text + "\n"
                print(f"[OK] Read DOCX: {filename}")
            except Exception as e:
                print(f"[ERROR] Error reading DOCX {filename}: {e}")
                continue

       # EXCEL files
        elif filename.endswith((".xlsx", ".xls")):
            try:
                xl = pd.ExcelFile(filepath)
                print(f"[INFO] Found sheets: {xl.sheet_names}")
                for sheet_name in xl.sheet_names:
                    try:
                # Read raw without header assumption
                        df = xl.parse(sheet_name, header=None)

                # Drop completely empty rows and columns
                        df = df.dropna(how="all").dropna(axis=1, how="all")

                        if df.empty:
                           print(f"[WARN] Sheet '{sheet_name}' is empty, skipping")
                           continue

                        content += f"\n[Sheet: {sheet_name}]\n"

                # Convert each row to readable text
                        for _, row in df.iterrows():
                            row_text = " | ".join([
                                str(val).strip()
                                for val in row
                                if str(val).strip() not in ["nan", "None", ""]
                            ])
                            if row_text:
                               content += row_text + "\n"

                        print(f"[OK] Read sheet: {sheet_name}")

                    except Exception as sheet_error:
                        print(f"[WARN] Error reading sheet {sheet_name}: {sheet_error}")
                        continue

                print(f"[OK] Read Excel: {filename}")
            except Exception as e:
                print(f"[ERROR] Error reading Excel {filename}: {e}")
                continue

        else:
            continue

        if content.strip():
            documents.append({
                "filename": filename,
                "content": content
            })
        else:
            print(f"[WARN] No text found in: {filename}")

    print(f"[OK] Total loaded: {len(documents)} document(s)")
    return documents


def chunk_document(content: str, chunk_size: int = 300) -> list[str]:
    """Split a document into smaller overlapping pieces."""
    words = content.split()
    chunks = []
    step = chunk_size - 50

    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + chunk_size])
        if len(chunk) > 100:
            chunks.append(chunk)
    return chunks


def get_embedding(text: str) -> list:
    """Convert text into a vector using local model."""
    embedding = embedding_model.encode(text)
    return embedding.tolist()


def index_documents(folder_path: str = "documents"):
    """Load, chunk, embed, and store all documents. Clears old data first."""
    global collection

    # Clear old collection and recreate fresh
    try:
        chroma_client.delete_collection(name="documents")
    except:
        pass
    collection = chroma_client.get_or_create_collection(name="documents")

    documents = load_documents(folder_path)
    doc_id = 0

    for doc in documents:
        chunks = chunk_document(doc["content"])
        for chunk in chunks:
            embedding = get_embedding(chunk)
            collection.add(
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[{"source": doc["filename"]}],
                ids=[str(doc_id)]
            )
            doc_id += 1

    print(f"[OK] Indexed {doc_id} chunks into ChromaDB")


def retrieve(question: str, n_results: int = 6) -> list[dict]:
    """Find the most relevant chunks for a question."""
    question_embedding = get_embedding(question)

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results
    )

    chunks = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        chunks.append({
            "text": doc,
            "source": meta["source"]
        })
    return chunks


def chat(user_message: str) -> str:
    """The complete RAG + memory pipeline."""
    if client is None:
        return "GROQ_API_KEY is not set. Add it in Streamlit secrets or your .env file."

    relevant_chunks = retrieve(user_message)

    if relevant_chunks:
        context_text = "\n\n".join([
            f"[From {c['source']}]\n{c['text']}"
            for c in relevant_chunks
        ])
    else:
        context_text = "No relevant documents found."

    system_prompt = f"""You are a helpful assistant. Answer questions using \
the document context provided below. If the answer is in the documents, \
use that. If not, answer from your general knowledge and say so.

DOCUMENT CONTEXT:
{context_text}"""

    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    recent_history = conversation_history[-MAX_HISTORY:]
    messages = [
        {"role": "system", "content": system_prompt}
    ] + recent_history

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        max_tokens=1024
    )

    assistant_reply = response.choices[0].message.content

    conversation_history.append({
        "role": "assistant",
        "content": assistant_reply
    })

    return assistant_reply