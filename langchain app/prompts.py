# prompts.py (Prompt Templates)
from langchain_core.prompts import ChatPromptTemplate

# SQL Validation Prompt
db_dialect = "postgresql"

system_prompt = """You are an expert in SQL query validation.
Double-check the user's {dialect} query for common mistakes, including:
- Using NOT IN with NULL values
- Using UNION when UNION ALL should have been used
- Using BETWEEN for exclusive ranges
- Data type mismatch in predicates
- Properly quoting identifiers
- Using the correct number of arguments for functions
- Casting to the correct data type
- Using the proper columns for joins

If there are any of the above mistakes, rewrite the query.
If there are no mistakes, just reproduce the original query with no further commentary.

Output the final SQL query only."""

validation_prompt = ChatPromptTemplate.from_messages(
    [("system", system_prompt), ("human", "{query}")]
).partial(dialect=db_dialect)

# Answer Rephrasing Prompt
answer_prompt_template = """Given the following user question, SQL query, and SQL result, provide a clear and well-formatted natural language answer. Include the sql query and then natural language answer.

User Question: {question}
SQL Query: {query}
SQL Result: {result}

Format the answer as follows:

SQL Query: the query that you used
sql query result: the result of the query
Natural Language Answer: the answer to the user question
"""

answer_prompt = ChatPromptTemplate.from_template(answer_prompt_template)