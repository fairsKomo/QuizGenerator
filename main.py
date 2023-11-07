from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def upload_pdf():
    if request.method == 'POST':
        pdf_file = request.files['pdfFile']
        if pdf_file and pdf_file.filename.endswith('.pdf'):
            pdf_file.save('uploads/' + pdf_file.filename)
            return 'File uploaded successfully.'
        else:
            return 'Please select a valid PDF file.'
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)