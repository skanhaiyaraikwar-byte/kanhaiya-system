from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>S.KANHAIYA SYSTEM</title>
    <style>
        body { background: #000; color: #0f0; font-family: 'Courier New', monospace; text-align: center; margin: 0; overflow: hidden; }
        .header { padding: 10px; border-bottom: 2px solid #0f0; background: #111; }
        .menu { display: flex; flex-direction: column; gap: 10px; padding: 20px; align-items: center; }
        .game-btn { border: 2px solid #0f0; padding: 12px; width: 85%; border-radius: 8px; text-decoration: none; color: #0f0; font-weight: bold; background: rgba(0,255,0,0.1); }
        .btn-back { background: #f00; color: #fff; padding: 8px; border-radius: 5px; text-decoration: none; display: inline-block; margin: 5px; font-size: 12px; }
        canvas { border: 2px solid #0f0; background: #050505; max-width: 90vw; margin-top: 5px; touch-action: none; }
    </style>
</head>
<body>
    <div class="header"><h3>S.KANHAIYA SYSTEM</h3></div>
    {% if not mode %}
    <div class="menu">
        <a href="/play/100box" class="game-btn" style="color:gold; border-color:gold;">⭐ 100 BOX (ORIGINAL)</a>
        <a href="/play/snake" class="game-btn">🐍 SNAKE MISSION</a>
        <a href="/play/jump" class="game-btn">🏃 JUMP CHALLENGE</a>
    </div>
    {% else %}
    <a href="/" class="btn-back">🔙 मेनू में वापस जाएँ</a>
    <h4 id="gTitle">लोड हो रहा है...</h4>
    <canvas id="gameCanvas" width="360" height="360"></canvas>
    <p id="hint" style="font-size:12px; color:#aaa;">स्क्रीन पर टच करें!</p>

    <script>
        const mode = "{{ mode }}";
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        document.getElementById('gTitle').innerText = mode.toUpperCase();

        if(mode === '100box') {
            let grid = Array(100).fill('#222');
            function draw() {
                ctx.clearRect(0,0,360,360);
                grid.forEach((c, i) => {
                    ctx.fillStyle = c;
                    ctx.fillRect((i%10)*36 + 1, Math.floor(i/10)*36 + 1, 34, 34);
                });
            }
            canvas.ontouchstart = (e) => {
                const r = canvas.getBoundingClientRect();
                const x = e.touches[0].clientX - r.left;
                const y = e.touches[0].clientY - r.top;
                const i = Math.floor(x/36) + Math.floor(y/36)*10;
                if(grid[i]) grid[i] = '#0f0';
                draw();
            };
            draw();
        } else if(mode === 'snake') {
            let s = [{x:10,y:10}], f = {x:5,y:5}, d = 'R';
            setInterval(() => {
                ctx.fillStyle="#000"; ctx.fillRect(0,0,360,360);
                ctx.fillStyle="red"; ctx.fillRect(f.x*18, f.y*18, 16, 16);
                ctx.fillStyle="#0f0"; s.forEach(p => ctx.fillRect(p.x*18, p.y*18, 16, 16));
                let h = {x: s[0].x+(d=='R'?1:d=='L'?-1:0), y: s[0].y+(d=='D'?1:d=='U'?-1:0)};
                s.unshift(h); if(h.x==f.x && h.y==f.y) f={x:Math.floor(Math.random()*20), y:Math.floor(Math.random()*20)}; else s.pop();
                if(h.x<0||h.x>=20||h.y<0||h.y>=20) s=[{x:10,y:10}];
            }, 150);
            canvas.ontouchstart = () => { d = d=='R'?'D':d=='D'?'L':d=='L'?'U':'R'; };
        } else if(mode === 'jump') {
            let py=300, v=0, ox=360, score=0;
            setInterval(() => {
                ctx.fillStyle="#000"; ctx.fillRect(0,0,360,360);
                ctx.fillStyle="#0f0"; ctx.fillRect(50, py, 30, 30); // Player
                ctx.fillStyle="#f00"; ctx.fillRect(ox, 310, 20, 20); // Obstacle
                py += v; v += 1.5; if(py > 300) { py=300; v=0; }
                ox -= 5; if(ox < -20) { ox=360; score++; }
                if(ox < 80 && ox > 30 && py > 280) { score=0; ox=360; } // Collision
                ctx.fillStyle="white"; ctx.fillText("Score: "+score, 10, 20);
            }, 30);
            canvas.ontouchstart = () => { if(py==300) v=-15; };
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)











#
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
