from flask import Flask, request, render_template, send_from_directory, url_for
from PIL import Image
import os
import sys
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'pmb_files'

# Create necessary folders if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

def convert_to_pmb(image_path, output_path=None):
    """Convert image to PMB format"""
    try:
        img = Image.open(image_path)
        pixelvalues = list(img.getdata())
        width, height = img.size
        x = 0

        name = os.path.splitext(os.path.basename(image_path))[0]
        
        if output_path is None:
            output_file = os.path.join(app.config['OUTPUT_FOLDER'], f"{name}.pmb")
        else:
            output_file = output_path
            
        with open(output_file, "w") as f:
            f.write(f"{name}\n")
            f.write(f"{width},{height}\n")
            for pixel in pixelvalues:
                if x != width:
                    f.write(str(pixel) + "\n")
                    x += 1
                if x == width:
                    f.write(str(pixel) + "N" + "\n")
                    x = 0
        
        return output_file
    except Exception as e:
        print(f"Error converting image: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('index.html', error='No file part')
    
    file = request.files['file']
    
    if file.filename == '':
        return render_template('index.html', error='No selected file')
    
    if file and file.filename:
        # Generate a unique filename to prevent conflicts
        original_filename = file.filename
        name, ext = os.path.splitext(original_filename)
        unique_filename = f"{name}_{uuid.uuid4().hex[:8]}{ext}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save the uploaded file
        file.save(file_path)
        
        # Convert to PMB
        pmb_file = convert_to_pmb(file_path)
        
        if pmb_file:
            download_url = url_for('download_file', filename=os.path.basename(pmb_file))
            return render_template('index.html', success=True, filename=os.path.basename(pmb_file), download_url=download_url)
        else:
            return render_template('index.html', error='Error converting file')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 