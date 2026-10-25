import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="WAREHOUSE COMMAND: ULTRA-REALISTIC 3D",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding: 0 !important; margin: 0 !important; max-width: 100% !important;}
    .stApp {background-color: #05070b; overflow: hidden;}
    iframe {display: block; border: none; width: 100vw !important; height: 100vh !important;}
</style>
""", unsafe_allow_html=True)

HTML_CODE = r'''<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Warehouse Command: Ultra-Realistic</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=Rajdhani:wght@500;600;700&display=swap" rel="stylesheet">
<style>
    * { box-sizing: border-box; user-select: none; }
    body { margin: 0; padding: 0; overflow: hidden; background: #05070b; font-family: 'Rajdhani', sans-serif; color: #e2e8f0; }
    #canvas-container { width: 100vw; height: 100vh; display: block; }
    #vignette { position: fixed; inset: 0; pointer-events: none; z-index: 2; background: radial-gradient(circle at center, transparent 55%, rgba(3, 6, 12, 0.78) 100%); }
    
    #top-bar {
        position: absolute; top: 0; left: 0; right: 0; height: 68px;
        background: linear-gradient(180deg, rgba(9, 13, 22, 0.96) 0%, rgba(9, 13, 22, 0.75) 100%);
        border-bottom: 1px solid rgba(56, 189, 248, 0.22);
        display: flex; justify-content: space-between; align-items: center;
        padding: 0 24px; z-index: 10; backdrop-filter: blur(12px);
    }
    .brand-cluster { display: flex; align-items: center; gap: 14px; }
    .brand-emblem {
        width: 42px; height: 42px; border-radius: 8px;
        background: linear-gradient(135deg, #f59e0b 0%, #b45309 100%);
        display: flex; align-items: center; justify-content: center;
        font-family: 'Orbitron', sans-serif; font-weight: 900; font-size: 20px; color: #05070b;
        box-shadow: 0 0 15px rgba(245, 158, 11, 0.4);
    }
    .brand-title h1 { margin: 0; font-family: 'Orbitron', sans-serif; font-size: 16px; font-weight: 800; letter-spacing: 2px; color: #f8fafc; }
    .brand-title span { font-size: 11px; color: #f59e0b; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700; display: block; }

    .versus-hud {
        display: flex; align-items: center; gap: 18px;
        background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(148, 163, 184, 0.2);
        padding: 6px 22px; border-radius: 40px;
    }
    .team-score { display: flex; align-items: center; gap: 10px; font-weight: 700; font-size: 14px; letter-spacing: 1px; }
    .team-score.blue { color: #38bdf8; }
    .team-score.orange { color: #fbbf24; }
    .score-pill { background: rgba(2, 6, 23, 0.8); padding: 2px 10px; border-radius: 12px; font-family: 'Orbitron', sans-serif; font-size: 14px; border: 1px solid currentColor; }
    #turn-banner {
        padding: 5px 16px; border-radius: 20px; font-family: 'Orbitron', sans-serif; font-size: 11px; font-weight: 800;
        letter-spacing: 1.5px; text-transform: uppercase;
    }
    .turn-blue { background: rgba(2, 132, 199, 0.3); color: #38bdf8; border: 1px solid #38bdf8; }
    .turn-orange { background: rgba(217, 119, 6, 0.3); color: #fbbf24; border: 1px solid #fbbf24; }

    .toolbar { display: flex; gap: 8px; }
    .t-btn {
        background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(148, 163, 184, 0.3);
        color: #cbd5e1; padding: 8px 13px; border-radius: 6px; font-family: 'Rajdhani', sans-serif;
        font-weight: 700; font-size: 13px; letter-spacing: 0.8px; text-transform: uppercase; cursor: pointer; transition: 0.2s;
    }
    .t-btn:hover { background: rgba(56, 189, 248, 0.15); border-color: #38bdf8; color: #fff; }
    .t-btn.active { background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%); border-color: #38bdf8; color: #fff; }

    #unit-inspector {
        position: absolute; top: 86px; left: 20px; width: 270px;
        background: linear-gradient(160deg, rgba(11, 17, 30, 0.92) 0%, rgba(7, 11, 20, 0.95) 100%);
        border: 1px solid rgba(56, 189, 248, 0.28); border-left: 4px solid #38bdf8;
        border-radius: 8px; padding: 14px 16px; z-index: 10; backdrop-filter: blur(10px);
    }
    .panel-tag { font-family: 'Orbitron', sans-serif; font-size: 10px; color: #64748b; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 4px; }
    #insp-name { font-family: 'Orbitron', sans-serif; font-size: 15px; font-weight: 800; color: #f8fafc; margin: 0 0 2px 0; }
    #insp-role { font-size: 12px; color: #f59e0b; font-weight: 700; margin-bottom: 10px; }
    .stat-row { margin: 6px 0; }
    .stat-label { display: flex; justify-content: space-between; font-size: 11px; color: #94a3b8; font-weight: 600; margin-bottom: 3px; }
    .stat-bar { height: 5px; background: rgba(30, 41, 59, 0.9); border-radius: 3px; overflow: hidden; }
    .stat-fill { height: 100%; background: linear-gradient(90deg, #0284c7, #38bdf8); }
    .roster-mini { margin-top: 12px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.08); font-size: 11px; color: #94a3b8; line-height: 1.55; }
    .roster-mini b { color: #e2e8f0; }

    #ops-panel {
        position: absolute; top: 86px; right: 20px; width: 265px;
        background: linear-gradient(160deg, rgba(11, 17, 30, 0.9) 0%, rgba(7, 11, 20, 0.94) 100%);
        border: 1px solid rgba(245, 158, 11, 0.25); border-right: 4px solid #f59e0b;
        border-radius: 8px; padding: 14px 16px; z-index: 10; backdrop-filter: blur(10px);
    }
    #move-history { max-height: 150px; overflow-y: auto; font-size: 12px; display: flex; flex-direction: column; gap: 5px; margin-top: 8px; padding-right: 4px; }
    .log-entry { background: rgba(15, 23, 42, 0.75); padding: 5px 8px; border-radius: 4px; border-left: 2px solid #475569; color: #cbd5e1; font-size: 11.5px; }
    .log-entry.combat { border-left-color: #ef4444; background: rgba(127, 29, 29, 0.25); color: #fca5a5; }

    #bottom-ticker {
        position: absolute; bottom: 18px; left: 50%; transform: translateX(-50%);
        background: rgba(9, 13, 22, 0.92); border: 1px solid rgba(56, 189, 248, 0.3);
        padding: 10px 28px; border-radius: 30px; display: flex; align-items: center; gap: 12px; z-index: 10; font-size: 14px; font-weight: 600;
    }
    .pulse-dot { width: 9px; height: 9px; border-radius: 50%; background: #22c55e; box-shadow: 0 0 10px #22c55e; }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>
    <div id="vignette"></div>

    <div id="top-bar">
        <div class="brand-cluster">
            <div class="brand-emblem">WC</div>
            <div class="brand-title">
                <h1>WAREHOUSE COMMAND</h1>
                <span>Ultra-Realistic Human Anatomy • 3D Simulator</span>
            </div>
        </div>

        <div class="versus-hud">
            <div class="team-score blue"><span>INBOUND</span><span id="score-blue" class="score-pill">16</span></div>
            <div id="turn-banner" class="turn-blue">SHIFT BIRU AKTIF</div>
            <div class="team-score orange"><span id="score-orange" class="score-pill">16</span><span>OUTBOUND</span></div>
        </div>

        <div class="toolbar">
            <button id="btn-ai" class="t-btn active" onclick="toggleAI()">🤖 vs AI Bot</button>
            <button class="t-btn" onclick="setCameraView('closeup')">🔍 Close-Up Anatomi</button>
            <button class="t-btn" onclick="setCameraView('perspective')">🎥 Kamera Taktis</button>
            <button class="t-btn" onclick="setCameraView('top')">📐 Radar Atas</button>
            <button class="t-btn" onclick="resetGame()">🔄 Reset Shift</button>
        </div>
    </div>

    <div id="unit-inspector">
        <div class="panel-tag">UNIT TELEMETRY INSPECTOR</div>
        <h2 id="insp-name">OPERATOR PICKER</h2>
        <div id="insp-role">Frontline Logistics • Pion</div>
        <div class="stat-row">
            <div class="stat-label"><span>AGILITY / KELINCAHAN</span><span id="st-pow-val">75%</span></div>
            <div class="stat-bar"><div id="st-pow" class="stat-fill" style="width:75%"></div></div>
        </div>
        <div class="stat-row">
            <div class="stat-label"><span>WORK CAPACITY</span><span id="st-rng-val">80%</span></div>
            <div class="stat-bar"><div id="st-rng" class="stat-fill" style="width:80%"></div></div>
        </div>
        <div class="roster-mini">
            <div><b>Pion:</b> Operator Picker (Manusia Asli)</div>
            <div><b>Benteng:</b> Forklift + Driver Manusia</div>
            <div><b>Kuda:</b> Reach Truck + Operator</div>
            <div><b>Gajah:</b> QC Auditor (Laser Scanner)</div>
            <div><b>Menteri:</b> Ops Supervisor</div>
            <div><b>Raja:</b> WMS Server Core</div>
        </div>
    </div>

    <div id="ops-panel">
        <div class="panel-tag">WMS OPERATIONS LOG</div>
        <div style="font-size:12px; color:#f59e0b; font-weight:700;">TRANSMISI GUDANG AKTIF</div>
        <div id="move-history"></div>
    </div>

    <div id="bottom-ticker">
        <div class="pulse-dot"></div>
        <div id="action-log">Sistem WMS Online. Anatomi manusia realistis aktif. Pilih unit untuk melangkah.</div>
    </div>

    <div id="canvas-container"></div>

<script>
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x05070b);
scene.fog = new THREE.FogExp2(0x05070b, 0.014);

const camera = new THREE.PerspectiveCamera(38, window.innerWidth / window.innerHeight, 0.1, 220);
camera.position.set(0, 11.2, 14.2);

const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 0.72;
renderer.outputEncoding = THREE.sRGBEncoding;
container.appendChild(renderer.domElement);

const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.maxPolarAngle = Math.PI / 2 - 0.03;
controls.minDistance = 3.8;
controls.maxDistance = 26;
controls.target.set(0, 0.5, 0);

const ambient = new THREE.HemisphereLight(0x93c5fd, 0x090d16, 0.45);
scene.add(ambient);
const sunLight = new THREE.DirectionalLight(0xfff1e0, 1.15);
sunLight.position.set(9, 19, 11);
sunLight.castShadow = true;
sunLight.shadow.mapSize.set(2048, 2048);
const d = 8.2;
Object.assign(sunLight.shadow.camera, { left: -d, right: d, top: d, bottom: -d, near: 2, far: 42 });
sunLight.shadow.bias = -0.0004;
scene.add(sunLight);

const rimBlue = new THREE.PointLight(0x0284c7, 0.85, 26); rimBlue.position.set(-10, 6, 9); scene.add(rimBlue);
const rimAmber = new THREE.PointLight(0xd97706, 0.85, 26); rimAmber.position.set(10, 6, -9); scene.add(rimAmber);

function makeHazardTex() {
    const c = document.createElement('canvas'); c.width = 256; c.height = 256;
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#ca8a04'; ctx.fillRect(0,0,256,256);
    ctx.fillStyle = '#090d16';
    for (let i = -256; i < 512; i += 64) {
        ctx.beginPath(); ctx.moveTo(i,0); ctx.lineTo(i+32,0); ctx.lineTo(i-224,256); ctx.lineTo(i-256,256); ctx.fill();
    }
    const t = new THREE.CanvasTexture(c);
    t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(12, 1);
    return t;
}

function makeTileTex(isDark, lbl) {
    const c = document.createElement('canvas'); c.width = 256; c.height = 256;
    const ctx = c.getContext('2d');
    ctx.fillStyle = isDark ? '#0f172a' : '#1e293b'; ctx.fillRect(0,0,256,256);
    ctx.strokeStyle = isDark ? '#1e293b' : '#334155'; ctx.lineWidth = 8; ctx.strokeRect(4,4,248,248);
    ctx.fillStyle = 'rgba(234, 179, 8, 0.35)'; ctx.fillRect(14,14,16,3); ctx.fillRect(14,14,3,16);
    ctx.fillRect(226,14,16,3); ctx.fillRect(239,14,3,16);
    if (lbl) {
        ctx.fillStyle = isDark ? 'rgba(148,163,184,0.45)' : 'rgba(203,213,225,0.55)';
        ctx.font = 'bold 30px Orbitron, monospace'; ctx.fillText(lbl, 18, 234);
    }
    return new THREE.CanvasTexture(c);
}

function makeCardboardTex() {
    const c = document.createElement('canvas'); c.width = 256; c.height = 256;
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#9a6b3e'; ctx.fillRect(0,0,256,256);
    ctx.fillStyle = '#704822'; ctx.fillRect(0, 114, 256, 28);
    ctx.fillStyle = '#e2e8f0'; ctx.fillRect(24, 28, 92, 58);
    ctx.fillStyle = '#0f172a';
    for(let b=32; b<108; b+=6) ctx.fillRect(b, 36, (b%12===0)?4:2, 32);
    return new THREE.CanvasTexture(c);
}

const boardGroup = new THREE.Group(); scene.add(boardGroup);
const warehouseFloor = new THREE.Mesh(new THREE.PlaneGeometry(80, 80), new THREE.MeshStandardMaterial({ color: 0x070a12, roughness: 0.75 }));
warehouseFloor.rotation.x = -Math.PI/2; warehouseFloor.position.y = -0.36; warehouseFloor.receiveShadow = true; scene.add(warehouseFloor);

const base = new THREE.Mesh(new THREE.BoxGeometry(10.6, 0.36, 10.6), new THREE.MeshStandardMaterial({ color: 0x0b111e, roughness: 0.4 }));
base.position.y = -0.2; base.receiveShadow = true; boardGroup.add(base);

const hazMat = new THREE.MeshStandardMaterial({ map: makeHazardTex(), roughness: 0.5 });
[[0,-4.96,10.2,0.24],[0,4.96,10.2,0.24],[-4.96,0,0.24,10.2],[4.96,0,0.24,10.2]].forEach(([x,z,w,l]) => {
    const b = new THREE.Mesh(new THREE.BoxGeometry(w, 0.12, l), hazMat);
    b.position.set(x, -0.02, z); boardGroup.add(b);
});

const tileSize = 1.2, offset = 3.5 * tileSize, tiles = [], cols = ['A','B','C','D','E','F','G','H'];
for (let x = 0; x < 8; x++) {
    tiles[x] = [];
    for (let z = 0; z < 8; z++) {
        const isDark = (x + z) % 2 === 1;
        const lbl = (z === 7) ? cols[x] : (x === 0 ? String(8 - z) : '');
        const tile = new THREE.Mesh(
            new THREE.BoxGeometry(tileSize * 0.985, 0.1, tileSize * 0.985),
            new THREE.MeshStandardMaterial({ map: makeTileTex(isDark, lbl), roughness: 0.48 })
        );
        tile.position.set(x * tileSize - offset, 0, z * tileSize - offset);
        tile.receiveShadow = true; tile.userData = { gridX: x, gridZ: z };
        boardGroup.add(tile); tiles[x][z] = tile;
    }
}

const boxTex = makeCardboardTex();
function buildRack(xPos, zPos, rotY) {
    const r = new THREE.Group();
    const uMat = new THREE.MeshStandardMaterial({ color: 0x1e3a8a, roughness: 0.4 });
    const bMat = new THREE.MeshStandardMaterial({ color: 0xc2410c, roughness: 0.4 });
    const cMat = new THREE.MeshStandardMaterial({ map: boxTex, roughness: 0.75 });
    [-1.8, 0, 1.8].forEach(lx => [-0.42, 0.42].forEach(lz => {
        const p = new THREE.Mesh(new THREE.BoxGeometry(0.09, 3.8, 0.09), uMat);
        p.position.set(lx, 1.9, lz); p.castShadow = true; r.add(p);
    }));
    [0.85, 1.95, 3.05].forEach(ly => {
        [-0.42, 0.42].forEach(bz => {
            const bm = new THREE.Mesh(new THREE.BoxGeometry(3.7, 0.09, 0.07), bMat);
            bm.position.set(0, ly, bz); r.add(bm);
        });
        [-1.1, 0, 1.1].forEach(bx => {
            const bxMesh = new THREE.Mesh(new THREE.BoxGeometry(0.66, 0.5, 0.66), cMat);
            bxMesh.position.set(bx, ly + 0.3, 0); bxMesh.castShadow = true; r.add(bxMesh);
        });
    });
    r.position.set(xPos, -0.35, zPos); r.rotation.y = rotY; scene.add(r);
}
buildRack(-7.8, -2.4, Math.PI/2); buildRack(-7.8, 2.4, Math.PI/2);
buildRack(7.8, -2.4, -Math.PI/2); buildRack(7.8, 2.4, -Math.PI/2);

const HUMAN_WALKERS = ['pawn', 'bishop', 'queen'];
let activeMove = null;

const mats = {
    skin: new THREE.MeshStandardMaterial({ color: 0xd99b72, roughness: 0.55 }),
    hair: new THREE.MeshStandardMaterial({ color: 0x18130f, roughness: 0.8 }),
    cargoPants: new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.85 }),
    blackSteel: new THREE.MeshStandardMaterial({ color: 0x0f172a, metalness: 0.65, roughness: 0.4 }),
    chrome: new THREE.MeshStandardMaterial({ color: 0xe2e8f0, metalness: 0.9, roughness: 0.15 }),
    rubberTire: new THREE.MeshStandardMaterial({ color: 0x090d16, roughness: 0.92 }),
    leather: new THREE.MeshStandardMaterial({ color: 0x1c1917, roughness: 0.5 }),
    cardboard: new THREE.MeshStandardMaterial({ map: boxTex, roughness: 0.78 }),
    woodPallet: new THREE.MeshStandardMaterial({ color: 0x855832, roughness: 0.88 }),
    hiVisLime: new THREE.MeshStandardMaterial({ color: 0x84cc16, roughness: 0.45 }),
    hiVisOrange: new THREE.MeshStandardMaterial({ color: 0xea580c, roughness: 0.45 }),
    silverReflective: new THREE.MeshStandardMaterial({ color: 0xcbd5e1, metalness: 0.6, roughness: 0.3 }),
    whiteHelmet: new THREE.MeshStandardMaterial({ color: 0xf1f5f9, roughness: 0.3 }),
    goldHelmet: new THREE.MeshStandardMaterial({ color: 0xf59e0b, roughness: 0.25, metalness: 0.45 }),
    visorGlass: new THREE.MeshStandardMaterial({ color: 0x0284c7, roughness: 0.15, metalness: 0.8 }),
    serverGlass: new THREE.MeshStandardMaterial({ color: 0x090d16, roughness: 0.15, transparent: true, opacity: 0.7 }),
    amberBeacon: new THREE.MeshStandardMaterial({ color: 0xf59e0b, emissive: 0xd97706, emissiveIntensity: 1.0 })
};

function makeDetailedWheel(radius, width, rimMat) {
    const wGroup = new THREE.Group();
    const tire = new THREE.Mesh(new THREE.CylinderGeometry(radius, radius, width, 20), mats.rubberTire);
    tire.rotation.z = Math.PI / 2; tire.castShadow = true; wGroup.add(tire);
    const rim = new THREE.Mesh(new THREE.CylinderGeometry(radius * 0.55, radius * 0.55, width + 0.01, 14), rimMat);
    rim.rotation.z = Math.PI / 2; wGroup.add(rim);
    return wGroup;
}

function makeEuroPallet(w, l) {
    const p = new THREE.Group();
    for (let i = -2; i <= 2; i++) {
        const slat = new THREE.Mesh(new THREE.BoxGeometry(w, 0.02, l * 0.16), mats.woodPallet);
        slat.position.set(0, 0.06, i * (l * 0.2)); slat.castShadow = true; p.add(slat);
    }
    return p;
}

// =====================================================================
//  MANUSIA REALISTIS: rangka sendi (rig) + mesh organik
//  Proporsi dewasa (~7 kepala), tinggi total ±1.14 unit:
//  telapak kaki -> lutut -> pinggul -> pinggang -> dada/bahu -> leher -> kepala
//  Setiap segmen tubuh = 1 mesh gabungan (vertex color) supaya ringan.
// =====================================================================
const DIM = {
    ankleH: 0.05, shin: 0.245, thigh: 0.255, hipX: 0.062,
    spineUp: 0.07, shoulderX: 0.135, shoulderY: 0.28,
    upperArm: 0.20, foreArm: 0.175
};
DIM.hipY = DIM.ankleH + DIM.shin + DIM.thigh;   // 0.55

const humanMat = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.72, metalness: 0.0 });
const hardMat  = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.28, metalness: 0.2 });

const SKIN_TONES = [0xd99b72, 0xc58c5a, 0xe4b48a, 0x9a643c, 0x7a4a2b, 0xefc7a0];
const HAIR_TONES = [0x18130f, 0x2b1d14, 0x3d2a1c, 0x0d0d0d, 0x4a3320];

const _geoCache = {};
function cached(key, make) { return _geoCache[key] || (_geoCache[key] = make()); }
const sphG = () => cached('sph', () => new THREE.SphereGeometry(1, 14, 10));
const boxG = () => cached('box', () => new THREE.BoxGeometry(1, 1, 1));

const ellP   = (color, pos, scale, rot) => ({ geo: sphG(), color, pos, scale, rot });
const boxP   = (color, pos, scale, rot) => ({ geo: boxG(), color, pos, scale, rot });
const cylP   = (color, pos, rt, rb, h, rot, scale) => ({ geo: cached(`cyl${rt}_${rb}_${h}`, () => new THREE.CylinderGeometry(rt, rb, h, 14, 1)), color, pos, rot, scale });
const torusP = (color, pos, R, tube, rot, scale) => ({ geo: cached(`tor${R}_${tube}`, () => new THREE.TorusGeometry(R, tube, 6, 24)), color, pos, rot, scale });
const latheP = (key, color, pos, pts, scale, rot) => ({
    geo: cached('lat' + key, () => new THREE.LatheGeometry(pts.map(([r, y]) => new THREE.Vector2(r, y)), 16)),
    color, pos, scale, rot
});

// profil anggota badan: prof = [[t(0 atas -> 1 bawah), radius], ...]
function limbPts(len, prof, capped = true) {
    const pts = [];
    if (capped) pts.push([0, -len]);
    for (let i = prof.length - 1; i >= 0; i--) pts.push([prof[i][1], -prof[i][0] * len]);
    if (capped) pts.push([0, 0]);
    return pts;
}

function mergeParts(parts) {
    const pos = [], nor = [], col = [], idx = [];
    let base = 0;
    const q = new THREE.Quaternion(), e = new THREE.Euler(), mtx = new THREE.Matrix4(), c = new THREE.Color();
    parts.forEach(p => {
        const g = p.geo.clone();
        const r = p.rot || [0, 0, 0], s = p.scale || [1, 1, 1], t = p.pos || [0, 0, 0];
        e.set(r[0], r[1], r[2]); q.setFromEuler(e);
        mtx.compose(new THREE.Vector3(t[0], t[1], t[2]), q, new THREE.Vector3(s[0], s[1], s[2]));
        g.applyMatrix4(mtx);
        const pa = g.attributes.position, na = g.attributes.normal;
        c.set(p.color);
        for (let i = 0; i < pa.count; i++) {
            pos.push(pa.getX(i), pa.getY(i), pa.getZ(i));
            nor.push(na.getX(i), na.getY(i), na.getZ(i));
            col.push(c.r, c.g, c.b);
        }
        const ia = g.index;
        for (let i = 0; i < ia.count; i++) idx.push(ia.getX(i) + base);
        base += pa.count;
        g.dispose();
    });
    const out = new THREE.BufferGeometry();
    out.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    out.setAttribute('normal', new THREE.Float32BufferAttribute(nor, 3));
    out.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
    out.setIndex(idx);
    return out;
}

function makeMesh(parts, mat) {
    const m = new THREE.Mesh(mergeParts(parts), mat);
    m.castShadow = true;
    return m;
}

function buildHuman(o) {
    const sk = o.skin, hr = o.hair, shirt = o.shirt, pantsC = o.pants || 0x1e293b;
    const bootC = 0x1c1917, silver = 0xcbd5e1;
    const lipC = new THREE.Color(sk).lerp(new THREE.Color(0x8a2f2f), 0.5).getHex();

    const rig = {
        root: new THREE.Group(), legs: [], arms: [],
        seated: false, canWalk: false, carry: false,
        phase: Math.random() * 6.28, k: 0, amp: 0.6, ip: Math.random() * 6.28
    };

    const hips = new THREE.Group(); hips.position.y = DIM.hipY; rig.root.add(hips);
    const spine = new THREE.Group(); spine.position.y = DIM.spineUp; hips.add(spine);
    const head = new THREE.Group(); head.position.set(0, 0.435, -0.006); spine.add(head);
    rig.hips = hips; rig.spine = spine; rig.head = head;

    // ---------------- PANGGUL ----------------
    const pelvisParts = [
        latheP('pelvis', pantsC, [0, 0, 0],
            [[0, -0.1], [0.07, -0.095], [0.1, -0.075], [0.113, -0.035], [0.113, 0], [0.105, 0.035], [0.095, 0.062], [0.09, 0.068], [0, 0.07]],
            [1, 1, 0.66]),
        cylP(0x1c1917, [0, 0.05, 0], 0.104, 0.106, 0.024, null, [1, 1, 0.68]),      // ikat pinggang
        boxP(0x9ca3af, [0, 0.05, -0.0735], [0.024, 0.018, 0.006])                    // gesper
    ];
    hips.add(makeMesh(pelvisParts, humanMat));

    // ---------------- TORSO (dada bidang, pinggang ramping, bahu) ----------------
    const torsoParts = [
        latheP('torso', shirt, [0, 0, 0],
            [[0, -0.012], [0.086, -0.012], [0.086, 0.04], [0.092, 0.1], [0.1, 0.17], [0.107, 0.225], [0.108, 0.26],
             [0.101, 0.29], [0.082, 0.31], [0.055, 0.325], [0.04, 0.333], [0, 0.335]],
            [1, 1, 0.68]),
        ellP(shirt, [0, 0.283, 0.004], [0.125, 0.04, 0.058]),                        // otot trapezius / garis bahu
        torusP(shirt, [0, 0.318, 0.004], 0.046, 0.011, [Math.PI / 2, 0, 0])          // kerah
    ];
    if (o.vest) {
        torsoParts.push(
            latheP('vest', o.vest, [0, 0, 0],
                [[0.097, 0.03], [0.1, 0.1], [0.108, 0.17], [0.115, 0.225], [0.116, 0.26], [0.109, 0.29], [0.092, 0.306]],
                [1, 1, 0.68]),
            torusP(silver, [0, 0.095, 0], 0.1015, 0.0045, [Math.PI / 2, 0, 0], [1, 0.68, 1]),
            torusP(silver, [0, 0.19, 0], 0.1115, 0.0045, [Math.PI / 2, 0, 0], [1, 0.68, 1]),
            boxP(silver, [-0.048, 0.2, -0.066], [0.022, 0.19, 0.014]),
            boxP(silver, [0.048, 0.2, -0.066], [0.022, 0.19, 0.014]),
            boxP(silver, [-0.048, 0.2, 0.066], [0.022, 0.19, 0.014]),
            boxP(silver, [0.048, 0.2, 0.066], [0.022, 0.19, 0.014])
        );
    }
    spine.add(makeMesh(torsoParts, humanMat));

    // ---------------- KEPALA (leher, tengkorak, rahang, telinga, hidung, mata, alis, bibir, rambut) ----------------
    const fz = (x, y) => -0.066 * Math.sqrt(Math.max(0.05, 1 - (x / 0.056) ** 2 - (y / 0.083) ** 2));
    const headParts = [
        cylP(sk, [0, -0.10, 0.004], 0.04, 0.046, 0.12),                              // leher
        ellP(sk, [0, 0, 0], [0.056, 0.083, 0.066]),                                  // tengkorak
        ellP(sk, [0, -0.045, -0.012], [0.045, 0.04, 0.052]),                         // rahang
        ellP(sk, [0, -0.07, -0.032], [0.024, 0.017, 0.021]),                         // dagu
        ellP(sk, [-0.055, -0.004, 0.008], [0.008, 0.022, 0.014]),                    // telinga kiri
        ellP(sk, [0.055, -0.004, 0.008], [0.008, 0.022, 0.014]),                     // telinga kanan
        ellP(sk, [0, -0.002, -0.061], [0.008, 0.02, 0.011], [0.25, 0, 0]),           // tulang hidung
        ellP(sk, [0, -0.022, -0.068], [0.012, 0.011, 0.012]),                        // ujung hidung
        ellP(sk, [-0.009, -0.025, -0.063], [0.007, 0.007, 0.008]),
        ellP(sk, [0.009, -0.025, -0.063], [0.007, 0.007, 0.008]),
        ellP(lipC, [0, -0.037, fz(0, -0.037) + 0.002], [0.018, 0.0045, 0.006]),      // bibir atas
        ellP(lipC, [0, -0.045, fz(0, -0.045) + 0.002], [0.014, 0.0045, 0.005]),      // bibir bawah
        { geo: cached('hair', () => new THREE.SphereGeometry(1, 14, 10, 0, Math.PI, 0, Math.PI * 0.64)), color: hr, pos: [0, 0.002, 0.004], scale: [0.059, 0.087, 0.07] }
    ];
    [-1, 1].forEach(s => {
        headParts.push(
            ellP(0xf4f1ea, [s * 0.021, 0.016, fz(s * 0.021, 0.016) + 0.002], [0.0105, 0.0075, 0.006]),   // putih mata
            ellP(0x2b1a10, [s * 0.021, 0.016, fz(s * 0.021, 0.016) - 0.002], [0.0052, 0.0052, 0.0035]),  // iris
            boxP(hr, [s * 0.022, 0.035, fz(s * 0.022, 0.035) + 0.001], [0.03, 0.006, 0.006], [0, 0, -s * 0.08])  // alis
        );
    });
    head.add(makeMesh(headParts, humanMat));

    // helm keselamatan (+ kacamata pelindung bila ada)
    const helmParts = [
        { geo: cached('dome', () => new THREE.SphereGeometry(1, 16, 8, 0, Math.PI * 2, 0, Math.PI * 0.5)), color: o.helmet, pos: [0, 0.046, -0.002], scale: [0.066, 0.062, 0.078] },
        cylP(o.helmet, [0, 0.045, -0.004], 1, 1, 0.008, null, [0.07, 1, 0.082]),
        boxP(o.helmet, [0, 0.043, -0.088], [0.07, 0.006, 0.03], [-0.18, 0, 0]),
        ellP(o.helmet, [0, 0.1, -0.004], [0.011, 0.01, 0.062])
    ];
    if (o.goggles) {
        helmParts.push(
            ellP(0x0f172a, [0, 0.016, -0.066], [0.054, 0.023, 0.0105]),
            ellP(0x38bdf8, [0, 0.016, -0.0685], [0.047, 0.017, 0.0105]),
            torusP(0x0f172a, [0, 0.016, 0.0], 1, 0.075, [Math.PI / 2, 0, 0], [0.057, 0.066, 0.057])
        );
    }
    head.add(makeMesh(helmParts, hardMat));

    // ---------------- KAKI ----------------
    [-1, 1].forEach(side => {
        const hipJ = new THREE.Group(); hipJ.position.set(side * DIM.hipX, 0, 0); hips.add(hipJ);
        hipJ.add(makeMesh([
            ellP(pantsC, [0, 0, 0], [0.054, 0.054, 0.058]),
            latheP('thigh', pantsC, [0, 0, 0], limbPts(DIM.thigh, [[0, 0.05], [0.12, 0.058], [0.35, 0.056], [0.7, 0.046], [1, 0.036]])),
            boxP(0x2a3850, [side * 0.056, -0.12, 0], [0.014, 0.075, 0.06])               // saku cargo
        ], humanMat));

        const kneeJ = new THREE.Group(); kneeJ.position.y = -DIM.thigh; hipJ.add(kneeJ);
        kneeJ.add(makeMesh([
            ellP(pantsC, [0, 0, 0], [0.036, 0.038, 0.038]),                              // lutut
            latheP('shin', pantsC, [0, 0, 0], limbPts(DIM.shin, [[0, 0.034], [0.15, 0.038], [0.3, 0.039], [0.55, 0.032], [0.8, 0.028], [0.9, 0.031], [1, 0.03]])),
            cylP(bootC, [0, -DIM.shin + 0.03, 0], 0.034, 0.032, 0.1)                     // betis sepatu bot
        ], humanMat));

        const ankleJ = new THREE.Group(); ankleJ.position.y = -DIM.shin; kneeJ.add(ankleJ);
        ankleJ.add(makeMesh([
            ellP(bootC, [0, -0.018, -0.04], [0.034, 0.03, 0.088]),
            ellP(bootC, [0, -0.024, -0.095], [0.03, 0.024, 0.05]),
            ellP(bootC, [0, -0.025, 0.03], [0.03, 0.025, 0.035]),
            boxP(0x0d0d0d, [0, -0.0455, -0.035], [0.068, 0.009, 0.19])                   // sol
        ], humanMat));

        rig.legs.push({ side, hip: hipJ, knee: kneeJ, ankle: ankleJ });
    });

    // ---------------- LENGAN ----------------
    [-1, 1].forEach(side => {
        const sJ = new THREE.Group(); sJ.position.set(side * DIM.shoulderX, DIM.shoulderY, 0); spine.add(sJ);
        sJ.add(makeMesh([
            ellP(shirt, [0, 0, 0], [0.043, 0.047, 0.045]),                               // otot deltoid
            latheP('uarm', sk, [0, 0, 0], limbPts(DIM.upperArm, [[0, 0.03], [0.2, 0.034], [0.45, 0.033], [0.8, 0.026], [1, 0.023]])),
            latheP('sleeve', shirt, [0, 0, 0], limbPts(0.115, [[0, 0.037], [0.3, 0.038], [1, 0.042]], false))   // lengan baju pendek
        ], humanMat));

        const eJ = new THREE.Group(); eJ.position.y = -DIM.upperArm; sJ.add(eJ);
        eJ.add(makeMesh([
            ellP(sk, [0, 0, 0], [0.025, 0.025, 0.025]),                                  // siku
            latheP('farm', sk, [0, 0, 0], limbPts(DIM.foreArm, [[0, 0.025], [0.2, 0.027], [0.5, 0.022], [1, 0.016]]))
        ], humanMat));

        const wJ = new THREE.Group(); wJ.position.y = -DIM.foreArm; eJ.add(wJ);
        wJ.add(makeMesh([
            ellP(sk, [0, -0.034, 0], [0.012, 0.034, 0.028]),                                                       // telapak
            ellP(sk, [-side * 0.01, -0.075, 0], [0.011, 0.03, 0.026], [0, 0, -side * 0.35]),                       // 4 jari menekuk
            ellP(sk, [-side * 0.014, -0.04, -0.026], [0.009, 0.026, 0.011], [0.5, 0, -side * 0.15])                // ibu jari
        ], humanMat));

        rig.arms.push({ side, shoulder: sJ, elbow: eJ, wrist: wJ, hand: wJ, base: { x: 0.04, z: side * 0.07, e: 0.14 }, swing: true });
    });

    return rig;
}

function setArm(rig, side, x, z, e, swing) {
    const a = rig.arms.find(a => a.side === side);
    a.base = { x, z: side * z, e };
    a.swing = swing;
    return a;
}

function setSeated(rig) {
    rig.seated = true;
    rig.hips.position.y = DIM.shin + DIM.ankleH;
    rig.legs.forEach(l => { l.hip.rotation.x = 1.5; l.knee.rotation.x = -1.5; l.ankle.rotation.x = 0; });
}

// Pose per-frame: berdiri diam (napas, menoleh) <-> berjalan (siklus langkah penuh)
function poseHuman(rig, t) {
    const k = rig.k, idle = 1 - k, ph = rig.phase;
    const ampS = Math.min(1, 0.45 + rig.amp);
    const breathe = Math.sin(t * 1.9 + rig.ip);

    if (rig.seated) {
        rig.spine.position.y = DIM.spineUp + breathe * 0.0015;
        rig.head.rotation.y = Math.sin(t * 0.6 + rig.ip) * 0.22;
    } else {
        let hipH = 0;
        for (const leg of rig.legs) {
            const p = ph + (leg.side > 0 ? 0 : Math.PI);          // kaki kiri berlawanan fase
            const sp = Math.sin(p), cp = Math.cos(p);
            const h = rig.amp * sp * k;                           // ayunan paha (+ = maju)
            const swingW = Math.pow(Math.max(0, Math.cos(p + 0.5)), 1.2);
            const flex = k * (0.07 + 0.95 * ampS * swingW);       // lutut menekuk saat kaki terayun
            const toeOff = k * 0.5 * Math.max(0, -sp) * Math.sqrt(Math.max(0, -cp));  // tumit terangkat saat mendorong
            const ankle = (flex - h) - 0.9 * toeOff;              // telapak tetap rata ke lantai
            leg.hip.rotation.x = h;
            leg.knee.rotation.x = -flex;
            leg.ankle.rotation.x = ankle;

            // tinggi panggul dihitung dari kaki terendah -> kaki selalu menapak, TIDAK melayang / meloncat
            const psi = -0.9 * toeOff;
            const sinp = Math.sin(psi), cosp = Math.cos(psi);
            const yToe = -0.05 * cosp + 0.135 * sinp;
            const yHeel = -0.05 * cosp - 0.05 * sinp;
            const need = DIM.thigh * Math.cos(h) + DIM.shin * Math.cos(h - flex) - Math.min(yToe, yHeel);
            if (need > hipH) hipH = need;
        }
        rig.hips.position.y = hipH;
        rig.hips.position.x = -0.012 * Math.cos(ph) * k;          // pindah bobot ke kaki tumpu
        rig.hips.rotation.y = 0.11 * ampS * Math.sin(ph) * k;     // panggul berputar
        const tw = rig.carry ? 0.3 : 1;
        rig.spine.rotation.y = -0.19 * ampS * Math.sin(ph) * k * tw;   // dada berlawanan arah panggul
        rig.spine.rotation.x = -0.05 * k + breathe * 0.008 * idle;
        rig.spine.position.y = DIM.spineUp + breathe * 0.0015;
        rig.head.rotation.y = -(rig.hips.rotation.y + rig.spine.rotation.y) * 0.85 + Math.sin(t * 0.7 + rig.ip) * 0.22 * idle;
        rig.head.rotation.x = 0.05 * k + Math.sin(t * 0.5 + rig.ip) * 0.03 * idle;
    }

    for (const arm of rig.arms) {
        let sw = 0, el = 0;
        if (arm.swing && !rig.seated) {
            const s = Math.sin(ph + (arm.side > 0 ? 0 : Math.PI));    // fase kaki sisi yang sama
            sw = -rig.amp * 0.8 * s * k;                              // lengan berayun berlawanan dgn kaki
            el = k * (0.28 + 0.3 * Math.max(0, -s));
        }
        const micro = (arm.swing && !rig.seated) ? breathe * 0.012 * idle : 0;
        arm.shoulder.rotation.set(arm.base.x + sw + micro, 0, arm.base.z);
        arm.elbow.rotation.x = arm.base.e + el;
    }
}

// =====================================================================
//  PEMBUAT UNIT
// =====================================================================
function humanStyle(team, extra) {
    const isBlue = team === 'blue';
    return Object.assign({
        skin: SKIN_TONES[Math.floor(Math.random() * SKIN_TONES.length)],
        hair: HAIR_TONES[Math.floor(Math.random() * HAIR_TONES.length)],
        shirt: isBlue ? 0x0369a1 : 0xc2410c,
        vest: isBlue ? 0x84cc16 : 0xea580c,
        helmet: isBlue ? 0x0ea5e9 : 0xf59e0b,
        goggles: false
    }, extra || {});
}

function boxMesh(w, h, d, mat, x, y, z, cast = true) {
    const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat);
    m.position.set(x, y, z); m.castShadow = cast;
    return m;
}

function createUnitMesh(type, team) {
    const root = new THREE.Group();
    const isBlue = team === 'blue';
    const teamPrimary = new THREE.MeshStandardMaterial({ color: isBlue ? 0x0369a1 : 0xc2410c, roughness: 0.4 });
    const teamAccent = new THREE.MeshStandardMaterial({ color: isBlue ? 0x0ea5e9 : 0xf59e0b, roughness: 0.35 });

    root.userData.rigs = [];
    root.userData.wheels = [];
    root.rotation.y = isBlue ? 0 : Math.PI;      // arah hadap awal (biru ke -Z, oranye ke +Z)

    const baseRing = new THREE.Mesh(new THREE.TorusGeometry(0.46, 0.016, 10, 32), teamAccent);
    baseRing.rotation.x = Math.PI / 2; baseRing.position.y = 0.015; root.add(baseRing);

    const dir = new THREE.Group();
    root.add(dir);

    const addRig = (r) => { root.userData.rigs.push(r); return r; };
    const addWheel = (g, r) => root.userData.wheels.push({ g, r });

    if (type === 'pawn') {
        // Operator picker: membawa kardus dengan kedua tangan
        const rig = addRig(buildHuman(humanStyle(team)));
        rig.canWalk = true; rig.carry = true;
        setArm(rig, -1, 0.2, 0.06, 1.6, false);
        setArm(rig, 1, 0.2, 0.06, 1.6, false);
        rig.spine.add(boxMesh(0.27, 0.2, 0.24, mats.cardboard, 0, 0.15, -0.205));
        dir.add(rig.root);

    } else if (type === 'rook') {
        [[-0.28, 0.14, -0.22, 0.14, 0.09], [0.28, 0.14, -0.22, 0.14, 0.09], [-0.25, 0.1, 0.28, 0.1, 0.08], [0.25, 0.1, 0.28, 0.1, 0.08]]
            .forEach(([x, y, z, r, w]) => { const wh = makeDetailedWheel(r, w, teamAccent); wh.position.set(x, y, z); dir.add(wh); addWheel(wh, r); });

        dir.add(boxMesh(0.48, 0.15, 0.68, mats.blackSteel, 0, 0.16, 0.04));            // sasis
        dir.add(boxMesh(0.46, 0.16, 0.14, mats.blackSteel, 0, 0.2, 0.44));             // counterweight
        dir.add(boxMesh(0.3, 0.17, 0.29, mats.leather, 0, 0.32, 0.055));               // dudukan
        dir.add(boxMesh(0.28, 0.24, 0.05, mats.leather, 0, 0.53, 0.2));                // sandaran

        const driver = addRig(buildHuman(humanStyle(team, { goggles: true })));
        setSeated(driver);
        setArm(driver, -1, 0.8, 0.03, 0.9, false);
        setArm(driver, 1, 0.8, 0.03, 0.9, false);
        driver.root.scale.setScalar(0.74);
        driver.root.position.set(0, 0.235, 0.06);
        dir.add(driver.root);

        const wheel = new THREE.Mesh(new THREE.TorusGeometry(0.1, 0.012, 8, 20), mats.blackSteel);
        wheel.position.set(0, 0.63, -0.19); wheel.rotation.x = -0.9; dir.add(wheel);
        dir.add(boxMesh(0.03, 0.3, 0.03, mats.blackSteel, 0, 0.42, -0.2));

        [[-0.22, 0.22], [0.22, 0.22], [-0.22, -0.18], [0.22, -0.18]].forEach(([px, pz]) => {
            const post = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.6, 10), mats.blackSteel);
            post.position.set(px, 0.7, pz); dir.add(post);
        });
        dir.add(boxMesh(0.48, 0.035, 0.48, mats.blackSteel, 0, 1.02, 0.02));
        [-0.13, 0.13].forEach(mx => dir.add(boxMesh(0.04, 0.9, 0.04, mats.blackSteel, mx, 0.5, -0.33)));   // tiang mast
        dir.add(boxMesh(0.4, 0.2, 0.03, mats.blackSteel, 0, 0.2, -0.36));
        [-0.14, 0.14].forEach(mx => dir.add(boxMesh(0.05, 0.025, 0.4, mats.chrome, mx, 0.1, -0.52)));     // garpu

    } else if (type === 'knight') {
        dir.add(boxMesh(0.4, 0.4, 0.26, teamPrimary, 0, 0.25, 0.08));
        [[-0.2, 0.08, -0.18, 0.08], [0.2, 0.08, -0.18, 0.08], [-0.12, 0.07, 0.2, 0.07], [0.12, 0.07, 0.2, 0.07]].forEach(([x, y, z, r]) => {
            const wh = makeDetailedWheel(r, 0.07, teamAccent); wh.position.set(x, y, z); dir.add(wh); addWheel(wh, r);
        });
        [-0.17, 0.17].forEach(mx => dir.add(boxMesh(0.03, 0.75, 0.03, mats.blackSteel, mx, 0.425, -0.03)));  // mast reach truck
        dir.add(boxMesh(0.34, 0.04, 0.3, mats.blackSteel, 0, 0.06, 0.34));                                    // pijakan operator
        dir.add(boxMesh(0.02, 0.15, 0.02, mats.blackSteel, 0, 0.525, 0.047));                                 // tiang kemudi
        dir.add(boxMesh(0.28, 0.025, 0.025, mats.blackSteel, 0, 0.6, 0.047));                                 // stang kemudi

        const rider = addRig(buildHuman(humanStyle(team)));
        setArm(rider, -1, 0.7, 0.05, 0.5, false);
        setArm(rider, 1, 0.7, 0.05, 0.5, false);
        rider.root.scale.setScalar(0.78);
        rider.root.position.set(0, 0.08, 0.3);
        dir.add(rider.root);

        const pallet = makeEuroPallet(0.44, 0.42);
        pallet.position.set(0, 0.04, -0.24); dir.add(pallet);
        dir.add(boxMesh(0.38, 0.22, 0.36, mats.cardboard, 0, 0.2, -0.24));

    } else if (type === 'bishop') {
        // QC Auditor: tangan kanan memegang laser scanner, tangan kiri berayun
        const rig = addRig(buildHuman(humanStyle(team, { helmet: 0xf1f5f9, goggles: true })));
        rig.canWalk = true;
        const hold = setArm(rig, 1, 0.55, 0.05, 1.1, false);
        setArm(rig, -1, 0.04, 0.07, 0.15, true);
        const scanner = new THREE.Group();
        scanner.add(boxMesh(0.04, 0.1, 0.05, mats.blackSteel, 0, -0.1, 0, false));
        scanner.add(boxMesh(0.028, 0.045, 0.034, mats.blackSteel, 0, -0.07, 0.04, false));
        const tip = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.012, 10),
            new THREE.MeshStandardMaterial({ color: 0xef4444, emissive: 0xef4444, emissiveIntensity: 1.2 }));
        tip.position.set(0, -0.156, 0); scanner.add(tip);
        const beam = new THREE.Mesh(new THREE.CylinderGeometry(0.0025, 0.0025, 0.35, 6),
            new THREE.MeshBasicMaterial({ color: 0xff2a2a, transparent: true, opacity: 0.55 }));
        beam.position.set(0, -0.34, 0); scanner.add(beam);
        hold.hand.add(scanner);
        dir.add(rig.root);

    } else if (type === 'queen') {
        // Ops Supervisor: jaket gelap, helm emas, memegang tablet di tangan kiri
        const rig = addRig(buildHuman(humanStyle(team, { vest: 0x0f172a, helmet: 0xf59e0b, goggles: true })));
        rig.canWalk = true;
        rig.root.scale.setScalar(1.04);
        const hold = setArm(rig, -1, 0.35, 0.02, 1.45, false);
        setArm(rig, 1, 0.04, 0.07, 0.15, true);
        hold.hand.add(boxMesh(0.012, 0.11, 0.08, mats.blackSteel, 0.028, -0.075, 0, false));
        hold.hand.add(new THREE.Mesh(new THREE.BoxGeometry(0.003, 0.095, 0.066),
            new THREE.MeshStandardMaterial({ color: 0x38bdf8, emissive: 0x0ea5e9, emissiveIntensity: 0.7 })));
        hold.hand.children[hold.hand.children.length - 1].position.set(0.035, -0.075, 0);
        dir.add(rig.root);

    } else if (type === 'king') {
        dir.add(boxMesh(0.52, 1.0, 0.5, mats.blackSteel, 0, 0.58, 0.04));
        dir.add(boxMesh(0.46, 0.93, 0.02, mats.serverGlass, 0, 0.58, -0.22, false));
        [[-0.2, -0.17], [0.2, -0.17], [-0.2, 0.25], [0.2, 0.25]].forEach(([x, z]) => {
            const wh = makeDetailedWheel(0.05, 0.04, mats.chrome); wh.position.set(x, 0.05, z); dir.add(wh); addWheel(wh, 0.05);
        });
        dir.add(boxMesh(0.5, 0.04, 0.48, mats.blackSteel, 0, 0.08, 0.04));
    }

    return root;
}


let pieces = [], selectedPiece = null, validMoves = [], currentTurn = 'blue', isAnimating = false, vsAI = true, highlights = [];

const unitSpecs = {
    pawn:   { name: 'OPERATOR PICKER', role: 'Frontline Inventory • Pion', pow: 45, rng: 40 },
    rook:   { name: 'COUNTERBALANCE FORKLIFT', role: 'Heavy Logistics Armor • Benteng', pow: 95, rng: 90 },
    knight: { name: 'ELECTRIC REACH PALLET', role: 'Tactical L-Maneuver • Kuda', pow: 75, rng: 70 },
    bishop: { name: 'QC LASER AUDITOR', role: 'Diagonal Precision • Gajah', pow: 78, rng: 85 },
    queen:  { name: 'WAREHOUSE OPS SUPERVISOR', role: 'Full-Floor Commander • Menteri', pow: 100, rng: 100 },
    king:   { name: 'MAIN WMS SERVER CORE', role: 'Central System Hub • Raja', pow: 100, rng: 35 }
};
const weights = { pawn: 10, knight: 30, bishop: 30, rook: 50, queen: 90, king: 900 };

function inspectUnitUI(type) {
    const s = unitSpecs[type];
    if (!s) return;
    document.getElementById('insp-name').innerText = s.name;
    document.getElementById('insp-role').innerText = s.role;
}

function addBattleLog(text, isCombat = false) {
    const box = document.getElementById('move-history');
    const div = document.createElement('div');
    div.className = 'log-entry' + (isCombat ? ' combat' : '');
    div.innerText = text; box.prepend(div);
}

function updateScoreUI() {
    const bCount = pieces.filter(p => p.userData.alive && p.userData.team === 'blue').length;
    const oCount = pieces.filter(p => p.userData.alive && p.userData.team === 'orange').length;
    document.getElementById('score-blue').innerText = bCount;
    document.getElementById('score-orange').innerText = oCount;
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
            new THREE.PlaneGeometry(tileSize * 0.82, tileSize * 0.82),
            new THREE.MeshBasicMaterial({ color: m.attack ? 0xef4444 : 0x22c55e, transparent: true, opacity: 0.42, side: THREE.DoubleSide })
        );
        mk.rotation.x = -Math.PI/2; mk.position.set(m.x * tileSize - offset, 0.065, m.z * tileSize - offset);
        scene.add(mk); highlights.push(mk);
    });
}

function triggerExplosion(pos) {
    for (let i = 0; i < 16; i++) {
        const p = new THREE.Mesh(new THREE.BoxGeometry(0.15, 0.13, 0.15), mats.cardboard);
        p.position.copy(pos); p.position.y += 0.4; scene.add(p);
        const vx = (Math.random()-0.5)*0.2, vz = (Math.random()-0.5)*0.25; let vy = Math.random()*0.2 + 0.05;
        const tick = () => {
            p.position.x += vx; p.position.y += vy; p.position.z += vz; vy -= 0.012;
            p.scale.multiplyScalar(0.94);
            if (p.scale.x > 0.03 && p.position.y > -0.2) requestAnimationFrame(tick); else scene.remove(p);
        };
        tick();
    }
}

// =====================================================================
//  GERAKAN: bidak BERJALAN di atas papan (tanpa meloncat)
//  - menghadap ke arah tujuan, lalu melangkah dengan siklus jalan
//  - kuda berjalan lewat garis pembatas antar petak (bentuk L), tidak melompati bidak lain
//  - kendaraan melaju dengan roda berputar
// =====================================================================
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
function angDiff(a, b) {
    let d = (b - a) % (Math.PI * 2);
    if (d > Math.PI) d -= Math.PI * 2;
    if (d < -Math.PI) d += Math.PI * 2;
    return d;
}
function approachAngle(a, b, maxStep) {
    const d = angDiff(a, b);
    return Math.abs(d) <= maxStep ? a + d : a + Math.sign(d) * maxStep;
}

function buildPath(piece, mv) {
    const sx = piece.position.x, sz = piece.position.z;
    const ex = mv.x * tileSize - offset, ez = mv.z * tileSize - offset;
    const pts = [[sx, sz]];
    if (piece.userData.type === 'knight') {
        const dx = mv.x - piece.userData.gridX, dz = mv.z - piece.userData.gridZ;
        const half = tileSize / 2;
        if (Math.abs(dx) === 2) {
            const zb = sz + Math.sign(dz) * half;
            pts.push([sx, zb], [ex, zb]);
        } else {
            const xb = sx + Math.sign(dx) * half;
            pts.push([xb, sz], [xb, ez]);
        }
    }
    pts.push([ex, ez]);
    return pts;
}

function executeMove(piece, moveData) {
    isAnimating = true; clearHighlights();
    const pts = buildPath(piece, moveData);
    const segs = [];
    let total = 0;
    for (let i = 0; i < pts.length - 1; i++) {
        const dx = pts[i + 1][0] - pts[i][0], dz = pts[i + 1][1] - pts[i][1], len = Math.hypot(dx, dz);
        if (len < 1e-6) continue;
        segs.push({ x0: pts[i][0], z0: pts[i][1], dx: dx / len, dz: dz / len, len, start: total, heading: Math.atan2(-dx, -dz) });
        total += len;
    }
    const walker = HUMAN_WALKERS.includes(piece.userData.type);
    let vmax, amp = 0.6, stepLen = 0.5;
    if (walker) {
        vmax = clamp(total / 4.2, 1.55, 2.2);
        amp = clamp(0.40 + 0.14 * vmax, 0.5, 0.72);
        stepLen = 0.95 * Math.sin(amp);
    } else {
        vmax = clamp(total / 2.4, 1.8, 3.4);
    }
    activeMove = {
        piece, mv: moveData, segs, total, s: 0, vmax, amp, stepLen, walker, captured: false,
        ex: moveData.x * tileSize - offset, ez: moveData.z * tileSize - offset
    };
}

function captureVictim(m) {
    if (m.captured || !m.mv.attack || !m.mv.target) return;
    m.captured = true;
    const v = m.mv.target;
    v.userData.alive = false; scene.remove(v);
    triggerExplosion(v.position);
    const uName = unitSpecs[m.piece.userData.type].name;
    const vName = unitSpecs[v.userData.type].name;
    const coord = `${cols[m.mv.x]}${8 - m.mv.z}`;
    addBattleLog(`${uName} ⚔️ ${vName} (${coord})`, true);
    updateScoreUI();
}

function finishMove(m) {
    const piece = m.piece, moveData = m.mv;
    piece.position.set(m.ex, 0.05, m.ez);
    piece.userData.gridX = moveData.x; piece.userData.gridZ = moveData.z; piece.userData.hasMoved = true;
    activeMove = null;

    const uName = unitSpecs[piece.userData.type].name;
    const coord = `${cols[moveData.x]}${8 - moveData.z}`;
    let msg = `${uName} berjalan ke zona ${coord}.`;

    if (moveData.attack && moveData.target) {
        captureVictim(m);
        const vName = unitSpecs[moveData.target.userData.type].name;
        msg = `💥 ELIMINASI! ${uName} menyingkirkan ${vName} di ${coord}!`;
        if (moveData.target.userData.type === 'king') {
            updateHUD(`🏆 OVERRIDE SELESAI! Tim ${currentTurn.toUpperCase()} menguasai WMS Server!`);
            isAnimating = false; return;
        }
    } else {
        addBattleLog(`${uName} ➔ ${coord}`, false);
    }

    currentTurn = currentTurn === 'blue' ? 'orange' : 'blue';
    selectedPiece = null; validMoves = []; isAnimating = false;
    updateHUD(msg);
    if (vsAI && currentTurn === 'orange') setTimeout(runAIBot, 450);
}

function updateMove(dt) {
    const m = activeMove;
    if (!m) return;
    const p = m.piece;
    const findSeg = () => { for (const sg of m.segs) if (m.s < sg.start + sg.len) return sg; return m.segs[m.segs.length - 1]; };

    // 1. badan berputar menghadap arah jalan (tidak menyamping / mundur)
    let seg = findSeg();
    const before = p.rotation.y;
    p.rotation.y = approachAngle(p.rotation.y, seg.heading, 10 * dt);
    const dTheta = p.rotation.y - before;
    const align = Math.max(0, Math.cos(angDiff(p.rotation.y, seg.heading)));

    // 2. kecepatan: mulai pelan, melaju, melambat saat tiba; berhenti sebentar di tikungan sampai badan lurus
    const remaining = m.total - m.s;
    const ease = Math.min(1, 0.22 + m.s / 0.7, 0.22 + remaining / 0.8);
    const v = m.vmax * ease * align;
    const ds = v * dt;
    m.s = Math.min(m.total, m.s + ds);

    // 3. posisi di sepanjang jalur (tinggi Y tetap -> tidak ada lompatan)
    seg = findSeg();
    const d = Math.min(seg.len, m.s - seg.start);
    p.position.x = seg.x0 + seg.dx * d;
    p.position.z = seg.z0 + seg.dz * d;
    p.position.y = 0.05;

    // 4. animasi lokomosi
    if (m.walker) {
        const vr = v / m.vmax;
        p.userData.rigs.forEach(r => {
            r.amp = m.amp * (0.35 + 0.65 * vr);
            r.phase += (Math.PI * v / m.stepLen) * dt + Math.abs(dTheta) * 0.6;
        });
    } else {
        p.userData.wheels.forEach(w => { w.g.rotation.x -= ds / w.r; });
    }

    // 5. lawan tersingkir saat penyerang sudah dekat
    if (m.mv.attack && m.mv.target && !m.captured && (m.total - m.s) < tileSize * 0.55) captureVictim(m);

    if (m.s >= m.total - 1e-4) finishMove(m);
}

// Pose semua unit: gait untuk mover, menghadap kembali ke posisi awal untuk yang lain
function updatePieces(dt, t) {
    for (const p of pieces) {
        if (!p.userData.alive) continue;
        const mover = activeMove && activeMove.piece === p;
        let turning = false;
        if (!mover) {
            const d = angDiff(p.rotation.y, p.userData.restYaw);
            if (Math.abs(d) > 0.002) {
                p.rotation.y = approachAngle(p.rotation.y, p.userData.restYaw, 6 * dt);
                turning = Math.abs(d) > 0.1;
            }
        }
        for (const r of p.userData.rigs) {
            if (r.canWalk) {
                const tk = mover ? 1 : (turning ? 0.9 : 0);
                if (turning) { r.amp = 0.34; r.phase += dt * 8; }
                r.k += (tk - r.k) * Math.min(1, dt * 10);
            }
            poseHuman(r, t);
        }
    }
}


function runAIBot() {
    const aiPieces = pieces.filter(p => p.userData.alive && p.userData.team === 'orange');
    let allMoves = [];
    aiPieces.forEach(p => {
        getValidMoves(p).forEach(m => {
            let score = m.attack && m.target ? weights[m.target.userData.type] : (m.z * 0.5 + Math.random() * 2);
            allMoves.push({ piece: p, move: m, score });
        });
    });
    if (allMoves.length === 0) return;
    allMoves.sort((a, b) => b.score - a.score);
    executeMove(allMoves[0].piece, allMoves[0].move);
}

function spawnUnit(type, team, gx, gz) {
    const m = createUnitMesh(type, team);
    m.position.set(gx * tileSize - offset, 0.05, gz * tileSize - offset);
    Object.assign(m.userData, { type, team, gridX: gx, gridZ: gz, alive: true, hasMoved: false, restYaw: team === 'blue' ? 0 : Math.PI });
    scene.add(m); pieces.push(m);
}

function resetGame() {
    clearHighlights(); pieces.forEach(p => scene.remove(p)); pieces = [];
    activeMove = null;
    document.getElementById('move-history').innerHTML = '';
    selectedPiece = null; validMoves = []; currentTurn = 'blue'; isAnimating = false;
    const row = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook'];
    for (let i = 0; i < 8; i++) {
        spawnUnit(row[i], 'orange', i, 0); spawnUnit('pawn', 'orange', i, 1);
        spawnUnit('pawn', 'blue', i, 6); spawnUnit(row[i], 'blue', i, 7);
    }
    updateScoreUI();
    addBattleLog("Shift Operasional Dimulai. Anatomi manusia aktif.");
    updateHUD("Shift Baru Dimulai! Karakter kini berwujud manusia asli.");
}

function updateHUD(msg) {
    const b = document.getElementById('turn-banner');
    b.className = currentTurn === 'blue' ? 'turn-blue' : 'turn-orange';
    b.innerText = currentTurn === 'blue' ? 'SHIFT BIRU AKTIF' : 'SHIFT ORANYE AKTIF';
    if (msg) document.getElementById('action-log').innerText = msg;
}

function toggleAI() {
    vsAI = !vsAI;
    const btn = document.getElementById('btn-ai');
    btn.innerText = vsAI ? '🤖 vs AI Bot' : '👥 2 Player';
    btn.classList.toggle('active', vsAI);
}

function setCameraView(mode) {
    if (mode === 'top') {
        camera.position.set(0, 18.5, 0.01); controls.target.set(0, 0, 0);
    } else if (mode === 'closeup') {
        camera.position.set(-2.2, 3.2, 6.8); controls.target.set(-1.0, 0.7, 3.2);
    } else {
        camera.position.set(0, 11.2, 14.2); controls.target.set(0, 0.5, 0);
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
    if (unit) inspectUnitUI(unit.userData.type);

    if (unit && unit.userData.team === currentTurn) {
        selectedPiece = unit; validMoves = getValidMoves(unit); showHighlights(validMoves);
        updateHUD(`Unit Siap: ${unitSpecs[unit.userData.type].name} di zona ${cols[coords.x]}${8 - coords.z}`);
    } else {
        selectedPiece = null; validMoves = []; clearHighlights();
    }
});

let lastT = performance.now() / 1000;
resetGame();

function animate() {
    requestAnimationFrame(animate);
    const now = performance.now() / 1000;
    const dt = Math.min(0.05, Math.max(0.0001, now - lastT));
    lastT = now;
    updateMove(dt);
    updatePieces(dt, now);
    controls.update();
    renderer.render(scene, camera);
}
animate();

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});
</script>
</body>
</html>'''

components.html(HTML_CODE, height=900, scrolling=False)
