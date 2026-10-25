import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="WAREHOUSE COMMAND: AAA COMBAT EDITION",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding: 0 !important; margin: 0 !important; max-width: 100% !important;}
    .stApp {background-color: #04060a; overflow: hidden;}
    iframe {display: block; border: none; width: 100vw !important; height: 100vh !important;}
</style>
""", unsafe_allow_html=True)

HTML_CODE = r'''<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Warehouse Command: AAA Tactical Combat</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=Rajdhani:wght@600;700&display=swap" rel="stylesheet">
<style>
    * { box-sizing: border-box; user-select: none; }
    body { margin: 0; padding: 0; overflow: hidden; background: #04060a; font-family: 'Rajdhani', sans-serif; color: #f8fafc; }
    #canvas-container { width: 100vw; height: 100vh; display: block; }

    /* CINEMATIC LETTERBOX BARS (MUNCUL SAAT ADEGAN BERKELAHI EPIC) */
    .cine-bar {
        position: fixed; left: 0; right: 0; height: 0px; background: #000;
        z-index: 25; transition: height 0.35s cubic-bezier(0.16, 1, 0.3, 1); pointer-events: none;
    }
    #cine-top { top: 0; border-bottom: 1px solid rgba(245, 158, 11, 0.4); }
    #cine-bot { bottom: 0; border-top: 1px solid rgba(245, 158, 11, 0.4); }
    body.combat-mode #cine-top, body.combat-mode #cine-bot { height: 75px; }

    /* COMBAT BANNER POPUP */
    #combat-banner {
        position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%) scale(0.5);
        font-family: 'Orbitron', sans-serif; font-size: 42px; font-weight: 900;
        color: #fff; text-transform: uppercase; letter-spacing: 4px;
        text-shadow: 0 0 25px #ef4444, 0 0 50px #f59e0b;
        opacity: 0; pointer-events: none; z-index: 30;
        transition: all 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        white-space: nowrap;
    }
    #combat-banner.show { opacity: 1; transform: translate(-50%, -50%) scale(1); }

    /* TOP COMMAND BAR */
    #top-bar {
        position: absolute; top: 0; left: 0; right: 0; height: 64px;
        background: linear-gradient(180deg, rgba(6, 10, 18, 0.96) 0%, rgba(6, 10, 18, 0.75) 100%);
        border-bottom: 1px solid rgba(56, 189, 248, 0.25);
        display: flex; justify-content: space-between; align-items: center;
        padding: 0 22px; z-index: 10; backdrop-filter: blur(10px);
    }
    .brand-cluster { display: flex; align-items: center; gap: 12px; }
    .brand-emblem {
        width: 38px; height: 38px; border-radius: 6px;
        background: linear-gradient(135deg, #f59e0b, #ea580c);
        display: flex; align-items: center; justify-content: center;
        font-family: 'Orbitron', sans-serif; font-weight: 900; font-size: 18px; color: #05070b;
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
    .team-score.orange { color: #fbbf24; }
    .score-pill { background: #020617; padding: 2px 9px; border-radius: 10px; font-family: 'Orbitron', sans-serif; border: 1px solid currentColor; }
    #turn-banner { padding: 4px 14px; border-radius: 16px; font-family: 'Orbitron', sans-serif; font-size: 11px; font-weight: 800; }
    .turn-blue { background: rgba(2, 132, 199, 0.35); color: #38bdf8; border: 1px solid #38bdf8; }
    .turn-orange { background: rgba(217, 119, 6, 0.35); color: #fbbf24; border: 1px solid #fbbf24; }

    .toolbar { display: flex; gap: 6px; }
    .t-btn {
        background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(148, 163, 184, 0.3);
        color: #e2e8f0; padding: 7px 12px; border-radius: 5px; font-family: 'Rajdhani', sans-serif;
        font-weight: 700; font-size: 12px; text-transform: uppercase; cursor: pointer; transition: 0.2s;
    }
    .t-btn:hover { border-color: #38bdf8; color: #fff; background: rgba(56, 189, 248, 0.2); }
    .t-btn.active { background: #0284c7; border-color: #38bdf8; }

    /* LEFT PANEL */
    #unit-inspector {
        position: absolute; top: 80px; left: 18px; width: 265px;
        background: rgba(9, 14, 26, 0.92); border: 1px solid rgba(56, 189, 248, 0.3);
        border-left: 4px solid #38bdf8; border-radius: 8px; padding: 12px 15px; z-index: 10;
        backdrop-filter: blur(8px);
    }
    .panel-tag { font-family: 'Orbitron', sans-serif; font-size: 9px; color: #64748b; letter-spacing: 1.5px; }
    #insp-name { font-family: 'Orbitron', sans-serif; font-size: 14px; font-weight: 800; margin: 2px 0; color: #fff; }
    #insp-role { font-size: 12px; color: #f59e0b; font-weight: 700; margin-bottom: 8px; }
    #insp-weapon { font-size: 11.5px; color: #38bdf8; margin-bottom: 8px; font-weight: 600; }
    .roster-mini { margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.1); font-size: 11px; color: #cbd5e1; line-height: 1.55; }
    .badge-cls { display: inline-block; width: 62px; color: #fbbf24; font-weight: 700; }

    /* RIGHT LOG */
    #ops-panel {
        position: absolute; top: 80px; right: 18px; width: 255px;
        background: rgba(9, 14, 26, 0.92); border: 1px solid rgba(245, 158, 11, 0.3);
        border-right: 4px solid #f59e0b; border-radius: 8px; padding: 12px 15px; z-index: 10;
    }
    #move-history { max-height: 145px; overflow-y: auto; display: flex; flex-direction: column; gap: 4px; margin-top: 6px; }
    .log-entry { background: rgba(15, 23, 42, 0.85); padding: 4px 8px; border-radius: 4px; border-left: 2px solid #475569; font-size: 11px; }
    .log-entry.combat { border-left-color: #ef4444; background: rgba(127, 29, 29, 0.35); color: #fca5a5; font-weight: 700; }

    /* BOTTOM STATUS */
    #bottom-ticker {
        position: absolute; bottom: 16px; left: 50%; transform: translateX(-50%);
        background: rgba(6, 10, 18, 0.94); border: 1px solid rgba(56, 189, 248, 0.35);
        padding: 8px 24px; border-radius: 24px; display: flex; align-items: center; gap: 10px; z-index: 10; font-size: 13px; font-weight: 600;
    }
    .pulse-dot { width: 8px; height: 8px; border-radius: 50%; background: #22c55e; box-shadow: 0 0 10px #22c55e; }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>
    <div id="cine-top" class="cine-bar"></div>
    <div id="cine-bot" class="cine-bar"></div>
    <div id="combat-banner">⚔️ CRITICAL TAKEDOWN!</div>

    <div id="top-bar">
        <div class="brand-cluster">
            <div class="brand-emblem">WC</div>
            <div class="brand-title">
                <h1>WAREHOUSE COMMAND</h1>
                <span>Sculpted 3D Classes • Close-Quarters Combat Engine</span>
            </div>
        </div>

        <div class="versus-hud">
            <div class="team-score blue"><span>INBOUND</span><span id="score-blue" class="score-pill">16</span></div>
            <div id="turn-banner" class="turn-blue">SHIFT BIRU AKTIF</div>
            <div class="team-score orange"><span id="score-orange" class="score-pill">16</span><span>OUTBOUND</span></div>
        </div>

        <div class="toolbar">
            <button id="btn-ai" class="t-btn active" onclick="toggleAI()">🤖 vs AI Bot</button>
            <button class="t-btn" onclick="demoCombat()">🔥 Demo Aksi Berkelahi</button>
            <button class="t-btn" onclick="setCameraView('closeup')">🔍 Lihat Karakter</button>
            <button class="t-btn" onclick="setCameraView('perspective')">🎥 Kamera Taktis</button>
            <button class="t-btn" onclick="resetGame()">🔄 Reset</button>
        </div>
    </div>

    <div id="unit-inspector">
        <div class="panel-tag">UNIT CLASS SPECIFICATION</div>
        <h2 id="insp-name">HEAVY FORKLIFT</h2>
        <div id="insp-role">Armored Juggernaut • Benteng (Rook)</div>
        <div id="insp-weapon">⚡ Serangan: Hydraulic Fork Ram & Flip</div>
        <div class="roster-mini">
            <div><span class="badge-cls">PION</span> Striker (Exoskeleton + Kunci Besi)</div>
            <div><span class="badge-cls">BENTENG</span> Heavy Forklift (Seruduk Garpu)</div>
            <div><span class="badge-cls">KUDA</span> Speed Trike (Motor Kargo Taktis)</div>
            <div><span class="badge-cls">GAJAH</span> Cyber Sniper (Laser Rifle + Drone)</div>
            <div><span class="badge-cls">MENTERI</span> Ops Commander (Dual Baton Listrik)</div>
            <div><span class="badge-cls">RAJA</span> Mech-Core WMS (Menara Pertahanan)</div>
        </div>
    </div>

    <div id="ops-panel">
        <div class="panel-tag">COMBAT TELEMETRY LOG</div>
        <div id="move-history"></div>
    </div>

    <div id="bottom-ticker">
        <div class="pulse-dot"></div>
        <div id="action-log">Klik tombol "🔥 Demo Aksi Berkelahi" di kanan atas atau makan bidak lawan untuk melihat duel epik!</div>
    </div>

    <div id="canvas-container"></div>

<script>
// ============================================================================
// 1. ENGINE & DRAMATIC LIGHTING
// ============================================================================
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x04060b);
scene.fog = new THREE.FogExp2(0x04060b, 0.014);

const camera = new THREE.PerspectiveCamera(38, window.innerWidth / window.innerHeight, 0.1, 200);
camera.position.set(0, 11.0, 13.8);

const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 0.82;
renderer.outputEncoding = THREE.sRGBEncoding;
container.appendChild(renderer.domElement);

const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.06;
controls.maxPolarAngle = Math.PI / 2 - 0.03;
controls.minDistance = 2.8;
controls.maxDistance = 24;
controls.target.set(0, 0.6, 0);

scene.add(new THREE.HemisphereLight(0x93c5fd, 0x090d16, 0.55));
const keyLight = new THREE.DirectionalLight(0xfff1e0, 1.35);
keyLight.position.set(8, 18, 10);
keyLight.castShadow = true;
keyLight.shadow.mapSize.set(2048, 2048);
const d = 8.2;
Object.assign(keyLight.shadow.camera, { left: -d, right: d, top: d, bottom: -d, near: 2, far: 40 });
keyLight.shadow.bias = -0.0004;
scene.add(keyLight);

const rim1 = new THREE.PointLight(0x38bdf8, 1.2, 24); rim1.position.set(-9, 5, 8); scene.add(rim1);
const rim2 = new THREE.PointLight(0xf59e0b, 1.2, 24); rim2.position.set(9, 5, -8); scene.add(rim2);

// ============================================================================
// 2. BOARD & WAREHOUSE ARENA
// ============================================================================
function makeTileTex(isDark, lbl) {
    const c = document.createElement('canvas'); c.width = 256; c.height = 256;
    const ctx = c.getContext('2d');
    ctx.fillStyle = isDark ? '#0b111e' : '#162032'; ctx.fillRect(0,0,256,256);
    ctx.strokeStyle = isDark ? '#162032' : '#26354d'; ctx.lineWidth = 8; ctx.strokeRect(4,4,248,248);
    ctx.fillStyle = 'rgba(245, 158, 11, 0.35)';
    ctx.fillRect(14,14,16,3); ctx.fillRect(14,14,3,16);
    if (lbl) {
        ctx.fillStyle = 'rgba(148,163,184,0.5)';
        ctx.font = 'bold 28px Orbitron, monospace'; ctx.fillText(lbl, 18, 234);
    }
    return new THREE.CanvasTexture(c);
}

const boardGroup = new THREE.Group(); scene.add(boardGroup);
const floor = new THREE.Mesh(new THREE.PlaneGeometry(80, 80), new THREE.MeshStandardMaterial({ color: 0x05070c, roughness: 0.8 }));
floor.rotation.x = -Math.PI/2; floor.position.y = -0.35; floor.receiveShadow = true; scene.add(floor);

const base = new THREE.Mesh(new THREE.BoxGeometry(10.4, 0.35, 10.4), new THREE.MeshStandardMaterial({ color: 0x090e1a, roughness: 0.4, metalness: 0.5 }));
base.position.y = -0.2; base.receiveShadow = true; boardGroup.add(base);

const tileSize = 1.2, offset = 3.5 * tileSize, tiles = [], cols = ['A','B','C','D','E','F','G','H'];
for (let x = 0; x < 8; x++) {
    tiles[x] = [];
    for (let z = 0; z < 8; z++) {
        const isDark = (x + z) % 2 === 1;
        const lbl = (z === 7) ? cols[x] : (x === 0 ? String(8 - z) : '');
        const tile = new THREE.Mesh(
            new THREE.BoxGeometry(tileSize * 0.985, 0.1, tileSize * 0.985),
            new THREE.MeshStandardMaterial({ map: makeTileTex(isDark, lbl), roughness: 0.45 })
        );
        tile.position.set(x * tileSize - offset, 0, z * tileSize - offset);
        tile.receiveShadow = true; tile.userData = { gridX: x, gridZ: z };
        boardGroup.add(tile); tiles[x][z] = tile;
    }
}

// Rak Gudang Industri di Kiri & Kanan
function buildRack(xPos, zPos, rotY) {
    const r = new THREE.Group();
    const uMat = new THREE.MeshStandardMaterial({ color: 0x1d4ed8, roughness: 0.4 });
    const bMat = new THREE.MeshStandardMaterial({ color: 0xc2410c, roughness: 0.4 });
    const cMat = new THREE.MeshStandardMaterial({ color: 0x9a6b3e, roughness: 0.75 });
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
// 3. SCULPTED HUMAN FACE & ANATOMY ENGINE (BUKAN BOLA POLOS / BONEKA KAYU!)
// ============================================================================
function makeRealisticFaceTexture(skinHex, beardColor, hasScars) {
    const c = document.createElement('canvas'); c.width = 512; c.height = 512;
    const ctx = c.getContext('2d');

    // Gradasi Kulit Wajah Alami dengan Shading Pipi & Rahang
    const grad = ctx.createRadialGradient(256, 256, 40, 256, 256, 260);
    grad.addColorStop(0, skinHex);
    grad.addColorStop(1, '#8c583a');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 512, 512);

    // Bayangan Rongga Mata & Tepi Hidung
    ctx.fillStyle = 'rgba(60, 30, 15, 0.28)';
    ctx.beginPath(); ctx.ellipse(205, 225, 26, 16, 0, 0, Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.ellipse(307, 225, 26, 16, 0, 0, Math.PI*2); ctx.fill();
    ctx.fillRect(246, 225, 20, 55);

    // Mata Tajam Realistis (Sclera Putih, Iris Berwarna, Pupil Hitam, Eyeliner)
    [[205, 225], [307, 225]].forEach(([ex, ey]) => {
        ctx.fillStyle = '#f8fafc';
        ctx.beginPath(); ctx.ellipse(ex, ey, 18, 9, 0, 0, Math.PI*2); ctx.fill();
        ctx.fillStyle = '#2563eb';
        ctx.beginPath(); ctx.arc(ex, ey, 7, 0, Math.PI*2); ctx.fill();
        ctx.fillStyle = '#020617';
        ctx.beginPath(); ctx.arc(ex, ey, 3.5, 0, Math.PI*2); ctx.fill();
        ctx.fillStyle = '#ffffff';
        ctx.beginPath(); ctx.arc(ex - 2, ey - 2, 1.8, 0, Math.PI*2); ctx.fill();
        // Alis Tebal Miring Tegas
        ctx.fillStyle = '#1c1917';
        ctx.fillRect(ex - 22, ey - 19, 44, 6);
    });

    // Bibir & Rahang Tegas
    ctx.fillStyle = '#6e3b2b';
    ctx.fillRect(228, 308, 56, 6);
    ctx.fillStyle = 'rgba(0,0,0,0.22)';
    ctx.fillRect(236, 322, 40, 5);

    // Cambang / Janggut Tipis Maskulin (Stubble)
    if (beardColor) {
        ctx.fillStyle = beardColor;
        ctx.fillRect(175, 295, 162, 70);
        ctx.fillStyle = '#7c3f2c';
        ctx.fillRect(232, 306, 48, 7);
    }

    return new THREE.CanvasTexture(c);
}

// Fungsi Pahatan Vertex (Memahat Bola Menjadi Tengkorak & Rahang Manusia Asli)
function createSculptedHeadGeometry() {
    const geo = new THREE.SphereGeometry(0.115, 28, 24);
    const pos = geo.attributes.position;
    for (let i = 0; i < pos.count; i++) {
        let x = pos.getX(i), y = pos.getY(i), z = pos.getZ(i);
        // Pipihkan pelipis kiri-kanan seperti kepala manusia
        x *= 0.86;
        // Bentuk rahang bawah & dagu meruncing ke depan
        if (y < 0) {
            const jawFactor = 1.0 + (y / 0.115) * 0.35;
            x *= Math.max(0.55, jawFactor);
            if (z < -0.04) z -= 0.015; // Tonjolkan dagu
        }
        // Pahat tonjolan tulang hidung & alis secara organik (Bukan tempelan bola!)
        if (z < -0.07 && Math.abs(x) < 0.025 && y > -0.03 && y < 0.025) {
            z -= 0.024 * (1 - Math.abs(x) / 0.025);
        }
        pos.setXYZ(i, x, y, z);
    }
    geo.computeVertexNormals();
    return geo;
}

// Pahatan Torso Berotot (V-Taper Chest & Shoulders, Bukan Tabung Lurus!)
function createSculptedTorsoGeometry() {
    const geo = new THREE.CylinderGeometry(0.165, 0.115, 0.38, 24, 10);
    const pos = geo.attributes.position;
    for (let i = 0; i < pos.count; i++) {
        let x = pos.getX(i), y = pos.getY(i), z = pos.getZ(i);
        // Pipihkan kedalaman perut-punggung, lebarkan dada & bahu
        z *= 0.72;
        if (y > 0.02) {
            x *= 1.18; // Otot dada & bahu bidang
            if (z < 0) z *= 1.12; // Busungkan dada depan
        } else {
            x *= 0.92; // Pinggang atletis ramping
        }
        pos.setXYZ(i, x, y, z);
    }
    geo.computeVertexNormals();
    return geo;
}

const sculptedHeadGeo = createSculptedHeadGeometry();
const sculptedTorsoGeo = createSculptedTorsoGeometry();
const faceTexClean = makeRealisticFaceTexture('#dfb18b', null, false);
const faceTexBeard = makeRealisticFaceTexture('#d2996c', 'rgba(28, 25, 23, 0.38)', true);

const mats = {
    skin: new THREE.MeshStandardMaterial({ color: 0xd9a17c, roughness: 0.48 }),
    faceClean: new THREE.MeshStandardMaterial({ map: faceTexClean, roughness: 0.5 }),
    faceBeard: new THREE.MeshStandardMaterial({ map: faceTexBeard, roughness: 0.5 }),
    pantsDark: new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.8 }),
    boots: new THREE.MeshStandardMaterial({ color: 0x141210, roughness: 0.45, metalness: 0.2 }),
    blackSteel: new THREE.MeshStandardMaterial({ color: 0x0f172a, metalness: 0.75, roughness: 0.3 }),
    darkArmor: new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.65, roughness: 0.35 }),
    chrome: new THREE.MeshStandardMaterial({ color: 0xf1f5f9, metalness: 0.92, roughness: 0.12 }),
    rubber: new THREE.MeshStandardMaterial({ color: 0x090d16, roughness: 0.9 }),
    cardboard: new THREE.MeshStandardMaterial({ color: 0xb48352, roughness: 0.75 }),
    wood: new THREE.MeshStandardMaterial({ color: 0x855832, roughness: 0.85 }),
    gold: new THREE.MeshStandardMaterial({ color: 0xf59e0b, metalness: 0.8, roughness: 0.2 }),
    laserRed: new THREE.MeshStandardMaterial({ color: 0xef4444, emissive: 0xdc2626, emissiveIntensity: 2.0 }),
    plasmaBlue: new THREE.MeshStandardMaterial({ color: 0x38bdf8, emissive: 0x0284c7, emissiveIntensity: 2.0 }),
    plasmaAmber: new THREE.MeshStandardMaterial({ color: 0xfbbf24, emissive: 0xd97706, emissiveIntensity: 2.0 })
};

// ============================================================================
// 4. DISTINCT 6 UNIT CLASSES (SETIAP BIDAK SANGAT BERBEDA DARI JAUH & DEKAT!)
// ============================================================================
const animatedParts = [];
const humanRigs = [];

// Merakit Karakter Manusia dengan Sendi Artikulasi Penuh untuk Berkelahi
function buildRiggedFighter(teamMat, armorMat, helmetStyle, useBeard) {
    const root = new THREE.Group();

    // Kaki Kiri & Kanan Berotot + Sepatu Taktis + Pelindung Tulang Kering
    const leftLeg = new THREE.Group(); leftLeg.position.set(-0.095, 0.52, 0); root.add(leftLeg);
    const rightLeg = new THREE.Group(); rightLeg.position.set(0.095, 0.52, 0); root.add(rightLeg);

    [leftLeg, rightLeg].forEach(legGrp => {
        const thigh = new THREE.Mesh(new THREE.CylinderGeometry(0.066, 0.052, 0.25, 16), mats.pantsDark);
        thigh.position.y = -0.12; thigh.castShadow = true; legGrp.add(thigh);

        const kneeArmor = new THREE.Mesh(new THREE.BoxGeometry(0.075, 0.07, 0.09), mats.blackSteel);
        kneeArmor.position.set(0, -0.24, -0.02); legGrp.add(kneeArmor);

        const shin = new THREE.Mesh(new THREE.CylinderGeometry(0.054, 0.044, 0.23, 16), mats.pantsDark);
        shin.position.y = -0.36; shin.castShadow = true; legGrp.add(shin);

        const boot = new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.09, 0.19), mats.boots);
        boot.position.set(0, -0.48, -0.03); boot.castShadow = true; legGrp.add(boot);
    });

    // Pinggul & Sabuk Taktis Ber-Holster
    const pelvis = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.12, 0.11, 18), mats.pantsDark);
    pelvis.scale.set(1.15, 1, 0.78); pelvis.position.y = 0.54; root.add(pelvis);

    const belt = new THREE.Mesh(new THREE.BoxGeometry(0.31, 0.05, 0.21), mats.boots);
    belt.position.y = 0.58; root.add(belt);

    // Upper Body (Bisa Membungkuk, Memutar Bahu & Meninju saat Berkelahi)
    const upperBody = new THREE.Group();
    upperBody.position.set(0, 0.6, 0);
    root.add(upperBody);

    const torso = new THREE.Mesh(sculptedTorsoGeo, teamMat);
    torso.position.y = 0.19; torso.castShadow = true; upperBody.add(torso);

    // Chest Rig / Exoskeleton Vest
    const armorVest = new THREE.Mesh(new THREE.BoxGeometry(0.29, 0.26, 0.22), armorMat);
    armorVest.position.set(0, 0.21, 0); armorVest.castShadow = true; upperBody.add(armorVest);

    // Kerah Jaket Tinggi & Leher Berotot
    const neck = new THREE.Mesh(new THREE.CylinderGeometry(0.048, 0.056, 0.09, 16), mats.skin);
    neck.position.y = 0.41; upperBody.add(neck);

    // Kepala Hasil Pahatan Vertex + Tekstur Wajah Nyata
    const headGroup = new THREE.Group();
    headGroup.position.set(0, 0.51, 0);
    upperBody.add(headGroup);

    const headMesh = new THREE.Mesh(sculptedHeadGeo, useBeard ? mats.faceBeard : mats.faceClean);
    headMesh.rotation.y = -Math.PI / 2;
    headMesh.castShadow = true;
    headGroup.add(headMesh);

    // Daun Telinga
    [-0.1, 0.1].forEach(ex => {
        const ear = new THREE.Mesh(new THREE.SphereGeometry(0.022, 10, 10), mats.skin);
        ear.scale.set(0.45, 1.2, 0.75); ear.position.set(ex, 0, 0); headGroup.add(ear);
    });

    // Gaya Penutup Kepala yang Berbeda-beda sesuai Jabatan/Kelas!
    if (helmetStyle === 'hardhat') {
        // Pion: Helm Safety Gudang + Earmuff Pelindung Telinga
        const dome = new THREE.Mesh(new THREE.SphereGeometry(0.118, 20, 14, 0, Math.PI*2, 0, Math.PI*0.52), armorMat);
        dome.position.y = 0.03; headGroup.add(dome);
        const brim = new THREE.Mesh(new THREE.CylinderGeometry(0.122, 0.132, 0.015, 20), armorMat);
        brim.position.set(0, 0.03, -0.02); headGroup.add(brim);
        [-0.115, 0.115].forEach(mx => {
            const muff = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.03, 12), mats.blackSteel);
            muff.rotation.z = Math.PI/2; muff.position.set(mx, 0, 0); headGroup.add(muff);
        });
    } else if (helmetStyle === 'visor_sniper') {
        // Gajah (QC Sniper): Tactical Beret / Hood + Single Red Cyber Eye Scope
        const cap = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.112, 0.06, 20), mats.blackSteel);
        cap.position.set(0, 0.07, 0); cap.rotation.z = 0.12; headGroup.add(cap);
        const scope = new THREE.Mesh(new THREE.CylinderGeometry(0.026, 0.026, 0.06, 12), mats.laserRed);
        scope.rotation.x = Math.PI/2; scope.position.set(0.045, 0.015, -0.1); headGroup.add(scope);
    } else if (helmetStyle === 'commander_crown') {
        // Menteri (Supervisor): Executive Gold-Trimmed Visor Cap + Tactical Sunglasses + Headset
        const crown = new THREE.Mesh(new THREE.CylinderGeometry(0.118, 0.11, 0.075, 20), mats.blackSteel);
        crown.position.set(0, 0.075, 0); headGroup.add(crown);
        const goldBand = new THREE.Mesh(new THREE.CylinderGeometry(0.114, 0.114, 0.02, 20), mats.gold);
        goldBand.position.set(0, 0.045, 0); headGroup.add(goldBand);
        const shades = new THREE.Mesh(new THREE.BoxGeometry(0.17, 0.038, 0.05), mats.blackSteel);
        shades.position.set(0, 0.015, -0.09); headGroup.add(shades);
    }

    // Lengan Kiri & Kanan dengan Sendi Bahu + Siku untuk Animasi Meninju / Mengayun Senjata
    function makeArm(side) {
        const shoulderPivot = new THREE.Group();
        shoulderPivot.position.set(side * 0.21, 0.33, 0);
        upperBody.add(shoulderPivot);

        // Pelindung Bahu (Pauldron)
        const pauldron = new THREE.Mesh(new THREE.SphereGeometry(0.062, 14, 12, 0, Math.PI*2, 0, Math.PI*0.6), armorMat);
        pauldron.rotation.z = side * -0.4; shoulderPivot.add(pauldron);

        const bicep = new THREE.Mesh(new THREE.CylinderGeometry(0.048, 0.04, 0.19, 14), teamMat);
        bicep.position.y = -0.095; bicep.castShadow = true; shoulderPivot.add(bicep);

        const elbowPivot = new THREE.Group();
        elbowPivot.position.set(0, -0.19, 0);
        shoulderPivot.add(elbowPivot);

        const forearm = new THREE.Mesh(new THREE.CylinderGeometry(0.042, 0.034, 0.18, 14), mats.skin);
        forearm.position.y = -0.09; forearm.castShadow = true; elbowPivot.add(forearm);

        const fist = new THREE.Mesh(new THREE.BoxGeometry(0.055, 0.065, 0.065), mats.boots);
        fist.position.y = -0.19; elbowPivot.add(fist);

        return { shoulderPivot, elbowPivot, fist };
    }

    const leftArm = makeArm(-1);
    const rightArm = makeArm(1);

    const rig = { root, upperBody, headGroup, leftLeg, rightLeg, leftArm, rightArm, phase: Math.random() * 6.28 };
    humanRigs.push(rig);
    return rig;
}

// ============================================================================
// 5. UNIT FACTORY: 6 SILUET KELAS YANG SANGAT KONTRAS & MUDAH DIBEDAKAN
// ============================================================================
function createUnitMesh(type, team) {
    const containerGrp = new THREE.Group();
    const isBlue = team === 'blue';

    const teamMat = new THREE.MeshStandardMaterial({ color: isBlue ? 0x0284c7 : 0xea580c, roughness: 0.35, metalness: 0.25 });
    const armorMat = new THREE.MeshStandardMaterial({ color: isBlue ? 0x38bdf8 : 0xfbbf24, roughness: 0.25, metalness: 0.55 });
    const glowMat = isBlue ? mats.plasmaBlue : mats.plasmaAmber;

    // Pangkalan Ring Taktis
    const baseRing = new THREE.Mesh(new THREE.TorusGeometry(0.47, 0.02, 12, 32), glowMat);
    baseRing.rotation.x = Math.PI / 2; baseRing.position.y = 0.02;
    containerGrp.add(baseRing);

    const dir = new THREE.Group();
    dir.rotation.y = isBlue ? 0 : Math.PI;
    containerGrp.add(dir);

    // ------------------------------------------------------------------------
    // KELAS 1: PION -> "EXOSKELETON STRIKER" (Petarung Jarak Dekat dengan Kunci Pipa Besar & Perisai Kargo)
    // ------------------------------------------------------------------------
    if (type === 'pawn') {
        const rig = buildRiggedFighter(teamMat, armorMat, 'hardhat', false);
        dir.add(rig.root);

        // Tangan Kiri memegang Perisai Pintu Kontainer Baja (Riot Cargo Shield)
        rig.leftArm.shoulderPivot.rotation.set(0.6, 0.3, -0.2);
        rig.leftArm.elbowPivot.rotation.x = 0.9;
        const shield = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.42, 0.04), mats.darkArmor);
        shield.position.set(-0.04, -0.15, -0.08);
        const shieldStripe = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.06, 0.045), armorMat);
        shield.add(shieldStripe);
        rig.leftArm.elbowPivot.add(shield);

        // Tangan Kanan menggenggam Heavy Wrench / Crowbar Baja siap memukul
        rig.rightArm.shoulderPivot.rotation.set(0.4, -0.2, 0.25);
        rig.rightArm.elbowPivot.rotation.x = 1.1;
        const wrench = new THREE.Mesh(new THREE.CylinderGeometry(0.022, 0.02, 0.48, 12), mats.chrome);
        wrench.rotation.x = Math.PI / 2; wrench.position.set(0, -0.19, -0.16);
        const wrenchJaw = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.09, 0.08), mats.gold);
        wrenchJaw.position.set(0, 0, -0.22); wrench.add(wrenchJaw);
        rig.rightArm.elbowPivot.add(wrench);

        containerGrp.userData.rig = rig;
    }

    // ------------------------------------------------------------------------
    // KELAS 2: BENTENG -> "ARMORED BULLDOZER FORKLIFT" (Kendaraan Raksasa Lebar Tanpa Terlihat Seperti Orang!)
    // ------------------------------------------------------------------------
    else if (type === 'rook') {
        const vehicle = new THREE.Group();
        dir.add(vehicle);

        // 4 Roda Raksasa Off-Road Gudang
        [[-0.34, 0.17, -0.25], [0.34, 0.17, -0.25], [-0.32, 0.14, 0.28], [0.32, 0.14, 0.28]].forEach(([wx, wy, wz]) => {
            const tire = new THREE.Mesh(new THREE.CylinderGeometry(wy, wy, 0.13, 20), mats.rubber);
            tire.rotation.z = Math.PI/2; tire.position.set(wx, wy, wz); tire.castShadow = true; vehicle.add(tire);
            const hub = new THREE.Mesh(new THREE.CylinderGeometry(wy*0.55, wy*0.55, 0.14, 12), armorMat);
            hub.rotation.z = Math.PI/2; hub.position.set(wx, wy, wz); vehicle.add(hub);
        });

        // Bodi Lapis Baja Lebar & Kabin Tertutup
        const hull = new THREE.Mesh(new THREE.BoxGeometry(0.62, 0.34, 0.72), teamMat);
        hull.position.set(0, 0.32, 0.04); hull.castShadow = true; vehicle.add(hull);

        const engineBlock = new THREE.Mesh(new THREE.BoxGeometry(0.56, 0.38, 0.28), mats.blackSteel);
        engineBlock.position.set(0, 0.38, 0.28); vehicle.add(engineBlock);

        // Kabin Kaca Baja & Lampu Sirine Ganda
        const cage = new THREE.Mesh(new THREE.BoxGeometry(0.52, 0.42, 0.44), mats.darkArmor);
        cage.position.set(0, 0.68, 0.02); cage.castShadow = true; vehicle.add(cage);
        const windshield = new THREE.Mesh(new THREE.BoxGeometry(0.46, 0.26, 0.46), glowMat);
        windshield.position.set(0, 0.7, 0.02); vehicle.add(windshield);

        // Garpu Hidrolik Raksasa (Bisa Bergerak Mengangkat Lawan Saat Berkelahi!)
        const forkPivot = new THREE.Group();
        forkPivot.position.set(0, 0.15, -0.35);
        vehicle.add(forkPivot);

        [-0.19, 0.19].forEach(fx => {
            const mast = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.95, 0.07), mats.blackSteel);
            mast.position.set(fx, 0.42, 0); vehicle.add(mast);
            const blade = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.035, 0.48), mats.chrome);
            blade.position.set(fx, 0, -0.2); forkPivot.add(blade);
        });
        const ramPlate = new THREE.Mesh(new THREE.BoxGeometry(0.56, 0.26, 0.05), armorMat);
        ramPlate.position.set(0, 0.12, -0.02); forkPivot.add(ramPlate);

        containerGrp.userData.forkPivot = forkPivot;
        containerGrp.userData.vehicle = vehicle;
    }

    // ------------------------------------------------------------------------
    // KELAS 3: KUDA -> "HIGH-SPEED LOGISTICS TRIKE" (Motor Kargo Cepat Beroda 3 +Tombak Kejut)
    // ------------------------------------------------------------------------
    else if (type === 'knight') {
        const bike = new THREE.Group();
        dir.add(bike);

        // Roda Depan Tunggal Miring & 2 Roda Belakang
        const frontWheel = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.16, 0.09, 20), mats.rubber);
        frontWheel.rotation.z = Math.PI/2; frontWheel.position.set(0, 0.16, -0.36); bike.add(frontWheel);
        [-0.26, 0.26].forEach(bx => {
            const bw = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, 0.1, 18), mats.rubber);
            bw.rotation.z = Math.PI/2; bw.position.set(bx, 0.14, 0.26); bike.add(bw);
        });

        // Sasis Aerodinamis Motor Trike & Fairing Depan
        const frame = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.24, 0.65), teamMat);
        frame.position.set(0, 0.26, 0); bike.add(frame);
        const noseCone = new THREE.Mesh(new THREE.ConeGeometry(0.2, 0.4, 8), armorMat);
        noseCone.rotation.x = -Math.PI/2; noseCone.position.set(0, 0.34, -0.32); bike.add(noseCone);

        // Pengendara Membungkuk Balap + Tombak Listrik (Shock Lance)
        const rider = buildRiggedFighter(teamMat, armorMat, 'visor_sniper', false);
        rider.root.scale.set(0.82, 0.82, 0.82);
        rider.root.position.set(0, 0.14, 0.08);
        rider.upperBody.rotation.x = 0.45;
        rider.rightArm.shoulderPivot.rotation.x = 1.25;

        // Tombak Kavaleri Gudang (Shock Lance Panjang)
        const lance = new THREE.Mesh(new THREE.ConeGeometry(0.05, 0.85, 10), mats.chrome);
        lance.rotation.x = -Math.PI/2; lance.position.set(0, -0.15, -0.35);
        const lanceTip = new THREE.Mesh(new THREE.ConeGeometry(0.06, 0.25, 10), glowMat);
        lanceTip.position.y = 0.35; lance.add(lanceTip);
        rider.rightArm.elbowPivot.add(lance);

        bike.add(rider.root);
        containerGrp.userData.rig = rider;
    }

    // ------------------------------------------------------------------------
    // KELAS 4: GAJAH -> "CYBER QC SNIPER + FLOATING DRONE" (Penembak Jitu Laser Jarak Jauh)
    // ------------------------------------------------------------------------
    else if (type === 'bishop') {
        const rig = buildRiggedFighter(teamMat, mats.blackSteel, 'visor_sniper', true);
        dir.add(rig.root);

        // Jubah Taktis Belakang (Cape)
        const cape = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.55, 0.03), mats.darkArmor);
        cape.position.set(0, 0.06, 0.13); cape.rotation.x = 0.18;
        rig.upperBody.add(cape);

        // Memegang Long-Range Barcode Laser Rifle Dua Tangan
        rig.rightArm.shoulderPivot.rotation.set(1.1, -0.15, 0);
        rig.rightArm.elbowPivot.rotation.x = 0.4;
        rig.leftArm.shoulderPivot.rotation.set(1.0, 0.35, 0);
        rig.leftArm.elbowPivot.rotation.x = 0.6;

        const rifle = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.1, 0.68), mats.blackSteel);
        rifle.position.set(0, -0.16, -0.22);
        const barrel = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.018, 0.4, 10), mats.chrome);
        barrel.rotation.x = Math.PI/2; barrel.position.set(0, 0.02, -0.38); rifle.add(barrel);
        const coreGlow = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.04, 0.25), mats.laserRed);
        coreGlow.position.set(0, 0.03, -0.1); rifle.add(coreGlow);
        rig.rightArm.elbowPivot.add(rifle);

        // Drone Scanner Melayang di Atas Bahu
        const drone = new THREE.Group();
        drone.position.set(0.32, 1.25, 0);
        const dBody = new THREE.Mesh(new THREE.SphereGeometry(0.09, 14, 14), armorMat);
        const dEye = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.08, 12), mats.laserRed);
        dEye.rotation.x = Math.PI/2; dEye.position.z = -0.07;
        drone.add(dBody, dEye);
        dir.add(drone);
        animatedParts.push({ mesh: drone, type: 'hover', baseY: 1.25 });

        containerGrp.userData.rig = rig;
    }

    // ------------------------------------------------------------------------
    // KELAS 5: MENTERI (QUEEN) -> "SUPREME OPS COMMANDER" (Postur Tinggi, Bahu Emas, Dual Plasma Batons!)
    // ------------------------------------------------------------------------
    else if (type === 'queen') {
        const rig = buildRiggedFighter(teamMat, mats.gold, 'commander_crown', true);
        rig.root.scale.set(1.12, 1.12, 1.12); // Lebih tinggi & gagah
        dir.add(rig.root);

        // Sayap Komando / Antena Taktis di Punggung
        [-0.16, 0.16].forEach(wx => {
            const wing = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.45, 0.14), mats.gold);
            wing.position.set(wx, 0.32, 0.12); wing.rotation.z = wx * -0.5;
            rig.upperBody.add(wing);
        });

        // Dual-Wielding Electro-Plasma Batons di Kedua Tangan!
        [rig.leftArm, rig.rightArm].forEach((arm, idx) => {
            arm.shoulderPivot.rotation.set(0.55, 0, idx === 0 ? -0.35 : 0.35);
            arm.elbowPivot.rotation.x = 0.95;
            const batonHilt = new THREE.Mesh(new THREE.CylinderGeometry(0.022, 0.022, 0.16, 10), mats.blackSteel);
            batonHilt.rotation.x = Math.PI/2; batonHilt.position.set(0, -0.19, -0.08);
            const batonBlade = new THREE.Mesh(new THREE.CylinderGeometry(0.026, 0.015, 0.38, 12), glowMat);
            batonBlade.position.y = -0.22; batonHilt.add(batonBlade);
            arm.elbowPivot.add(batonHilt);
        });

        containerGrp.userData.rig = rig;
    }

    // ------------------------------------------------------------------------
    // KELAS 6: RAJA (KING) -> "MECH-CORE WMS CITADEL" (Menara Server + Perisai Energi Berputar)
    // ------------------------------------------------------------------------
    else if (type === 'king') {
        const citadel = new THREE.Group();
        dir.add(citadel);

        const basePed = new THREE.Mesh(new THREE.CylinderGeometry(0.38, 0.44, 0.18, 8), mats.blackSteel);
        basePed.position.y = 0.09; citadel.add(basePed);

        const tower = new THREE.Mesh(new THREE.BoxGeometry(0.46, 0.95, 0.46), mats.darkArmor);
        tower.position.y = 0.62; tower.castShadow = true; citadel.add(tower);

        // 4 Pilar Pelindung Emas
        [[-0.24,-0.24],[0.24,-0.24],[-0.24,0.24],[0.24,0.24]].forEach(([px,pz]) => {
            const col = new THREE.Mesh(new THREE.BoxGeometry(0.06, 1.02, 0.06), mats.gold);
            col.position.set(px, 0.64, pz); citadel.add(col);
        });

        // Inti Reaktor WMS Menyala
        const reactor = new THREE.Mesh(new THREE.OctahedronGeometry(0.22, 1), glowMat);
        reactor.position.y = 1.35; citadel.add(reactor);

        const shieldRing = new THREE.Mesh(new THREE.TorusGeometry(0.34, 0.02, 10, 28), mats.gold);
        shieldRing.position.y = 1.35; citadel.add(shieldRing);

        animatedParts.push({ mesh: reactor, type: 'spin' });
        animatedParts.push({ mesh: shieldRing, type: 'orbit' });
    }

    return containerGrp;
}

// ============================================================================
// 6. EPIC CLOSE-QUARTERS COMBAT CHOREOGRAPHY ENGINE (DUEL SINEMATIK!)
// ============================================================================
let pieces = [], selectedPiece = null, validMoves = [], currentTurn = 'blue', isAnimating = false, vsAI = true, highlights = [];

const unitSpecs = {
    pawn:   { name: 'EXOSKELETON STRIKER', role: 'Frontline Brawler • Pion', wpn: '⚡ Heavy Wrench Combo & Shield Bash' },
    rook:   { name: 'ARMORED FORKLIFT', role: 'Heavy Juggernaut • Benteng', wpn: '⚡ Hydraulic Fork Lift & Slam' },
    knight: { name: 'SPEED LOGISTICS TRIKE', role: 'Cavalry Raider • Kuda', wpn: '⚡ High-Speed Shock Lance Charge' },
    bishop: { name: 'CYBER QC SNIPER', role: 'Long-Range Assassin • Gajah', wpn: '⚡ Overcharged Red Laser Barrage' },
    queen:  { name: 'SUPREME OPS COMMANDER', role: 'Elite Dual-Wielder • Menteri', wpn: '⚡ Twin Plasma Baton Whirlwind' },
    king:   { name: 'MECH-CORE WMS CITADEL', role: 'Central Command Hub • Raja', wpn: '⚡ EMP Orbital Discharge' }
};
const weights = { pawn: 10, knight: 30, bishop: 30, rook: 50, queen: 90, king: 900 };

function showCombatBanner(text) {
    const b = document.getElementById('combat-banner');
    b.innerText = text;
    b.classList.add('show');
    setTimeout(() => b.classList.remove('show'), 1100);
}

// Efek Ledakan Percikan Api, Gelombang Kejut & Serpihan Armor
function spawnImpactFX(pos, colorHex = 0xf59e0b) {
    // 1. Gelombang Kejut Melingkar (Shockwave Ring)
    const ringGeo = new THREE.RingGeometry(0.1, 0.22, 28);
    const ringMat = new THREE.MeshBasicMaterial({ color: colorHex, side: THREE.DoubleSide, transparent: true, opacity: 0.9 });
    const ring = new THREE.Mesh(ringGeo, ringMat);
    ring.rotation.x = -Math.PI / 2;
    ring.position.set(pos.x, 0.08, pos.z);
    scene.add(ring);

    let rScale = 1;
    const expandRing = () => {
        rScale += 0.35;
        ring.scale.set(rScale, rScale, rScale);
        ringMat.opacity -= 0.06;
        if (ringMat.opacity > 0) requestAnimationFrame(expandRing);
        else scene.remove(ring);
    };
    expandRing();

    // 2. Semburan Partikel Percikan Api & Serpihan Baja
    for (let i = 0; i < 26; i++) {
        const p = new THREE.Mesh(
            new THREE.BoxGeometry(0.12, 0.12, 0.12),
            i % 2 === 0 ? mats.plasmaAmber : mats.cardboard
        );
        p.position.set(pos.x, pos.y + 0.55, pos.z);
        scene.add(p);
        const vx = (Math.random() - 0.5) * 0.32;
        const vz = (Math.random() - 0.5) * 0.32;
        let vy = Math.random() * 0.28 + 0.08;
        const tick = () => {
            p.position.x += vx; p.position.y += vy; p.position.z += vz;
            vy -= 0.015;
            p.rotation.x += 0.25; p.rotation.y += 0.25;
            p.scale.multiplyScalar(0.92);
            if (p.scale.x > 0.02 && p.position.y > -0.3) requestAnimationFrame(tick);
            else scene.remove(p);
        };
        tick();
    }
}

// SKENARIO PERTARUNGAN EPIK (CLOSE-UP CAMERA + KOREOGRAFI PUKULAN + RAGDOLL KNOCKBACK)
function playEpicCombatSequence(attacker, defender, targetX, targetZ, onComplete) {
    document.body.classList.add('combat-mode');

    const startX = attacker.position.x, startZ = attacker.position.z;
    const endX = targetX * tileSize - offset, endZ = targetZ * tileSize - offset;

    // Arah vektor serangan
    const dx = endX - startX, dz = endZ - startZ;
    const dist = Math.hypot(dx, dz) || 1;
    const dirX = dx / dist, dirZ = dz / dist;

    // Posisi berhenti tepat di depan wajah musuh untuk berduel
    const duelX = endX - dirX * 0.65;
    const duelZ = endZ - dirZ * 0.65;

    // Putar kedua unit agar saling bertatapan mata!
    const angleToDef = Math.atan2(dx, dz);
    attacker.children[1].rotation.y = angleToDef + Math.PI;
    defender.children[1].rotation.y = angleToDef;

    // Pindahkan Kamera ke Sudut Sinematik Samping Duel (Action Cam)
    const camSideX = endX + dirZ * 2.6 - dirX * 1.2;
    const camSideZ = endZ - dirX * 2.6 - dirZ * 1.2;
    camera.position.set(camSideX, 2.1, camSideZ);
    controls.target.set((duelX + endX) * 0.5, 0.7, (duelZ + endZ) * 0.5);
    controls.update();

    // TAHAP 1: PENYERANG BERLARI MENERJANG KE DEPAN MUSUH
    let p1 = 0;
    const phase1Dash = () => {
        p1 += 0.08;
        if (p1 < 1) {
            attacker.position.x = startX + (duelX - startX) * p1;
            attacker.position.z = startZ + (duelZ - startZ) * p1;
            attacker.position.y = 0.05 + Math.sin(p1 * Math.PI) * 0.35;
            requestAnimationFrame(phase1Dash);
        } else {
            attacker.position.set(duelX, 0.05, duelZ);
            phase2Strike();
        }
    };

    // TAHAP 2: KOREOGRAFI BERKELAHI (PUKULAN KOMBO / TEMBAKAN LASER / ANGKATAN FORKLIFT)
    let p2 = 0;
    const atkRig = attacker.userData.rig;
    const defRig = defender.userData.rig;
    const forkPivot = attacker.userData.forkPivot;

    // Jika Gajah (Sniper), tembakkan sinar laser merah tebal ke dada musuh
    let laserBeam = null;
    if (attacker.userData.type === 'bishop') {
        laserBeam = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 1.2, 12), mats.laserRed);
        laserBeam.rotation.x = Math.PI / 2;
        laserBeam.position.set((duelX + endX)*0.5, 0.75, (duelZ + endZ)*0.5);
        laserBeam.lookAt(endX, 0.75, endZ);
        scene.add(laserBeam);
    }

    const phase2Strike = () => {
        p2 += 0.05;
        // Kamera berputar dramatis mengelilingi pertarungan
        camera.position.x += dirX * 0.02;
        controls.update();

        // Gerakan Mengayun Senjata / Meninju Beruntun
        if (atkRig) {
            atkRig.upperBody.rotation.y = Math.sin(p2 * 22) * 0.65;
            atkRig.upperBody.rotation.x = 0.25;
            atkRig.rightArm.shoulderPivot.rotation.x = 1.5 + Math.sin(p2 * 25) * 1.2;
            atkRig.leftArm.shoulderPivot.rotation.x = 1.2 - Math.sin(p2 * 25) * 1.0;
        }
        // Jika Benteng (Forklift), angkat garpu hidrolik dan lambungkan lawan ke atas!
        if (forkPivot) {
            forkPivot.position.y = 0.15 + Math.min(0.65, p2 * 0.8);
            defender.position.y = 0.05 + Math.min(0.75, p2 * 0.9);
            defender.rotation.x = p2 * 0.6;
        }
        // Lawan terguncang menerima serangan (Hit-Stun)
        if (defRig) {
            defRig.upperBody.rotation.x = -0.35 * Math.abs(Math.sin(p2 * 18));
        }
        if (Math.abs(p2 - 0.5) < 0.03) {
            spawnImpactFX(defender.position, 0x38bdf8);
        }

        if (p2 < 1.0) {
            requestAnimationFrame(phase2Strike);
        } else {
            if (laserBeam) scene.remove(laserBeam);
            if (atkRig) { atkRig.upperBody.rotation.set(0,0,0); }
            if (forkPivot) forkPivot.position.y = 0.15;

            // Puncak Pukulan Pamungkas (FINISHER HIT!)
            showCombatBanner("💥 CRITICAL TAKEDOWN!");
            spawnImpactFX(defender.position, 0xef4444);
            phase3Knockback();
        }
    };

    // TAHAP 3: MUSUH TERPENTAL RAGDOLL KE UDARA & PENYERANG MENDUDUKI PETAK
    let p3 = 0;
    const phase3Knockback = () => {
        p3 += 0.06;
        // Screen Shake pada kamera di awal ledakan
        if (p3 < 0.35) {
            camera.position.y = 2.1 + (Math.random() - 0.5) * 0.25;
        }

        // Musuh terpental jauh ke belakang sambil berputar (Ragdoll Physics)
        defender.position.x = endX + dirX * (p3 * 2.8);
        defender.position.z = endZ + dirZ * (p3 * 2.8);
        defender.position.y = 0.2 + Math.sin(p3 * Math.PI) * 1.6;
        defender.rotation.x += 0.22;
        defender.rotation.z += 0.18;
        defender.scale.multiplyScalar(0.95);

        // Penyerang maju dengan gagah ke petak tujuan
        attacker.position.x = duelX + (endX - duelX) * Math.min(1, p3 * 1.5);
        attacker.position.z = duelZ + (endZ - duelZ) * Math.min(1, p3 * 1.5);

        if (p3 < 1.0) {
            requestAnimationFrame(phase3Knockback);
        } else {
            defender.userData.alive = false;
            scene.remove(defender);
            attacker.position.set(endX, 0.05, endZ);
            attacker.children[1].rotation.y = attacker.userData.team === 'blue' ? 0 : Math.PI;

            setTimeout(() => {
                document.body.classList.remove('combat-mode');
                camera.position.set(0, 11.0, 13.8);
                controls.target.set(0, 0.6, 0);
                controls.update();
                onComplete();
            }, 320);
        }
    };

    phase1Dash();
}

// ============================================================================
// 7. CHESS LOGIC, AI & DEMO COMBAT TRIGGER
// ============================================================================
function inspectUnitUI(type) {
    const s = unitSpecs[type];
    if (!s) return;
    document.getElementById('insp-name').innerText = s.name;
    document.getElementById('insp-role').innerText = s.role;
    document.getElementById('insp-weapon').innerText = s.wpn;
}

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
            new THREE.MeshBasicMaterial({ color: m.attack ? 0xef4444 : 0x22c55e, transparent: true, opacity: 0.48, side: THREE.DoubleSide })
        );
        mk.rotation.x = -Math.PI/2; mk.position.set(m.x * tileSize - offset, 0.065, m.z * tileSize - offset);
        scene.add(mk); highlights.push(mk);
    });
}

function executeMove(piece, moveData) {
    isAnimating = true; clearHighlights();
    const uName = unitSpecs[piece.userData.type].name;
    const coord = `${cols[moveData.x]}${8 - moveData.z}`;

    // JIKA MENYERANG MUSUH -> JALANKAN KOREOGRAFI BERKELAHI EPIK!
    if (moveData.attack && moveData.target) {
        const victim = moveData.target;
        const vName = unitSpecs[victim.userData.type].name;
        updateHUD(`⚔️ DUEL BERLANGSUNG: ${uName} menyerang ${vName}!`);

        playEpicCombatSequence(piece, victim, moveData.x, moveData.z, () => {
            piece.userData.gridX = moveData.x;
            piece.userData.gridZ = moveData.z;
            piece.userData.hasMoved = true;

            addBattleLog(`${uName} 💥 KO ${vName} (${coord})`, true);
            updateScoreUI();

            if (victim.userData.type === 'king') {
                updateHUD(`🏆 VICTORY! Tim ${currentTurn.toUpperCase()} menghancurkan Mech-Core WMS lawan!`);
                isAnimating = false; return;
            }

            currentTurn = currentTurn === 'blue' ? 'orange' : 'blue';
            selectedPiece = null; validMoves = []; isAnimating = false;
            updateHUD(`💥 ${uName} memenangkan duel di zona ${coord}!`);
            if (vsAI && currentTurn === 'orange') setTimeout(runAIBot, 450);
        });
        return;
    }

    // LANGKAH BIASA (BERJALAN TAKTIS)
    const sx = piece.position.x, sz = piece.position.z;
    const ex = moveData.x * tileSize - offset, ez = moveData.z * tileSize - offset;
    let prog = 0;
    const step = () => {
        prog += 0.075;
        if (prog < 1) {
            piece.position.x = sx + (ex - sx) * prog;
            piece.position.z = sz + (ez - sz) * prog;
            piece.position.y = 0.05 + Math.sin(prog * Math.PI) * 0.35;
            requestAnimationFrame(step);
        } else {
            piece.position.set(ex, 0.05, ez);
            piece.userData.gridX = moveData.x; piece.userData.gridZ = moveData.z; piece.userData.hasMoved = true;
            addBattleLog(`${uName} ➔ ${coord}`, false);
            currentTurn = currentTurn === 'blue' ? 'orange' : 'blue';
            selectedPiece = null; validMoves = []; isAnimating = false;
            updateHUD(`${uName} mengamankan posisi ${coord}.`);
            if (vsAI && currentTurn === 'orange') setTimeout(runAIBot, 450);
        }
    };
    step();
}

// Tombol Instan untuk Mendemonstrasikan Aksi Berkelahi Epik tanpa menunggu langkah panjang!
function demoCombat() {
    if (isAnimating) return;
    const blueAttackers = pieces.filter(p => p.userData.alive && p.userData.team === 'blue' && p.userData.type !== 'king');
    const orangeTargets = pieces.filter(p => p.userData.alive && p.userData.team === 'orange' && p.userData.type !== 'king');
    if (blueAttackers.length === 0 || orangeTargets.length === 0) return;

    const atk = blueAttackers[Math.floor(Math.random() * blueAttackers.length)];
    const def = orangeTargets[Math.floor(Math.random() * orangeTargets.length)];
    currentTurn = 'blue';
    executeMove(atk, { x: def.userData.gridX, z: def.userData.gridZ, attack: true, target: def });
}

function runAIBot() {
    const aiPieces = pieces.filter(p => p.userData.alive && p.userData.team === 'orange');
    let allMoves = [];
    aiPieces.forEach(p => {
        getValidMoves(p).forEach(m => {
            let score = m.attack && m.target ? weights[m.target.userData.type] * 2 : (m.z * 0.5 + Math.random() * 2);
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
    m.userData = Object.assign(m.userData || {}, { type, team, gridX: gx, gridZ: gz, alive: true, hasMoved: false });
    scene.add(m); pieces.push(m);
}

function resetGame() {
    clearHighlights(); pieces.forEach(p => scene.remove(p)); pieces = [];
    humanRigs.length = 0; animatedParts.length = 0;
    document.getElementById('move-history').innerHTML = '';
    selectedPiece = null; validMoves = []; currentTurn = 'blue'; isAnimating = false;
    const row = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook'];
    for (let i = 0; i < 8; i++) {
        spawnUnit(row[i], 'orange', i, 0); spawnUnit('pawn', 'orange', i, 1);
        spawnUnit('pawn', 'blue', i, 6); spawnUnit(row[i], 'blue', i, 7);
    }
    updateScoreUI();
    addBattleLog("Shift Tempur Dimulai. Semua Kelas Siap.");
    updateHUD("Klik tombol '🔥 Demo Aksi Berkelahi' di atas untuk langsung melihat koreografi pertarungan!");
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
        camera.position.set(-1.8, 2.4, 6.2); controls.target.set(-0.6, 0.65, 3.6);
    } else {
        camera.position.set(0, 11.0, 13.8); controls.target.set(0, 0.6, 0);
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
        updateHUD(`Unit Siap: ${unitSpecs[unit.userData.type].name} (${cols[coords.x]}${8 - coords.z})`);
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
        if (p.type === 'spin') { p.mesh.rotation.y = t * 2.2; p.mesh.rotation.x = t * 1.1; }
        else if (p.type === 'orbit') { p.mesh.rotation.x = Math.sin(t * 2) * 0.8; p.mesh.rotation.y = t * 3; }
        else if (p.type === 'hover') { p.mesh.position.y = p.baseY + Math.sin(t * 3.5) * 0.08; }
    });

    if (!isAnimating) {
        humanRigs.forEach(r => {
            r.upperBody.position.y = 0.6 + Math.sin(t * 2.8 + r.phase) * 0.009;
            r.headGroup.rotation.y = Math.sin(t * 1.3 + r.phase) * 0.08;
        });
    }

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
