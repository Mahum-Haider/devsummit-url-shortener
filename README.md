# DevSummit URL Shortener

A fully serverless URL shortener built for a tech conference scenario where speakers need branded short links for their talk resources.

---

## 📌 The Problem

Speakers at DevSummit share resource links during talks, but long URLs on slides are unreadable. This system allows organizers to generate short, memorable links that attendees can easily type or scan via QR codes.

---

## 🏗 Architecture

This system follows a fully serverless, event-driven design with two main flows:

### Flow 1 — Create Short URL
POST /shorten  
→ API Gateway  
→ Lambda (createShortUrl)  
→ DynamoDB (store mapping)

### Flow 2 — Redirect User
GET /{code}  
→ API Gateway  
→ Lambda (redirectUrl)  
→ DynamoDB (lookup)  
→ 301 Redirect response

---

## 🧩 Architecture Diagram
![Architecture](assets/screenshots/architecture-diagram.png)

---

## ☁️ AWS Services Used

| Service | Purpose |
|---|---|
| AWS Lambda | Serverless compute for create and redirect logic |
| API Gateway | HTTP API exposing POST /shorten and GET /{code} |
| DynamoDB | NoSQL database storing URL mappings and click counts |
| IAM | Scoped execution role with least privilege access |

---

## ✨ Features

- Create short codes from long URLs  
- Instant 301 redirects with millisecond DynamoDB lookups  
- Atomic click counter per link  
- Duplicate URL detection via GSI reverse lookup  
- Least privilege IAM role scoped to one table  

---

## 📸 Screenshots

### 🗄 DynamoDB Setup
![DynamoDB Table](assets/screenshots/dynamodb-table-created.png)  
![GSI Active](assets/screenshots/dynamodb-gsi-active.png)

### ⚙️ Lambda Functions
![Lambda Create](assets/screenshots/lambda-create-deployed.png)  
![Lambda Redirect](assets/screenshots/lambda-redirect-deployed.png)

### 🌐 API Gateway
![API Gateway](assets/screenshots/api-gateway-routes.png)

### 🔁 End-to-End Test
![Redirect Test](assets/screenshots/test-redirect-working.png)

### 📊 Click Tracking
![Click Counter](assets/screenshots/dynamodb-click-counter.png)

---

## 🚀 What I Learned

- Designing stateless serverless architectures using AWS Lambda  
- Structuring DynamoDB for both primary access and reverse lookups (GSI)  
- Implementing efficient redirects with minimal latency  
- Applying least-privilege IAM policies in real-world scenarios  
- Building production-style APIs using API Gateway  

---

## 📌 Future Improvements

- Add custom domain (Route 53 + CloudFront)  
- Implement rate limiting & abuse protection  
- Add authentication for link creation  
- Build an analytics dashboard for link performance  

---

## 🛠 Setup & Deployment (Optional)

> Add your deployment steps here if you want recruiters to see reproducibility.
