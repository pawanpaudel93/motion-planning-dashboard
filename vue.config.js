const BundleTracker = require("webpack-bundle-tracker");
const webpack = require('webpack');

// Change this to match the path to your files in production (could be S3, CloudFront, etc.)
const DEPLOYMENT_PATH = "/static/dist";

module.exports = {
  publicPath:
    process.env.NODE_ENV === "production"
      ? DEPLOYMENT_PATH
      : "http://localhost:8080/",
  outputDir: "staticfiles/dist",

  devServer: {
    // public: "localhost:8080",

    proxy: "http://localhost:8000", // This will tell the dev server to proxy any unknown requests (requests that did not match a static file) to http://localhost:8000
    headers: {
      "Access-Control-Allow-Origin": "*"
    },
  },
  // uncomment to remove eslint
    chainWebpack: config => {
      config.module.rules.delete('eslint');
  },
  configureWebpack: {
    plugins: [
      new BundleTracker({ path: __dirname, filename: "webpack-stats.json" }),
      new webpack.optimize.LimitChunkCountPlugin({
        maxChunks: 6
      })
    ],
  },
  transpileDependencies: ["vuetify"],
  pwa: {
    name: 'PX4-AUTOPILOT',
    themeColor: '#344675',
    msTileColor: '#344675',
    appleMobileWebAppCapable: 'yes',
    appleMobileWebAppStatusBarStyle: '#344675'
  },
  css: {
    // Enable CSS source maps.
    sourceMap: process.env.NODE_ENV !== 'production'
  }
};
