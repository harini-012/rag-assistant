import os
import json
from flask import Flask, request, jsonify, render_template
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def load_notes():
    with open("notes.json", "r", encoding="utf-8") as file:
        return json.load(file)

def retrieve_notes(question):

    notes = load_notes()

    question = question.lower()

    matched = []

    for note in notes:

        topic = note["topic"].lower()

        if topic in question:

            matched.append(note["content"])

    

    return "\n".join(matched)


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    question = data.get("question", "")

    retrieved_text = retrieve_notes(question)

    prompt =f"""
You are an AI Learning Assistant.

If relevant notes are provided, answer using them.

If no relevant notes are available, answer using your own knowledge.



Question:
{question}

Keep the answer simple and easy to understand.
"""

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role": "system",
                "content": "You are a helpful AI teacher."
            },

            {
                "role": "user",
                "content": prompt
            }

        ]

    )

    answer = response.choices[0].message.content

    return jsonify({

        "question": question,

        

        "answer": answer

    })


if __name__ == "__main__":

    app.run(debug=True)