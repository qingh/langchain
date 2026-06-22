from base import chat
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate


llm = chat()


examples = [
    {"input": "列出所有用户", "sql": "SELECT * FROM users"},
    {"input": "查找叫张三的用户", "sql": "SELECT * FROM users WHERE name = '张三'"},
    {"input": "统计订单总数", "sql": "SELECT COUNT(*) FROM orders"},
]

example_prompt = ChatPromptTemplate.from_messages([("human", "{input}"), ("ai", "sql")])


few_shot_prompt = FewShotChatMessagePromptTemplate(
    examples=examples, example_prompt=example_prompt
)

final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个sql专家。根据用户的自然语言描述生成对应的sql查询。"),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)

chain = final_prompt | llm

result = chain.invoke({"input": "找出消费超过1000元的用户"})

print(result.content)
