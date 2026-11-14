// Uso: node render.js [salida.mp4] [frameUnico_seg]
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
(async () => {
  const out = process.argv[2] || 'ren-showreel.mp4';
  const only = process.argv[3];
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await pg.goto('file://' + path.join(__dirname, 'index.html'));
  await pg.waitForFunction('window.ready===true');
  if (only !== undefined) {
    const d = await pg.evaluate(t => window.renderFrame(t), parseFloat(only));
    fs.writeFileSync(out, Buffer.from(d, 'base64'));
    await b.close(); return;
  }
  const ff = spawn('ffmpeg', ['-y', '-f', 'image2pipe', '-framerate', '30', '-i', '-',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-pix_fmt', 'yuv420p',
    '-movflags', '+faststart', out], { stdio: ['pipe', 'ignore', 'inherit'] });
  for (let f = 0; f < 450; f++) {
    const d = await pg.evaluate(t => window.renderFrame(t), f / 30);
    if (!ff.stdin.write(Buffer.from(d, 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close();
})();
