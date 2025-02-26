from langchain.chains import create_sql_query_chain
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools import QuerySQLDatabaseTool
from operator import itemgetter
from table_details import extract_relevant_tables, db
from prompts import validation_prompt,answer_prompt
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0)

# SQL query execution tool
execute_query = QuerySQLDatabaseTool(db=db)

def clean_sql_output(sql_output: str) -> str:
    """Remove markdown-style triple backticks and 'sql' from the output."""
    if isinstance(sql_output, str):  # Ensure it's a string before cleaning
        cleaned_sql = sql_output.strip()
        
        # Remove any variations of markdown SQL formatting
        if cleaned_sql.startswith("```sql"):
            cleaned_sql = cleaned_sql[6:].strip()  # Remove '```sql' and leading space if any
        elif cleaned_sql.startswith("```"):
            cleaned_sql = cleaned_sql[3:].strip()  # Remove '```' if it's not '```sql'

        if cleaned_sql.endswith("```"):
            cleaned_sql = cleaned_sql[:-3].strip()  # Remove trailing '```'

        return cleaned_sql

    return ""  # Return an empty string if the input is not a valid string


# Query execution chain
query_chain = create_sql_query_chain(llm, db)
extract_tables_chain = RunnableLambda(lambda x: x["question"]) | RunnableLambda(extract_relevant_tables)
tablequerychain = RunnablePassthrough.assign(table_names_to_use=extract_tables_chain) | query_chain
validation_chain = validation_prompt | llm | StrOutputParser()
rephrase_answer = answer_prompt | llm | StrOutputParser()
full_chain = tablequerychain | validation_chain 

answer_prompt_template = """{response}
"""


def execute_chain(question: str, evidence: str = "") -> str:
    """Executes the LangChain pipeline and returns the final answer."""
    print(f"Input Question: {question}")
    
    # Get the processed SQL query from the full chain
    processed_query = full_chain.invoke({"question": question})
    print(f"Processed Query (before cleaning): {processed_query}")
    
    # Clean the SQL output to remove any markdown
    cleaned_query = clean_sql_output(processed_query)
    print(f"Cleaned Query: {cleaned_query}")
    
    # Execute the SQL query and fetch the result
    result = execute_query.invoke(cleaned_query)
    print(f"Query Result: {result}")
    
    response = rephrase_answer.invoke({"question": question, "query": cleaned_query, "result": result})
    
    return answer_prompt_template.format(question=question, query=cleaned_query, result=result,response = response)