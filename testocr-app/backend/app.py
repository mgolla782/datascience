from flask import Flask,request,jsonify
import easyocr
from pdf2image import convert_from_bytes,convert_from_path
import io
from flask_cors import CORS
from PIL import Image
import numpy as np

app = Flask(__name__)
CORS(app)
reader = easyocr.Reader(['en'])

@app.route('/upload',methods=['POST'])
def upload_pdf():

    file = request.files['file']
    print("file object",file)
    
    #images = convert_from_bytes(pdf_bytes)
    result_text = ""
    result = reader.readtext(file)
    result_text += "\n".join(result) + "\n"

#    for image in images:
#        result = reader.readtext(image, detail=0)
#        result_text += "\n".join(result) + "\n"

    return jsonify({'text': result_text})

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']

    #poppler_path = r'D:/poppler/poppler-24.08.0/Library/bin'  # Change this to your actual path
    pdf_bytes = file.read()

    # Convert PDF pages to images (list of PIL Images)
    images = convert_from_bytes(pdf_bytes)

    # Save each page as a separate image
    for i, image in enumerate(images):
        image.save(f'page_{i+1}.png', 'PNG')


    image = Image.open(file.stream).convert('RGB')
    image_np = np.array(image)

    results = reader.readtext(image_np)
    extracted_text = [text for _, text, _ in results]

    return jsonify({'text': extracted_text})

@app.route('/newocr', methods=['POST'])
def newocr():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    filename = file.filename.lower()
    #poppler_path = r'D:/poppler/poppler-24.08.0/Library/bin'  # Change this to your actual path

    texts = []

    try:
        if filename.endswith('.pdf'):
            images = convert_from_bytes(file.read())
            for img in images:
                img_np = np.array(img)
                result = reader.readtext(img_np)
                #texts.extend([text for _, text, _ in result])
                texts.extend([{'bbox': clean_bbox(bbox), 'text': str(text),'prob': prob} for bbox, text, prob in result])
        else:
            image = Image.open(file.stream).convert('RGB')
            img_np = np.array(image)
            result = reader.readtext(img_np)
            #texts = [text for _, text, _ in result]
            texts.extend([{'bbox': clean_bbox(bbox), 'text': str(text), 'prob': prob} for bbox, text, prob in result])

        return jsonify({'results': texts})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def clean_bbox(bbox):
    return [[float(x), float(y)] for x, y in bbox]

if __name__ == '__main__':
    app.run(debug=True)

