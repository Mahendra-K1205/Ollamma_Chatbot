import './globals.css'

export const metadata = {
  title: 'Ollama Chatbot',
  description: 'Local LLM chatbot powered by Ollama',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
