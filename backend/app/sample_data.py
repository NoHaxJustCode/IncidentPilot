INCIDENTS = [
    {
        "id": "inc_checkout_4921",
        "ticket": "Checkout latency increased for premium users after deploy 4921. p95 went from 240ms to 1800ms around 14:05 UTC.",
        "expected_service": "checkout-service",
        "expected_category": "latency_regression",
        "expected_deploy_id": "4921",
        "expected_evidence_ids": ["metric_checkout_p95", "log_checkout_timeout", "deploy_4921", "trace_checkout_slow"],
    },
    {
        "id": "inc_payment_2277",
        "ticket": "Payment authorization timeouts increased after deploy 2277. Customers see intermittent payment failures.",
        "expected_service": "payment-service",
        "expected_category": "timeout_regression",
        "expected_deploy_id": "2277",
        "expected_evidence_ids": ["metric_payment_errors", "log_payment_timeout", "deploy_2277", "trace_payment_timeout"],
    },
    {
        "id": "inc_invoice_8810",
        "ticket": "Invoice generation is producing duplicate line items after deploy 8810 for enterprise accounts.",
        "expected_service": "invoice-service",
        "expected_category": "data_duplication",
        "expected_deploy_id": "8810",
        "expected_evidence_ids": ["metric_invoice_duplicates", "log_invoice_duplicate", "deploy_8810", "code_invoice_idempotency"],
    },
]

SERVICES = [
    {"name": "checkout-service", "owner": "commerce", "language": "python"},
    {"name": "payment-service", "owner": "payments", "language": "java"},
    {"name": "invoice-service", "owner": "billing", "language": "python"},
    {"name": "user-service", "owner": "identity", "language": "go"},
]

DEPLOYS = [
    {"id": "deploy_4921", "deploy_id": "4921", "service": "checkout-service", "timestamp": "2026-06-01T14:02:00Z", "summary": "Changed premium pricing cache lookup."},
    {"id": "deploy_2277", "deploy_id": "2277", "service": "payment-service", "timestamp": "2026-06-02T09:17:00Z", "summary": "Reduced payment gateway timeout budget."},
    {"id": "deploy_8810", "deploy_id": "8810", "service": "invoice-service", "timestamp": "2026-06-03T18:40:00Z", "summary": "Refactored invoice item merge logic."},
]

METRICS = [
    {"id": "metric_checkout_p95", "service": "checkout-service", "metric": "p95_latency_ms", "before": 240, "after": 1800, "timestamp": "2026-06-01T14:06:00Z", "summary": "checkout-service p95 latency spiked after deploy 4921."},
    {"id": "metric_payment_errors", "service": "payment-service", "metric": "error_rate", "before": 0.01, "after": 0.14, "timestamp": "2026-06-02T09:25:00Z", "summary": "payment-service timeout errors rose after deploy 2277."},
    {"id": "metric_invoice_duplicates", "service": "invoice-service", "metric": "duplicate_line_items", "before": 0, "after": 143, "timestamp": "2026-06-03T18:47:00Z", "summary": "invoice-service duplicate items appeared after deploy 8810."},
]

LOGS = [
    {"id": "log_checkout_timeout", "service": "checkout-service", "level": "WARN", "timestamp": "2026-06-01T14:07:00Z", "message": "premium checkout cache miss loop after deploy 4921 request=req-1001 latency_ms=1842"},
    {"id": "log_payment_timeout", "service": "payment-service", "level": "ERROR", "timestamp": "2026-06-02T09:26:00Z", "message": "gateway authorization timeout after deploy 2277 request=req-2001 timeout_ms=750"},
    {"id": "log_invoice_duplicate", "service": "invoice-service", "level": "ERROR", "timestamp": "2026-06-03T18:49:00Z", "message": "duplicate invoice line item detected after deploy 8810 account_tier=enterprise"},
]

TRACES = [
    {"id": "trace_checkout_slow", "request_id": "req-1001", "service": "checkout-service", "duration_ms": 1842, "summary": "checkout -> pricing-cache repeated premium lookup before response."},
    {"id": "trace_payment_timeout", "request_id": "req-2001", "service": "payment-service", "duration_ms": 782, "summary": "payment-service waited on gateway until the new shorter timeout fired."},
    {"id": "trace_invoice_duplicate", "request_id": "req-3001", "service": "invoice-service", "duration_ms": 410, "summary": "invoice-service merge step emitted duplicate invoice items."},
]

CODE = [
    {"id": "code_checkout_cache", "service": "checkout-service", "path": "checkout/pricing.py", "snippet": "premium_price = cache.get(key) or fetch_price(key); retry_on_miss=True"},
    {"id": "code_payment_timeout", "service": "payment-service", "path": "PaymentGatewayClient.java", "snippet": "Duration timeout = Duration.ofMillis(750);"},
    {"id": "code_invoice_idempotency", "service": "invoice-service", "path": "invoice/merge.py", "snippet": "merge_line_items(items) # TODO: restore idempotency key check"},
]
