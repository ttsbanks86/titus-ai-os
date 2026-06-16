#!/usr/bin/env python3
"""AI OS Brain scanner.

Builds a local graph of Titus AI OS runtimes, agents, skills, projects,
troubleshooting notes, and risk gates. The output is static JSON consumed by
index.html.
"""
from __future__ import annotations

import csv
import json
import os
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent
LIVE_COWORK = ROOT.parent
HOME = Path.home()
DATA_DIR = ROOT / "brain-data"
GRAPH_PATH = DATA_DIR / "graph.json"
REGISTRY_CSV = LIVE_COWORK / "AI-OS-GOVERNANCE" / "AGENT-SKILL-REGISTRY.csv"
LESSONS = LIVE_COWORK / "AI-OS-GOVERNANCE" / "LESSONS.md"
OBSIDIAN = LIVE_COWORK / "OBSIDIAN-AI-OS"

RUNTIME_COLORS = {
    "opencode": "#38bdf8",
    "claude": "#a78bfa",
    "goose": "#34d399",
    "workspace": "#fb923c",
    "memory": "#facc15",
    "project": "#e5e7eb",
    "gateway": "#f472b6",
    "risk": "#fb7185",
    "portfolio": "#22d3ee",
    "desktop": "#94a3b8",
}

HIGH_RISK_TERMS = (
    "delete",
    "remove",
    "gmail",
    "linkedin",
    "browser",
    "desktop",
    "system-cleanup",
    "automation",
    "identity",
    "file-ops",
    "send",
    "post",
    "deploy",
    "token",
    "secret",
)

PROJECTS = [
    {
        "id": "project:command-center",
        "label": "Command Center",
        "path": str(LIVE_COWORK / "BUSINESS-SUITE" / "analytics-dashboard"),
        "description": "Desktop control surface for bots, apps, CRM/API, learning captures, and AI OS controls.",
        "links": ["runtime:opencode", "memory:lessons", "workflow:desktop-app-build"],
    },
    {
        "id": "project:docflow",
        "label": "DocFlow",
        "path": str(LIVE_COWORK / "DOCFLOW"),
        "description": "Local desktop document workflow app; recent recursion crash fixed and EXE rebuilt.",
        "links": ["memory:troubleshooting:docflow-recursion", "workflow:desktop-app-build"],
    },
    {
        "id": "project:hermes-gateway",
        "label": "Hermes/OpenClaw Gateway",
        "path": str(LIVE_COWORK),
        "description": "Gateway/bot runtime with Telegram provider and OpenCode-Go model integration.",
        "links": ["memory:troubleshooting:Bot-Setup-Mismatch", "risk:token-safety"],
    },
    {
        "id": "project:learning-captures",
        "label": "Learning Captures",
        "path": str(LIVE_COWORK / "LEARNING-CAPTURES"),
        "description": "Captured reels, source links, extracted lessons, website snapshots, and cloned repositories.",
        "links": ["skill:opencode:learning-extractor", "workflow:learning-capture"],
    },
    {
        "id": "project:ai-os-brain",
        "label": "AI OS Brain",
        "path": str(ROOT),
        "description": "Visual local system brain showing how agents, skills, projects, workflows, memory, and risks connect.",
        "links": ["memory:platform-separation", "memory:lessons", "runtime:opencode", "runtime:claude", "runtime:goose", "runtime:workspace"],
    },
    {
        "id": "project:portfolio",
        "label": "Portfolio",
        "path": str(LIVE_COWORK),
        "description": "Public-facing story of AI systems, business tooling, and product collaboration work.",
        "links": ["portfolio:whisper-my-idea-pro", "portfolio:nollarita", "portfolio:darkflow-pipeline-serium", "portfolio:command-center", "portfolio:ai-os-brain"],
    },
]

WORKFLOWS = [
    {
        "id": "workflow:ceo-delegation",
        "label": "CEO Delegation Loop",
        "description": "User request → CEO agent → specialist subagent → tool execution → verification → summary/memory.",
        "links": ["agent:opencode:ceo", "agent:opencode:engineer", "agent:opencode:qa", "skill:opencode:verification-loop", "memory:lessons"],
    },
    {
        "id": "workflow:learning-capture",
        "label": "Learning Capture Loop",
        "description": "Source link/video → extraction → repo/site capture → report → adoption decision.",
        "links": ["skill:opencode:learning-extractor", "project:learning-captures", "memory:lessons"],
    },
    {
        "id": "workflow:desktop-app-build",
        "label": "Desktop App Build Loop",
        "description": "Patch source → compile/check → build EXE → verify shortcut → save troubleshooting lesson.",
        "links": ["agent:opencode:engineer", "agent:opencode:qa", "skill:opencode:windows-automation", "memory:lessons"],
    },
    {
        "id": "workflow:portfolio-story",
        "label": "Portfolio Story Loop",
        "description": "Project inventory → smart case-study framing → portfolio update → verification.",
        "links": ["project:portfolio", "agent:opencode:documentation", "skill:opencode:web-artifacts-builder"],
    },
]

PORTFOLIO_ITEMS = [
    ("portfolio:ai-os-brain", "AI OS Brain", "Visual map of agents, skills, projects, workflows, memory, and risks."),
    ("portfolio:whisper-my-idea-pro", "Whisper My Idea Pro", "AI productization workflow for turning spoken/raw ideas into structured execution assets."),
    ("portfolio:nola-voice-reader", "NOLA Voice Reader", "Clipboard-aware local TTS reader for turning copied text into spoken audio."),
    ("portfolio:docflow-pipeline-crm", "DocFlow + Pipeline CRM", "Document workflow and pipeline operations tooling framed around visibility, handoffs, and repeatable process."),
    ("portfolio:command-center", "Command Center", "Desktop operations cockpit for local apps, bots, APIs, and learning workflows."),
]


@dataclass
class Node:
    id: str
    label: str
    type: str
    runtime: str = ""
    path: str = ""
    status: str = "active"
    risk: str = "low"
    description: str = ""
    color: str = "#94a3b8"


@dataclass
class Edge:
    source: str
    target: str
    type: str
    label: str = ""


def safe_id(*parts: str) -> str:
    return ":".join(str(p).strip().lower().replace(" ", "-").replace("\\", "/").replace("/", "-") for p in parts if p)


def first_description(path: Path) -> str:
    candidates = []
    if path.is_dir():
        candidates.extend([path / "SKILL.md", path / "README.md", path / "README.mdx"])
    else:
        candidates.append(path)
    for file in candidates:
        if file.exists() and file.is_file():
            try:
                for line in file.read_text(encoding="utf-8", errors="ignore").splitlines()[:40]:
                    text = line.strip().strip("#").strip()
                    if not text or text.startswith("---") or text.lower().startswith("name:"):
                        continue
                    if len(text) > 8:
                        return text[:240]
            except OSError:
                pass
    return ""


def infer_risk(name: str, desc: str = "") -> str:
    haystack = f"{name} {desc}".lower()
    return "high" if any(term in haystack for term in HIGH_RISK_TERMS) else "low"


def add_node(nodes: dict[str, Node], node: Node) -> None:
    if node.id not in nodes:
        if not node.color:
            node.color = RUNTIME_COLORS.get(node.runtime, "#94a3b8")
        nodes[node.id] = node


def add_edge(edges: list[Edge], source: str, target: str, type_: str, label: str = "") -> None:
    if source and target and source != target:
        edges.append(Edge(source, target, type_, label))


def scan_named_children(path: Path, runtime: str, item_type: str) -> Iterable[tuple[str, Path, str]]:
    if not path.exists():
        return []
    items = []
    for child in sorted(path.iterdir(), key=lambda p: p.name.lower()):
        if child.name.startswith("."):
            continue
        if item_type == "agent" and child.suffix.lower() != ".md":
            continue
        if item_type == "skill" and not (child.is_dir() or child.suffix.lower() in (".md", "")):
            continue
        name = child.stem if child.is_file() else child.name
        items.append((name, child, first_description(child)))
    return items


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    nodes: dict[str, Node] = {}
    edges: list[Edge] = []

    runtimes = {
        "opencode": {
            "label": "OpenCode",
            "paths": [HOME / ".config" / "opencode" / "agent", HOME / ".config" / "opencode" / "skills"],
            "description": "Primary local execution and CEO-agent runtime.",
        },
        "claude": {
            "label": "Claude / Cloud",
            "paths": [HOME / ".claude" / "agents", HOME / ".claude" / "skills"],
            "description": "Specialist research, review, guardrail, and deep-skill runtime.",
        },
        "goose": {
            "label": "Goose / .agents",
            "paths": [HOME / ".agents" / "skills"],
            "description": "Reusable personal workflow skill layer.",
        },
        "workspace": {
            "label": "Workspace Skills",
            "paths": [LIVE_COWORK / ".agents" / "skills"],
            "description": "Project-specific HyperFrames/media/adapter workflows.",
        },
    }

    for runtime, info in runtimes.items():
        rid = f"runtime:{runtime}"
        add_node(nodes, Node(rid, info["label"], "runtime", runtime, status="active", risk="low", description=info["description"], color=RUNTIME_COLORS[runtime]))

    # Agents
    agent_roots = [
        (HOME / ".config" / "opencode" / "agent", "opencode"),
        (HOME / ".claude" / "agents", "claude"),
    ]
    for root, runtime in agent_roots:
        for name, path, desc in scan_named_children(root, runtime, "agent"):
            nid = safe_id("agent", runtime, name)
            add_node(nodes, Node(nid, name, "agent", runtime, str(path), "active", infer_risk(name, desc), desc, RUNTIME_COLORS[runtime]))
            add_edge(edges, f"runtime:{runtime}", nid, "contains", "contains")

    # Skills
    skill_roots = [
        (HOME / ".config" / "opencode" / "skills", "opencode"),
        (HOME / ".claude" / "skills", "claude"),
        (HOME / ".agents" / "skills", "goose"),
        (LIVE_COWORK / ".agents" / "skills", "workspace"),
    ]
    skill_names: list[tuple[str, str, str]] = []
    for root, runtime in skill_roots:
        for name, path, desc in scan_named_children(root, runtime, "skill"):
            nid = safe_id("skill", runtime, name)
            risk = infer_risk(name, desc)
            add_node(nodes, Node(nid, name, "skill", runtime, str(path), "active", risk, desc, RUNTIME_COLORS[runtime]))
            add_edge(edges, f"runtime:{runtime}", nid, "contains", "contains")
            skill_names.append((name.lower(), nid, runtime))
            if risk == "high":
                add_edge(edges, nid, "risk:approval-gated", "approval_required", "approval required")

    # Duplicate skill edges
    grouped: dict[str, list[str]] = defaultdict(list)
    for name, nid, _runtime in skill_names:
        grouped[name].append(nid)
    for name, ids in grouped.items():
        if len(ids) > 1:
            duplicate_id = safe_id("duplicate", name)
            add_node(nodes, Node(duplicate_id, f"Duplicate: {name}", "duplicate", "risk", status="review", risk="medium", description="Same skill name appears in multiple runtimes; compare before archiving.", color="#f59e0b"))
            for nid in ids:
                add_edge(edges, duplicate_id, nid, "duplicates", "duplicate")

    # Risk nodes
    add_node(nodes, Node("risk:approval-gated", "Approval-Gated Actions", "risk", "risk", status="active", risk="high", description="Actions requiring approval: sends/posts, account connects, deletion, spending, deployments, secrets, always-on mic/camera.", color=RUNTIME_COLORS["risk"]))
    add_node(nodes, Node("risk:token-safety", "Token Safety", "risk", "risk", status="active", risk="high", description="Pasted tokens are treated as exposed and must be rotated before production.", color=RUNTIME_COLORS["risk"]))

    # Memory nodes
    memory_nodes = [
        ("memory:governance", "AI OS Governance", LIVE_COWORK / "AI-OS-GOVERNANCE", "Plans, registry, lessons, and architecture files."),
        ("memory:lessons", "Lessons.md", LESSONS, "Compact troubleshooting lessons for future agents."),
        ("memory:obsidian", "Obsidian AI OS Vault", OBSIDIAN, "Human-readable linked side-brain."),
        ("memory:platform-separation", "Platform Separation Plan", LIVE_COWORK / "AI-OS-GOVERNANCE" / "PLATFORM-SEPARATION-AND-MEMORY-PLAN.md", "Plan for keeping OpenCode, Claude, Goose, and workspace skills standalone."),
        ("memory:system-brain-plan", "System Brain App Plan", LIVE_COWORK / "AI-OS-GOVERNANCE" / "SYSTEM-BRAIN-APP-RESEARCH-AND-PLAN.md", "Research and build plan for this visual brain viewer."),
    ]
    for mid, label, path, desc in memory_nodes:
        add_node(nodes, Node(mid, label, "memory", "memory", str(path), "active", "low", desc, RUNTIME_COLORS["memory"]))
    add_edge(edges, "memory:governance", "memory:lessons", "contains", "contains")
    add_edge(edges, "memory:governance", "memory:platform-separation", "contains", "contains")
    add_edge(edges, "memory:governance", "memory:system-brain-plan", "contains", "contains")
    add_edge(edges, "memory:obsidian", "memory:governance", "documents", "documents")

    # Troubleshooting notes
    troubleshooting_dir = OBSIDIAN / "04-Troubleshooting"
    if troubleshooting_dir.exists():
        for note in sorted(troubleshooting_dir.glob("*.md")):
            nid = safe_id("memory", "troubleshooting", note.stem)
            add_node(nodes, Node(nid, note.stem.replace("-", " "), "troubleshooting", "memory", str(note), "active", infer_risk(note.stem), first_description(note), RUNTIME_COLORS["memory"]))
            add_edge(edges, "memory:obsidian", nid, "contains", "contains")
            if "Token" in note.stem:
                add_edge(edges, nid, "risk:token-safety", "documents", "documents")

    # Projects
    for project in PROJECTS:
        add_node(nodes, Node(project["id"], project["label"], "project", "project", project["path"], "active", infer_risk(project["label"], project["description"]), project["description"], RUNTIME_COLORS["project"]))
        for link in project["links"]:
            add_edge(edges, project["id"], link, "connected_to", "connected")

    # Workflows
    for wf in WORKFLOWS:
        add_node(nodes, Node(wf["id"], wf["label"], "workflow", "project", status="active", risk="medium", description=wf["description"], color="#60a5fa"))
        for link in wf["links"]:
            add_edge(edges, wf["id"], link, "uses", "uses")

    # Portfolio items
    for nid, label, desc in PORTFOLIO_ITEMS:
        add_node(nodes, Node(nid, label, "portfolio", "portfolio", status="active", risk="low", description=desc, color=RUNTIME_COLORS["portfolio"]))
        add_edge(edges, "project:portfolio", nid, "showcases", "showcases")

    # Load registry rows as source metadata nodes if present
    if REGISTRY_CSV.exists():
        add_node(nodes, Node("file:agent-skill-registry", "Agent Skill Registry CSV", "file", "memory", str(REGISTRY_CSV), "active", "low", "Structured source of truth for agents, skills, status, risk, and keep/archive actions.", RUNTIME_COLORS["memory"]))
        add_edge(edges, "memory:governance", "file:agent-skill-registry", "contains", "contains")

    # Runtime health stats
    counts = Counter(node.type for node in nodes.values())
    runtime_counts = Counter(node.runtime for node in nodes.values())
    risk_counts = Counter(node.risk for node in nodes.values())

    graph = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "root": str(LIVE_COWORK),
        "summary": {
            "nodes": len(nodes),
            "edges": len(edges),
            "by_type": dict(counts),
            "by_runtime": dict(runtime_counts),
            "by_risk": dict(risk_counts),
        },
        "nodes": [asdict(node) for node in sorted(nodes.values(), key=lambda n: (n.type, n.runtime, n.label.lower()))],
        "edges": [asdict(edge) for edge in edges if edge.source in nodes and edge.target in nodes],
    }

    GRAPH_PATH.write_text(json.dumps(graph, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {GRAPH_PATH}")
    print(json.dumps(graph["summary"], indent=2))


if __name__ == "__main__":
    main()
