from website import create_app
# Run this Script to start the webserver
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')