from typing import Literal

import chromadb
import chromadb.config

import marvin
from marvin.utilities.async_utils import run_async


def get_client(settings: chromadb.config.Settings = None) -> chromadb.Client:
    return chromadb.Client(settings=settings or marvin.settings.chroma)


class Chroma:
    def __init__(
        self,
        topic_name: str = None,
        settings: chromadb.config.Settings = None,
    ):
        self.client = get_client(settings=settings)
        self.collection = self.client.get_or_create_collection(
            topic_name or marvin.settings.default_topic
        )

    async def delete(self, ids: list[str] = None, where: dict = None):
        await run_async(self.collection.delete, ids=ids, where=where)

    async def delete_collection(self, collection_name: str):
        await run_async(self.client.delete_collection, collection_name=collection_name)

    async def add(
        self,
        documents: list[str] = None,
        embeddings: list[list[float]] = None,
        metadatas: list[dict] = None,
        ids: list[str] = None,
    ):
        await run_async(
            self.collection.add,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids,
        )
        await run_async(self.client.persist)

    async def query(
        self,
        query_embeddings: list[list[float]] = None,
        query_texts: list[str] = None,
        n_results: int = 10,
        where: dict = None,
        where_document: dict = None,
        include: list[Literal["embeddings", "documents", "metadata"]] = None,
        **kwargs
    ):
        return await run_async(
            self.collection.query,
            query_embeddings=query_embeddings,
            query_texts=query_texts,
            n_results=n_results,
            where=where,
            where_document=where_document,
            include=include or [],
            **kwargs
        )

    async def get(
        self,
        ids: list[str] = None,
        where: dict = None,
        include: list[Literal["embeddings", "documents", "metadata"]] = None,
    ):
        await run_async(
            self.collection.get, ids=ids, where=where, include=include or []
        )
