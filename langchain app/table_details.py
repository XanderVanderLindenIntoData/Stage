# table_details.py (Table Extraction)
from langchain_community.utilities.sql_database import SQLDatabase
from langchain.chains.openai_tools import create_extraction_chain_pydantic
from langchain_openai import ChatOpenAI
from pydantic.v1 import BaseModel, Field
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

db = SQLDatabase.from_uri(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
)

llm = ChatOpenAI(model="gpt-4o", temperature=0)

class TableSchema(BaseModel):
    """Table in SQL database."""
    name: str = Field(description="Name of table in SQL database.")

def extract_relevant_tables(input_text):
    """Extract relevant table names based on user question."""
    table_names = "\n".join(db.get_usable_table_names())
    system_prompt = f"""Given the following list of SQL tables, identify ALL tables that MIGHT be relevant to the user question.
    
    The tables are:
    {table_names}
    
    Include ALL POTENTIALLY RELEVANT tables."""
    
    table_chain = create_extraction_chain_pydantic(TableSchema, llm, system_message=system_prompt)
    extracted = table_chain.invoke({"input": input_text})
    return [table.name for table in extracted]