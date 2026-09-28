# -*- coding: utf-8 -*-
"""
Genera ../02-wireframe.html (recorrido en grises con pines, estacionamiento y regla de scroll)
y audita el copy contra ../00-context/COPY-PUBLICADO.md.
Uso:  python3 build.py
"""
import json, re, html, os, sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import content as C

# ------------------------------------------------------------------ plantilla
TEMPLATE = r"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Wireframe de recorrido — Digizen B v04</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&family=Inter:wght@100..900&display=swap" rel="stylesheet">
<style>
/* ===== Escala del espécimen (Tipografía esencial): móvil·tablet < 860px ≤ desktop ===== */
:root{
  color-scheme: light;
  --micro:11px; --small:13px; --body:16px; --sub:19px; --head:24px; --semi:34px; --mon:48px; --mxl:64px;
  --gap:16px; --padY:28px; --padX:24px;
  --col-read:27rem; /* columna de lectura (≈38 caracteres de cuerpo); su borde izquierdo es el eje de lectura */
  /* wireframe: solo grises */
  --bg:#f1f1f1; --ink:#141414; --panel:#ffffff; --line:#d4d4d4; --night:#171717; --night-ink:#ececec;
  --chrome:#5c5c5c; --btn:#262626;
}
@media (min-width:860px){
  :root{ --micro:12px; --small:14px; --body:18px; --sub:24px; --head:32px; --semi:56px; --mon:96px; --mxl:144px;
         --gap:24px; --padY:24px; --padX:24px; }
}
*,*::before,*::after{box-sizing:border-box}
html,body{margin:0}
body{background:var(--bg);color:var(--ink);font-family:Inter,system-ui,sans-serif;font-weight:500;overflow-x:hidden}
p,h1,h2,h3,figure{margin:0}
.pf{font-family:"Playfair Display",Georgia,serif} .in{font-family:Inter,system-ui,sans-serif}
.w1{font-weight:100}.w3{font-weight:300}.w4{font-weight:400}.w5{font-weight:500}.w6{font-weight:600}.w7{font-weight:700}.w8{font-weight:800}.w9{font-weight:900}
.it{font-style:italic}
.t-micro{font-size:var(--micro);line-height:1.3;letter-spacing:.04em}
.t-small{font-size:var(--small);line-height:1.5}
.t-body{font-size:var(--body);line-height:1.5}
.t-sub{font-size:var(--sub);line-height:1.3}
.t-head{font-size:var(--head);line-height:1.1}
.t-semi{font-size:var(--semi);line-height:1.02;letter-spacing:-.01em}
.t-mon{font-size:var(--mon);line-height:1.02;letter-spacing:-.01em}
.t-mxl{font-size:var(--mxl);line-height:.95;letter-spacing:-.02em}
.bw{text-wrap:balance} .essay p, .sup p{text-wrap:pretty}
.acc{font-style:italic;text-decoration:underline dotted;text-decoration-thickness:.05em;text-underline-offset:.12em}
mark.val{background:#d9d9d9;color:inherit;padding:0 .15em}
.lnk{font-weight:600;text-decoration:underline;text-underline-offset:.2em;color:inherit;cursor:pointer}

/* ===== escenario / paradas ===== */
.pin{position:relative}
.stage{position:relative;height:100svh;overflow:hidden;background:var(--bg)}
.night{position:absolute;inset:0;background:var(--night);opacity:0;pointer-events:none;z-index:0}
.stop{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;padding:var(--padY) var(--padX);z-index:1;pointer-events:none}
.stop.is-active{pointer-events:auto}
.stop.nightc{color:var(--night-ink)}
@media (max-width:859px){.only-d{display:none!important}}
@media (min-width:860px){.only-m{display:none!important}}

/* ===== composiciones (espécimen) ===== */
.c{width:100%;max-width:1180px;margin:0 auto}
.ctr{text-align:center} .left{text-align:left}
.stack{display:flex;flex-direction:column;gap:10px} .ctr.stack{align-items:center}
.l06{margin-left:max(0px, calc((100% - var(--col-read)) / 2));margin-right:0;
  width:calc(100% - max(0px, calc((100% - var(--col-read)) / 2)));max-width:none}
/* golpe dentro de párrafo: el golpe centrado; el resto del párrafo en la columna de lectura, 32/48 px debajo */
.b01-l{align-items:center}
.b01-l .t-semi{max-width:18ch;text-align:center}
.b01-l > .t-body{width:min(100%, var(--col-read));text-align:left;margin-top:22px}
@media (min-width:860px){ .b01-l > .t-body{margin-top:38px} }
.b03 .lead-l{max-width:34ch}
.b03 > [data-beat=close]{margin-top:22px} /* entrada → golpe: 32 px en móvil (10 de gap + 22) */
@media (min-width:860px){ .b03 > [data-beat=close]{margin-top:38px} } /* 48 px en desktop */
.reveal > [data-beat=close]{margin-top:0}
.solo-lead .lead-l{max-width:32ch}
.b09{gap:24px} .b09 .t-small{max-width:40ch}
.b06{gap:0}
.l06 .t-head{max-width:22ch}
.l06 .sup{max-width:var(--col-read);margin-top:12px}
.l06 .sup p + p{margin-top:1em}
.l07 .essay{width:min(100%, var(--col-read));margin:0 auto} .l07 .essay p{line-height:1.6} .l07 .essay p + p{margin-top:1em}
.l07 .essay h3{margin:1em 0 .5em}
.l03{max-width:720px}
.l03 .row{display:flex;align-items:baseline;gap:20px;padding:16px 0;position:relative}
.l03 .row + .row{border-top:1px solid var(--line)}
.l03 .n{width:1.4em;flex-shrink:0}
.acc-mark{position:absolute;right:0;top:50%;transform:translateY(-50%);font:600 10px/1 ui-monospace,Menlo,monospace;border:1px dotted var(--ink);padding:2px 5px}
.l05{display:grid;grid-template-columns:repeat(12,1fr);gap:var(--gap);align-items:center}
.l05 .w-q{grid-column:span 5}
.l05 .def{grid-column:span 7;border-left:1px solid var(--line);padding-left:20px}
.l05 .def p{max-width:44ch}
.l05 .def p + p{margin-top:.8em}
.q-in{margin:.15em 0}
.reveal{display:grid;align-items:center;justify-items:center}
.reveal > *{grid-area:1 / 1}
.flowmode .reveal{display:flex;flex-direction:column;gap:10px}
.l04 .q{max-width:32ch}
.l08 .entries{display:grid;grid-template-columns:repeat(12,1fr);gap:var(--gap);margin-top:22px}
.l08 .entries:first-child{margin-top:0}
.entry{border-top:1px solid var(--line);padding-top:12px}
.s3{grid-column:span 3}.s4{grid-column:span 4}.s12{grid-column:span 12}
.price{display:grid;grid-template-columns:1fr 1fr;gap:var(--gap)}
.piece{background:var(--panel);border:1px solid var(--line);padding:24px;display:flex;flex-direction:column;gap:10px}
.price-after{margin-top:22px;max-width:64ch}
.guar{max-width:52ch;text-align:left;margin-bottom:22px}
.cta{display:flex;gap:16px;justify-content:center;width:100%}
.btn{flex:1 1 0;max-width:340px;min-height:56px;padding:0 24px;border-radius:999px;background:var(--btn);color:#fff;font-weight:600;font-size:var(--body);display:flex;align-items:center;justify-content:center;text-decoration:none;cursor:pointer;position:relative}
.btn:active{transform:scale(.97)}
.dlg{max-width:560px;display:flex;flex-direction:column;gap:12px}
.dlg-k{margin-top:-6px;margin-bottom:6px}
.msg{max-width:85%;padding:12px 16px;border-radius:18px}
.msg p{max-width:34ch}
.msg.ada{align-self:flex-start;background:#e2e2e2;border-bottom-left-radius:6px}
.msg.hijo{align-self:flex-end;background:#cbcbcb;border-bottom-right-radius:6px;text-align:left}
.who{display:block;margin-bottom:4px}
/* avatares como en la versión A: cuadrados de 34 px, radio 10, 9 px de la burbuja; el hijo a la derecha */
.msg-row{display:flex;align-items:flex-end;gap:9px;max-width:92%}
.msg-row.ada{align-self:flex-start}
.msg-row.hijo{align-self:flex-end;flex-direction:row-reverse}
.msg-row .msg{max-width:none;align-self:auto}
.avatar{width:52px;height:52px;border-radius:14px;overflow:hidden;flex:none;background:#d0d0d0} /* más grandes que en A (pedido del usuario) */
.avatar img{width:100%;height:100%;object-fit:cover;filter:grayscale(1)}
.stop.k-seal{padding:0}
.c-seal{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
.c-seq canvas{position:absolute;inset:0}
.c-seq .seq-poster{position:absolute;inset:0}
.c-seq.ready .seq-poster{visibility:hidden}
.flowmode .c-seq canvas{display:none}
.c-seal img,.c-seq canvas{width:100%;height:100%;object-fit:cover;filter:grayscale(1) contrast(.95)} /* sin viñeta: bordes limpios (decisión del usuario) */
picture{display:contents}
.c-seal[data-fit=contain] img{object-fit:contain} /* escena completa, sin recortar (04-shield) */
.vmiss{display:none}
@media (max-width:859px){ .vmiss{display:block;position:absolute;left:12px;right:12px;bottom:44px;z-index:5;font:500 11px/1.4 ui-monospace,Menlo,monospace;color:#1a1a1a;background:rgba(255,255,255,.94);border:1px dashed #444;padding:6px 8px;text-align:left} }
.nonotes .vmiss{display:none!important}
.img-missing{position:absolute;inset:12%;display:flex;align-items:center;justify-content:center;text-align:center;padding:16px;border:2px dashed #555;background:#e9e9e9;color:#222;font:500 12px/1.5 ui-monospace,Menlo,monospace;z-index:2}
.wf-file{position:absolute;bottom:10px;right:12px;font:500 10px/1.2 ui-monospace,Menlo,monospace;color:var(--chrome);background:rgba(255,255,255,.85);padding:2px 6px}
.stop.k-hero{padding:0}
.hero-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:grayscale(1);transform-origin:50% 45%}
.scrim{position:absolute;inset:0;background:linear-gradient(to top,rgba(16,16,16,.78) 0%,rgba(16,16,16,.35) 55%,rgba(16,16,16,.1) 100%)}
.hero-text{position:relative;z-index:2;color:var(--night-ink);padding:0 var(--padX);max-width:24ch}
@media (max-width:859px){
  .l05 .w-q,.l05 .def{grid-column:span 12}
  .l05 .def{border-left:0;border-top:1px solid var(--line);padding-left:0;padding-top:16px}
  .s3,.s4{grid-column:span 12}
  .l08 .entries{gap:14px}
  .price{grid-template-columns:1fr}
  .piece{padding:16px}
  .cta{flex-direction:column;align-items:stretch}
  .dlg{gap:10px} .msg{max-width:92%;padding:10px 14px} .who{margin-bottom:2px}
  .msg-row{max-width:100%;gap:8px} .avatar{width:34px;height:34px;border-radius:10px}
  .dlg{gap:8px} .msg{padding:8px 12px} .dlg-k{margin-bottom:2px}
  .btn{max-width:none}
  .c-seal img{height:auto;max-height:100%}
}

/* ===== Hero: configuración propia de desktop (no es la de móvil escalada) ===== */
@media (min-width:860px){
  .stop.k-hero{align-items:flex-end}
  .stop .hero-text{text-align:left;width:100%;max-width:1180px;margin:0 auto;padding:0 var(--padX) 10vh}
  .stop .hero-text h1{max-width:calc(1180px * 7 / 12)}
  .stop .scrim{background:linear-gradient(to top,rgba(16,16,16,.82) 0%,rgba(16,16,16,.5) 30%,rgba(16,16,16,0) 60%)}
}

/* ===== presentación de ADA: texto a la izquierda (7 col), ADA a la derecha (5 col) ===== */
.ada-intro{display:grid;grid-template-columns:repeat(12,1fr);gap:var(--gap);align-items:center}
.ada-text{grid-column:1 / span 7;display:flex;flex-direction:column;gap:12px;max-width:var(--col-read);justify-self:end}
.ada-fig{grid-column:8 / span 5;position:relative;justify-self:center;margin:0;height:min(70svh, 616px);aspect-ratio:400 / 616}
.ada-fig canvas,.ada-fig .ada-still{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;filter:grayscale(1)}
.ada-fig.ready .ada-still{visibility:hidden}
.flowmode .ada-fig canvas{display:none}
@media (max-width:859px){
  .ada-text,.ada-fig{grid-column:1 / -1}
  .ada-text{justify-self:stretch;max-width:none}
  .ada-fig{height:28svh} /* móvil/tablet: abajo del párrafo */
  .ada-fig canvas{display:none}
}

/* tablet vertical (600–859 px): el texto de la presentación de ADA no se estira a todo el ancho */
@media (min-width:600px) and (max-width:859px){
  .ada-text{max-width:var(--col-read);justify-self:center}
}

/* ===== indicador de continuar (triángulos que titilan en secuencia) ===== */
.cue{position:absolute;left:50%;bottom:calc(var(--padY) + 6px);transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;gap:5px;z-index:4;pointer-events:none}
.cue span{width:0;height:0;border-left:7px solid transparent;border-right:7px solid transparent;border-top:9px solid currentColor;opacity:.2;animation:cueBlink 1.8s ease-in-out infinite}
.cue span:nth-child(2){animation-delay:.25s} .cue span:nth-child(3){animation-delay:.5s}
@keyframes cueBlink{0%,100%{opacity:.2;transform:translateY(0)}40%{opacity:1;transform:translateY(3px)}}
.cue-path{gap:10px} /* camino: centrado a lo ancho, como los demás indicadores */
.stop.k-hero .cue{color:var(--night-ink)}
.flowmode .cue span{animation:none;opacity:.6}

/* ===== horizontal (cap. 02) ===== */
.t-h .track{display:flex;height:100%;width:calc(var(--n,4) * 100vw)}
.t-h .stop.panel{position:relative;flex:0 0 100vw;height:100%;inset:auto;pointer-events:auto}

/* ===== flujo (FAQ, footer) ===== */
.t-flow{padding:96px var(--padX);background:var(--bg)}
.faq{max-width:760px;margin:0 auto}
.faq h2{margin-bottom:24px}
.faq details{border-top:1px solid var(--line)}
.faq details:last-child{border-bottom:1px solid var(--line)}
.faq summary{list-style:none;display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:56px;padding:12px 0;cursor:pointer}
.faq summary::-webkit-details-marker{display:none}
.faq details p{padding:0 48px 20px 0;max-width:64ch}
.ind{width:32px;height:32px;border:1.5px solid var(--btn);border-radius:999px;flex-shrink:0;position:relative}
.ind::before{content:"";position:absolute;left:50%;top:44%;width:8px;height:8px;border-right:1.5px solid var(--btn);border-bottom:1.5px solid var(--btn);transform:translate(-50%,-50%) rotate(45deg)}
.faq details[open] .ind::before{top:58%;transform:translate(-50%,-50%) rotate(-135deg)}
.faq summary:active .ind{transform:scale(.92)}
.foot{max-width:1180px;margin:0 auto;display:flex;flex-direction:column;gap:6px}
.logo-ph{border:1px dashed var(--chrome);align-self:flex-start;padding:4px 10px;margin-bottom:10px}
.foot-links{margin-top:14px}

/* ===== modo reducido / sin GSAP ===== */
.flowmode .stage{height:auto;overflow:visible}
.flowmode .stop{position:relative;inset:auto;min-height:100svh;opacity:0;transition:opacity .2s ease;pointer-events:auto}
.flowmode .stop.inview{opacity:1}
.flowmode .stop.nightc{background:var(--night)}
.flowmode .night{display:none}
.flowmode .t-h .track{display:block;width:auto}
.flowmode .t-h .stop.panel{flex:none;height:auto;min-height:100svh}
.flowmode .c-seal{position:relative;inset:auto;min-height:100svh}

/* ===== chrome del wireframe (no es UI) ===== */
.tag{position:absolute;top:8px;left:8px;z-index:6;font:500 10px/1.35 ui-monospace,Menlo,monospace;color:var(--chrome);background:rgba(255,255,255,.92);border:1px solid #c9c9c9;padding:2px 6px;max-width:calc(100% - 16px);pointer-events:none;text-align:left}
.nightc .tag{background:rgba(0,0,0,.65);color:#bdbdbd;border-color:#444}
.tag .fill{margin-left:4px}
.tag .fill.tight{font-weight:700}
.tag .fill.over{background:#000;color:#fff;padding:0 4px;font-weight:700}
.btn::after{content:attr(data-role);position:absolute;top:-16px;left:50%;transform:translateX(-50%);font:500 9px/1 ui-monospace,Menlo,monospace;color:var(--chrome);white-space:nowrap}
.nonotes .tag,.nonotes .btn::after,.nonotes .wf-file,.nonotes .acc-mark::after{display:none}
.t-flow .tag{position:relative;top:auto;left:auto;display:inline-block;margin-bottom:16px}
#hud{position:fixed;left:10px;bottom:10px;z-index:60;width:min(440px,calc(100vw - 44px));font:500 11px/1.45 ui-monospace,Menlo,monospace;color:#1a1a1a;background:rgba(255,255,255,.96);border:1px solid #bdbdbd;box-shadow:0 2px 10px rgba(0,0,0,.12);padding:8px 10px}
#hud b{font-weight:700}
#hud .row{display:flex;gap:8px;flex-wrap:wrap}
#hud .note{margin-top:4px;color:#333;font-family:Inter,system-ui,sans-serif;font-size:12px;line-height:1.4}
#hud .btns{display:flex;gap:6px;flex-wrap:wrap;margin-top:6px}
#hud button{font:600 10px/1 ui-monospace,Menlo,monospace;background:#fff;border:1px solid #9a9a9a;padding:5px 7px;cursor:pointer;color:#1a1a1a}
#hud button:active{transform:scale(.96)}
#hud .warn{margin-top:6px;padding:5px 6px;background:#ececec;border-left:3px solid #333;font-family:Inter,system-ui,sans-serif;font-size:11px}
#hud.collapsed .more{display:none}
#legend{display:none;margin-top:6px;border-top:1px solid #ddd;padding-top:6px;font-family:Inter,system-ui,sans-serif;font-size:11px;line-height:1.45}
#hud.showlegend #legend{display:block}
#ruler{position:fixed;right:6px;top:6vh;height:88vh;width:14px;z-index:55;background:#fff;border:1px solid #bdbdbd}
#ruler .seg{position:absolute;left:0;right:0}
.s-read,.s-lead,.s-cta,.s-panel,.s-dialog{background:#cfcfcf}
.s-golpe,.s-two,.s-reveal,.s-hero{background:#7d7d7d}
.s-night{background:#111}
.s-seal,.s-seq{background:repeating-linear-gradient(45deg,#9b9b9b 0 2px,#e4e4e4 2px 5px)}
.s-transit{background:#fff}
.s-flow{background:#ececec}
#ruler .tick{position:absolute;left:-5px;width:22px;height:9px;margin-top:-4px;padding:0;border:0;background:transparent;cursor:pointer}
#ruler .tick::after{content:"";position:absolute;left:3px;right:3px;top:4px;height:1px;background:#000}
#ruler .tick:hover::after{height:3px;top:3px}
#cursor{position:absolute;left:-8px;right:-8px;height:2px;background:#000;pointer-events:none}
#cursor::before{content:"";position:absolute;left:-2px;top:-4px;border:5px solid transparent;border-left-color:#000}
@media (max-width:859px){ #ruler{width:9px;right:3px} #hud{font-size:10px} }
</style>
</head>
<body>
<main id="wf"></main>
<aside id="ruler" aria-label="Escala del recorrido"></aside>
<aside id="hud" aria-live="polite">
  <div class="row"><b>WIREFRAME · Fase 2</b><span>grises · copy literal · no es el build</span><button id="bCollapse" style="margin-left:auto">–</button></div>
  <div class="row"><span>Parada <b id="hStop">—</b></span><span id="hComp"></span><span id="hE"></span></div>
  <div class="more">
    <div class="row"><span id="hPin"></span></div>
    <div class="row"><span>Recorrido: E <b id="hPos">0</b> / <b id="totE">—</b></span><span id="hVp"></span></div>
    <div class="note" id="hNote"></div>
    <div id="hWarn"></div>
    <div class="btns"><button id="bNotes">Notas: sí</button><button id="bMode">Ver modo reducido</button><button id="bLegend">Leyenda</button></div>
    <div id="legend">
      <b>E</b> = un encuadre de scroll (100svh; 16:8.6 en desktop, 9:15.3 en móvil). Cada parada está estacionada su E; el snap la deja quieta en su punto.<br>
      <b>Regla derecha</b> = escala del recorrido completo, a proporción: gris claro lectura · gris medio golpe · negro escenario oscuro · rayado escena · blanco tránsito entre pines (1 E) · gris muy claro flujo (FAQ/footer). Cada raya es un punto de snap: clic para ir.<br>
      <b>Etiqueta</b> de parada: id · composición · E · ★ = escaneo de 3 s · % = ocupación del encuadre a tu tamaño de pantalla (<b>negro = desborda</b>).<br>
      <b>Subrayado punteado</b> = acento de color en el build. Botones grises = par de CTA (azul / violeta en el build).<br>
      Cambia el ancho de la ventana: por debajo de 860 px se usa la escala y el encuadre móvil.
    </div>
  </div>
</aside>
<script type="application/json" id="wf-data">/*__DATA__*/</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollToPlugin.min.js"></script>
<script>
(function(){
"use strict";
var DATA = JSON.parse(document.getElementById('wf-data').textContent);
var root = document.getElementById('wf');
var LS = { get:function(k){ try{ return localStorage.getItem(k); }catch(e){ return null; } },
           set:function(k,v){ try{ localStorage.setItem(k,v); }catch(e){} } };
var hasGsap = typeof window.gsap !== 'undefined' && typeof window.ScrollTrigger !== 'undefined';
var mode = LS.get('wf-mode') || 'full';
if(!hasGsap) mode = 'flow';
var notes = LS.get('wf-notes') !== 'off';
if(!notes) document.body.classList.add('nonotes');
var STOPS = [], POS = [], isD = window.innerWidth >= 860;

function fmtE(e){ return (Math.round(e*100)/100).toString(); }
function tagHtml(s){ return '<div class="tag"><b>'+s.id+'</b> · '+s.comp+(s.E!=null?' · '+fmtE(s.E)+' E':'')+(s.scan?' · ★':'')+(s.night?' · oscuro':'')+'<span class="fill"></span></div>'; }

// ---------- render ----------
DATA.pins.forEach(function(pin){
  var sec = document.createElement('section');
  sec.className = 'pin t-' + pin.type; sec.id = pin.id;
  if(pin.type === 'flow'){
    sec.innerHTML = tagHtml({id:pin.id, comp:pin.comp, E:null}) + pin.html;
    root.appendChild(sec);
    STOPS.push({id:pin.id, el:sec, pin:pin, s:{id:pin.id, comp:pin.comp, note:pin.note, kind:'flow', bp:'all'}, flow:true});
    return;
  }
  var stage = document.createElement('div'); stage.className = 'stage';
  var box = stage;
  if(pin.type === 'h'){ var tr = document.createElement('div'); tr.className = 'track'; stage.appendChild(tr); box = tr; }
  else { var nl = document.createElement('div'); nl.className = 'night'; stage.appendChild(nl); }
  pin.stops.forEach(function(s){
    var el = document.createElement('div');
    el.className = 'stop k-'+s.kind+(s.night?' nightc':'')+(s.bp==='d'?' only-d':'')+(s.bp==='m'?' only-m':'')+(pin.type==='h'?' panel':'');
    el.setAttribute('data-id', s.id);
    el.innerHTML = s.html + tagHtml(s);
    box.appendChild(el);
    STOPS.push({id:s.id, el:el, pin:pin, s:s});
  });
  sec.appendChild(stage); root.appendChild(sec);
});
// ---------- imágenes: si no cargan, aviso visible con la ruta (no se esconde el problema) ----------
Array.prototype.forEach.call(document.querySelectorAll('#wf img'), function(img){
  function missing(){
    if(img.dataset.missing) return; img.dataset.missing = '1';
    var box = document.createElement('div'); box.className = 'img-missing';
    box.textContent = 'No se pudo cargar: ' + img.getAttribute('src') + ' · Abre 02-wireframe.html desde su carpeta del proyecto (Chrome o Safari); una vista previa que solo recibe el HTML no ve la carpeta 00-context/scenes/.';
    img.insertAdjacentElement('afterend', box);
  }
  img.addEventListener('error', missing);
  if(img.complete && img.naturalWidth === 0 && img.getAttribute('src')) missing();
});
function rec(s){ for(var i=0;i<STOPS.length;i++){ if(STOPS[i].s===s) return STOPS[i]; } }
function visible(s){ return !s.bp || s.bp==='all' || (isD ? s.bp==='d' : s.bp==='m'); }

// ---------- HUD ----------
var hud = document.getElementById('hud');
function $(id){ return document.getElementById(id); }
if(window.innerWidth < 860) hud.classList.add('collapsed');
$('bCollapse').onclick = function(){ hud.classList.toggle('collapsed'); this.textContent = hud.classList.contains('collapsed') ? '+' : '–'; };
$('bCollapse').textContent = hud.classList.contains('collapsed') ? '+' : '–';
$('bNotes').textContent = 'Notas: ' + (notes ? 'sí' : 'no');
$('bNotes').onclick = function(){ notes = !notes; document.body.classList.toggle('nonotes', !notes); LS.set('wf-notes', notes ? 'on' : 'off'); this.textContent = 'Notas: ' + (notes ? 'sí' : 'no'); };
$('bMode').textContent = mode === 'full' ? 'Ver modo reducido' : 'Ver recorrido con pines';
$('bMode').onclick = function(){ if(!hasGsap) return; LS.set('wf-mode', mode === 'full' ? 'flow' : 'full'); location.reload(); };
$('bLegend').onclick = function(){ hud.classList.toggle('showlegend'); };
var warn = '';
if(!hasGsap) warn = 'GSAP no cargó (sin conexión o bloqueado): se muestra el modo reducido, sin pines. Ábrelo en un navegador con internet para ver el recorrido.';
else if(mode === 'full' && window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) warn = 'Tu sistema tiene «reducir movimiento» activado. Este wireframe lo ignora para mostrarte los pines; la landing real sí lo respeta (botón «Ver modo reducido»).';
else if(mode === 'flow') warn = 'Modo reducido: sin pines ni scrub; cada encuadre es un bloque en flujo con fundido corto. Así lo verá quien tenga «reducir movimiento».';
if(warn) $('hWarn').innerHTML = '<div class="warn">'+warn+'</div>';
function vpText(){ var w = innerWidth, h = innerHeight; return w+'×'+h+' · '+(w>=860?'desktop (16:8.6 = 1.86)':'móvil (9:15.3 = 0.59)')+' · actual '+(w/h).toFixed(2); }

var current = null;
function setActive(p, y){
  $('hPos').textContent = (y/innerHeight).toFixed(1);
  $('hVp').textContent = vpText();
  if(!p){ return; }
  var key = p.kind === 'transit' ? 't:'+p.pin.id : p.id;
  if(current === key) return; current = key;
  STOPS.forEach(function(x){ x.el.classList.remove('is-active'); });
  if(p.kind === 'transit'){
    $('hStop').textContent = 'tránsito'; $('hComp').textContent = '→ '+p.pin.id; $('hE').textContent = '1 E';
    $('hPin').textContent = 'Entre pines: la siguiente escala sube a pantalla (scroll normal, 1 E).';
    $('hNote').textContent = ''; return;
  }
  var x = p.x; if(x && x.el) x.el.classList.add('is-active');
  var s = x ? x.s : {};
  $('hStop').textContent = p.id; $('hComp').textContent = s.comp || ''; $('hE').textContent = s.E!=null ? fmtE(s.E)+' E' : 'flujo';
  var pin = p.pin, vis = pin.stops ? pin.stops.filter(visible) : [];
  var tot = vis.reduce(function(a,b){ return a+b.E; },0);
  $('hPin').textContent = pin.type==='flow' ? pin.cap+' · flujo normal (no pineado)' : 'Pin '+pin.id+' · '+pin.cap+' · '+vis.length+' parada(s) · '+fmtE(tot)+' E';
  $('hNote').textContent = s.note || '';
}

// ---------- ocupación del encuadre ----------
function measureFills(){
  STOPS.forEach(function(x){
    var f = x.el.querySelector(':scope > .tag .fill'); if(!f) return;
    if(x.flow || x.s.kind==='seal' || x.s.kind==='seq' || x.s.kind==='hero'){ f.textContent=''; return; }
    var c = x.el.querySelector(':scope > .c'); if(!c || !x.el.offsetParent && getComputedStyle(x.el).display==='none'){ f.textContent=''; return; }
    var cs = getComputedStyle(x.el);
    var inner = (mode==='full' ? x.el.clientHeight : innerHeight) - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom);
    if(inner <= 0 || !c.offsetHeight){ f.textContent=''; return; }
    var r = c.offsetHeight / inner;
    f.textContent = Math.round(r*100)+' %';
    f.className = 'fill' + (r > 1 ? ' over' : (r > .85 ? ' tight' : ''));
  });
}

// ---------- regla ----------
function maxScroll(){ return Math.max(1, (hasGsap && mode==='full') ? ScrollTrigger.maxScroll(window) : (document.documentElement.scrollHeight - innerHeight)); }
function drawRuler(){
  var r = $('ruler'); r.innerHTML = '';
  var max = maxScroll();
  function pct(v){ return (Math.max(0, Math.min(max, v)) / max * 100); }
  POS.forEach(function(p){
    if(p.kind === 'label'){
      var t = document.createElement('button'); t.className = 'tick'; t.style.top = pct(p.at)+'%'; t.title = p.id;
      t.setAttribute('aria-label', 'Ir a '+p.id); t.onclick = function(){ scrollToY(p.at); }; r.appendChild(t); return;
    }
    var seg = document.createElement('div');
    seg.className = 'seg s-'+(p.night ? 'night' : p.kind);
    seg.style.top = pct(p.from)+'%'; seg.style.height = Math.max(0.15, pct(p.to)-pct(p.from))+'%';
    r.appendChild(seg);
  });
  var cur = document.createElement('div'); cur.id = 'cursor'; r.appendChild(cur);
  $('totE').textContent = (max/innerHeight + 1).toFixed(1);
  onScroll();
}
function scrollToY(y){
  if(hasGsap && window.ScrollToPlugin){ gsap.to(window, {scrollTo:{y:y, autoKill:true}, duration:0.9, ease:'power2.inOut'}); }
  else window.scrollTo({top:y, behavior:'smooth'});
}
function goTo(id){
  for(var i=0;i<POS.length;i++){ if(POS[i].kind==='label' && POS[i].id===id){ scrollToY(POS[i].at); return; } }
  for(var j=0;j<POS.length;j++){ if(POS[j].id===id && POS[j].from!=null){ scrollToY(POS[j].from); return; } }
}
document.addEventListener('click', function(e){ var a = e.target.closest('[data-goto]'); if(a){ e.preventDefault(); goTo(a.getAttribute('data-goto')); } });
var ticking = false;
function onScroll(){
  if(ticking) return; ticking = true;
  requestAnimationFrame(function(){
    ticking = false;
    var y = window.scrollY, max = maxScroll();
    var cur = $('cursor'); if(cur) cur.style.top = (Math.min(max, y)/max*100)+'%';
    var probe = y + 1, hit = null;
    for(var i=0;i<POS.length;i++){ var p = POS[i]; if(p.kind==='label') continue; if(probe >= p.from && probe < p.to){ if(!hit || hit.kind==='transit') hit = p; } }
    setActive(hit, y);
  });
}
window.addEventListener('scroll', onScroll, {passive:true});

// ---------- modo recorrido (GSAP) ----------
function buildPin(sec, vis, pin){
  var total = vis.reduce(function(a,x){ return a + x.s.E; }, 0);
  var night = sec.querySelector('.night');
  vis.forEach(function(x){ gsap.set(x.el, {opacity:0}); });
  gsap.set(night, {opacity:0});
  var tl = gsap.timeline({ defaults:{ease:'none'}, scrollTrigger:{
    id:pin.id, trigger:sec, pin:true, start:'top top',
    end:function(){ return '+=' + (total * window.innerHeight); },
    scrub:0.4, invalidateOnRefresh:true,
    snap:{ snapTo:'labels', duration:{min:0.2, max:0.5}, delay:0.08, ease:'power1.inOut' }
  }});
  tl.to({}, {duration:total}, 0);
  var labels = [], t = 0;
  vis.forEach(function(x, i){
    var s = x.s, el = x.el, span = s.E, first = i===0, last = i===vis.length-1;
    var c = el.querySelector(':scope > .c') || el;
    var prevN = i>0 && vis[i-1].s.night, nextN = !last && vis[i+1].s.night;
    var dIn = span * (s.kind==='golpe' ? 0.10 : 0.15);
    if(first){ gsap.set(el, {opacity:1}); if(s.night) gsap.set(night, {opacity:1}); }
    else {
      tl.fromTo(el, {opacity:0}, {opacity:1, duration:dIn}, t);
      if(s.kind==='read' || s.kind==='cta' || s.kind==='dialog') tl.fromTo(c, {y:24}, {y:0, duration:dIn, ease:'power2.out'}, t);
      if(s.kind==='lead' || s.kind==='two' || s.kind==='reveal'){ var ld = el.querySelector('[data-beat=lead]') || c; tl.fromTo(ld, {x:-16}, {x:0, duration:dIn, ease:'power2.out'}, t); }
      if(s.night && !prevN) tl.to(night, {opacity:1, duration:span*0.10}, t);
    }
    var holdStart = t + (first ? 0 : dIn), holdEnd = t + span*0.85, lt;
    if(s.kind==='two'){
      var cl = el.querySelector('[data-beat=close]');
      gsap.set(cl, {opacity:0});
      tl.to(cl, {opacity:1, duration:span*0.10}, t + span*0.30);
      var la = first ? t : t + span*0.20;
      tl.addLabel(s.id+'·a', la); labels.push([s.id+' (puente)', la, x]);
      holdStart = t + span*0.40;
    }
    if(el.querySelector('[data-seq]')) buildSeq(el, tl, t, span);
    if(s.kind==='reveal'){ /* revelación en tres tiempos: puente → se desvanece → paso 1 → paso 2 */
      var rl = el.querySelector('[data-beat=lead]'), steps = el.querySelectorAll('[data-step]');
      if(rl){ /* con puente: puente → se desvanece → paso 1 → paso 2 (01.3) */
        Array.prototype.forEach.call(steps, function(st){ gsap.set(st, {opacity:0}); });
        var la1 = first ? t : t + span*0.18;
        tl.addLabel(s.id+'·a', la1); labels.push([s.id+' (puente)', la1, x]);
        tl.to(rl, {opacity:0, duration:span*0.08}, t + span*0.26);
        if(steps[0]){ tl.to(steps[0], {opacity:1, duration:span*0.05}, t + span*0.36); tl.addLabel(s.id+'·b', t + span*0.46); labels.push([s.id+' (paso 1)', t + span*0.46, x]); }
        if(steps[1]){ tl.to(steps[1], {opacity:1, duration:span*0.05}, t + span*0.54); }
        holdStart = t + span*0.60;
      } else { /* golpe en dos alturas sin puente: paso 1 entra con la parada → paso 2 (05.4) */
        if(steps[1]){ gsap.set(steps[1], {opacity:0}); tl.to(steps[1], {opacity:1, duration:span*0.05}, t + span*0.36); }
        var lb = first ? t : t + span*0.2;
        tl.addLabel(s.id+'·a', lb); labels.push([s.id+' (paso 1)', lb, x]);
        holdStart = t + span*0.45;
      }
    }
    if(s.kind==='dialog'){
      var msgs = el.querySelectorAll('.msg-row'); if(!msgs.length) msgs = el.querySelectorAll('.msg'); /* el avatar entra con su burbuja */
      Array.prototype.forEach.call(msgs, function(m, k){
        var at = t + span*(0.12 + k*0.18);
        tl.fromTo(m, {opacity:0, x:(m.classList.contains('hijo') ? 16 : -16)}, {opacity:1, x:0, duration:span*0.08, ease:'power2.out'}, at);
        tl.addLabel(s.id+'·'+(k+1), at + span*0.09); labels.push([s.id+' · mensaje '+(k+1), at + span*0.09, x]);
      });
    }
    if(s.kind==='seal'){ /* zoom-out con scroll; data-zoom = escala inicial (por defecto 1.06) */
      var img = el.querySelector('img'), fig = el.querySelector('[data-zoom]');
      var z = fig ? parseFloat(fig.getAttribute('data-zoom')) : 1.06;
      var zin = fig && fig.getAttribute('data-zoom-dir') === 'in';
      if(img){
        if(fig && fig.getAttribute('data-origin')) gsap.set(img, {transformOrigin:fig.getAttribute('data-origin')});
        tl.fromTo(img, {scale:(zin ? 1 : z)}, {scale:(zin ? z : 1), duration:span*0.7, ease:(z > 1.2 ? (zin ? 'power1.in' : 'power1.out') : 'none')}, t);
      }
    }
    Array.prototype.forEach.call(el.querySelectorAll('[data-at=exit]'), function(m){ gsap.set(m, {opacity:0}); tl.to(m, {opacity:1, duration:span*0.08}, t + span*0.78); });
    if(s.kind!=='dialog'){
      lt = (s.kind==='seal' || s.kind==='seq') ? t + span*0.78 : ((first && s.kind!=='two' && s.kind!=='reveal') ? t : (holdStart + holdEnd)/2); /* escena: se estaciona cuando terminó el zoom-out */
      tl.addLabel(s.id, lt); labels.push([s.id, lt, x]);
    }
    if(!last){
      var outAt = t + span*(s.kind==='golpe' ? 0.92 : 0.85), outD = span*(s.kind==='golpe' ? 0.08 : 0.15);
      tl.to(el, {opacity:0, duration:outD}, outAt);
      if(s.night && !nextN) tl.to(night, {opacity:0, duration:span*0.15}, t + span*0.85);
    }
    t += span;
  });
  tl.addLabel('fin', total);
  sec._wf = {total:total, labels:labels, vis:vis};
}
/* ---- scrub de video como secuencia de cuadros en canvas ---- */
function drawCover(ctx, im, cw, ch){
  var ir = im.naturalWidth / im.naturalHeight, cr = cw / ch, w, h, x, y;
  if(ir > cr){ h = ch; w = h * ir; x = (cw - w) / 2; y = 0; } else { w = cw; h = w / ir; x = 0; y = (ch - h) / 2; }
  ctx.drawImage(im, x, y, w, h);
}
function drawContain(ctx, im, cw, ch){
  var s = Math.min(cw / im.naturalWidth, ch / im.naturalHeight), w = im.naturalWidth * s, h = im.naturalHeight * s;
  ctx.drawImage(im, (cw - w) / 2, (ch - h) / 2, w, h);
}
function buildSeq(el, tl, t, span){
  var fig = el.querySelector('[data-seq]'); if(!fig) return;
  if(!isD && fig.getAttribute('data-mobile') === 'still') return; /* móvil/tablet: cuadro fijo, sin descargar la secuencia (como en A) */
  var cv = fig.querySelector('canvas'), ctx = cv.getContext('2d');
  var n = +fig.getAttribute('data-n'), base = fig.getAttribute('data-seq');
  var start = +(fig.getAttribute('data-start') || 1), contain = fig.getAttribute('data-fit') === 'contain';
  var dur = parseFloat(fig.getAttribute('data-span') || 0.7);
  var imgs = [], state = {f:0};
  function ok(im){ return im && im.complete && im.naturalWidth; }
  function draw(){
    var i = Math.max(0, Math.min(n - 1, Math.round(state.f))), im = imgs[i];
    while(i > 0 && !ok(im)){ i--; im = imgs[i]; }
    if(!ok(im)) return;
    ctx.clearRect(0, 0, cv.width, cv.height); (contain ? drawContain : drawCover)(ctx, im, cv.width, cv.height);
  }
  function size(){
    var r = Math.min(window.devicePixelRatio || 1, 2);
    cv.width = Math.max(1, Math.round(cv.clientWidth * r)); cv.height = Math.max(1, Math.round(cv.clientHeight * r)); draw();
  }
  for(var k = 1; k <= n; k++){ (function(k){
    var im = new Image(); im.decoding = 'async';
    im.onload = function(){ if(k === 1){ fig.classList.add('ready'); size(); } else if(Math.round(state.f) === k - 1) draw(); };
    im.src = base + '/f' + ('00' + (start + k - 1)).slice(-3) + '.webp'; imgs.push(im);
  })(k); }
  if(fig._seqSize) window.removeEventListener('resize', fig._seqSize);
  fig._seqSize = size; window.addEventListener('resize', size);
  if(fig.getAttribute('data-play') === 'time'){ /* gesto de un solo uso: en tiempo real al entrar, se repite al regresar (no scrub) */
    var fps = +(fig.getAttribute('data-fps') || 24);
    var play = gsap.fromTo(state, {f:0}, {f:n - 1, duration:(n - 1) / fps, ease:'none', paused:true, onUpdate:draw});
    ScrollTrigger.create({ trigger:el.closest('.pin'), start:'top 60%',
      onEnter:function(){ play.restart(); }, onEnterBack:function(){ play.restart(); } });
    return;
  }
  tl.fromTo(state, {f:0}, {f:n - 1, duration:span * dur, ease:'none', onUpdate:draw}, t);
}
function buildH(sec, vis, pin){
  /* Carrusel horizontal: cada panel LLEGA y se ESTACIONA (70 % de su E) y solo después se desplaza (30 %).
     Snap a la mitad de cada estacionamiento, sin inercia: si el usuario deja de scrollear, el panel se queda. */
  var track = sec.querySelector('.track'), n = vis.length;
  track.style.setProperty('--n', n);
  vis.forEach(function(x){ gsap.set(x.el, {opacity:1}); });
  var total = vis.reduce(function(a,x){ return a + x.s.E; }, 0);
  var tl = gsap.timeline({ defaults:{ease:'none'}, scrollTrigger:{
    id:pin.id, trigger:sec, pin:true, start:'top top',
    end:function(){ return '+=' + (total * window.innerHeight); },
    scrub:0.4, invalidateOnRefresh:true,
    snap:{ snapTo:'labels', duration:{min:0.3, max:0.6}, delay:0.15, ease:'power1.inOut', inertia:false }
  }});
  tl.to({}, {duration:total}, 0);
  var labels = [], t = 0;
  vis.forEach(function(x, i){
    var last = i === n - 1, hold = last ? x.s.E : x.s.E * 0.7, move = x.s.E - hold;
    var lt = t + hold / 2;
    tl.addLabel(x.s.id, lt); labels.push([x.s.id, lt, x]);
    if(!last){
      tl.to(track, { x:function(){ return -(i + 1) * window.innerWidth; }, duration:move, ease:'power2.inOut' }, t + hold);
    }
    t += x.s.E;
  });
  tl.addLabel('fin', total);
  sec._wf = {total:total, labels:labels, vis:vis};
}
function buildHero(sec, vis, pin){
  var x = vis[0], el = x.el; gsap.set(el, {opacity:1});
  var img = el.querySelector('.hero-img'), scrim = el.querySelector('.scrim'), txt = el.querySelector('.hero-text');
  var tl = gsap.timeline({paused:true});
  tl.fromTo(img, {scale:2.6}, {scale:1, duration:3.7, ease:'power2.inOut'})
    .to({}, {duration:0.6})
    .fromTo(scrim, {opacity:0}, {opacity:1, duration:0.5})
    .fromTo(txt, {opacity:0}, {opacity:1, duration:0.5});
  var cue = el.querySelector('.cue'); if(cue) tl.fromTo(cue, {opacity:0}, {opacity:1, duration:0.4});
  ScrollTrigger.create({ id:pin.id, trigger:sec, pin:true, start:'top top',
    end:function(){ return '+=' + (x.s.E * window.innerHeight); },
    onEnterBack:function(){ tl.restart(); } });
  tl.restart();
  sec._wf = {total:x.s.E, labels:[[x.s.id, 0, x]], vis:vis};
}
function computePositions(){
  POS = [];
  var H = window.innerHeight;
  DATA.pins.forEach(function(pin){
    var sec = document.getElementById(pin.id);
    if(pin.type === 'flow'){
      var top = sec.getBoundingClientRect().top + window.scrollY;
      var x = STOPS.filter(function(z){ return z.id===pin.id; })[0];
      POS.push({kind:'flow', id:pin.id, from:top, to:top+sec.offsetHeight, x:x, pin:pin});
      POS.push({kind:'label', id:pin.id, at:top, x:x, pin:pin});
      return;
    }
    var st = ScrollTrigger.getById(pin.id); if(!st || !sec._wf) return;
    var w = sec._wf, len = st.end - st.start, t = 0;
    if(st.start > 0) POS.push({kind:'transit', from:Math.max(0, st.start - H), to:st.start, pin:pin});
    w.vis.forEach(function(x){
      POS.push({kind:x.s.kind, night:x.s.night, id:x.s.id, from:st.start + t/w.total*len, to:st.start + (t + x.s.E)/w.total*len, x:x, pin:pin});
      t += x.s.E;
    });
    w.labels.forEach(function(l){ POS.push({kind:'label', id:l[0].split(' ')[0], at:st.start + l[1]/w.total*len, x:l[2], pin:pin}); });
  });
  drawRuler();
}
function computeFlowPositions(){
  POS = [];
  STOPS.forEach(function(x){
    if(!x.flow && !visible(x.s)) return;
    var el = x.el; if(!el.offsetHeight) return;
    var top = el.getBoundingClientRect().top + window.scrollY;
    POS.push({kind:x.flow ? 'flow' : x.s.kind, night:x.s.night, id:x.id, from:top, to:top + el.offsetHeight, x:x, pin:x.pin});
    POS.push({kind:'label', id:x.id, at:top, x:x, pin:x.pin});
  });
  drawRuler();
}

if(mode === 'full'){
  document.body.classList.add('fullmode');
  gsap.registerPlugin(ScrollTrigger);
  if(window.ScrollToPlugin) gsap.registerPlugin(ScrollToPlugin);
  ScrollTrigger.addEventListener('refresh', function(){ computePositions(); measureFills(); });
  var mm = gsap.matchMedia();
  mm.add({ isD:'(min-width: 860px)', isM:'(max-width: 859px)' }, function(ctx){
    isD = !!ctx.conditions.isD;
    DATA.pins.forEach(function(pin){
      if(pin.type === 'flow') return;
      var sec = document.getElementById(pin.id);
      var vis = pin.stops.filter(visible).map(rec);
      if(pin.type === 'hero') buildHero(sec, vis, pin);
      else if(pin.type === 'h') buildH(sec, vis, pin);
      else buildPin(sec, vis, pin);
    });
    ScrollTrigger.refresh();
    return function(){ POS = []; current = null; };
  });
  if(document.fonts && document.fonts.ready) document.fonts.ready.then(function(){ ScrollTrigger.refresh(); });
  window.addEventListener('load', function(){ ScrollTrigger.refresh(); });
} else {
  document.body.classList.add('flowmode');
  var io = ('IntersectionObserver' in window) ? new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting) e.target.classList.add('inview'); }); }, {threshold:0.15}) : null;
  STOPS.forEach(function(x){ if(x.flow) return; if(io) io.observe(x.el); else x.el.classList.add('inview'); });
  function refreshFlow(){ isD = window.innerWidth >= 860; computeFlowPositions(); measureFills(); }
  requestAnimationFrame(refreshFlow);
  if(document.fonts && document.fonts.ready) document.fonts.ready.then(refreshFlow);
  window.addEventListener('load', refreshFlow);
  window.addEventListener('resize', function(){ clearTimeout(window._rf); window._rf = setTimeout(refreshFlow, 200); });
}
})();
</script>
</body>
</html>
"""

# ------------------------------------------------------------------ texto de las paradas
class TextOf(HTMLParser):
    def __init__(self):
        super().__init__(); self.out = []; self.skip = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if any(k in (a.get('class') or '') for k in ('wf-file', 'acc-mark', 'vmiss')):
            self.skip += 1
    def handle_endtag(self, tag):
        if self.skip and tag in ('figcaption', 'span'):
            self.skip -= 1
    def handle_data(self, d):
        if not self.skip: self.out.append(d)
def text_of(h):
    p = TextOf(); p.feed(h); return re.sub(r'\s+', ' ', html.unescape(''.join(p.out))).strip()

def stream(bp):
    parts = []
    for pin in C.PINS:
        if pin['type'] == 'flow':
            parts.append(text_of(pin['html'])); continue
        for s in pin['stops']:
            if s['bp'] in ('all', bp):
                parts.append(text_of(s['html']))
    return ' '.join(parts)

# ------------------------------------------------------------------ segmentos de la fuente
def source_segments():
    raw = open(os.path.join(ROOT, '00-context', 'COPY-PUBLICADO.md'), encoding='utf-8').read()
    body, notes = raw.split('\n---\n', 1)
    segs, internals = [], ['Etiqueta de sección «## Footer» (no aparece en el sitio de referencia).',
                           'Etiqueta «(FAQ)» del encabezado «Por si te quedó una duda. (FAQ)» (no aparece en el sitio de referencia).',
                           'Nota de procedencia al final del archivo: ' + re.sub(r'\s+', ' ', notes.strip())]
    for line in body.split('\n'):
        l = line.strip()
        if not l or l == '## Footer': continue
        if l.startswith('## '):
            l = l[3:]
            if l.endswith(' (FAQ)'): l = l[:-6]
        if l.startswith('- '): l = l[2:]
        l = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', l)
        if l.startswith('**Una pregunta que abre otra puerta**'):
            segs += ['Una pregunta que abre otra puerta', '— Conversación de ejemplo']; continue
        l = l.replace('**', '')
        m = re.match(r'^(ADA|HIJO): (.+)$', l)
        if m:
            segs += [m.group(1), m.group(2)]; continue
        if l == 'Inscribir a mi hijo ↗ · Conversar con ADA primero':
            segs += ['Inscribir a mi hijo ↗', 'Conversar con ADA primero']; continue
        segs.append(re.sub(r'\s+', ' ', l))
    return segs, internals

def audit(bp):
    txt = stream(bp); segs, _ = source_segments()
    pos, missing = 0, []
    for sgm in segs:
        i = txt.find(sgm, pos)
        if i < 0:
            j = txt.find(sgm)
            missing.append((sgm, 'fuera de orden' if j >= 0 else 'FALTA'))
        else:
            pos = i + len(sgm)
    return len(segs), missing

# ------------------------------------------------------------------ estimador de ocupación (móvil 360×612)
from PIL import ImageFont
FD = os.path.expanduser('~/Library/Fonts/')
_fc = {}
def font(fam, px, w, ital=False):
    k = (fam, px, w, ital)
    if k in _fc: return _fc[k]
    f = 'PlayfairDisplay-Italic-VariableFont_wght.ttf' if (fam == 'pf' and ital) else ('PlayfairDisplay-VariableFont_wght.ttf' if fam == 'pf' else 'Inter-VariableFont_slnt,wght.ttf')
    F = ImageFont.truetype(FD + f, px); vals = []
    for a in F.get_variation_axes():
        n = a.get('name', b''); n = n.decode() if isinstance(n, bytes) else str(n)
        vals.append(w if 'eight' in n.lower() else a.get('default', 0))
    F.set_variation_by_axes(vals); _fc[k] = F; return F
MOB = dict(micro=11, small=13, body=16, sub=19, head=24, semi=34, mon=48, mxl=64)
LH = dict(micro=1.3, small=1.5, body=1.5, sub=1.3, head=1.1, semi=1.02, mon=1.02, mxl=.95)
def lines(F, text, width):
    n, cur = 0, ''
    for wd in text.split(' '):
        t = (cur + ' ' + wd).strip()
        if F.getlength(t) <= width: cur = t
        else: n += 1; cur = wd
    return n + (1 if cur else 0)

class Blocks(HTMLParser):
    BLOCK = ('p', 'h1', 'h2', 'h3', 'summary')
    def __init__(self):
        super().__init__(); self.stack = []; self.blocks = []; self.cur = None; self.skip = 0
    def handle_starttag(self, tag, attrs):
        cls = dict(attrs).get('class') or ''
        self.stack.append(cls)
        if any(k in cls for k in ('wf-file', 'acc-mark', 'vmiss')): self.skip += 1
        if tag in self.BLOCK or (tag == 'span' and 'who' in cls):
            self.cur = [cls, '', ' '.join(self.stack)]
    def handle_endtag(self, tag):
        cls = self.stack.pop() if self.stack else ''
        if any(k in cls for k in ('wf-file', 'acc-mark', 'vmiss')): self.skip -= 1
        if self.cur and (tag in self.BLOCK or (tag == 'span' and 'who' in cls)):
            self.blocks.append(self.cur); self.cur = None
    def handle_data(self, d):
        if self.cur is not None and not self.skip: self.cur[1] += d

def estimate(h, W=312, Hs=556):
    P = Blocks(); P.feed(h)
    tot = 0.0; nb = 0
    for cls, txt, ctx in P.blocks:
        txt = re.sub(r'\s+', ' ', html.unescape(txt)).strip()
        if not txt: continue
        size = next((k for k in MOB if f't-{k}' in cls.split()), 'body')
        fam = 'pf' if 'pf' in cls.split() else 'in'
        w = next((int(c[1:]) * 100 for c in cls.split() if re.fullmatch(r'w\d', c)), 500)
        ital = 'it' in cls.split()
        width = W
        if ' row' in ' ' + ctx or 'row' in ctx.split(): width = W - 34 - 20
        if 'msg' in ctx: width = W - 42 - 24  # avatar 34 + separación 8 + padding de la burbuja (móvil)
        if 'piece' in ctx: width = W - 32
        if 'summary' in ctx or 'faq' in ctx: width = W - 48
        n = lines(font(fam, MOB[size], w, ital), txt, width)
        tot += n * MOB[size] * LH[size]; nb += 1
    tot += max(0, nb - 1) * 10
    tot += h.count("class='row") * 33 + h.count("class='entry") * 26 + h.count("class='piece'") * 48 + h.count("class='msg ") * 26
    if "class='entries'" in h and '<h3' in h: tot += 22
    if "class='btn'" in h: tot += 2 * 56 + 16
    tot += (h.count("<p class='in w5 t-body'>") - 1) * 6 if ('essay' in h or "class='sup'" in h) else 0
    return tot / Hs

# ------------------------------------------------------------------ salida
VERT_REL = '00-context/scenes/vertical'

def with_verticals(pins):
    """Cada escena tiene versión horizontal (desktop) y vertical 3:4 (móvil/tablet, < 860 px).
    Si la vertical existe en 00-context/scenes/vertical/<nombre>-v.webp se usa con <picture>;
    si todavía no existe, en móvil se muestra un aviso con el archivo que falta."""
    import copy
    P = copy.deepcopy(pins)
    pat = re.compile(r"<img([^>]*?) src='00-context/scenes/([^'/]+)\.webp'([^>]*)>")
    def sub(m):
        vrel = f"{VERT_REL}/{m.group(2)}-v.webp"
        if os.path.exists(os.path.join(ROOT, vrel)):
            return f"<picture><source media='(max-width: 859px)' srcset='{vrel}'>{m.group(0)}</picture>"
        return m.group(0) + f"<span class='vmiss'>Falta versión vertical 3:4 (móvil/tablet) · {vrel}</span>"
    for p in P:
        for st in p.get('stops', []):
            st['html'] = pat.sub(sub, st['html'])
            if st['id'] == '03.4m':
                vrel = f"{VERT_REL}/03-fastidio-v.webp"
                if os.path.exists(os.path.join(ROOT, vrel)):
                    st['html'] = st['html'].replace('assets/seq/03-fastidio/fastidio-f064.webp', vrel).replace('PROVISIONAL · cuadro 64 del video · se reemplaza por la imagen fija nueva', '03-fastidio-v.webp')
                else:
                    st['html'] = st['html'].replace('</figure>', f"<span class='vmiss'>Imagen fija PROVISIONAL · falta la vertical 3:4 · {vrel}</span></figure>", 1)
    return P

def vertical_status():
    names = sorted(set(re.findall(r"src='00-context/scenes/([^'/]+)\.webp'", json.dumps({'p': C.PINS}, ensure_ascii=False)))) + ['03-fastidio']
    return [(nm, os.path.exists(os.path.join(ROOT, VERT_REL, f'{nm}-v.webp'))) for nm in names]

def main():
    data = json.dumps({'pins': with_verticals(C.PINS)}, ensure_ascii=False).replace('</', '<\\/')
    out = TEMPLATE.replace('/*__DATA__*/', data)
    open(os.path.join(ROOT, '02-wireframe.html'), 'w', encoding='utf-8').write(out)

    print('== Auditoría fuente → wireframe ==')
    for bp in ('d', 'm'):
        n, miss = audit(bp)
        print(f"  {'desktop' if bp=='d' else 'móvil  '}: {n} segmentos de la fuente · {len(miss)} problemas")
        for m in miss: print('     ', m)
    print('\n== Versiones verticales (móvil/tablet) ==')
    for nm, ok in vertical_status(): print(f"  {'OK   ' if ok else 'FALTA'} {VERT_REL}/{nm}-v.webp")
    print('\n== Partitura (E por pin) ==')
    tots = {'d': 0, 'm': 0}; npins = 0
    rows = []
    for pin in C.PINS:
        if pin['type'] == 'flow': continue
        npins += 1
        for bp in ('d', 'm'):
            tots[bp] += sum(s['E'] for s in pin['stops'] if s['bp'] in ('all', bp))
        rows.append((pin['id'], pin['cap'], len([s for s in pin['stops'] if s['bp'] in ('all','d')]), sum(s['E'] for s in pin['stops'] if s['bp'] in ('all', 'd')),
                     len([s for s in pin['stops'] if s['bp'] in ('all','m')]), sum(s['E'] for s in pin['stops'] if s['bp'] in ('all', 'm'))))
    for r in rows: print(f"  {r[0]:7s} {r[1][:44]:44s} D {r[2]} paradas {r[3]:5.2f} E | M {r[4]} paradas {r[5]:5.2f} E")
    print(f"  pines: {npins} · paradas desktop {tots['d']:.2f} E · móvil {tots['m']:.2f} E · tránsitos entre pines {npins-1} E")
    print('\n== Ocupación estimada, móvil 360×612 (PIL; el % real lo mide la página) ==')
    flag = []
    for pin in C.PINS:
        if pin['type'] == 'flow': continue
        for s in pin['stops']:
            if s['kind'] in ('seal', 'hero') or s['bp'] == 'd': continue
            r = estimate(s['html'])
            if r > .85: flag.append((s['id'], round(r * 100)))
            print(f"  {s['id']:7s} {s['comp'][:28]:28s} {r*100:5.0f} %{'  <-- justo' if .85 < r <= 1 else ('  <-- DESBORDA' if r > 1 else '')}")
    print('  paradas > 85 %:', flag)

def partitura_md():
    rows = ["| Pin | Parada | Composición | E | Marcas | Intención |", "|---|---|---|---:|---|---|"]
    tot = {'d': 0, 'm': 0}; npins = 0
    for pin in C.PINS:
        if pin['type'] == 'flow':
            rows.append(f"| {pin['id']} | — | {pin['comp']} | flujo | ★ | {pin['note'].replace('|','/')} |"); continue
        npins += 1
        for s in pin['stops']:
            for bp in ('d', 'm'):
                if s['bp'] in ('all', bp): tot[bp] += s['E']
            marks = ' '.join(x for x in [('★' if s['scan'] else ''), ('oscuro' if s['night'] else ''), ({'d': 'solo desktop', 'm': 'solo móvil'}.get(s['bp'], ''))] if x)
            rows.append(f"| {pin['id']} | {s['id']} | {s['comp']} | {s['E']:g} | {marks} | {s['note'].replace('|','/')} |")
    rows.append('')
    rows.append(f"**Totales:** paradas {tot['d']:.2f} E (desktop) / {tot['m']:.2f} E (móvil) · {npins} pines → {npins-1} E de tránsito · "
                f"total aprox. {tot['d']+npins-1+2.5:.0f} E desktop / {tot['m']+npins-1+3.5:.0f} E móvil (con FAQ y footer).")
    return '\n'.join(rows)

def write_md_partitura():
    md_path = os.path.join(ROOT, '02-wireframe.md')
    if not os.path.exists(md_path): return
    md = open(md_path, encoding='utf-8').read()
    a, b = '<!-- PARTITURA:INICIO -->', '<!-- PARTITURA:FIN -->'
    if a in md and b in md:
        md = md.split(a)[0] + a + '\n' + partitura_md() + '\n' + b + md.split(b)[1]
        open(md_path, 'w', encoding='utf-8').write(md)
        print('\n02-wireframe.md: partitura actualizada')

if __name__ == '__main__':
    main()
    write_md_partitura()
