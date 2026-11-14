# Invitación REN 2026

Invitación digital (sitio estático, en español) para la celebración de fin de año de
**Logística y Transportes REN**: Misa de acción de gracias (viernes 11 de diciembre de 2026) y
celebración (sábado 12 de diciembre de 2026). Pensada para compartirse como enlace por WhatsApp.

**URL publicada:** https://fiesta2026.transportes-ren.com.mx/

## Estructura

```
index.html                 página completa (HTML + CSS + JS en línea, sin dependencias externas)
assets/favicon.svg         monograma "R"
assets/fonts/              Instrument Serif (normal e itálica) e Inter variable, woff2 autoalojadas
assets/img/ren-logo.svg    logo REN vectorizado (calcado del original)
assets/img/ren-logo.png    logo REN 1088×588, fondo transparente
assets/img/virgen.jpg      recorte de la Virgen de Guadalupe (misa)
assets/img/jesus.jpg       recorte de Jesús (misa)
assets/img/grupo-contraste.jpg  panorámica de Grupo Contraste (grupo-contraste-m.jpg: recorte 4:3 para móvil)
assets/img/orn-*.svg       ornamentos originales de trazo fino (rayos, rosa, estrella, filete)
assets/img/wall-house.png  logo de DJ Wall-House sobre negro
assets/img/portada-whatsapp.jpg  miniatura para WhatsApp / redes (1200×630)
                           Las fotos son recortes sin texto de los flyers del cliente (original/referencias/);
                           los ornamentos son trabajo vectorial original.
original/                  versión 1 y archivos originales, solo como referencia
docs/PLAN.md               plan de diseño
```

## Ver en local

Abre `index.html` directamente en el navegador, o sirve la carpeta (recomendado, para que las
fuentes y la descarga .ics funcionen igual que en línea):

```
python3 -m http.server 8000
# luego abre http://localhost:8000
```

## Publicar con GitHub Pages

1. Sube los cambios a la rama `main`.
2. En GitHub: **Settings → Pages → Build and deployment → Deploy from a branch**,
   rama `main`, carpeta `/ (root)` → **Save**.
3. En el plan gratuito el repositorio debe ser **público**.
4. En uno o dos minutos estará en la URL de arriba. La miniatura de WhatsApp usa
   `assets/img/portada-whatsapp.jpg` con URL absoluta; WhatsApp guarda en caché las vistas previas,
   así que si cambias la imagen puede tardar en actualizarse.

## Si cambian fechas, horas o direcciones

Todo está en `index.html`: textos visibles, fechas de los contadores, enlaces de Google Maps y los
datos del calendario (Google, Outlook y archivo .ics). Busca la fecha o la dirección actual y
reemplázala en todos los lugares donde aparezca. Las horas se interpretan en America/Mexico_City
(UTC−6). Si cambian las fechas, actualiza también la portada `portada-whatsapp.jpg`.

## Notas

- La misa **no tiene hora de término confirmada**: el calendario usa 7:30 p. m. solo como
  estimación técnica, no como horario anunciado.
- Las imágenes de la Virgen, Jesús, Grupo Contraste y Wall-House son recortes (ampliados y
  retocados con suavidad) de los flyers de referencia suministrados. El logo REN se vectorizó a
  partir de un archivo de baja resolución (272×147 px). Sustituirlos por fotografías y logotipos
  originales en alta resolución mejoraría la calidad.
- Sin formularios, sin recopilación de datos y sin servicios de terceros.

## Música

La música es el archivo `assets/audio/musica.mp3`, proporcionado por el cliente. Para cambiarla, sustituye ese archivo por otro MP3 con el mismo nombre. Solo suena si el visitante elige "Entrar con música" o la activa arriba a la derecha.

## Reel de la fiesta

`reel/fiesta-ren-2026.mp4` es un video vertical de 15 s (1080x1920) para historias y estados. Se genera con:

1. `python3 reel/logo_build.py assets/img/ren-logo-vector.svg` (logo vectorial redibujado).
2. `python3 reel/audio.py audio.wav` (música original).
3. `FPS=120 node reel/render.js http://localhost:8765/reel/reel.html cuadros/` sirviendo la carpeta del proyecto por HTTP.
4. `ffmpeg` une los cuadros (mezclando 4 por cuadro para el desenfoque de movimiento) con el audio.

`reel/reel.html?play` muestra la animación en el navegador.
