from flask import Flask, request, jsonify, send_file
from PIL import Image
from ultralytics import YOLO
import os
import csv
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for communication with React frontend

# Define the folder to store results
results_folder = 'results'
if not os.path.exists(results_folder):
    os.makedirs(results_folder)

# Load YOLO model
model = YOLO('best.pt')

class_labels = {
    0: 'A1', 1: 'A2', 2: 'A3', 3: 'B4', 4: 'B5', 5: 'C10', 6: 'C11', 7: 'C12', 8: 'C6',
    9: 'C7', 10: 'C8', 11: 'C9', 12: 'D13', 13: 'D14', 14: 'D15', 15: 'E16', 16: 'E17',
    17: 'E18', 18: 'F19', 19: 'F20', 20: 'G21', 21: 'G22', 22: 'X', 23: 'Y'
}

chromosome_pairs = {
    'A1': '1st pair chromosome', 'A2': '2nd pair chromosome', 'A3': '3rd pair chromosome',
    'B4': '4th pair chromosome', 'B5': '5th pair chromosome', 'C6': '6th pair chromosome',
    'C7': '7th pair chromosome', 'C8': '8th pair chromosome', 'C9': '9th pair chromosome',
    'C10': '10th pair chromosome', 'C11': '11th pair chromosome', 'C12': '12th pair chromosome',
    'D13': '13th pair chromosome', 'D14': '14th pair chromosome', 'D15': '15th pair chromosome',
    'E16': '16th pair chromosome', 'E17': '17th pair chromosome', 'E18': '18th pair chromosome',
    'F19': '19th pair chromosome', 'F20': '20th pair chromosome', 'G21': '21st pair chromosome',
    'G22': '22nd pair chromosome', 'X': 'X chromosome', 'Y': 'Y chromosome'
}

chromosome_disorders = {
    'Down Syndrome': ['21st pair chromosome'],
    'Klinefelter Syndrome': ['X'],
    'Edwards Syndrome': ['18th pair chromosome'],
    'Patau Syndrome': ['13th pair chromosome'],
    'Cri-du-chat Syndrome': ['5th pair chromosome'],
    'Jacobs Syndrome': ['Y'],
    'Trisomy 9': ['9th pair chromosome'],
    'Trisomy 8': ['8th pair chromosome'],
    'Trisomy 16': ['16th pair chromosome'],
    'Angelman Syndrome': ['15th pair chromosome'],
    'DiGeorge Syndrome': ['22nd pair chromosome'],
}

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        image = Image.open(file)
        results = model(image)

        result_image_path = os.path.join(results_folder, 'result.jpg')
        bar_chart_path = os.path.join(results_folder, 'bar_chart.png')

        for r in results:
            r.save(filename=result_image_path)
            r.save_txt(os.path.join(results_folder, 'ex'), save_conf=True)

        results_from_txt = []
        with open(os.path.join(results_folder, 'ex'), 'r') as file:
            lines = file.readlines()
            for line in lines:
                data = line.split()
                results_from_txt.append(list(map(float, data)))

        output_csv = os.path.join(results_folder, 'results.csv')
        class_counts = {label: 0 for label in class_labels.values()}
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Category', 'X1', 'Y1', 'X2', 'Y2', 'Confidence', 'Count'])
            for r in results_from_txt:
                category = class_labels[int(r[0])]
                x1, y1, x2, y2 = r[1:5]
                confidence = round(r[5] * 100, 2)
                class_counts[category] += 1
                writer.writerow([category, x1, y1, x2, y2, confidence, class_counts[category]])

        categories = [class_labels[int(r[0])] for r in results_from_txt]
        category_counts = Counter(categories)
        with open(os.path.join(results_folder, 'category_counts.csv'), 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Category', 'Chromosome Pair', 'Count'])
            for category, chromosome_pair in chromosome_pairs.items():
                count = category_counts.get(category, 0)
                writer.writerow([category, chromosome_pair, count])

        chromosomal_disorder_output = []
        for disorder, categories in chromosome_disorders.items():
            disorder_count = sum(category_counts.get(cat, 0) for cat in categories)
            if disorder_count > 2:
                chromosomal_disorder_output.append(disorder)

        sns.set_style("whitegrid")
        plt.figure(figsize=(10, 6))
        sns.barplot(x=list(category_counts.keys()), y=list(category_counts.values()), palette='viridis')
        plt.xlabel('Category')
        plt.ylabel('Count')
        plt.title('Count of Each Category')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(bar_chart_path)

        print(f"Disorders detected: {chromosomal_disorder_output}")

        return jsonify({
            "result_image": "result.jpg",
            "bar_chart": "bar_chart.png",
            "disorders": chromosomal_disorder_output
        })

@app.route('/results/<filename>', methods=['GET'])
def get_result_file(filename):
    return send_file(os.path.join(results_folder, filename))

if __name__ == '__main__':
    app.run(debug=False)
