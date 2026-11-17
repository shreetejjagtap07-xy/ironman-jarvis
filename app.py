
import os
from flask import Flask, request, jsonify, render_template
from groq import Groq

app = Flask(__name__)

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        message = request.json.get("message", "")

        result = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are JARVIS, a futuristic personal AI assistant. "
                        "Reply naturally in Marathi, Hindi or English. "
                        "Never claim an action was performed unless verified."
                    )
                },
                {"role": "user", "content": message}
            ]
        )

        return jsonify({
            "reply": result.choices[0].message.content
        })

    except Exception:
        return jsonify({
            "reply": "JARVIS AI connection unavailable."
        }), 500

if __name__ == "__main__":
    app.run()

