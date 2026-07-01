import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
import os
import sys
from typing import List

from app.rag.document_loader import DocumentLoader, TextSplitter, Document
from app.rag.embeddings import EmbeddingClient
from app.rag.vector_store import VectorStore


def build_index(data_dir: str = "data", index_path: str = "data/faiss_index"):
    print(f">>> 开始从 {data_dir} 构建知识检索索引")
    loader = DocumentLoader(data_dir=data_dir)
    docs = loader.load_directory()
    if not docs:
        print(">>> 未发现可处理的文档，支持 .txt .md .pdf")
        return

    print(f">>> 共加载 {len(docs)} 个文档，开始切分文本")
    splitter = TextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    print(f">>> 切分为 {len(chunks)} 个文档块")

    print(">>> 开始生成向量嵌入")
    embedding_client = EmbeddingClient(model_type="local")
    texts = [chunk.content for chunk in chunks]
    embeddings = embedding_client.embed(texts)
    print(f">>> 生成 {len(embeddings)} 条向量")

    vector_store = VectorStore(index_path=index_path, embedding_dim=len(embeddings[0]) if embeddings else 768)
    vector_store.add_documents(chunks, embeddings)
    vector_store.save()
    print(f">>> 向量索引构建完成，已保存到 {index_path}.faiss")
    print(f">>> 文档块总数: {vector_store.get_document_count()}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="构建 data 目录的 FAISS 检索索引")
    parser.add_argument("--data-dir", default="data", help="数据目录路径，默认 data")
    parser.add_argument("--index-path", default="data/faiss_index", help="索引文件前缀，默认 data/faiss_index")
    args = parser.parse_args()

    build_index(data_dir=args.data_dir, index_path=args.index_path)
