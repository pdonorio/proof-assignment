module.exports = {
  use: [
    ['@neutrinojs/airbnb', {
      include: [ './src', './test'],
      eslint: {
        rules: {
          "jsx-a11y/anchor-is-valid": [ "error", {
            "components": [ "Link" ],
            "specialLink": [ "to", "hrefLeft", "hrefRight" ],
            "aspects": [ "noHref", "invalidHref", "preferButton" ]
          }],
          "jsx-a11y/label-has-for": [
            "error", {
              "components": [ "label"  ],
              "required": {
                "every": [ "id" ]
              }
            }
          ],
          'import/extensions': [
            "error", "ignorePackages"
          ],
          'react/forbid-prop-types': 'off',
          'react/jsx-boolean-value': 'off',
          'react/no-array-index-key': 'off'
        },
      }
    }
    ],
    [
      '@neutrinojs/react',
      {
        html: {
          title: 'Proof - The game',
          links: [
            {
              href: 'https://fonts.googleapis.com/icon?family=Material+Icons',
              rel: 'stylesheet'
            },
          ]
        },
        style: {
          test: /\.(css|sass|scss)$/,
          modulesTest: /\.module\.(css|sass|scss)$/,
          loaders: [
            {
              loader: 'sass-loader',
              useId: 'sass'
            }
          ]
        },
        env: [
          'API_URL',
        ],
      }
    ],
    ['@neutrinojs/jest', {
      setupFiles: [
        '<rootDir>/test/setup.js',
      ],
      snapshotSerializers: ['enzyme-to-json/serializer']
    }],
    neutrino => neutrino.config.output.publicPath('/')
  ]
};
