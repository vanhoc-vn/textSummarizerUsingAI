from flask import Flask, request, jsonify
from flask_cors import CORS  
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

app = Flask(__name__)
CORS(app)  # Thêm CORS

# (Phần còn lại của code server.py giữ nguyên)
tokenizer = AutoTokenizer.from_pretrained("./vit5_vietnamese_summarization_final")
model = AutoModelForSeq2SeqLM.from_pretrained("./vit5_vietnamese_summarization_final")
summarizer = pipeline(
    "summarization",
    model=model,
    tokenizer=tokenizer,
    framework="pt"
)

def summarize_text(text):
    try:
        if len(text) > 2000:
            raise ValueError("Text too long. Please shorten it.")
        tokens = tokenizer.encode(text, max_length=762, truncation=True)
        text = tokenizer.decode(tokens, skip_special_tokens=True)
        summary = summarizer(text, max_length=150, min_length=10, do_sample=False)
        return summary[0]["summary_text"]
    except Exception as e:
        raise Exception(f"Error summarizing: {e}")

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.get_json()
        text = data.get("text", "")
        print("Received text:", text)
        if not text:
            print("Error: No text provided")
            return jsonify({"error": "No text provided"}), 400
        summary = summarize_text(text)
        print("Summary:", summary)
        return jsonify({"summary": summary})
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, threaded=True)