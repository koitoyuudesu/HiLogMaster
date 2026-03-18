"""
向量存储模块
管理 ChromaDB 向量数据库操作
"""

import chromadb
from typing import List, Dict, Optional
from config import Config


class VectorStore:
    """ChromaDB 向量存储"""

    def __init__(self, persist_directory: Optional[str] = None):
        self.persist_directory = persist_directory or str(Config.CHROMADB_PATH)
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        self.collection_name = "log_embeddings"
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_embedding(
        self,
        record_id: int,
        summary: str,
        metadata: Dict
    ):
        """
        添加摘要向量

        Args:
            record_id: 记录 ID
            summary: 分析摘要
            metadata: 元数据（包含 package_name, error_count 等）
        """
        self.collection.add(
            documents=[summary],
            metadatas=[metadata],
            ids=[str(record_id)]
        )

    def search(
        self,
        query: str,
        n_results: int = 5
    ) -> List[Dict]:
        """
        语义搜索

        Args:
            query: 查询文本
            n_results: 返回结果数量

        Returns:
            搜索结果列表
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )

        formatted_results = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                formatted_results.append({
                    'id': results['ids'][0][i],
                    'document': doc,
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                    'distance': results['distances'][0][i] if 'distances' in results else None
                })

        return formatted_results

    def delete_by_id(self, record_id: int):
        """
        删除指定 ID 的向量

        Args:
            record_id: 记录 ID
        """
        self.collection.delete(ids=[str(record_id)])