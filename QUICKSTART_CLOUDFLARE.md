# ARC Reply - Cloudflare Workers Quick Start Guide

Get ARC Reply running on Cloudflare Workers in 10 minutes with auto-deploy from GitHub.

---

## Prerequisites

- ✅ Cloudflare account (free tier works)
- ✅ GitHub account with ARC-Reply repository access
- ✅ Telegram Bot Token (from @BotFather)
- ✅ TwitterAPI.io API Key
- ✅ Groq API Key

---

## Step 1: Connect GitHub to Cloudflare (2 minutes)

1. **Open Cloudflare Dashboard**
   - Go to https://dash.cloudflare.com
   - Click "Workers & Pages"

2. **Create a new Worker**
   - Click "Create" → "Deploy with Git"
   - Select GitHub as source
   - Authorize Cloudflare to access GitHub

3. **Select Repository**
   - Search for and select `tokenarc/ARC-Reply`
   - Click "Connect"

4. **Configure Build Settings**
   - Framework: `None`
   - Build command: `npm install`
   - Build output directory: `.`
   - Root directory: `/`

5. **Deploy**
   - Click "Save and Deploy"
   - Wait for deployment to complete (~1-2 minutes)

---

## Step 2: Set Environment Secrets (3 minutes)

1. **Go to Worker Settings**
   - Cloudflare Dashboard → Workers & Pages
   - Click your worker name (`arc-reply`)
   - Click "Settings"

2. **Add Secrets**
   - Click "Add variable" under "Secrets"
   - Add three secrets:

   **Secret 1: TELEGRAM_BOT_TOKEN**
   - Name: `TELEGRAM_BOT_TOKEN`
   - Value: Your Telegram bot token from @BotFather
   - Click "Encrypt"

   **Secret 2: TWITTER_API_KEY**
   - Name: `TWITTER_API_KEY`
   - Value: Your TwitterAPI.io API key
   - Click "Encrypt"

   **Secret 3: GROQ_API_KEY**
   - Name: `GROQ_API_KEY`
   - Value: Your Groq API key
   - Click "Encrypt"

3. **Redeploy Worker**
   - After adding secrets, redeploy:
   - Click "Deployments" → Latest deployment → "Rollback & Redeploy"
   - Or wait for next GitHub push to auto-deploy

---

## Step 3: Configure Telegram Webhook (2 minutes)

1. **Get Your Worker URL**
   - Cloudflare Dashboard → Workers & Pages → Your worker
   - Copy the URL (e.g., `https://arc-reply.yourdomain.workers.dev`)

2. **Set Telegram Webhook**
   - Replace `<YOUR_BOT_TOKEN>` and `<WORKER_URL>`:
   ```bash
   curl -X POST https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook \
     -H "Content-Type: application/json" \
     -d '{"url": "<WORKER_URL>/webhook"}'
   ```

3. **Verify Webhook**
   ```bash
   curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo
   ```
   
   Should show:
   ```json
   {
     "ok": true,
     "result": {
       "url": "<WORKER_URL>/webhook",
       "has_custom_certificate": false,
       "pending_update_count": 0
     }
   }
   ```

---

## Step 4: Test Your Bot (2 minutes)

1. **Open Telegram**
   - Search for your bot
   - Send `/start` command

2. **Expected Response**
   ```
   👋 Welcome to ARC Reply, [Your Name]!
   
   I help you generate creative replies for Twitter/X posts...
   ```

3. **Test Reply Generation**
   - Send `/reply`
   - Follow the prompts to generate a reply

---

## Step 5: Enable Auto-Deploy (1 minute)

Auto-deploy is already enabled! Every time you push to `main` branch:

1. **Make changes** to the code
2. **Commit and push** to GitHub
3. **Cloudflare automatically deploys** within 1-2 minutes
4. **Check deployment status** in Cloudflare Dashboard

---

## Monitoring & Logs

### View Real-Time Logs

```bash
# Install Wrangler CLI (if not already installed)
npm install -g wrangler

# View logs
wrangler tail --service arc-reply
```

### Cloudflare Dashboard Logs

1. Go to Cloudflare Dashboard → Workers & Pages
2. Click your worker name
3. Click "Logs" tab
4. View real-time requests and responses

---

## Troubleshooting

### "Webhook not receiving updates"

1. **Verify webhook is set:**
   ```bash
   curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo
   ```

2. **Check worker URL is correct:**
   - Should be: `https://arc-reply.yourdomain.workers.dev/webhook`
   - Not: `https://arc-reply.yourdomain.workers.dev`

3. **Verify secrets are set:**
   - Go to Worker Settings → Secrets
   - All three secrets should be listed

4. **Redeploy after changing secrets:**
   - Secrets require redeployment to take effect

### "Invalid API Key" Error

1. **Verify API key is correct:**
   - Copy from original source (no extra spaces)
   - Check key hasn't expired

2. **Update secret:**
   - Go to Worker Settings → Secrets
   - Delete old secret
   - Add new secret with correct value
   - Redeploy worker

### Deployment Failed

1. **Check GitHub Actions:**
   - Go to GitHub → ARC-Reply → Actions
   - View workflow logs for errors

2. **Manual redeploy:**
   - Cloudflare Dashboard → Workers → Deployments
   - Click "Rollback & Redeploy" on previous version

---

## Next Steps

1. ✅ Bot is running on Cloudflare Workers
2. ✅ Telegram webhook is configured
3. ✅ Auto-deploy from GitHub is enabled
4. ✅ Start using the bot!

**Optional:**
- Set up custom domain (Cloudflare → Workers → Routes)
- Configure monitoring alerts
- Set up GitHub Actions for testing
- Add more reply styles or languages

---

## Support

For issues or questions:

1. **Check logs:** `wrangler tail --service arc-reply`
2. **Review documentation:** See `CLOUDFLARE_DEPLOYMENT.md`
3. **GitHub Issues:** Create issue in ARC-Reply repository
4. **Cloudflare Support:** https://support.cloudflare.com

---

## Key Files

| File | Purpose |
|------|---------|
| `worker.js` | Cloudflare Workers webhook handler |
| `wrangler.toml` | Worker configuration |
| `package-workers.json` | Dependencies for Workers |
| `CLOUDFLARE_DEPLOYMENT.md` | Detailed deployment guide |
| `ENV_TEMPLATE.md` | Environment variables reference |

---

**Status:** ✅ Ready for Production

Your ARC Reply bot is now live on Cloudflare Workers with auto-deploy enabled!
