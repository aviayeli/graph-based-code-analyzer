# Phase 1 — Target Repository Record

| Field | Value |
|-------|-------|
| **Name** | crewAI |
| **Org** | crewAIInc |
| **URL** | https://github.com/crewAIInc/crewAI |
| **Cloned to** | `workspace/crewAI/` (shallow, read-only) |
| **Primary language** | Python 3.11+ |
| **Source root** | `lib/crewai/src/crewai/` |
| **Python files (src)** | 497 |
| **Total LOC (src)** | 106,761 |
| **LOC requirement** | ≥ 10,000 ✅ (10.7× over minimum) |
| **Classes** | 855 |
| **Functions** | 3,286 |

## Preliminary God-Node Sketch (manual + AST)

| Node | Type | In-Degree | Evidence |
|------|------|-----------|----------|
| `crewai_event_bus` | Singleton/module | 50 | Imported by every domain |
| `Task` | Class | 44 | Core data model, universal dependency |
| `BaseTool` | ABC | 37 | Tool interface, 8 direct subclasses + ecosystem |
| `BaseLLM` | ABC | 36 | LLM interface, 6 provider subclasses |
| `utilities` | Package | 224 (agg.) | God-package, no bounded context |
| `Crew` | Class | 22 | 95-method orchestrator, SRP violation |
| `Flow` | Class | 19 | 85-method runtime, 3,873 LOC |

## Architecture Summary

CrewAI is a multi-agent orchestration framework. Its execution model:

```
User → Crew.kickoff()
  → Task resolution (sequential / hierarchical / parallel Process)
    → Agent.execute_task()
      → CrewAgentExecutor.invoke()
        → LLM.call() [via BaseLLM → provider completions]
        → Tool.run() [via BaseTool hierarchy]
  → Memory.save() [via unified_memory]
  → Event emission [via crewai_event_bus]
  → Flow routing [if Flow-based orchestration]
```

Key subsystems: A2A (agent-to-agent delegation), MCP (tool wrappers), RAG (95 files of embeddings), Knowledge, Skills, Telemetry (OTLP).
