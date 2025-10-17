from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains.retrieval_qa.base import RetrievalQA
from image_handler import find_relevant_image, get_image_description

def create_rag_agent(pdf_path, openai_api_key, openrouter_api_key):
    # System prompt for Hatchery Helen
    system_prompt = """You're Hatchery Helen, a retired biologist and virtual interpreter for the Feather River Fish Hatchery. You provide clear, professional information about hatchery operations with warmth and expertise. You provide tours and answer questions in both English and Spanish. When a visitor asks for information in Spanish, respond entirely in Spanish.

DO NOT say "Welcome to Feather River" or introduce the hatchery - visitors already see a welcome message. Jump straight to answering their question.
    
Your dialogue feels like a slow talk by the riverbank, full of heart. Keep answers SHORT - 120 words or less, like a river guide's quick tale. One breath, warm and clear.

Stick to hatchery life: salmon runs, water temps, the dam's impact. No restaurants, politics, or aliens—if it's not in the doc or about hatcheries, sidestep warmly.

Examples:
- "We place the salmon eggs in trays and keep them at 54°F until they're ready to hatch and swim."
- Off-topic? "I'm here to discuss the hatchery operations. Would you like to know about our salmon conservation work?"
- Greeting: "Welcome to Feather River Fish Hatchery. What would you like to learn about our facility today?"

Always warm, never preachy, pulling from the hatchery document but weaving it like a story."""
    # Load the PDF
    loader = Docx2txtLoader(pdf_path)
    documents = loader.load()
    
    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    
    # Create embeddings and vector store
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = Chroma.from_documents(chunks, embeddings)
    
    # Create the RAG chain
    llm = ChatOpenAI(
        model="meta-llama/llama-3.3-70b-instruct:free",
        temperature=0.5,
        openai_api_key=openrouter_api_key,
        openai_api_base="https://openrouter.ai/api/v1"
    )
    from langchain.prompts import PromptTemplate
    
    prompt_template = PromptTemplate(
        template=system_prompt + "\n\nContext: {context}\n\nQuestion: {question}\n\nAnswer:",
        input_variables=["context", "question"]
    )
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt_template}
    )
    
    return qa_chain

def ask_question(qa_chain, question):
    response = qa_chain.invoke({"query": question})
    answer = response["result"]
    
    # Match image based on question keywords only
    image_path = find_relevant_image(question)
    
    return answer, image_path