#not implemented in the chains yet

from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,FewShotChatMessagePromptTemplate,PromptTemplate


# List of examples from different themes
examples = [
     {
         "input": "Among the members with t-shirt size of medium, what is the percentage of the amount 50 received by the Student_Club?",
         "query": "SELECT  CAST(SUM(CASE WHEN `T2`.`amount` = 50 THEN 1.0 ELSE 0 END) AS DOUBLE) * 100 / COUNT(`T2`.`income_id`) FROM `member` AS `T1` INNER JOIN `income` AS `T2`  ON `T1`.`member_id` = `T2`.`link_to_member` WHERE `T1`.`position` = 'Member' AND `T1`.`t_shirt_size` = 'Medium'"
     },
     {
         "input": "Identify superheroes who can control wind and list their names in alphabetical order.",
         "query": "SELECT  `T1`.`superhero_name`FROM `superhero` AS `T1`INNER JOIN `hero_power` AS `T2`  ON `T1`.`id` = `T2`.`hero_id` INNER JOIN `superpower` AS `T3`  ON `T2`.`power_id` = `T3`.`id`\nWHERE\n  `T3`.`power_name` = 'Wind Control'\nORDER BY\n  `T1`.`superhero_name`"
     },
     
 ]

 

example_prompt = ChatPromptTemplate.from_messages(
     [
         ("human", "{input}\nSQLQuery:"),
         ("ai", "{query}"),
     ]
 )
few_shot_prompt = FewShotChatMessagePromptTemplate(
     example_prompt=example_prompt,
     examples=examples,
     # input_variables=["input","top_k"],
     input_variables=["input"],
 )
print(few_shot_prompt.format(input1="How many products are there?"))

vectorstore = Chroma()
vectorstore.delete_collection()
example_selector = SemanticSimilarityExampleSelector.from_examples(
     examples,
     OpenAIEmbeddings(),
     vectorstore,
     k=2,
     input_keys=["input"],
 )
example_selector.select_examples({"input": "how many employees we have?"})
few_shot_prompt = FewShotChatMessagePromptTemplate(
     example_prompt=example_prompt,
     example_selector=example_selector,
     input_variables=["input","top_k"],
 )
print(few_shot_prompt.format(input="How many products are there?"))
