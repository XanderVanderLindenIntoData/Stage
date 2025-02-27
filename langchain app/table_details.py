# table_details.py (Table Extraction)
from langchain_community.utilities.sql_database import SQLDatabase
from langchain.chains.openai_tools import create_extraction_chain_pydantic
from langchain_openai import ChatOpenAI
from pydantic.v1 import BaseModel, Field
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Access variables using os.getenv()
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")

encoded_password = quote_plus(db_password)

db_uri = f"postgresql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"
db = SQLDatabase.from_uri(db_uri)
print(db_uri)  # Debugging

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