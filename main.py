from website import create_app

app = create_app()
app.secret_key = "ff11223344"
if __name__ == "__main__":
    app.run(debug=True)