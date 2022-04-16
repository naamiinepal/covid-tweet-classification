module.exports = {
  purge: ['./src/**/*.{js,jsx,ts,tsx}', './public/index.html'],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      backgroundImage: {
        'hero-pattern': "url('svgs/Frontline.svg')",
      },
      colors: {
        primary:"#247881",
        // filterBackground:"#247990"
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
