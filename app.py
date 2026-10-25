import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="WAREHOUSE COMMAND: TACTICAL CHESS 3D",
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
<title>Warehouse Command: Tactical 3D Chess</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=Rajdhani:wght@500;600;700&display=swap" rel="stylesheet">
<style>
    * { box-sizing: border-box; user-select: none; }
    body {
        margin: 0; padding: 0; overflow: hidden;
        background: #05070b;
        font-family: 'Rajdhani', 'Segoe UI', sans-serif;
        color: #e2e8f0;
    }
    #canvas-container { width: 100vw; height: 100vh; display: block; }

    /* CINEMATIC VIGNETTE OVERLAY (Mencegah Silau di Tepi Layar) */
    #vignette {
        position: fixed; inset: 0; pointer-events: none; z-index: 2;
        background: radial-gradient(circle at center, transparent 55%, rgba(3, 6, 12, 0.75) 100%);
    }

    /* TOP COMMAND BAR (AAA ESPORTS / TACTICAL HUD) */
    #top-bar {
        position: absolute; top: 0; left: 0; right: 0; height: 68px;
        background: linear-gradient(180deg, rgba(9, 13, 22, 0.96) 0%, rgba(9, 13, 22, 0.75) 100%);
        border-bottom: 1px solid rgba(56, 189, 248, 0.22);
        display: flex; justify-content: space-between; align-items: center;
        padding: 0 24px; z-index: 10; backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.7);
    }
    .brand-cluster { display: flex; align-items: center; gap: 14px; }
    .brand-emblem {
        width: 42px; height: 42px; border-radius: 8px;
        background: linear-gradient(135deg, #f59e0b 0%, #b45309 100%);
        display: flex; align-items: center; justify-content: center;
        font-family: 'Orbitron', sans-serif; font-weight: 900; font-size: 20px; color: #05070b;
        box-shadow: 0 0 15px rgba(245, 158, 11, 0.4);
    }
    .brand-title h1 {
        margin: 0; font-family: 'Orbitron', sans-serif; font-size: 16px;
        font-weight: 800; letter-spacing: 2px; color: #f8fafc;
    }
    .brand-title span {
        font-size: 11px; color: #f59e0b; text-transform: uppercase;
        letter-spacing: 1.5px; font-weight: 700; display: block;
    }

    /* SCORE & TURN CENTER HUD */
    .versus-hud {
        display: flex; align-items: center; gap: 18px;
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(148, 163, 184, 0.2);
        padding: 6px 22px; border-radius: 40px;
    }
    .team-score { display: flex; align-items: center; gap: 10px; font-weight: 700; font-size: 14px; letter-spacing: 1px; }
    .team-score.blue { color: #38bdf8; }
    .team-score.orange { color: #fbbf24; }
    .score-pill {
        background: rgba(2, 6, 23, 0.8); padding: 2px 10px; border-radius: 12px;
        font-family: 'Orbitron', sans-serif; font-size: 14px; border: 1px solid currentColor;
    }
    #turn-banner {
        padding: 5px 16px; border-radius: 20px;
        font-family: 'Orbitron', sans-serif; font-size: 11px; font-weight: 800;
        letter-spacing: 1.5px; text-transform: uppercase;
        transition: all 0.3s;
    }
    .turn-blue { background: rgba(2, 132, 199, 0.3); color: #38bdf8; border: 1px solid #38bdf8; box-shadow: 0 0 14px rgba(56, 189, 248, 0.3); }
    .turn-orange { background: rgba(217, 119, 6, 0.3); color: #fbbf24; border: 1px solid #fbbf24; box-shadow: 0 0 14px rgba(251, 191, 36, 0.3); }

    /* TOP RIGHT CONTROLS */
    .toolbar { display: flex; gap: 8px; }
    .t-btn {
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(148, 163, 184, 0.3);
        color: #cbd5e1; padding: 8px 13px; border-radius: 6px;
        font-family: 'Rajdhani', sans-serif; font-weight: 700; font-size: 13px;
        letter-spacing: 0.8px; text-transform: uppercase; cursor: pointer;
        transition: all 0.2s;
    }
    .t-btn:hover { background: rgba(56, 189, 248, 0.15); border-color: #38bdf8; color: #fff; transform: translateY(-1px); }
    .t-btn.active { background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%); border-color: #38bdf8; color: #fff; }

    /* LEFT PANEL: UNIT INSPECTOR TELEMETRY CARD */
    #unit-inspector {
        position: absolute; top: 86px; left: 20px; width: 270px;
        background: linear-gradient(160deg, rgba(11, 17, 30, 0.92) 0%, rgba(7, 11, 20, 0.95) 100%);
        border: 1px solid rgba(56, 189, 248, 0.28);
        border-left: 4px solid #38bdf8;
        border-radius: 8px; padding: 14px 16px; z-index: 10;
        backdrop-filter: blur(10px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.75);
    }
    .panel-tag {
        font-family: 'Orbitron', sans-serif; font-size: 10px; color: #64748b;
        letter-spacing: 2px; text-transform: uppercase; margin-bottom: 4px;
    }
    #insp-name {
        font-family: 'Orbitron', sans-serif; font-size: 15px; font-weight: 800;
        color: #f8fafc; margin: 0 0 2px 0;
    }
    #insp-role { font-size: 12px; color: #f59e0b; font-weight: 700; margin-bottom: 10px; }
    .stat-row { margin: 6px 0; }
    .stat-label { display: flex; justify-content: space-between; font-size: 11px; color: #94a3b8; font-weight: 600; margin-bottom: 3px; }
    .stat-bar { height: 5px; background: rgba(30, 41, 59, 0.9); border-radius: 3px; overflow: hidden; }
    .stat-fill { height: 100%; background: linear-gradient(90deg, #0284c7, #38bdf8); transition: width 0.3s; }
    .roster-mini {
        margin-top: 12px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.08);
        font-size: 11px; color: #94a3b8; line-height: 1.55;
    }
    .roster-mini b { color: #e2e8f0; }

    /* RIGHT PANEL: BATTLE OPERATIONS LOG */
    #ops-panel {
        position: absolute; top: 86px; right: 20px; width: 265px;
        background: linear-gradient(160deg, rgba(11, 17, 30, 0.9) 0%, rgba(7, 11, 20, 0.94) 100%);
        border: 1px solid rgba(245, 158, 11, 0.25);
        border-right: 4px solid #f59e0b;
        border-radius: 8px; padding: 14px 16px; z-index: 10;
        backdrop-filter: blur(10px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.75);
    }
    #move-history {
        max-height: 150px; overflow-y: auto; font-size: 12px;
        display: flex; flex-direction: column; gap: 5px; margin-top: 8px;
        padding-right: 4px;
    }
    .log-entry {
        background: rgba(15, 23, 42, 0.75); padding: 5px 8px; border-radius: 4px;
        border-left: 2px solid #475569; color: #cbd5e1; font-size: 11.5px;
    }
    .log-entry.combat { border-left-color: #ef4444; background: rgba(127, 29, 29, 0.25); color: #fca5a5; }

    /* BOTTOM TACTICAL TICKER */
    #bottom-ticker {
        position: absolute; bottom: 18px; left: 50%; transform: translateX(-50%);
        background: rgba(9, 13, 22, 0.92);
        border: 1px solid rgba(56, 189, 248, 0.3);
        padding: 10px 28px; border-radius: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
        display: flex; align-items: center; gap: 12px; z-index: 10;
        font-size: 14px; font-weight: 600; letter-spacing: 0.5px;
    }
    .pulse-dot {
        width: 9px; height: 9px; border-radius: 50%; background: #22c55e;
        box-shadow: 0 0 10px #22c55e;
    }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>
    <div id="vignette"></div>

    <!-- TOP PROFESSIONAL GAME BAR -->
    <div id="top-bar">
        <div class="brand-cluster">
            <div class="brand-emblem">WC</div>
            <div class="brand-title">
                <h1>WAREHOUSE COMMAND</h1>
                <span>Tactical Logistics Operations • 3D Simulator</span>
            </div>
        </div>

        <div class="versus-hud">
            <div class="team-score blue">
                <span>INBOUND</span>
                <span id="score-blue" class="score-pill">16</span>
            </div>
            <div id="turn-banner" class="turn-blue">SHIFT BIRU AKTIF</div>
            <div class="team-score orange">
                <span id="score-orange" class="score-pill">16</span>
                <span>OUTBOUND</span>
            </div>
        </div>

        <div class="toolbar">
            <button id="btn-ai" class="t-btn active" onclick="toggleAI()">🤖 vs AI Bot</button>
            <button class="t-btn" onclick="setCameraView('closeup')">🔍 Inspeksi Unit</button>
            <button class="t-btn" onclick="setCameraView('perspective')">🎥 Kamera Taktis</button>
            <button class="t-btn" onclick="setCameraView('top')">📐 Radar Atas</button>
            <button class="t-btn" onclick="resetGame()">🔄 Reset Shift</button>
        </div>
    </div>

    <!-- LEFT TELEMETRY & UNIT INSPECTOR -->
    <div id="unit-inspector">
        <div class="panel-tag">UNIT TELEMETRY INSPECTOR</div>
        <h2 id="insp-name">COUNTERBALANCE FORKLIFT</h2>
        <div id="insp-role">Heavy Logistics Armor • Benteng (Rook)</div>
        <div class="stat-row">
            <div class="stat-label"><span>DAYA ANGKUT / POWER</span><span id="st-pow-val">95%</span></div>
            <div class="stat-bar"><div id="st-pow" class="stat-fill" style="width:95%"></div></div>
        </div>
        <div class="stat-row">
            <div class="stat-label"><span>MOBILITAS / JANGKAUAN</span><span id="st-rng-val">90%</span></div>
            <div class="stat-bar"><div id="st-rng" class="stat-fill" style="width:90%"></div></div>
        </div>
        <div class="roster-mini">
            <div><b>Pion:</b> Operator Gudang (Bawa Kardus)</div>
            <div><b>Benteng:</b> Heavy Forklift + Pengemudi</div>
            <div><b>Kuda:</b> Electric Reach Truck + Operator</div>
            <div><b>Gajah:</b> QC Auditor (Laser Scanner)</div>
            <div><b>Menteri:</b> Ops Supervisor (HT + Tablet)</div>
            <div><b>Raja:</b> Main WMS Server Core</div>
        </div>
    </div>

    <!-- RIGHT BATTLE LOG -->
    <div id="ops-panel">
        <div class="panel-tag">WMS OPERATIONS LOG</div>
        <div style="font-size:12px; color:#f59e0b; font-weight:700;">RIWAYAT TRANSMISI GUDANG</div>
        <div id="move-history"></div>
    </div>

    <!-- BOTTOM STATUS TICKER -->
    <div id="bottom-ticker">
        <div class="pulse-dot"></div>
        <div id="action-log">Sistem WMS Online. Pilih personel atau kendaraan Biru untuk memulai instruksi kerja.</div>
    </div>

    <div id="canvas-container"></div>

<script>
// ============================================================================
// 1. CINEMATIC ANTI-GLARE RENDERER (TANPA ROOM-ENVIRONMENT YANG MENYILAUKAN)
// ============================================================================
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x060911);
scene.fog = new THREE.FogExp2(0x060911, 0.015);

const camera = new THREE.PerspectiveCamera(38, window.innerWidth / window.innerHeight, 0.1, 220);
camera.position.set(0, 11.2, 14.2);

const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
// Exposure diturunkan ke 0.72 agar warna sangat pekat, kontras tinggi & TIDAK SILAU
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

// BALANCED DRAMATIC THREE-POINT STUDIO LIGHTING
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

// Rim Lights Lembut (Biru Dingin & Amber Hangat)
const rimBlue = new THREE.PointLight(0x0284c7, 0.85, 26); rimBlue.position.set(-10, 6, 9); scene.add(rimBlue);
const rimAmber = new THREE.PointLight(0xd97706, 0.85, 26); rimAmber.position.set(10, 6, -9); scene.add(rimAmber);

// ============================================================================
// 2. HIGH-CONTRAST DARK INDUSTRIAL TEXTURES (ZERO GLARE)
// ============================================================================
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
    // Warna lantai jauh lebih gelap & elegan (Dark Slate vs Deep Steel) agar tidak silau
    ctx.fillStyle = isDark ? '#0f172a' : '#1e293b';
    ctx.fillRect(0,0,256,256);

    // Tekstur micro-grid taktis
    ctx.strokeStyle = isDark ? 'rgba(51,65,85,0.35)' : 'rgba(71,85,105,0.4)';
    ctx.lineWidth = 1;
    for(let g=32; g<256; g+=32) {
        ctx.beginPath(); ctx.moveTo(g,0); ctx.lineTo(g,256); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(0,g); ctx.lineTo(256,g); ctx.stroke();
    }

    // Garis border petak industri
    ctx.strokeStyle = isDark ? '#1e293b' : '#334155';
    ctx.lineWidth = 8; ctx.strokeRect(4,4,248,248);

    // Siku marka kuning redup di sudut petak
    ctx.fillStyle = 'rgba(234, 179, 8, 0.35)';
    ctx.fillRect(14,14,16,3); ctx.fillRect(14,14,3,16);
    ctx.fillRect(226,14,16,3); ctx.fillRect(239,14,3,16);

    if (lbl) {
        ctx.fillStyle = isDark ? 'rgba(148,163,184,0.45)' : 'rgba(203,213,225,0.55)';
        ctx.font = 'bold 30px Orbitron, monospace';
        ctx.fillText(lbl, 18, 234);
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
    ctx.strokeStyle = '#5c3a1b'; ctx.lineWidth = 6; ctx.strokeRect(3,3,250,250);
    return new THREE.CanvasTexture(c);
}

function makeFaceTex() {
    const c = document.createElement('canvas'); c.width = 256; c.height = 256;
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#d99b72'; ctx.fillRect(0,0,256,256);
    // Rambut samping & belakang
    ctx.fillStyle = '#1e1b18'; ctx.fillRect(0, 0, 256, 75);
    // Alis tegas
    ctx.fillStyle = '#1e1b18';
    ctx.fillRect(88, 96, 28, 7); ctx.fillRect(140, 96, 28, 7);
    // Mata putih + pupil hitam
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(92, 108, 22, 12); ctx.fillRect(142, 108, 22, 12);
    ctx.fillStyle = '#0f172a';
    ctx.fillRect(100, 109, 10, 10); ctx.fillRect(146, 109, 10, 10);
    // Mulut & ekspresi tegas
    ctx.fillStyle = '#8c4f32';
    ctx.fillRect(110, 162, 36, 6);
    return new THREE.CanvasTexture(c);
}

// ============================================================================
// 3. FULL WAREHOUSE BUILDING ARCHITECTURE (WALLS, DOCK DOORS, RACKS, BOLLARDS)
// ============================================================================
const boardGroup = new THREE.Group(); scene.add(boardGroup);

// Lantai Beton Gudang Utama (Matte Dark Concrete)
const warehouseFloor = new THREE.Mesh(
    new THREE.PlaneGeometry(80, 80),
    new THREE.MeshStandardMaterial({ color: 0x070a12, roughness: 0.75, metalness: 0.1 })
);
warehouseFloor.rotation.x = -Math.PI/2; warehouseFloor.position.y = -0.36; warehouseFloor.receiveShadow = true;
scene.add(warehouseFloor);

// Bingkai Platform Taktis Papan Catur
const base = new THREE.Mesh(
    new THREE.BoxGeometry(10.6, 0.36, 10.6),
    new THREE.MeshStandardMaterial({ color: 0x0b111e, roughness: 0.4, metalness: 0.5 })
);
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
            new THREE.MeshStandardMaterial({
                map: makeTileTex(isDark, lbl),
                roughness: 0.48, // Tidak lagi terlalu licin/mengkilap agar bebas silau
                metalness: 0.12
            })
        );
        tile.position.set(x * tileSize - offset, 0, z * tileSize - offset);
        tile.receiveShadow = true;
        tile.userData = { gridX: x, gridZ: z };
        boardGroup.add(tile);
        tiles[x][z] = tile;
    }
}

// Dinding Belakang Loading Dock & Pintu Rolling Door Gudang
const backWall = new THREE.Mesh(
    new THREE.BoxGeometry(36, 10, 0.5),
    new THREE.MeshStandardMaterial({ color: 0x0b111e, roughness: 0.8 })
);
backWall.position.set(0, 4.6, -13.5);
scene.add(backWall);

// 4 Pintu Loading Dock dengan Lampu Indikator Hijau/Merah
[-9, -3, 3, 9].forEach((dx, i) => {
    const doorFrame = new THREE.Mesh(new THREE.BoxGeometry(3.4, 4.2, 0.6), new THREE.MeshStandardMaterial({ color: 0x1e293b }));
    doorFrame.position.set(dx, 1.8, -13.4); scene.add(doorFrame);

    const shutter = new THREE.Mesh(new THREE.BoxGeometry(3.0, 3.8, 0.65), new THREE.MeshStandardMaterial({ color: 0x334155, metalness: 0.5, roughness: 0.5 }));
    shutter.position.set(dx, 1.7, -13.38); scene.add(shutter);

    // Lampu Status Dock
    const dockLight = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.15, 0.7), new THREE.MeshStandardMaterial({
        color: i % 2 === 0 ? 0x22c55e : 0xf59e0b,
        emissive: i % 2 === 0 ? 0x16a34a : 0xd97706,
        emissiveIntensity: 0.9
    }));
    dockLight.position.set(dx, 4.1, -13.35); scene.add(dockLight);
});

// Tiang Bollard Pelindung Kuning di Sudut Area Papan
const bollardMat = new THREE.MeshStandardMaterial({ color: 0xeab308, roughness: 0.35, metalness: 0.3 });
[[-5.6, -5.6], [5.6, -5.6], [-5.6, 5.6], [5.6, 5.6]].forEach(([bx, bz]) => {
    const post = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.1, 0.9, 14), bollardMat);
    post.position.set(bx, 0.1, bz); post.castShadow = true; scene.add(post);
});

// Rak Gudang Heavy-Duty di Kiri & Kanan
const boxTex = makeCardboardTex();
function buildRack(xPos, zPos, rotY) {
    const r = new THREE.Group();
    const uMat = new THREE.MeshStandardMaterial({ color: 0x1e3a8a, metalness: 0.5, roughness: 0.4 });
    const bMat = new THREE.MeshStandardMaterial({ color: 0xc2410c, metalness: 0.4, roughness: 0.4 });
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

// ============================================================================
// 4. REALISTIC CHARACTER ANATOMY & CAD VEHICLE MODELS (WITH SEATED DRIVERS!)
// ============================================================================
const animatedParts = [];
const humanIdles = [];
const faceTex = makeFaceTex();

const mats = {
    skin: new THREE.MeshStandardMaterial({ color: 0xd99b72, roughness: 0.55 }),
    face: new THREE.MeshStandardMaterial({ map: faceTex, roughness: 0.55 }),
    cargoPants: new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.85 }),
    kneePad: new THREE.MeshStandardMaterial({ color: 0x090d16, roughness: 0.5 }),
    darkIron: new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.7, roughness: 0.35 }),
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
    stretchWrap: new THREE.MeshStandardMaterial({ color: 0xbae6fd, roughness: 0.2, transparent: true, opacity: 0.38 }),
    serverGlass: new THREE.MeshStandardMaterial({ color: 0x090d16, roughness: 0.15, transparent: true, opacity: 0.7 }),
    amberBeacon: new THREE.MeshStandardMaterial({ color: 0xf59e0b, emissive: 0xd97706, emissiveIntensity: 1.0 })
};

function makeDetailedWheel(radius, width, rimMat) {
    const wGroup = new THREE.Group();
    const tire = new THREE.Mesh(new THREE.CylinderGeometry(radius, radius, width, 20), mats.rubberTire);
    tire.rotation.z = Math.PI / 2; tire.castShadow = true; wGroup.add(tire);
    const rim = new THREE.Mesh(new THREE.CylinderGeometry(radius * 0.55, radius * 0.55, width + 0.01, 14), rimMat);
    rim.rotation.z = Math.PI / 2; wGroup.add(rim);
    const hub = new THREE.Mesh(new THREE.CylinderGeometry(radius * 0.2, radius * 0.2, width + 0.02, 10), mats.blackSteel);
    hub.rotation.z = Math.PI / 2; wGroup.add(hub);
    return wGroup;
}

function makeEuroPallet(w, l) {
    const p = new THREE.Group();
    for (let i = -2; i <= 2; i++) {
        const slat = new THREE.Mesh(new THREE.BoxGeometry(w, 0.02, l * 0.16), mats.woodPallet);
        slat.position.set(0, 0.06, i * (l * 0.2)); slat.castShadow = true; p.add(slat);
    }
    [-w * 0.4, 0, w * 0.4].forEach(bx => {
        const block = new THREE.Mesh(new THREE.BoxGeometry(0.055, 0.045, l * 0.95), mats.woodPallet);
        block.position.set(bx, 0.03, 0); p.add(block);
    });
    return p;
}

// PEMBANGUN MANUSIA REALISTIS (DENGAN SAKU KARGO, KNEE PADS, KERAH BAJU, WAJAH & RAMBUT)
function buildRealisticHuman(teamMat, vestMat, helmetMat, hasGoggles, isSeated = false) {
    const human = new THREE.Group();

    if (!isSeated) {
        // Kaki Berdiri Proporsional + Knee Pads + Saku Kargo Samping
        [-0.095, 0.095].forEach(lx => {
            const sole = new THREE.Mesh(new THREE.BoxGeometry(0.095, 0.038, 0.2), mats.rubberTire);
            sole.position.set(lx, 0.019, -0.02); human.add(sole);

            const boot = new THREE.Mesh(new THREE.BoxGeometry(0.088, 0.09, 0.15), mats.leather);
            boot.position.set(lx, 0.075, -0.01); boot.castShadow = true; human.add(boot);

            const calf = new THREE.Mesh(new THREE.CylinderGeometry(0.052, 0.044, 0.22, 14), mats.cargoPants);
            calf.position.set(lx, 0.21, 0); calf.castShadow = true; human.add(calf);

            // Pelindung Lutut Taktis (Knee Pad)
            const kPad = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.065, 0.03), mats.kneePad);
            kPad.position.set(lx, 0.31, -0.045); human.add(kPad);

            const thigh = new THREE.Mesh(new THREE.CylinderGeometry(0.064, 0.054, 0.23, 14), mats.cargoPants);
            thigh.position.set(lx, 0.43, 0); thigh.castShadow = true; human.add(thigh);

            // Saku Kargo Timbul di Paha Luar
            const pocket = new THREE.Mesh(new THREE.BoxGeometry(0.025, 0.09, 0.08), mats.cargoPants);
            pocket.position.set(lx + (lx < 0 ? -0.055 : 0.055), 0.43, 0); human.add(pocket);
        });
    } else {
        // Posisi Kaki Duduk Mengemudi di Kursi Forklift
        [-0.09, 0.09].forEach(lx => {
            const thigh = new THREE.Mesh(new THREE.CylinderGeometry(0.058, 0.05, 0.22, 12), mats.cargoPants);
            thigh.rotation.x = Math.PI / 2.2;
            thigh.position.set(lx, 0.52, -0.08); human.add(thigh);

            const calf = new THREE.Mesh(new THREE.CylinderGeometry(0.048, 0.04, 0.2, 12), mats.cargoPants);
            calf.position.set(lx, 0.4, -0.17); human.add(calf);

            const boot = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.07, 0.15), mats.leather);
            boot.position.set(lx, 0.3, -0.2); human.add(boot);
        });
    }

    const baseY = isSeated ? 0.54 : 0.54;
    const pelvis = new THREE.Mesh(new THREE.BoxGeometry(0.26, 0.1, 0.16), mats.cargoPants);
    pelvis.position.set(0, baseY, 0); human.add(pelvis);

    const belt = new THREE.Mesh(new THREE.BoxGeometry(0.275, 0.04, 0.175), mats.leather);
    belt.position.set(0, baseY + 0.04, 0); human.add(belt);
    const buckle = new THREE.Mesh(new THREE.BoxGeometry(0.055, 0.042, 0.185), mats.chrome);
    buckle.position.set(0, baseY + 0.04, 0); human.add(buckle);

    const upperBody = new THREE.Group();
    upperBody.position.set(0, baseY + 0.06, 0);
    human.add(upperBody);

    // Torso Anatomis (Bahu Lebar, Pinggang Ramping)
    const chest = new THREE.Mesh(new THREE.CylinderGeometry(0.155, 0.125, 0.34, 16), teamMat);
    chest.scale.set(1.18, 1, 0.78); chest.position.set(0, 0.17, 0); chest.castShadow = true;
    upperBody.add(chest);

    // Rompi Safety
    const vest = new THREE.Mesh(new THREE.CylinderGeometry(0.162, 0.132, 0.31, 16), vestMat);
    vest.scale.set(1.19, 1, 0.8); vest.position.set(0, 0.17, 0); vest.castShadow = true;
    upperBody.add(vest);

    // Garis Scotchlite Perak
    [0.08, 0.19].forEach(sy => {
        const hStrip = new THREE.Mesh(new THREE.CylinderGeometry(0.165, 0.145, 0.028, 16), mats.silverReflective);
        hStrip.scale.set(1.2, 1, 0.81); hStrip.position.set(0, sy, 0); upperBody.add(hStrip);
    });

    // Kerah Baju Polo
    const collar = new THREE.Mesh(new THREE.TorusGeometry(0.068, 0.018, 8, 16), teamMat);
    collar.rotation.x = Math.PI / 2; collar.position.set(0, 0.34, 0); upperBody.add(collar);

    const neck = new THREE.Mesh(new THREE.CylinderGeometry(0.052, 0.06, 0.08, 14), mats.skin);
    neck.position.set(0, 0.37, 0); upperBody.add(neck);

    const headGroup = new THREE.Group();
    headGroup.position.set(0, 0.47, 0);
    upperBody.add(headGroup);

    // Kepala dengan Tekstur Wajah (Mata, Alis, Rambut, Mulut)
    const headMesh = new THREE.Mesh(new THREE.SphereGeometry(0.112, 20, 20), mats.face);
    headMesh.scale.set(0.95, 1.08, 1.0);
    headMesh.rotation.y = -Math.PI / 2; // Arahkan tekstur wajah ke depan (-Z)
    headMesh.castShadow = true;
    headGroup.add(headMesh);

    const nose = new THREE.Mesh(new THREE.ConeGeometry(0.02, 0.045, 8), mats.skin);
    nose.rotation.x = -Math.PI / 2; nose.position.set(0, -0.005, -0.115); headGroup.add(nose);

    [-0.105, 0.105].forEach(ex => {
        const ear = new THREE.Mesh(new THREE.SphereGeometry(0.024, 10, 10), mats.skin);
        ear.scale.set(0.5, 1.2, 0.8); ear.position.set(ex, 0, 0); headGroup.add(ear);
    });

    if (hasGoggles) {
        const goggles = new THREE.Mesh(new THREE.BoxGeometry(0.175, 0.045, 0.07), mats.visorGlass);
        goggles.position.set(0, 0.015, -0.09); headGroup.add(goggles);
    }

    // Helm Proyek Industrial dengan Brim & Suspensi
    const dome = new THREE.Mesh(new THREE.SphereGeometry(0.125, 20, 14, 0, Math.PI * 2, 0, Math.PI * 0.54), helmetMat);
    dome.position.set(0, 0.025, 0); dome.castShadow = true; headGroup.add(dome);
    const ridge = new THREE.Mesh(new THREE.BoxGeometry(0.034, 0.03, 0.22), helmetMat);
    ridge.position.set(0, 0.14, 0); headGroup.add(ridge);
    const brim = new THREE.Mesh(new THREE.CylinderGeometry(0.135, 0.142, 0.016, 20), helmetMat);
    brim.position.set(0, 0.03, -0.015); headGroup.add(brim);

    humanIdles.push({ upperBody, headGroup, baseY: baseY + 0.06, phase: Math.random() * Math.PI * 2 });
    return { root: human, upperBody, headGroup };
}

function attachArm(upperBody, side, sRotX, sRotZ, eRotX, teamMat, gloveMat) {
    const sGroup = new THREE.Group();
    sGroup.position.set(side * 0.195, 0.29, 0);
    sGroup.rotation.set(sRotX, 0, sRotZ);
    upperBody.add(sGroup);

    const shoulder = new THREE.Mesh(new THREE.SphereGeometry(0.05, 12, 12), teamMat);
    sGroup.add(shoulder);

    const upperArm = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.038, 0.18, 12), teamMat);
    upperArm.position.set(0, -0.09, 0); upperArm.castShadow = true; sGroup.add(upperArm);

    const eGroup = new THREE.Group();
    eGroup.position.set(0, -0.18, 0);
    eGroup.rotation.x = eRotX;
    sGroup.add(eGroup);

    const forearm = new THREE.Mesh(new THREE.CylinderGeometry(0.038, 0.032, 0.17, 12), mats.skin);
    forearm.position.set(0, -0.085, 0); forearm.castShadow = true; eGroup.add(forearm);

    const hand = new THREE.Mesh(new THREE.SphereGeometry(0.038, 12, 12), gloveMat);
    hand.scale.set(0.85, 1.1, 1.2); hand.position.set(0, -0.18, 0); eGroup.add(hand);

    return { sGroup, eGroup, hand };
}

// ============================================================================
// 5. UNIT FACTORY (6 LOGISTICS CLASSES)
// ============================================================================
function createUnitMesh(type, team) {
    const root = new THREE.Group();
    const isBlue = team === 'blue';

    const teamPrimary = new THREE.MeshStandardMaterial({
        color: isBlue ? 0x0369a1 : 0xc2410c, roughness: 0.4, metalness: 0.25
    });
    const teamAccent = new THREE.MeshStandardMaterial({
        color: isBlue ? 0x0ea5e9 : 0xf59e0b, roughness: 0.35, metalness: 0.35
    });
    const vestMat = isBlue ? mats.hiVisLime : mats.hiVisOrange;

    // Ring Taktis Tipis
    const baseRing = new THREE.Mesh(new THREE.TorusGeometry(0.46, 0.016, 10, 32), teamAccent);
    baseRing.rotation.x = Math.PI / 2; baseRing.position.y = 0.015;
    root.add(baseRing);

    const dir = new THREE.Group();
    dir.rotation.y = isBlue ? 0 : Math.PI;
    root.add(dir);

    // 1. PION: OPERATOR PICKER (MEMBAWA KARDUS LOGISTIK)
    if (type === 'pawn') {
        const { root: fig, upperBody } = buildRealisticHuman(teamPrimary, vestMat, teamAccent, false, false);
        dir.add(fig);
        attachArm(upperBody, -1, 0.65, -0.15, 1.05, teamPrimary, mats.leather);
        attachArm(upperBody, 1, 0.65, 0.15, 1.05, teamPrimary, mats.leather);

        const box = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.24, 0.27), mats.cardboard);
        box.position.set(0, 0.13, -0.25); box.castShadow = true; upperBody.add(box);
    }

    // 2. BENTENG: COUNTERBALANCE FORKLIFT + OPERATOR DUDUK MENGEMUDI DI DALAM KABIN!
    else if (type === 'rook') {
        const wFL = makeDetailedWheel(0.145, 0.095, teamAccent); wFL.position.set(-0.28, 0.145, -0.22); dir.add(wFL);
        const wFR = makeDetailedWheel(0.145, 0.095, teamAccent); wFR.position.set(0.28, 0.145, -0.22); dir.add(wFR);
        const wBL = makeDetailedWheel(0.105, 0.085, teamAccent); wBL.position.set(-0.25, 0.105, 0.28); dir.add(wBL);
        const wBR = makeDetailedWheel(0.105, 0.085, teamAccent); wBR.position.set(0.25, 0.105, 0.28); dir.add(wBR);

        const chassis = new THREE.Mesh(new THREE.BoxGeometry(0.48, 0.15, 0.68), mats.blackSteel);
        chassis.position.set(0, 0.16, 0.04); chassis.castShadow = true; dir.add(chassis);

        const bodyHood = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.22, 0.34), teamPrimary);
        bodyHood.position.set(0, 0.31, -0.06); bodyHood.castShadow = true; dir.add(bodyHood);

        const cw = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.24, 0.34, 20), mats.darkIron);
        cw.scale.set(1, 1, 0.72); cw.position.set(0, 0.31, 0.27); cw.castShadow = true; dir.add(cw);

        // Kursi & Pengemudi Duduk Memegang Setir Forklift
        const seat = new THREE.Mesh(new THREE.BoxGeometry(0.24, 0.05, 0.22), mats.leather);
        seat.position.set(0, 0.44, 0.06); dir.add(seat);

        const driver = buildRealisticHuman(teamPrimary, vestMat, teamAccent, true, true);
        driver.root.scale.set(0.76, 0.76, 0.76);
        driver.root.position.set(0, 0.06, 0.06);
        attachArm(driver.upperBody, -1, 0.85, -0.1, 0.65, teamPrimary, mats.leather);
        attachArm(driver.upperBody, 1, 0.85, 0.1, 0.65, teamPrimary, mats.leather);
        dir.add(driver.root);

        // Setir Kemudi
        const steerCol = new THREE.Mesh(new THREE.CylinderGeometry(0.022, 0.028, 0.25, 10), mats.blackSteel);
        steerCol.position.set(0, 0.52, -0.15); steerCol.rotation.x = 0.42; dir.add(steerCol);
        const sWheel = new THREE.Mesh(new THREE.TorusGeometry(0.07, 0.013, 8, 18), mats.leather);
        sWheel.position.set(0, 0.63, -0.1); sWheel.rotation.x = Math.PI/2 + 0.42; dir.add(sWheel);

        // Overhead Guard Roll-Cage
        [[-0.22, -0.2], [0.22, -0.2], [-0.22, 0.24], [0.22, 0.24]].forEach(([px, pz]) => {
            const post = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.62, 10), mats.blackSteel);
            post.position.set(px, 0.72, pz); post.castShadow = true; dir.add(post);
        });
        const roof = new THREE.Mesh(new THREE.BoxGeometry(0.48, 0.035, 0.48), mats.blackSteel);
        roof.position.set(0, 1.03, 0.02); dir.add(roof);

        const beacon = new THREE.Mesh(new THREE.CylinderGeometry(0.038, 0.048, 0.08, 12), mats.amberBeacon);
        beacon.position.set(0, 1.09, 0.18); dir.add(beacon);
        animatedParts.push({ mesh: beacon, type: 'pulse' });

        // Tiang Hidrolik & Garpu Baja
        [-0.15, 0.15].forEach(mx => {
            const rail = new THREE.Mesh(new THREE.BoxGeometry(0.048, 1.06, 0.055), mats.blackSteel);
            rail.position.set(mx, 0.58, -0.32); rail.castShadow = true; dir.add(rail);
            const fork = new THREE.Mesh(new THREE.BoxGeometry(0.055, 0.025, 0.42), mats.chrome);
            fork.position.set(mx, 0.1, -0.54); fork.castShadow = true; dir.add(fork);
        });
        const piston = new THREE.Mesh(new THREE.CylinderGeometry(0.026, 0.03, 0.96, 12), mats.chrome);
        piston.position.set(0, 0.54, -0.32); dir.add(piston);
    }

    // 3. KUDA: ELECTRIC RIDE-ON PALLET TRUCK + OPERATOR BERDIRI DI PLATFORM BELAKANG
    else if (type === 'knight') {
        //Unit Motor & Palet Kargo di Depan
        const body = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.42, 0.26), teamPrimary);
        body.position.set(0, 0.25, 0.08); body.castShadow = true; dir.add(body);

        const tiller = new THREE.Mesh(new THREE.CylinderGeometry(0.022, 0.025, 0.36, 10), mats.blackSteel);
        tiller.position.set(0, 0.58, 0.14); tiller.rotation.x = 0.35; dir.add(tiller);

        // Platform Pijakan & Operator Mengendalikan Reach Pallet
        const standPad = new THREE.Mesh(new THREE.BoxGeometry(0.38, 0.04, 0.24), mats.darkIron);
        standPad.position.set(0, 0.08, 0.32); dir.add(standPad);

        const rider = buildRealisticHuman(teamPrimary, vestMat, teamAccent, false, false);
        rider.root.scale.set(0.78, 0.78, 0.78);
        rider.root.position.set(0, 0.1, 0.32);
        attachArm(rider.upperBody, -1, 0.75, -0.1, 0.55, teamPrimary, mats.leather);
        attachArm(rider.upperBody, 1, 0.75, 0.1, 0.55, teamPrimary, mats.leather);
        dir.add(rider.root);

        // Palet & Kargo di Depan
        const pallet = makeEuroPallet(0.46, 0.44);
        pallet.position.set(0, 0.04, -0.24); dir.add(pallet);

        const b1 = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.24, 0.38), mats.cardboard);
        b1.position.set(0, 0.22, -0.24); b1.castShadow = true; dir.add(b1);
        const b2 = new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.2, 0.32), mats.cardboard);
        b2.position.set(0, 0.44, -0.24); b2.rotation.y = 0.12; b2.castShadow = true; dir.add(b2);
    }

    // 4. GAJAH: QC INSPECTOR (HELM PUTIH, CLIPBOARD & LASER BARCODE SCANNER)
    else if (type === 'bishop') {
        const { root: fig, upperBody } = buildRealisticHuman(teamPrimary, vestMat, mats.whiteHelmet, true, false);
        dir.add(fig);

        const leftArm = attachArm(upperBody, -1, 0.45, 0.1, 0.95, teamPrimary, mats.skin);
        const board = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.22, 0.015), mats.woodPallet);
        board.position.set(0.04, -0.18, -0.06); board.rotation.set(1.2, 0.2, -0.3);
        leftArm.eGroup.add(board);

        const rightArm = attachArm(upperBody, 1, 0.85, -0.05, 0.65, teamPrimary, mats.skin);
        const scanner = new THREE.Mesh(new THREE.BoxGeometry(0.045, 0.05, 0.13), mats.amberBeacon);
        scanner.position.set(0, -0.21, -0.07); rightArm.eGroup.add(scanner);

        const laser = new THREE.Mesh(
            new THREE.ConeGeometry(0.11, 0.38, 14),
            new THREE.MeshBasicMaterial({ color: 0xef4444, transparent: true, opacity: 0.42 })
        );
        laser.rotation.x = Math.PI / 2; laser.position.set(0, -0.21, -0.31);
        rightArm.eGroup.add(laser);
    }

    // 5. MENTERI (QUEEN): WAREHOUSE OPERATIONS SUPERVISOR
    else if (type === 'queen') {
        const { root: fig, upperBody } = buildRealisticHuman(teamPrimary, mats.darkIron, mats.goldHelmet, true, false);
        fig.scale.set(1.06, 1.06, 1.06);
        dir.add(fig);

        [-0.16, 0.16].forEach(ex => {
            const ep = new THREE.Mesh(new THREE.BoxGeometry(0.075, 0.02, 0.095), mats.goldHelmet);
            ep.position.set(ex, 0.34, 0); upperBody.add(ep);
        });

        const radio = new THREE.Mesh(new THREE.BoxGeometry(0.048, 0.095, 0.035), mats.blackSteel);
        radio.position.set(-0.11, 0.25, -0.13); upperBody.add(radio);

        attachArm(upperBody, -1, 0.55, -0.1, 1.1, teamPrimary, mats.skin);
        attachArm(upperBody, 1, 0.4, 0.15, 0.9, teamPrimary, mats.skin);

        const tablet = new THREE.Mesh(new THREE.BoxGeometry(0.25, 0.17, 0.022), mats.blackSteel);
        tablet.position.set(0, 0.18, -0.25); tablet.rotation.x = -0.55; upperBody.add(tablet);
        const screen = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.14, 0.025), new THREE.MeshStandardMaterial({
            color: 0x0284c7, emissive: 0x0ea5e9, emissiveIntensity: 0.7
        }));
        screen.position.copy(tablet.position); screen.rotation.copy(tablet.rotation); upperBody.add(screen);
    }

    // 6. RAJA (KING): MAIN WMS SERVER RACK + DUAL COMMAND MONITORS
    else if (type === 'king') {
        const cab = new THREE.Mesh(new THREE.BoxGeometry(0.54, 1.1, 0.52), mats.blackSteel);
        cab.position.set(0, 0.55, 0.04); cab.castShadow = true; dir.add(cab);

        [-0.27, 0.27].forEach(px => {
            const trim = new THREE.Mesh(new THREE.BoxGeometry(0.035, 1.12, 0.54), teamAccent);
            trim.position.set(px, 0.56, 0.04); dir.add(trim);
        });

        for (let i = 0; i < 7; i++) {
            const sy = 0.16 + i * 0.13;
            const led = new THREE.Mesh(new THREE.BoxGeometry(0.38, 0.022, 0.02), new THREE.MeshStandardMaterial({
                color: isBlue ? 0x38bdf8 : 0xfbbf24,
                emissive: isBlue ? 0x0284c7 : 0xd97706,
                emissiveIntensity: 1.1
            }));
            led.position.set(0, sy, -0.22); dir.add(led);
        }

        const door = new THREE.Mesh(new THREE.BoxGeometry(0.48, 1.04, 0.02), mats.serverGlass);
        door.position.set(0, 0.55, -0.24); dir.add(door);

        const core = new THREE.Mesh(new THREE.OctahedronGeometry(0.15, 1), new THREE.MeshStandardMaterial({
            color: isBlue ? 0x38bdf8 : 0xfbbf24,
            emissive: isBlue ? 0x0284c7 : 0xd97706,
            emissiveIntensity: 0.9, wireframe: true
        }));
        core.position.set(0, 1.32, 0.04); dir.add(core);
        animatedParts.push({ mesh: core, type: 'spin' });
    }

    return root;
}

// ============================================================================
// 6. CHESS RULES, TELEMETRY INSPECTOR & BATTLE LOG
// ============================================================================
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
    document.getElementById('st-pow-val').innerText = s.pow + '%';
    document.getElementById('st-pow').style.width = s.pow + '%';
    document.getElementById('st-rng-val').innerText = s.rng + '%';
    document.getElementById('st-rng').style.width = s.rng + '%';
}

function addBattleLog(text, isCombat = false) {
    const box = document.getElementById('move-history');
    const div = document.createElement('div');
    div.className = 'log-entry' + (isCombat ? ' combat' : '');
    div.innerText = text;
    box.prepend(div);
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
    for (let i = 0; i < 18; i++) {
        const p = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.14, 0.16), i % 2 === 0 ? mats.cardboard : mats.woodPallet);
        p.position.copy(pos); p.position.y += 0.4; scene.add(p);
        const vx = (Math.random()-0.5)*0.22, vz = (Math.random()-0.5)*0.22; let vy = Math.random()*0.22 + 0.06;
        const tick = () => {
            p.position.x += vx; p.position.y += vy; p.position.z += vz; vy -= 0.012;
            p.rotation.x += 0.16; p.rotation.y += 0.14; p.scale.multiplyScalar(0.94);
            if (p.scale.x > 0.03 && p.position.y > -0.2) requestAnimationFrame(tick); else scene.remove(p);
        };
        tick();
    }
}

function executeMove(piece, moveData) {
    isAnimating = true; clearHighlights();
    const sx = piece.position.x, sz = piece.position.z;
    const ex = moveData.x * tileSize - offset, ez = moveData.z * tileSize - offset;
    let prog = 0;
    const step = () => {
        prog += 0.065;
        if (prog < 1) {
            piece.position.x = sx + (ex - sx) * prog;
            piece.position.z = sz + (ez - sz) * prog;
            piece.position.y = 0.05 + Math.sin(prog * Math.PI) * 0.55;
            requestAnimationFrame(step);
        } else {
            piece.position.set(ex, 0.05, ez);
            piece.userData.gridX = moveData.x; piece.userData.gridZ = moveData.z; piece.userData.hasMoved = true;
            const uName = unitSpecs[piece.userData.type].name;
            const coord = `${cols[moveData.x]}${8 - moveData.z}`;
            let msg = `${uName} bergeser ke zona ${coord}.`;

            if (moveData.attack && moveData.target) {
                const v = moveData.target; v.userData.alive = false; scene.remove(v);
                triggerExplosion(piece.position);
                const vName = unitSpecs[v.userData.type].name;
                msg = `💥 ELIMINASI! ${uName} menyingkirkan ${vName} di ${coord}!`;
                addBattleLog(`${uName} ⚔️ ${vName} (${coord})`, true);
                updateScoreUI();
                if (v.userData.type === 'king') {
                    updateHUD(`🏆 OVERRIDE SELESAI! Tim ${currentTurn.toUpperCase()} menguasai Main WMS Server!`);
                    isAnimating = false; return;
                }
            } else {
                addBattleLog(`${uName} ➔ ${coord}`, false);
            }

            if (piece.userData.type === 'pawn' && (moveData.z === 0 || moveData.z === 7)) {
                const tm = piece.userData.team; scene.remove(piece);
                pieces = pieces.filter(p => p !== piece);
                spawnUnit('queen', tm, moveData.x, moveData.z);
                msg = `⭐ PROMOSI JABATAN! Operator diangkat menjadi Warehouse Ops Supervisor!`;
            }

            currentTurn = currentTurn === 'blue' ? 'orange' : 'blue';
            selectedPiece = null; validMoves = []; isAnimating = false;
            updateHUD(msg);

            if (vsAI && currentTurn === 'orange') setTimeout(runAIBot, 450);
        }
    };
    step();
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
    addBattleLog("Shift Operasional Dimulai. WMS Aktif.");
    updateHUD("Shift Baru Dimulai! Klik tombol '🔍 Inspeksi Unit' untuk melihat pengemudi di dalam Forklift.");
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
        camera.position.set(0, 18.5, 0.01);
        controls.target.set(0, 0, 0);
    } else if (mode === 'closeup') {
        camera.position.set(-2.6, 3.2, 7.2);
        controls.target.set(-1.2, 0.7, 3.6);
    } else {
        camera.position.set(0, 11.2, 14.2);
        controls.target.set(0, 0.5, 0);
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
        if (p.type === 'spin') { p.mesh.rotation.y = t * 1.8; p.mesh.rotation.x = t * 0.9; }
        else if (p.type === 'pulse') { p.mesh.material.emissiveIntensity = 0.8 + Math.sin(t * 9) * 0.5; }
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
