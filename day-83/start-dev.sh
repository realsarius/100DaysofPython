#!/bin/bash

# Activate the virtual environment
source .venv/bin/activate

# Set environment variable for Flask
export FLASK_APP=main

# Run Flask in debug mode
flask run --debug &

# Run Webpack in watch mode
npx webpack --config webpack.config.js --watch &

# Run Tailwind CSS in watch mode
npx tailwindcss -i ./src/css/styles.css -o ./static/dist/main.css --watch &

# Wait for all background processes to finish
wait

