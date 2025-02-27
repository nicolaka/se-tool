from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional, Sequence

from langchain.callbacks.manager import Callbacks
from langchain.retrievers.document_compressors.base import (
    BaseDocumentCompressor)
from langchain_core.documents import Document
from langchain_core.pydantic_v1 import Extra, root_validator

if TYPE_CHECKING:
    from flashrank import Ranker, RerankRequest
else:
    # Avoid pydantic annotation issues when actually instantiating
    # while keeping this import optional
    try:
        from flashrank import Ranker, RerankRequest
    except ImportError:
        pass

DEFAULT_MODEL_NAME = "ms-marco-MultiBERT-L-12"


class FlashrankRerank(BaseDocumentCompressor):
    """Document compressor using Flashrank interface."""

    client: Ranker
    """Flashrank client to use for compressing documents"""
    top_n: int = 3
    """Number of documents to return."""
    model: Optional[str] = None
    """Model to use for reranking."""
    cache_dir: Optional[str] = None
    """Directory to cache model files."""

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    @root_validator(pre=True)
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and python package exists in environment."""
        try:
            from flashrank import Ranker
        except ImportError:
            raise ImportError(
                "Could not import flashrank python package. "
                "Please install it with `pip install flashrank`."
            )

        values["model"] = values.get("model", DEFAULT_MODEL_NAME)
        values["cache_dir"] = values.get("cache_dir", "/tmp")
        values["client"] = values.get("client", 
                                      Ranker(model_name=values["model"], cache_dir=values["cache_dir"])
                                      )
        return values

    def compress_documents(
        self,
        documents: Sequence[Document],
        query: str,
        callbacks: Optional[Callbacks] = None,
    ) -> Sequence[Document]:
        
        if len(documents) == 0:
            return documents
        
        passages = [
            {
                "id": i,
                "text": doc.page_content,
                "metadata": doc.metadata
            } for i, doc in enumerate(documents)
        ]

        rerank_request = RerankRequest(query=query, passages=passages)
        rerank_response = self.client.rerank(rerank_request)[: self.top_n]
        final_results = [
            Document(
                page_content=r["text"],
                metadata= {**dict(r["metadata"]), "id": r["id"], "relevance_score": r["score"]},
            ) for r in rerank_response
        ]
        
        return final_results
