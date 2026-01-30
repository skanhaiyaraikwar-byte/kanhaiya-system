from flask import Flask, render_template_string, request
‎import time
‎
‎app = Flask(__name__)
‎
‎# --- गेम का HTML, CSS और JAVASCRIPT ---
‎HTML_TEMPLATE = '''
‎<!DOCTYPE html>
‎<html lang="hi">
‎<head>
‎    <meta charset="UTF-8">
‎    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
‎    <title>S KANHAIYA | MEGA 100 BOX</title>
‎    <style>
‎        html, body { 
‎            width: 100%; height: 100%; margin: 0; padding: 0;
‎            background: #000; color: #0f0; font-family: 'Courier New', monospace;
‎            overflow: hidden; touch-action: none;
‎        }
‎        .header { padding: 10px; border-bottom: 2px solid #0f0; text-align: center; background: rgba(0,0,0,0.8); font-size: 16px; font-weight: bold; }
‎        .score-container { display: flex; justify-content: center; gap: 8px; margin: 5px 0; }
‎        .p-info { display: flex; flex-direction: column; align-items: center; opacity: 0.3; transition: 0.3s; }
‎        .active-p { opacity: 1; transform: scale(1.1); filter: drop-shadow(0 0 10px #fff); }
‎        .player-head { width: 32px; height: 32px; border-radius: 50%; border: 2px solid #fff; display: flex; align-items: center; justify-content: center; font-weight: bold; }
‎        canvas { border: 2px solid #0f0; background: rgba(0, 10, 0, 0.95); display: block; margin: auto; max-width: 90vw; max-height: 60vh; box-shadow: 0 0 20px #0f0; }
‎        .status-msg { color: #fff; font-size: 12px; text-align: center; height: 15px; margin: 8px 0; font-weight: bold; }
‎        .btn { background: #0f0; color: #000; border: none; padding: 10px 18px; font-weight: bold; cursor: pointer; border-radius: 5px; text-decoration: none; display: inline-block; margin: 5px; }
‎    </style>
‎</head>
‎<body>
‎    <div class="header">S KANHAIYA | 100 BOX (STRICT ANGLE)</div>
‎
‎    {% if not in_game %}
‎    <div style="text-align:center; margin-top:50px; background:rgba(0,0,0,0.9); padding:25px; border:2px solid #0f0; display:inline-block; position:absolute; left:50%; transform:translateX(-50%); width: 85%;">
‎        <h3>MEGA GAME SETUP</h3>
‎        <p style="color: #0f0; font-size: 11px;">नियम: केवल 90° का कोण (L/T Shape) मान्य है!</p>
‎        <form action="/play" method="GET">
‎            <p>प्लेयर: <select name="humans" style="background:#000; color:#0f0;"><option value="1">1</option><option value="2">2</option></select></p>
‎            <p>बॉट (AI): <select name="bots" style="background:#000; color:#0f0;"><option value="1">1</option><option value="2">2</option></select></p>
‎            <button type="submit" class="btn">START MISSION 🚀</button>
‎        </form>
‎    </div>
‎    {% else %}
‎    <div class="score-container">
‎        <div id="p-box-0" class="p-info"><div class="player-head" style="background:#0f0; color:#000;">1</div><span id="p0-score">0</span></div>
‎        <div id="p-box-1" class="p-info"><div class="player-head" style="background:#f00; color:#fff;">2</div><span id="p1-score">0</span></div>
‎        <div id="p-box-2" class="p-info"><div class="player-head" style="background:#ff0; color:#000;">3</div><span id="p2-score">0</span></div>
‎        <div id="p-box-3" class="p-info"><div class="player-head" style="background:#00f; color:#fff;">4</div><span id="p3-score">0</span></div>
‎    </div>
‎
‎    <canvas id="gameCanvas" width="440" height="440"></canvas>
‎    <div class="status-msg" id="msg"></div>
‎
‎    <div style="text-align:center; margin-top:10px;">
‎        <button class="btn" onclick="location.reload()" style="background:#f44; color:#fff;">रिसेट</button>
‎        <a href="/" class="btn" style="background:#333; color:#fff;">EXIT</a>
‎    </div>
‎
‎    <script>
‎        const canvas = document.getElementById('gameCanvas');
‎        const ctx = canvas.getContext('2d');
‎        const hCount = {{ h_count }}, bCount = {{ b_count }}, totalPlayers = Math.min(4, hCount + bCount);
‎        const GRID=10, DOTS=11, CELL=40, OFF=20;
‎        let lines=[], boxes=[], scores=[0,0,0,0], turn=0, firstMoveMade=false;
‎        const colors=['#00ff00', '#ff0000', '#ffff00', '#0000ff'];
‎
‎        function init() {
‎            for(let r=0; r<DOTS; r++) for(let c=0; c<DOTS; c++) {
‎                if(c<GRID) lines.push({r1:r, c1:c, r2:r, c2:c+1, owner:-1, isVert:false});
‎                if(r<GRID) lines.push({r1:r, c1:c, r2:r+1, c2:c, owner:-1, isVert:true});
‎            }
‎            for(let r=0; r<GRID; r++) for(let c=0; c<GRID; c++) boxes.push({r,c,owner:-1});
‎            draw(); updateUI();
‎        }
‎
‎        function draw() {
‎            ctx.clearRect(0,0,440,440);
‎            boxes.forEach(b => { if(b.owner!==-1) { ctx.fillStyle=colors[b.owner]+"44"; ctx.fillRect(b.c*CELL+OFF, b.r*CELL+OFF, CELL, CELL); } });
‎            lines.forEach(l => {
‎                ctx.beginPath(); ctx.lineWidth=l.owner===-1?1:4.5;
‎                ctx.strokeStyle=l.owner===-1?"#111":colors[l.owner];
‎                ctx.moveTo(l.c1*CELL+OFF, l.r1*CELL+OFF); ctx.lineTo(l.c2*CELL+OFF, l.r2*CELL+OFF); ctx.stroke();
‎            });
‎            for(let r=0; r<DOTS; r++) for(let c=0; c<DOTS; c++) {
‎                ctx.fillStyle = isDotConnected(r,c) ? "#fff" : "#0f0";
‎                ctx.beginPath(); ctx.arc(c*CELL+OFF, r*CELL+OFF, 3.5, 0, 7); ctx.fill();
‎            }
‎        }
‎
‎        function isDotConnected(r, c) { return lines.some(l => l.owner !== -1 && ((l.r1===r && l.c1===c) || (l.r2===r && l.c2===c))); }
‎
‎        function checkStrictAngle(newLine) {
‎            return lines.some(old => {
‎                if (old.owner === -1) return false;
‎                let sharesPoint = (newLine.r1 === old.r1 && newLine.c1 === old.c1) ||
‎                                  (newLine.r1 === old.r2 && newLine.c1 === old.c2) ||
‎                                  (newLine.r2 === old.r1 && newLine.c2 === old.c1) ||
‎                                  (newLine.r2 === old.r2 && newLine.c2 === old.c2);
‎                return sharesPoint && (newLine.isVert !== old.isVert);
‎            });
‎        }
‎
‎        canvas.onclick = (e) => {
‎            if(turn >= hCount) return;
‎            const r=canvas.getBoundingClientRect();
‎            const x=(e.clientX-r.left)*(440/r.width), y=(e.clientY-r.top)*(440/r.height);
‎            let best=null, dist=22;
‎            
‎            lines.forEach(l => {
‎                if(l.owner!==-1) return;
‎                let mx=((l.c1+l.c2)/2)*CELL+OFF, my=((l.r1+l.r2)/2)*CELL+OFF;
‎                let d=Math.hypot(x-mx, y-my);
‎                if(d < dist) {
‎                    if(!firstMoveMade || checkStrictAngle(l)) { best=l; dist=d; }
‎                }
‎            });
‎
‎            if(best) { applyMove(best); document.getElementById('msg').innerText = ""; }
‎            else if(firstMoveMade) document.getElementById('msg').innerText = "गलत चाल! 90° का कोण बनाएँ।";
‎        };
‎
‎        function applyMove(l) {
‎            l.owner=turn; firstMoveMade=true;
‎            let scored=false;
‎            boxes.forEach(b => { if(b.owner===-1 && isBoxClosed(b)) { b.owner=turn; scores[turn]++; scored=true; } });
‎            draw();
‎            if(!scored) turn=(turn+1)%totalPlayers;
‎            updateUI();
‎            if(turn >= hCount) setTimeout(botMove, 500);
‎        }
‎
‎        function isBoxClosed(b) {
‎            return lines.filter(ln => ln.owner!==-1 && (
‎                (ln.r1==b.r && ln.c1==b.c && ln.r2==b.r && ln.c2==b.c+1) ||
‎                (ln.r1==b.r+1 && ln.c1==b.c && ln.r2==b.r+1 && ln.c2==b.c+1) ||
‎                (ln.r1==b.r && ln.c1==b.c && ln.r2==b.r+1 && ln.c2==b.c) ||
‎                (ln.r1==b.r && ln.c1==b.c+1 && ln.r2==b.r+1 && ln.c2==b.c+1)
‎            )).length === 4;
‎        }
‎
‎        function botMove() {
‎            let avail = lines.filter(l => l.owner===-1 && (!firstMoveMade || checkStrictAngle(l)));
‎            if(avail.length === 0) return;
‎            for(let l of avail) { l.owner=turn; if(boxes.some(b=>b.owner===-1 && isBoxClosed(b))) { l.owner=-1; applyMove(l); return; } l.owner=-1; }
‎            applyMove(avail[Math.floor(Math.random()*avail.length)]);
‎        }
‎
‎        function updateUI() {
‎            for(let i=0; i<4; i++){
‎                const box = document.getElementById(`p-box-${i}`);
‎                if(i < totalPlayers) {
‎                    box.style.display="flex"; document.getElementById(`p${i}-score`).innerText=scores[i];
‎                    box.className = (turn==i)?"p-info active-p":"p-info";
‎                } else box.style.display="none";
‎            }
‎        }
‎        init();
‎    </script>
‎    {% endif %}
‎</body>
‎</html>
‎'''
‎
‎@app.route('/')
‎def home(): return render_template_string(HTML_TEMPLATE, in_game=False)
‎
‎@app.route('/play')
‎def play():
‎    h = int(request.args.get('humans', 1))
‎    b = int(request.args.get('bots', 1))
‎    return render_template_string(HTML_TEMPLATE, in_game=True, h_count=h, b_count=b)
‎
‎if __name__ == '__main__':
‎    app.run(host='0.0.0.0', port=10000)
‎