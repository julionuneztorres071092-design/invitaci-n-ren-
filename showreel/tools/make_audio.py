# Audio sintético 100% generado por código, sincronizado a los eventos del showreel.
import numpy as np, wave, sys
from scipy.signal import lfilter, butter
SR=44100; DUR=15.0; N=int(SR*DUR)
L=np.zeros(N); R=np.zeros(N)
rng=np.random.default_rng(7)
def add(sig,t0,gain=1.0,pan=0.0):
    i=int(t0*SR)
    if i>=N or i<0: return
    sig=sig[:N-i]; g=gain
    L[i:i+len(sig)]+=sig*g*(1-max(0,pan)); R[i:i+len(sig)]+=sig*g*(1+min(0,pan))
def tt(d): return np.arange(int(d*SR))/SR
def env(d,a=.003,k=8): t=tt(d); return np.minimum(1,t/a)*np.exp(-k*t/d)
def kick(f0=160,f1=42,d=.28):
    t=tt(d); ph=2*np.pi*np.cumsum(f1+(f0-f1)*np.exp(-t*28))/SR
    return np.sin(ph)*env(d,.001,6)
def noise(d): return rng.standard_normal(int(d*SR))
def bp_sweep(d,f_a,f_b,q=2.5):
    x=noise(d); out=np.zeros_like(x); ch=256; zi=None
    for i in range(0,len(x),ch):
        f=f_a*(f_b/f_a)**(i/len(x)); w=f/(SR/2); w=min(.95,max(.005,w))
        b,a=butter(2,[max(.003,w*(1-1/(2*q))),min(.97,w*(1+1/(2*q)))],'band')
        if zi is None or len(zi)!=max(len(a),len(b))-1: zi=np.zeros(max(len(a),len(b))-1)
        y,zi=lfilter(b,a,x[i:i+ch],zi=zi); out[i:i+ch]=y
    return out/(np.abs(out).max()+1e-9)
def whoosh(d=.55,up=True):
    s=bp_sweep(d,400,6000,1.2) if up else bp_sweep(d,6000,400,1.2)
    t=tt(d); e=np.sin(np.pi*np.clip(t/d,0,1))**1.5
    return s*e
def riser(d=.6):
    s=bp_sweep(d,300,7000,1.5); t=tt(d); return s*(t/d)**2
def hp(x,fc):
    b,a=butter(2,fc/(SR/2),'high'); return lfilter(b,a,x)
def hat(d=.05): return hp(noise(d),7000)*env(d,.001,9)
def clap(d=.18): return hp(noise(d),1200)*env(d,.001,7)
def blip(f,d=.07): t=tt(d); return np.sin(2*np.pi*f*t)*env(d,.002,6)
def boom(d=.9):
    t=tt(d); ph=2*np.pi*np.cumsum(30+70*np.exp(-t*6))/SR
    return (np.sin(ph)+.4*hp(noise(d),200)*np.exp(-t*14))*env(d,.001,4)
def chime(f,d=1.4):
    t=tt(d); s=sum(a*np.sin(2*np.pi*f*m*t) for m,a in [(1,1),(2,.5),(3,.25),(4.01,.15)])
    return s*env(d,.004,4)
def sub(f,d): t=tt(d); return np.sin(2*np.pi*f*t)*np.minimum(1,t/.05)*np.minimum(1,(d-t)/.1)

S=[0,2.6,5.2,7.8,10.4,12.0]; beat=2.6/6
# pulso rítmico (S1–S4 y S6), con hi-hat a contratiempo
for sc,end in [(0,2.6),(2.6,5.2),(5.2,7.8),(7.8,10.4),(12.0,14.4)]:
    k=0
    while sc+k*beat<end-.05:
        t0=sc+k*beat
        add(kick(),t0,.55)
        add(hat(),t0+beat/2,.16,pan=.3)
        if k%2==1 and sc!=12.0: add(clap(),t0,.18)
        k+=1
# S1 MUEVE: golpes ascendentes por letra, barra roja
for i in range(5): add(blip(330*2**(i/6)*2,.09),.42+i*.07,.35,pan=(i-2)*.15); add(kick(120,50,.15),.45+i*.07,.4)
add(boom(.6),.62,.6); add(whoosh(.35,True),.82,.4)
for i in range(8): add(blip(1200+i*90,.04),.95+i*.04,.16)
# transiciones: riser previo + whoosh + impacto
for i in range(1,6):
    t=S[i]
    if i<5: add(riser(.6),t-.6,.45)
    add(whoosh(.6,True),t-.05,.75)
    add(boom(.7),t+.28,.7); add(clap(.25),t+.28,.35)
# S2: anillos, círculo rojo, letras
add(bp_sweep(1.2,800,5000,3)*np.sin(np.pi*np.clip(tt(1.2)/1.2,0,1)),S[1]+.05,.28)
add(blip(520,.2)*1.0,S[1]+.52,.5); add(boom(.5),S[1]+.5,.4)
for i in range(9): add(blip(500+i*60,.05),S[1]+.25+i*.055,.22,pan=-.3)
for i in range(12): add(blip(900+i*40,.035),S[1]+.78+i*.03,.12,pan=.3)
# S3: panel y letras
add(boom(.7),S[2]+.55,.75); add(clap(.25),S[2]+.55,.4)
for i in range(13): add(blip(700+i*35,.04),S[2]+.55+i*.03,.16)
add(whoosh(.4,False),S[2]+1.0,.25)
# S4: cuadros y texto
rs=np.random.default_rng(3)
for i in range(26): add(blip(rs.uniform(900,2400),.03),S[3]+rs.uniform(0,.9),.14,pan=rs.uniform(-.6,.6))
add(boom(.7),S[3]+.8,.75)
for i in range(11): add(blip(420+i*45,.06),S[3]+.65+i*.05,.25)
# S5: tres cortes con golpe creciente
for i in range(3):
    t=S[4]+i*(1.6/3)
    add(boom(.5),t,.85); add(clap(.22),t,.5); add(blip(220*2**(i/3),.25),t,.45)
    add(whoosh(.18,True),t-.1,.5)
# S6: logo
add(whoosh(.8,True),S[5]+.0,.65)
for i in range(5): add(blip(900+i*100,.04),S[5]+.02+i*.06,.2)
add(boom(.7),S[5]+.62,.8); add(boom(.5),S[5]+.9,.5)
for i in range(11): add(blip(1300+i*70,.03),S[5]+1.0+i*.045,.14,pan=(i-5)/9)
add(riser(.5),S[5]+1.0,.3)
for f,dl in [(523.25,0),(659.25,.06),(783.99,.12),(1046.5,.18)]: add(chime(f,1.6),S[5]+1.5+dl,.3)
add(blip(900,.25),S[5]+1.5,.5)  # pop CTA
add(boom(1.2),S[5]+1.5,.5)
add(sub(55,2.0),13.2,.3)
# master
m=np.maximum(np.abs(L),np.abs(R)).max(); 
fade=np.minimum(1,(DUR-tt(DUR)[:N])/.5)
L=np.tanh(L/m*1.6)*.9*fade[:N]; R=np.tanh(R/m*1.6)*.9*fade[:N]
pcm=(np.stack([L,R],1)*32767).astype('<i2')
with wave.open(sys.argv[1],'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
