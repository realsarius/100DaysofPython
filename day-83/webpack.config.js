const path = require('path');

module.exports = {
  entry: './src/js/index.js', // Main entry point for JS
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'static/dist'),
    publicPath: '/static/dist/'
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env']
          }
        }
      },
      {
        test: /\.css$/, // Target CSS files
        use: [
          'style-loader',
          'css-loader',
          'postcss-loader' // Add postcss-loader to handle Tailwind and Autoprefixer
        ]
      }
    ]
  },
  mode: 'development' // or 'production' for optimized output
};