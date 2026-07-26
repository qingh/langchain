import os
import sys

# Windows 终端默认 GBK，打印中文会乱码
sys.stdout.reconfigure(encoding="utf-8")

# 国内网络拉 HuggingFace 模型慢，可解开走镜像
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from base import chat
from langchain_chroma import Chroma
from langchain_community.document_loaders import (
    DirectoryLoader,
    PyMuPDFLoader,  # 对中文 PDF 抽得更干净，比 PyPDFLoader 稳
)
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

llm = chat()

# ========== 1. 加载 PDF ==========
loader = DirectoryLoader(
    "./document",
    glob="**/*.pdf",
    loader_cls=PyMuPDFLoader,
)

try:
    documents = loader.load()
except (FileNotFoundError, RuntimeError) as e:
    print(f"加载文档失败: {e}", file=sys.stderr)
    sys.exit(1)

print(f"已加载 {len(documents)} 个文档片段")

# ========== 2. 切分 ==========
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # 配合 bge-large-zh 的 512 token 上限比较合适
    chunk_overlap=80,  # 重叠多一些，避免句意被切碎
    separators=["\n\n", "\n", "。", "！", "？", "，", " ", ""],
)
chunks = text_splitter.split_documents(documents)
print(f"已切分为 {len(chunks)} 个 chunk")

# ========== 3. Embedding ==========
embeddings = HuggingFaceEmbeddings(
    # model_name="BAAI/bge-large-zh-v1.5",
    model_name="BAAI/bge-small-zh-v1.5",
    encode_kwargs={"normalize_embeddings": True},  # bge 系列官方建议做 L2 normalize
)

# ========== 4. 存入 Chroma（避免重复写入） ==========
persist_directory = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "chroma_db",
)
if os.path.exists(persist_directory) and os.listdir(persist_directory):
    print(f"检测到已有向量库 {persist_directory}，直接加载")
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
    )
else:
    print("首次运行，正在构建向量库（首次会下载模型，可能较慢）...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory,
    )
    print(f"向量库已保存到 {persist_directory}")

# ========== 5. 检索 ==========
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 6, "fetch_k": 20},
)

prompt = ChatPromptTemplate.from_template("""
你是公司内部的智能问答助手，请仅根据以下检索到的内部文档，用简洁的语言回答用户问题。
如果文档中没有相关信息，请明确告知用户，不要编造答案。

【检索到的文档】
{context}

【用户问题】
{question}
""")


def format_docs(docs):
    return "\n\n".join(
        f"[来源: {doc.metadata.get('source', '未知')}]\n{doc.page_content}"
        for doc in docs
    )


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# answer = rag_chain.invoke("这份录用通知书里，报到接待人是谁？")
# answer = rag_chain.invoke("这份录用通知书里，报到地点是在哪里？")
# answer = rag_chain.invoke("这份录用通知书里，接待人电话是多少？")
answer = rag_chain.invoke("这份录用通知书里，候选人税前薪资和税后薪资分别是多少？")
print(answer)
