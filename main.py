‎import os
from flask import Flask, render_template_string, send_from_directory

app = Flask(__name__)

# --- कॉन्फ़िगरेशन ---
SITE_TITLE = "K.R file download"
PASSCODE = "1234" 
SECRET_DIR = "my_private_files"

# फोल्डर बनाना अगर नहीं है
if not os.path.exists(SECRET_DIR):
    os.makedirs(SECRET_DIR)

@app.route('/')
def index():
    # फाइलों की लिस्ट बनाना (जो my_private_files फोल्डर में होंगी)
    files = [f for f in os.listdir(SECRET_DIR) if os.path.isfile(os.path.join(SECRET_DIR, f))]
    file_list_html = "".join([f'<li><a href="/download/{f}" download>{f}</a></li>' for f in files])

    html_content = f"""<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{SITE_TITLE}</title>
    <style>
        body {{ background: #0f172a; color: white; font-family: sans-serif; text-align: center; padding: 20px; }}
        .box {{ background: #1e293b; padding: 30px; border-radius: 15px; border: 1px solid #38bdf8; display: inline-block; min-width: 300px; box-shadow: 0 0 20px rgba(56, 189, 248, 0.2); }}
        input {{ padding: 12px; border-radius: 8px; border: none; width: 85%; margin-bottom: 15px; background: #334155; color: white; outline: none; }}
        .btn {{ background: #38bdf8; color: black; padding: 12px 25px; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; width: 100%; transition: 0.3s; }}
        .btn:hover {{ background: #0ea5e9; }}
        ul {{ padding: 0; }}
        li {{ background: #334155; margin: 8px 0; padding: 12px; border-radius: 8px; border-left: 4px solid #38bdf8; text-align: left; list-style:none; }}
        li a {{ color: #38bdf8; text-decoration: none; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="box" id="login-box">
        <h1 style="color:#38bdf8;">{SITE_TITLE}</h1>
        <p>सिक्योरिटी कोड डालें:</p>
        <input type="password" id="code" placeholder="Enter Code">
        <button class="btn" onclick="unlock()">अनलॉक करें</button>
    </div>
    <div class="box" id="secret-area" style="display:none;">
        <h2 style="color:#00ff88;">🔓 एक्सेस मिल गया!</h2>
        <ul>{file_list_html if file_list_html else "<li>कोई फाइल नहीं मिली</li>"}</ul>
    </div>
    <script>
        function unlock() {{
            if(document.getElementById("code").value === "{PASSCODE}") {{
                document.getElementById("login-box").style.display = "none";
                document.getElementById("secret-area").style.display = "block";
            }} else {{ alert("गलत कोड!"); }}
        }}
    </script>
</body>
</html>"""
    return render_template_string(html_content)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(SECRET_DIR, filename)

if __name__ == "__main__":
    # Render के लिए पोर्ट सेट करना
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
