# python -m venv venv
# venv\Scripts\activate
# pip freeze > requirements.txt
#pip install -r requirements.txt


from flask import Flask, render_template, request
import easyocr
from langdetect import detect
from googletrans import Translator
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

reader = easyocr.Reader(['en', 'hi'])  # You can add more languages
translator = Translator()

@app.route("/", methods=["GET", "POST"])
def index():
    hindi_text = ""
    extracted_text = ""
    if request.method == "POST":
        file = request.files["image"]
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # OCR Extraction
            result = reader.readtext(filepath, detail=0)
            extracted_text = " ".join(result)

            # Language Detection
            try:
                lang = detect(extracted_text)
            except:
                lang = "unknown"

            # Translation
            if lang != "hi":
                try:
                    translated = translator.translate(extracted_text, src=lang, dest='hi')
                    hindi_text = translated.text
                except Exception as e:
                    hindi_text = f"Translation Error: {e}"
            else:
                hindi_text = extracted_text

            return render_template("index.html", original_text=extracted_text, hindi_text=hindi_text, image_path=filepath)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

