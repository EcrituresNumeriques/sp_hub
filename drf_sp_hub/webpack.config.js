var path = require('path')
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')

module.exports = {
    // absolute path
    context: __dirname,
    // our entry point - suffix added (see later)
    entry: './assets/js/index',
    output: {
        path: path.resolve('./assets/bundles/'),
        filename: '[name]-[hash].js',
    },
    
    plugins: [
        new BundleTracker({filename: './webpack-stats.json'}),
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            'window.jQuery': 'jquery',
        }),
    ],
    
    module: {
        loaders: [
            {   test: /\.jsx?$/,
                // don't transpile files in node_modules (too long)
                exclude: /node_modules/,
                loader: 'babel-loader',
                query: {
                  presets: ['react'],
                }
            }
        ]
    },
    
    resolve: {
        // where to look for moduels
        modules: ['node_modules'],
        extensions: ['.js', '.jsx']
    }
}