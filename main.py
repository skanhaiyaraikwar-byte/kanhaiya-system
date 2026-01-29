from flask import Flask, render_template_string

app = Flask(__name__)

# --- मास्टर कोड: सब कुछ एक ही जगह ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>S.KANHAIYA SYSTEM</title>
    <style>
        body { background: #000; color: #0f0; font-family: 'Courier New', monospace; text-align: center; margin: 0; }
        .header { padding: 15px; border-bottom: 2px solid #0f0; background: #111; }
        .menu { display: flex; flex-direction: column; gap: 15px; padding: 20px; align-items: center; }
        .game-btn { border: 2px solid #0f0; padding: 15px; width: 85%; border-radius: 10px; cursor: pointer; text-decoration: none; color: #0f0; font-weight: bold; background: rgba(0,255,0,0.1); font-size: 18px; }
        .btn-back { background: #f00; color: #fff; padding: 10px; border-radius: 5px; text-decoration: none; display: inline-block; margin: 10px; }
        canvas { border: 2px solid #0f0; background: #000; max-width: 95vw; margin-top: 10px; touch-action: none; }
    </style>
</head>
<body>
    <div class="header"><h1>S.KANHAIYA SYSTEM</h1></div>
    {% if not mode %}
    <div class="menu">
        <a href="/play/100box" class="game-btn" style="border-color:gold; color:gold;">⭐ MISSION: 100 BOX (Original)</a>
        <a href="/play/snake" class="game-btn">🐍 SNAKE MISSION</a>
        <a href="/play/tictac" class="game-btn">❌ TIC-TAC-TOE</a>
    </div>
    {% else %}
    <a href="/" class="btn-back">🔙 मेनू में वापस जाएँ</a>
    <h2 id="gTitle">लोड हो रहा है...</h2>
    <canvas id="gameCanvas" width="400" height="400"></canvas>
    <div id="status" style="margin-top:10px;"></div>

    <script>
        const mode = "{{ mode }}";
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const status = document.getElementById('status');

        if(mode === '100box') {
            document.getElementById('gTitle').innerText = "100 BOX ORIGINAL";
            // --- आपका पुराना 100 BOX लॉजिक यहाँ शुरू होता है ---
            let boxes = [];
            for(let i=0; i<100; i++) boxes.push({x: (i%10)*40, y: Math.floor(i/10)*40, color: '#222'});
            function draw() {
                ctx.clearRect(0,0,400,400);
                boxes.forEach(b => {
                    ctx.fillStyle = b.color;
                    ctx.fillRect(b.x+1, b.y+1, 38, 38);
                });
            }
            canvas.onclick = (e) => {
                const rect = canvas.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const i = Math.floor(x/40) + Math.floor(y/40)*10;
                if(boxes[i]) boxes[i].color = '#0f0';
                draw();
            };
            draw();
            status.innerText = "स्क्रीन पर टच करके बॉक्स भरें!";
        } else if(mode === 'snake') {
            document.getElementById('gTitle').innerText = "SNAKE GAME";
            // सांप वाला गेम लॉजिक...
            let snake = [{x:10, y:10}], food = {x:5, y:5}, dir = 'R';
            function game() {
                ctx.fillStyle="black"; ctx.fillRect(0,0,400,400);
                ctx.fillStyle="red"; ctx.fillRect(food.x*20, food.y*20, 18, 18);
                ctx.fillStyle="#0f0"; snake.forEach(s => ctx.fillRect(s.x*20, s.y*20, 18, 18));
                let head = {x: snake[0].x + (dir=='R'?1:dir=='L'?-1:0), y: snake[0].y + (dir=='D'?1:dir=='U'?-1:0)};
                snake.unshift(head);
                if(head.x==food.x && head.y==food.y) food={x:Math.floor(Math.random()*20), y:Math.floor(Math.random()*20)};
                else snake.pop();
                if(head.x<0 || head.x>=20 || head.y<0 || head.y>=20) { snake=[{x:10,y:10}]; }
            }
            setInterval(game, 150);
            window.onclick = () => { dir = dir=='R'?'D':dir=='D'?'L':dir=='L'?'U':'R'; };
        }
    </script>
    {% endif %}
</body>
</html>
'''

@app.route('/')
def index(): return render_template_string(HTML_TEMPLATE, mode=None)

@app.route('/play/<mode>')
def play(mode): return render_template_string(HTML_TEMPLATE, mode=mode)
