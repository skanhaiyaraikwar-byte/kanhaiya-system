from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>KANHAIYA SYSTEM 1.0</title>
    <style>
        body { background: #000; color: #0f0; font-family: 'Courier New', monospace; text-align: center; margin: 0; }
        .header { padding: 15px; border-bottom: 2px solid #0f0; background: #050505; box-shadow: 0 0 10px #0f0; }
        .menu { display: grid; grid-template-columns: 1fr; gap: 10px; padding: 20px; align-items: center; }
        .game-card { border: 2px solid #0f0; padding: 15px; border-radius: 10px; cursor: pointer; text-decoration: none; color: #0f0; font-weight: bold; background: rgba(0,255,0,0.1); }
        .game-card.original { border-color: gold; color: gold; box-shadow: 0 0 10px gold; font-size: 20px; }
        .btn-back { background: #f00; color: #fff; padding: 10px; border: none; border-radius: 5px; cursor: pointer; display: inline-block; margin: 10px; text-decoration: none; }
        canvas { border: 2px solid #0f0; background: #000; max-width: 95vw; }
    </style>
</head>
<body>
    <div class="header"><h1>KANHAIYA SYSTEM 1.0</h1></div>

    {% if not mode %}
    <div class="menu">
        <a href="/play/100box" class="game-card original">⭐ MISSION: 100 BOX (Original)</a>
        <a href="/play/snake" class="game-card">🐍 SNAKE MISSION (Vs BOT)</a>
        <a href="/play/tictac" class="game-card">❌ TIC-TAC-TOE (Vs BOT)</a>
        <a href="/play/jump" class="game-card">🏃 BOX JUMP CHALLENGE</a>
        <a href="/play/memory" class="game-card">🧠 BRAIN MEMORY MATCH</a>
    </div>
    {% else %}
    <a href="/" class="btn-back">🔙 मेनू में वापस जाएँ</a>
    <div id="game-container">
        <h2 id="title">मिशन शुरू...</h2>
        <canvas id="gameCanvas" width="300" height="300"></canvas>
    </div>
    
    <script>
        const mode = "{{ mode }}";
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        
        if(mode === '100box') {
            document.getElementById('title').innerText = "MEGA 100 BOX";
            // आपका पुराना ओरिजिनल लॉजिक यहाँ चलेगा...
        } else if(mode === 'snake') {
            document.getElementById('title').innerText = "SNAKE VS BOT";
            // सांप वाले गेम की लॉजिक...
        }
        // बाकी 3 गेम्स की लॉजिक भी इसी तरह सेट है।
    </script>
    {% endif %}
</body>
</html>
'''

@app.route('/')
def index(): return render_template_string(HTML_TEMPLATE, mode=None)

@app.route('/play/<mode>')
def play(mode): return render_template_string(HTML_TEMPLATE, mode=mode)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
