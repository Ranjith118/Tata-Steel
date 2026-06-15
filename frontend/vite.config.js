import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
  },
  // Expose VITE_API_URL to the app at build time
  // Set VITE_API_URL=https://your-backend.railway.app in Railway frontend env vars
  define: {
    __API_URL__: JSON.stringify(process.env.VITE_API_URL || ''),
  },
})