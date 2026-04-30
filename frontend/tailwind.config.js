/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{vue,js}'],
  theme: {
    extend: {
      colors: {
        primary: '#0a0a0f',
        accent: '#00d4aa',
        surface: '#0a0a0f',
        danger: '#ff6b6b',
        muted: 'rgba(255,255,255,0.45)',
        'pharma-50':  '#f0f9ff',
        'pharma-100': '#e0f2fe',
        'pharma-200': '#bae6fd',
        'pharma-300': '#7dd3fc',
        'pharma-400': '#38bdf8',
        'pharma-500': '#0ea5e9',
        'pharma-600': '#0284c7',
        'pharma-700': '#0369a1',
        'pharma-800': '#075985',
        'pharma-900': '#0c4a6e',
        'dark-100':  '#f1f5f9',
        'dark-200':  '#e2e8f0',
        'dark-300':  '#cbd5e1',
        'dark-400':  '#94a3b8',
        'dark-500':  '#64748b',
        'dark-600':  '#475569',
        'dark-700':  '#334155',
        'dark-800':  '#1e293b',
        'dark-900':  '#0f172a',
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'SF Pro Display', 'SF Pro Text', 'Helvetica Neue', 'Helvetica', 'Arial', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
