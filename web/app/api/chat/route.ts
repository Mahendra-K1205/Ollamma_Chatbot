export const runtime = 'edge';

export async function POST(request: Request) {
  const { message, model, history } = await request.json();
  
  const ollamaUrl = process.env.OLLAMA_API_URL || 'http://localhost:11434';
  
  try {
    const response = await fetch(`${ollamaUrl}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: model || 'llama3.2:latest',
        messages: [...history, { role: 'user', content: message }],
        stream: false
      })
    });
    
    if (!response.ok) {
      throw new Error(`Ollama API error: ${response.statusText}`);
    }
    
    const data = await response.json();
    return Response.json({ 
      message: data.message.content,
      success: true 
    });
    
  } catch (error) {
    return Response.json({ 
      error: error.message,
      success: false 
    }, { status: 500 });
  }
}
