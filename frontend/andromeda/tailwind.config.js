/** @type {import('tailwindcss').Config} */

module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        poppins: ['Poppins', 'sans-serif'],
        chakra: ['Chakra Petch', 'sans-serif']
      },
      colors: {
        'deep-blue': '#0c0032',
        'royal-purple': '#4b0082',
        'purple': '#6a5acd',
        'pink': '#ff69b4',
      }
    },
  },
  plugins: [],
}
