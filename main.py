from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    # यहाँ आपका पुराना kr.py वाला लॉजिक ब्राउज़र के लिए सेट है
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>S KANHAIYA SYSTEM - KR.PY EDITION</title>
    <style>
        body { background: #000; color: #0f0; text-align: center; margin: 0; overflow: hidden; }
        canvas { border: 5px solid #0f0; box-shadow: 0 0 20px #0f0; margin-top: 15px; }
        h1 { text-shadow: 0 0 10px #0f0; font-family: monospace; }
    </style>
</head>
<body>
    <h1>S KANHAIYA SYSTEM</h1>
    <canvas id="gameCanvas"></canvas>
    <p style="font-family: monospace;">९०° कोण का नियम चालू है</p>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth * 0.95;
        canvas.height = window.innerHeight * 0.7;

        let boxes = [];
        // आपका असली '१०० बॉक्स' वाला सिस्टम
        for(let i=0; i<100; i++) {
            boxes.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                w: 15, h: 15,
                dx: (Math.random() < 0.5 ? 4 : -4), // ९० डिग्री मूवमेंट के लिए
                dy: (Math.random() < 0.5 ? 4 : -4),
                color: `hsl(${Math.random() * 360}, 100%, 50%)`
            });
        }

        function runSystem() {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            boxes.forEach(b => {
                ctx.strokeStyle = b.color;
                ctx.strokeRect(b.x, b.y, b.w, b.h);
                
                b.x += b.dx;
                b.y += b.dy;

                // ९० डिग्री टकराने का नियम
                if(b.x <= 0 || b.x + b.w >= canvas.width) b.dx *= -1;
                if(b.y <= 0 || b.y + b.h >= canvas.height) b.dy *= -1;
            });
            requestAnimationFrame(runSystem);
        }
        runSystem();
    </script>
</body>
</html>
''')

if __name__ == '__main__':
    # Render के लिए पोर्ट १०००० ज़रूरी है
    app.run(host='0.0.0.0', port=10000)
