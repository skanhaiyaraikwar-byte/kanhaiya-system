from flask import Flask, render_template_string, request
import os

app = Flask(__name__)

# आपका पूरा गेम वाला HTML (100 Box और 90 Degree रूल के साथ)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>S KANHAIYA SYSTEM</title>
    <style>
        body { background: #000; color: #0f0; text-align: center; font-family: 'Courier New', monospace; }
        canvas { border: 2px solid #0f0; max-width: 95vw; background: rgba(0,10,0,0.95); box-shadow: 0 0 20px #0f0; }
    </style>
</head>
<body>
    <h1>S KANHAIYA SYSTEM</h1>
    <canvas id="gameCanvas" width="440" height="440"></canvas>
    <p>90° कोण का नियम लागू है</p>
    <script>
        // यहाँ आपका पुराना सारा गेम लॉजिक आएगा
        console.log("Kanhaiya System Online");
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
