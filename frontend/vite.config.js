import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  // In production (HF Spaces) the React app is served from the same origin
  // as the API, so no proxy is needed.  The proxy only applies during local dev.
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
    // Ensure asset paths are relative so they work under any sub-path
    assetsDir: 'assets',
  },
})