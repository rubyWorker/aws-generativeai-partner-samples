import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import basicSsl from '@vitejs/plugin-basic-ssl'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(),
    basicSsl()  // Enable HTTPS with self-signed cert
  ],
  server: {
    https: true,
    port: 9000,
    host: 'localhost',
    proxy: {
      '/api/agentcore': {
        target: 'https://bedrock-agentcore.us-east-2.amazonaws.com',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/agentcore/, ''),
      },
    },
  }
})
