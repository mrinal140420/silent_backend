

# 🔐 SilentDrop Backend

**SilentDrop Backend** is a **zero-knowledge, privacy-first file transfer service** built with **FastAPI** and **MongoDB GridFS**, where **all encryption happens on the client side** and the server **never accesses plaintext data or encryption keys**.

This repository contains the **fully deployed, tested, and security-hardened backend** of the SilentDrop system.

**Frontend Repo**
👉[https://github.com/mrinal140420/silent_frontend](https://github.com/mrinal140420/silent_frontend)

## ✨ Key Features

* 🔒 **Zero-Knowledge Architecture**

  * Server never sees plaintext files
  * No encryption keys stored or processed backend-side

* 📦 **Encrypted File Storage**

  * Uses MongoDB GridFS to store encrypted blobs
  * Handles large files beyond MongoDB document limits

* 🔗 **Secure Link-Based Access**

  * Cryptographically strong access tokens
  * Optional password protection (bcrypt-hashed)

* ⏱️ **Controlled File Lifecycle**

  * Time-based expiry (TTL)
  * Download-count limits
  * Automatic self-destruction after final download

* 🛡️ **Security Hardening**

  * Rate limiting (IP + token)
  * Security HTTP headers
  * Privacy-preserving `404` responses after destruction

* 🚀 **Production Deployed**

  * Live on Render (free tier)
  * HTTPS enabled
  * Environment-based configuration

---

## 🧠 Zero-Knowledge Guarantee

SilentDrop enforces **strict zero-knowledge principles**:

| Aspect                 | Guarantee                  |
| ---------------------- | -------------------------- |
| Plaintext files        | ❌ Never handled by backend |
| Encryption keys        | ❌ Never stored or logged   |
| File inspection        | ❌ Not performed            |
| Metadata exposure      | ✅ Minimal & non-sensitive  |
| Database breach impact | ✅ Encrypted data only      |



## 🏗️ Tech Stack

* **Framework:** FastAPI (Python 3.11+)
* **Database:** MongoDB Atlas (Free Tier)
* **File Storage:** MongoDB GridFS
* **Security:** bcrypt, rate limiting, security headers
* **Deployment:** Render
* **Docs:** OpenAPI / Swagger



## 📁 Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── upload.py
│   │   ├── download.py
│   │   ├── metadata.py
│   │   ├── links.py
│   │   └── destroy.py
│   ├── services/
│   │   ├── cleanup.py
│   │   └── rate_limit.py
│   ├── utils/
│   │   └── security.py
│   ├── db/
│   │   └── mongo.py
│   └── main.py
├── requirements.txt
└── README.md
```

---

## 🌐 Deployed Backend

**Base URL:**

```
https://silent-backend-2l1v.onrender.com
```

### API Documentation (Swagger)

```
/docs
```

---

## 🔌 API Endpoints

| Method | Endpoint                      | Description                  |
| ------ | ----------------------------- | ---------------------------- |
| POST   | `/api/upload`                 | Upload encrypted file        |
| POST   | `/api/create-link`            | Generate secure access link  |
| GET    | `/api/file/{token}/metadata`  | Fetch non-sensitive metadata |
| GET    | `/api/file/{token}/download`  | Download encrypted file      |
| POST   | `/api/file/{file_id}/destroy` | Manually destroy file        |
| GET    | `/health`                     | Health check                 |

---

## 🧪 Backend Verification (Automated Test)

The deployed backend has been validated using an **automated end-to-end test script** covering:

* Upload
* Link creation
* Metadata access
* Download
* Auto-destruction
* Post-destruction privacy behavior

### ✅ Test Result

```
🎉 ALL DEPLOYED BACKEND TESTS PASSED
```

This confirms **functional correctness, security enforcement, and lifecycle integrity**.

---

## 🔐 Security Measures Implemented

* Cryptographically secure tokens
* bcrypt password hashing
* Rate limiting (IP + token)
* Upload abuse protection
* Security headers:

  * `X-Content-Type-Options`
  * `X-Frame-Options`
  * `Referrer-Policy`
  * `Permissions-Policy`
* Privacy-preserving error semantics (404 after destroy)

---

## ⚠️ Explicitly Out of Scope

The backend **intentionally does NOT** implement:

* File previews
* Virus scanning
* Server-side decryption
* Content inspection
* User accounts / OAuth
* Object storage (S3, GCS)

These are excluded to **preserve zero-knowledge guarantees**.

---

## 🔧 Environment Variables

```env
MONGODB_ATLAS_URI=your_mongodb_uri
JWT_SECRET=strong_random_secret
APP_ENV=production
```

Secrets are managed **only via environment variables** and never hard-coded.

---

## 🎓 Academic Context

This backend is designed as part of a **Mini Project Semester VI** demonstrating:

* Privacy-by-design architecture
* Zero-knowledge security models
* Secure cloud deployment on free tier
* Real-world backend engineering practices



## 📜 License

This project is provided for **academic and educational purposes**.






