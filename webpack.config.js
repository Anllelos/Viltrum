const path = require('path');

module.exports = {
  // Archivo de entrada (React)
  entry: './frontend/src/index.js',  // Ajusta esta ruta si es necesario

  // Archivo de salida (dónde se va a generar el archivo compilado)
  output: {
    path: path.resolve(__dirname, './static/frontend'),  // Carpeta donde se guardarán los archivos compilados
    filename: 'main.js',  // Nombre del archivo compilado
  },

  // Configuración de módulos y loaders
  module: {
    rules: [
      {
        test: /\.js$/,  // Aplica este loader a archivos .js
        exclude: /node_modules/,  // Excluye la carpeta node_modules
        use: {
          loader: 'babel-loader',  // Usa Babel para transpilar el código
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react'],  // Presets para soportar ES6+ y JSX
          },
        },
      },
    ],
  },

  // Configuración de modo de desarrollo
  mode: 'development',
};
