# TODO

This list is ordered by resume value and demo impact.

## 0. Polish before publishing

- [ ] Add screenshots or a short demo GIF to the README.
- [ ] Verify the repo runs from a clean clone on macOS/Linux.
- [ ] Add a public GitHub description: `Agentic production debugging platform for ticket-driven incident investigation.`
- [ ] Add topics: `ai-agents`, `fastapi`, `observability`, `incident-response`, `tool-calling`, `evals`, `python`, `sqlite`.
- [ ] Confirm all data is synthetic and public-safe.

## 1. Product/demo upgrades

- [ ] Add a polished React or Next.js dashboard instead of the static HTML page.
- [ ] Add investigation history with saved reports.
- [ ] Add clickable evidence cards that expand logs, metrics, traces, SQL, and code snippets.
- [ ] Add a timeline visualization for deploys, metric spikes, log bursts, and trace failures.
- [ ] Add copy-to-markdown export for the final incident report.

## 2. Agent upgrades

- [ ] Add optional LLM planner mode behind an environment flag.
- [ ] Keep deterministic mode as the default for tests/evals.
- [ ] Add structured planner output with `hypotheses`, `tools_to_call`, `expected_evidence`, and `stop_condition`.
- [ ] Add reflection step that checks whether every root-cause claim has cited evidence.
- [ ] Add confidence calibration based on evidence diversity, severity, and tool agreement.

## 3. Observability upgrades

- [ ] Export agent steps and tool calls as OpenTelemetry-style JSON spans.
- [ ] Add per-tool latency, result count, and error-rate metrics.
- [ ] Add a local traces endpoint for completed investigations.
- [ ] Add flamegraph-style display for trace spans in the dashboard.

## 4. Eval upgrades

- [ ] Expand from 8 to 50 labeled synthetic incidents.
- [ ] Add ambiguous incidents with multiple plausible services.
- [ ] Add noisy incidents where logs contain misleading deploy IDs.
- [ ] Add negative-control tickets where no confident root cause exists.
- [ ] Add per-category metrics and a confusion matrix.
- [ ] Add regression tests that fail if hallucinated evidence increases.

## 5. Integration upgrades

- [ ] Add GitHub issue mode: investigate an issue title/body and post a Markdown report.
- [ ] Add Slack-style ticket input payloads.
- [ ] Add local file ingestion for synthetic log bundles.
- [ ] Add a mock CloudWatch adapter and mock Athena adapter while keeping the default data synthetic.

## 6. Deployment upgrades

- [ ] Deploy the FastAPI app to AWS App Runner, ECS Fargate, or Lambda + API Gateway.
- [ ] Add Terraform or AWS CDK infrastructure.
- [ ] Add GitHub Actions release workflow.
- [ ] Add a hosted demo link.

## 7. Resume-ready final state

- [ ] README has architecture diagram, screenshots, eval table, and CLI/dashboard demo commands.
- [ ] Evals run in CI.
- [ ] Dashboard looks clean enough to open during interviews.
- [ ] Repo has a clear security/confidentiality note.
- [ ] Resume bullets point to measurable project features: eval harness, cited evidence, tool calling, CLI, dashboard, Docker, CI.
