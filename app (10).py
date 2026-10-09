import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hello World Motion Lab", page_icon="✨", layout="wide")
st.title("✨ Hello World Motion Lab")
st.caption("Type your name, customize its appearance, and explore looping animations!")

with st.sidebar:
    st.header("Customize your greeting")
    name = st.text_input("Your name", "Hello World", max_chars=80)
    font = st.selectbox("Font", ["Arial", "Georgia", "Verdana", "Courier New", "Times New Roman", "Trebuchet MS", "Impact", "Comic Sans MS", "Palatino Linotype"])
    size = st.slider("Font size (pixels)", 20, 110, 58)
    background = st.selectbox("Background", ["Light", "Dark", "Ocean", "Sunset", "Forest", "Midnight", "Candy"])
    mode = st.selectbox("Display mode", ["Centered", "Ticker Tape", "Repeated"])
    effect = st.selectbox("Weather / celebration", ["None", "Rain", "Snow", "Hail", "Wind Gusts", "Confetti", "Tornadoes"])
    speed = st.slider("Animation speed", 0.25, 3.0, 1.0, 0.25)
    count = st.slider("Effect intensity", 15, 140, 65, 5)

backgrounds = {
    "Light": ("#f8fafc", "#172033"),
    "Dark": ("#101827", "#ffffff"),
    "Ocean": ("linear-gradient(135deg,#073b64,#0e7490,#67e8f9)", "#ffffff"),
    "Sunset": ("linear-gradient(135deg,#ffb36b,#e85d75,#693b89)", "#ffffff"),
    "Forest": ("linear-gradient(135deg,#163b2c,#28744b,#a0c77d)", "#ffffff"),
    "Midnight": ("linear-gradient(135deg,#070a24,#23225c,#50388a)", "#ffffff"),
    "Candy": ("linear-gradient(135deg,#ffe4f2,#c7d2fe,#a5f3fc)", "#292044"),
}
bg, fg = backgrounds[background]
config = {"name": name or "Hello World", "font": font, "size": size, "background": bg,
          "foreground": fg, "mode": mode, "effect": effect, "speed": speed, "count": count}
# JSON serialization prevents user input from becoming executable HTML/JavaScript.
settings = json.dumps(config).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
html = r'''<!doctype html><html><head><meta charset="utf-8"><style>
*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;overflow:hidden}
#stage{height:580px;width:100%;position:relative;overflow:hidden;isolation:isolate}
#effects{position:absolute;inset:0;pointer-events:none;z-index:2}
#names{position:absolute;inset:0;z-index:1;display:flex;align-items:center;justify-content:center;overflow:hidden}
.name{text-align:center;font-weight:700;max-width:95%;overflow-wrap:anywhere;text-shadow:0 3px 14px #0003}
#names.repeated{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));align-content:space-evenly;justify-items:center;gap:8px}
#names.repeated .name{font-size:.65em}
#names.ticker{display:block;white-space:nowrap}
#names.ticker .track{display:flex;align-items:center;gap:100px;width:max-content;height:100%;animation:marquee 14s linear infinite}
#names.ticker .name{flex-shrink:0;white-space:nowrap}
@keyframes marquee{from{transform:translateX(100vw)}to{transform:translateX(-100%)}}
.particle{position:absolute;top:0;left:0;will-change:transform;user-select:none;white-space:nowrap}
@keyframes fall{from{transform:translate3d(var(--x),-70px,0) rotate(0deg)}to{transform:translate3d(calc(var(--x) + var(--drift)),660px,0) rotate(var(--spin))}}
@keyframes gust{from{transform:translate3d(-120px,var(--y),0)}to{transform:translate3d(calc(100vw + 130px),calc(var(--y) - 50px),0)}}
@keyframes swirl{0%{transform:translate3d(calc(var(--x) - 80px),-60px,0) rotate(0deg) scale(.5)}50%{transform:translate3d(calc(var(--x) + 80px),270px,0) rotate(540deg) scale(1.3)}100%{transform:translate3d(calc(var(--x) - 80px),650px,0) rotate(1080deg) scale(.5)}}
</style></head><body><div id="stage"><div id="names"></div><div id="effects"></div></div>
<script>
const cfg=__SETTINGS__;
const stage=document.getElementById('stage'),names=document.getElementById('names'),effects=document.getElementById('effects');
stage.style.background=cfg.background;stage.style.color=cfg.foreground;
names.style.fontFamily=JSON.stringify(cfg.font)+',sans-serif';names.style.fontSize=cfg.size+'px';
function label(){const d=document.createElement('div');d.className='name';d.textContent=cfg.name;return d;}
if(cfg.mode==='Centered'){names.append(label());}
else if(cfg.mode==='Repeated'){names.className='repeated';for(let i=0;i<6;i++)names.append(label());}
else{names.className='ticker';const track=document.createElement('div');track.className='track';for(let i=0;i<3;i++)track.append(label());track.style.animationDuration=(14/cfg.speed)+'s';names.append(track);}
const symbols={'Rain':['💧','💦'],'Snow':['❄️','❅','❆'],'Hail':['●','⚪'],'Wind Gusts':['💨','〰','➰'],'Confetti':['🎊','🎉','✨','🟨','🟪','🟦','🟥'],'Tornadoes':['🌪️','🌀']};
const list=symbols[cfg.effect]||[];
for(let i=0;i<(cfg.effect==='None'?0:cfg.count);i++){
 const el=document.createElement('span');el.className='particle';el.textContent=list[Math.floor(Math.random()*list.length)];
 const x=Math.random()*100,delay=-Math.random()*12;
 el.style.setProperty('--x',x+'vw');el.style.setProperty('--y',Math.random()*580+'px');
 el.style.setProperty('--drift',((Math.random()-.5)*240)+'px');el.style.setProperty('--spin',(Math.random()*900-450)+'deg');
 el.style.fontSize=(cfg.effect==='Tornadoes'?20+Math.random()*30:13+Math.random()*18)+'px';
 el.style.opacity=String(.4+Math.random()*.55);
 const wind=cfg.effect==='Wind Gusts',tornado=cfg.effect==='Tornadoes';
 const duration=(wind?3:tornado?6:5)+Math.random()*5;
 el.style.animation=`${wind?'gust':tornado?'swirl':'fall'} ${duration/cfg.speed}s linear ${delay/cfg.speed}s infinite`;
 effects.append(el);
}
</script></body></html>'''.replace('__SETTINGS__', settings)
components.html(html, height=590, scrolling=False)
st.info("Try changing the font, background, display mode, and animation. The motion runs continuously in your browser without rerunning Python.")
with st.expander("How this app works"):
    st.markdown("**Streamlit** creates the controls. **Python** sends the selected settings to an embedded HTML/CSS/JavaScript scene. **CSS keyframe animations** make particles and ticker text move smoothly in an infinite loop. No extra packages are needed.")
