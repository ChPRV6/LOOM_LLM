from flask import Flask, render_template, request, jsonify,send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# Allow serving uploaded images
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Mock function to simulate extracting testing instructions from an image
def extract_feature_from_image(image_path):
    # This is where the multimodal model would process the image.
    # For now, let's simulate it with predefined outputs.
    features = {
        "Source, Destination, and Date Selection": "Verify that the user can successfully select source, destination, and date.",
        "Bus Selection": "Ensure that available buses are displayed based on the selected route and date.",
        "Seat Selection": "Check that the user can pick a seat from available options and it is marked as selected.",
        "Pick-up and Drop-off Point Selection": "Verify that pick-up and drop-off points are displayed and selectable.",
        "Offers": "Ensure that any applicable offers or discounts are highlighted.",
        "Filters": "Check that filters (time, price, bus type) are working as expected.",
        "Bus Information": "Ensure that details about the bus (amenities, user reviews) are displayed."
    }
    
    # Randomly select a feature for demonstration purposes
    import random
    selected_feature = random.choice(list(features.keys()))
    
    return {
        "feature": selected_feature,
        "testing_instructions": features[selected_feature]
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"})

    files = request.files.getlist('file')

    if not files:
        return jsonify({"error": "No file selected for uploading"})

    analysis_results = []

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Simulate extracting features from the image
            feature_info = extract_feature_from_image(file_path)

            analysis_results.append({
                "filename": filename,
                "feature": feature_info["feature"],
                "testing_instructions": feature_info["testing_instructions"]
            })

    return jsonify({"status": "success", "analysis_results": analysis_results})

if __name__ == '__main__':
    app.run(debug=True)
