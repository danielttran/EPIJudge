import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  cacheDir: process.env.EPI_VITE_CACHE_DIR || 'node_modules/.vite',
  optimizeDeps: {
    // Pre-bundle every grammar before opening the
    // browser so loading it cannot invalidate React's dependency bundle.
    entries: ['index.html', 'src/Editor.tsx'],
    include: [
      'react',
      'react-dom',
      'react-dom/client',
      'react/jsx-runtime',
      'react/jsx-dev-runtime',
      'lucide-react',
      'monaco-editor/esm/vs/editor/editor.api',
      ...['csharp', 'javascript', 'python', 'cpp', 'java'].map(
        (language) => `monaco-editor/esm/vs/basic-languages/${language}/${language}`,
      ),
    ],
  },
  server: {
    host: 'localhost',
    port: 5173,
    strictPort: true,
    warmup: { clientFiles: ['./src/main.tsx', './src/Editor.tsx'] },
    hmr: process.env.EPI_WEB_PORT
      ? { clientPort: Number(process.env.EPI_WEB_PORT), path: '/__vite_hmr' }
      : undefined,
    proxy: { '/api': { target: 'http://localhost:5178', changeOrigin: true } },
  },
  build: {
    chunkSizeWarningLimit: 2500,
    rollupOptions: {
      output: {
        manualChunks: (id) => id.includes('/node_modules/monaco-editor/') ? 'monaco' : undefined,
      },
    },
  },
});
