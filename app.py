import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="WAREHOUSE COMMAND: EPIC TACTICAL 3D",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding: 0 !important; margin: 0 !important; max-width: 100% !important;}
    .stApp {background-color: #030508; overflow: hidden;}
    iframe {display: block; border: none; width: 100vw !important; height: 100vh !important;}
</style>
""", unsafe_allow_html=True)

HTML_CODE = r'''<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Warehouse Command: Epic Combat Edition</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=Rajdhani:wght@500;600;700&display=swap" rel="stylesheet">
<style>
    * { box-sizing: border-box; user-select: none; }
    body { margin: 0; padding: 0; overflow: hidden; background: #030508; font-family: 'Rajdhani', sans-serif; color: #e2e8f0; }
    #canvas-container { width: 100vw; height: 100vh; display: block; }
    #vignette { position: fixed; inset: 0; pointer-events: none; z-index: 2; background: radial-gradient(circle at center, transparent 50%, rgba(2, 4, 8, 0.85) 100%); }
    
    #top-bar {
        position: absolute; top: 0; left: 0; right: 0; height: 68px;
        background: linear-gradient(180deg, rgba(7, 11, 18, 0.98) 0%, rgba(7, 11, 18, 0.8) 100%);
        border-bottom: 1px solid rgba(56, 189, 248, 0.25);
        display: flex; justify-content: space-between; align-items: center;
        padding: 0 24px; z-index: 10; backdrop-filter: blur(12px);
    }
    .brand-cluster { display: flex; align-items: center; gap: 14px; }
    .brand-emblem {
        width: 42px; height: 42px; border-radius: 8px;
        background: linear-gradient(135deg, #f59e0b 0%, #b45309 100%);
        display: flex; align-items: center; justify-content: center;
        font-family: 'Orbitron', sans-serif; font-weight: 900; font-size: 20px; color: #030508;
        box-shadow: 0 0 18px rgba(245, 158, 11, 0.5);
    }
    .brand-title h1 { margin: 0; font-family: 'Orbitron', sans-serif; font-size: 16px; font-weight: 800; letter-spacing: 2px; color: #f8fafc; }
    .brand-title span { font-size: 11px; color: #f59e0b; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700; display: block; }

    .versus-hud {
        display: flex; align-items: center; gap: 18px;
        background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(148, 163, 184, 0.25);
        padding: 6px 22px; border-radius: 40px;
    }
    .team-score { display: flex; align-items: center; gap: 10px; font-weight: 700; font-size: 14px; letter-spacing: 1px; }
    .team-score.blue { color: #38bdf8; }
    .team-score.orange { color: #fbbf24; }
    .score-pill { background: rgba(2, 6, 23, 0.85); padding: 2px 10px; border-radius: 12px; font-family: 'Orbitron', sans-serif; font-size: 14px; border: 1px solid currentColor; }
    #turn-banner {
        padding: 5px 16px; border-radius: 20px; font-family: 'Orbitron', sans-serif; font-size: 11px; font-weight: 800;
        letter-spacing: 1.5px; text-transform: uppercase;
    }
    .turn-blue { background: rgba(2, 132, 199, 0.35); color: #38bdf8; border: 1px solid #38bdf8; }
    .turn-orange { background: rgba(217, 119, 6, 0.35); color: #fbbf24; border: 1px solid #fbbf24; }

    .toolbar { display: flex; gap: 8px; }
    .t-btn {
        background: rgba(15, 23, 42, 0.92); border: 1px solid rgba(148, 163, 184, 0.3);
        color: #cbd5e1; padding: 8px 13px; border-radius: 6px; font-family: 'Rajdhani', sans-serif;
        font-weight: 700; font-size: 13px; letter-spacing: 0.8px; text-transform: uppercase; cursor: pointer; transition: 0.2s;
    }
    .t-btn:hover { background: rgba(56, 189, 248, 0.15); border-color: #38bdf8; color: #fff; }
    .t-btn.active { background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%); border-color: #38bdf8; color: #fff; }

    #unit-inspector {
        position: absolute; top: 86px; left: 20px; width: 275px;
        background: linear-gradient(160deg, rgba(11, 17, 30, 0.95) 0%, rgba(7, 11, 20, 0.98) 100%);
        border: 1px solid rgba(56, 189, 248, 0.3); border-left: 4px solid #38bdf8;
        border-radius: 8px; padding: 14px 16px; z-index: 10; backdrop-filter: blur(10px);
    }
    .panel-tag { font-family: 'Orbitron', sans-serif; font-size: 10px; color: #64748b; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 4px; }
    #insp-name { font-family: 'Orbitron', sans-serif; font-size: 15px; font-weight: 800; color: #f8fafc; margin: 0 0 2px 0; }
    #insp-role { font-size: 12px; color: #f59e0b; font-weight: 700; margin-bottom: 10px; }
    .stat-row { margin: 6px 0; }
    .stat-label { display: flex; justify-content: space-between; font-size: 11px; color: #94a3b8; font-weight: 600; margin-bottom: 3px; }
    .stat-bar { height: 5px; background: rgba(30, 41, 59, 0.9); border-radius: 3px; overflow: hidden; }
    .stat-fill { height: 100%; background: linear-gradient(90deg, #0284c7, #38bdf8); }
    .roster-mini { margin-top: 12px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.08); font-size: 11px; color: #94a3b8; line-height: 1.5; }
    .roster-mini b { color: #e2e8f0; }

    #ops-panel {
        position: absolute; top: 86px; right: 20px; width: 265px;
        background: linear-gradient(160deg, rgba(11, 17, 30, 0.92) 0%, rgba(7, 11, 20, 0.96) 100%);
        border: 1px solid rgba(245, 158, 11, 0.3); border-right: 4px solid #f59e0b;
        border-radius: 8px; padding: 14px 16px; z-index: 10; backdrop-filter: blur(10px);
    }
    #move-history { max-height: 150px; overflow-y: auto; font-size: 12px; display: flex; flex-direction: column; gap: 5px; margin-top: 8px; padding-right: 4px; }
    .log-entry { background: rgba(15, 23, 42, 0.8); padding: 5px 8px; border-radius: 4px; border-left: 2px solid #475569; color: #cbd5e1; font-size: 11.5px; }
    .log-entry.combat { border-left-color: #ef4444; background: rgba(127, 29, 29, 0.3); color: #fca5a5; font-weight: 700; }

    #bottom-ticker {
        position: absolute; bottom: 18px; left: 50%; transform: translateX(-50%);
        background: rgba(7, 11, 18, 0.94); border: 1px solid rgba(56, 189, 248, 0.35);
        padding: 10px 28px; border-radius: 30px; display: flex; align-items: center; gap: 12px; z-index: 10; font-size: 14px; font-weight: 600;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
    }
    .pulse-dot { width: 9px; height: 9px; border-radius: 50%; background: #22c55e; box-shadow: 0 0 12px #22c55e; }
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
                <span>Epic Combat & Distinct Classes • AAA 3D Simulator</span>
            </div>
        </div>

        <div class="versus-hud">
            <div class="team-score blue"><span>INBOUND</span><span id="score-blue" class="score-pill">16</span></div>
            <div id="turn-banner" class="turn-blue">SHIFT BIRU AKTIF</div>
            <div class="team-score orange"><span id="score-orange" class="score-pill">16</span><span>OUTBOUND</span></div>
        </div>

        <div class="toolbar">
            <button id="btn-ai" class="t-btn active" onclick="toggleAI()">🤖 vs AI Bot</button>
            <button class="t-btn" onclick="setCameraView('closeup')">🔍 Close-Up Aksi</button>
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
            <div class="stat-label"><span>COMBAT POWER</span><span id="st-pow-val">50%</span></div>
            <div class="stat-bar"><div id="st-pow" class="stat-fill" style="width:50%"></div></div>
        </div>
        <div class="stat-row">
            <div class="stat-label"><span>TACTICAL SPEED</span><span id="st-rng-val">70%</span></div>
            <div class="stat-bar"><div id="st-rng" class="stat-fill" style="width:70%"></div></div>
        </div>
        <div class="roster-mini">
            <div><b>Pion:</b> Operator Picker (Kardus)</div>
            <div><b>Benteng:</b> Heavy Forklift (Mesin Berat)</div>
            <div><b>Kuda:</b> Reach Truck (Palet Elektrik)</div>
            <div><b>Gajah:</b> QC Auditor (Laser Scanner)</div>
            <div><b>Menteri:</b> Ops Supervisor (Komandan)</div>
            <div><b>Raja:</b> Main WMS Server Hub</div>
        </div>
    </div>

    <div id="ops-panel">
        <div class="panel-tag">WMS COMBAT LOG</div>
        <div style="font-size:12px; color:#f59e0b; font-weight:700;">AKSI EPIC & ELIMINASI</div>
        <div id="move-history"></div>
    </div>

    <div id="bottom-ticker">
        <div class="pulse-dot"></div>
        <div id="action-log">Sistem WMS Online. Setiap peran unit kini memiliki ciri khas & animasi tempur epic!</div>
    </div>

    <div id="canvas-container"></div>

<script>
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x030508);
scene.fog = new THREE.FogExp2(0x030508, 0.013);

const camera = new THREE.PerspectiveCamera(38, window.innerWidth / window.innerHeight, 0.1, 220);
camera.position.set(0, 11.2, 14.2);

const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 0.75;
renderer.outputEncoding = THREE.sRGBEncoding;
container.appendChild(renderer.domElement);

const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.maxPolarAngle = Math.PI / 2 - 0.03;
controls.minDistance = 3.5;
controls.maxDistance = 26;
controls.target.set(0, 0.5, 0);

const ambient = new THREE.HemisphereLight(0x93c5fd, 0x070b12, 0.5);
scene.add(ambient);
const sunLight = new THREE.DirectionalLight(0xfff1e0, 1.2);
sunLight.position.set(9, 19, 11);
sunLight.castShadow = true;
sunLight.shadow.mapSize.set(2048, 2048);
const d = 8.2;
Object.assign(sunLight.shadow.camera, { left: -d, right: d, top: d, bottom: -d, near: 2, far: 42 });
sunLight.shadow.bias = -0.0004;
scene.add(sunLight);

const rimBlue = new THREE.PointLight(0x0284c7, 0.9, 26); rimBlue.position.set(-10, 6, 9); scene.add(rimBlue);
const rimAmber = new THREE.PointLight(0xd97706, 0.9, 26); rimAmber.position.set(10, 6, -9); scene.add(rimAmber);

function makeHazardTex() {
    const c = document.createElement('canvas'); c.width = 256; c.height = 256;
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#ca8a04'; ctx.fillRect(0,0,256,256);
    ctx.fillStyle = '#030508';
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
    ctx.fillStyle = isDark ? '#0b111e' : '#172033'; ctx.fillRect(0,0,256,256);
    ctx.strokeStyle = isDark ? '#172033' : '#283548'; ctx.lineWidth = 8; ctx.strokeRect(4,4,248,248);
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
    ctx.fillStyle = '#030508';
    for(let b=32; b<108; b+=6) ctx.fillRect(b, 36, (b%12===0)?4:2, 32);
    return new THREE.CanvasTexture(c);
}

const boardGroup = new THREE.Group(); scene.add(boardGroup);
const warehouseFloor = new THREE.Mesh(new THREE.PlaneGeometry(80, 80), new THREE.MeshStandardMaterial({ color: 0x05080e, roughness: 0.75 }));
warehouseFloor.rotation.x = -Math.PI/2; warehouseFloor.position.y = -0.36; warehouseFloor.receiveShadow = true; scene.add(warehouseFloor);

const base = new THREE.Mesh(new THREE.BoxGeometry(10.6, 0.36, 10.6), new THREE.MeshStandardMaterial({ color: 0x070b16, roughness: 0.4 }));
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

const animatedParts = [];
const humanIdles = [];

const mats = {
    skin: new THREE.MeshStandardMaterial({ color: 0xd99b72, roughness: 0.55 }),
    hair: new THREE.MeshStandardMaterial({ color: 0x18130f, roughness: 0.8 }),
    cargoPants: new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.85 }),
    blackSteel: new THREE.MeshStandardMaterial({ color: 0x0f172a, metalness: 0.65, roughness: 0.4 }),
    chrome: new THREE.MeshStandardMaterial({ color: 0xe2e8f0, metalness: 0.9, roughness: 0.15 }),
    rubberTire: new THREE.MeshStandardMaterial({ color: 0x030508, roughness: 0.92 }),
    leather: new THREE.MeshStandardMaterial({ color: 0x1c1917, roughness: 0.5 }),
    cardboard: new THREE.MeshStandardMaterial({ map: boxTex, roughness: 0.78 }),
    woodPallet: new THREE.MeshStandardMaterial({ color: 0x855832, roughness: 0.88 }),
    hiVisLime: new THREE.MeshStandardMaterial({ color: 0x84cc16, roughness: 0.45 }),
    hiVisOrange: new THREE.MeshStandardMaterial({ color: 0xea580c, roughness: 0.45 }),
    silverReflective: new THREE.MeshStandardMaterial({ color: 0xcbd5e1, metalness: 0.6, roughness: 0.3 }),
    whiteHelmet: new THREE.MeshStandardMaterial({ color: 0xf1f5f9, roughness: 0.3 }),
    goldHelmet: new THREE.MeshStandardMaterial({ color: 0xf59e0b, roughness: 0.25, metalness: 0.45 }),
    visorGlass: new THREE.MeshStandardMaterial({ color: 0x0284c7, roughness: 0.15, metalness: 0.8 }),
    serverGlass: new THREE.MeshStandardMaterial({ color: 0x030508, roughness: 0.15, transparent: true, opacity: 0.7 }),
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

function buildOrganicHuman(teamMat, vestMat, helmetMat, hasGoggles, isSeated = false) {
    const human = new THREE.Group();
    if (!isSeated) {
        [-0.09, 0.09].forEach(lx => {
            const boot = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.08, 0.16), mats.leather);
            boot.position.set(lx, 0.04, -0.01); boot.castShadow = true; human.add(boot);
            const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.032, 0.44, 16), mats.cargoPants);
            leg.position.set(lx, 0.28, 0); leg.castShadow = true; human.add(leg);
        });
    } else {
        [-0.085, 0.085].forEach(lx => {
            const thigh = new THREE.Mesh(new THREE.CylinderGeometry(0.048, 0.04, 0.22, 12), mats.cargoPants);
            thigh.rotation.x = Math.PI / 2.2; thigh.position.set(lx, 0.52, -0.08); human.add(thigh);
            const boot = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.06, 0.14), mats.leather);
            boot.position.set(lx, 0.3, -0.2); human.add(boot);
        });
    }

    const baseY = 0.52;
    const pelvis = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.1, 0.12, 16), mats.cargoPants);
    pelvis.position.set(0, baseY, 0); human.add(pelvis);

    const upperBody = new THREE.Group();
    upperBody.position.set(0, baseY + 0.08, 0);
    human.add(upperBody);

    const torso = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.11, 0.35, 16), teamMat);
    torso.position.set(0, 0.17, 0); torso.castShadow = true; upperBody.add(torso);

    const vest = new THREE.Mesh(new THREE.CylinderGeometry(0.146, 0.116, 0.32, 16), vestMat);
    vest.position.set(0, 0.17, 0); vest.castShadow = true; upperBody.add(vest);

    [0.08, 0.19].forEach(sy => {
        const hStrip = new THREE.Mesh(new THREE.CylinderGeometry(0.148, 0.12, 0.024, 16), mats.silverReflective);
        hStrip.position.set(0, sy, 0); upperBody.add(hStrip);
    });

    const neck = new THREE.Mesh(new THREE.CylinderGeometry(0.042, 0.05, 0.08, 14), mats.skin);
    neck.position.set(0, 0.37, 0); upperBody.add(neck);

    const headGroup = new THREE.Group();
    headGroup.position.set(0, 0.46, 0);
    upperBody.add(headGroup);

    const skull = new THREE.Mesh(new THREE.SphereGeometry(0.1, 20, 20), mats.skin);
    skull.scale.set(0.9, 1.15, 1.0); skull.castShadow = true; headGroup.add(skull);

    const hair = new THREE.Mesh(new THREE.SphereGeometry(0.102, 16, 12, 0, Math.PI*2, 0, Math.PI*0.5), mats.hair);
    hair.position.set(0, 0.03, -0.01); headGroup.add(hair);

    const nose = new THREE.Mesh(new THREE.ConeGeometry(0.015, 0.035, 8), mats.skin);
    nose.rotation.x = -Math.PI / 2; nose.position.set(0, -0.01, -0.1); headGroup.add(nose);

    if (hasGoggles) {
        const goggles = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.04, 0.06), mats.visorGlass);
        goggles.position.set(0, 0.01, -0.08); headGroup.add(goggles);
    }

    const helmet = new THREE.Mesh(new THREE.SphereGeometry(0.118, 18, 14, 0, Math.PI*2, 0, Math.PI*0.55), helmetMat);
    helmet.position.set(0, 0.03, 0); helmet.castShadow = true; headGroup.add(helmet);
    const brim = new THREE.Mesh(new THREE.CylinderGeometry(0.125, 0.13, 0.015, 18), helmetMat);
    brim.position.set(0, 0.03, -0.02); headGroup.add(brim);

    humanIdles.push({ upperBody, headGroup, baseY: baseY + 0.08, phase: Math.random() * Math.PI * 2 });
    return { root: human, upperBody, headGroup };
}

function attachOrganicArm(upperBody, side, sRotX, sRotZ, eRotX, teamMat) {
    const sGroup = new THREE.Group();
    sGroup.position.set(side * 0.16, 0.28, 0);
    sGroup.rotation.set(sRotX, 0, sRotZ);
    upperBody.add(sGroup);

    const shoulder = new THREE.Mesh(new THREE.SphereGeometry(0.042, 12, 12), teamMat);
    sGroup.add(shoulder);

    const upperArm = new THREE.Mesh(new THREE.CylinderGeometry(0.036, 0.03, 0.18, 12), teamMat);
    upperArm.position.set(0, -0.09, 0); upperArm.castShadow = true; sGroup.add(upperArm);

    const eGroup = new THREE.Group();
    eGroup.position.set(0, -0.18, 0); eGroup.rotation.x = eRotX;
    sGroup.add(eGroup);

    const forearm = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.025, 0.17, 12), mats.skin);
    forearm.position.set(0, -0.085, 0); forearm.castShadow = true; eGroup.add(forearm);

    const hand = new THREE.Mesh(new THREE.SphereGeometry(0.032, 10, 10), mats.leather);
    hand.scale.set(0.8, 1.1, 1.2); hand.position.set(0, -0.18, 0); eGroup.add(hand);

    return { sGroup, eGroup };
}

// PEMBUATAN UNIT DENGAN PEMBEDA PERAN SANGAT JELAS
function createUnitMesh(type, team) {
    const root = new THREE.Group();
    const isBlue = team === 'blue';
    const teamPrimary = new THREE.MeshStandardMaterial({ color: isBlue ? 0x0369a1 : 0xc2410c, roughness: 0.4 });
    const teamAccent = new THREE.MeshStandardMaterial({ color: isBlue ? 0x0ea5e9 : 0xf59e0b, roughness: 0.35 });
    const vestMat = isBlue ? mats.hiVisLime : mats.hiVisOrange;

    const baseRing = new THREE.Mesh(new THREE.TorusGeometry(0.46, 0.016, 10, 32), teamAccent);
    baseRing.rotation.x = Math.PI / 2; baseRing.position.y = 0.015; root.add(baseRing);

    const dir = new THREE.Group();
    dir.rotation.y = isBlue ? 0 : Math.PI;
    root.add(dir);

    // 1. PION: OPERATOR PICKER (Membawa Kardus Logistik)
    if (type === 'pawn') {
        const { root: fig, upperBody } = buildOrganicHuman(teamPrimary, vestMat, teamAccent, false, false);
        dir.add(fig);
        attachOrganicArm(upperBody, -1, 0.65, -0.15, 1.05, teamPrimary);
        attachOrganicArm(upperBody, 1, 0.65, 0.15, 1.05, teamPrimary);

        const box = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.22, 0.26), mats.cardboard);
        box.position.set(0, 0.13, -0.24); box.castShadow = true; upperBody.add(box);
    } 
    // 2. BENTENG: HEAVY FORKLIFT + DRIVER MANUSIA DI DALAM KABIN
    else if (type === 'rook') {
        const wFL = makeDetailedWheel(0.14, 0.09, teamAccent); wFL.position.set(-0.28, 0.14, -0.22); dir.add(wFL);
        const wFR = makeDetailedWheel(0.14, 0.09, teamAccent); wFR.position.set(0.28, 0.14, -0.22); dir.add(wFR);
        const wBL = makeDetailedWheel(0.1, 0.08, teamAccent); wBL.position.set(-0.25, 0.1, 0.28); dir.add(wBL);
        const wBR = makeDetailedWheel(0.1, 0.08, teamAccent); wBR.position.set(0.25, 0.1, 0.28); dir.add(wBR);

        const chassis = new THREE.Mesh(new THREE.BoxGeometry(0.48, 0.15, 0.68), mats.blackSteel);
        chassis.position.set(0, 0.16, 0.04); chassis.castShadow = true; dir.add(chassis);

        const driver = buildOrganicHuman(teamPrimary, vestMat, teamAccent, true, true);
        driver.root.scale.set(0.74, 0.74, 0.74); driver.root.position.set(0, 0.06, 0.06);
        attachOrganicArm(driver.upperBody, -1, 0.85, -0.1, 0.65, teamPrimary);
        attachOrganicArm(driver.upperBody, 1, 0.85, 0.1, 0.65, teamPrimary);
        dir.add(driver.root);

        [-0.22, 0.22].forEach(px => {
            const post = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.6, 10), mats.blackSteel);
            post.position.set(px, 0.7, 0.22); dir.add(post);
        });
        const roof = new THREE.Mesh(new THREE.BoxGeometry(0.48, 0.035, 0.48), mats.blackSteel);
        roof.position.set(0, 1.02, 0.02); dir.add(roof);

        [-0.14, 0.14].forEach(mx => {
            const fork = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.025, 0.4), mats.chrome);
            fork.position.set(mx, 0.1, -0.52); dir.add(fork);
        });
    } 
    // 3. KUDA: ELECTRIC REACH TRUCK + PALET ELEKTRIK
    else if (type === 'knight') {
        const body = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.4, 0.26), teamPrimary);
        body.position.set(0, 0.25, 0.08); dir.add(body);

        const rider = buildOrganicHuman(teamPrimary, vestMat, teamAccent, false, false);
        rider.root.scale.set(0.75, 0.75, 0.75); rider.root.position.set(0, 0.08, 0.3);
        attachOrganicArm(rider.upperBody, -1, 0.7, -0.1, 0.5, teamPrimary);
        attachOrganicArm(rider.upperBody, 1, 0.7, 0.1, 0.5, teamPrimary);
        dir.add(rider.root);

        const pallet = makeEuroPallet(0.44, 0.42);
        pallet.position.set(0, 0.04, -0.24); dir.add(pallet);
        const b1 = new THREE.Mesh(new THREE.BoxGeometry(0.38, 0.22, 0.36), mats.cardboard);
        b1.position.set(0, 0.2, -0.24); b1.castShadow = true; dir.add(b1);
    } 
    // 4. GAJAH: QC INSPECTOR (Membawa Clipboard & Laser Barcode Scanner)
    else if (type === 'bishop') {
        const { root: fig, upperBody } = buildOrganicHuman(teamPrimary, vestMat, mats.whiteHelmet, true, false);
        dir.add(fig);
        attachOrganicArm(upperBody, -1, 0.45, 0.1, 0.95, teamPrimary);
        attachOrganicArm(upperBody, 1, 0.85, -0.05, 0.65, teamPrimary);

        const clipboard = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.18, 0.015), mats.woodPallet);
        clipboard.position.set(-0.12, 0.18, -0.15); clipboard.rotation.x = 0.3; upperBody.add(clipboard);
    } 
    // 5. MENTERI: WAREHOUSE SUPERVISOR (Helm Emas & Tablet WMS)
    else if (type === 'queen') {
        const { root: fig, upperBody } = buildOrganicHuman(teamPrimary, mats.blackSteel, mats.goldHelmet, true, false);
        fig.scale.set(1.04, 1.04, 1.04); dir.add(fig);
        attachOrganicArm(upperBody, -1, 0.55, -0.1, 1.1, teamPrimary);
        attachOrganicArm(upperBody, 1, 0.4, 0.15, 0.9, teamPrimary);

        const tablet = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.15, 0.02), mats.blackSteel);
        tablet.position.set(0, 0.18, -0.25); tablet.rotation.x = -0.55; upperBody.add(tablet);
    } 
    // 6. RAJA: MAIN WMS SERVER RACK (Pintu Kaca & Hologram Core)
    else if (type === 'king') {
        const cab = new THREE.Mesh(new THREE.BoxGeometry(0.52, 1.05, 0.5), mats.blackSteel);
        cab.position.set(0, 0.53, 0.04); cab.castShadow = true; dir.add(cab);
        const door = new THREE.Mesh(new THREE.BoxGeometry(0.46, 0.98, 0.02), mats.serverGlass);
        door.position.set(0, 0.53, -0.22); dir.add(door);

        const core = new THREE.Mesh(new THREE.OctahedronGeometry(0.15, 1), new THREE.MeshStandardMaterial({
            color: isBlue ? 0x38bdf8 : 0xfbbf24, emissive: isBlue ? 0x0284c7 : 0xd97706, emissiveIntensity: 0.9, wireframe: true
        }));
        core.position.set(0, 1.25, 0.04); dir.add(core);
        animatedParts.push({ mesh: core, type: 'spin' });
    }

    return root;
}

let pieces = [], selectedPiece = null, validMoves = [], currentTurn = 'blue', isAnimating = false, vsAI = true, highlights = [];

const unitSpecs = {
    pawn:   { name: 'OPERATOR PICKER', role: 'Frontline Inventory • Pion', pow: 50, rng: 70 },
    rook:   { name: 'COUNTERBALANCE FORKLIFT', role: 'Heavy Logistics Armor • Benteng', pow: 95, rng: 90 },
    knight: { name: 'ELECTRIC REACH PALLET', role: 'Tactical L-Maneuver • Kuda', pow: 75, rng: 75 },
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
    document.getElementById('st-pow-val').innerText = s.pow + '%';
    document.getElementById('st-pow').style.width = s.pow + '%';
    document.getElementById('st-rng-val').innerText = s.rng + '%';
    document.getElementById('st-rng').style.width = s.rng + '%';
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

function triggerEpicCombatExplosion(pos) {
    for (let i = 0; i < 22; i++) {
        const p = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.14, 0.16), i % 2 === 0 ? mats.cardboard : mats.woodPallet);
        p.position.copy(pos); p.position.y += 0.4; scene.add(p);
        const vx = (Math.random()-0.5)*0.28, vz = (Math.random()-0.5)*0.28; let vy = Math.random()*0.28 + 0.08;
        const tick = () => {
            p.position.x += vx; p.position.y += vy; p.position.z += vz; vy -= 0.014;
            p.rotation.x += 0.18; p.scale.multiplyScalar(0.93);
            if (p.scale.x > 0.03 && p.position.y > -0.2) requestAnimationFrame(tick); else scene.remove(p);
        };
        tick();
    }
}

// SINEMATIK EPIC COMBAT & CUTSCENE ZOOM
function executeMove(piece, moveData) {
    isAnimating = true; clearHighlights();
    const sx = piece.position.x, sz = piece.position.z;
    const ex = moveData.x * tileSize - offset, ez = moveData.z * tileSize - offset;
    
    // Efek Sinematik Kamera Mendekat Saat Menyerang Lawan
    if (moveData.attack) {
        camera.position.set(ex, 3.2, ez + 3.8);
        controls.target.set(ex, 0.6, ez);
    }

    let prog = 0;
    const step = () => {
        prog += 0.065;
        if (prog < 1) {
            piece.position.x = sx + (ex - sx) * prog;
            piece.position.z = sz + (ez - sz) * prog;
            piece.position.y = 0.05 + Math.sin(prog * Math.PI) * (moveData.attack ? 0.9 : 0.55);
            requestAnimationFrame(step);
        } else {
            piece.position.set(ex, 0.05, ez);
            piece.userData.gridX = moveData.x; piece.userData.gridZ = moveData.z; piece.userData.hasMoved = true;
            const uName = unitSpecs[piece.userData.type].name;
            const coord = `${cols[moveData.x]}${8 - moveData.z}`;
            let msg = `${uName} bergeser ke zona ${coord}.`;

            if (moveData.attack && moveData.target) {
                const v = moveData.target; v.userData.alive = false; scene.remove(v);
                triggerEpicCombatExplosion(piece.position);
                const vName = unitSpecs[v.userData.type].name;
                msg = `⚔️ EPIC COMBAT! ${uName} melibas habis ${vName} di ${coord}!`;
                addBattleLog(`${uName} 💥 ELIMINATED ${vName} (${coord})`, true);
                updateScoreUI();
                if (v.userData.type === 'king') {
                    updateHUD(`🏆 OVERRIDE SELESAI! Tim ${currentTurn.toUpperCase()} menguasai WMS Server!`);
                    isAnimating = false; return;
                }
            } else {
                addBattleLog(`${uName} ➔ ${coord}`, false);
            }

            currentTurn = currentTurn === 'blue' ? 'orange' : 'blue';
            selectedPiece = null; validMoves = []; isAnimating = false;
            updateHUD(msg);

            // Kembalikan Posisi Kamera Taktis
            camera.position.set(0, 11.2, 14.2); controls.target.set(0, 0.5, 0); controls.update();

            if (vsAI && currentTurn === 'orange') setTimeout(runAIBot, 500);
        }
    };
    step();
}

function runAIBot() {
    const aiPieces = pieces.filter(p => p.userData.alive && p.userData.team === 'orange');
    let allMoves = [];
    aiPieces.forEach(p => {
        getValidMoves(p).forEach(m => {
            let score = m.attack && m.target ? weights[m.target.userData.type] * 1.5 : (m.z * 0.5 + Math.random() * 2);
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
    m.userData = { type, team, gridX: gx, gridZ: gz, alive: true, hasMoved: false };
    scene.add(m); pieces.push(m);
}

function resetGame() {
    clearHighlights(); pieces.forEach(p => scene.remove(p)); pieces = [];
    humanIdles.length = 0; animatedParts.length = 0;
    document.getElementById('move-history').innerHTML = '';
    selectedPiece = null; validMoves = []; currentTurn = 'blue'; isAnimating = false;
    const row = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook'];
    for (let i = 0; i < 8; i++) {
        spawnUnit(row[i], 'orange', i, 0); spawnUnit('pawn', 'orange', i, 1);
        spawnUnit('pawn', 'blue', i, 6); spawnUnit(row[i], 'blue', i, 7);
    }
    updateScoreUI();
    addBattleLog("Shift Operasional Dimulai. Sistem Tempur Epic Aktif.");
    updateHUD("Shift Baru Dimulai! Perbedaan peran unit & aksi tempur sinematik siap dimainkan.");
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

const clock = new THREE.Clock();
resetGame();

function animate() {
    requestAnimationFrame(animate);
    const t = clock.getElapsedTime();

    animatedParts.forEach(p => {
        if (p.type === 'spin') p.mesh.rotation.y = t * 1.8;
    });

    humanIdles.forEach(h => {
        h.upperBody.position.y = h.baseY + Math.sin(t * 2.4 + h.phase) * 0.007;
        h.headGroup.rotation.y = Math.sin(t * 1.1 + h.phase) * 0.07;
    });

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
