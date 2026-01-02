# API Documentation

## Overview
This API provides services for analyzing security reports (Semgrep, Gitleaks).

## Versioning
The API uses path-based versioning (e.g., `/v1/`).

## Endpoints

### Explain Semgrep
- **URL**: `/v1/explain/semgrep`
- **Method**: `POST` (Note: Changed from GET to POST to support body payload)
- **Body**: SARIF JSON content.

### Explain Gitleaks
- **URL**: `/v1/explain/gitleaks`
- **Method**: `POST`
- **Body**: JSON content.
