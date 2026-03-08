/**
 * ARC Reply - Cloudflare Workers Webhook Handler
 * Handles Telegram bot webhook updates using native fetch-based pattern
 */

/**
 * Send a message to Telegram
 */
async function sendMessage(token, chatId, text) {
  await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ chat_id: chatId, text })
  });
}

/**
 * Process incoming Telegram update and generate a reply
 */
async function processUpdate(update, env) {
  if (update.message?.text) {
    const chatId = update.message.chat.id;
    const userText = update.message.text;

    // Log incoming message
    console.log(`Message from ${chatId}: ${userText}`);

    // Generate reply using Groq API
    let replyText = 'I received your message.';
    try {
      const groqResponse = await fetch('https://api.groq.com/openai/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${env.GROQ_API_KEY}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: 'llama3-8b-8192',
          messages: [
            { role: 'system', content: 'You are ARC-Reply, a helpful assistant.' },
            { role: 'user', content: userText },
          ],
        }),
      });

      if (groqResponse.ok) {
        const data = await groqResponse.json();
        replyText = data.choices[0].message.content;
      }
    } catch (error) {
      console.error('Groq API error:', error);
      replyText = 'Sorry, I encountered an error processing your message.';
    }

    // Send reply back to Telegram
    await sendMessage(env.TELEGRAM_BOT_TOKEN, chatId, replyText);
  }
}

/**
 * Main fetch handler for Cloudflare Workers
 */
export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Health check endpoint
    if (url.pathname === '/health') {
      return new Response(JSON.stringify({ status: 'healthy', bot: 'ARC Reply' }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // Webhook endpoint for Telegram updates
    if (url.pathname === '/webhook' && request.method === 'POST') {
      try {
        const update = await request.json();
        console.log('Incoming update:', JSON.stringify(update, null, 2));

        // Process the update asynchronously
        await processUpdate(update, env);

        return new Response(JSON.stringify({ ok: true }), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        });
      } catch (error) {
        console.error('Webhook error:', error);
        return new Response(JSON.stringify({ ok: false, error: error.message }), {
          status: 500,
          headers: { 'Content-Type': 'application/json' },
        });
      }
    }

    // Root endpoint
    if (url.pathname === '/') {
      return new Response(JSON.stringify({
        message: 'ARC Reply Bot - Cloudflare Workers',
        version: '1.0.0',
        endpoints: {
          webhook: '/webhook (POST)',
          health: '/health (GET)',
        }
      }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // 404 for unknown routes
    return new Response(JSON.stringify({ error: 'Not Found' }), {
      status: 404,
      headers: { 'Content-Type': 'application/json' },
    });
  },
};
