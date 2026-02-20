export const runtime = 'edge';

export async function GET() {
  const ollamaUrl = process.env.OLLAMA_API_URL || 'http://localhost:11434';
  
  try {
    const response = await fetch(`${ollamaUrl}/api/tags`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    });
    
    if (!response.ok) {
      throw new Error(`Ollama API error: ${response.statusText}`);
    }
    
    const data = await response.json();
    const models = data.models.map(m => m.name);
    
    return Response.json({ 
      models,
      success: true 
    });
    
  } catch (error) {
    return Response.json({ 
      error: error.message,
      success: false 
    }, { status: 500 });
  }
}
