# Plan de rediseño · Invitación REN 2026 (v2)

Objetivo: llevar la invitación a un nivel editorial de alta gama (referencia: sitios premiados 2026 —
tipografía serif protagonista, paleta contenida, movimiento lento y con intención) y dejarla lista
para compartirse como enlace por WhatsApp.

## 1. Crítica de la v1 (hallazgos)

| # | Hallazgo | Corrección |
|---|----------|-----------|
| 1 | Paleta dispersa: azul, rojo vino, dorado, blanco y confeti de 4 colores compiten | Una sola paleta: tinta nocturna + marfil + **un** acento champán |
| 2 | Tipografía de sistema (Georgia + sans genérica), tracking negativo excesivo que pega las letras | Serif editorial autoalojada (Instrument Serif) + Inter; escala tipográfica definida |
| 3 | Decoración de plantilla: copos, confeti, esfera, camión emoji, rayos cónicos | Eliminar todo. Sustituir por grano sutil, polvo dorado discreto y líneas finas |
| 4 | Emojis como iconos (🕡 📍 🎉 👔 🚛) | Sin emojis: etiquetas tipográficas en versalitas e iconos SVG de trazo fino si hacen falta |
| 5 | Imágenes recortadas de flyers con texto cortado ("TRANSPORTES", "Misa de", "GRUPO…") | Recortes limpios sin texto; díptico en arcos para la misa; banda panorámica para el grupo |
| 6 | Logo REN pixelado al ampliarlo a 480 px (el archivo mide 272 px) | Usarlo pequeño (≤136 px CSS) como sello sobre placa marfil; el protagonista es la tipografía |
| 7 | Textos genéricos y repetitivos ("agradecer, compartir y celebrar" tres veces) | Reescritura sobria y cálida (ver §4) |
| 8 | Transiciones uniformes (fade + translate en todo), animaciones infinitas distraen | Coreografía: revelado por líneas con máscara, entrada escalonada, curvas `cubic-bezier(.2,.8,.2,1)`, 0.9–1.4 s |
| 9 | Botones tipo píldora con degradado dorado brillante; 3 chips de calendario pequeños (objetivo táctil < 44 px) | Botones sobrios, borde fino, mínimo 48 px de alto; calendario en un solo menú |
| 10 | Navegación superior apretada en móvil (4 píldoras + marca) | Barra mínima: marca a la izquierda, música a la derecha; índice discreto |
| 11 | Jerarquía plana: las dos fechas no se entienden de un vistazo | Portada con "11 — 12 · Diciembre · 2026" y programa numerado I / II |
| 12 | Hueco vacío bajo el contador; secciones con `min-height` que dejan aire muerto | Ritmo vertical por escala de espaciado, sin alturas forzadas |
| 13 | `og:image` relativo: WhatsApp no muestra miniatura | URL absoluta + portada 1200×630 nueva, coherente con el diseño |
| 14 | Sin estado claro para "después del evento" y sin `noscript` | Estados del contador: antes / hoy / concluido; contenido visible sin JS |

## 2. Dirección de arte: "Editorial de noche"

- **Paleta** (tokens CSS):
  `--ink:#080c15` (fondo) · `--ink-2:#0e1422` (superficies) · `--line:rgba(236,226,204,.14)` ·
  `--ivory:#f1ead9` (texto) · `--muted:#9a9685` (secundario) · `--gold:#c9a25e` (acento único) ·
  `--gold-soft:#e4cd9c` (énfasis en titulares). Azul REN solo dentro del logo.
- **Tipografía**: `Instrument Serif` (regular + itálica) para titulares; `Inter` variable para texto y
  etiquetas (versalitas 11–12 px, tracking .22em). Autoalojadas en `assets/fonts/` (woff2, latin).
- **Textura**: grano SVG fijo al 5–7 % de opacidad; un único resplandor radial cálido muy tenue en portada.
- **Forma**: esquinas rectas o radio 2 px; imágenes en arco (medio punto) para la misa; filetes de 1 px.
- **Movimiento**: pantalla de apertura ("Abrir invitación") que se levanta como telón; titulares que
  suben línea a línea tras máscara; imágenes con `clip-path` + ligera escala; parallax ≤ 6 %;
  contador con dígitos tabulares sin saltos. Todo respeta `prefers-reduced-motion`.
- **Sonido**: se ofrece al abrir ("Entrar con música" / "Entrar en silencio"); conmutador discreto arriba.

## 3. Estructura

0. **Apertura** — sello REN, "Estás invitado", dos botones (con música / en silencio).
1. **Portada** — eyebrow "Logística y Transportes REN", titular "Gracias por un gran *2026*",
   fechas "11 — 12 · Diciembre", indicador de scroll.
2. **Gratitud** — manifiesto en serif grande con revelado por palabras al hacer scroll.
3. **I · La Misa** — viernes 11 dic., 6:30 p. m., C. Manuel Bauche 2. Díptico Virgen / Jesús en arcos.
4. **II · La Celebración** — sábado 12 dic., 2:00 p. m. – 1:00 a. m., Jesús Capistrán 94.
   Grupo Contraste + DJ Wall-House. Vestimenta: casual elegante.
5. **Cierre** — "Te esperamos", anfitriones, accesos rápidos.

Cada evento: ficha (Fecha / Hora / Lugar / Vestimenta), contador, "Cómo llegar" (Maps) y
"Agregar al calendario" (Google, Outlook, Apple .ics).

## 4. Textos (definitivos)

- Apertura: **"Estás invitado"** · "Celebración de fin de año · REN 2026"
- Portada: **"Gracias por un gran 2026"** · "Dos encuentros para cerrar el año como lo vivimos: juntos."
- Gratitud (manifiesto): "Este año nos puso a prueba y nos encontró unidos. Damos gracias a Dios y a
  la Virgen de Guadalupe por cada kilómetro recorrido con bien, y a cada colaborador y a su familia
  por el esfuerzo que hay detrás de cada entrega."
  Remate: "Antes de celebrar, queremos agradecer."
- Misa: eyebrow "I — Viernes 11 de diciembre" · título **"Misa de acción de gracias"** ·
  "Un momento de fe y recogimiento para agradecer lo vivido y encomendar el año que comienza."
- Fiesta: eyebrow "II — Sábado 12 de diciembre" · título **"La celebración"** ·
  "Una tarde que se vuelve noche: buena mesa, música en vivo y la alegría de estar juntos."
  Música: "Grupo Contraste, La Orquesta de las Estrellas · En cabina, DJ Wall-House".
- Cierre: **"Te esperamos"** · "Será un honor recibirte." · Anfitriones: "Eder Javier Pineda Gutiérrez
  y familia" · "Dirección de Logística y Transportes REN" · "Evento privado · Invitación personal".

Datos que NO cambian: fechas, horas, direcciones, enlaces de Maps, zona horaria (UTC−6), vestimenta,
nombres. La misa no tiene hora de término confirmada (el .ics usa 7:30 p. m. como estimación).

## 5. Contrato de archivos

```
index.html            página (HTML + CSS + JS en línea, sin dependencias externas)
assets/fonts/instrument-serif-latin-400-normal.woff2
assets/fonts/instrument-serif-latin-400-italic.woff2
assets/fonts/inter-latin-wght-normal.woff2
assets/img/ren-logo.png        logo original (272×147), sin reescalar
assets/img/virgen.jpg          recorte vertical ~3:4, sin texto
assets/img/jesus.jpg           recorte vertical ~3:4, sin texto
assets/img/grupo-contraste.jpg panorámica sin el rótulo inferior
assets/img/wall-house.png      logo sobre negro, sin los puntos del borde izquierdo
assets/img/portada-whatsapp.jpg  1200×630, diseño nuevo
assets/favicon.svg
original/             v1 de referencia (no se publica como principal)
```

## 6. Reparto de agentes

| Agente | Responsabilidad | Archivos |
|--------|-----------------|----------|
| A · Recursos | Fuentes, recortes, portada OG, favicon, README | `assets/**`, `README.md`, `LEEME.txt` |
| B · Construcción | Diseño, textos, movimiento, lógica | `index.html` |
| C · Crítica y corrección | Revisión visual en móvil/escritorio, accesibilidad, enlaces, correcciones | todo |

Verificación final: capturas en 390 px y 1280 px, consola sin errores, contador, calendario, Maps,
música, `prefers-reduced-motion`, peso total < 1 MB.

## 7. Publicación

GitHub Pages desde la raíz del repositorio. URL prevista:
`https://julionuneztorres071092-design.github.io/invitaci-n-ren-/` (usada en `og:url` / `og:image`).
