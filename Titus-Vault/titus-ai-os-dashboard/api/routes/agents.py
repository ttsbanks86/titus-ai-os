"""Agents API routes."""

from fastapi import APIRouter

router = APIRouter()

# Eight approved agents
AGENTS = [
    {
        "id": "ceo",
        "name": "CEO Agent",
        "role": "Orchestration",
        "purpose": "Primary orchestrator, delegates to subagents",
        "status": "idle",
        "permissions": ["read", "write", "delegate"],
        "current_task": None,
        "queue": [],
    },
    {
        "id": "engineer",
        "name": "Engineer Agent",
        "role": "Engineering",
        "purpose": "Writes, debugs, and reviews code",
        "status": "idle",
        "permissions": ["read", "write", "code"],
        "current_task": None,
        "queue": [],
    },
    {
        "id": "qa",
        "name": "QA Agent",
        "role": "Quality Assurance",
        "purpose": "Testing, code review, bug finding",
        "status": "idle",
        "permissions": ["read", "test", "review"],
        "current_task": None,
        "queue": [],
    },
    {
        "id": "research",
        "name": "Research Agent",
        "role": "Research",
        "purpose": "Web research, information gathering",
        "status": "idle",
        "permissions": ["read", "search"],
        "current_task": None,
        "queue": [],
    },
    {
        "id": "reasoning",
        "name": "Reasoning Agent",
        "role": "Analysis",
        "purpose": "Complex analysis, decision support",
        "status": "idle",
        "permissions": ["read", "analyze"],
        "current_task": None,
        "queue": [],
    },
    {
        "id": "browser",
        "name": "Browser Agent",
        "role": "Web Automation",
        "purpose": "Browser automation, web scraping",
        "status": "idle",
        "permissions": ["read", "browse"],
        "current_task": None,
        "queue": [],
    },
    {
        "id": "automation",
        "name": "Automation Agent",
        "role": "Automation",
        "purpose": "PowerShell scripts, system operations",
        "status": "idle",
        "permissions": ["read", "write", "execute"],
        "current_task": None,
        "queue": [],
    },
    {
        "id": "documentation",
        "name": "Documentation Agent",
        "role": "Documentation",
        "purpose": "Writes README, technical docs, user guides",
        "status": "idle",
        "permissions": ["read", "write"],
        "current_task": None,
        "queue": [],
    },
]


@router.get("/")
async def list_agents():
    """List all agents with status."""
    return {"agents": AGENTS, "total": len(AGENTS)}


@router.get("/{agent_id}")
async def get_agent(agent_id: str):
    """Get agent details."""
    for agent in AGENTS:
        if agent["id"] == agent_id:
            return agent
    return {"error": "Agent not found"}


@router.get("/{agent_id}/context")
async def get_agent_context(agent_id: str):
    """Get agent's current context."""
    # Import M2 modules
    import sys
    sys.path.insert(0, str(__file__).parent.parent.parent.parent)
    
    try:
        from knowledge_engine import AgentContextProvider, AgentRole
        
        role_map = {
            "ceo": AgentRole.CEO,
            "engineer": AgentRole.ENGINEER,
            "qa": AgentRole.QA,
        }
        
        if agent_id in role_map:
            provider = AgentContextProvider()
            context = provider.get_context(role_map[agent_id])
            return {
                "agent_id": agent_id,
                "context": {
                    "documents": len(context.documents),
                    "tokens_used": context.tokens_used,
                    "budget": context.budget,
                }
            }
    except Exception as e:
        pass
    
    return {
        "agent_id": agent_id,
        "context": {"documents": 0, "tokens_used": 0, "budget": 4000},
        "note": "Context not available"
    }
