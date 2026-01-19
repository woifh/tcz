/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.html",
    "./app/static/js/**/*.js",
  ],
  safelist: [
    // Temporary block colors (generated dynamically in dashboard.js and templates)
    'bg-yellow-400',
    'bg-yellow-100',
    'bg-yellow-50',
    'text-yellow-700',
    'text-yellow-800',
    'text-yellow-900',
    'border-yellow-400',
  ],
  theme: {
    extend: {
      colors: {
        'court-available': '#10b981',  // green-500
        'court-reserved': '#ef4444',   // red-500
        'court-blocked': '#6b7280',    // gray-500
      },
    },
  },
  plugins: [],
}
