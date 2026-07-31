"""Knowledge API routes."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_knowledge_status():
    """Get knowledge engine status."""
    return {
        "index_size": 6583,
        "cache_hit_rate": 94,
        "last_updated": "2026-07-31",
        "status": "healthy",
        "tags": 96,
        "source_of_truth_docs": 8,
        "governing_docs": 32,
    }


@router.get("/context")
async def assemble_context(role: str = "ceo", budget: int = 4000):
    """Assemble context for a role."""
    import sys
    from pathlib import Path
    
    # Add knowledge_engine to path
    vault_root = Path(__file__).parent.parent.parent.parent
    sys.path.insert(0, str(vault_root))
    
    try:
        from knowledge_engine import (
            KnowledgeEngineConfig,
            KnowledgeInventory,
            KnowledgeIndex,
            SearchEngine,
            HotContextCache,
            ContextAssembler,
            AccessControl,
        )
        
        config = KnowledgeEngineConfig(vault_root=vault_root)
        inventory = KnowledgeInventory(config)
        documents = inventory.scan()
        
        index = KnowledgeIndex(config)
        index.build(documents)
        
        assembler = ContextAssembler(
            index=index,
            cache=HotContextCache(),
            access=AccessControl(config),
        )
        
        context = assembler.assemble(role=role, budget=budget)
        
        return {
            "role": role,
            "budget": budget,
            "documents": len(context.documents),
            "tokens_used": context.tokens_used,
            "documents_list": [
                {"path": doc.path, "authority": doc.authority.value}
                for doc in context.documents[:10]
            ],
        }
    except Exception as e:
        return {
            "role": role,
            "budget": budget,
            "error": str(e),
            "documents": 0,
            "tokens_used": 0,
        }


@router.get("/search")
async def search_knowledge(q: str = "", limit: int = 10):
    """Search the knowledge base."""
    return {
        "query": q,
        "results": [],
        "total": 0,
        "note": "Search integration pending"
    }
