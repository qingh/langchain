from base import chat
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

llm = chat()


examples = [
    {"input": "列出所有用户", "sql": "SELECT * FROM users"},
    {"input": "查找叫张三的用户", "sql": "SELECT * FROM users WHERE name = '张三'"},
    {"input": "统计订单总数", "sql": "SELECT COUNT(*) FROM orders"},
    {"input": "按金额降序排列订单", "sql": "SELECT * FROM orders ORDER BY amount DESC"},
    {
        "input": "计算每个用户的平均消费",
        "sql": "SELECT user_id, AVG(amount) FROM orders GROUP BY user_id",
    },
]

examples_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    OpenAIEmbeddings(),  # 用于计算语义相似度的嵌入模型
    InMemoryVectorStore,  # 向量存储后端
    k=2,  # 只选最相关的 2 个示例
)

example_prompt = ChatPromptTemplate.from_messages(
    [("human", "{input}"), ("ai", "{sql}")]
)

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_selector=examples_selector, example_prompt=example_prompt
)
