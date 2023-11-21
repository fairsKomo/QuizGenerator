from website import create_app
import os
app = create_app()
app.secret_key = "ff11223344"
if __name__ == "__main__":
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host="0.0.0.0", port=port)
    app.run(debug=True)