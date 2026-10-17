import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    host: 'localhost',
    port: 5173,
    strictPort: true,
    hmr: process.env.EPI_WEB_PORT
      ? { clientPort: Number(process.env.EPI_WEB_PORT), path: '/__vite_hmr' }
      : undefined,
    proxy: { '/api': { target: 'http://localhost:5178', changeOrigin: true } },
  },
  build: { chunkSizeWarningLimit: 2500 },
});
