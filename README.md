# ARC-Reply

## Overview
ARC-Reply is a powerful framework for building serverless applications. Designed for high performance and simplicity, it allows developers to quickly create and deploy applications without worrying about the infrastructure.

## Features
- Fast response times and low latency
- Automatic scaling with Cloudflare Workers
- Rich set of built-in utilities
- **Note**: OCR capabilities are disabled for Cloudflare Workers deployment.

## Installation
1. Clone this repository
2. Install dependencies using npm or yarn
3. Deploy to Cloudflare Workers as per the deployment guide

## Technology Stack
- Node.js (Cloudflare Workers runtime)
- Telegram Bot API
- Groq API for LLM-powered replies
- Zod for schema validation
- Axios for HTTP requests

## Migration Note
The project has been migrated from Python to Node.js to better support Cloudflare Workers. Python-only dependencies have been removed, and the core logic now resides in `index.js`.

## Contribution Guidelines
Please refer to the CONTRIBUTING.md file for more details on how to contribute to this project.