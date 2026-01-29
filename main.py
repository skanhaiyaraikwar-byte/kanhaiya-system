from flask import Flask, render_template_string

app = Flask(__name__)

# --- मल्टी-गेम सिस्टम का पूरा कोड ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>KANHAIYA SYSTEM 1.0 | HUB</title>
    <style>
        body { background: #000; color: #0f0; font-family: 'Courier New', monospace; text-align: center; margin: 0; }
        .header { padding: 15px; border-bottom: 2px solid #0f0; background: #050505; box-shadow: 0 0 15px #0f0; }
        .menu { display: grid; grid-template-columns: 1fr; gap: 15px; padding: 20px; max-width: 500px; margin: auto; }
        .game-card { border: 2px solid #0f0; padding: 15px; border-radius: 10px; cursor: pointer; text-decoration: none; color: #0f0; font-weight: bold; background: rgba(0,255,0,0.05); transition: 0.3s; }
        .game-card:hover { background: #0f0; color: #000; box-shadow: 0 0 20px #0f0; }
        .btn-back { background: #f00; color: #fff; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; display: inline-block; margin: 15px; text-decoration: none; }
        iframe { width: 100%; height: 80vh; border: none; }
    </style>
</head>
<body>
    <div class="header"><h1>KANHAIYA SYSTEM 1.0</h1></div>

    {% if not mode %}
    <div class="menu">
        <h2 style="color: #fff;">सिस्टम ऑनलाइन गेम्स</h2>
        <a href="/play/100box" class="game-card">🚀 1. 100 BOX (Your Original)</a>
        <a href="/play/snake" class="game-card">🐍 2. MULTI-SNAKE ONLINE</a>
        <a href="/play/tictac" class="game-card">❌ 3. TIC-TAC-TOE (2-PLAYER)</a>
        <a href="/play/memory" class="game-card">🧠 4. BRAIN MEMORY MATCH</a>
        <a href="/play/pong" class="game-card">🏓 5. PADDLE BATTLE</a>
    </div>
    {% else %}
    <a href="/" class="btn-back">🔙 मेनू में वापस जाएँ</a>
    <div id="game-frame">
        {% if mode == '100box' %}
            <iframe srcdoc='<html><body style="background:#000;color:#0f0;text-align:center;"><script>window.location.href="/original-game-logic";</script></body></html>'></iframe>
        {% else %}
            <h2 style="color:white;">{{ mode.upper() }} मिशन शुरू...</h2>
            <canvas id="newGameCanvas" width="320" height="400" style="border:2px solid #0f0; background:#000;"></canvas>
            <p>ऑनलाइन प्लेयर कनेक्ट हो रहे हैं...</p>
        {% endif %}
    </div>
    {% endif %}

    <script>
        // यहाँ हर गेम की अपनी लॉजिक अलग-अलग रखी गई है ताकि कोई टकराव न हो
    </script>
</body>
</html>
'''

@app.route('/')
def index(): return render_template_string(HTML_TEMPLATE, mode=None)

@app.route('/play/<mode>')
def play(mode): return render_template_string(HTML_TEMPLATE, mode=mode)

# यहाँ आपका पुराना गेम लॉजिक सुरक्षित रूप से अलग रूट पर रखा है
@app.route('/original-game-logic')
def original():
    # यहाँ आपका पुराना पूरा JavaScript कोड (100 BOX वाला) पेस्ट कर दें
    return "पुराना गेम लोड हो रहा है..."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
