/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  env: {
    OLLAMA_API_URL: process.env.OLLAMA_API_URL || 'http://localhost:11434',
  },
}

module.exports = nextConfig
