import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Warehouse Logistics Chess 3D - Realistic Edition",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding: 0 !important; margin: 0 !important; max-width: 100% !important;}
    .stApp {background-color: #070b12; overflow: hidden;}
    iframe {display: block; border: none; width: 100vw !important; height: 100vh !important;}
</style>
""", unsafe_allow_html=True)

HTML_CODE = r'''<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Warehouse Logistics Chess 3D - Realistic</title>
<style>
    * { box-sizing: border-box; user-select: none; }
    body { margin: 0; padding: 0; overflow: hidden; background: #070b12; font-family: 'Segoe UI', system-ui, sans-serif; color: #f8fafc; }
    #canvas-container { width: 100vw; height: 100vh; display: block; }
    #hud-top { position: absolute; top: 16px; left: 20px; right: 20px; display: flex; justify-content: space-between; align-items: flex-start; pointer-events: none; z-index: 10; flex-wrap: wrap; gap: 10px; }
    .brand-box { background: rgba(15, 23, 42, 0.88); border-left: 5px solid #f59e0b; padding: 10px 18px; border-radius: 8px; box-shadow: 0 10px 25px rgba(0,0,0,0.65); backdrop-filter: blur(8px); border-top: 1px solid rgba(255,255,255,0.1); }
    .brand-box h1 { margin: 0; font-size: 18px; font-weight: 800; letter-spacing: 1px; text-transform: uppercase; color: #f59e0b; }
    .brand-box p { margin: 3px 0 0 0; font-size: 12px; color: #94a3b8; }
    .controls-box { pointer-events: auto; display: flex; gap: 8px; flex-wrap: wrap; }
    .btn { background: rgba(30, 41, 59, 0.92); border: 1px solid #475569; color: #e2e8f0; padding: 8px 14px; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 12px; transition: 0.2s; }
    .btn:hover { background: #334155; border-color: #38bdf8; color: #fff; }
    .btn.active { background: #0284c7; border-color: #38bdf8; color: #fff; }
    #legend-panel { position: absolute; top: 92px; left: 20px; background: rgba(15, 23, 42, 0.82); border: 1px solid rgba(255,255,255,0.08); padding: 10px 14px; border-radius: 8px; font-size: 11px; color: #cbd5e1; pointer-events: none; line-height: 1.65; backdrop-filter: blur(6px); }
    .key-role { color: #f59e0b; font-weight: bold; }
    #hud-bottom { position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); background: rgba(15, 23, 42, 0.92); border: 1px solid rgba(255,255,255,0.14); padding: 12px 24px; border-radius: 10px; box-shadow: 0 12px 30px rgba(0,0,0,0.75); display: flex; align-items: center; gap: 16px; z-index: 10; white-space: nowrap; backdrop-filter: blur(10px); }
    .shift-badge { padding: 5px 12px; border-radius: 6px; font-weight: 800; font-size: 12px; text-transform: uppercase; }
    .shift-blue { background: rgba(2, 132, 199, 0.25); color: #38bdf8; border: 1px solid #0284c7; }
    .shift-orange { background: rgba(217, 119, 6, 0.25); color: #fbbf24; border: 1px solid #d97706; }
    #action-log { font-size: 13px; color: #e2e8f0; }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/environments/RoomEnvironment.js"></script>
</head>
<body>
    <div id="hud-top">
        <div class="brand-box">
            <h1>Warehouse Tactical Chess 3D</h1>
            <p>Realistic Anatomy & CAD Machinery • Blender HDRI Studio</p>
        </div>
        <div class="controls-box">
            <button id="btn-ai" class="btn active" onclick="toggleAI()">🤖 Mode: vs AI Bot</button>
            <button class="btn" onclick="setCameraView('closeup')">🔍 Zoom Karakter</button>
            <button class="btn" onclick="setCameraView('perspective')">🎥 Kamera 3D</button>
            <button class="btn" onclick="setCameraView('top')">📐 Denah Atas</button>
            <button class="btn" onclick="resetGame()">🔄 Reset Shift</button>
        </div>
    </div>

    <div id="legend-panel">
        <div><span class="key-role">Pion:</span> Operator Picker (Anatomi Manusia + Kardus)</div>
        <div><span class="key-role">Benteng:</span> Counterbalance Forklift (Kabin + Kemudi + Rantai)</div>
        <div><span class="key-role">Kuda:</span> Electric Pallet Truck (Palet Kayu + Stretch Wrap)</div>
        <div><span class="key-role">Gajah:</span> QC Inspector (Clipboard + Laser Barcode Scanner)</div>
        <div><span class="key-role">Menteri:</span> Warehouse Ops Supervisor (HT + Tablet + Safety Goggles)</div>
        <div><span class="key-role">Raja:</span> Main WMS Server Rack (Pintu Kaca + Blade LED + Monitor)</div>
    </div>

    <div id="hud-bottom">
        <div id="turn-badge" class="shift-badge shift-blue">SHIFT BIRU (INBOUND)</div>
        <div id="action-log">Klik unit Biru untuk memulai operasional...</div>
    </div>

    <div id="canvas-container"></div>

<script>
// ============================================================================
// 1. RENDERER & BLENDER HDRI STUDIO ENVIRONMENT
// ============================================================================
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0f1a);
scene.fog = new THREE.FogExp2(0x0a0f1a, 0.014);

const camera = new THREE.PerspectiveCamera(40, window.innerWidth / window.innerHeight, 0.1, 200);
camera.position.set(0, 11.5, 13.5);

const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;
renderer.outputEncoding = THREE.sRGBEncoding;
container.appendChild(renderer.domElement);

// Blender-like Studio HDRI Environment untuk pantulan logam & kaca nyata
const pmremGenerator = new THREE.PMREMGenerator(renderer);
scene.environment = pmremGenerator.fromScene(new THREE.RoomEnvironment(), 0.04).texture;

const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.maxPolarAngle = Math.PI / 2 - 0.03;
controls.minDistance = 4;
controls.maxDistance = 26;
controls.target.set(0, 0.6, 0);

// LIGHTING
const keyLight = new THREE.DirectionalLight(0xfff7ed, 1.25);
keyLight.position.set(10, 20, 12);
keyLight.castShadow = true;
keyLight.shadow.mapSize.set(2048, 2048);
const d = 8.5;
Object.assign(keyLight.shadow.camera, { left: -d, right: d, top: d, bottom: -d, near: 2, far: 45 });
keyLight.shadow.bias = -0.0005;
scene.add(keyLight);

const fillLight1 = new THREE.PointLight(0x38bdf8, 1.1, 28); fillLight1.position.set(-9, 7, 9); scene.add(fillLight1);
const fillLight2 = new THREE.PointLight(0xf59e0b, 1.1, 28); fillLight2.position.set(9, 7, -9); scene.add(fillLight2);

// ============================================================================
// 2. PROCEDURAL TEXTURES (EPOXY FLOOR, BARCODE BOX, HAZARD STRIPES)
// ============================================================================
function makeHazardTex() {
    const c = document.createElement('canvas'); c.width = 256; c.height = 256;
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#eab308'; ctx.fillRect(0,0,256,256);
    ctx.fillStyle = '#0f172a';
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
    ctx.fillStyle = isDark ? '#1e293b' : '#334155'; ctx.fillRect(0,0,256,256);
    ctx.strokeStyle = isDark ? '#334155' : '#475569'; ctx.lineWidth = 5; ctx.strokeRect(6,6,244,244);
    ctx.fillStyle = 'rgba(250, 204, 21, 0.28)';
    ctx.fillRect(12,12,14,3); ctx.fillRect(12,12,3,14);
    ctx.fillRect(230,12,14,3); ctx.fillRect(241,12,3,14);
    if (lbl) { ctx.fillStyle = 'rgba(203,213,225,0.45)'; ctx.font = 'bold 28px monospace'; ctx.fillText(lbl, 18, 236); }
    return new THREE.CanvasTexture(c);
}

function makeCardboardTex() {
    const c = document.createElement('canvas'); c.width = 256; c.height = 256;
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#b88655'; ctx.fillRect(0,0,256,256);
    // Serat kardus
    ctx.fillStyle = 'rgba(0,0,0,0.04)';
    for(let i=0; i<120; i++) ctx.fillRect(Math.random()*256, Math.random()*256, 18, 2);
    // Lakban coklat di tengah
    ctx.fillStyle = '#8c5a2b'; ctx.fillRect(0, 112, 256, 32);
    // Label putih barcode pengiriman
    ctx.fillStyle = '#ffffff'; ctx.fillRect(28, 30, 90, 56);
    ctx.fillStyle = '#000000';
    for(let b=36; b<110; b+=6) ctx.fillRect(b, 40, (b%12===0)?4:2, 30);
    // Simbol Fragile / Panah
    ctx.fillStyle = '#1e293b'; ctx.fillRect(180, 180, 40, 6);
    return new THREE.CanvasTexture(c);
}

// ============================================================================
// 3. WAREHOUSE FLOOR, BOARD & SELECTIVE PALLET RACKS
// ============================================================================
const boardGroup = new THREE.Group(); scene.add(boardGroup);
const floor = new THREE.Mesh(new THREE.PlaneGeometry(65,65), new THREE.MeshStandardMaterial({ color: 0x090d16, roughness: 0.35, metalness: 0.1 }));
floor.rotation.x = -Math.PI/2; floor.position.y = -0.35; floor.receiveShadow = true; scene.add(floor);

const base = new THREE.Mesh(new THREE.BoxGeometry(10.6, 0.35, 10.6), new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.25, metalness: 0.6 }));
base.position.y = -0.2; base.receiveShadow = true; boardGroup.add(base);

const hazMat = new THREE.MeshStandardMaterial({ map: makeHazardTex(), roughness: 0.3 });
[[0,-4.95,10.2,0.25],[0,4.95,10.2,0.25],[-4.95,0,0.25,10.2],[4.95,0,0.25,10.2]].forEach(([x,z,w,l]) => {
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
            new THREE.BoxGeometry(tileSize, 0.1, tileSize),
            new THREE.MeshStandardMaterial({ map: makeTileTex(isDark, lbl), roughness: isDark ? 0.15 : 0.24, metalness: 0.15 })
        );
        tile.position.set(x * tileSize - offset, 0, z * tileSize - offset);
        tile.receiveShadow = true;
        tile.userData = { gridX: x, gridZ: z };
        boardGroup.add(tile);
        tiles[x][z] = tile;
    }
}

const boxTex = makeCardboardTex();
function buildRack(xPos, zPos, rotY) {
    const r = new THREE.Group();
    const uMat = new THREE.MeshStandardMaterial({ color: 0x1d4ed8, metalness: 0.65, roughness: 0.25 });
    const bMat = new THREE.MeshStandardMaterial({ color: 0xea580c, metalness: 0.45, roughness: 0.3 });
    const cMat = new THREE.MeshStandardMaterial({ map: boxTex, roughness: 0.7 });
    [-1.8, 0, 1.8].forEach(lx => [-0.4, 0.4].forEach(lz => {
        const p = new THREE.Mesh(new THREE.BoxGeometry(0.09, 3.6, 0.09), uMat);
        p.position.set(lx, 1.8, lz); p.castShadow = true; r.add(p);
    }));
    [0.8, 1.9, 3.0].forEach(ly => {
        [-0.4, 0.4].forEach(bz => {
            const bm = new THREE.Mesh(new THREE.BoxGeometry(3.7, 0.09, 0.07), bMat);
            bm.position.set(0, ly, bz); r.add(bm);
        });
        [-1.1, 0, 1.1].forEach(bx => {
            const bxMesh = new THREE.Mesh(new THREE.BoxGeometry(0.65, 0.5, 0.65), cMat);
            bxMesh.position.set(bx, ly + 0.3, 0); bxMesh.castShadow = true; r.add(bxMesh);
        });
    });
    r.position.set(xPos, -0.35, zPos); r.rotation.y = rotY; scene.add(r);
}
buildRack(-7.6, -2.3, Math.PI/2); buildRack(-7.6, 2.3, Math.PI/2);
buildRack(7.6, -2.3, -Math.PI/2); buildRack(7.6, 2.3, -Math.PI/2);

// ============================================================================
// 4. REALISTIC PBR MATERIALS & ANATOMY/CAD MODEL BUILDERS
// ============================================================================
const animatedParts = [];
const humanIdles = [];

const mats = {
    skin: new THREE.MeshStandardMaterial({ color: 0xe8b48a, roughness: 0.45, metalness: 0.05 }),
    navyPants: new THREE.MeshStandardMaterial({ color: 0x172554, roughness: 0.8 }),
    darkIron: new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.85, roughness: 0.25 }),
    blackSteel: new THREE.MeshStandardMaterial({ color: 0x0f172a, metalness: 0.75, roughness: 0.35 }),
    chrome: new THREE.MeshStandardMaterial({ color: 0xf8fafc, metalness: 0.98, roughness: 0.05 }),
    rubberTire: new THREE.MeshStandardMaterial({ color: 0x111827, roughness: 0.92, metalness: 0.05 }),
    leatherSeat: new THREE.MeshStandardMaterial({ color: 0x18181b, roughness: 0.4, metalness: 0.1 }),
    cardboard: new THREE.MeshStandardMaterial({ map: boxTex, roughness: 0.72 }),
    woodPallet: new THREE.MeshStandardMaterial({ color: 0x9c6b3b, roughness: 0.85 }),
    hiVisLime: new THREE.MeshStandardMaterial({ color: 0xa3e635, roughness: 0.32, emissive: 0x365314, emissiveIntensity: 0.15 }),
    hiVisOrange: new THREE.MeshStandardMaterial({ color: 0xf97316, roughness: 0.32, emissive: 0x7c2d12, emissiveIntensity: 0.15 }),
    reflectiveStrip: new THREE.MeshStandardMaterial({ color: 0xe2e8f0, metalness: 0.9, roughness: 0.1, emissive: 0x94a3b8, emissiveIntensity: 0.35 }),
    whiteHelmet: new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.15, metalness: 0.1 }),
    goldHelmet: new THREE.MeshStandardMaterial({ color: 0xfbbf24, roughness: 0.18, metalness: 0.6 }),
    visorGlass: new THREE.MeshPhysicalMaterial({ color: 0x0284c7, metalness: 0.1, roughness: 0.05, transmission: 0.7, transparent: true, opacity: 0.8 }),
    stretchWrap: new THREE.MeshPhysicalMaterial({ color: 0xe0f2fe, roughness: 0.1, transmission: 0.65, transparent: true, opacity: 0.45 }),
    serverGlass: new THREE.MeshPhysicalMaterial({ color: 0x0f172a, roughness: 0.08, metalness: 0.2, transmission: 0.75, transparent: true, opacity: 0.65 }),
    amberBeacon: new THREE.MeshStandardMaterial({ color: 0xf59e0b, emissive: 0xff8800, emissiveIntensity: 1.8 }),
    headlight: new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0xe0f2fe, emissiveIntensity: 2.0 })
};

// HELPER: Roda Kendaraan Detail (Ban Karet + Velg Baja + Poros Baut)
function makeDetailedWheel(radius, width, rimMat) {
    const wGroup = new THREE.Group();
    const tire = new THREE.Mesh(new THREE.CylinderGeometry(radius, radius, width, 24), mats.rubberTire);
    tire.rotation.z = Math.PI / 2;
    tire.castShadow = true;
    wGroup.add(tire);

    const rim = new THREE.Mesh(new THREE.CylinderGeometry(radius * 0.58, radius * 0.58, width + 0.01, 16), rimMat);
    rim.rotation.z = Math.PI / 2;
    wGroup.add(rim);

    const hub = new THREE.Mesh(new THREE.CylinderGeometry(radius * 0.22, radius * 0.22, width + 0.025, 10), mats.darkIron);
    hub.rotation.z = Math.PI / 2;
    wGroup.add(hub);
    return wGroup;
}

// HELPER: Palet Kayu Euro Standar Gudang (Papan Atas + Balok Penyangga + Papan Bawah)
function makeEuroPallet(w, l) {
    const p = new THREE.Group();
    // 5 Papan Kayu Atas
    for (let i = -2; i <= 2; i++) {
        const slat = new THREE.Mesh(new THREE.BoxGeometry(w, 0.02, l * 0.16), mats.woodPallet);
        slat.position.set(0, 0.07, i * (l * 0.2));
        slat.castShadow = true;
        p.add(slat);
    }
    // 3 Balok Stringer Penyangga
    [-w * 0.4, 0, w * 0.4].forEach(bx => {
        const block = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.05, l * 0.96), mats.woodPallet);
        block.position.set(bx, 0.035, 0);
        p.add(block);
    });
    return p;
}

// HELPER: Karakter Manusia Proporsional Realistis (Articulated Human Figure)
function buildArticulatedHuman(teamMat, vestMat, helmetMat, hasGoggles) {
    const human = new THREE.Group();

    // 1. SEPATU SAFETY BOOTS (Kiri & Kanan dengan Sol Tebal + Ujung Steel-Toe)
    [-0.095, 0.095].forEach(lx => {
        const bootSole = new THREE.Mesh(new THREE.BoxGeometry(0.095, 0.04, 0.19), mats.rubberTire);
        bootSole.position.set(lx, 0.02, -0.02);
        human.add(bootSole);

        const bootUpper = new THREE.Mesh(new THREE.BoxGeometry(0.088, 0.09, 0.15), mats.leatherSeat);
        bootUpper.position.set(lx, 0.07, -0.01);
        bootUpper.castShadow = true;
        human.add(bootUpper);

        // Betis & Paha (Celana Kerja Kargo)
        const calf = new THREE.Mesh(new THREE.CylinderGeometry(0.052, 0.044, 0.22, 14), mats.navyPants);
        calf.position.set(lx, 0.21, 0);
        calf.castShadow = true;
        human.add(calf);

        const knee = new THREE.Mesh(new THREE.SphereGeometry(0.052, 12, 12), mats.navyPants);
        knee.position.set(lx, 0.32, 0);
        human.add(knee);

        const thigh = new THREE.Mesh(new THREE.CylinderGeometry(0.064, 0.054, 0.23, 14), mats.navyPants);
        thigh.position.set(lx, 0.43, 0);
        thigh.castShadow = true;
        human.add(thigh);
    });

    // 2. PINGGUL & SABUK KERJA (Pelvis & Utility Belt dengan Gesper Perak)
    const pelvis = new THREE.Mesh(new THREE.BoxGeometry(0.27, 0.1, 0.17), mats.navyPants);
    pelvis.position.set(0, 0.54, 0);
    human.add(pelvis);

    const belt = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.04, 0.18), mats.leatherSeat);
    belt.position.set(0, 0.58, 0);
    human.add(belt);

    const buckle = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.045, 0.19), mats.chrome);
    buckle.position.set(0, 0.58, 0);
    human.add(buckle);

    // 3. UPPER BODY GROUP (Untuk Animasi Bernapas Halus)
    const upperBody = new THREE.Group();
    upperBody.position.set(0, 0.6, 0);
    human.add(upperBody);

    // Dada / Kemeja Seragam Tim (Tapered Torso)
    const chest = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.13, 0.34, 16), teamMat);
    chest.scale.set(1.15, 1, 0.78);
    chest.position.set(0, 0.17, 0);
    chest.castShadow = true;
    upperBody.add(chest);

    // Rompi Keselamatan (Hi-Vis Safety Vest + Dual Reflective Strips)
    const vest = new THREE.Mesh(new THREE.CylinderGeometry(0.168, 0.138, 0.31, 16), vestMat);
    vest.scale.set(1.16, 1, 0.8);
    vest.position.set(0, 0.17, 0);
    vest.castShadow = true;
    upperBody.add(vest);

    // Bukaan Kerah V-Neck depan
    const vNeck = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.12, 0.15), teamMat);
    vNeck.position.set(0, 0.27, -0.06);
    upperBody.add(vNeck);

    // 2 Garis Scotchlite Reflektif Horizontal & 2 Vertikal
    [0.08, 0.19].forEach(sy => {
        const hStrip = new THREE.Mesh(new THREE.CylinderGeometry(0.171, 0.15, 0.032, 16), mats.reflectiveStrip);
        hStrip.scale.set(1.17, 1, 0.81);
        hStrip.position.set(0, sy, 0);
        upperBody.add(hStrip);
    });
    [-0.08, 0.08].forEach(sx => {
        const vStrip = new THREE.Mesh(new THREE.BoxGeometry(0.032, 0.31, 0.23), mats.reflectiveStrip);
        vStrip.position.set(sx, 0.175, 0);
        upperBody.add(vStrip);
    });

    // 4. LEHER, KEPALA, WAJAH (MATA, HIDUNG, TELINGA) & HELM PROYEK OSHA
    const neck = new THREE.Mesh(new THREE.CylinderGeometry(0.055, 0.065, 0.09, 14), mats.skin);
    neck.position.set(0, 0.37, 0);
    upperBody.add(neck);

    const headGroup = new THREE.Group();
    headGroup.position.set(0, 0.48, 0);
    upperBody.add(headGroup);

    // Tengkorak & Rahang
    const cranium = new THREE.Mesh(new THREE.SphereGeometry(0.115, 20, 20), mats.skin);
    cranium.scale.set(0.95, 1.08, 1.0);
    cranium.castShadow = true;
    headGroup.add(cranium);

    // Hidung
    const nose = new THREE.Mesh(new THREE.ConeGeometry(0.022, 0.05, 8), mats.skin);
    nose.rotation.x = -Math.PI / 2;
    nose.position.set(0, -0.01, -0.12);
    headGroup.add(nose);

    // Telinga Kiri & Kanan
    [-0.11, 0.11].forEach(ex => {
        const ear = new THREE.Mesh(new THREE.SphereGeometry(0.025, 10, 10), mats.skin);
        ear.scale.set(0.5, 1.2, 0.8);
        ear.position.set(ex, 0, 0);
        headGroup.add(ear);
    });

    // Mata atau Kacamata Safety Goggles
    if (hasGoggles) {
        const goggles = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.048, 0.08), mats.visorGlass);
        goggles.position.set(0, 0.015, -0.09);
        headGroup.add(goggles);
        const strap = new THREE.Mesh(new THREE.CylinderGeometry(0.116, 0.116, 0.025, 16), mats.leatherSeat);
        strap.position.set(0, 0.015, 0);
        headGroup.add(strap);
    } else {
        [-0.04, 0.04].forEach(mx => {
            const eye = new THREE.Mesh(new THREE.SphereGeometry(0.014, 8, 8), mats.leatherSeat);
            eye.position.set(mx, 0.015, -0.105);
            headGroup.add(eye);
        });
    }

    // HELM SAFETY PROYEK (Dome + Top Ridge + Visor Brim Depan)
    const dome = new THREE.Mesh(new THREE.SphereGeometry(0.128, 20, 14, 0, Math.PI * 2, 0, Math.PI * 0.54), helmetMat);
    dome.position.set(0, 0.02, 0);
    dome.castShadow = true;
    headGroup.add(dome);

    const ridge = new THREE.Mesh(new THREE.BoxGeometry(0.036, 0.035, 0.23), helmetMat);
    ridge.position.set(0, 0.14, 0);
    headGroup.add(ridge);

    const rim = new THREE.Mesh(new THREE.CylinderGeometry(0.136, 0.14, 0.018, 20), helmetMat);
    rim.position.set(0, 0.03, 0);
    headGroup.add(rim);

    const visorBrim = new THREE.Mesh(new THREE.CylinderGeometry(0.138, 0.145, 0.018, 16, 1, false, Math.PI * 0.65, Math.PI * 0.7), helmetMat);
    visorBrim.position.set(0, 0.025, -0.035);
    headGroup.add(visorBrim);

    humanIdles.push({ upperBody, headGroup, phase: Math.random() * Math.PI * 2 });
    return { root: human, upperBody, headGroup };
}

// HELPER: Buat Lengan Berartikulasi (Bahu -> Lengan Atas -> Siku -> Lengan Bawah -> Sarung Tangan)
function attachArm(upperBody, side, shoulderRotX, shoulderRotZ, elbowRotX, teamMat, gloveMat) {
    const sGroup = new THREE.Group();
    sGroup.position.set(side * 0.2, 0.3, 0);
    sGroup.rotation.set(shoulderRotX, 0, shoulderRotZ);
    upperBody.add(sGroup);

    const shoulderBall = new THREE.Mesh(new THREE.SphereGeometry(0.052, 12, 12), teamMat);
    sGroup.add(shoulderBall);

    const upperArm = new THREE.Mesh(new THREE.CylinderGeometry(0.046, 0.038, 0.19, 12), teamMat);
    upperArm.position.set(0, -0.095, 0);
    upperArm.castShadow = true;
    sGroup.add(upperArm);

    const eGroup = new THREE.Group();
    eGroup.position.set(0, -0.19, 0);
    eGroup.rotation.x = elbowRotX;
    sGroup.add(eGroup);

    const elbowBall = new THREE.Mesh(new THREE.SphereGeometry(0.04, 10, 10), mats.skin);
    eGroup.add(elbowBall);

    const forearm = new THREE.Mesh(new THREE.CylinderGeometry(0.038, 0.032, 0.18, 12), mats.skin);
    forearm.position.set(0, -0.09, 0);
    forearm.castShadow = true;
    eGroup.add(forearm);

    const hand = new THREE.Mesh(new THREE.SphereGeometry(0.04, 12, 12), gloveMat);
    hand.scale.set(0.85, 1.1, 1.2);
    hand.position.set(0, -0.19, 0);
    eGroup.add(hand);

    return { sGroup, eGroup, hand };
}

// ============================================================================
// 5. PEMBANGUN 6 UNIT BIDAK LOGISTIK SUPER REALISTIS
// ============================================================================
function createUnitMesh(type, team) {
    const root = new THREE.Group();
    const isBlue = team === 'blue';
    
    const teamPrimary = new THREE.MeshStandardMaterial({
        color: isBlue ? 0x0284c7 : 0xea580c,
        roughness: 0.25, metalness: 0.35
    });
    const teamSecondary = new THREE.MeshStandardMaterial({
        color: isBlue ? 0x38bdf8 : 0xfbbf24,
        roughness: 0.2, metalness: 0.5
    });

    // Ring Indikator Taktis Tipis di Lantai (Tanpa Podium Tebal agar Seperti Dunia Nyata)
    const pad = new THREE.Mesh(new THREE.CylinderGeometry(0.48, 0.5, 0.02, 32), mats.darkIron);
    pad.position.y = 0.01; pad.receiveShadow = true;
    root.add(pad);

    const glowRing = new THREE.Mesh(new THREE.TorusGeometry(0.49, 0.018, 12, 32), teamSecondary);
    glowRing.rotation.x = Math.PI / 2;
    glowRing.position.y = 0.02;
    root.add(glowRing);

    const dir = new THREE.Group();
    dir.rotation.y = isBlue ? 0 : Math.PI;
    dir.position.y = 0.02;
    root.add(dir);

    // ------------------------------------------------------------------------
    // 1. PION: OPERATOR PICKER (ANATOMI MANUSIA MEMBAWA KARDUS BERLABEL)
    // ------------------------------------------------------------------------
    if (type === 'pawn') {
        const vestMat = isBlue ? mats.hiVisLime : mats.hiVisOrange;
        const { root: fig, upperBody } = buildArticulatedHuman(teamPrimary, vestMat, teamSecondary, false);
        dir.add(fig);

        // Kedua tangan merengkuh kardus di depan dada
        attachArm(upperBody, -1, 0.65, -0.15, 1.05, teamPrimary, mats.leatherSeat);
        attachArm(upperBody, 1, 0.65, 0.15, 1.05, teamPrimary, mats.leatherSeat);

        // Kardus Logistik Detail dengan Lakban & Barcode
        const box = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.25, 0.28), mats.cardboard);
        box.position.set(0, 0.13, -0.26);
        box.castShadow = true;
        upperBody.add(box);
    }

    // ------------------------------------------------------------------------
    // 2. BENTENG: COUNTERBALANCE FORKLIFT (KABIN, KURSI, SETIR, RANTAI, BAN)
    // ------------------------------------------------------------------------
    else if (type === 'rook') {
        // 4 Roda Detail (Roda Depan Lebih Besar dari Roda Kemudi Belakang)
        const wFL = makeDetailedWheel(0.15, 0.1, teamSecondary); wFL.position.set(-0.29, 0.15, -0.22); dir.add(wFL);
        const wFR = makeDetailedWheel(0.15, 0.1, teamSecondary); wFR.position.set(0.29, 0.15, -0.22); dir.add(wFR);
        const wBL = makeDetailedWheel(0.11, 0.09, teamSecondary); wBL.position.set(-0.26, 0.11, 0.28); dir.add(wBL);
        const wBR = makeDetailedWheel(0.11, 0.09, teamSecondary); wBR.position.set(0.26, 0.11, 0.28); dir.add(wBR);

        // Sasis Bawah & Body Utama Berlekuk
        const underbody = new THREE.Mesh(new THREE.BoxGeometry(0.48, 0.14, 0.68), mats.darkIron);
        underbody.position.set(0, 0.16, 0.04); underbody.castShadow = true; dir.add(underbody);

        const cowling = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.24, 0.34), teamPrimary);
        cowling.position.set(0, 0.32, -0.08); cowling.castShadow = true; dir.add(cowling);

        // Counterweight Melengkung Berat di Belakang + Knalpot
        const cw = new THREE.Mesh(new THREE.CylinderGeometry(0.26, 0.25, 0.34, 20), mats.darkIron);
        cw.scale.set(1.0, 1.0, 0.75);
        cw.position.set(0, 0.31, 0.26); cw.castShadow = true; dir.add(cw);

        const cwStripe = new THREE.Mesh(new THREE.CylinderGeometry(0.263, 0.255, 0.08, 20), teamSecondary);
        cwStripe.scale.set(1.0, 1.0, 0.76);
        cwStripe.position.set(0, 0.31, 0.26); dir.add(cwStripe);

        // Kursi Kulit Pengemudi (Bantalan + Sandaran)
        const seatBase = new THREE.Mesh(new THREE.BoxGeometry(0.24, 0.06, 0.24), mats.leatherSeat);
        seatBase.position.set(0, 0.46, 0.08); dir.add(seatBase);
        const seatBack = new THREE.Mesh(new THREE.BoxGeometry(0.24, 0.24, 0.05), mats.leatherSeat);
        seatBack.position.set(0, 0.58, 0.19); seatBack.rotation.x = -0.15; dir.add(seatBack);

        // Kolom Kemudi, Setir Bundar & 2 Tuas Hidrolik
        const steerCol = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.03, 0.26, 10), mats.blackSteel);
        steerCol.position.set(0, 0.54, -0.14); steerCol.rotation.x = 0.45; dir.add(steerCol);

        const wheel = new THREE.Mesh(new THREE.TorusGeometry(0.075, 0.014, 10, 20), mats.leatherSeat);
        wheel.position.set(0, 0.65, -0.09); wheel.rotation.x = Math.PI / 2 + 0.45; dir.add(wheel);

        [0.12, 0.16].forEach((lx, idx) => {
            const lever = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 0.14, 8), mats.chrome);
            lever.position.set(lx, 0.5, -0.12 + idx * 0.04); lever.rotation.x = 0.3; dir.add(lever);
            const knob = new THREE.Mesh(new THREE.SphereGeometry(0.018, 8, 8), mats.leatherSeat);
            knob.position.set(lx, 0.56, -0.1 + idx * 0.04); dir.add(knob);
        });

        // Overhead Guard Roll-Cage + Kisi Pelindung Atap
        [[-0.22, -0.2], [0.22, -0.2], [-0.22, 0.24], [0.22, 0.24]].forEach(([px, pz]) => {
            const post = new THREE.Mesh(new THREE.CylinderGeometry(0.022, 0.022, 0.58, 10), mats.blackSteel);
            post.position.set(px, 0.68, pz); post.castShadow = true; dir.add(post);
        });
        const roofFrame = new THREE.Mesh(new THREE.BoxGeometry(0.48, 0.04, 0.48), mats.blackSteel);
        roofFrame.position.set(0, 0.96, 0.02); dir.add(roofFrame);
        for (let gz = -0.16; gz <= 0.18; gz += 0.08) {
            const bar = new THREE.Mesh(new THREE.BoxGeometry(0.44, 0.015, 0.02), mats.darkIron);
            bar.position.set(0, 0.97, gz); dir.add(bar);
        }

        // Lampu Sorot Depan LED & Rotary Amber Beacon di Atap
        [-0.19, 0.19].forEach(hx => {
            const hLight = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.05, 0.04), mats.headlight);
            hLight.position.set(hx, 0.88, -0.22); dir.add(hLight);
        });
        const beacon = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.05, 0.09, 14), mats.amberBeacon);
        beacon.position.set(0, 1.03, 0.18); dir.add(beacon);
        animatedParts.push({ mesh: beacon, type: 'pulse' });

        // Tiang Hidrolik Ganda (Dual Mast Rails + Silinder Tengah + Rantai + Backrest + Garpu Baja)
        [-0.15, 0.15].forEach(mx => {
            const rail = new THREE.Mesh(new THREE.BoxGeometry(0.05, 1.05, 0.06), mats.blackSteel);
            rail.position.set(mx, 0.58, -0.32); rail.castShadow = true; dir.add(rail);

            // Lempengan Garpu L-Shaped Chrome
            const forkVert = new THREE.Mesh(new THREE.BoxGeometry(0.055, 0.28, 0.025), mats.chrome);
            forkVert.position.set(mx, 0.24, -0.36); dir.add(forkVert);
            const forkBlade = new THREE.Mesh(new THREE.BoxGeometry(0.055, 0.025, 0.42), mats.chrome);
            forkBlade.position.set(mx, 0.11, -0.55); forkBlade.castShadow = true; dir.add(forkBlade);
        });

        // Silinder Hidrolik Tengah & Load Backrest
        const piston = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.035, 0.95, 12), mats.chrome);
        piston.position.set(0, 0.54, -0.32); dir.add(piston);
        const backrest = new THREE.Mesh(new THREE.BoxGeometry(0.38, 0.22, 0.02), mats.blackSteel);
        backrest.position.set(0, 0.32, -0.35); dir.add(backrest);
    }

    // ------------------------------------------------------------------------
    // 3. KUDA: ELECTRIC PALLET JACK + EURO PALLET + STRETCH-WRAPPED CARGO
    // ------------------------------------------------------------------------
    else if (type === 'knight') {
        // Roda Penggerak Belakang & Load Rollers Depan
        const driveWheel = makeDetailedWheel(0.1, 0.08, mats.chrome);
        driveWheel.position.set(0, 0.1, 0.28); dir.add(driveWheel);

        // Rumah Mesin Elektrik Melengkung (Battery & Motor Compartment)
        const housing = new THREE.Mesh(new THREE.BoxGeometry(0.44, 0.44, 0.26), teamPrimary);
        housing.position.set(0, 0.28, 0.24); housing.castShadow = true; dir.add(housing);

        const topCover = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.22, 0.26, 16), teamSecondary);
        topCover.rotation.x = Math.PI / 2;
        topCover.scale.set(1, 0.4, 1);
        topCover.position.set(0, 0.5, 0.24); dir.add(topCover);

        // Stang Kemudi Ergonomis (Tiller Arm + Butterfly Grips + Emergency Stop Belly Button Merah)
        const tillerArm = new THREE.Mesh(new THREE.CylinderGeometry(0.024, 0.028, 0.48, 12), mats.blackSteel);
        tillerArm.position.set(0, 0.68, 0.3); tillerArm.rotation.x = -0.38; dir.add(tillerArm);

        const tillerHead = new THREE.Mesh(new THREE.BoxGeometry(0.24, 0.06, 0.08), mats.darkIron);
        tillerHead.position.set(0, 0.89, 0.39); dir.add(tillerHead);

        const eStop = new THREE.Mesh(new THREE.SphereGeometry(0.028, 10, 10), new THREE.MeshStandardMaterial({ color: 0xef4444, emissive: 0x991b1b }));
        eStop.position.set(0, 0.91, 0.42); dir.add(eStop);

        // Garpu Pallet Jack + Euro Wood Pallet + 3 Kardus Bertumpuk + Plastik Stretch Wrap
        [-0.14, 0.14].forEach(fx => {
            const pFork = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.04, 0.58), mats.blackSteel);
            pFork.position.set(fx, 0.06, -0.15); dir.add(pFork);
        });

        const euroPallet = makeEuroPallet(0.5, 0.54);
        euroPallet.position.set(0, 0.06, -0.16);
        dir.add(euroPallet);

        // Tumpukan Kargo Kardus
        const box1 = new THREE.Mesh(new THREE.BoxGeometry(0.23, 0.24, 0.44), mats.cardboard);
        box1.position.set(-0.12, 0.26, -0.16); box1.castShadow = true; dir.add(box1);
        const box2 = new THREE.Mesh(new THREE.BoxGeometry(0.23, 0.24, 0.44), mats.cardboard);
        box2.position.set(0.12, 0.26, -0.16); box2.castShadow = true; dir.add(box2);
        const box3 = new THREE.Mesh(new THREE.BoxGeometry(0.38, 0.22, 0.38), mats.cardboard);
        box3.position.set(0, 0.49, -0.16); box3.rotation.y = 0.08; box3.castShadow = true; dir.add(box3);

        // Selubung Plastik Stretch-Wrap Bening Mengkilap
        const wrap = new THREE.Mesh(new THREE.BoxGeometry(0.49, 0.48, 0.47), mats.stretchWrap);
        wrap.position.set(0, 0.38, -0.16);
        dir.add(wrap);
    }

    // ------------------------------------------------------------------------
    // 4. GAJAH: QC INSPECTOR (HELM PUTIH, CLIPBOARD & PISTOL BARCODE SCANNER)
    // ------------------------------------------------------------------------
    else if (type === 'bishop') {
        const vestMat = isBlue ? mats.hiVisLime : mats.hiVisOrange;
        const { root: fig, upperBody } = buildArticulatedHuman(teamPrimary, vestMat, mats.whiteHelmet, true);
        dir.add(fig);

        // Lengan Kiri Memegang Papan Clipboard Pemeriksaan
        const leftArm = attachArm(upperBody, -1, 0.45, 0.1, 0.95, teamPrimary, mats.skin);
        const clipboard = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.22, 0.015), mats.woodPallet);
        clipboard.position.set(0.04, -0.18, -0.06);
        clipboard.rotation.set(1.2, 0.2, -0.3);
        leftArm.eGroup.add(clipboard);
        const paper = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.19, 0.018), mats.whiteHelmet);
        paper.position.copy(clipboard.position); paper.rotation.copy(clipboard.rotation);
        leftArm.eGroup.add(paper);

        // Lengan Kanan Menodongkan Pistol Laser Barcode Scanner
        const rightArm = attachArm(upperBody, 1, 0.85, -0.05, 0.65, teamPrimary, mats.skin);
        const gunGrip = new THREE.Mesh(new THREE.BoxGeometry(0.035, 0.09, 0.04), mats.blackSteel);
        gunGrip.position.set(0, -0.2, -0.02);
        rightArm.eGroup.add(gunGrip);
        const gunBarrel = new THREE.Mesh(new THREE.BoxGeometry(0.045, 0.05, 0.13), mats.amberBeacon);
        gunBarrel.position.set(0, -0.22, -0.07);
        rightArm.eGroup.add(gunBarrel);

        // Sorot Laser Merah Fan-Beam
        const laserFan = new THREE.Mesh(
            new THREE.ConeGeometry(0.14, 0.42, 16),
            new THREE.MeshBasicMaterial({ color: 0xff0044, transparent: true, opacity: 0.5 })
        );
        laserFan.rotation.x = -Math.PI / 2;
        laserFan.position.set(0, -0.22, -0.34);
        rightArm.eGroup.add(laserFan);
    }

    // ------------------------------------------------------------------------
    // 5. MENTERI (QUEEN): WAREHOUSE OPERATIONS SUPERVISOR
    // ------------------------------------------------------------------------
    else if (type === 'queen') {
        // Supervisor menggunakan Helm Emas Eksekutif, Goggles & Rompi Khusus
        const { root: fig, upperBody } = buildArticulatedHuman(teamPrimary, mats.darkIron, mats.goldHelmet, true);
        fig.scale.set(1.06, 1.06, 1.06);
        dir.add(fig);

        // Epaulet Pangkat Emas di Kedua Bahu
        [-0.16, 0.16].forEach(ex => {
            const ep = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.02, 0.1), mats.goldHelmet);
            ep.position.set(ex, 0.34, 0);
            upperBody.add(ep);
        });

        // Radio HT Walkie-Talkie + Antena Tinggi di Dada Kiri
        const radio = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.1, 0.035), mats.blackSteel);
        radio.position.set(-0.11, 0.25, -0.14);
        upperBody.add(radio);
        const ant = new THREE.Mesh(new THREE.CylinderGeometry(0.005, 0.005, 0.16, 8), mats.chrome);
        ant.position.set(-0.12, 0.36, -0.14);
        upperBody.add(ant);

        // Lengan Kiri Memegang Tablet Ruggedized WMS Berlayar Menyala
        attachArm(upperBody, -1, 0.55, -0.1, 1.1, teamPrimary, mats.skin);
        attachArm(upperBody, 1, 0.4, 0.15, 0.9, teamPrimary, mats.skin);

        const tabletFrame = new THREE.Mesh(new THREE.BoxGeometry(0.26, 0.18, 0.025), mats.blackSteel);
        tabletFrame.position.set(0, 0.18, -0.26);
        tabletFrame.rotation.x = -0.55;
        upperBody.add(tabletFrame);

        const screen = new THREE.Mesh(new THREE.BoxGeometry(0.23, 0.15, 0.028), new THREE.MeshStandardMaterial({
            color: 0x0284c7, emissive: 0x38bdf8, emissiveIntensity: 0.95
        }));
        screen.position.copy(tabletFrame.position);
        screen.rotation.copy(tabletFrame.rotation);
        upperBody.add(screen);
    }

    // ------------------------------------------------------------------------
    // 6. RAJA (KING): ENTERPRISE WMS SERVER CABINET + GLASS DOOR + MONITOR
    // ------------------------------------------------------------------------
    else if (type === 'king') {
        // Sasis Kabinet Server 42U
        const rackChassis = new THREE.Mesh(new THREE.BoxGeometry(0.56, 1.12, 0.54), mats.blackSteel);
        rackChassis.position.set(0, 0.56, 0.04);
        rackChassis.castShadow = true;
        dir.add(rackChassis);

        // Pilar Aksen Samping Berwarna Tim
        [-0.28, 0.28].forEach(px => {
            const pillar = new THREE.Mesh(new THREE.BoxGeometry(0.04, 1.14, 0.56), teamSecondary);
            pillar.position.set(px, 0.57, 0.04);
            dir.add(pillar);
        });

        // 7 Unit Blade Server Internal dengan Deretan LED Berkedip
        for (let i = 0; i < 7; i++) {
            const sy = 0.16 + i * 0.135;
            const blade = new THREE.Mesh(new THREE.BoxGeometry(0.46, 0.09, 0.48), mats.darkIron);
            blade.position.set(0, sy, 0.04);
            dir.add(blade);

            const ledStrip = new THREE.Mesh(new THREE.BoxGeometry(0.38, 0.025, 0.02), new THREE.MeshStandardMaterial({
                color: isBlue ? 0x38bdf8 : 0xfbbf24,
                emissive: isBlue ? 0x0284c7 : 0xd97706,
                emissiveIntensity: 1.5
            }));
            ledStrip.position.set(0, sy, -0.2);
            dir.add(ledStrip);
        }

        // Pintu Kaca Tempered Transparan di Bagian Depan + Gagang Krom
        const glassDoor = new THREE.Mesh(new THREE.BoxGeometry(0.5, 1.06, 0.02), mats.serverGlass);
        glassDoor.position.set(0, 0.56, -0.24);
        dir.add(glassDoor);

        const doorHandle = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.22, 10), mats.chrome);
        doorHandle.position.set(0.2, 0.56, -0.26);
        dir.add(doorHandle);

        // Kipas Pendingin Ganda & Dish Transceiver WMS di Atap Server
        const topFan = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.2, 0.05, 20), mats.darkIron);
        topFan.position.set(0, 1.15, 0.04);
        dir.add(topFan);

        // Hologram Core Data Berputar di Puncak Kabinet
        const core = new THREE.Mesh(new THREE.OctahedronGeometry(0.16, 1), new THREE.MeshStandardMaterial({
            color: isBlue ? 0x38bdf8 : 0xfbbf24,
            emissive: isBlue ? 0x0284c7 : 0xf59e0b,
            emissiveIntensity: 1.2,
            wireframe: true
        }));
        core.position.set(0, 1.36, 0.04);
        dir.add(core);
        animatedParts.push({ mesh: core, type: 'spin' });
    }

    return root;
}

// ============================================================================
// 6. CHESS ENGINE, AI BOT & REALISTIC EXPLOSION
// ============================================================================
let pieces = [], selectedPiece = null, validMoves = [], currentTurn = 'blue', isAnimating = false, vsAI = true, highlights = [];
const names = { pawn: 'Operator Picker', rook: 'Counterbalance Forklift', knight: 'Electric Pallet Truck', bishop: 'QC Inspector', queen: 'Warehouse Supervisor', king: 'Main WMS Server' };
const weights = { pawn: 10, knight: 30, bishop: 30, rook: 50, queen: 90, king: 900 };

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
            new THREE.MeshBasicMaterial({ color: m.attack ? 0xef4444 : 0x22c55e, transparent: true, opacity: 0.45, side: THREE.DoubleSide })
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
            let msg = `${names[piece.userData.type]} menuju zona ${cols[moveData.x]}${8 - moveData.z}.`;

            if (moveData.attack && moveData.target) {
                const v = moveData.target; v.userData.alive = false; scene.remove(v);
                triggerExplosion(piece.position);
                msg = `💥 EPIC ACTION! ${names[piece.userData.type]} menyingkirkan ${names[v.userData.type]}!`;
                if (v.userData.type === 'king') {
                    updateHUD(`🏆 OVERRIDE SELESAI! Tim ${currentTurn.toUpperCase()} menguasai WMS Server!`);
                    isAnimating = false; return;
                }
            }

            if (piece.userData.type === 'pawn' && (moveData.z === 0 || moveData.z === 7)) {
                const tm = piece.userData.team; scene.remove(piece);
                pieces = pieces.filter(p => p !== piece);
                spawnUnit('queen', tm, moveData.x, moveData.z);
                msg = `⭐ PROMOSI JABATAN! Operator diangkat menjadi Warehouse Supervisor!`;
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
    selectedPiece = null; validMoves = []; currentTurn = 'blue'; isAnimating = false;
    const row = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook'];
    for (let i = 0; i < 8; i++) {
        spawnUnit(row[i], 'orange', i, 0); spawnUnit('pawn', 'orange', i, 1);
        spawnUnit('pawn', 'blue', i, 6); spawnUnit(row[i], 'blue', i, 7);
    }
    updateHUD("Shift Baru Dimulai! Klik tombol '🔍 Zoom Karakter' untuk melihat detail anatomi & forklift.");
}

function updateHUD(msg) {
    const b = document.getElementById('turn-badge');
    b.className = currentTurn === 'blue' ? 'shift-badge shift-blue' : 'shift-badge shift-orange';
    b.innerText = currentTurn === 'blue' ? 'SHIFT BIRU (INBOUND)' : 'SHIFT ORANYE (OUTBOUND)';
    if (msg) document.getElementById('action-log').innerText = msg;
}

function toggleAI() {
    vsAI = !vsAI;
    const btn = document.getElementById('btn-ai');
    btn.innerText = vsAI ? '🤖 Mode: vs AI Bot' : '👥 Mode: 2 Player';
    btn.classList.toggle('active', vsAI);
}

function setCameraView(mode) {
    if (mode === 'top') {
        camera.position.set(0, 18.5, 0.01);
        controls.target.set(0, 0, 0);
    } else if (mode === 'closeup') {
        camera.position.set(-2.5, 3.8, 7.8);
        controls.target.set(0, 0.8, 3.2);
    } else {
        camera.position.set(0, 11.5, 13.5);
        controls.target.set(0, 0.6, 0);
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
    if (unit && unit.userData.team === currentTurn) {
        selectedPiece = unit; validMoves = getValidMoves(unit); showHighlights(validMoves);
        updateHUD(`Terpilih: ${names[unit.userData.type]} (${cols[coords.x]}${8 - coords.z})`);
    } else {
        selectedPiece = null; validMoves = []; clearHighlights();
    }
});

const clock = new THREE.Clock();
resetGame();

function animate() {
    requestAnimationFrame(animate);
    const t = clock.getElapsedTime();

    // Animasi mesin & hologram
    animatedParts.forEach(p => {
        if (p.type === 'spin') { p.mesh.rotation.y = t * 1.8; p.mesh.rotation.x = t * 0.9; }
        else if (p.type === 'pulse') { p.mesh.material.emissiveIntensity = 1.0 + Math.sin(t * 9) * 0.7; }
    });

    // Animasi bernapas & gerakan kepala manusia realistis
    humanIdles.forEach(h => {
        h.upperBody.position.y = 0.6 + Math.sin(t * 2.5 + h.phase) * 0.008;
        h.headGroup.rotation.y = Math.sin(t * 1.2 + h.phase) * 0.08;
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
