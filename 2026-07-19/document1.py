import os
import sys

# Windows 终端默认 GBK，打印中文会乱码
sys.stdout.reconfigure(encoding="utf-8")

# 国内网络拉 HuggingFace 模型慢，可解开走镜像
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from langchain_chroma import Chroma
from langchain_community.document_loaders import (
    DirectoryLoader,
    PyMuPDFLoader,  # 对中文 PDF 抽得更干净，比 PyPDFLoader 稳
)
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

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
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
relevant_docs = retriever.invoke("这份录用通知书里，报到接待人是谁？")

print("\n\n#### 检索结果 ####\n")
for i, doc in enumerate(relevant_docs, 1):
    print(f"--- 结果 {i} ---")
    print(doc.page_content.strip())
    source = doc.metadata.get("source", "未知")
    page = doc.metadata.get("page", "")
    if page != "":
        print(f"(来源: {source} · 第 {page + 1} 页)")
    else:
        print(f"(来源: {source})")
    print()
