// Captura los cuadros del reel con Playwright.
// Uso: node render.js <url de reel.html> <carpeta de salida> [lista de tiempos separados por coma para pruebas]
const {chromium}=require('playwright');
const [url,out,only]=process.argv.slice(2);
const FPS=+(process.env.FPS||30),DUR=15;
(async()=>{
  const b=await chromium.launch();
  const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
  const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
  await p.goto(url);await p.waitForFunction('window.ready===true',null,{timeout:20000});
  if(only){
    for(const t of only.split(',').map(Number)){await p.evaluate(v=>window.seek(v),t);await p.screenshot({path:`${out}/t${t.toFixed(2).replace('.','_')}.jpg`,type:'jpeg',quality:80})}
  }else{
    const n=FPS*DUR;
    for(let f=0;f<n;f++){await p.evaluate(v=>window.seek(v),f/FPS);await p.screenshot({path:`${out}/f${String(f).padStart(4,'0')}.jpg`,type:'jpeg',quality:95});
      if(f%450===0)console.log('cuadro',f,'/',n)}
  }
  console.log('errores',errs);await b.close();
})();
