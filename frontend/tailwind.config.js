/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      colors: {
        medical: {
          blue: '#2563eb',
          teal: '#0d9488',
          red: '#dc2626',
          green: '#16a34a',
          purple: '#7c3aed',
          orange: '#ea580c',
        }
      }
    },
  },
  plugins: [],
}

