import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react({
      babel: {
        plugins: [['babel-plugin-react-compiler']],
      },
    }),
    tailwindcss(),
  ],
  // Forward API calls to FastAPI so the browser only talks to the Vite dev server (same origin).
  // Fixes 404s when requests accidentally hit :5173 instead of :8000, and avoids CORS issues in dev.
  server: {
    proxy: {
      // Use localhost so it matches how many users start uvicorn (avoids 127.0.0.1 vs localhost mismatches).
      // IPv4 avoids Windows resolving "localhost" to ::1 while uvicorn listens on 127.0.0.1
      '/auth': { target: 'http://127.0.0.1:8000', changeOrigin: true },
      '/api': { target: 'http://127.0.0.1:8000', changeOrigin: true },
    },
  },
})
