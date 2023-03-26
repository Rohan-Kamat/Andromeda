/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
 
    // Or if using `src` directory:
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        // https://fonts.google.com/specimen/Chakra+Petch?preview.text=Andromeda&preview.size=72&preview.text_type=custom
        chakra: ['Chakra Petch', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
