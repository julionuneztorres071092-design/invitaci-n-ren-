"""Redibuja el logo REN como vector geométrico limpio (coordenadas en el lienzo 1088x588)."""
import sys
out = sys.argv[1]
DARK, LIGHT, RED, GREY = '#0f4984', '#2675b7', '#e81d37', '#585858'

# Barras de velocidad: (x_izq, y_sup, y_inf) y muescas blancas entre ellas (x_fin)
bars = [(298, 138, 165), (206, 190, 217), (365, 242, 269), (262, 287, 313), (343, 338, 365)]
notch = [387, 420, 456, 405]
p = []
x0, t, b = bars[0]
r = (b - t) / 2
p.append(f'M{x0 + r},{t}')
# borde superior hasta el chaflán de la R
p.append('H503 L521,156 Q524,165 514,165 H471')
# tallo blanco de la R: baja por x=471 y sale por el pie
p.append('V336 Q471,340 475,340 H513 Q518,340 518,335 V288 Q518,283 523,283 H533 Q539,283 542,288 L557,313 Q560,319 555,324 L512,362 Q508,365 503,365')
# borde inferior hacia la izquierda y perfil izquierdo (barras y muescas) de abajo arriba
for i in range(4, -1, -1):
    x, t, b = bars[i]
    r = (b - t) / 2
    p.append(f'H{x + r} A{r},{r} 0 0 1 {x + r},{t}')
    if i > 0:
        pt, pb = bars[i - 1][1], bars[i - 1][2]
        g = (t - pb) / 2
        n = notch[i - 1]
        p.append(f'H{n - g} A{g},{g} 0 0 0 {n - g},{pb}')
p.append('Z')
dark = ' '.join(p)
counter = 'M523,201 H547 A22.5,22.5 0 0 1 547,246 H523 Q519,246 519,242 V205 Q519,201 523,201 Z'

E = ('M592,168 H712 Q717,168 717,173 V201 Q717,206 712,206 H637 Q633,206 633,210 V232 Q633,236 637,236 H694 Q699,236 699,241 '
     'V265 Q699,270 694,270 H637 Q633,270 633,274 V295 Q633,299 637,299 H714 Q719,299 719,304 V334 Q719,339 714,339 H632 '
     'Q626,339 623,334 L591,277 Q588,272 593,268 Q618,247 616,222 Q614,198 590,174 Q586,168 592,168 Z')
N = ('M730,168 H768 Q773,168 776,173 L830,251 Q836,259 836,249 V173 Q836,168 841,168 H877 Q882,168 882,173 V334 Q882,339 877,339 '
     'H838 Q833,339 830,334 L777,252 Q771,243 771,253 V334 Q771,339 766,339 H730 Q725,339 725,334 V173 Q725,168 730,168 Z')

reds = [(206, 139, 268, 165), (213, 242, 258, 269), (285, 242, 347, 269), (280, 338, 326, 364)]

# TRANSPORTES en trazo redondeado
T0, B0, MID = 397.5, 443.5, 420.5
L = []
def t_(a, b): c = (a + b) / 2; return f'M{a + 4.5},{T0} H{b - 4.5} M{c},{T0} V{B0}'
def r_(a, b): return f'M{a + 4.5},{B0} V{T0} H{b - 18} a13,13 0 0 1 0,26 H{a + 4.5} M{b - 20},{T0 + 26} L{b - 4.5},{B0}'
def a_(a, b): c = (a + b) / 2; return f'M{a + 4.5},{B0} L{c},{T0} L{b - 4.5},{B0} M{a + 13.5},{B0 - 16} H{b - 13.5}'
def n_(a, b): return f'M{a + 4.5},{B0} V{T0} L{b - 4.5},{B0} V{T0}'
def s_(a, b): return (f'M{b - 5},{T0 + 6} C{b - 11},{T0 - 3} {a + 4},{T0 - 4} {a + 5},{T0 + 12} '
                      f'C{a + 6},{MID + 2} {b - 4},{MID - 3} {b - 5},{B0 - 12} C{b - 5},{B0 + 4} {a + 9},{B0 + 3} {a + 4.5},{B0 - 7}')
def p_(a, b): return f'M{a + 4.5},{B0} V{T0} H{b - 18} a13.5,13.5 0 0 1 0,27 H{a + 4.5}'
def e_(a, b): return f'M{b - 4.5},{T0} H{a + 4.5} V{B0} H{b - 4.5} M{a + 4.5},{MID} H{b - 8}'
word = [(t_, 318, 359), (r_, 369, 409), (a_, 417, 467), (n_, 478, 526), (s_, 537, 573), (p_, 583, 619), (None, 625, 681),
        (r_, 691, 731), (t_, 735, 776), (e_, 786, 818), (s_, 827, 863)]
letters = []
for f, a, b in word:
    if f is None:
        letters.append(f'<ellipse cx="{(a + b) / 2}" cy="{MID}" rx="{(b - a) / 2 - 4.5}" ry="23"/>')
    else:
        letters.append(f'<path d="{f(a, b)}"/>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="190 122 708 344" role="img" aria-label="REN Transportes">
<g id="reds" fill="{RED}">{''.join(f'<rect x="{a}" y="{b}" width="{c - a}" height="{d - b}" rx="{(d - b) / 2}"/>' for a, b, c, d in reds)}</g>
<g id="mark" fill="{DARK}"><path d="{dark}"/><path d="{counter}"/></g>
<g id="en" fill="{LIGHT}"><path id="E" d="{E}"/><path id="N" d="{N}"/></g>
<g id="word" fill="none" stroke="{GREY}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round">{''.join(letters)}</g>
</svg>
'''
open(out, 'w', encoding='utf-8').write(svg)
print('ok', len(svg))
