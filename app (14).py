import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Warehouse Command - 3D Chess",
    page_icon="♟️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }
        iframe {
            width: 100vw !important;
            height: 100vh !important;
            border: none !important;
            display: block !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

HTML_CODE = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
<title>Warehouse Command 3D Chess</title>
<style>
    * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; -webkit-user-select: none; }
    html, body {
        width: 100%; height: 100%; overflow: hidden;
        background: #0a0e17;
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        color: #f1f5f9;
    }
    #canvas-container {
        width: 100%; height: 100%;
        position: absolute; top: 0; left: 0; z-index: 1;
    }
    .hud-top {
        position: absolute; top: 12px; left: 12px; right: 12px; z-index: 10;
        display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between;
        gap: 10px;
        background: rgba(15, 23, 42, 0.86);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 12px;
        padding: 10px 16px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.45);
    }
    .brand { display: flex; align-items: center; gap: 10px; }
    .brand-title {
        font-size: 16px; font-weight: 800; letter-spacing: 0.5px;
        background: linear-gradient(90deg, #38bdf8, #fb923c);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .turn-badge {
        padding: 5px 12px; border-radius: 999px; font-size: 12px; font-weight: 700;
        letter-spacing: 0.4px; text-transform: uppercase;
        transition: all 0.25s ease;
    }
    .turn-blue {
        background: rgba(14, 165, 233, 0.22); color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.5);
    }
    .turn-orange {
        background: rgba(249, 115, 22, 0.22); color: #fb923c;
        border: 1px solid rgba(251, 146, 60, 0.5);
    }
    .hud-status {
        flex: 1; min-width: 200px; text-align: center;
        font-size: 13px; font-weight: 600; color: #e2e8f0;
        padding: 6px 12px; border-radius: 8px;
        background: rgba(30, 41, 59, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.15);
    }
    .hud-status.check-alert {
        background: rgba(220, 38, 38, 0.28);
        border-color: #ef4444; color: #fca5a5;
        animation: pulseCheck 1s infinite alternate;
    }
    .hud-status.mate-alert {
        background: rgba(234, 179, 8, 0.28);
        border-color: #facc15; color: #fde047;
    }
    @keyframes pulseCheck {
        from { transform: scale(1); }
        to { transform: scale(1.02); }
    }
    .controls { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
    .btn {
        background: rgba(30, 41, 59, 0.9);
        color: #e2e8f0;
        border: 1px solid rgba(148, 163, 184, 0.3);
        padding: 6px 11px; border-radius: 8px;
        font-size: 12px; font-weight: 600; cursor: pointer;
        transition: all 0.18s ease;
    }
    .btn:hover { background: rgba(51, 65, 85, 0.95); border-color: #38bdf8; }
    .btn.active { background: #0284c7; border-color: #38bdf8; color: #fff; }
    .btn-danger { background: rgba(185, 28, 28, 0.82); border-color: #f87171; }
    .btn-danger:hover { background: rgba(220, 38, 38, 0.95); }

    .hud-bottom {
        position: absolute; bottom: 12px; left: 12px; right: 12px; z-index: 10;
        display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center;
        gap: 8px; pointer-events: none;
    }
    .score-card {
        pointer-events: auto;
        background: rgba(15, 23, 42, 0.84);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(148, 163, 184, 0.2);
        padding: 8px 14px; border-radius: 10px;
        font-size: 12px; display: flex; gap: 14px; align-items: center;
    }
    .score-blue { color: #38bdf8; font-weight: 700; }
    .score-orange { color: #fb923c; font-weight: 700; }
    .hint-text { font-size: 11px; color: #94a3b8; }

    #gameover-modal {
        display: none;
        position: absolute; inset: 0; z-index: 30;
        background: rgba(2, 6, 23, 0.75);
        backdrop-filter: blur(6px);
        align-items: center; justify-content: center;
        padding: 20px;
    }
    .modal-box {
        background: linear-gradient(145deg, #0f172a, #1e293b);
        border: 1px solid rgba(56, 189, 248, 0.4);
        border-radius: 16px;
        padding: 28px 24px;
        max-width: 420px; width: 100%;
        text-align: center;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.65);
    }
    .modal-title { font-size: 22px; font-weight: 800; margin-bottom: 10px; color: #facc15; }
    .modal-sub { font-size: 14px; color: #cbd5e1; margin-bottom: 20px; line-height: 1.5; }
    @media (max-width: 640px) {
        .hud-top { padding: 8px 10px; gap: 6px; }
        .brand-title { font-size: 14px; }
        .hud-status { font-size: 12px; width: 100%; order: 3; }
        .btn { padding: 5px 8px; font-size: 11px; }
    }
</style>
</head>
<body>

<div id="canvas-container"></div>

<div class="hud-top">
    <div class="brand">
        <span class="brand-title">🏭 WAREHOUSE CHESS 3D</span>
        <span id="turn-indicator" class="turn-badge turn-blue">GILIRAN: TIM BIRU</span>
    </div>
    <div id="hud-msg" class="hud-status">
        Pilih staf atau unit logistik Tim Biru untuk memulai langkah.
    </div>
    <div class="controls">
        <button id="btn-ai" class="btn active" onclick="toggleAIMode()">🤖 vs AI: ON</button>
        <button class="btn" onclick="setCameraPreset('tactical')">📐 Taktis</button>
        <button class="btn" onclick="setCameraPreset('top')">🗺️ Atas</button>
        <button class="btn" onclick="setCameraPreset('closeup')">👤 Zoom Wajah Pekerja</button>
        <button class="btn btn-danger" onclick="resetGame()">🔄 Reset</button>
    </div>
</div>

<div class="hud-bottom">
    <div class="score-card">
        <span class="score-blue">TIM BIRU: <span id="blue-count">16</span> Unit</span>
        <span>|</span>
        <span class="score-orange">TIM ORANYE: <span id="orange-count">16</span> Unit</span>
    </div>
    <div class="score-card hint-text">
        Putar Kamera: Geser 1 Jari / Klik Kiri • Zoom: Cubit 2 Jari / Scroll • Animasi Berjalan & Aturan Catur FIDE Aktif
    </div>
</div>

<div id="gameover-modal">
    <div class="modal-box">
        <div id="modal-title" class="modal-title">🏆 SKAKMAT!</div>
        <div id="modal-desc" class="modal-sub">Permainan selesai.</div>
        <button class="btn active" style="padding:10px 20px;font-size:14px;" onclick="resetGame()">
            🔄 Main Lagi
        </button>
    </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>

<script>
// ============================================================================
// 1. INISIALISASI SCENE, KAMERA & PENCAHAYAAN PBR REALISTIS
// ============================================================================
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0b101b);
scene.fog = new THREE.FogExp2(0x0b101b, 0.025);

const camera = new THREE.PerspectiveCamera(40, window.innerWidth / window.innerHeight, 0.08, 100);
camera.position.set(0, 6.8, -7.4);

const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputEncoding = THREE.sRGBEncoding;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.12;
container.appendChild(renderer.domElement);

const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.target.set(0, 0.45, 0);
controls.enableDamping = true;
controls.dampingFactor = 0.07;
controls.maxPolarAngle = Math.PI * 0.485;
controls.minDistance = 0.8;
controls.maxDistance = 18;
controls.update();

const hemiLight = new THREE.HemisphereLight(0xf8fafc, 0x1e293b, 0.90);
hemiLight.position.set(0, 15, 0);
scene.add(hemiLight);

const keyLight = new THREE.DirectionalLight(0xfff5ea, 1.15);
keyLight.position.set(5, 11, -6);
keyLight.castShadow = true;
keyLight.shadow.mapSize.width = 2048;
keyLight.shadow.mapSize.height = 2048;
keyLight.shadow.bias = -0.0005;
scene.add(keyLight);

const rimLight = new THREE.DirectionalLight(0x93c5fd, 0.50);
rimLight.position.set(-6, 6, 7);
scene.add(rimLight);

const frontFill = new THREE.DirectionalLight(0xfffbeb, 0.45);
frontFill.position.set(0, 2.5, -8);
scene.add(frontFill);

// Koordinat Papan Catur 8x8
const TILE_SIZE = 1.0;
function gridToWorld(gx, gz) {
    return { x: (gx - 3.5) * TILE_SIZE, z: (gz - 3.5) * TILE_SIZE };
}
function inBounds(gx, gz) {
    return gx >= 0 && gx < 8 && gz >= 0 && gz < 8;
}

const boardGroup = new THREE.Group();
scene.add(boardGroup);

const warehouseFloor = new THREE.Mesh(
    new THREE.PlaneGeometry(32, 32),
    new THREE.MeshStandardMaterial({ color: 0x161d2a, roughness: 0.88, metalness: 0.08 })
);
warehouseFloor.rotation.x = -Math.PI / 2;
warehouseFloor.position.y = -0.02;
warehouseFloor.receiveShadow = true;
scene.add(warehouseFloor);

const borderMesh = new THREE.Mesh(
    new THREE.BoxGeometry(8.44, 0.08, 8.44),
    new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.7, metalness: 0.2 })
);
borderMesh.position.y = -0.03;
borderMesh.receiveShadow = true;
boardGroup.add(borderMesh);

const tileMeshes = [];
for (let gx = 0; gx < 8; gx++) {
    for (let gz = 0; gz < 8; gz++) {
        const isLight = (gx + gz) % 2 === 0;
        const baseColor = isLight ? 0x3b4758 : 0x1e2633;
        const tile = new THREE.Mesh(
            new THREE.BoxGeometry(TILE_SIZE * 0.985, 0.06, TILE_SIZE * 0.985),
            new THREE.MeshStandardMaterial({ color: baseColor, roughness: 0.75, metalness: 0.1 })
        );
        const pos = gridToWorld(gx, gz);
        tile.position.set(pos.x, 0, pos.z);
        tile.receiveShadow = true;
        tile.userData = { isTile: true, gridX: gx, gridZ: gz, baseColor };
        boardGroup.add(tile);
        tileMeshes.push(tile);
    }
}

// ============================================================================
// 2. SISTEM DNA KARAKTER MANUSIA UNIK (WAJAH & POSTUR BERBEDA TIAP INDIVIDU)
// ============================================================================
let workerIdCounter = 0;

const SKIN_PALETTES = [
    { base: [238, 196, 170], shadow: [192, 142, 114], high: [252, 224, 206], lip: [186, 108, 98], hex: 0xeec4aa },
    { base: [226, 178, 144], shadow: [178, 128, 96],  high: [244, 206, 178], lip: [174, 96, 86],  hex: 0xe2b290 },
    { base: [210, 156, 118], shadow: [162, 110, 78],  high: [230, 184, 150], lip: [160, 84, 74],  hex: 0xd29c76 },
    { base: [192, 134, 96],  shadow: [144, 90, 60],   high: [214, 162, 126], lip: [146, 72, 62],  hex: 0xc08660 },
    { base: [166, 110, 74],  shadow: [120, 72, 46],   high: [190, 138, 100], lip: [128, 60, 52],  hex: 0xa66e4a },
    { base: [138, 88, 56],   shadow: [96, 56, 34],    high: [162, 112, 78],  lip: [108, 50, 44],  hex: 0x8a5838 },
    { base: [108, 66, 42],   shadow: [72, 42, 24],    high: [134, 88, 60],   lip: [88, 42, 38],   hex: 0x6c422a },
    { base: [218, 170, 140], shadow: [168, 120, 94],  high: [238, 198, 172], lip: [168, 92, 84],  hex: 0xdaaa8c }
];

const HAIR_PALETTES = [
    { css: '#161311', hex: 0x161311 },
    { css: '#261d16', hex: 0x261d16 },
    { css: '#3b2819', hex: 0x3b2819 },
    { css: '#543924', hex: 0x543924 },
    { css: '#2f2d2c', hex: 0x2f2d2c },
    { css: '#646260', hex: 0x646260 }
];

const IRIS_PALETTES = [
    '#2b1d0e', '#473018', '#171717', '#3b4b35', '#2c3d4f'
];

function createSeededRandom(seed) {
    let s = (seed * 9301 + 49297) % 233280;
    return function () {
        s = (s * 9301 + 49297) % 233280;
        return s / 233280;
    };
}

function gauss(x, mu, sigma) {
    const d = (x - mu) / sigma;
    return Math.exp(-0.5 * d * d);
}

function generateWorkerDNA(o) {
    workerIdCounter++;
    const seed = (o && typeof o.seed === 'number')
        ? o.seed
        : workerIdCounter * 59 + (o && o.team === 'blue' ? 23 : 101);
    const rand = createSeededRandom(seed);
    const range = (min, max) => min + rand() * (max - min);

    const skin = SKIN_PALETTES[(workerIdCounter + Math.floor(rand() * 3)) % SKIN_PALETTES.length];
    const hair = HAIR_PALETTES[(workerIdCounter + Math.floor(rand() * 2)) % HAIR_PALETTES.length];
    const iris = IRIS_PALETTES[workerIdCounter % IRIS_PALETTES.length];

    return {
        id: workerIdCounter,
        skin,
        hair,
        iris,
        heightScale: range(0.95, 1.06),
        shoulderWidth: range(0.94, 1.10),
        torsoBulk: range(0.92, 1.12),
        headWidth: range(0.94, 1.07),
        headLength: range(0.95, 1.06),
        jawWidth: range(0.88, 1.16),
        chinWidth: range(0.90, 1.12),
        noseLength: range(0.92, 1.12),
        noseWidth: range(0.90, 1.14),
        mouthWidth: range(0.90, 1.12),
        lipFullness: range(0.90, 1.16),
        eyeSpacing: range(0.31, 0.36), // dalam radian lon
        eyeSlant: range(-0.06, 0.06),
        browThickness: range(0.85, 1.30),
        browAngle: range(-0.10, 0.12),
        // 0 = bersih, 1 = stubble halus, 2 = kumis, 3 = goatee, 4 = brewok rahang rapi
        facialHairType: workerIdCounter % 5
    };
}

// ============================================================================
// 3. TEKSTUR WAJAH SFERIS AKURAT 1024x1024 (TERUJI 100% MENGHADAP DEPAN -Z)
// ============================================================================
function createRealisticFaceTexture(dna) {
    const size = 1024;
    const canvas = document.createElement('canvas');
    canvas.width = size;
    canvas.height = size;
    const ctx = canvas.getContext('2d');

    const [rB, gB, bB] = dna.skin.base;
    const [rS, gS, bS] = dna.skin.shadow;
    const [rH, gH, bH] = dna.skin.high;
    const [rL, gL, bL] = dna.skin.lip;

    // 1. Gradasi Dasar Kulit Manusia
    const bgGrad = ctx.createLinearGradient(0, 0, 0, size);
    bgGrad.addColorStop(0.00, `rgb(${rH},${gH},${bH})`);
    bgGrad.addColorStop(0.48, `rgb(${rB},${gB},${bB})`);
    bgGrad.addColorStop(0.82, `rgb(${Math.round((rB+rS)/2)},${Math.round((gB+gS)/2)},${Math.round((bB+bS)/2)})`);
    bgGrad.addColorStop(1.00, `rgb(${rS},${gS},${bS})`);
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, size, size);

    // Pemetaan Eksak dari Koordinat Sferis 3D (lon, ny) ke Piksel Canvas (px, py)
    // untuk SphereGeometry(1, 64, 48, Math.PI * 0.5, Math.PI * 2, 0, Math.PI):
    // Wajah depan (-Z) berada tepat di lon = 0 -> u = 0.5 -> px = 512!
    function toPx(lon, ny) {
        const nyClamped = Math.max(-0.999, Math.min(0.999, ny));
        const u = 0.5 - lon / (2.0 * Math.PI);
        const py = (Math.acos(nyClamped) / Math.PI) * size;
        return [u * size, py];
    }

    function softGlow(lon, ny, rxPx, ryPx, colorStr) {
        const [px, py] = toPx(lon, ny);
        ctx.save();
        ctx.translate(px, py);
        ctx.scale(rxPx, ryPx);
        const g = ctx.createRadialGradient(0, 0, 0, 0, 0, 1);
        g.addColorStop(0, colorStr);
        g.addColorStop(1, 'rgba(0,0,0,0)');
        ctx.fillStyle = g;
        ctx.beginPath();
        ctx.arc(0, 0, 1, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }

    // 2. Rona Pipi, Dahi, Hidung & Bayangan Rongga Mata Alami
    softGlow(-0.42, -0.08, 48, 42, 'rgba(198, 78, 68, 0.16)');
    softGlow( 0.42, -0.08, 48, 42, 'rgba(198, 78, 68, 0.16)');
    softGlow( 0.00, -0.15, 28, 26, 'rgba(198, 72, 62, 0.18)');
    softGlow( 0.00,  0.34, 75, 45, `rgba(${rH},${gH},${bH}, 0.45)`);
    softGlow(-dna.eyeSpacing, 0.07, 36, 28, `rgba(${rS-28},${gS-24},${bS-20}, 0.45)`);
    softGlow( dna.eyeSpacing, 0.07, 36, 28, `rgba(${rS-28},${gS-24},${bS-20}, 0.45)`);

    // Garis Senyum Halus (Nasolabial Folds)
    ctx.strokeStyle = `rgba(${rS-35}, ${gS-28}, ${bS-22}, 0.30)`;
    ctx.lineWidth = 3.2;
    ctx.lineCap = 'round';
    [-1, 1].forEach(side => {
        const [x1, y1] = toPx(side * 0.16, -0.18);
        const [x2, y2] = toPx(side * 0.30, -0.29);
        const [x3, y3] = toPx(side * 0.25, -0.41);
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.quadraticCurveTo(x2, y2, x3, y3);
        ctx.stroke();
    });

    // Bayangan Batang Hidung, Philtrum & Lubang Hidung (ny = -0.19)
    softGlow(0.0, -0.28, 12, 18, `rgba(${rS-30},${gS-25},${bS-20}, 0.35)`);
    [-1, 1].forEach(side => {
        softGlow(side * 0.13, -0.04, 11, 44, `rgba(${rS-28},${gS-22},${bS-18}, 0.34)`);
        const [nx, ny] = toPx(side * 0.085 * dna.noseWidth, -0.20);
        ctx.save();
        ctx.translate(nx, ny);
        ctx.rotate(side * 0.32);
        ctx.fillStyle = 'rgba(36, 18, 14, 0.78)';
        ctx.beginPath();
        ctx.ellipse(0, 0, 7.5 * dna.noseWidth, 4.2, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    });

    // 3. MATA MANUSIA REALISTIS (ny = +0.06, lon = +/- dna.eyeSpacing)
    [-1, 1].forEach(side => {
        const [ex, ey] = toPx(side * dna.eyeSpacing, 0.06);
        const ew = 26;
        const eh = 13;

        ctx.save();
        ctx.translate(ex, ey);
        ctx.rotate(-side * dna.eyeSlant);

        // Lipatan kelopak mata atas
        ctx.strokeStyle = `rgba(${rS-48}, ${gS-40}, ${bS-34}, 0.68)`;
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.moveTo(-ew * 1.05, -eh * 0.30);
        ctx.quadraticCurveTo(0, -eh * 1.50, ew * 1.05, -eh * 0.20);
        ctx.stroke();

        // Bentuk Almond Mata
        ctx.save();
        ctx.beginPath();
        ctx.moveTo(-ew, 0);
        ctx.quadraticCurveTo(0, -eh * 1.15, ew, 0);
        ctx.quadraticCurveTo(0, eh * 0.95, -ew, 0);
        ctx.closePath();
        ctx.clip();

        // Sklera Putih Mata dengan Bayangan Atas
        const scGrad = ctx.createLinearGradient(0, -eh, 0, eh);
        scGrad.addColorStop(0.0, '#c8d0d8');
        scGrad.addColorStop(0.35, '#f8fafc');
        scGrad.addColorStop(1.0, '#e2e8f0');
        ctx.fillStyle = scGrad;
        ctx.fillRect(-ew, -eh, ew * 2, eh * 2);

        // Iris Berwarna & Cincin Limbal
        const irisR = 10.8;
        ctx.fillStyle = '#141210';
        ctx.beginPath();
        ctx.arc(0, -0.5, irisR, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = dna.iris;
        ctx.beginPath();
        ctx.arc(0, -0.5, irisR * 0.86, 0, Math.PI * 2);
        ctx.fill();

        // Serat Radial Iris
        ctx.strokeStyle = 'rgba(255, 235, 205, 0.20)';
        ctx.lineWidth = 1.0;
        for (let a = 0; a < 20; a++) {
            const ang = (a / 20) * Math.PI * 2;
            ctx.beginPath();
            ctx.moveTo(Math.cos(ang) * 3.2, -0.5 + Math.sin(ang) * 3.2);
            ctx.lineTo(Math.cos(ang) * (irisR * 0.82), -0.5 + Math.sin(ang) * (irisR * 0.82));
            ctx.stroke();
        }

        // Pupil & Catchlight
        ctx.fillStyle = '#050505';
        ctx.beginPath();
        ctx.arc(0, -0.5, 4.2, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = 'rgba(255, 255, 255, 0.94)';
        ctx.beginPath();
        ctx.arc(-3.0, -3.4, 2.2, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = 'rgba(255, 255, 255, 0.55)';
        ctx.beginPath();
        ctx.arc(2.8, 2.0, 1.1, 0, Math.PI * 2);
        ctx.fill();

        ctx.restore(); // End eye clip

        // Garis Bulu Mata Atas
        ctx.strokeStyle = '#120d0a';
        ctx.lineWidth = 3.2;
        ctx.beginPath();
        ctx.moveTo(-ew, 0.5);
        ctx.quadraticCurveTo(0, -eh * 1.15, ew, 0.5);
        ctx.stroke();

        // Garis Kelopak Bawah
        ctx.strokeStyle = `rgba(${rS-40}, ${gS-34}, ${bS-28}, 0.55)`;
        ctx.lineWidth = 1.6;
        ctx.beginPath();
        ctx.moveTo(-ew * 0.88, 1.0);
        ctx.quadraticCurveTo(0, eh * 0.95, ew * 0.88, 1.0);
        ctx.stroke();

        ctx.restore();

        // 4. ALIS SERAT RAMBUT (ny = +0.21)
        const [bx, by] = toPx(side * dna.eyeSpacing, 0.21);
        ctx.save();
        ctx.translate(bx, by);
        ctx.rotate(-side * dna.browAngle);
        ctx.strokeStyle = dna.hair.css;
        ctx.lineWidth = 2.2 * dna.browThickness;
        ctx.lineCap = 'round';
        for (let i = -16; i <= 16; i++) {
            const t = i / 16;
            const px = t * 29;
            const archY = -Math.sin((1 - Math.abs(t)) * Math.PI) * 6.5;
            ctx.beginPath();
            ctx.moveTo(px, archY + 3.8 * dna.browThickness);
            ctx.lineTo(px - side * 4.5, archY - 3.8 * dna.browThickness);
            ctx.stroke();
        }
        ctx.restore();
    });

    // 5. BIBIR & MULUT MANUSIA PROPORSIONAL (ny = -0.38)
    const [mx, my] = toPx(0.0, -0.38);
    const mw = 32 * dna.mouthWidth;
    const mh = 9.5 * dna.lipFullness;

    // Bibir Atas
    ctx.fillStyle = `rgba(${rL-10}, ${gL-10}, ${bL-8}, 0.88)`;
    ctx.beginPath();
    ctx.moveTo(mx - mw, my);
    ctx.quadraticCurveTo(mx - mw * 0.45, my - mh * 0.95, mx - 4.5, my - mh * 0.55);
    ctx.lineTo(mx, my - mh * 0.32);
    ctx.lineTo(mx + 4.5, my - mh * 0.55);
    ctx.quadraticCurveTo(mx + mw * 0.45, my - mh * 0.95, mx + mw, my);
    ctx.closePath();
    ctx.fill();

    // Bibir Bawah
    const lipGrad = ctx.createLinearGradient(0, my, 0, my + mh * 1.2);
    lipGrad.addColorStop(0.0, `rgba(${rL+10}, ${gL+5}, ${bL+5}, 0.90)`);
    lipGrad.addColorStop(0.55, `rgba(${rL+24}, ${gL+15}, ${bL+14}, 0.92)`);
    lipGrad.addColorStop(1.0, `rgba(${rS}, ${gS}, ${bS}, 0.35)`);
    ctx.fillStyle = lipGrad;
    ctx.beginPath();
    ctx.moveTo(mx - mw * 0.90, my);
    ctx.quadraticCurveTo(mx, my + mh * 1.22, mx + mw * 0.90, my);
    ctx.closePath();
    ctx.fill();

    // Garis Belahan Bibir
    ctx.strokeStyle = 'rgba(42, 18, 16, 0.80)';
    ctx.lineWidth = 2.4;
    ctx.beginPath();
    ctx.moveTo(mx - mw, my);
    ctx.quadraticCurveTo(mx - mw * 0.4, my + 1.2, mx, my - 0.4);
    ctx.quadraticCurveTo(mx + mw * 0.4, my + 1.2, mx + mw, my);
    ctx.stroke();

    // Cekungan Bawah Bibir (ny = -0.49)
    softGlow(0.0, -0.49, 24, 10, `rgba(${rS-35},${gS-28},${bS-22}, 0.38)`);

    // 6. RAMBUT BELAKANG, CAMBANG & VARIASI KUMIS/BREWOK SERAT HALUS
    ctx.fillStyle = dna.hair.css;
    const [, pyCrown] = toPx(0, 0.56);
    ctx.fillRect(0, 0, size, pyCrown);

    // Rambut bagian belakang kepala (|lon| > 1.15 rad)
    const [pxLeftBack] = toPx(1.15, 0);
    const [pxRightBack] = toPx(-1.15, 0);
    const [, pyNape] = toPx(0, -0.68);
    ctx.fillRect(0, 0, pxLeftBack, pyNape);
    ctx.fillRect(pxRightBack, 0, size - pxRightBack, pyNape);

    // Cambang di depan telinga
    const [sbL1, sbY1] = toPx(0.96, 0.16);
    const [sbL2, sbY2] = toPx(1.16, -0.20);
    ctx.fillRect(sbL2, sbY1, sbL1 - sbL2, sbY2 - sbY1);
    const [sbR1] = toPx(-0.96, 0.16);
    const [sbR2] = toPx(-1.16, -0.20);
    ctx.fillRect(sbR1, sbY1, sbR2 - sbR1, sbY2 - sbY1);

    // Kumis / Stubble / Goatee / Brewok
    if (dna.facialHairType > 0) {
        ctx.save();
        ctx.strokeStyle = dna.hair.css;
        ctx.globalAlpha = dna.facialHairType === 1 ? 0.25 : 0.70;
        ctx.lineWidth = dna.facialHairType === 1 ? 1.3 : 2.1;

        // Kumis di atas bibir (ny = -0.31)
        const [, mustY] = toPx(0.0, -0.31);
        for (let i = -24; i <= 24; i++) {
            if (Math.abs(i) < 2) continue;
            const hx = mx + i * 1.3 * dna.mouthWidth;
            const hy = mustY + Math.abs(i) * 0.15;
            ctx.beginPath();
            ctx.moveTo(hx, hy - 4);
            ctx.lineTo(hx + (i > 0 ? 2 : -2), hy + 4);
            ctx.stroke();
        }

        // Janggut Dagu (ny = -0.62)
        if (dna.facialHairType === 1 || dna.facialHairType === 3 || dna.facialHairType === 4) {
            const [, chinY] = toPx(0.0, -0.62);
            for (let i = -22; i <= 22; i++) {
                for (let j = -8; j <= 8; j++) {
                    if ((i * i) / 480 + (j * j) / 70 > 1) continue;
                    const hx = mx + i * 1.5;
                    const hy = chinY + j * 2.0;
                    ctx.beginPath();
                    ctx.moveTo(hx, hy);
                    ctx.lineTo(hx, hy + 4.5);
                    ctx.stroke();
                }
            }
        }

        // Brewok Rahang Samping (untuk tipe 1 stubble atau tipe 4 full beard)
        if (dna.facialHairType === 1 || dna.facialHairType === 4) {
            ctx.globalAlpha = dna.facialHairType === 1 ? 0.20 : 0.52;
            [-1, 1].forEach(side => {
                for (let step = 0; step < 36; step++) {
                    const t = step / 36;
                    const [bx, by] = toPx(side * (0.22 + t * 0.68), -0.60 + t * 0.36);
                    for (let k = -3; k <= 3; k++) {
                        ctx.beginPath();
                        ctx.moveTo(bx + k * 3, by - 3.5);
                        ctx.lineTo(bx + k * 3, by + 4.0);
                        ctx.stroke();
                    }
                }
            });
        }
        ctx.restore();
    }

    const tex = new THREE.CanvasTexture(canvas);
    tex.encoding = THREE.sRGBEncoding;
    tex.needsUpdate = true;
    return tex;
}

// ============================================================================
// 4. GEOMETRI KEPALA DARI NATIVE SPHEREGEOMETRY (100% ANTI-TERBALIK!)
// ============================================================================
function createSculptedHeadGeometry(dna) {
    // Menggunakan native THREE.SphereGeometry dengan phiStart = Math.PI * 0.5
    // sehingga normal permukaan 100% menghadap ke luar (FrontSide) dan u=0.5 tepat di wajah depan (-Z)!
    const geom = new THREE.SphereGeometry(1, 64, 48, Math.PI * 0.5, Math.PI * 2, 0, Math.PI);
    const pos = geom.attributes.position;

    const hw = 0.058 * dna.headWidth;
    const hl = 0.075 * dna.headLength;
    const hd = 0.065;

    for (let i = 0; i < pos.count; i++) {
        const nx = pos.getX(i);
        const ny = pos.getY(i);
        const nz = pos.getZ(i); // nz < 0 adalah wajah depan (-Z)

        const lon = Math.atan2(nx, -nz);
        const frontW = Math.max(0.0, -nz);

        // Kontur rahang manusia proporsional (TIDAK meruncing seperti kerucut!)
        const jawFullness = gauss(ny, -0.38, 0.26) * 0.08 * dna.jawWidth;
        const templeIn = gauss(ny, 0.16, 0.22) * (-0.03);
        const chinRound = ny < -0.65 ? (1.0 - 0.08 * Math.pow((-ny - 0.65) / 0.35, 2)) : 1.0;

        let x = nx * hw * (1.0 + jawFullness + templeIn) * chinRound;
        let y = ny * hl;
        let z = nz * hd;

        // Majukan sedikit dagu depan & dahi agar profil samping tegak manusiawi
        if (nz < 0) {
            const chinProj = gauss(ny, -0.62, 0.22) * gauss(lon, 0.0, 0.55) * 0.009;
            const browLift = gauss(ny, 0.21, 0.08) * gauss(lon, 0.0, 0.55) * 0.004;
            const eyeSocket = gauss(ny, 0.06, 0.08) * gauss(Math.abs(lon), dna.eyeSpacing, 0.13) * 0.0045;
            z -= (chinProj + browLift - eyeSocket) * frontW;

            // Pahatan Hidung 3D المulus di tengah wajah (ny = +0.06 s/d -0.20)
            const noseBridge = gauss(ny, -0.04, 0.13) * gauss(lon, 0.0, 0.11 * dna.noseWidth) * 0.011 * dna.noseLength;
            const noseTip = gauss(ny, -0.18, 0.065) * gauss(lon, 0.0, 0.095 * dna.noseWidth) * 0.015 * dna.noseLength;
            const nostril = gauss(ny, -0.19, 0.05) * gauss(Math.abs(lon), 0.11 * dna.noseWidth, 0.05) * 0.005;
            z -= (noseBridge + noseTip + nostril) * frontW;

            // Pahatan Bibir Halus (ny = -0.38)
            const mouthW = gauss(lon, 0.0, 0.22 * dna.mouthWidth);
            const upperLip = gauss(ny, -0.35, 0.04) * mouthW * 0.0038 * dna.lipFullness;
            const lowerLip = gauss(ny, -0.42, 0.045) * mouthW * 0.0042 * dna.lipFullness;
            z -= (upperLip + lowerLip) * frontW;
        }

        // Daun Telinga 3D Kiri & Kanan
        const earLon = gauss(Math.abs(lon), Math.PI * 0.50, 0.10);
        const earLat = gauss(ny, -0.02, 0.16);
        x += (nx > 0 ? 1 : -1) * earLon * earLat * 0.009;

        pos.setXYZ(i, x, y, z);
    }

    geom.computeVertexNormals();
    return geom;
}

// ============================================================================
// 5. TORSO & SERAGam KERJA DARI NATIVE CYLINDER/SPHERE (ANTI-TERBALIK!)
// ============================================================================
function createUniformTexture(team) {
    const size = 512;
    const canvas = document.createElement('canvas');
    canvas.width = size;
    canvas.height = size;
    const ctx = canvas.getContext('2d');

    // Kemeja Kerja Gelap di Bawah Rompi
    const shirtColor = team === 'blue' ? '#17253b' : '#262322';
    ctx.fillStyle = shirtColor;
    ctx.fillRect(0, 0, size, size);

    // Rompi Safety High-Vis (di bagian tengah badan, dengan bukaan resleting depan di u = 0.5)
    const vestColor = team === 'blue' ? '#0284c7' : '#ea580c';
    ctx.fillStyle = vestColor;
    ctx.fillRect(0, size * 0.16, size * 0.46, size * 0.70);
    ctx.fillRect(size * 0.54, size * 0.16, size * 0.46, size * 0.70);

    // List Hitam Rompi & Kerah V-Neck
    ctx.strokeStyle = '#0f172a';
    ctx.lineWidth = 7;
    ctx.strokeRect(4, size * 0.16, size * 0.455, size * 0.70);
    ctx.strokeRect(size * 0.54, size * 0.16, size * 0.455, size * 0.70);

    // Pita Reflektif Perak 3M Horizontal & Vertikal
    ctx.fillStyle = '#e2e8f0';
    ctx.fillRect(0, size * 0.48, size * 0.455, 16);
    ctx.fillRect(size * 0.545, size * 0.48, size * 0.455, 16);
    ctx.fillRect(0, size * 0.66, size * 0.455, 16);
    ctx.fillRect(size * 0.545, size * 0.66, size * 0.455, 16);
    ctx.fillRect(size * 0.36, size * 0.16, 14, size * 0.32);
    ctx.fillRect(size * 0.61, size * 0.16, 14, size * 0.32);

    // ID Badge di Dada
    ctx.fillStyle = '#f8fafc';
    ctx.fillRect(size * 0.57, size * 0.28, 24, 34);
    ctx.fillStyle = '#0284c7';
    ctx.fillRect(size * 0.57, size * 0.28, 24, 8);

    // Sabuk Kerja Hitam & Gesper
    ctx.fillStyle = '#111318';
    ctx.fillRect(0, size * 0.86, size, size * 0.14);
    ctx.fillStyle = '#94a3b8';
    ctx.fillRect(size * 0.47, size * 0.88, size * 0.06, size * 0.09);

    const tex = new THREE.CanvasTexture(canvas);
    tex.encoding = THREE.sRGBEncoding;
    tex.needsUpdate = true;
    return tex;
}

function createAnatomicalTorsoGeometry(dna) {
    // Menggunakan native THREE.SphereGeometry(1, 48, 32) yang dimodifikasi ke bentuk torso V-taper manusia
    // sehingga tidak ada tutup kaleng datar DAN 100% menghadap ke luar (tidak pernah inside-out!)
    const geom = new THREE.SphereGeometry(1, 48, 32, Math.PI * 0.5, Math.PI * 2, 0, Math.PI);
    const pos = geom.attributes.position;
    const bw = dna.shoulderWidth;
    const tb = dna.torsoBulk;

    for (let i = 0; i < pos.count; i++) {
        const nx = pos.getX(i);
        const ny = pos.getY(i); // -1 (pinggul) s/d +1 (bahu/kerah leher)
        const nz = pos.getZ(i);

        // Profil lebar dada V-taper (ramping di pinggang, bidang di dada/bahu, melengkung mulus ke leher)
        let rx, rz;
        if (ny > 0.65) {
            const t = (ny - 0.65) / 0.35;
            rx = (0.128 * (1 - t) + 0.042 * t) * bw;
            rz = (0.072 * (1 - t) + 0.040 * t) * tb;
        } else if (ny >= 0.0) {
            const t = ny / 0.65;
            rx = (0.094 * (1 - t) + 0.128 * t) * bw;
            rz = (0.064 * (1 - t) + 0.074 * t) * tb;
        } else {
            const t = -ny;
            rx = (0.094 * (1 - t * 0.5) + 0.096 * (t * 0.5)) * tb;
            rz = 0.064 * tb;
        }

        // Ratakan sedikit bagian atas & bawah agar menyambung mulus dengan panggul & leher
        const y = ny * 0.21;
        const lon = Math.atan2(nx, -nz);
        const squareFactor = 1.0 + 0.06 * Math.cos(2.0 * lon) * (1.0 - Math.abs(ny));
        const x = Math.sin(lon) * rx * squareFactor;
        const z = -Math.cos(lon) * rz * squareFactor;

        pos.setXYZ(i, x, y, z);
    }

    geom.computeVertexNormals();
    return geom;
}

// ============================================================================
// 6. PERAKITAN PEKERJA REALISTIS DENGAN RIG SENDI BERJALAN (buildHuman)
// ============================================================================
const cardboardMat = new THREE.MeshStandardMaterial({ color: 0xc49a6c, roughness: 0.85 });
const tapeMat = new THREE.MeshStandardMaterial({ color: 0xe5dccb, roughness: 0.6 });

function buildCardboardBox() {
    const boxGroup = new THREE.Group();
    const box = new THREE.Mesh(new THREE.BoxGeometry(0.20, 0.145, 0.165), cardboardMat);
    box.castShadow = true;
    boxGroup.add(box);

    const tape = new THREE.Mesh(new THREE.BoxGeometry(0.202, 0.008, 0.035), tapeMat);
    tape.position.y = 0.070;
    boxGroup.add(tape);

    const label = new THREE.Mesh(
        new THREE.PlaneGeometry(0.062, 0.030),
        new THREE.MeshBasicMaterial({ color: 0xf8fafc })
    );
    label.position.set(-0.035, 0.01, -0.084);
    label.rotation.y = Math.PI;
    boxGroup.add(label);
    return boxGroup;
}

function createTaperedLimbMesh(rTop, rBot, length, mat) {
    // Silinder diperhalus dengan ujung bulat yang titik putarnya (pivot) berada di sendi atas (y = 0)
    const group = new THREE.Group();
    const cylGeom = new THREE.CylinderGeometry(rTop, rBot, length, 18, 1, false);
    cylGeom.translate(0, -length * 0.5, 0);
    const cylMesh = new THREE.Mesh(cylGeom, mat);
    cylMesh.castShadow = true;
    cylMesh.receiveShadow = true;
    group.add(cylMesh);

    const capGeom = new THREE.SphereGeometry(rTop * 0.99, 16, 12);
    const capMesh = new THREE.Mesh(capGeom, mat);
    capMesh.castShadow = true;
    group.add(capMesh);
    return group;
}

function buildHuman(o = {}) {
    const group = new THREE.Group();
    const team = o.team || 'blue';
    const role = o.role || 'pawn';
    const dna = generateWorkerDNA(o);

    const skinMat = new THREE.MeshStandardMaterial({
        color: dna.skin.hex,
        roughness: 0.58,
        metalness: 0.03
    });
    const shirtColorHex = team === 'blue' ? 0x17253b : 0x262322;
    const sleeveMat = new THREE.MeshStandardMaterial({
        color: shirtColorHex,
        roughness: 0.78,
        metalness: 0.04
    });
    const pantsMat = new THREE.MeshStandardMaterial({
        color: 0x1e2532,
        roughness: 0.84,
        metalness: 0.04
    });
    const bootMat = new THREE.MeshStandardMaterial({
        color: 0x1b1512,
        roughness: 0.52,
        metalness: 0.08
    });

    const bw = dna.shoulderWidth;
    const tb = dna.torsoBulk;

    // 1. ROOT PELVIS (Pinggul tempat kaki & badan berporos saat berjalan)
    const pelvisGroup = new THREE.Group();
    pelvisGroup.position.y = 0.44;
    group.add(pelvisGroup);

    const pelvisGeom = new THREE.SphereGeometry(1, 24, 16);
    pelvisGeom.scale(0.094 * tb, 0.068, 0.064 * tb);
    const pelvisMesh = new THREE.Mesh(pelvisGeom, pantsMat);
    pelvisMesh.castShadow = true;
    pelvisGroup.add(pelvisMesh);

    // 2. TORSO ANATOMIS + LEHER + KEPALA PAHAT
    const chestGroup = new THREE.Group();
    chestGroup.position.y = 0.18;
    pelvisGroup.add(chestGroup);

    const torsoMat = new THREE.MeshStandardMaterial({
        map: createUniformTexture(team),
        roughness: 0.75,
        metalness: 0.04
    });
    const torsoMesh = new THREE.Mesh(createAnatomicalTorsoGeometry(dna), torsoMat);
    torsoMesh.castShadow = true;
    torsoMesh.receiveShadow = true;
    chestGroup.add(torsoMesh);

    // Leher Anatomis
    const neckGeom = new THREE.CylinderGeometry(0.034 * dna.headWidth, 0.041 * bw, 0.09, 20);
    const neckMesh = new THREE.Mesh(neckGeom, skinMat);
    neckMesh.position.set(0, 0.21, 0.004);
    neckMesh.castShadow = true;
    chestGroup.add(neckMesh);

    // Kepala Pahat + Wajah Sferis 1024x1024
    const headGroup = new THREE.Group();
    headGroup.position.set(0, 0.295, -0.004);
    chestGroup.add(headGroup);

    const faceTex = createRealisticFaceTexture(dna);
    const headMat = new THREE.MeshStandardMaterial({
        map: faceTex,
        roughness: 0.56,
        metalness: 0.03
    });
    const headMesh = new THREE.Mesh(createSculptedHeadGeometry(dna), headMat);
    headMesh.castShadow = true;
    headMesh.receiveShadow = true;
    headGroup.add(headMesh);

    // Helm Proyek Keselamatan (Terletak di atas kubah kepala agar alis & mata terlihat 100% jelas)
    const helmetGroup = new THREE.Group();
    helmetGroup.position.set(0, 0.038, 0.002);
    helmetGroup.rotation.x = -0.08;
    const helmetColor = role === 'supervisor'
        ? 0xfacc15
        : (team === 'blue' ? 0x0ea5e9 : 0xf97316);
    const helmetMat = new THREE.MeshStandardMaterial({
        color: helmetColor,
        roughness: 0.30,
        metalness: 0.12
    });

    const domeGeom = new THREE.SphereGeometry(0.062 * dna.headWidth, 28, 20, 0, Math.PI * 2, 0, Math.PI * 0.46);
    domeGeom.scale(1.02, 0.92, 1.12);
    const domeMesh = new THREE.Mesh(domeGeom, helmetMat);
    domeMesh.castShadow = true;
    helmetGroup.add(domeMesh);

    const ridgeMesh = new THREE.Mesh(new THREE.BoxGeometry(0.018, 0.014, 0.11), helmetMat);
    ridgeMesh.position.set(0, 0.052, 0.0);
    helmetGroup.add(ridgeMesh);

    const brimGeom = new THREE.CylinderGeometry(0.062 * dna.headWidth, 0.069 * dna.headWidth, 0.006, 24, 1, false, Math.PI * 0.72, Math.PI * 0.56);
    brimGeom.scale(1.0, 1.0, 1.22);
    const brimMesh = new THREE.Mesh(brimGeom, helmetMat);
    brimMesh.position.set(0, 0.004, -0.015);
    helmetGroup.add(brimMesh);
    headGroup.add(helmetGroup);

    // 3. LENGAN BERPOROS (Bahu -> Lengan Atas -> Siku -> Lengan Bawah -> Tangan)
    const leftShoulder = new THREE.Group();
    const rightShoulder = new THREE.Group();
    leftShoulder.position.set(-0.116 * bw, 0.12, 0);
    rightShoulder.position.set( 0.116 * bw, 0.12, 0);
    chestGroup.add(leftShoulder);
    chestGroup.add(rightShoulder);

    const leftElbow = new THREE.Group();
    const rightElbow = new THREE.Group();
    leftElbow.position.set(0, -0.125, 0);
    rightElbow.position.set(0, -0.125, 0);

    [[leftShoulder, leftElbow, -1], [rightShoulder, rightElbow, 1]].forEach(([shGroup, elGroup, side]) => {
        // Lengan kemeja atas (Deltoid sleeve yang menyatu ke bahu)
        const upperSleeve = createTaperedLimbMesh(0.033 * bw, 0.027, 0.125, sleeveMat);
        shGroup.add(upperSleeve);
        shGroup.add(elGroup);

        // Lengan bawah kulit (Forearm)
        const forearm = createTaperedLimbMesh(0.025, 0.019, 0.12, skinMat);
        elGroup.add(forearm);

        // Telapak tangan & jari
        const handGeom = new THREE.SphereGeometry(1, 14, 12);
        handGeom.scale(0.016, 0.024, 0.011);
        const handMesh = new THREE.Mesh(handGeom, skinMat);
        handMesh.position.set(0, -0.13, -0.004);
        handMesh.castShadow = true;
        elGroup.add(handMesh);
    });

    // Atur pose lengan sesuai peran (Pawn memegang kardus, Supervisor memegang tablet)
    if (role === 'pawn') {
        leftShoulder.rotation.set(0.45, 0, -0.12);
        rightShoulder.rotation.set(0.45, 0, 0.12);
        leftElbow.rotation.set(0.85, 0, 0.22);
        rightElbow.rotation.set(0.85, 0, -0.22);

        const boxProp = buildCardboardBox();
        boxProp.position.set(0, -0.04, -0.17);
        chestGroup.add(boxProp);
    } else if (role === 'supervisor') {
        leftShoulder.rotation.set(0.06, 0, 0.06);
        leftElbow.rotation.set(0.18, 0, 0);
        rightShoulder.rotation.set(0.38, 0, -0.10);
        rightElbow.rotation.set(0.82, 0, -0.18);

        const tablet = new THREE.Mesh(
            new THREE.BoxGeometry(0.012, 0.085, 0.062),
            new THREE.MeshStandardMaterial({ color: 0x0f172a, emissive: 0x0284c7, emissiveIntensity: 0.45, roughness: 0.2 })
        );
        tablet.position.set(-0.02, -0.13, -0.03);
        tablet.rotation.set(0.4, 0.2, 0);
        rightElbow.add(tablet);
    } else {
        leftShoulder.rotation.set(0.05, 0, 0.05);
        rightShoulder.rotation.set(0.05, 0, -0.05);
        leftElbow.rotation.set(0.16, 0, 0);
        rightElbow.rotation.set(0.16, 0, 0);
    }

    // 4. KAKI BERPOROS UNTUK ANIMASI BERJALAN (Pinggul -> Paha -> Lutut -> Betis -> Sepatu)
    const leftHip = new THREE.Group();
    const rightHip = new THREE.Group();
    leftHip.position.set(-0.048 * tb, -0.01, 0);
    rightHip.position.set( 0.048 * tb, -0.01, 0);
    pelvisGroup.add(leftHip);
    pelvisGroup.add(rightHip);

    const leftKnee = new THREE.Group();
    const rightKnee = new THREE.Group();
    leftKnee.position.set(0, -0.20, 0);
    rightKnee.position.set(0, -0.20, 0);

    [[leftHip, leftKnee], [rightHip, rightKnee]].forEach(([hipGroup, kneeGroup]) => {
        const thigh = createTaperedLimbMesh(0.046 * tb, 0.036, 0.20, pantsMat);
        hipGroup.add(thigh);
        hipGroup.add(kneeGroup);

        const calf = createTaperedLimbMesh(0.035, 0.028, 0.19, pantsMat);
        kneeGroup.add(calf);

        const bootGeom = new THREE.SphereGeometry(1, 16, 12);
        bootGeom.scale(0.033, 0.025, 0.058);
        const bootMesh = new THREE.Mesh(bootGeom, bootMat);
        bootMesh.position.set(0, -0.20, -0.018);
        bootMesh.castShadow = true;
        kneeGroup.add(bootMesh);
    });

    group.scale.set(dna.heightScale, dna.heightScale, dna.heightScale);
    group.userData.dna = dna;
    group.userData.head = headGroup;
    group.userData.rig = {
        role,
        pelvis: pelvisGroup,
        chest: chestGroup,
        head: headGroup,
        leftHip,
        rightHip,
        leftKnee,
        rightKnee,
        leftShoulder,
        rightShoulder,
        leftElbow,
        rightElbow,
        baseLeftShoulderX: leftShoulder.rotation.x,
        baseRightShoulderX: rightShoulder.rotation.x
    };
    return group;
}

// ============================================================================
// 7. PEMBUATAN UNIT CATUR GUDANG (MENYIMPAN REFERENSI RIG MANUSIA)
// ============================================================================
function createChessPieceMesh(type, team) {
    const root = new THREE.Group();
    const isBlue = team === 'blue';
    const teamColor = isBlue ? 0x0ea5e9 : 0xf97316;
    const metalMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.4, metalness: 0.6 });
    const bodyMat = new THREE.MeshStandardMaterial({ color: teamColor, roughness: 0.45, metalness: 0.2 });

    const ringGeom = new THREE.RingGeometry(0.32, 0.37, 32);
    ringGeom.rotateX(-Math.PI / 2);
    const baseRing = new THREE.Mesh(
        ringGeom,
        new THREE.MeshBasicMaterial({ color: teamColor, side: THREE.DoubleSide, transparent: true, opacity: 0.65 })
    );
    baseRing.position.y = 0.005;
    root.add(baseRing);

    let humanActor = null;

    if (type === 'pawn') {
        humanActor = buildHuman({ team, role: 'pawn' });
        root.add(humanActor);
    } else if (type === 'bishop') {
        humanActor = buildHuman({ team, role: 'supervisor' });
        root.add(humanActor);
    } else if (type === 'knight') {
        humanActor = buildHuman({ team, role: 'operator' });
        humanActor.position.z = 0.14;
        root.add(humanActor);

        const cart = new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.22, 0.24), bodyMat);
        cart.position.set(0, 0.14, -0.14);
        cart.castShadow = true;
        root.add(cart);

        const handle = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.014, 0.36, 12), metalMat);
        handle.position.set(0, 0.38, -0.02);
        root.add(handle);
    } else if (type === 'rook') {
        const truckBase = new THREE.Mesh(new THREE.BoxGeometry(0.54, 0.24, 0.54), bodyMat);
        truckBase.position.y = 0.15;
        truckBase.castShadow = true;
        root.add(truckBase);

        const cargoBox = buildCardboardBox();
        cargoBox.scale.set(1.5, 1.5, 1.5);
        cargoBox.position.set(0, 0.38, 0.08);
        root.add(cargoBox);

        humanActor = buildHuman({ team, role: 'operator' });
        humanActor.scale.multiplyScalar(0.90);
        humanActor.position.set(0, 0.10, -0.12);
        root.add(humanActor);
    } else if (type === 'queen') {
        const agvDeck = new THREE.Mesh(new THREE.CylinderGeometry(0.38, 0.40, 0.08, 28), metalMat);
        agvDeck.position.y = 0.04;
        root.add(agvDeck);

        humanActor = buildHuman({ team, role: 'supervisor' });
        humanActor.position.y = 0.06;
        root.add(humanActor);
    } else if (type === 'king') {
        const serverRack = new THREE.Mesh(
            new THREE.BoxGeometry(0.42, 1.02, 0.32),
            new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.3, metalness: 0.5 })
        );
        serverRack.position.set(-0.13, 0.52, 0.10);
        serverRack.castShadow = true;
        root.add(serverRack);

        const ledMat = new THREE.MeshBasicMaterial({ color: isBlue ? 0x38bdf8 : 0xf97316 });
        for (let i = 0; i < 4; i++) {
            const led = new THREE.Mesh(new THREE.BoxGeometry(0.26, 0.025, 0.02), ledMat);
            led.position.set(-0.13, 0.34 + i * 0.16, -0.07);
            root.add(led);
        }

        humanActor = buildHuman({ team, role: 'supervisor' });
        humanActor.position.set(0.15, 0, -0.06);
        root.add(humanActor);
    }

    root.rotation.y = isBlue ? Math.PI : 0;
    if (humanActor) {
        root.userData.head = humanActor.userData.head;
        root.userData.rig = humanActor.userData.rig;
    }
    return root;
}

// Fungsi untuk mengembalikan sendi kaki & tangan ke sikap berdiri tegak setelah selesai berjalan
function resetPieceWalkRig(piece) {
    const rig = piece && piece.userData ? piece.userData.rig : null;
    if (!rig) return;
    rig.pelvis.position.y = 0.44;
    rig.pelvis.rotation.set(0, 0, 0);
    rig.chest.rotation.set(0, 0, 0);
    rig.leftHip.rotation.set(0, 0, 0);
    rig.rightHip.rotation.set(0, 0, 0);
    rig.leftKnee.rotation.set(0, 0, 0);
    rig.rightKnee.rotation.set(0, 0, 0);
    rig.leftShoulder.rotation.x = rig.baseLeftShoulderX;
    rig.rightShoulder.rotation.x = rig.baseRightShoulderX;
}

// ============================================================================
// 8. STATE PERMAINAN & ATURAN CATUR FIDE LENGKAP (SKAK, SKAKMAT, STALEMATE)
// ============================================================================
const pieces = [];
let currentTurn = 'blue';
let selectedPiece = null;
let validMoves = [];
let isAnimating = false;
let isGameOver = false;
let vsAI = true;
let activeMoveAnim = null;
const particles = [];

function getPieceAt(gx, gz) {
    for (let i = 0; i < pieces.length; i++) {
        const p = pieces[i];
        if (p.userData.alive && p.userData.gridX === gx && p.userData.gridZ === gz) {
            return p;
        }
    }
    return null;
}

function spawnPiece(type, team, gx, gz) {
    const mesh = createChessPieceMesh(type, team);
    const pos = gridToWorld(gx, gz);
    mesh.position.set(pos.x, 0.03, pos.z);
    mesh.userData = Object.assign(mesh.userData || {}, {
        type, team, gridX: gx, gridZ: gz, alive: true, hasMoved: false
    });
    scene.add(mesh);
    pieces.push(mesh);
}

function initBoardPieces() {
    pieces.forEach(p => scene.remove(p));
    pieces.length = 0;
    workerIdCounter = 0;

    const backRank = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook'];
    for (let x = 0; x < 8; x++) {
        spawnPiece(backRank[x], 'blue', x, 0);
        spawnPiece('pawn', 'blue', x, 1);

        spawnPiece('pawn', 'orange', x, 6);
        spawnPiece(backRank[x], 'orange', x, 7);
    }
    updateScoreUI();
}

function getRawMoves(piece, includeCastling = true) {
    const valid = [];
    if (!piece || !piece.userData || !piece.userData.alive) return valid;

    const type = piece.userData.type;
    const team = piece.userData.team;
    const gx = piece.userData.gridX;
    const gz = piece.userData.gridZ;

    const isEnemy = (x, z) => {
        const target = getPieceAt(x, z);
        return target && target.userData.team !== team;
    };
    const isEmpty = (x, z) => !getPieceAt(x, z);

    if (type === 'pawn') {
        const dir = team === 'blue' ? 1 : -1;
        if (inBounds(gx, gz + dir) && isEmpty(gx, gz + dir)) {
            valid.push({ x: gx, z: gz + dir, attack: false });
            if (!piece.userData.hasMoved && inBounds(gx, gz + 2 * dir) && isEmpty(gx, gz + 2 * dir)) {
                valid.push({ x: gx, z: gz + 2 * dir, attack: false });
            }
        }
        [-1, 1].forEach(dx => {
            const nx = gx + dx, nz = gz + dir;
            if (inBounds(nx, nz) && isEnemy(nx, nz)) {
                valid.push({ x: nx, z: nz, attack: true, target: getPieceAt(nx, nz) });
            }
        });
    } else if (type === 'knight') {
        const jumps = [[1, 2], [2, 1], [-1, 2], [-2, 1], [1, -2], [2, -1], [-1, -2], [-2, -1]];
        jumps.forEach(([dx, dz]) => {
            const nx = gx + dx, nz = gz + dz;
            if (inBounds(nx, nz)) {
                if (isEmpty(nx, nz)) valid.push({ x: nx, z: nz, attack: false });
                else if (isEnemy(nx, nz)) valid.push({ x: nx, z: nz, attack: true, target: getPieceAt(nx, nz) });
            }
        });
    }

    if (type === 'rook' || type === 'queen') {
        const dirs = [[1, 0], [-1, 0], [0, 1], [0, -1]];
        dirs.forEach(([dx, dz]) => {
            let step = 1;
            while (inBounds(gx + dx * step, gz + dz * step)) {
                const nx = gx + dx * step, nz = gz + dz * step;
                if (isEmpty(nx, nz)) valid.push({ x: nx, z: nz, attack: false });
                else {
                    if (isEnemy(nx, nz)) valid.push({ x: nx, z: nz, attack: true, target: getPieceAt(nx, nz) });
                    break;
                }
                step++;
            }
        });
    }

    if (type === 'bishop' || type === 'queen') {
        const dirs = [[1, 1], [1, -1], [-1, 1], [-1, -1]];
        dirs.forEach(([dx, dz]) => {
            let step = 1;
            while (inBounds(gx + dx * step, gz + dz * step)) {
                const nx = gx + dx * step, nz = gz + dz * step;
                if (isEmpty(nx, nz)) valid.push({ x: nx, z: nz, attack: false });
                else {
                    if (isEnemy(nx, nz)) valid.push({ x: nx, z: nz, attack: true, target: getPieceAt(nx, nz) });
                    break;
                }
                step++;
            }
        });
    }

    if (type === 'king') {
        const dirs = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]];
        dirs.forEach(([dx, dz]) => {
            const nx = gx + dx, nz = gz + dz;
            if (inBounds(nx, nz)) {
                if (isEmpty(nx, nz)) valid.push({ x: nx, z: nz, attack: false });
                else if (isEnemy(nx, nz)) valid.push({ x: nx, z: nz, attack: true, target: getPieceAt(nx, nz) });
            }
        });

        if (includeCastling && !piece.userData.hasMoved && !isInCheck(team)) {
            const row = team === 'blue' ? 0 : 7;
            const rookK = getPieceAt(7, row);
            if (rookK && rookK.userData.type === 'rook' && !rookK.userData.hasMoved) {
                if (isEmpty(5, row) && isEmpty(6, row) && !isSquareAttacked(5, row, team) && !isSquareAttacked(6, row, team)) {
                    valid.push({ x: 6, z: row, attack: false, castlingRook: rookK, rookNewX: 5 });
                }
            }
            const rookQ = getPieceAt(0, row);
            if (rookQ && rookQ.userData.type === 'rook' && !rookQ.userData.hasMoved) {
                if (isEmpty(1, row) && isEmpty(2, row) && isEmpty(3, row) && !isSquareAttacked(3, row, team) && !isSquareAttacked(2, row, team)) {
                    valid.push({ x: 2, z: row, attack: false, castlingRook: rookQ, rookNewX: 3 });
                }
            }
        }
    }

    return valid;
}

function findKing(team) {
    return pieces.find(p => p.userData && p.userData.alive && p.userData.team === team && p.userData.type === 'king') || null;
}

function isSquareAttacked(tx, tz, defenderTeam) {
    const enemyTeam = defenderTeam === 'blue' ? 'orange' : 'blue';
    for (let i = 0; i < pieces.length; i++) {
        const p = pieces[i];
        if (!p.userData || !p.userData.alive || p.userData.team !== enemyTeam) continue;
        const raw = getRawMoves(p, false);
        for (let j = 0; j < raw.length; j++) {
            if (raw[j].x === tx && raw[j].z === tz) return true;
        }
    }
    return false;
}

function isInCheck(team) {
    const king = findKing(team);
    if (!king) return true;
    return isSquareAttacked(king.userData.gridX, king.userData.gridZ, team);
}

function wouldLeaveKingInCheck(piece, move) {
    const origX = piece.userData.gridX;
    const origZ = piece.userData.gridZ;
    const capturedTarget = (move.attack && move.target) ? move.target : getPieceAt(move.x, move.z);
    const origTargetAlive = capturedTarget ? capturedTarget.userData.alive : false;

    piece.userData.gridX = move.x;
    piece.userData.gridZ = move.z;
    if (capturedTarget && capturedTarget !== piece) {
        capturedTarget.userData.alive = false;
    }

    const inDanger = isInCheck(piece.userData.team);

    piece.userData.gridX = origX;
    piece.userData.gridZ = origZ;
    if (capturedTarget && capturedTarget !== piece) {
        capturedTarget.userData.alive = origTargetAlive;
    }

    return inDanger;
}

function getValidMoves(piece) {
    if (isGameOver || !piece || !piece.userData || !piece.userData.alive) return [];
    const raw = getRawMoves(piece, true);
    return raw.filter(mv => !wouldLeaveKingInCheck(piece, mv));
}

function getAllLegalMovesForTeam(team) {
    const allMoves = [];
    for (let i = 0; i < pieces.length; i++) {
        const p = pieces[i];
        if (p.userData && p.userData.alive && p.userData.team === team) {
            const moves = getValidMoves(p);
            moves.forEach(mv => allMoves.push({ piece: p, mv }));
        }
    }
    return allMoves;
}

function triggerExplosion(pos) {
    for (let i = 0; i < 18; i++) {
        const p = new THREE.Mesh(
            new THREE.BoxGeometry(0.08, 0.08, 0.08),
            new THREE.MeshBasicMaterial({ color: i % 2 === 0 ? 0xf97316 : 0xfacc15 })
        );
        p.position.copy(pos);
        p.position.y += 0.35;
        p.userData.vel = new THREE.Vector3(
            (Math.random() - 0.5) * 0.14,
            Math.random() * 0.14 + 0.04,
            (Math.random() - 0.5) * 0.14
        );
        p.userData.life = 28;
        scene.add(p);
        particles.push(p);
    }
}

function captureVictim(m) {
    if (m.captured || !m.mv.attack || !m.mv.target) return;
    m.captured = true;
    const v = m.mv.target;
    v.userData.alive = false;
    scene.remove(v);
    triggerExplosion(v.position);
    updateScoreUI();
}

function startMove(piece, mv) {
    isAnimating = true;
    clearTileHighlights();
    const targetPos = gridToWorld(mv.x, mv.z);
    const dx = targetPos.x - piece.position.x;
    const dz = targetPos.z - piece.position.z;
    const dist = Math.hypot(dx, dz) || 1;

    // Arahkan badan pekerja menghadap langsung ke arah petak tujuan saat berjalan
    // (karena wajah menghadap -Z lokal, sudut hadap ke (dx, dz) adalah Math.atan2(-dx, -dz))
    piece.rotation.y = Math.atan2(-dx, -dz);

    activeMoveAnim = {
        piece, mv,
        sx: piece.position.x, sz: piece.position.z,
        ex: targetPos.x, ez: targetPos.z,
        dist,
        speed: 0.032 / Math.max(0.65, Math.sqrt(dist * 0.5)),
        progress: 0, captured: false
    };
}

function finishMove(m) {
    const piece = m.piece, moveData = m.mv;
    piece.position.set(m.ex, 0.03, m.ez);
    piece.userData.gridX = moveData.x;
    piece.userData.gridZ = moveData.z;
    piece.userData.hasMoved = true;

    // Kembalikan sikap berdiri tegak & arah hadap ke tim lawan
    resetPieceWalkRig(piece);
    piece.rotation.y = piece.userData.team === 'blue' ? Math.PI : 0;

    if (moveData.castlingRook) {
        const r = moveData.castlingRook;
        const rPos = gridToWorld(moveData.rookNewX, moveData.z);
        r.position.set(rPos.x, 0.03, rPos.z);
        r.userData.gridX = moveData.rookNewX;
        r.userData.hasMoved = true;
    }

    if (moveData.attack && moveData.target) {
        captureVictim(m);
        if (moveData.target.userData.type === 'king') {
            endGame(`🏆 SKAKMAT! Tim ${currentTurn === 'blue' ? 'BIRU' : 'ORANYE'} Menang!`, `WMS Server lawan berhasil dikuasai sepenuhnya.`);
            isAnimating = false;
            return;
        }
    }

    if (piece.userData.type === 'pawn') {
        const promoRow = piece.userData.team === 'blue' ? 7 : 0;
        if (piece.userData.gridZ === promoRow) {
            const oldX = piece.userData.gridX;
            const oldZ = piece.userData.gridZ;
            const team = piece.userData.team;
            piece.userData.alive = false;
            scene.remove(piece);
            spawnPiece('queen', team, oldX, oldZ);
            updateHUD(`⭐ PROMOSI! Staf Logistik Tim ${team.toUpperCase()} naik pangkat menjadi Chief Supervisor (Queen)!`, '');
        }
    }

    const winnerLabel = currentTurn === 'blue' ? 'TIM BIRU' : 'TIM ORANYE';
    currentTurn = currentTurn === 'blue' ? 'orange' : 'blue';
    const nextLabel = currentTurn === 'blue' ? 'TIM BIRU' : 'TIM ORANYE';
    selectedPiece = null;
    validMoves = [];
    isAnimating = false;
    updateTurnBadge();

    const nextLegalMoves = getAllLegalMovesForTeam(currentTurn);
    const nextInCheck = isInCheck(currentTurn);
    highlightCheckedKing();

    if (nextLegalMoves.length === 0) {
        if (nextInCheck) {
            endGame(
                `🏆 SKAKMAT! ${winnerLabel} MENANG!`,
                `WMS Server ${nextLabel} sedang di-skak dan tidak memiliki langkah penyelamatan yang sah.`
            );
        } else {
            endGame(
                `🤝 REMIS (STALEMATE)!`,
                `${nextLabel} tidak sedang di-skak, tetapi tidak memiliki langkah sah yang tersisa.`
            );
        }
        return;
    }

    if (nextInCheck) {
        updateHUD(`⚠️ SKAK! WMS Server ${nextLabel} sedang terancam! Wajib diselamatkan!`, 'check-alert');
    } else {
        updateHUD(`Giliran ${nextLabel} melangkah.`, '');
    }

    if (!isGameOver && vsAI && currentTurn === 'orange') {
        setTimeout(runAIBot, 480);
    }
}

const PIECE_WEIGHT = { king: 1000, queen: 90, rook: 50, bishop: 32, knight: 30, pawn: 10 };
function runAIBot() {
    if (isGameOver || currentTurn !== 'orange' || isAnimating) return;
    const allMoves = getAllLegalMovesForTeam('orange');
    if (allMoves.length === 0) return;

    allMoves.sort((a, b) => {
        const scoreA = (a.mv.attack && a.mv.target ? PIECE_WEIGHT[a.mv.target.userData.type] || 10 : 0) + Math.random() * 4;
        const scoreB = (b.mv.attack && b.mv.target ? PIECE_WEIGHT[b.mv.target.userData.type] || 10 : 0) + Math.random() * 4;
        return scoreB - scoreA;
    });

    const chosen = allMoves[0];
    startMove(chosen.piece, chosen.mv);
}

// ============================================================================
// 9. INTERAKSI KLIK, KAMERA & ANIMASI BERJALAN MANUSIA (WALK CYCLE)
// ============================================================================
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

function clearTileHighlights() {
    tileMeshes.forEach(t => {
        t.material.color.setHex(t.userData.baseColor);
        t.material.emissive.setHex(0x000000);
    });
    highlightCheckedKing();
}

function highlightCheckedKing() {
    ['blue', 'orange'].forEach(tm => {
        if (isInCheck(tm)) {
            const k = findKing(tm);
            if (k) {
                const tile = tileMeshes.find(t => t.userData.gridX === k.userData.gridX && t.userData.gridZ === k.userData.gridZ);
                if (tile) {
                    tile.material.color.setHex(0xdc2626);
                    tile.material.emissive.setHex(0x7f1d1d);
                }
            }
        }
    });
}

function showValidMoveHighlights(piece, moves) {
    clearTileHighlights();
    const curTile = tileMeshes.find(t => t.userData.gridX === piece.userData.gridX && t.userData.gridZ === piece.userData.gridZ);
    if (curTile) curTile.material.color.setHex(0x0284c7);

    moves.forEach(mv => {
        const tile = tileMeshes.find(t => t.userData.gridX === mv.x && t.userData.gridZ === mv.z);
        if (tile) {
            tile.material.color.setHex(mv.attack ? 0xef4444 : 0x22c55e);
        }
    });
}

function onPointerDown(e) {
    if (isGameOver || isAnimating) return;
    if (vsAI && currentTurn === 'orange') return;

    const rect = renderer.domElement.getBoundingClientRect();
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;

    mouse.x = ((clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((clientY - rect.top) / rect.height) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(boardGroup.children, true);
    let hitTile = null;
    for (let i = 0; i < intersects.length; i++) {
        if (intersects[i].object.userData && intersects[i].object.userData.isTile) {
            hitTile = intersects[i].object;
            break;
        }
    }

    if (!hitTile) {
        const pieceHits = raycaster.intersectObjects(pieces, true);
        if (pieceHits.length > 0) {
            let obj = pieceHits[0].object;
            while (obj.parent && !obj.userData.type) obj = obj.parent;
            if (obj.userData && obj.userData.alive) {
                hitTile = tileMeshes.find(t => t.userData.gridX === obj.userData.gridX && t.userData.gridZ === obj.userData.gridZ);
            }
        }
    }

    if (!hitTile) return;
    const gx = hitTile.userData.gridX;
    const gz = hitTile.userData.gridZ;

    if (selectedPiece) {
        const chosenMove = validMoves.find(m => m.x === gx && m.z === gz);
        if (chosenMove) {
            startMove(selectedPiece, chosenMove);
            return;
        }
    }

    const clickedPiece = getPieceAt(gx, gz);
    if (clickedPiece && clickedPiece.userData.team === currentTurn) {
        selectedPiece = clickedPiece;
        validMoves = getValidMoves(clickedPiece);
        showValidMoveHighlights(clickedPiece, validMoves);
        if (validMoves.length === 0 && isInCheck(currentTurn)) {
            updateHUD(`⚠️ Bidak ini tidak bisa menyelamatkan WMS Server dari Skak! Pilih bidak lain.`, 'check-alert');
        }
    } else {
        selectedPiece = null;
        validMoves = [];
        clearTileHighlights();
    }
}

renderer.domElement.addEventListener('pointerdown', onPointerDown);

function updateHUD(msg, alertClass = '') {
    const el = document.getElementById('hud-msg');
    el.textContent = msg;
    el.className = 'hud-status ' + alertClass;
}

function updateTurnBadge() {
    const badge = document.getElementById('turn-indicator');
    if (currentTurn === 'blue') {
        badge.textContent = 'GILIRAN: TIM BIRU';
        badge.className = 'turn-badge turn-blue';
    } else {
        badge.textContent = 'GILIRAN: TIM ORANYE';
        badge.className = 'turn-badge turn-orange';
    }
}

function updateScoreUI() {
    const blueAlive = pieces.filter(p => p.userData.alive && p.userData.team === 'blue').length;
    const orangeAlive = pieces.filter(p => p.userData.alive && p.userData.team === 'orange').length;
    document.getElementById('blue-count').textContent = blueAlive;
    document.getElementById('orange-count').textContent = orangeAlive;
}

function endGame(title, desc) {
    isGameOver = true;
    updateHUD(title, 'mate-alert');
    document.getElementById('modal-title').textContent = title;
    document.getElementById('modal-desc').textContent = desc;
    document.getElementById('gameover-modal').style.display = 'flex';
}

function resetGame() {
    isGameOver = false;
    isAnimating = false;
    activeMoveAnim = null;
    currentTurn = 'blue';
    selectedPiece = null;
    validMoves = [];
    document.getElementById('gameover-modal').style.display = 'none';
    initBoardPieces();
    clearTileHighlights();
    updateTurnBadge();
    updateHUD('Permainan baru dimulai. Pilih unit Tim Biru untuk melangkah.', '');
}

function toggleAIMode() {
    vsAI = !vsAI;
    const btn = document.getElementById('btn-ai');
    btn.textContent = vsAI ? '🤖 vs AI: ON' : '👥 2 Pemain';
    btn.classList.toggle('active', vsAI);
    if (vsAI && currentTurn === 'orange' && !isGameOver && !isAnimating) {
        setTimeout(runAIBot, 400);
    }
}

function setCameraPreset(mode) {
    if (mode === 'tactical') {
        camera.position.set(0, 6.8, -7.4);
        controls.target.set(0, 0.45, 0);
    } else if (mode === 'top') {
        camera.position.set(0, 11.5, -0.01);
        controls.target.set(0, 0, 0);
    } else if (mode === 'closeup') {
        camera.position.set(-0.5, 1.15, -1.05);
        controls.target.set(-0.5, 0.92, -2.5);
    }
    controls.update();
}

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

let clock = new THREE.Clock();

function animate() {
    requestAnimationFrame(animate);
    const elapsed = clock.getElapsedTime();

    // Animasi idle bernapas & menoleh halus
    pieces.forEach((p, idx) => {
        if (!p.userData.alive) return;
        if (activeMoveAnim && activeMoveAnim.piece === p) return;
        const head = p.userData.head;
        if (head) {
            head.rotation.y = Math.sin(elapsed * 1.3 + idx * 1.7) * 0.06;
            head.rotation.x = Math.cos(elapsed * 1.0 + idx) * 0.025;
        }
    });

    // ANIMASI BERJALAN MANUSIA (Bukan Loncat!): Ayunan paha, lutut, lengan, dan pinggul
    if (activeMoveAnim) {
        activeMoveAnim.progress += activeMoveAnim.speed;
        const t = Math.min(activeMoveAnim.progress, 1);
        const p = activeMoveAnim.piece;

        // Interpolasi posisi X dan Z secara mulus di atas lantai (TIDAK melompat ke udara)
        p.position.x = activeMoveAnim.sx + (activeMoveAnim.ex - activeMoveAnim.sx) * t;
        p.position.z = activeMoveAnim.sz + (activeMoveAnim.ez - activeMoveAnim.sz) * t;
        p.position.y = 0.03;

        const rig = p.userData.rig;
        if (rig) {
            // Siklus langkah kaki proporsional dengan jarak tempuh
            const walkCycles = Math.max(2, Math.round(activeMoveAnim.dist * 2.5));
            const phase = t * walkCycles * Math.PI * 2;
            const stride = Math.sin(phase);
            const cStride = Math.cos(phase);

            // Ayunan Paha Kiri & Kanan berlawanan
            rig.leftHip.rotation.x = stride * 0.62;
            rig.rightHip.rotation.x = -stride * 0.62;

            // Tekukan Lutut Alami (menekuk ke belakang saat kaki diangkat melangkah)
            rig.leftKnee.rotation.x = -Math.max(0, -cStride) * 0.68;
            rig.rightKnee.rotation.x = -Math.max(0, cStride) * 0.68;

            // Ayunan Pinggul Naik-Turun Halus (1.4 cm) & Goyangan Bahu Manusiawi
            rig.pelvis.position.y = 0.44 + Math.abs(cStride) * 0.014;
            rig.pelvis.rotation.y = stride * 0.08;
            rig.chest.rotation.y = -stride * 0.07;
            rig.chest.rotation.x = 0.06; // Sedikit condong ke depan saat berjalan

            // Ayunan Lengan
            if (rig.role === 'pawn') {
                // Jika membawa kardus, lengan menjaga kardus sambil sedikit memantul halus
                rig.leftShoulder.rotation.x = rig.baseLeftShoulderX + Math.abs(stride) * 0.06;
                rig.rightShoulder.rotation.x = rig.baseRightShoulderX + Math.abs(stride) * 0.06;
            } else {
                rig.leftShoulder.rotation.x = rig.baseLeftShoulderX - stride * 0.42;
                rig.rightShoulder.rotation.x = rig.baseRightShoulderX + stride * 0.42;
            }
        }

        if (t >= 0.78 && !activeMoveAnim.captured) {
            captureVictim(activeMoveAnim);
        }
        if (t >= 1) {
            const done = activeMoveAnim;
            activeMoveAnim = null;
            finishMove(done);
        }
    }

    for (let i = particles.length - 1; i >= 0; i--) {
        const pt = particles[i];
        pt.position.add(pt.userData.vel);
        pt.userData.vel.y -= 0.006;
        pt.userData.life--;
        if (pt.userData.life <= 0) {
            scene.remove(pt);
            particles.splice(i, 1);
        }
    }

    controls.update();
    renderer.render(scene, camera);
}

initBoardPieces();
animate();
</script>
</body>
</html>
"""

components.html(HTML_CODE, height=900, scrolling=False)