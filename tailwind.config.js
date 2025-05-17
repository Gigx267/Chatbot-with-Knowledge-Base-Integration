/** @type {import('tailwindcss').Config} */

const plugin = require("tailwindcss/plugin");

module.exports = {
  content: ["*"],
  theme: {
    extend: {
      fontFamily: {
        'heading': ['Merriweather', 'serif'],
        'sans': ['Jaldi', 'sans-serif']
      },
      colors: {
        primary: '#E54646',
        bodyColor: '#222222',
      }
    },
  },

  plugins: [
    plugin(({ addBase, theme }) => {
      addBase({
        html : { color: theme("colors.bodyColor") },
      });
    }),
    require('@tailwindcss/forms'),
  ],
}

