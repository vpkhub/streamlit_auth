from flask import Flask, render_template, request, Response
import openai
import json
import time

app = Flask(__name__)
openai.api_key = 'your-api-key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['message']
    return Response(stream_response(user_message), content_type='text/event-stream')

def stream_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        stream=True
    )
    for chunk in response:
        chunk_message = chunk['choices'][0]['text']
        yield f"data: {chunk_message}\n\n"
        time.sleep(0.1)  # Simulate a delay for more realistic streaming

if __name__ == '__main__':
    app.run(debug=True)
