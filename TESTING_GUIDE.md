# ARC Reply - Testing Guide

Comprehensive testing procedures for webhook endpoint and bot functionality.

---

## Pre-Testing Checklist

- ✅ Cloudflare Worker deployed
- ✅ All secrets configured (TELEGRAM_BOT_TOKEN, TWITTER_API_KEY, GROQ_API_KEY)
- ✅ Telegram webhook set
- ✅ Worker URL accessible
- ✅ GitHub repository connected

---

## 1. Webhook Endpoint Tests

### 1.1 Health Check Endpoint

**Test health endpoint:**

```bash
curl https://arc-reply.yourdomain.workers.dev/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "bot": "ARC Reply"
}
```

**Status Code:** `200 OK`

---

### 1.2 Root Endpoint

**Test root endpoint:**

```bash
curl https://arc-reply.yourdomain.workers.dev/
```

**Expected Response:**
```json
{
  "message": "ARC Reply Bot - Cloudflare Workers",
  "version": "1.0.0",
  "endpoints": {
    "webhook": "/webhook (POST)",
    "health": "/health (GET)"
  }
}
```

**Status Code:** `200 OK`

---

### 1.3 Webhook Endpoint (POST)

**Test webhook with mock Telegram update:**

```bash
curl -X POST https://arc-reply.yourdomain.workers.dev/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "update_id": 1,
    "message": {
      "message_id": 1,
      "date": 1234567890,
      "chat": {
        "id": 123456789,
        "type": "private"
      },
      "from": {
        "id": 123456789,
        "is_bot": false,
        "first_name": "Test"
      },
      "text": "/start"
    }
  }'
```

**Expected Response:**
```json
{
  "ok": true
}
```

**Status Code:** `200 OK`

---

### 1.4 Invalid Request Test

**Test with invalid method (GET to webhook):**

```bash
curl -X GET https://arc-reply.yourdomain.workers.dev/webhook
```

**Expected Response:**
```
Method Not Allowed
```

**Status Code:** `405 Method Not Allowed`

---

### 1.5 Unknown Route Test

**Test with non-existent endpoint:**

```bash
curl https://arc-reply.yourdomain.workers.dev/unknown
```

**Expected Response:**
```json
{
  "error": "Not Found"
}
```

**Status Code:** `404 Not Found`

---

## 2. Telegram Bot Tests

### 2.1 Start Command

1. **Open Telegram**
2. **Find your bot** (search by name)
3. **Send `/start`**

**Expected Response:**
```
👋 Welcome to ARC Reply, [Your Name]!

I help you generate creative replies for Twitter/X posts. Here's what I can do:

🔄 **Generate Replies** - Send me:
  • A tweet link (twitter.com/user/status/...)
  • A screenshot of a tweet
  • Plain text of a tweet

🎨 **Customize Style** - Choose from:
  • GenZ - Trendy and casual
  • Professional - Formal and business-like
  • Casual - Friendly and conversational
  • Sarcastic - Witty and ironic
  • Motivational - Inspirational and uplifting

📏 **Adjust Length** - Pick:
  • Short (10-30 words)
  • Medium (50-100 words)
  • Long (150-250 words)
  • Custom word count

🌍 **Multiple Languages** - Supported:
  • English, Urdu, Japanese, Spanish, French
  • German, Chinese, Hindi, Portuguese, Russian

Use /reply to get started!
```

---

### 2.2 Reply Command

1. **Send `/reply`**

**Expected Response:**
```
📝 Let's generate a reply! Send me:
  • A tweet link (twitter.com/user/status/...)
  • A screenshot of a tweet
  • Plain text of a tweet

Or send /cancel to go back.
```

---

### 2.3 Text Input Test

1. **Send `/reply`**
2. **Send plain text:** `"This is an amazing product! Everyone should try it."`

**Expected Response:**
```
Great! Now choose a reply style:

🎨 **Style Options:**
  1️⃣ GenZ - Trendy and casual
  2️⃣ Professional - Formal and business-like
  3️⃣ Casual - Friendly and conversational
  4️⃣ Sarcastic - Witty and ironic
  5️⃣ Motivational - Inspirational and uplifting

Send the number (1-5) or the style name.
```

---

### 2.4 Style Selection Test

1. **Complete text input**
2. **Send `1` (for GenZ style)**

**Expected Response:**
```
Perfect! Now choose reply length:

📏 **Length Options:**
  1️⃣ Short (10-30 words)
  2️⃣ Medium (50-100 words)
  3️⃣ Long (150-250 words)
  4️⃣ Custom (specify word count)

Send the number (1-4) or the length name.
```

---

### 2.5 Length Selection Test

1. **Complete style selection**
2. **Send `2` (for Medium length)**

**Expected Response:**
```
Great! Now choose a language:

🌍 **Language Options:**
  1️⃣ English
  2️⃣ Urdu
  3️⃣ Japanese
  4️⃣ Spanish
  5️⃣ French
  6️⃣ German
  7️⃣ Chinese
  8️⃣ Hindi
  9️⃣ Portuguese
  🔟 Russian

Send the number (1-10) or the language name.
```

---

### 2.6 Language Selection & Reply Generation

1. **Complete length selection**
2. **Send `1` (for English)**

**Expected Response:**
```
✨ Generating replies...

Here are 3 reply options:

**Option 1 (GenZ):**
[AI-generated reply in GenZ style]

**Option 2 (GenZ):**
[AI-generated reply in GenZ style]

**Option 3 (GenZ):**
[AI-generated reply in GenZ style]

Select a reply to post to X or send /cancel to go back.
```

---

### 2.7 Help Command

1. **Send `/help`**

**Expected Response:**
```
📚 **ARC Reply Help**

Commands:
  /start - Welcome message
  /reply - Generate a reply
  /help - Show this help message
  /cancel - Cancel current operation

Features:
  • Generate multiple reply styles
  • Choose reply length
  • Support for 10 languages
  • Direct posting to X (Twitter)
  • OCR for tweet screenshots

For more info, visit: [GitHub URL]
```

---

### 2.8 Cancel Command

1. **Send `/reply`**
2. **Send `/cancel`**

**Expected Response:**
```
Operation cancelled. Send /reply to start again or /help for more options.
```

---

## 3. Error Handling Tests

### 3.1 Invalid API Key

**Simulate invalid Groq API key:**

1. **Go to Cloudflare Dashboard**
2. **Update GROQ_API_KEY secret** with invalid key
3. **Redeploy worker**
4. **Send `/reply` and complete setup**

**Expected Response:**
```
❌ Error generating replies: Invalid API key

Please try again or contact support.
```

---

### 3.2 Network Error Handling

1. **Simulate network timeout** (by disconnecting internet briefly)
2. **Send `/reply` command**

**Expected Response:**
```
⚠️ Network error. Please try again.
```

---

### 3.3 Malformed JSON

**Test with invalid JSON:**

```bash
curl -X POST https://arc-reply.yourdomain.workers.dev/webhook \
  -H "Content-Type: application/json" \
  -d '{invalid json}'
```

**Expected Response:**
```json
{
  "ok": false,
  "error": "Invalid JSON"
}
```

**Status Code:** `500 Internal Server Error`

---

## 4. Performance Tests

### 4.1 Response Time

**Measure webhook response time:**

```bash
time curl -X POST https://arc-reply.yourdomain.workers.dev/webhook \
  -H "Content-Type: application/json" \
  -d '{"update_id": 1}'
```

**Expected:** Response time < 100ms

---

### 4.2 Concurrent Requests

**Test with multiple concurrent requests:**

```bash
for i in {1..10}; do
  curl -X POST https://arc-reply.yourdomain.workers.dev/webhook \
    -H "Content-Type: application/json" \
    -d "{\"update_id\": $i}" &
done
wait
```

**Expected:** All requests succeed with 200 OK

---

## 5. Logging Tests

### 5.1 View Real-Time Logs

```bash
wrangler tail --service arc-reply
```

**Expected:** See incoming webhook requests and bot responses

---

### 5.2 Check Error Logs

1. **Send invalid command to bot**
2. **Check logs for error messages**

```bash
wrangler tail --service arc-reply | grep -i error
```

---

## 6. Deployment Tests

### 6.1 GitHub Auto-Deploy

1. **Make a code change** in GitHub
2. **Commit and push** to `main` branch
3. **Check GitHub Actions** for deployment status
4. **Verify worker updated** by checking logs

---

### 6.2 Rollback Test

1. **Go to Cloudflare Dashboard**
2. **Workers → Deployments**
3. **Click "Rollback & Redeploy"** on previous version
4. **Verify bot still works**

---

## 7. Integration Tests

### 7.1 Tweet Link Processing

1. **Send `/reply`**
2. **Send tweet link:** `https://twitter.com/user/status/1234567890`

**Expected:** Bot fetches tweet and processes it

---

### 7.2 Screenshot Processing

1. **Send `/reply`**
2. **Send screenshot of tweet**

**Expected:** Bot extracts text via OCR and processes it

---

## Test Results Template

```markdown
# Test Results - [Date]

## Webhook Tests
- [ ] Health check: PASS/FAIL
- [ ] Root endpoint: PASS/FAIL
- [ ] Webhook POST: PASS/FAIL
- [ ] Invalid method: PASS/FAIL
- [ ] Unknown route: PASS/FAIL

## Bot Tests
- [ ] /start command: PASS/FAIL
- [ ] /reply command: PASS/FAIL
- [ ] Text input: PASS/FAIL
- [ ] Style selection: PASS/FAIL
- [ ] Length selection: PASS/FAIL
- [ ] Language selection: PASS/FAIL
- [ ] Reply generation: PASS/FAIL
- [ ] /help command: PASS/FAIL
- [ ] /cancel command: PASS/FAIL

## Error Handling
- [ ] Invalid API key: PASS/FAIL
- [ ] Network error: PASS/FAIL
- [ ] Malformed JSON: PASS/FAIL

## Performance
- [ ] Response time < 100ms: PASS/FAIL
- [ ] Concurrent requests: PASS/FAIL

## Deployment
- [ ] Auto-deploy works: PASS/FAIL
- [ ] Rollback works: PASS/FAIL

## Notes
[Any issues or observations]
```

---

## Troubleshooting Failed Tests

### Webhook not responding

1. Check worker is deployed: `wrangler deployments list`
2. Verify URL is correct
3. Check Cloudflare dashboard for errors
4. Review logs: `wrangler tail --service arc-reply`

### Bot not responding in Telegram

1. Verify webhook is set: `curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo`
2. Check secrets are configured correctly
3. Redeploy worker after changing secrets
4. Review logs for errors

### Slow response times

1. Check CPU usage in Cloudflare dashboard
2. Optimize code if needed
3. Check API response times from external services
4. Consider increasing CPU limit in `wrangler.toml`

---

## Next Steps

After all tests pass:

1. ✅ Deploy to production
2. ✅ Monitor logs regularly
3. ✅ Set up alerts for errors
4. ✅ Plan regular testing schedule

---

**Testing Status:** Ready for comprehensive testing

Run through all tests to ensure ARC Reply is functioning correctly on Cloudflare Workers.
