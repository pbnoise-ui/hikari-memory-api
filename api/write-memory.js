export const config = {
  runtime: 'edge',
}

export default async function handler(req) {
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Only POST allowed' }), {
      status: 405,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const { user_input, response } = await req.json();
  const timestamp = new Date().toISOString();

  const memoryEntry = {
    user_input,
    response,
    timestamp
  };

  // Replace this URL with your actual Render Flask API
  const flaskEndpoint = "https://hikari-memory-api.onrender.com/write_memory";

  const result = await fetch(flaskEndpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(memoryEntry)
  });

  const body = await result.text();
  return new Response(body, {
    status: result.status,
    headers: { 'Content-Type': 'application/json' }
  });
}
