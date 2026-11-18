# Security policy

## Scope
StratifyAI is a portfolio MVP and local demonstration. It is not currently designed or approved for sensitive, confidential, or production customer data.

## Reporting a vulnerability
Please do not publish exploitable vulnerability details in a public issue. Contact the repository maintainer privately through GitHub's available contact options and include a concise description, affected component, and safe reproduction steps.

## Current security limitations
- Authentication and workspace-level authorisation are not implemented.
- Rate limiting, audit logging, and production secrets management are not implemented.
- Demo reset deletes the feedback, opportunity, and experiment rows in the configured database.
- The Docker Compose credentials are development-only.
- Do not commit secrets, access tokens, customer-identifiable feedback, or private interview notes.

Before any production or customer-data use, perform a security and privacy review and implement appropriate identity, authorisation, data retention, backup, and operational controls.
