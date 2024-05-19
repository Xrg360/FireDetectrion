from flask import Flask, request, send_from_directory
from werkzeug.utils import secure_filename
import os
import subprocess

app = Flask(__name__, static_url_path='/static')


uploads_dir = os.path.join(app.instance_path, 'uploads')


@app.get("/")
async def get_index():
    return send_from_directory('', 'index.html')


@app.route("/detect", methods=['POST'])
def detect():
    if not request.method == "POST":
        return

    image = request.files['image']
    filename = secure_filename(image.filename)
    os.makedirs(uploads_dir, exist_ok=True)

    image.save(os.path.join(uploads_dir, filename))

    subprocess.run(['python', 'detect.py', '--source', os.path.join(uploads_dir, filename), '--weights', './best.pt'])

    output_dir = './runs/detect/'
    exp_dirs = [d for d in os.listdir(output_dir) if d.startswith('exp')]
    latest_exp_dir = max(exp_dirs, key=lambda d: os.path.getmtime(os.path.join(output_dir, d)))
    output_file = os.listdir(os.path.join(output_dir, latest_exp_dir))[0]

    return send_from_directory(os.path.join(output_dir, latest_exp_dir), output_file)


@app.route("/detectvideo", methods=['POST'])
def detect_video():
    if not request.method == "POST":
        return

    video = request.files['video']
    filename = secure_filename(video.filename)

    # Ensure the uploads directory exists
    os.makedirs(uploads_dir, exist_ok=True)

    video.save(os.path.join(uploads_dir, filename))

    subprocess.run(['python', 'detect.py', '--source', os.path.join(uploads_dir, filename), '--weights', './best.pt'])

    
    output_dir = './runs/detect/'
    exp_dirs = [d for d in os.listdir(output_dir) if d.startswith('exp')]
    latest_exp_dir = max(exp_dirs, key=lambda d: os.path.getmtime(os.path.join(output_dir, d)))

    # Assuming there's only one file in the directory
    output_file = os.listdir(os.path.join(output_dir, latest_exp_dir))[0]

    print(f"Output file: {os.path.join(output_dir, latest_exp_dir, output_file)}")  # Display the path of the output file

    return send_from_directory(os.path.join(output_dir, latest_exp_dir), output_file)



@app.route("/detectwebcam", methods=['POST'])
def detect_webcam():
    if not request.method == "POST":
        return

    subprocess.run(['python', 'detect.py', '--source', '0', '--weights', 'best.pt'])

    # Assuming detect.py saves the output in a directory like /runs/detect/exp*
    output_dir = './runs/detect/'
    exp_dirs = [d for d in os.listdir(output_dir) if d.startswith('exp')]
    latest_exp_dir = max(exp_dirs, key=lambda d: os.path.getmtime(os.path.join(output_dir, d)))

    # Assuming there's only one file in the directory
    output_file = os.listdir(os.path.join(output_dir, latest_exp_dir))[0]

    print(f"Output file: {os.path.join(output_dir, latest_exp_dir, output_file)}")  # Display the path of the output file

    return send_from_directory(os.path.join(output_dir, latest_exp_dir), output_file)