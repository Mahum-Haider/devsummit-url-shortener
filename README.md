# DevSummit URL Shortener

A fully serverless URL shortener built for a tech conference scenario where speakers need branded short links for their talk resources.

## The Problem
Speakers at DevSummit share resource links during talks, but long URLs on slides are unreadable. This system lets organizers create short, memorable links that attendees can type or scan as QR codes.

## Architecture

Flow 1 — Speaker creates a short URL

POST /shorten → API Gateway → Lambda (createShortUrl) → DynamoDB

Flow 2 — Attendee scans QR code or types short URL

GET /{code} → API Gateway → Lambda (redirectUrl) → DynamoDB → 301 Redirect

## Architecture Diagram
![Architecture](docs/screenshots/architecture-diagram.png)

## AWS Services Used

| Service | Purpose |
|---|---|
| AWS Lambda | Serverless compute for create and redirect logic |
| API Gateway | HTTP API exposing POST /shorten and GET /{code} |
| DynamoDB | NoSQL database storing URL mappings and click counts |
| IAM | Scoped execution role with least privilege access |

## Features
- Create short codes from long URLs
- Instant 301 redirects with millisecond DynamoDB lookups
- Atomic click counter per link
- Duplicate URL detection via GSI reverse lookup
- Least privilege IAM role scoped to one table

## Deployment Evidence

### DynamoDB Table
![DynamoDB Table](docs/screenshots/dynamodb-table-created.png)

### GSI Active
![GSI Active](docs/screenshots/dynamodb-gsi-active.png)

### IAM Role
![IAM Role](docs/screenshots/iam-role-created.png)

### Lambda Functions Deployed
![Lambda Create](docs/screenshots/lambda-create-deployed.png)
![Lambda Redirect](docs/screenshots/lambda-redirect-deployed.png)

### API Gateway Routes
![API Gateway](docs/screenshots/api-gateway-routes.png)

### Live Redirect Working
![Redirect Test](docs/screenshots/test-redirect-working.png)

### DynamoDB Click Counter
![Click Counter](docs/screenshots/dynamodb-click-counter.png)

### Duplicate Detection
![Duplicate Detection](docs/screenshots/test-duplicate-detection.png)

## Key Design Decisions

**Why Lambda?**
Traffic spikes are unpredictable at conferences — 5,000 attendees might scan a QR code simultaneously. Lambda auto-scales instantly with no pre-provisioned servers.

**Why DynamoDB?**
Single-digit millisecond reads on partition key lookups. A redirect needs to be near-instant or the attendee experience suffers.

**Why HTTP API Gateway over REST API?**
70% cheaper per million requests and lower latency — the right choice for a high-volume redirect use case.

**Why a GSI?**
DynamoDB can only query by partition key by default. The GSI on original_url lets us detect duplicates before creating a new short code.

**Why least privilege IAM?**
Lambda only needs 4 DynamoDB actions on one table. Scoping the role minimizes blast radius if the function were ever compromised.

## What I'd Build Next
- Custom domain (devsummit.io/s/abc123)
- CloudWatch dashboard for monitoring
- Auto-generated QR code per short link
- Admin panel to view all links and click counts
