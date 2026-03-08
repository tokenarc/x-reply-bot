/**
 * ARC Reply - Cloudflare Workers Webhook Handler
 * Handles Telegram bot updates and replies using Groq API
 */

import axios from 'axios';
import { z } from 'zod';

// Schema for incoming Telegram updates (minimal for our needs)
const TelegramUpdateSchema = z.object({
  message: z.object({
    chat: z.object({
      id: z.number(),
    }),
    text: z.string().optional(),
  }).optional(),
});

/**
 * Send a message back to Telegram
 */
async function sendTelegramMessage(chatId, text, token) {
  const url = `https://api.telegram.org/bot${token}/sendMessage`;
  try {
    await axios.post(url, {
      chat_id: chatId,
      text: text,
    });
  } catch (error) {
    console.error('Error sending Telegram message:', error.response?.data || error.message);
  }
}

/**
 * Generate a reply using Groq API
 */
async function generateGroqReply(userMessage, apiKey) {
  const url = 'https://api.groq.com/openai/v1/chat/completions';
  try {
    const response = await axios.post(
      url,
      {
        model: 'llama3-8b-8192',
        messages: [
          { role: 'system', content: 'You are ARC-Reply, a helpful assistant.' },
          { role: 'user', content: userMessage },
        ],
      },
      {
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data.choices[0].message.content;
  } catch (error) {
    console.error('Error calling Groq API:', error.response?.data || error.message);
    return "Sorry, I'm having trouble thinking right now.";
  }
}

/**
 * Main fetch handler for Cloudflare Workers
 */
export default {
  async fetch(request, env, ctx) {
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
        const body = await request.json();
        console.log('Received Telegram update:', JSON.stringify(body));

        const result = TelegramUpdateSchema.safeParse(body);
        if (!result.success) {
          return new Response('Invalid update format', { status: 400 });
        }

        const { message } = result.data;
        if (message && message.text) {
          const chatId = message.chat.id;
          const userText = message.text;

          // Generate reply via Groq
          const replyText = await generateGroqReply(userText, env.GROQ_API_KEY);

          // Send reply back to Telegram
          await sendTelegramMessage(chatId, replyText, env.TELEGRAM_BOT_TOKEN);
        }

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

    // Default response
    return new Response(JSON.stringify({ 
      message: 'ARC Reply Bot - Cloudflare Workers',
      endpoints: {
        webhook: '/webhook (POST)',
        health: '/health (GET)',
      }
    }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  },
};
