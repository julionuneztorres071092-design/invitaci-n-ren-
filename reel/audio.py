"""Música original del reel (15 s, 120 ppm): cascabeles, campanitas, bombo y transiciones.
Uso: python3 audio.py salida.wav"""
import sys
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR, DUR, BEAT = 44100, 15.0, 0.5
N = int(SR * DUR)
L = np.zeros(N + SR)
Rr = np.zeros(N + SR)
rng = np.random.default_rng(1212)


def add(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i < 0 or i >= N:
        return
    n = min(len(sig), len(L) - i)
    L[i:i + n] += sig[:n] * gain * (1 - max(0, pan))
    Rr[i:i + n] += sig[:n] * gain * (1 + min(0, pan))


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def tt(d):
    return np.arange(int(SR * d)) / SR


def bp(x, lo, hi):
    return sosfilt(butter(2, [lo, hi], 'bandpass', fs=SR, output='sos'), x)


def hp(x, f):
    return sosfilt(butter(2, f, 'highpass', fs=SR, output='sos'), x)


def lp(x, f):
    return sosfilt(butter(2, f, 'lowpass', fs=SR, output='sos'), x)


def bell(m, d=1.4):  # campanita / glockenspiel
    t = tt(d)
    f = hz(m)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 4.5)
    s += .45 * np.sin(2 * np.pi * f * 2.756 * t) * np.exp(-t * 9)
    s += .22 * np.sin(2 * np.pi * f * 5.404 * t) * np.exp(-t * 16)
    s[:60] *= np.linspace(0, 1, 60)
    return s


def kick():
    t = tt(.32)
    f = 46 + 110 * np.exp(-t * 34)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
    return s + .25 * hp(rng.standard_normal(len(t)), 2000) * np.exp(-t * 120)


def clap():
    t = tt(.22)
    n = bp(rng.standard_normal(len(t)), 900, 3800)
    env = sum(np.exp(-np.maximum(t - d, 0) * 46) * (t >= d) for d in (0, .011, .023))
    return n * env * .5


def sleigh(acc=1.0):  # cascabel
    t = tt(.2)
    n = bp(rng.standard_normal(len(t)), 5200, 11500) * np.exp(-t * 26)
    ring = sum(np.sin(2 * np.pi * f * t + rng.uniform(0, 6)) for f in rng.uniform(3300, 7600, 7)) / 7
    return (n * .8 + ring * np.exp(-t * 20) * .7) * acc


def bass(m, d=.22):
    t = tt(d)
    f = hz(m)
    s = np.sin(2 * np.pi * f * t) + .35 * np.sin(2 * np.pi * 2 * f * t) + .15 * np.sin(2 * np.pi * 3 * f * t)
    env = np.minimum(1, t * 200) * np.exp(-t * 5)
    return s * env


def whoosh(d=.42, up=True):
    t = tt(d)
    n = rng.standard_normal(len(t))
    out = np.zeros(len(t))
    k = 8
    for i in range(k):  # barrido de filtro por tramos
        a, b = i * len(t) // k, (i + 1) * len(t) // k + 400
        u = (i + .5) / k
        u = u if up else 1 - u
        fc = 500 * (16 ** u)
        seg = bp(n, fc * .7, min(fc * 1.5, 18000))[a:b]
        w = np.hanning(len(seg))
        out[a:a + len(seg)] += seg[:len(out) - a] * w[:len(out) - a]
    env = (t / d) ** 2.2 if up else (1 - t / d) ** 1.5
    return out * env


def impact():
    t = tt(1.6)
    f = 38 + 90 * np.exp(-t * 16)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.2)
    cym = hp(rng.standard_normal(len(t)), 5000) * np.exp(-t * 3.4) * .32
    return boom + cym


def pad(notes, d):
    t = tt(d)
    s = sum(np.sin(2 * np.pi * hz(n) * t * (1 + dt)) + .3 * np.sin(2 * np.pi * hz(n) * 2 * t) for n in notes for dt in (-.003, .003))
    env = np.minimum(1, t / .06) * np.minimum(1, (d - t) / .5)
    return lp(s, 2600) * env / len(notes)


def snare():
    t = tt(.12)
    return (bp(rng.standard_normal(len(t)), 1500, 7000) * np.exp(-t * 40) + .5 * np.sin(2 * np.pi * 190 * t) * np.exp(-t * 50)) * .6


# Armonía por compás (2 s): Do – La m – Fa – Sol – Do – Sol
CH = [(48, [60, 64, 67]), (45, [57, 60, 64]), (41, [57, 60, 65]), (43, [59, 62, 67]), (48, [60, 64, 67]), (43, [59, 62, 67])]
# Melodía original en corcheas (campanitas), una lista por compás
MEL = [
    [76, 79, 84, 79, 76, 79, 81, 79],
    [76, 81, 84, 81, 76, 81, 83, 81],
    [77, 81, 84, 81, 86, 84, 81, 77],
    [79, 83, 86, 83, 79, 83, 86, 88],
    [84, 88, 91, 88, 84, 88, 86, 84],
    [83, 86, 91, 86, 83, 86, 91, 93],
]

# --- Intro (0–2 s): golpes en cada pulso, alineados con SÁBADO / 12 / DICIEMBRE / etiqueta
for i, m in enumerate([72, 76, 79, 84]):
    add(kick(), i * BEAT, 1.0)
    add(bell(m, 1.0), i * BEAT, .5)
    add(bell(m - 12, 1.0), i * BEAT, .3)
add(impact(), 1.5, .55)

# --- Cuerpo (0–12 s)
for bar in range(6):
    t0 = bar * 2.0
    root, tri = CH[bar]
    add(pad(tri, 2.0), t0, .16 if bar else .1)
    for k in range(8):  # corcheas
        t = t0 + k * .25
        add(sleigh(1.0 if k % 2 == 0 else .55), t, .26, pan=.25 if k % 2 else -.25)
        if bar >= 1:
            add(bell(MEL[bar][k], .9), t, .34, pan=(-.2 if k % 2 else .2))
            if k % 2 == 1:
                add(bass(root if k % 4 == 1 else root + 7), t, .5)
        if bar >= 1 and k % 2 == 0:
            add(kick(), t, .95)
            add(bass(root, .2), t, .42)
        if bar >= 1 and k % 4 == 2:
            add(clap(), t, .75)

# --- Transiciones: barrido antes de cada corte e impacto en el corte
for cut in (2, 4, 6, 8, 10):
    add(whoosh(.42, True), cut - .42, .5)
    add(impact(), cut, .42)
    add(whoosh(.5, False), cut, .22)
add(bell(88, 1.2), 3.0, .3)  # acentos de tipografía
for tk in (4.5, 5.0, 6.5, 8.5, 9.0, 10.5, 11.0):
    add(snare(), tk, .4)

# --- Subida final (11–12 s): redoble acelerado y barrido largo
tk = 11.0
step = .125
while tk < 11.97:
    add(snare(), tk, .32 + .5 * (tk - 11))
    if tk > 11.5:
        step = .0625
    tk += step
add(whoosh(1.0, True), 11.0, .75)

# --- Final (12–15 s): acorde, arpegio de campanas y avisos de la llamada a la acción
add(impact(), 12.0, .95)
add(pad([48, 60, 64, 67, 72], 3.0), 12.0, .3)
for i, m in enumerate([72, 76, 79, 84, 88, 91, 96]):
    add(bell(m, 2.4), 12.0 + i * .085, .42, pan=(i - 3) * .12)
for k in range(8):
    add(sleigh(1.0 if k % 2 == 0 else .5), 12.0 + k * .25, .2 * (1 - k / 10))
add(bell(91, 2.0), 13.0, .5)   # ¡Te esperamos!
add(bell(84, 2.0), 13.0, .3)
add(bell(96, 2.2), 13.5, .55)  # botón
add(bell(88, 2.2), 13.5, .35)
add(bell(100, 1.6), 14.0, .3)

x = np.stack([L[:N], Rr[:N]], 1)
fade = np.ones(N)
k = int(SR * .9)
fade[-k:] = np.linspace(1, 0, k) ** 1.5
x *= fade[:, None]
x = np.tanh(x * 1.5 / np.percentile(np.abs(x), 99.9)) * .93  # limitador suave
wavfile.write(sys.argv[1], SR, (x * 32767).astype(np.int16))
print('ok', x.shape, float(np.abs(x).max()))
