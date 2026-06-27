from langchain_core.documents import Document

path = "data/work.md"
with open(path, encoding="utf-8") as f:
    content = f.read()

docs = [Document(page_content=content, metadata={"source": path})]

print(f"加载了{len(docs)}个文档")
print(f"内容预览：{docs[0].page_content}")
print(f"元数据：{docs[0].metadata}")
