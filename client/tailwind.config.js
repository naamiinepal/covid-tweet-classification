module.exports = {
  purge: ['./src/**/*.{js,jsx,ts,tsx}', './public/index.html'],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        primary:"#2196F3"
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
