from langchain_unstructured import UnstructuredLoader


loader = UnstructuredLoader(
    file_path="data/1.语法同步练习基础语法合集.pdf",
    # 透传给底层 unstructured.partition.pdf
    strategy="fast",  # "fast" | "hi_res" | "ocr_only"
    mode="paged",  # "single" | "paged" | "elements"
    infer_table_structure=True,
    # languages=["chi_sim", "eng"],  # 中文 OCR 用
)
docs = loader.load()

print(f"加载了 {len(docs)} 个文档")
for i, d in enumerate(docs[:3]):
    print(f"\n--- 第 {i + 1} 段 ---")
    print(d.page_content[:200])
    print("元数据:", d.metadata)
