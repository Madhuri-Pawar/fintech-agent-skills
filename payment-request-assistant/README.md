# Payment request assistant

A Claude skill for answering questions about ISO 20022 Request-to-Pay payments from your own Postgres database. Product managers, support and ops can ask "Why did this payment fail?", "Can it still be cancelled?" or "Where is it stuck?" and get a plain-language answer built from read-only SQL.

It recognizes the ID you paste (payment ID, EndToEndId, ResourceID or internal UUID), traces a payment from the client through the clearing house and back, and translates statuses and ISO reason codes into words. It only runs `SELECT` queries, always adds a `LIMIT`, skips PII columns and refuses to touch environments you mark as off limits.

Message types covered: pain.013, pain.014, pacs.002, camt.056 and camt.029.

## Structure

```
payment-request-assistant/
  SKILL.md              # instructions and safety rules
  references/
    data-model.md       # config, IDs, tables, statuses, reason codes
    queries.md          # ready-made SQL and the journey query
SETUP.md
```

## Getting started

See [SETUP.md](SETUP.md).

## License

MIT
