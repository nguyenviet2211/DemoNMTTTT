from flask import Flask, render_template, request, jsonify
from model import NaiveBayes

app = Flask(__name__)

# Load the trained model
try:
    model = NaiveBayes.load_model('spam_classifier.pkl')
except FileNotFoundError:
    print("Không tìm thấy file mô hình. Vui lòng chạy train.py trước!")
    exit(1)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    message = request.json.get('message', '')
    if not message:
        return jsonify({'error': 'Vui lòng nhập tin nhắn'}), 400
    
    ham, spam = model.classify(message)
    return jsonify({
        'result': 'HAM' if ham > spam else 'SPAM',
        'message': message,
        'accuracy': max(ham, spam),
        'a': min(ham, spam)
    })

if __name__ == '__main__':
    app.run(debug=True) 