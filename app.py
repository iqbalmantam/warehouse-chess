import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="WAREHOUSE COMMAND - Developed by iqbalmantam",
    page_icon="♟️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding: 0 !important; margin: 0 !important; max-width: 100% !important;}
    .stApp {background-color: #020408; overflow: hidden;}
    iframe {display: block; border: none; width: 100vw !important; height: 100vh !important;}
</style>
""", unsafe_allow_html=True)

HTML_CODE = r'''<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Warehouse Command - Developed by iqbalmantam</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=Rajdhani:wght@600;700&display=swap" rel="stylesheet">
<style>
    * { box-sizing: border-box; user-select: none; }
    body { margin: 0; padding: 0; overflow: hidden; background: #020408; font-family: 'Rajdhani', sans-serif; color: #f8fafc; }
    #canvas-container { width: 100vw; height: 100vh; display: block; }

    /* LOADING SCREEN */
    #loading-overlay {
        position: fixed; inset: 0; background: radial-gradient(circle at center, #0f172a 0%, #020617 100%);
        z-index: 100; display: flex; flex-direction: column; align-items: center; justify-content: center;
        transition: opacity 0.6s ease;
    }
    #loading-overlay.hidden { opacity: 0; pointer-events: none; }
    .loader-title { font-family: 'Orbitron', sans-serif; font-size: 25px; font-weight: 900; letter-spacing: 4px; color: #38bdf8; margin-bottom: 8px; }
    .loader-sub { font-size: 14px; color: #94a3b8; letter-spacing: 1.5px; margin-bottom: 24px; }
    .progress-wrap { width: 340px; height: 8px; background: #1e293b; border-radius: 4px; overflow: hidden; border: 1px solid rgba(56,189,248,0.4); }
    #progress-bar { width: 10%; height: 100%; background: linear-gradient(90deg, #38bdf8, #ef4444); transition: width 0.25s; }
    .loader-credit { margin-top: 22px; font-family: 'Orbitron', sans-serif; font-size: 12px; letter-spacing: 3px; color: #f59e0b; text-transform: uppercase; font-weight: 800; }

    /* WATERMARK BADGE (ALWAYS VISIBLE AT BOTTOM-RIGHT) */
    #dev-watermark {
        position: fixed; bottom: 16px; right: 20px; z-index: 40;
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.92) 0%, rgba(2, 6, 23, 0.96) 100%);
        border: 1px solid rgba(245, 158, 11, 0.45);
        border-right: 4px solid #f59e0b;
        padding: 7px 16px; border-radius: 6px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.8), 0 0 15px rgba(245, 158, 11, 0.15);
        backdrop-filter: blur(8px);
        display: flex; align-items: center; gap: 10px;
        pointer-events: auto; text-decoration: none;
        transition: all 0.25s ease;
    }
    #dev-watermark:hover {
        border-color: #38bdf8; border-right-color: #38bdf8;
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(56, 189, 248, 0.3);
    }
    .wm-dot {
        width: 7px; height: 7px; border-radius: 50%; background: #f59e0b;
        box-shadow: 0 0 8px #f59e0b;
    }
    .wm-text {
        font-family: 'Orbitron', sans-serif; font-size: 11px; font-weight: 800;
        letter-spacing: 2px; color: #cbd5e1; text-transform: uppercase;
    }
    .wm-text span {
        color: #f59e0b; font-weight: 900;
        text-shadow: 0 0 10px rgba(245, 158, 11, 0.4);
    }

    /* CINEMATIC LETTERBOX & FIGHTING HUD */
    .cine-bar { position: fixed; left: 0; right: 0; height: 0px; background: #020408; z-index: 25; transition: height 0.4s cubic-bezier(0.16, 1, 0.3, 1); pointer-events: none; }
    #cine-top { top: 0; border-bottom: 2px solid #ef4444; }
    #cine-bot { bottom: 0; border-top: 2px solid #38bdf8; }
    body.combat-mode #cine-top, body.combat-mode #cine-bot { height: 85px; }
    body.combat-mode #top-bar, body.combat-mode #unit-inspector, body.combat-mode #ops-panel { opacity: 0; pointer-events: none; transition: opacity 0.3s; }

    #duel-hud {
        position: fixed; top: 18px; left: 50%; transform: translateX(-50%);
        width: 82vw; max-width: 960px; display: flex; align-items: center; justify-content: space-between;
        z-index: 30; opacity: 0; pointer-events: none; transition: opacity 0.35s;
    }
    body.combat-mode #duel-hud { opacity: 1; }
    .fighter-box { width: 42%; }
    .fighter-name { font-family: 'Orbitron', sans-serif; font-size: 14px; font-weight: 900; letter-spacing: 1.5px; margin-bottom: 5px; display: flex; justify-content: space-between; }
    .hp-track { width: 100%; height: 18px; background: rgba(15, 23, 42, 0.9); border: 2px solid #cbd5e1; border-radius: 4px; overflow: hidden; box-shadow: 0 0 20px rgba(0,0,0,0.8); }
    .hp-fill { height: 100%; width: 100%; transition: width 0.2s ease-out; }
    .hp-blue { background: linear-gradient(90deg, #0284c7, #38bdf8); }
    .hp-orange { background: linear-gradient(270deg, #991b1b, #ef4444); float: right; }
    .vs-emblem { font-family: 'Orbitron', sans-serif; font-size: 26px; font-weight: 900; color: #f59e0b; text-shadow: 0 0 15px #ef4444; padding: 0 12px; }

    #combat-banner {
        position: fixed; top: 52%; left: 50%; transform: translate(-50%, -50%) scale(0.4);
        font-family: 'Orbitron', sans-serif; font-size: 44px; font-weight: 900;
        color: #fff; text-transform: uppercase; letter-spacing: 5px;
        text-shadow: 0 0 25px #ef4444, 0 0 60px #f59e0b;
        opacity: 0; pointer-events: none; z-index: 35; transition: 0.22s cubic-bezier(0.175, 0.885, 0.32, 1.275); white-space: nowrap;
    }
    #combat-banner.show { opacity: 1; transform: translate(-50%, -50%) scale(1); }

    #combo-counter {
        position: fixed; bottom: 110px; left: 60px; z-index: 35;
        font-family: 'Orbitron', sans-serif; font-size: 34px; font-weight: 900;
        color: #38bdf8; text-shadow: 0 0 20px #0284c7;
        opacity: 0; transform: translateX(-30px); transition: 0.2s; pointer-events: none;
    }
    #combo-counter.show { opacity: 1; transform: translateX(0); }

    /* TOP BAR */
    #top-bar {
        position: absolute; top: 0; left: 0; right: 0; height: 64px;
        background: linear-gradient(180deg, rgba(5, 9, 18, 0.96) 0%, rgba(5, 9, 18, 0.75) 100%);
        border-bottom: 1px solid rgba(56, 189, 248, 0.3);
        display: flex; justify-content: space-between; align-items: center;
        padding: 0 22px; z-index: 10; backdrop-filter: blur(10px); transition: opacity 0.3s;
    }
    .brand-cluster { display: flex; align-items: center; gap: 12px; }
    .brand-emblem {
        width: 38px; height: 38px; border-radius: 6px;
        background: linear-gradient(135deg, #38bdf8, #ef4444);
        display: flex; align-items: center; justify-content: center;
        font-family: 'Orbitron', sans-serif; font-weight: 900; font-size: 17px; color: #020617;
    }
    .brand-title h1 { margin: 0; font-family: 'Orbitron', sans-serif; font-size: 15px; font-weight: 800; letter-spacing: 2px; }
    .brand-title span { font-size: 11px; color: #f59e0b; letter-spacing: 1px; display: block; font-weight: 700; }

    .versus-hud {
        display: flex; align-items: center; gap: 16px;
        background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(148, 163, 184, 0.25);
        padding: 5px 20px; border-radius: 30px;
    }
    .team-score { display: flex; align-items: center; gap: 8px; font-weight: 700; font-size: 13px; }
    .team-score.blue { color: #38bdf8; }
    .team-score.orange { color: #ef4444; }
    .score-pill { background: #020617; padding: 2px 9px; border-radius: 10px; font-family: 'Orbitron', sans-serif; border: 1px solid currentColor; }
    #turn-banner { padding: 4px 14px; border-radius: 16px; font-family: 'Orbitron', sans-serif; font-size: 11px; font-weight: 800; }
    .turn-blue { background: rgba(2, 132, 199, 0.35); color: #38bdf8; border: 1px solid #38bdf8; }
    .turn-orange { background: rgba(220, 38, 38, 0.35); color: #f87171; border: 1px solid #ef4444; }

    .toolbar { display: flex; gap: 6px; }
    .t-btn {
        background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(148, 163, 184, 0.3);
        color: #e2e8f0; padding: 7px 12px; border-radius: 5px; font-family: 'Rajdhani', sans-serif;
        font-weight: 700; font-size: 12px; text-transform: uppercase; cursor: pointer; transition: 0.2s;
    }
    .t-btn:hover { border-color: #38bdf8; color: #fff; background: rgba(56, 189, 248, 0.2); }
    .t-btn.active { background: #0284c7; border-color: #38bdf8; }
    .t-btn.epic-btn { background: linear-gradient(135deg, #dc2626, #ea580c); border-color: #fbbf24; color: #fff; box-shadow: 0 0 12px rgba(239,68,68,0.4); }

    #unit-inspector {
        position: absolute; top: 80px; left: 18px; width: 295px;
        background: rgba(8, 13, 24, 0.92); border: 1px solid rgba(56, 189, 248, 0.3);
        border-left: 4px solid #38bdf8; border-radius: 8px; padding: 12px 15px; z-index: 10; backdrop-filter: blur(8px); transition: opacity 0.3s;
    }
    .panel-tag { font-family: 'Orbitron', sans-serif; font-size: 9px; color: #64748b; letter-spacing: 1.5px; }
    #insp-name { font-family: 'Orbitron', sans-serif; font-size: 14px; font-weight: 800; margin: 2px 0; color: #fff; }
    #insp-role { font-size: 12px; color: #f59e0b; font-weight: 700; margin-bottom: 6px; }
    #insp-weapon { font-size: 11.5px; color: #38bdf8; margin-bottom: 8px; font-weight: 600; }
    .roster-mini { margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.1); font-size: 10.5px; color: #cbd5e1; line-height: 1.55; }
    .f-hdr { font-family: 'Orbitron', sans-serif; font-size: 10px; font-weight: 800; margin: 6px 0 3px 0; display: block; }

    #ops-panel {
        position: absolute; top: 80px; right: 18px; width: 255px;
        background: rgba(8, 13, 24, 0.92); border: 1px solid rgba(239, 68, 68, 0.3);
        border-right: 4px solid #ef4444; border-radius: 8px; padding: 12px 15px; z-index: 10; transition: opacity 0.3s;
    }
    #move-history { max-height: 145px; overflow-y: auto; display: flex; flex-direction: column; gap: 4px; margin-top: 6px; }
    .log-entry { background: rgba(15, 23, 42, 0.85); padding: 4px 8px; border-radius: 4px; border-left: 2px solid #475569; font-size: 11px; }
    .log-entry.combat { border-left-color: #ef4444; background: rgba(127, 29, 29, 0.35); color: #fca5a5; font-weight: 700; }

    #bottom-ticker {
        position: absolute; bottom: 16px; left: 42%; transform: translateX(-50%);
        background: rgba(5, 9, 18, 0.95); border: 1px solid rgba(56, 189, 248, 0.35);
        padding: 8px 22px; border-radius: 24px; display: flex; align-items: center; gap: 10px; z-index: 30; font-size: 13px; font-weight: 600;
    }
    .pulse-dot { width: 8px; height: 8px; border-radius: 50%; background: #22c55e; box-shadow: 0 0 10px #22c55e; }
</style>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/utils/SkeletonUtils.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/EffectComposer.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/RenderPass.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/ShaderPass.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/shaders/CopyShader.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/shaders/LuminosityHighPassShader.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/UnrealBloomPass.js"></script>
</head>
<body>
    <div id="loading-overlay">
        <div class="loader-title">HUMANS VS ROGUE AI AUTOMATION</div>
        <div id="loader-status" class="loader-sub">Menyiapkan Papan Catur Klasik Hitam-Putih & Karakter 3D...</div>
        <div class="progress-wrap"><div id="progress-bar"></div></div>
        <div class="loader-credit">⚡ DEVELOPED BY IQBALMANTAM ⚡</div>
    </div>

    <!-- WATERMARK RESMI DEVELOPED BY IQBALMANTAM -->
    <a id="dev-watermark" href="https://github.com/iqbalmantam/warehouse-chess" target="_blank" title="Official Repository by iqbalmantam">
        <div class="wm-dot"></div>
        <div class="wm-text">DEVELOPED BY <span>IQBALMANTAM</span></div>
    </a>

    <div id="cine-top" class="cine-bar"></div>
    <div id="cine-bot" class="cine-bar"></div>
    <div id="duel-hud">
        <div class="fighter-box">
            <div class="fighter-name"><span id="duel-atk-name" style="color:#38bdf8">HUMAN CORPS</span><span id="duel-atk-hp-txt">100%</span></div>
            <div class="hp-track"><div id="duel-atk-bar" class="hp-fill hp-blue"></div></div>
        </div>
        <div class="vs-emblem">VS</div>
        <div class="fighter-box">
            <div class="fighter-name"><span id="duel-def-hp-txt">100%</span><span id="duel-def-name" style="color:#ef4444">ROGUE AI BOT</span></div>
            <div class="hp-track"><div id="duel-def-bar" class="hp-fill hp-orange"></div></div>
        </div>
    </div>
    <div id="combat-banner">⚔️ ROUND 1 - FIGHT!</div>
    <div id="combo-counter">3 HIT COMBO!</div>

    <div id="top-bar">
        <div class="brand-cluster">
            <div class="brand-emblem">IM</div>
            <div class="brand-title">
                <h1>WAREHOUSE COMMAND: ASYMMETRIC WARFARE</h1>
                <span>🔵 Human Corps vs 🔴 Rogue AI • Developed by iqbalmantam</span>
            </div>
        </div>

        <div class="versus-hud">
            <div class="team-score blue"><span>HUMANS</span><span id="score-blue" class="score-pill">16</span></div>
            <div id="turn-banner" class="turn-blue">GILIRAN MANUSIA</div>
            <div class="team-score orange"><span id="score-orange" class="score-pill">16</span><span>ROGUE AI</span></div>
        </div>

        <div class="toolbar">
            <button id="btn-ai" class="t-btn active" onclick="toggleAI()">🤖 Lawan AI</button>
            <button class="t-btn epic-btn" onclick="demoCombat()">🔥 Duel Manusia vs Robot!</button>
            <button class="t-btn" onclick="setCameraView('enemy')">👁️ Zoom Faksi Lawan</button>
            <button class="t-btn" onclick="setCameraView('perspective')">🎥 Kamera Arena</button>
            <button class="t-btn" onclick="resetGame()">🔄 Reset</button>
        </div>
    </div>

    <div id="unit-inspector">
        <div class="panel-tag">ASYMMETRIC FACTION INSPECTOR</div>
        <h2 id="insp-name">ANDROID WORKER DRONE</h2>
        <div id="insp-role">Faksi Lawan • Autonomous Robot</div>
        <div id="insp-weapon">⚡ Senjata: Hydraulic Servo Punch</div>
        <div class="roster-mini">
            <span class="f-hdr" style="color:#38bdf8">🔵 FAKSI BIRU (MANUSIA ASLI):</span>
            <div>• <b>Pion:</b> Operator Manusia | <b>Benteng:</b> Forklift</div>
            <div>• <b>Kuda:</b> Hover Cruiser | <b>Gajah:</b> QC Sniper</div>
            <div>• <b>Menteri:</b> Exo-Commander | <b>Raja:</b> WMS Server</div>
            <span class="f-hdr" style="color:#ef4444">🔴 FAKSI LAWAN (MESIN OTOMASI / ROBOT):</span>
            <div>• <b>Pion:</b> Android Bot (.GLB) | <b>Benteng:</b> 6-Leg Spider Tank</div>
            <div>• <b>Kuda:</b> Quadcopter Drone | <b>Gajah:</b> Tripod Railgun</div>
            <div>• <b>Menteri:</b> Goliath Cyber-Mech | <b>Raja:</b> AI Singularity Core</div>
        </div>
    </div>

    <div id="ops-panel">
        <div class="panel-tag">COMBAT TELEMETRY LOG</div>
        <div id="move-history"></div>
    </div>

    <div id="bottom-ticker">
        <div class="pulse-dot"></div>
        <div id="action-log">Warehouse Command 3D • Developed by iqbalmantam. Pilih bidak Biru untuk melangkah!</div>
    </div>

    <div id="canvas-container"></div>

<script>
// ============================================================================
// 1. RENDERER & UNREAL BLOOM POST-PROCESSING
// ============================================================================
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x060a12);
scene.fog = new THREE.FogExp2(0x060a12, 0.012);

const camera = new THREE.PerspectiveCamera(36, window.innerWidth / window.innerHeight, 0.1, 200);
camera.position.set(0, 10.6, 13.4);

const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 0.95;
renderer.outputEncoding = THREE.sRGBEncoding;
container.appendChild(renderer.domElement);

const maxAnisotropy = renderer.capabilities.getMaxAnisotropy();

const renderScene = new THREE.RenderPass(scene, camera);
const bloomPass = new THREE.UnrealBloomPass(
    new THREE.Vector2(window.innerWidth, window.innerHeight),
    0.38, 0.32, 0.92
);
const composer = new THREE.EffectComposer(renderer);
composer.addPass(renderScene);
composer.addPass(bloomPass);

const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.06;
controls.maxPolarAngle = Math.PI / 2 - 0.03;
controls.minDistance = 2.2;
controls.maxDistance = 24;
controls.target.set(0, 0.6, 0);

const hemiLight = new THREE.HemisphereLight(0xffffff, 0x1e293b, 0.85);
scene.add(hemiLight);

const mainLight = new THREE.DirectionalLight(0xfffbeb, 1.35);
mainLight.position.set(8, 19, 11);
mainLight.castShadow = true;
mainLight.shadow.mapSize.set(2048, 2048);
const d = 8.4;
Object.assign(mainLight.shadow.camera, { left: -d, right: d, top: d, bottom: -d, near: 2, far: 42 });
mainLight.shadow.bias = -0.0004;
scene.add(mainLight);

const blueRim = new THREE.PointLight(0x38bdf8, 1.1, 26); blueRim.position.set(-9, 6, 9); scene.add(blueRim);
const redRim = new THREE.PointLight(0xef4444, 1.1, 26); redRim.position.set(9, 6, -9); scene.add(redRim);

const duelLight = new THREE.PointLight(0xffffff, 0, 12);
scene.add(duelLight);

// ============================================================================
// 2. PAPAN CATUR KLASIK HITAM & PUTIH + PLAKAT 3D "DEVELOPED BY IQBALMANTAM"
// ============================================================================
function makeTileTex(isDark, lbl) {
    const c = document.createElement('canvas'); c.width = 512; c.height = 512;
    const ctx = c.getContext('2d');

    ctx.fillStyle = isDark ? '#18181b' : '#f1f5f9';
    ctx.fillRect(0, 0, 512, 512);

    ctx.strokeStyle = isDark ? 'rgba(255,255,255,0.04)' : 'rgba(15,23,42,0.05)';
    ctx.lineWidth = 2;
    for(let i = 64; i < 512; i += 64) {
        ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, 512); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(0, i); ctx.lineTo(512, i); ctx.stroke();
    }

    ctx.strokeStyle = isDark ? '#27272a' : '#cbd5e1';
    ctx.lineWidth = 12;
    ctx.strokeRect(6, 6, 500, 500);

    ctx.fillStyle = isDark ? 'rgba(245, 158, 11, 0.45)' : 'rgba(2, 132, 199, 0.45)';
    ctx.fillRect(22, 22, 26, 5); ctx.fillRect(22, 22, 5, 26);
    ctx.fillRect(464, 22, 26, 5); ctx.fillRect(485, 22, 5, 26);

    if (lbl) {
        ctx.fillStyle = isDark ? '#f8fafc' : '#0f172a';
        ctx.font = 'bold 54px Orbitron, monospace';
        ctx.fillText(lbl, 34, 470);
    }
    const tex = new THREE.CanvasTexture(c);
    tex.anisotropy = maxAnisotropy;
    return tex;
}

// Tekstur Plakat Logam Emas 3D di Bingkai Papan
function makeCreatorPlaqueTex() {
    const c = document.createElement('canvas'); c.width = 1024; c.height = 128;
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#090d16'; ctx.fillRect(0, 0, 1024, 128);
    ctx.strokeStyle = '#f59e0b'; ctx.lineWidth = 8; ctx.strokeRect(6, 6, 1012, 116);
    ctx.fillStyle = '#f59e0b';
    ctx.font = '900 42px Orbitron, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('⚡ DEVELOPED BY IQBALMANTAM ⚡', 512, 66);
    const tex = new THREE.CanvasTexture(c);
    tex.anisotropy = maxAnisotropy;
    return tex;
}

const boardGroup = new THREE.Group(); scene.add(boardGroup);
const floor = new THREE.Mesh(new THREE.PlaneGeometry(85, 85), new THREE.MeshStandardMaterial({ color: 0x050811, roughness: 0.8 }));
floor.rotation.x = -Math.PI/2; floor.position.y = -0.35; floor.receiveShadow = true; scene.add(floor);

const base = new THREE.Mesh(new THREE.BoxGeometry(10.5, 0.35, 10.5), new THREE.MeshStandardMaterial({ color: 0x111827, roughness: 0.4, metalness: 0.5 }));
base.position.y = -0.2; base.receiveShadow = true; boardGroup.add(base);

const goldBorder = new THREE.Mesh(new THREE.BoxGeometry(9.85, 0.12, 9.85), new THREE.MeshStandardMaterial({ color: 0xd97706, roughness: 0.3, metalness: 0.7 }));
goldBorder.position.y = -0.02; boardGroup.add(goldBorder);

// Plakat 3D "DEVELOPED BY IQBALMANTAM" di Sisi Depan & Belakang Papan Catur
const plaqueMat = new THREE.MeshStandardMaterial({ map: makeCreatorPlaqueTex(), roughness: 0.25, metalness: 0.4 });
const frontPlaque = new THREE.Mesh(new THREE.BoxGeometry(4.2, 0.24, 0.06), plaqueMat);
frontPlaque.position.set(0, -0.18, 5.26);
boardGroup.add(frontPlaque);

const tileSize = 1.2, offset = 3.5 * tileSize, tiles = [], cols = ['A','B','C','D','E','F','G','H'];
for (let x = 0; x < 8; x++) {
    tiles[x] = [];
    for (let z = 0; z < 8; z++) {
        const isDark = (x + z) % 2 === 1;
        const lbl = (z === 7) ? cols[x] : (x === 0 ? String(8 - z) : '');
        const tile = new THREE.Mesh(
            new THREE.BoxGeometry(tileSize * 0.99, 0.1, tileSize * 0.99),
            new THREE.MeshStandardMaterial({
                map: makeTileTex(isDark, lbl),
                roughness: isDark ? 0.45 : 0.62,
                metalness: 0.05
            })
        );
        tile.position.set(x * tileSize - offset, 0, z * tileSize - offset);
        tile.receiveShadow = true; tile.userData = { gridX: x, gridZ: z };
        boardGroup.add(tile); tiles[x][z] = tile;
    }
}

function buildRack(xPos, zPos, rotY) {
    const r = new THREE.Group();
    const uMat = new THREE.MeshStandardMaterial({ color: 0x1d4ed8, roughness: 0.35, metalness: 0.5 });
    const bMat = new THREE.MeshStandardMaterial({ color: 0xea580c, roughness: 0.35, metalness: 0.4 });
    const cMat = new THREE.MeshStandardMaterial({ color: 0x9a6b3e, roughness: 0.7 });
    [-1.8, 0, 1.8].forEach(lx => [-0.4, 0.4].forEach(lz => {
        const p = new THREE.Mesh(new THREE.BoxGeometry(0.09, 3.6, 0.09), uMat);
        p.position.set(lx, 1.8, lz); r.add(p);
    }));
    [0.85, 1.95, 3.05].forEach(ly => {
        const bm = new THREE.Mesh(new THREE.BoxGeometry(3.7, 0.08, 0.84), bMat);
        bm.position.set(0, ly, 0); r.add(bm);
        [-1.1, 0, 1.1].forEach(bx => {
            const box = new THREE.Mesh(new THREE.BoxGeometry(0.65, 0.48, 0.65), cMat);
            box.position.set(bx, ly + 0.28, 0); r.add(box);
        });
    });
    r.position.set(xPos, -0.35, zPos); r.rotation.y = rotY; scene.add(r);
}
buildRack(-7.6, -2.3, Math.PI/2); buildRack(-7.6, 2.3, Math.PI/2);
buildRack(7.6, -2.3, -Math.PI/2); buildRack(7.6, 2.3, -Math.PI/2);

// ============================================================================
// 3. BLENDER .GLB LOADER (SOLDIER UNTUK MANUSIA, ROBOT UNTUK MUSUH!)
// ============================================================================
let soldierAsset = null;
let mechAsset = null;
const mixers = [];
const animatedParts = [];

const mats = {
    blackSteel: new THREE.MeshStandardMaterial({ color: 0x0f172a, metalness: 0.85, roughness: 0.2 }),
    obsidian: new THREE.MeshStandardMaterial({ color: 0x18181b, metalness: 0.9, roughness: 0.15 }),
    chrome: new THREE.MeshStandardMaterial({ color: 0xf8fafc, metalness: 0.96, roughness: 0.08 }),
    rubber: new THREE.MeshStandardMaterial({ color: 0x090d16, roughness: 0.9 }),
    cardboard: new THREE.MeshStandardMaterial({ color: 0xb48352, roughness: 0.72 }),
    gold: new THREE.MeshStandardMaterial({ color: 0xf59e0b, metalness: 0.85, roughness: 0.18 }),
    blueArmor: new THREE.MeshStandardMaterial({ color: 0x0284c7, roughness: 0.28, metalness: 0.55 }),
    crimsonArmor: new THREE.MeshStandardMaterial({ color: 0x991b1b, roughness: 0.22, metalness: 0.75 }),
    neonBlue: new THREE.MeshStandardMaterial({ color: 0x38bdf8, emissive: 0x0284c7, emissiveIntensity: 2.3 }),
    neonRed: new THREE.MeshStandardMaterial({ color: 0xff0044, emissive: 0xdc2626, emissiveIntensity: 2.8 }),
    neonAmber: new THREE.MeshStandardMaterial({ color: 0xfbbf24, emissive: 0xd97706, emissiveIntensity: 2.3 })
};

const gltfLoader = new THREE.GLTFLoader();

function loadAllBlenderAssets() {
    const pBar = document.getElementById('progress-bar');
    const soldierURL = 'https://raw.githubusercontent.com/mrdoob/three.js/r128/examples/models/gltf/Soldier.glb';
    const mechURL = 'https://raw.githubusercontent.com/mrdoob/three.js/r128/examples/models/gltf/RobotExpressive/RobotExpressive.glb';

    Promise.all([
        new Promise(res => gltfLoader.load(soldierURL, g => { pBar.style.width = '55%'; res(g); }, undefined, () => res(null))),
        new Promise(res => gltfLoader.load(mechURL, g => { pBar.style.width = '100%'; res(g); }, undefined, () => res(null)))
    ]).then(([sGltf, mGltf]) => {
        soldierAsset = sGltf;
        mechAsset = mGltf;
        setTimeout(() => {
            document.getElementById('loading-overlay').classList.add('hidden');
            resetGame();
        }, 250);
    });
}

function spawnHumanCorpsGLB(scaleVal, tintHex, visorHex) {
    const wrapper = new THREE.Group();
    if (!soldierAsset) return { wrapper, setAnim: () => {} };

    const cloned = THREE.SkeletonUtils.clone(soldierAsset.scene);
    cloned.scale.set(scaleVal, scaleVal, scaleVal);
    cloned.rotation.y = Math.PI;

    cloned.traverse(child => {
        if (child.isMesh) {
            child.castShadow = true; child.receiveShadow = true;
            child.material = child.material.clone();
            if (child.material.map) child.material.map.anisotropy = maxAnisotropy;
            child.material.color.lerp(new THREE.Color(tintHex), 0.35);
        }
    });
    wrapper.add(cloned);

    if (visorHex) {
        const visor = new THREE.Mesh(
            new THREE.CylinderGeometry(0.13, 0.13, 0.035, 16),
            new THREE.MeshStandardMaterial({ color: visorHex, emissive: visorHex, emissiveIntensity: 1.5 })
        );
        visor.position.set(0, 1.05 * scaleVal, 0);
        wrapper.add(visor);
    }

    const mixer = new THREE.AnimationMixer(cloned);
    const clips = soldierAsset.animations;
    const actions = {
        Idle: mixer.clipAction(THREE.AnimationClip.findByName(clips, 'Idle') || clips[0]),
        Walk: mixer.clipAction(THREE.AnimationClip.findByName(clips, 'Walk') || clips[3]),
        Run:  mixer.clipAction(THREE.AnimationClip.findByName(clips, 'Run')  || clips[1])
    };
    actions.Idle.play();
    mixers.push(mixer);

    let cur = actions.Idle;
    function setAnim(name, speed = 1.0) {
        const next = actions[name] || actions.Idle;
        if (next) {
            next.timeScale = speed;
            if (next !== cur) { cur.fadeOut(0.14); next.reset().fadeIn(0.14).play(); cur = next; }
        }
    }
    return { wrapper, setAnim };
}

function spawnRogueRobotGLB(scaleVal, mainColorHex, eyeGlowMat) {
    const wrapper = new THREE.Group();
    if (!mechAsset) return { wrapper, setAnim: () => {} };

    const cloned = THREE.SkeletonUtils.clone(mechAsset.scene);
    cloned.scale.set(scaleVal, scaleVal, scaleVal);
    cloned.rotation.y = 0;

    cloned.traverse(c => {
        if (c.isMesh) {
            c.castShadow = true; c.receiveShadow = true;
            c.material = c.material.clone();
            c.material.metalness = 0.8;
            c.material.roughness = 0.25;
            if (c.material.name && c.material.name.includes('Main')) {
                c.material.color.setHex(mainColorHex);
            } else if (c.material.name && c.material.name.includes('Black')) {
                c.material.color.setHex(0x090d16);
            }
        }
    });
    wrapper.add(cloned);

    const chestCore = new THREE.Mesh(new THREE.SphereGeometry(0.32 * scaleVal, 12, 12), eyeGlowMat);
    chestCore.position.set(0, 1.8 * scaleVal, 0.45 * scaleVal);
    wrapper.add(chestCore);

    const mixer = new THREE.AnimationMixer(cloned);
    const clips = mechAsset.animations;
    const actions = {
        Idle:  mixer.clipAction(THREE.AnimationClip.findByName(clips, 'Idle')),
        Walk:  mixer.clipAction(THREE.AnimationClip.findByName(clips, 'Walking')),
        Run:   mixer.clipAction(THREE.AnimationClip.findByName(clips, 'Running')),
        Punch: mixer.clipAction(THREE.AnimationClip.findByName(clips, 'Punch')),
        Jump:  mixer.clipAction(THREE.AnimationClip.findByName(clips, 'Jump')),
        Wave:  mixer.clipAction(THREE.AnimationClip.findByName(clips, 'ThumbsUp') || THREE.AnimationClip.findByName(clips, 'Wave'))
    };
    if (actions.Idle) actions.Idle.play();
    mixers.push(mixer);

    let cur = actions.Idle;
    function setAnim(name, speed = 1.0) {
        const next = actions[name] || actions.Run || actions.Idle;
        if (next) {
            next.timeScale = speed;
            if (next !== cur) { if (cur) cur.fadeOut(0.12); next.reset().fadeIn(0.12).play(); cur = next; }
        }
    }
    return { wrapper, setAnim };
}

// ============================================================================
// 4. ASYMMETRIC UNIT FACTORY: FAKSI BIRU (MANUSIA) VS FAKSI ORANYE (ROBOT AI)
// ============================================================================
function createUnitMesh(type, team) {
    const root = new THREE.Group();
    const isBlue = team === 'blue';
    const glowMat = isBlue ? mats.neonBlue : mats.neonRed;

    const shadowDisc = new THREE.Mesh(
        new THREE.CylinderGeometry(0.47, 0.49, 0.02, 32),
        new THREE.MeshStandardMaterial({ color: isBlue ? 0x082f49 : 0x450a0a, roughness: 0.5 })
    );
    shadowDisc.position.y = 0.01;
    root.add(shadowDisc);

    const ring = new THREE.Mesh(new THREE.TorusGeometry(0.47, 0.022, 12, 32), glowMat);
    ring.rotation.x = Math.PI / 2; ring.position.y = 0.025;
    root.add(ring);

    const dir = new THREE.Group();
    root.add(dir);

    const frontPointer = new THREE.Mesh(new THREE.ConeGeometry(0.08, 0.16, 4), glowMat);
    frontPointer.rotation.x = Math.PI / 2;
    frontPointer.position.set(0, 0.035, 0.51);
    dir.add(frontPointer);

    // A. FAKSI BIRU: HUMAN LOGISTICS CORPS
    if (isBlue) {
        if (type === 'pawn') {
            const human = spawnHumanCorpsGLB(0.60, 0x38bdf8, null);
            dir.add(human.wrapper);
            const crate = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.22, 0.22), mats.cardboard);
            crate.position.set(-0.24, 0.12, 0.12); crate.castShadow = true;
            dir.add(crate);
            root.userData.setAnim = human.setAnim;
        }
        else if (type === 'rook') {
            const vehicle = new THREE.Group(); dir.add(vehicle);
            [[-0.32, 0.16, 0.24], [0.32, 0.16, 0.24], [-0.3, 0.13, -0.28], [0.3, 0.13, -0.28]].forEach(([wx, wy, wz]) => {
                const w = new THREE.Mesh(new THREE.CylinderGeometry(wy, wy, 0.12, 20), mats.rubber);
                w.rotation.z = Math.PI/2; w.position.set(wx, wy, wz); vehicle.add(w);
            });
            const chassis = new THREE.Mesh(new THREE.BoxGeometry(0.58, 0.28, 0.7), mats.blueArmor);
            chassis.position.set(0, 0.26, -0.05); chassis.castShadow = true; vehicle.add(chassis);

            const driver = spawnHumanCorpsGLB(0.46, 0x0284c7, null);
            driver.wrapper.position.set(0, 0.32, -0.05); vehicle.add(driver.wrapper);

            const roof = new THREE.Mesh(new THREE.BoxGeometry(0.52, 0.04, 0.48), mats.blackSteel);
            roof.position.set(0, 1.05, -0.05); vehicle.add(roof);

            const forkPivot = new THREE.Group(); forkPivot.position.set(0, 0.14, 0.34); vehicle.add(forkPivot);
            [-0.18, 0.18].forEach(fx => {
                const mast = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.96, 0.06), mats.blackSteel);
                mast.position.set(fx, 0.45, 0.32); vehicle.add(mast);
                const blade = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.03, 0.46), mats.chrome);
                blade.position.set(fx, 0, 0.22); forkPivot.add(blade);
            });
            root.userData.forkPivot = forkPivot;
            root.userData.setAnim = driver.setAnim;
        }
        else if (type === 'knight') {
            const speeder = new THREE.Group(); dir.add(speeder);
            const deck = new THREE.Mesh(new THREE.BoxGeometry(0.48, 0.1, 0.78), mats.blackSteel);
            deck.position.set(0, 0.14, 0); speeder.add(deck);
            const cowl = new THREE.Mesh(new THREE.ConeGeometry(0.24, 0.45, 6), mats.blueArmor);
            cowl.rotation.x = Math.PI/2; cowl.position.set(0, 0.34, 0.25); speeder.add(cowl);

            const pilot = spawnHumanCorpsGLB(0.54, 0x38bdf8, null);
            pilot.wrapper.position.set(0, 0.18, -0.14); speeder.add(pilot.wrapper);
            animatedParts.push({ mesh: speeder, type: 'hover', baseY: 0.04 });
            root.userData.setAnim = pilot.setAnim;
        }
        else if (type === 'bishop') {
            const sniper = spawnHumanCorpsGLB(0.64, 0xffffff, 0x38bdf8);
            dir.add(sniper.wrapper);
            const laserPod = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.055, 0.58, 12), mats.blackSteel);
            laserPod.rotation.x = Math.PI/2; laserPod.position.set(0.22, 0.80, 0.18);
            const tip = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.16, 12), mats.neonBlue);
            tip.position.y = 0.3; laserPod.add(tip);
            dir.add(laserPod);
            root.userData.setAnim = sniper.setAnim;
        }
        else if (type === 'queen') {
            const cmdr = spawnHumanCorpsGLB(0.72, 0xfbbf24, 0x38bdf8);
            dir.add(cmdr.wrapper);
            [-0.26, 0.26].forEach(wx => {
                const wing = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.65, 0.22), mats.gold);
                wing.position.set(wx, 0.85, -0.15); wing.rotation.z = wx * 0.6;
                dir.add(wing);
                const blade = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.01, 0.65, 10), mats.neonBlue);
                blade.rotation.x = Math.PI/2; blade.position.set(wx, 0.65, 0.32);
                dir.add(blade);
            });
            root.userData.setAnim = cmdr.setAnim;
        }
        else if (type === 'king') {
            const citadel = new THREE.Group(); dir.add(citadel);
            const tower = new THREE.Mesh(new THREE.BoxGeometry(0.5, 1.05, 0.5), mats.blackSteel);
            tower.position.y = 0.55; tower.castShadow = true; citadel.add(tower);
            for (let i = 0; i < 6; i++) {
                const blade = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.03, 0.52), mats.neonBlue);
                blade.position.set(0, 0.2 + i * 0.14, 0); citadel.add(blade);
            }
            const core = new THREE.Mesh(new THREE.OctahedronGeometry(0.22, 1), mats.neonBlue);
            core.position.y = 1.35; citadel.add(core);
            animatedParts.push({ mesh: core, type: 'spin' });
        }
    }

    // B. FAKSI LAWAN: APEX ROGUE AI MACHINES
    else {
        if (type === 'pawn') {
            const bot = spawnRogueRobotGLB(0.18, 0xd97706, mats.neonRed);
            dir.add(bot.wrapper);
            root.userData.setAnim = bot.setAnim;
            root.userData.isMech = true;
        }
        else if (type === 'rook') {
            const spider = new THREE.Group(); dir.add(spider);
            const thorax = new THREE.Mesh(new THREE.CylinderGeometry(0.36, 0.42, 0.28, 6), mats.crimsonArmor);
            thorax.position.set(0, 0.36, 0); thorax.castShadow = true; spider.add(thorax);

            const dome = new THREE.Mesh(new THREE.SphereGeometry(0.26, 16, 12, 0, Math.PI*2, 0, Math.PI*0.5), mats.obsidian);
            dome.position.set(0, 0.48, 0); spider.add(dome);

            const eye = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.07, 0.1), mats.neonRed);
            eye.position.set(0, 0.46, 0.26); spider.add(eye);

            [-1, 1].forEach(side => {
                [-0.24, 0, 0.24].forEach(zOff => {
                    const legGrp = new THREE.Group();
                    legGrp.position.set(side * 0.32, 0.32, zOff);
                    const femur = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.06, 0.06), mats.blackSteel);
                    femur.position.set(side * 0.08, 0.05, 0); femur.rotation.z = side * 0.35;
                    const tibia = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.015, 0.36, 8), mats.chrome);
                    tibia.position.set(side * 0.18, -0.14, 0); tibia.rotation.z = side * -0.2;
                    legGrp.add(femur, tibia);
                    spider.add(legGrp);
                });
            });

            const clawPivot = new THREE.Group();
            clawPivot.position.set(0, 0.28, 0.34);
            spider.add(clawPivot);
            [-0.18, 0.18].forEach(cx => {
                const pincer = new THREE.Mesh(new THREE.ConeGeometry(0.07, 0.42, 4), mats.neonAmber);
                pincer.rotation.x = Math.PI / 2;
                pincer.rotation.z = cx * -0.4;
                pincer.position.set(cx, 0, 0.16);
                clawPivot.add(pincer);
            });
            root.userData.forkPivot = clawPivot;
        }
        else if (type === 'knight') {
            const drone = new THREE.Group();
            drone.position.y = 0.65;
            dir.add(drone);

            const body = new THREE.Mesh(new THREE.OctahedronGeometry(0.28, 1), mats.obsidian);
            body.scale.set(1.1, 0.55, 1.4); body.castShadow = true; drone.add(body);

            const scanner = new THREE.Mesh(new THREE.SphereGeometry(0.11, 12, 12), mats.neonRed);
            scanner.position.set(0, -0.04, 0.32); drone.add(scanner);

            const payload = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.1, 0.42, 12), mats.crimsonArmor);
            payload.rotation.x = Math.PI/2; payload.position.set(0, -0.18, 0); drone.add(payload);

            [[-0.32, 0.32], [0.32, 0.32], [-0.32, -0.32], [0.32, -0.32]].forEach(([rx, rz]) => {
                const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.45, 8), mats.blackSteel);
                arm.rotation.z = Math.PI/2; arm.rotation.y = Math.atan2(rz, rx);
                arm.position.set(rx*0.5, 0, rz*0.5); drone.add(arm);

                const shroud = new THREE.Mesh(new THREE.TorusGeometry(0.15, 0.018, 8, 20), mats.crimsonArmor);
                shroud.rotation.x = Math.PI/2; shroud.position.set(rx, 0.04, rz); drone.add(shroud);

                const blade = new THREE.Mesh(new THREE.BoxGeometry(0.26, 0.01, 0.03), mats.neonAmber);
                blade.position.set(rx, 0.05, rz); drone.add(blade);
                animatedParts.push({ mesh: blade, type: 'rotor' });
            });
            animatedParts.push({ mesh: drone, type: 'hover', baseY: 0.65 });
        }
        else if (type === 'bishop') {
            const turret = new THREE.Group(); dir.add(turret);
            [0, 2.09, 4.18].forEach(ang => {
                const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.05, 0.65, 10), mats.obsidian);
                leg.position.set(Math.sin(ang)*0.22, 0.28, Math.cos(ang)*0.22);
                leg.rotation.z = -Math.sin(ang)*0.45; leg.rotation.x = Math.cos(ang)*0.45;
                turret.add(leg);
            });
            const mount = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.2, 0.25, 16), mats.crimsonArmor);
            mount.position.y = 0.62; turret.add(mount);

            const gunHead = new THREE.Group(); gunHead.position.y = 0.82; turret.add(gunHead);
            const housing = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.24, 0.44), mats.obsidian);
            gunHead.add(housing);

            [-0.1, 0.1].forEach(bx => {
                const barrel = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.035, 0.72, 12), mats.chrome);
                barrel.rotation.x = Math.PI/2; barrel.position.set(bx, 0, 0.32);
                gunHead.add(barrel);
            });
            const coreLaser = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, 0.55, 12), mats.neonRed);
            coreLaser.rotation.x = Math.PI/2; coreLaser.position.set(0, 0, 0.28);
            gunHead.add(coreLaser);
        }
        else if (type === 'queen') {
            const boss = spawnRogueRobotGLB(0.28, 0x991b1b, mats.neonRed);
            dir.add(boss.wrapper);
            [-0.32, 0.32].forEach(sx => {
                const pauldron = new THREE.Mesh(new THREE.ConeGeometry(0.16, 0.42, 5), mats.crimsonArmor);
                pauldron.position.set(sx, 0.95, 0); pauldron.rotation.z = sx * -0.6;
                dir.add(pauldron);
            });
            const crownHorn = new THREE.Mesh(new THREE.TorusGeometry(0.22, 0.03, 8, 20), mats.neonRed);
            crownHorn.rotation.x = Math.PI/3; crownHorn.position.set(0, 1.28, 0);
            dir.add(crownHorn);

            root.userData.setAnim = boss.setAnim;
            root.userData.isMech = true;
        }
        else if (type === 'king') {
            const nexus = new THREE.Group(); dir.add(nexus);
            const ped = new THREE.Mesh(new THREE.CylinderGeometry(0.38, 0.45, 0.2, 8), mats.obsidian);
            ped.position.y = 0.1; nexus.add(ped);

            [0, 2.09, 4.18].forEach(a => {
                const pylon = new THREE.Mesh(new THREE.BoxGeometry(0.07, 1.1, 0.12), mats.crimsonArmor);
                pylon.position.set(Math.sin(a)*0.34, 0.6, Math.cos(a)*0.34);
                nexus.add(pylon);
            });

            const aiBrain = new THREE.Mesh(new THREE.IcosahedronGeometry(0.24, 2), mats.neonRed);
            aiBrain.position.y = 0.78; nexus.add(aiBrain);

            const gyro1 = new THREE.Mesh(new THREE.TorusGeometry(0.36, 0.022, 10, 32), mats.neonAmber);
            gyro1.position.y = 0.78; nexus.add(gyro1);
            const gyro2 = new THREE.Mesh(new THREE.TorusGeometry(0.42, 0.018, 10, 32), mats.chrome);
            gyro2.position.y = 0.78; nexus.add(gyro2);

            animatedParts.push({ mesh: aiBrain, type: 'spin' });
            animatedParts.push({ mesh: gyro1, type: 'gyro1' });
            animatedParts.push({ mesh: gyro2, type: 'gyro2' });
        }
    }

    dir.rotation.y = isBlue ? Math.PI : 0;
    root.userData.dirGroup = dir;
    return root;
}

function faceUnitTowards(unit, targetWorldX, targetWorldZ) {
    const dx = targetWorldX - unit.position.x;
    const dz = targetWorldZ - unit.position.z;
    if (Math.hypot(dx, dz) > 0.001) {
        unit.userData.dirGroup.rotation.y = Math.atan2(dx, dz);
    }
}

function resetUnitDefaultFacing(unit) {
    unit.userData.dirGroup.rotation.y = unit.userData.team === 'blue' ? Math.PI : 0;
}

// ============================================================================
// 5. SPESIFIKASI FAKSI ASIMETRIS & 5-STAGE FIGHTING CHOREOGRAPHY
// ============================================================================
let pieces = [], selectedPiece = null, validMoves = [], currentTurn = 'blue', isAnimating = false, vsAI = true, highlights = [];

const factionSpecs = {
    blue: {
        pawn:   { name: 'HUMAN OPERATOR (.GLB)', role: 'Human Corps • Pion', wpn: '⚡ Tactical Sprint & Crate Smash' },
        rook:   { name: 'HEAVY FORKLIFT', role: 'Human Corps • Benteng', wpn: '⚡ Hydraulic Fork Lift & Throw' },
        knight: { name: 'HOVER PALLET CRUISER', role: 'Human Corps • Kuda', wpn: '⚡ Supersonic Hover Drift Ram' },
        bishop: { name: 'QC LASER SNIPER', role: 'Human Corps • Gajah', wpn: '⚡ Precision Blue Laser Beam' },
        queen:  { name: 'EXO-SUIT COMMANDER', role: 'Human Corps • Menteri', wpn: '⚡ Twin Plasma Blade Slash' },
        king:   { name: 'MAIN WMS SERVER RACK', role: 'Human Corps • Raja', wpn: '⚡ Firewall Surge' }
    },
    orange: {
        pawn:   { name: 'ANDROID WORKER DRONE', role: 'Rogue AI • Pion Robot', wpn: '⚡ Hydraulic Servo Fist Combo' },
        rook:   { name: '6-LEG SPIDER TANK AGV', role: 'Rogue AI • Benteng Mekanik', wpn: '⚡ Molten Pincer Crush & Flip' },
        knight: { name: 'QUADCOPTER ASSAULT DRONE', role: 'Rogue AI • Kuda Udara', wpn: '⚡ Aerial Dive-Bomb Strike' },
        bishop: { name: 'TRIPOD RAILGUN SENTRY', role: 'Rogue AI • Gajah Turret', wpn: '⚡ Dual Crimson Railgun Barrage' },
        queen:  { name: 'GOLIATH CYBER-OVERLORD', role: 'Rogue AI • Menteri Bos', wpn: '⚡ 5-Hit Earthquake Mecha Smash' },
        king:   { name: 'AI SINGULARITY CORE', role: 'Rogue AI • Inti Reaktor', wpn: '⚡ Gravity Singularity Pulse' }
    }
};
const weights = { pawn: 10, knight: 30, bishop: 30, rook: 50, queen: 90, king: 900 };

function getUnitInfo(piece) {
    return factionSpecs[piece.userData.team][piece.userData.type];
}

function inspectUnitUI(piece) {
    const s = getUnitInfo(piece);
    document.getElementById('insp-name').innerText = s.name;
    document.getElementById('insp-role').innerText = s.role;
    document.getElementById('insp-weapon').innerText = s.wpn;
}

function showCombatBanner(text, duration = 950) {
    const b = document.getElementById('combat-banner');
    b.innerText = text; b.classList.add('show');
    setTimeout(() => b.classList.remove('show'), duration);
}

function showComboText(hits) {
    const c = document.getElementById('combo-counter');
    if (!hits) { c.classList.remove('show'); return; }
    c.innerText = `${hits} HIT COMBO!`; c.classList.add('show');
}

function setDuelHP(atkHP, defHP) {
    document.getElementById('duel-atk-bar').style.width = atkHP + '%';
    document.getElementById('duel-atk-hp-txt').innerText = atkHP + '%';
    document.getElementById('duel-def-bar').style.width = defHP + '%';
    document.getElementById('duel-def-hp-txt').innerText = defHP + '%';
}

function spawnImpactFX(pos, colorHex = 0x38bdf8, scaleMul = 1.0) {
    const ringGeo = new THREE.RingGeometry(0.12, 0.28 * scaleMul, 32);
    const ringMat = new THREE.MeshBasicMaterial({ color: colorHex, side: THREE.DoubleSide, transparent: true, opacity: 0.95 });
    const ring = new THREE.Mesh(ringGeo, ringMat);
    ring.rotation.x = -Math.PI / 2; ring.position.set(pos.x, 0.08, pos.z);
    scene.add(ring);

    let sc = 1;
    const expand = () => {
        sc += 0.38 * scaleMul; ring.scale.set(sc, sc, sc); ringMat.opacity -= 0.055;
        if (ringMat.opacity > 0) requestAnimationFrame(expand); else scene.remove(ring);
    };
    expand();

    const count = Math.floor(20 * scaleMul);
    for (let i = 0; i < count; i++) {
        const p = new THREE.Mesh(
            new THREE.BoxGeometry(0.1 * scaleMul, 0.1 * scaleMul, 0.1 * scaleMul),
            i % 2 === 0 ? mats.neonAmber : mats.neonRed
        );
        p.position.set(pos.x, pos.y + 0.55, pos.z); scene.add(p);
        const vx = (Math.random() - 0.5) * 0.36 * scaleMul;
        const vz = (Math.random() - 0.5) * 0.36 * scaleMul;
        let vy = (Math.random() * 0.28 + 0.08) * scaleMul;
        const tick = () => {
            p.position.x += vx; p.position.y += vy; p.position.z += vz; vy -= 0.015;
            p.rotation.x += 0.25; p.scale.multiplyScalar(0.92);
            if (p.scale.x > 0.02 && p.position.y > -0.3) requestAnimationFrame(tick); else scene.remove(p);
        };
        tick();
    }
}

function playEpicCombatSequence(attacker, defender, targetX, targetZ, onComplete) {
    document.body.classList.add('combat-mode');

    document.getElementById('duel-atk-name').innerText = getUnitInfo(attacker).name;
    document.getElementById('duel-def-name').innerText = getUnitInfo(defender).name;
    setDuelHP(100, 100);

    const startX = attacker.position.x, startZ = attacker.position.z;
    const endX = targetX * tileSize - offset, endZ = targetZ * tileSize - offset;
    const dx = endX - startX, dz = endZ - startZ;
    const dist = Math.hypot(dx, dz) || 1;
    const dirX = dx / dist, dirZ = dz / dist;

    const clashX = endX - dirX * 0.78;
    const clashZ = endZ - dirZ * 0.78;
    const midX = (clashX + endX) * 0.5;
    const midZ = (clashZ + endZ) * 0.5;

    faceUnitTowards(attacker, endX, endZ);
    faceUnitTowards(defender, startX, startZ);

    duelLight.position.set(midX, 3.5, midZ);
    duelLight.intensity = 2.2;

    showCombatBanner("⚔️ MANUSIA VS MESIN!", 800);

    if (attacker.userData.setAnim) attacker.userData.setAnim('Run', 1.3);
    if (defender.userData.setAnim) defender.userData.setAnim('Walk', 0.8);

    let p1 = 0;
    const stage1Approach = () => {
        p1 += 0.028;
        attacker.position.x = startX + (clashX - startX) * p1;
        attacker.position.z = startZ + (clashZ - startZ) * p1;

        const camAngle = Math.atan2(dirZ, dirX) + 1.25;
        camera.position.set(midX + Math.cos(camAngle) * 3.1, 1.85, midZ + Math.sin(camAngle) * 3.1);
        controls.target.set(midX, 0.65, midZ);
        controls.update();

        if (p1 < 1) requestAnimationFrame(stage1Approach);
        else {
            attacker.position.set(clashX, 0.05, clashZ);
            faceUnitTowards(attacker, endX, endZ);
            faceUnitTowards(defender, clashX, clashZ);
            stage2ClashAndCounter();
        }
    };

    let p2 = 0, hit1Done = false, counterDone = false;
    const stage2ClashAndCounter = () => {
        p2 += 0.022;
        const orbitAngle = Math.atan2(dirZ, dirX) + 1.25 + p2 * 0.6;
        camera.position.set(midX + Math.cos(orbitAngle) * 2.75, 1.65, midZ + Math.sin(orbitAngle) * 2.75);
        controls.target.set(midX, 0.65, midZ);
        controls.update();

        if (p2 < 0.45) {
            const lunge = Math.sin((p2 / 0.45) * Math.PI);
            attacker.position.x = clashX + dirX * lunge * 0.38;
            attacker.position.z = clashZ + dirZ * lunge * 0.38;
            if (attacker.userData.isMech && attacker.userData.setAnim) attacker.userData.setAnim('Punch', 1.4);

            if (p2 > 0.22 && !hit1Done) {
                hit1Done = true;
                spawnImpactFX(defender.position, 0x38bdf8, 0.8);
                setDuelHP(100, 72);
                showComboText(1);
            }
        } else {
            const counterTime = (p2 - 0.45) / 0.55;
            const defLunge = Math.sin(counterTime * Math.PI);
            defender.position.x = endX - dirX * defLunge * 0.42;
            defender.position.z = endZ - dirZ * defLunge * 0.42;
            if (defender.userData.isMech && defender.userData.setAnim) defender.userData.setAnim('Punch', 1.4);

            if (counterTime > 0.35 && !counterDone) {
                counterDone = true;
                spawnImpactFX(attacker.position, 0xef4444, 0.85);
                setDuelHP(82, 72);
                showCombatBanner("⚡ COUNTER CLASH!", 650);
            }
            attacker.position.x = clashX - dirX * Math.sin(counterTime * Math.PI) * 0.22;
            attacker.position.z = clashZ - dirZ * Math.sin(counterTime * Math.PI) * 0.22;
        }

        if (p2 < 1.0) requestAnimationFrame(stage2ClashAndCounter);
        else {
            defender.position.set(endX, 0.05, endZ);
            stage3ComboBarrage();
        }
    };

    let p3 = 0, comboHits = 1, laserMesh = null;
    if (attacker.userData.type === 'bishop') {
        laserMesh = new THREE.Mesh(
            new THREE.CylinderGeometry(0.05, 0.05, 1.1, 12),
            attacker.userData.team === 'blue' ? mats.neonBlue : mats.neonRed
        );
        laserMesh.rotation.x = Math.PI / 2;
        scene.add(laserMesh);
    }

    const stage3ComboBarrage = () => {
        p3 += 0.022;
        const orbitAngle = Math.atan2(dirZ, dirX) + 1.85 + p3 * 1.1;
        camera.position.set(midX + Math.cos(orbitAngle) * 2.35, 1.45, midZ + Math.sin(orbitAngle) * 2.35);
        controls.target.set(midX, 0.7, midZ);
        controls.update();

        const wave = Math.sin(p3 * Math.PI * 6);
        attacker.position.x = clashX + dirX * Math.max(0, wave) * 0.42;
        attacker.position.z = clashZ + dirZ * Math.max(0, wave) * 0.42;
        attacker.userData.dirGroup.rotation.y = Math.atan2(dx, dz) + Math.sin(p3 * 25) * 0.35;

        defender.position.x = endX + (Math.random() - 0.5) * 0.09;
        defender.position.z = endZ + (Math.random() - 0.5) * 0.09;

        if (laserMesh) {
            laserMesh.position.set(midX, 0.78, midZ);
            laserMesh.lookAt(endX, 0.78, endZ);
            laserMesh.visible = wave > 0;
        }
        if (attacker.userData.forkPivot) {
            attacker.userData.forkPivot.position.y = 0.14 + p3 * 0.65;
            defender.position.y = 0.05 + p3 * 0.75;
        }

        if (p3 > 0.25 && comboHits === 1) { comboHits = 2; showComboText(2); setDuelHP(82, 48); spawnImpactFX(defender.position, 0x38bdf8, 0.9); }
        if (p3 > 0.58 && comboHits === 2) { comboHits = 3; showComboText(3); setDuelHP(82, 24); spawnImpactFX(defender.position, 0xf59e0b, 1.0); }
        if (p3 > 0.85 && comboHits === 3) { comboHits = 4; showComboText(4); setDuelHP(82, 10); spawnImpactFX(defender.position, 0xef4444, 1.1); }

        if (p3 < 1.0) requestAnimationFrame(stage3ComboBarrage);
        else {
            if (laserMesh) scene.remove(laserMesh);
            faceUnitTowards(attacker, endX, endZ);
            stage4UltimateFinisher();
        }
    };

    let p4 = 0;
    const stage4UltimateFinisher = () => {
        const speed = (p4 > 0.35 && p4 < 0.7) ? 0.014 : 0.032;
        p4 += speed;

        attacker.position.x = clashX + (endX - clashX) * Math.min(1, p4 * 1.15);
        attacker.position.z = clashZ + (endZ - clashZ) * Math.min(1, p4 * 1.15);
        attacker.position.y = 0.05 + Math.sin(p4 * Math.PI) * 1.35;

        camera.position.y = 1.1 + Math.sin(p4 * Math.PI) * 0.4;
        controls.target.set(endX, 0.85, endZ);
        controls.update();

        if (p4 < 1.0) requestAnimationFrame(stage4UltimateFinisher);
        else {
            if (attacker.userData.forkPivot) attacker.userData.forkPivot.position.y = 0.14;
            attacker.position.set(endX, 0.05, endZ);
            setDuelHP(82, 0);
            showComboText(5);
            showCombatBanner("💀 TARGET OBLITERATED!", 1200);
            spawnImpactFX(defender.position, 0xef4444, 1.65);
            stage5KnockoutRagdoll();
        }
    };

    let p5 = 0;
    if (attacker.userData.isMech && attacker.userData.setAnim) attacker.userData.setAnim('Wave', 1.2);
    else if (attacker.userData.setAnim) attacker.userData.setAnim('Idle', 1.0);

    const stage5KnockoutRagdoll = () => {
        p5 += 0.04;
        if (p5 < 0.45) {
            camera.position.x += (Math.random() - 0.5) * 0.24;
            camera.position.y += (Math.random() - 0.5) * 0.24;
        }

        defender.position.x = endX + dirX * (p5 * 3.6);
        defender.position.z = endZ + dirZ * (p5 * 3.6);
        defender.position.y = 0.25 + Math.sin(p5 * Math.PI) * 2.1;
        defender.rotation.x += 0.28;
        defender.rotation.z += 0.22;
        defender.scale.multiplyScalar(0.94);

        if (p5 < 1.0) requestAnimationFrame(stage5KnockoutRagdoll);
        else {
            defender.userData.alive = false;
            scene.remove(defender);
            showComboText(0);
            duelLight.intensity = 0;
            resetUnitDefaultFacing(attacker);

            setTimeout(() => {
                document.body.classList.remove('combat-mode');
                camera.position.set(0, 10.6, 13.4);
                controls.target.set(0, 0.6, 0);
                controls.update();
                onComplete();
            }, 420);
        }
    };

    stage1Approach();
}

// ============================================================================
// 6. CHESS RULES & GAMEPLAY CONTROLLERS
// ============================================================================
function addBattleLog(text, isCombat = false) {
    const box = document.getElementById('move-history');
    const div = document.createElement('div');
    div.className = 'log-entry' + (isCombat ? ' combat' : '');
    div.innerText = text; box.prepend(div);
}

function updateScoreUI() {
    document.getElementById('score-blue').innerText = pieces.filter(p => p.userData.alive && p.userData.team === 'blue').length;
    document.getElementById('score-orange').innerText = pieces.filter(p => p.userData.alive && p.userData.team === 'orange').length;
}

function getPieceAt(gx, gz) {
    return pieces.find(p => p.userData.alive && p.userData.gridX === gx && p.userData.gridZ === gz);
}

function getValidMoves(piece) {
    const moves = [], { type, team, gridX: x, gridZ: z, hasMoved } = piece.userData, fwd = team === 'blue' ? -1 : 1;
    const add = (nx, nz) => {
        if (nx < 0 || nx > 7 || nz < 0 || nz > 7) return false;
        const occ = getPieceAt(nx, nz);
        if (!occ) { moves.push({ x: nx, z: nz, attack: false }); return true; }
        if (occ.userData.team !== team) { moves.push({ x: nx, z: nz, attack: true, target: occ }); }
        return false;
    };
    if (type === 'pawn') {
        if (!getPieceAt(x, z + fwd)) {
            moves.push({ x, z: z + fwd, attack: false });
            if (!hasMoved && !getPieceAt(x, z + fwd * 2)) moves.push({ x, z: z + fwd * 2, attack: false });
        }
        [-1, 1].forEach(dx => {
            const en = getPieceAt(x + dx, z + fwd);
            if (en && en.userData.team !== team) moves.push({ x: x + dx, z: z + fwd, attack: true, target: en });
        });
    }
    if (type === 'rook' || type === 'queen') [[1,0],[-1,0],[0,1],[0,-1]].forEach(([dx,dz]) => { for (let s=1; s<8; s++) if (!add(x+dx*s, z+dz*s)) break; });
    if (type === 'bishop' || type === 'queen') [[1,1],[1,-1],[-1,1],[-1,-1]].forEach(([dx,dz]) => { for (let s=1; s<8; s++) if (!add(x+dx*s, z+dz*s)) break; });
    if (type === 'knight') [[1,2],[2,1],[-1,2],[-2,1],[1,-2],[2,-1],[-1,-2],[-2,-1]].forEach(([dx,dz]) => add(x+dx, z+dz));
    if (type === 'king') [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]].forEach(([dx,dz]) => add(x+dx, z+dz));
    return moves;
}

function clearHighlights() { highlights.forEach(m => scene.remove(m)); highlights = []; }

function showHighlights(moves) {
    clearHighlights();
    moves.forEach(m => {
        const mk = new THREE.Mesh(
            new THREE.PlaneGeometry(tileSize * 0.84, tileSize * 0.84),
            new THREE.MeshBasicMaterial({ color: m.attack ? 0xef4444 : 0x22c55e, transparent: true, opacity: 0.55, side: THREE.DoubleSide })
        );
        mk.rotation.x = -Math.PI/2; mk.position.set(m.x * tileSize - offset, 0.065, m.z * tileSize - offset);
        scene.add(mk); highlights.push(mk);
    });
}

function executeMove(piece, moveData) {
    isAnimating = true; clearHighlights();
    const uName = getUnitInfo(piece).name;
    const coord = `${cols[moveData.x]}${8 - moveData.z}`;

    if (moveData.attack && moveData.target) {
        const victim = moveData.target;
        const vName = getUnitInfo(victim).name;
        updateHUD(`⚔️ DUEL ASIMETRIS: ${uName} vs ${vName}!`);

        playEpicCombatSequence(piece, victim, moveData.x, moveData.z, () => {
            piece.userData.gridX = moveData.x;
            piece.userData.gridZ = moveData.z;
            piece.userData.hasMoved = true;

            addBattleLog(`${uName} 💀 K.O. ${vName} (${coord})`, true);
            updateScoreUI();

            if (victim.userData.type === 'king') {
                updateHUD(`🏆 VICTORY! Faksi ${currentTurn === 'blue' ? 'MANUSIA' : 'ROGUE AI'} memenangkan pertempuran gudang!`);
                isAnimating = false; return;
            }

            currentTurn = currentTurn === 'blue' ? 'orange' : 'blue';
            selectedPiece = null; validMoves = []; isAnimating = false;
            updateHUD(`💥 ${uName} menghancurkan lawan di zona ${coord}!`);
            if (vsAI && currentTurn === 'orange') setTimeout(runAIBot, 500);
        });
        return;
    }

    const sx = piece.position.x, sz = piece.position.z;
    const ex = moveData.x * tileSize - offset, ez = moveData.z * tileSize - offset;
    faceUnitTowards(piece, ex, ez);
    if (piece.userData.setAnim) piece.userData.setAnim('Run', 1.15);

    let prog = 0;
    const step = () => {
        prog += 0.05;
        if (prog < 1) {
            piece.position.x = sx + (ex - sx) * prog;
            piece.position.z = sz + (ez - sz) * prog;
            requestAnimationFrame(step);
        } else {
            if (piece.userData.setAnim) piece.userData.setAnim('Idle', 1.0);
            piece.position.set(ex, 0.05, ez);
            piece.userData.gridX = moveData.x; piece.userData.gridZ = moveData.z; piece.userData.hasMoved = true;
            resetUnitDefaultFacing(piece);

            addBattleLog(`${uName} ➔ ${coord}`, false);
            currentTurn = currentTurn === 'blue' ? 'orange' : 'blue';
            selectedPiece = null; validMoves = []; isAnimating = false;
            updateHUD(`${uName} mengamankan zona ${coord}.`);
            if (vsAI && currentTurn === 'orange') setTimeout(runAIBot, 450);
        }
    };
    step();
}

function demoCombat() {
    if (isAnimating) return;
    const blueUnits = pieces.filter(p => p.userData.alive && p.userData.team === 'blue' && p.userData.type !== 'king');
    const orangeUnits = pieces.filter(p => p.userData.alive && p.userData.team === 'orange' && p.userData.type !== 'king');
    if (!blueUnits.length || !orangeUnits.length) return;

    const atk = blueUnits[Math.floor(Math.random() * blueUnits.length)];
    const def = orangeUnits[Math.floor(Math.random() * orangeUnits.length)];
    currentTurn = 'blue';
    executeMove(atk, { x: def.userData.gridX, z: def.userData.gridZ, attack: true, target: def });
}

function runAIBot() {
    const aiPieces = pieces.filter(p => p.userData.alive && p.userData.team === 'orange');
    let allMoves = [];
    aiPieces.forEach(p => {
        getValidMoves(p).forEach(m => {
            let score = m.attack && m.target ? weights[m.target.userData.type] * 2.2 : (m.z * 0.5 + Math.random() * 2);
            allMoves.push({ piece: p, move: m, score });
        });
    });
    if (!allMoves.length) return;
    allMoves.sort((a, b) => b.score - a.score);
    executeMove(allMoves[0].piece, allMoves[0].move);
}

function spawnUnit(type, team, gx, gz) {
    const m = createUnitMesh(type, team);
    m.position.set(gx * tileSize - offset, 0.05, gz * tileSize - offset);
    m.userData = Object.assign(m.userData || {}, { type, team, gridX: gx, gridZ: gz, alive: true, hasMoved: false });
    scene.add(m); pieces.push(m);
}

function resetGame() {
    clearHighlights(); pieces.forEach(p => scene.remove(p)); pieces = [];
    mixers.length = 0; animatedParts.length = 0;
    document.getElementById('move-history').innerHTML = '';
    selectedPiece = null; validMoves = []; currentTurn = 'blue'; isAnimating = false;
    const row = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook'];
    for (let i = 0; i < 8; i++) {
        spawnUnit(row[i], 'orange', i, 0); spawnUnit('pawn', 'orange', i, 1);
        spawnUnit('pawn', 'blue', i, 6); spawnUnit(row[i], 'blue', i, 7);
    }
    updateScoreUI();
    addBattleLog("Developed by iqbalmantam • Engine Ready.");
    updateHUD("Warehouse Command 3D • Developed by iqbalmantam. Klik bidak Biru atau '🔥 Duel Manusia vs Robot!'");
}

function updateHUD(msg) {
    const b = document.getElementById('turn-banner');
    b.className = currentTurn === 'blue' ? 'turn-blue' : 'turn-orange';
    b.innerText = currentTurn === 'blue' ? 'GILIRAN MANUSIA' : 'GILIRAN ROGUE AI';
    if (msg) document.getElementById('action-log').innerText = msg;
}

function toggleAI() {
    vsAI = !vsAI;
    const btn = document.getElementById('btn-ai');
    btn.innerText = vsAI ? '🤖 Lawan AI' : '👥 2 Player';
    btn.classList.toggle('active', vsAI);
}

function setCameraView(mode) {
    if (mode === 'enemy') {
        camera.position.set(0, 3.2, -0.5); controls.target.set(0, 0.6, -3.6);
    } else {
        camera.position.set(0, 10.6, 13.4); controls.target.set(0, 0.6, 0);
    }
    controls.update();
}

const raycaster = new THREE.Raycaster(), mouse = new THREE.Vector2();
window.addEventListener('pointerdown', (e) => {
    if (isAnimating || e.target.tagName === 'BUTTON' || (vsAI && currentTurn === 'orange')) return;
    mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
    raycaster.setFromCamera(mouse, camera);

    let coords = null;
    const tHits = raycaster.intersectObjects(tiles.flat());
    if (tHits.length > 0) {
        coords = { x: tHits[0].object.userData.gridX, z: tHits[0].object.userData.gridZ };
    } else {
        const pHits = raycaster.intersectObjects(pieces.filter(p => p.userData.alive), true);
        if (pHits.length > 0) {
            let o = pHits[0].object;
            while (o.parent && !o.userData.type) o = o.parent;
            if (o.userData && o.userData.alive) coords = { x: o.userData.gridX, z: o.userData.gridZ };
        }
    }
    if (!coords) return;

    if (selectedPiece) {
        const mv = validMoves.find(m => m.x === coords.x && m.z === coords.z);
        if (mv) { executeMove(selectedPiece, mv); return; }
    }

    const unit = getPieceAt(coords.x, coords.z);
    if (unit) inspectUnitUI(unit);

    if (unit && unit.userData.team === currentTurn) {
        selectedPiece = unit; validMoves = getValidMoves(unit); showHighlights(validMoves);
        updateHUD(`Unit Siap: ${getUnitInfo(unit).name} (${cols[coords.x]}${8 - coords.z})`);
    } else {
        selectedPiece = null; validMoves = []; clearHighlights();
    }
});

const clock = new THREE.Clock();
loadAllBlenderAssets();

function animate() {
    requestAnimationFrame(animate);
    const delta = clock.getDelta();
    const elapsed = clock.getElapsedTime();

    mixers.forEach(m => m.update(delta));

    animatedParts.forEach(p => {
        if (p.type === 'spin') { p.mesh.rotation.y = elapsed * 2.2; p.mesh.rotation.x = elapsed * 1.1; }
        else if (p.type === 'hover') { p.mesh.position.y = p.baseY + Math.sin(elapsed * 3.8) * 0.06; }
        else if (p.type === 'rotor') { p.mesh.rotation.y = elapsed * 28.0; }
        else if (p.type === 'gyro1') { p.mesh.rotation.x = elapsed * 2.5; p.mesh.rotation.y = elapsed * 1.5; }
        else if (p.type === 'gyro2') { p.mesh.rotation.z = elapsed * 2.8; p.mesh.rotation.y = -elapsed * 1.8; }
    });

    controls.update();
    composer.render();
}
animate();

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    composer.setSize(window.innerWidth, window.innerHeight);
});
</script>
</body>
</html>'''

components.html(HTML_CODE, height=900, scrolling=False)
