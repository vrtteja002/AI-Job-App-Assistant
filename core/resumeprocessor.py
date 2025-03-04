from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

class ResumeProcessor:
    def __init__(self, api_key):
        self.api_key = api_key
        
        # Initialize LLM and embeddings if API key is available
        if self.api_key:
            self.llm = ChatOpenAI(openai_api_key=api_key, temperature=0.7, model="gpt-4o")
            self.embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        else:
            self.llm = None
            self.embeddings = None
        
        self.resume_db = None
        self.resume_highlights = None
    
    def load_resume(self, resume_path):
        """Load and process the user's resume"""
        if resume_path.endswith('.pdf'):
            loader = PyPDFLoader(resume_path)
        else:
            loader = TextLoader(resume_path)
            
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        
        if not self.api_key:
            # If no API key, just store the text without using embeddings
            self.resume_text = "\n\n".join([doc.page_content for doc in texts])
            self.resume_highlights = "API key required for detailed resume analysis."
            print("Resume loaded without detailed analysis (no API key).")
            return self.resume_highlights
        
        # Create vector database from documents
        self.resume_db = FAISS.from_documents(texts, self.embeddings)
        print("Resume loaded and processed successfully.")
        
        # Extract key skills and experiences
        self._extract_resume_highlights()
        return self.resume_highlights
        
    def _extract_resume_highlights(self):
        """Extract key skills and experiences from resume"""
        if not self.resume_db:
            raise ValueError("No resume has been loaded. Please load a resume first.")
        
        if not self.api_key:
            self.resume_highlights = "API key required for detailed resume analysis."
            return
            
        prompt = PromptTemplate(
            input_variables=["resume_text"],
            template="""
            Based on the following resume, extract:
            1. Top 10 technical skills
            2. Top 3 soft skills
            3. Key professional achievements (max 3)
            4. Years of experience in primary field
            
            Resume:
            {resume_text}
            
            Format your response like :
            Top 10 technical skills : 
            Top 3 soft skills
            3. Key professional achievements (max 3):
            4. Years of experience in primary field :
            .
            """
        )
        
        resume_chain = LLMChain(llm=self.llm, prompt=prompt)
        
        # Get the full resume text from vector store
        resume_text = " ".join([doc.page_content for doc in self.resume_db.similarity_search("skills experience", k=10)])
        
        self.resume_highlights = resume_chain.run(resume_text=resume_text)
        print("Resume highlights extracted.")
    
    def get_resume_highlights(self):
        """Return extracted resume highlights"""
        if not self.resume_highlights:
            raise ValueError("No resume highlights available. Please load a resume first.")
        return self.resume_highlights
    
    def get_resume_text(self):
        """Get full resume text"""
        if not self.resume_db and not hasattr(self, 'resume_text'):
            raise ValueError("No resume has been loaded. Please load a resume first.")
        
        if hasattr(self, 'resume_text'):
            return self.resume_text
            
        # Get the full resume text from vector store
        resume_text = " ".join([doc.page_content for doc in self.resume_db.similarity_search("", k=100)])
        return resume_text
    
    def search_resume(self, query, k=5):
        """Search resume for specific information"""
        if not self.resume_db:
            raise ValueError("No resume has been loaded. Please load a resume first.")
            
        results = self.resume_db.similarity_search(query, k=k)
        return [doc.page_content for doc in results]