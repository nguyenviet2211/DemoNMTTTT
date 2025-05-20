from flask import Flask, render_template, request, jsonify
from model import NaiveBayes
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
import io

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

@app.route('/classify_csv', methods=['POST'])
def classify_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'Không tìm thấy file'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Không có file được chọn'}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'File phải có định dạng CSV'}), 400

    try:
        # Đọc file CSV
        content = file.read().decode('utf-8')
        test_data = pd.read_csv(io.StringIO(content), encoding='utf-8', on_bad_lines='skip')
        
        # Làm sạch dữ liệu
        test_data = test_data.dropna()
        test_data.columns = ['Label', 'SMS']
        test_data['Label'] = test_data['Label'].str.lower()
        
        # Phân loại và thu thập kết quả
        y_true = []
        y_pred = []
        
        for index, row in test_data.iterrows():
            message = row['SMS']
            expected = row['Label']
            ham, spam = model.classify(message)
            predicted = "ham" if ham > spam else "spam"
            
            # if expected != predicted:
            #     print(f"Tin nhắn: {message} - Dự đoán: {predicted} - Thực tế: {expected}")

            y_true.append(expected)
            y_pred.append(predicted)
        
        # Tính toán các chỉ số đánh giá
        precision = precision_score(y_true, y_pred, pos_label='spam')
        recall = recall_score(y_true, y_pred, pos_label='spam')
        f1 = f1_score(y_true, y_pred, pos_label='spam')
        conf_matrix = confusion_matrix(y_true, y_pred, labels=['spam', 'ham'])
        
        return jsonify({
            'precision': float(precision),
            'recall': float(recall),
            'f1': float(f1),
            'confusion_matrix': conf_matrix.tolist()
        })
        
    except Exception as e:
        return jsonify({'error': f'Lỗi xử lý file: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(debug=True) 