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
        Putar Kamera: Geser 1 Jari / Klik Kiri • Zoom: Cubit 2 Jari / Scroll • Aturan Catur FIDE (Skak & Skakmat Aktif)
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
// 1. INISIALISASI SCENE, KAMERA & PENCAHAYAAN PBR REALISTIS (ACES FILMIC)
// ============================================================================
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0b101b);
scene.fog = new THREE.FogExp2(0x0b101b, 0.028);

const camera = new THREE.PerspectiveCamera(42, window.innerWidth / window.innerHeight, 0.08, 100);
camera.position.set(0, 6.8, -7.4);

const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputEncoding = THREE.sRGBEncoding;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.08;
container.appendChild(renderer.domElement);

const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.target.set(0, 0.45, 0);
controls.enableDamping = true;
controls.dampingFactor = 0.07;
controls.maxPolarAngle = Math.PI * 0.485;
controls.minDistance = 0.9;
controls.maxDistance = 18;
controls.update();

// Pencahayaan Studio / Gudang Realistis (Hemisphere + Warm Key Light + Cool Rim Light)
const hemiLight = new THREE.HemisphereLight(0xf1f5f9, 0x1e293b, 0.85);
hemiLight.position.set(0, 15, 0);
scene.add(hemiLight);

const keyLight = new THREE.DirectionalLight(0xfff4e6, 1.15);
keyLight.position.set(5, 11, -6);
keyLight.castShadow = true;
keyLight.shadow.mapSize.width = 2048;
keyLight.shadow.mapSize.height = 2048;
keyLight.shadow.bias = -0.0005;
scene.add(keyLight);

const rimLight = new THREE.DirectionalLight(0x93c5fd, 0.55);
rimLight.position.set(-6, 6, 7);
scene.add(rimLight);

const frontFill = new THREE.DirectionalLight(0xfef3c7, 0.38);
frontFill.position.set(0, 3, -8);
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
// 2. SISTEM DNA MANUSIA & PEModelan MESH ORGANIK UTUH (TANPA BOLA TEMPELAN!)
// ============================================================================
let workerIdCounter = 0;

// Palet Kulit Manusia Realistis (RGB & Hex untuk Tekstur PBR)
const SKIN_PALETTES = [
    { base: [236, 194, 168], shadow: [188, 138, 112], highlight: [250, 222, 204], lip: [188, 112, 104], hex: 0xecc2a8 },
    { base: [224, 176, 142], shadow: [174, 124, 94],  highlight: [242, 204, 176], lip: [175, 98, 88],   hex: 0xe0b08e },
    { base: [208, 154, 116], shadow: [158, 106, 74],  highlight: [228, 182, 148], lip: [162, 86, 76],   hex: 0xd09a74 },
    { base: [190, 132, 94],  shadow: [140, 88, 58],   highlight: [212, 160, 124], lip: [146, 74, 64],   hex: 0xbe845e },
    { base: [164, 108, 72],  shadow: [118, 70, 44],   highlight: [188, 136, 98],  lip: [128, 62, 54],   hex: 0xa46c48 },
    { base: [134, 84, 54],   shadow: [92, 52, 32],    highlight: [158, 108, 76],  lip: [106, 50, 44],   hex: 0x865436 },
    { base: [102, 62, 38],   shadow: [68, 38, 22],    highlight: [128, 84, 56],   lip: [84, 40, 36],    hex: 0x663e26 },
    { base: [216, 168, 138], shadow: [166, 118, 92],  highlight: [236, 196, 170], lip: [168, 94, 86],   hex: 0xd8a88a }
];

const HAIR_PALETTES = [
    '#14110f', // Hitam alami
    '#231b14', // Hitam kecokelatan
    '#382618', // Cokelat tua
    '#523822', // Cokelat medium
    '#2c2a29', // Charcoal / beruban tipis
    '#686664'  // Abu-abu senior
];

const IRIS_PALETTES = [
    '#2b1d0e', '#473018', '#181818', '#3b4b35', '#2c3d4f'
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
        : workerIdCounter * 53 + (o && o.team === 'blue' ? 19 : 97);
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
        // Proporsi Fisik Anatomis (Berbeda tiap orang: atletis, kekar, ramping, tinggi, sedang)
        heightScale: range(0.95, 1.06),
        shoulderWidth: range(0.93, 1.10),
        torsoBulk: range(0.90, 1.14),
        // Morfologi Tulang Wajah (Dipahat langsung pada mesh kepala tunggal, tanpa bola tambahan!)
        headWidth: range(0.93, 1.08),
        headLength: range(0.95, 1.07),
        jawWidth: range(0.86, 1.15),
        chinProminence: range(0.90, 1.12),
        cheekboneWidth: range(0.92, 1.12),
        noseLength: range(0.90, 1.14),
        noseWidth: range(0.88, 1.16),
        mouthWidth: range(0.90, 1.12),
        lipFullness: range(0.88, 1.18),
        // Fitur Wajah Lukis Resolusi Tinggi
        eyeSpacing: range(0.052, 0.060),
        eyeSlant: range(-0.06, 0.06),
        browArch: range(0.0, 0.012),
        browThickness: range(0.85, 1.35),
        browAngle: range(-0.12, 0.14),
        // 0 = bersih, 1 = stubble halus, 2 = kumis rapi, 3 = goatee, 4 = brewok rahang penuh
        facialHairType: workerIdCounter % 5,
        ageLines: rand() > 0.45
    };
}

// ============================================================================
// 3. TEKSTUR WAJAH MANUSIA 1024x1024 (PORI KULIT, MATA DETAIL, SERAT ALIS/BREWOK)
// ============================================================================
function createRealisticFaceTexture(dna) {
    const size = 1024;
    const canvas = document.createElement('canvas');
    canvas.width = size;
    canvas.height = size;
    const ctx = canvas.getContext('2d');

    const [rB, gB, bB] = dna.skin.base;
    const [rS, gS, bS] = dna.skin.shadow;
    const [rH, gH, bH] = dna.skin.highlight;
    const [rL, gL, bL] = dna.skin.lip;

    // 1. Dasar Kulit Manusia dengan Gradasi Vertikal Alami
    const bgGrad = ctx.createLinearGradient(0, 0, 0, size);
    bgGrad.addColorStop(0.00, `rgb(${rH},${gH},${bH})`);
    bgGrad.addColorStop(0.45, `rgb(${rB},${gB},${bB})`);
    bgGrad.addColorStop(0.78, `rgb(${Math.round((rB+rS)/2)},${Math.round((gB+gS)/2)},${Math.round((bB+bS)/2)})`);
    bgGrad.addColorStop(1.00, `rgb(${rS},${gS},${bS})`);
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, size, size);

    // Helper koordinat UV ke Canvas (u=0.5 adalah tengah wajah depan, v=0.5 adalah garis tengah mata/hidung)
    const cx = u => u * size;
    const cy = v => (1.0 - v) * size;

    // 2. Subsurface Scattering (Rona Pipi, Ujung Hidung, & Bayangan Rongga Mata/Rahang)
    function softRadial(u, v, radX, radY, colorStr) {
        ctx.save();
        ctx.translate(cx(u), cy(v));
        ctx.scale(radX * size, radY * size);
        const g = ctx.createRadialGradient(0, 0, 0, 0, 0, 1);
        g.addColorStop(0, colorStr);
        g.addColorStop(1, 'rgba(0,0,0,0)');
        ctx.fillStyle = g;
        ctx.beginPath();
        ctx.arc(0, 0, 1, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }

    // Rona hangat pipi kiri, pipi kanan, dan ujung hidung
    softRadial(0.425, 0.46, 0.055, 0.065, 'rgba(195, 75, 65, 0.16)');
    softRadial(0.575, 0.46, 0.055, 0.065, 'rgba(195, 75, 65, 0.16)');
    softRadial(0.500, 0.43, 0.032, 0.035, 'rgba(195, 70, 60, 0.18)');

    // Highlight tulang dahi, batang hidung, dan dagu
    softRadial(0.500, 0.66, 0.080, 0.055, `rgba(${rH},${gH},${bH}, 0.45)`);
    softRadial(0.500, 0.50, 0.014, 0.075, `rgba(${rH},${gH},${bH}, 0.55)`);
    softRadial(0.500, 0.22, 0.038, 0.032, `rgba(${rH},${gH},${bH}, 0.38)`);

    // Bayangan anatomis rongga mata & bawah dagu
    const eyeUOffset = dna.eyeSpacing;
    softRadial(0.5 - eyeUOffset, 0.535, 0.042, 0.038, `rgba(${rS-25},${gS-25},${bS-20}, 0.48)`);
    softRadial(0.5 + eyeUOffset, 0.535, 0.042, 0.038, `rgba(${rS-25},${gS-25},${bS-20}, 0.48)`);
    softRadial(0.500, 0.12, 0.18, 0.08, `rgba(${rS-35},${gS-30},${bS-25}, 0.65)`);

    // 3. Garis Anatomi Wajah: Lipatan Senyum (Nasolabial Folds) & Lekuk Philtrum Bibir Atas
    ctx.strokeStyle = `rgba(${rS-35}, ${gS-30}, ${bS-25}, 0.32)`;
    ctx.lineWidth = 3.5;
    ctx.lineCap = 'round';
    [-1, 1].forEach(side => {
        ctx.beginPath();
        ctx.moveTo(cx(0.5 + side * 0.028), cy(0.41));
        ctx.quadraticCurveTo(cx(0.5 + side * 0.052), cy(0.35), cx(0.5 + side * 0.045), cy(0.285));
        ctx.stroke();
    });

    // Philtrum (cekungan di atas bibir)
    softRadial(0.500, 0.365, 0.012, 0.024, `rgba(${rS-30},${gS-25},${bS-20}, 0.35)`);

    // Bayangan Samping Batang Hidung & Lubang Hidung (Nostrils)
    [-1, 1].forEach(side => {
        softRadial(0.5 + side * 0.021, 0.49, 0.012, 0.065, `rgba(${rS-30},${gS-25},${bS-20}, 0.38)`);
        // Lubang hidung gelap natural
        ctx.save();
        ctx.translate(cx(0.5 + side * 0.014 * dna.noseWidth), cy(0.408));
        ctx.rotate(side * -0.35);
        ctx.fillStyle = `rgba(38, 20, 15, 0.78)`;
        ctx.beginPath();
        ctx.ellipse(0, 0, 8 * dna.noseWidth, 4.5, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    });

    // 4. MATA MANUSIA REALISTIS (Sklera Bergradasi, Iris Serat Radial, Pupil, Catchlight, Kelopak & Bulu Mata)
    [-1, 1].forEach(side => {
        const eu = 0.5 + side * eyeUOffset;
        const ev = 0.532;
        const ex = cx(eu);
        const ey = cy(ev);
        const ew = 28;
        const eh = 13.5;

        ctx.save();
        ctx.translate(ex, ey);
        ctx.rotate(side * dna.eyeSlant);

        // Lipatan kelopak mata atas (Supratarsal crease)
        ctx.strokeStyle = `rgba(${rS-45}, ${gS-38}, ${bS-32}, 0.65)`;
        ctx.lineWidth = 2.6;
        ctx.beginPath();
        ctx.moveTo(-ew * 1.05, -eh * 0.35);
        ctx.quadraticCurveTo(0, -eh * 1.55, ew * 1.05, -eh * 0.25);
        ctx.stroke();

        // Bentuk bukaan mata Almond (Clipping path)
        ctx.save();
        ctx.beginPath();
        ctx.moveTo(-ew, 0);
        ctx.quadraticCurveTo(0, -eh * 1.15, ew, 0);
        ctx.quadraticCurveTo(0, eh * 0.95, -ew, 0);
        ctx.closePath();
        ctx.clip();

        // Sklera (Putih mata dengan bayangan lembut di bagian atas dari kelopak)
        const scleraGrad = ctx.createLinearGradient(0, -eh, 0, eh);
        scleraGrad.addColorStop(0.0, '#c6cdd6');
        scleraGrad.addColorStop(0.35, '#f4f5f7');
        scleraGrad.addColorStop(1.0, '#e5e7eb');
        ctx.fillStyle = scleraGrad;
        ctx.fillRect(-ew, -eh, ew * 2, eh * 2);

        // Sudut mata dalam merah muda (Tear duct / Caruncle)
        ctx.fillStyle = 'rgba(205, 110, 105, 0.75)';
        ctx.beginPath();
        ctx.arc(side < 0 ? ew * 0.82 : -ew * 0.82, eh * 0.1, 4.5, 0, Math.PI * 2);
        ctx.fill();

        // Iris Berwarna + Cincin Limbal Gelap + Serat Radial
        const irisR = 11.2;
        ctx.fillStyle = '#141210';
        ctx.beginPath();
        ctx.arc(0, -0.5, irisR, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = dna.iris;
        ctx.beginPath();
        ctx.arc(0, -0.5, irisR * 0.88, 0, Math.PI * 2);
        ctx.fill();

        // Serat iris mata
        ctx.strokeStyle = 'rgba(255, 235, 200, 0.18)';
        ctx.lineWidth = 1.0;
        for (let a = 0; a < 24; a++) {
            const ang = (a / 24) * Math.PI * 2;
            ctx.beginPath();
            ctx.moveTo(Math.cos(ang) * 3.5, -0.5 + Math.sin(ang) * 3.5);
            ctx.lineTo(Math.cos(ang) * (irisR * 0.84), -0.5 + Math.sin(ang) * (irisR * 0.84));
            ctx.stroke();
        }

        // Pupil Hitam Pekat
        ctx.fillStyle = '#050505';
        ctx.beginPath();
        ctx.arc(0, -0.5, 4.4, 0, Math.PI * 2);
        ctx.fill();

        // Pantulan Cahaya Kornea (Dual Catchlights agar mata hidup seperti manusia asli)
        ctx.fillStyle = 'rgba(255, 255, 255, 0.92)';
        ctx.beginPath();
        ctx.arc(-3.2, -3.6, 2.3, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = 'rgba(255, 255, 255, 0.55)';
        ctx.beginPath();
        ctx.arc(3.0, 2.2, 1.2, 0, Math.PI * 2);
        ctx.fill();

        ctx.restore(); // End eye clip

        // Garis Bulu Mata Atas & Waterline Bawah
        ctx.strokeStyle = '#120d0a';
        ctx.lineWidth = 3.2;
        ctx.beginPath();
        ctx.moveTo(-ew, 0.5);
        ctx.quadraticCurveTo(0, -eh * 1.15, ew, 0.5);
        ctx.stroke();

        ctx.strokeStyle = `rgba(${rS-40}, ${gS-35}, ${bS-30}, 0.55)`;
        ctx.lineWidth = 1.6;
        ctx.beginPath();
        ctx.moveTo(-ew * 0.9, 1.0);
        ctx.quadraticCurveTo(0, eh * 0.95, ew * 0.9, 1.0);
        ctx.stroke();

        ctx.restore();

        // 5. ALIS SERAT RAMBUT REALISTIS (Puluhan goresan helai rambut, bukan balok!)
        const bx = cx(eu);
        const by = cy(ev + 0.048);
        ctx.save();
        ctx.translate(bx, by);
        ctx.rotate(side * dna.browAngle);
        ctx.strokeStyle = dna.hair;
        ctx.lineWidth = 2.2 * dna.browThickness;
        ctx.lineCap = 'round';
        for (let i = -18; i <= 18; i++) {
            const t = i / 18; // -1 to 1
            const px = t * 32;
            const archY = -Math.sin((1 - Math.abs(t)) * Math.PI) * (6 + dna.browArch * 450);
            ctx.beginPath();
            ctx.moveTo(px, archY + 4 * dna.browThickness);
            ctx.lineTo(px + side * 5, archY - 4 * dna.browThickness);
            ctx.stroke();
        }
        ctx.restore();
    });

    // 6. BIBIR & MULUT MANUSIA ALAMI (Cupid's Bow, Belahan Bibir, & Gradasi Halus)
    const mx = cx(0.5);
    const my = cy(0.308);
    const mw = 36 * dna.mouthWidth;
    const mh = 11 * dna.lipFullness;

    // Bibir Atas
    ctx.fillStyle = `rgba(${rL-12}, ${gL-12}, ${bL-10}, 0.88)`;
    ctx.beginPath();
    ctx.moveTo(mx - mw, my);
    ctx.quadraticCurveTo(mx - mw * 0.45, my - mh * 0.95, mx - 5, my - mh * 0.55);
    ctx.lineTo(mx, my - mh * 0.35);
    ctx.lineTo(mx + 5, my - mh * 0.55);
    ctx.quadraticCurveTo(mx + mw * 0.45, my - mh * 0.95, mx + mw, my);
    ctx.closePath();
    ctx.fill();

    // Bibir Bawah
    const lowerLipGrad = ctx.createLinearGradient(0, my, 0, my + mh * 1.15);
    lowerLipGrad.addColorStop(0.0, `rgba(${rL+8}, ${gL+4}, ${bL+4}, 0.90)`);
    lowerLipGrad.addColorStop(0.5, `rgba(${rL+22}, ${gL+14}, ${bL+12}, 0.92)`);
    lowerLipGrad.addColorStop(1.0, `rgba(${rS}, ${gS}, ${bS}, 0.4)`);
    ctx.fillStyle = lowerLipGrad;
    ctx.beginPath();
    ctx.moveTo(mx - mw * 0.92, my);
    ctx.quadraticCurveTo(mx, my + mh * 1.25, mx + mw * 0.92, my);
    ctx.closePath();
    ctx.fill();

    // Garis Tengah Belahan Mulut
    ctx.strokeStyle = 'rgba(42, 18, 16, 0.82)';
    ctx.lineWidth = 2.6;
    ctx.beginPath();
    ctx.moveTo(mx - mw, my);
    ctx.quadraticCurveTo(mx - mw * 0.4, my + 1.5, mx, my - 0.5);
    ctx.quadraticCurveTo(mx + mw * 0.4, my + 1.5, mx + mw, my);
    ctx.stroke();

    // Bayangan Cekungan Bawah Bibir (Labiomental Crease)
    softRadial(0.500, 0.255, 0.032, 0.015, `rgba(${rS-35},${gS-30},${bS-25}, 0.42)`);

    // 7. RAMBUT KEPALA, CAMBANG & VARIASI KUMIS/BREWOK SERAT HALUS (Bukan Balok Tempelan!)
    ctx.fillStyle = dna.hair;
    // Rambut bagian belakang & samping pelipis
    ctx.fillRect(0, 0, size, cy(0.75));
    ctx.fillRect(0, cy(0.76), cx(0.31), cy(0.32));
    ctx.fillRect(cx(0.69), cy(0.76), cx(0.31), cy(0.32));

    // Cambang (Sideburns) di depan telinga
    ctx.fillRect(cx(0.27), cy(0.62), cx(0.045), cy(0.44) - cy(0.62));
    ctx.fillRect(cx(0.685), cy(0.62), cx(0.045), cy(0.44) - cy(0.62));

    // Variasi Rambut Wajah (Stubble / Kumis / Goatee / Brewok Rahang) dengan goresan helai rambut
    if (dna.facialHairType > 0) {
        ctx.save();
        ctx.strokeStyle = dna.hair;
        ctx.globalAlpha = dna.facialHairType === 1 ? 0.28 : 0.72;
        ctx.lineWidth = dna.facialHairType === 1 ? 1.3 : 2.2;

        // Kumis (untuk tipe 1, 2, 3, 4)
        for (let i = -28; i <= 28; i++) {
            if (Math.abs(i) < 2) continue;
            const hx = mx + i * 1.35 * dna.mouthWidth;
            const hy = my - mh * 0.85 - Math.abs(i) * 0.12;
            ctx.beginPath();
            ctx.moveTo(hx, hy - 5);
            ctx.lineTo(hx + (i > 0 ? 2.5 : -2.5), hy + 4);
            ctx.stroke();
        }

        // Janggut Dagu / Goatee (untuk tipe 1, 3, 4)
        if (dna.facialHairType === 1 || dna.facialHairType === 3 || dna.facialHairType === 4) {
            const chinY = cy(0.205);
            for (let i = -26; i <= 26; i++) {
                for (let j = -10; j <= 12; j++) {
                    if ((i * i) / 680 + (j * j) / 140 > 1) continue;
                    const hx = mx + i * 1.6;
                    const hy = chinY + j * 2.2;
                    ctx.beginPath();
                    ctx.moveTo(hx, hy);
                    ctx.lineTo(hx + (i * 0.08), hy + 5.5);
                    ctx.stroke();
                }
            }
        }

        // Brewok Rahang Penuh (untuk tipe 1 stubble atau tipe 4 full beard)
        if (dna.facialHairType === 1 || dna.facialHairType === 4) {
            ctx.globalAlpha = dna.facialHairType === 1 ? 0.22 : 0.58;
            for (let side of [-1, 1]) {
                for (let step = 0; step < 55; step++) {
                    const t = step / 55;
                    const bx = mx + side * (32 + t * 95);
                    const by = cy(0.22 + t * 0.22);
                    for (let k = -4; k <= 4; k++) {
                        ctx.beginPath();
                        ctx.moveTo(bx + k * 3.2, by - 4);
                        ctx.lineTo(bx + k * 3.2 - side * 2, by + 5);
                        ctx.stroke();
                    }
                }
            }
        }
        ctx.restore();
    }

    const tex = new THREE.CanvasTexture(canvas);
    tex.encoding = THREE.sRGBEncoding;
    tex.needsUpdate = true;
    return tex;
}

// ============================================================================
// 4. GEOMETRI KEPALA PAHAT TUNGGAL (SINGLE CONTINUOUS MESH - TANPA BOLA PIPI!)
// ============================================================================
function createSculptedHeadGeometry(dna) {
    const segU = 64, segV = 48;
    const geom = new THREE.BufferGeometry();
    const positions = [];
    const uvs = [];
    const indices = [];

    const hw = 0.057 * dna.headWidth;
    const hl = 0.076 * dna.headLength;
    const hd = 0.066;

    for (let iv = 0; iv <= segV; iv++) {
        const v = iv / segV; // 0 = bawah dagu, 1 = puncak kepala
        const lat = (v - 0.5) * Math.PI;
        const ny = Math.sin(lat);
        const cosLat = Math.cos(lat);

        for (let iu = 0; iu <= segU; iu++) {
            const u = iu / segU;
            const lon = (u - 0.5) * 2.0 * Math.PI; // 0 = wajah depan (-Z)
            const nx = Math.sin(lon) * cosLat;
            const nz = -Math.cos(lon) * cosLat;

            // 1. Kontur lebar kepala ke rahang & dagu secara mulus (tanpa bola tempelan!)
            let xScale = 1.0;
            if (ny >= 0) {
                xScale = 1.0 - 0.06 * (ny * ny);
            } else {
                const tLow = -ny;
                const cheek = gauss(ny, -0.08, 0.18) * 0.045 * dna.cheekboneWidth;
                const jawTaper = 1.0 - (0.22 / dna.jawWidth) * Math.pow(tLow, 1.4) - 0.28 * Math.pow(tLow, 3.0);
                xScale = Math.max(0.32, jawTaper + cheek);
            }

            let x = nx * hw * xScale;
            let y = ny * hl;
            let z = nz * hd;

            const frontW = Math.max(0.0, -nz);

            // 2. Ratakan bidang wajah depan & majukan dagu sedikit agar profil samping manusiawi
            if (nz < 0) {
                const chinProj = gauss(ny, -0.68, 0.22) * gauss(lon, 0.0, 0.55) * 0.011 * dna.chinProminence;
                const foreheadProj = gauss(ny, 0.38, 0.28) * gauss(lon, 0.0, 0.70) * 0.005;
                z -= (chinProj + foreheadProj);
            }
            if (nz > 0 && ny < -0.15) {
                const napePull = Math.pow((-ny - 0.15) / 0.85, 1.3) * Math.pow(nz, 1.2);
                z -= napePull * 0.020;
            }

            // 3. Cekungan Rongga Mata (Eye Sockets) & Tulang Alis (Brow Ridge)
            const eyeY = gauss(ny, 0.06, 0.09);
            const eyeX = gauss(Math.abs(lon), 0.34, 0.14);
            const socketDepth = eyeY * eyeX * frontW * 0.0048;
            const browLift = gauss(ny, 0.21, 0.08) * gauss(lon, 0.0, 0.58) * frontW * 0.0042;
            z += socketDepth - browLift;

            // 4. Pahatan Hidung Kontinu pada Mesh yang Sama (Batang, Ujung, Cuping)
            const noseCenter = gauss(lon, 0.0, 0.13 * dna.noseWidth);
            const noseBridge = gauss(ny, -0.02, 0.14) * noseCenter * 0.011 * dna.noseLength;
            const noseTip = gauss(ny, -0.17, 0.075) * gauss(lon, 0.0, 0.11 * dna.noseWidth) * 0.014 * dna.noseLength;
            const nostrilWing = gauss(ny, -0.20, 0.055) * gauss(Math.abs(lon), 0.14 * dna.noseWidth, 0.06) * 0.0055;
            z -= (noseBridge + noseTip + nostrilWing) * frontW;

            // 5. Pahatan Bibir Halus & Lekuk Dagu
            const mouthX = gauss(lon, 0.0, 0.24 * dna.mouthWidth);
            const upperLip = gauss(ny, -0.35, 0.045) * mouthX * 0.0042 * dna.lipFullness;
            const mouthCleft = gauss(ny, -0.40, 0.022) * mouthX * (-0.0022);
            const lowerLip = gauss(ny, -0.45, 0.048) * mouthX * 0.0046 * dna.lipFullness;
            const chinGroove = gauss(ny, -0.55, 0.045) * mouthX * (-0.0028);
            z -= (upperLip + mouthCleft + lowerLip + chinGroove) * frontW;

            // 6. Pahatan Daun Telinga Halus di Kiri & Kanan
            const earLon = gauss(Math.abs(lon), Math.PI * 0.52, 0.12);
            const earLat = gauss(ny, -0.04, 0.18);
            x += (nx > 0 ? 1 : -1) * earLon * earLat * 0.0085;

            positions.push(x, y, z);
            uvs.push(u, v);
        }
    }

    for (let iv = 0; iv < segV; iv++) {
        for (let iu = 0; iu < segU; iu++) {
            const a = iv * (segU + 1) + iu;
            const b = a + 1;
            const c = (iv + 1) * (segU + 1) + iu;
            const d = c + 1;
            indices.push(a, b, d);
            indices.push(a, d, c);
        }
    }

    geom.setIndex(indices);
    geom.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geom.setAttribute('uv', new THREE.Float32BufferAttribute(uvs, 2));
    geom.computeVertexNormals();
    return geom;
}

// ============================================================================
// 5. TORSO + BAHU + KERAH + LEHER UTUH (LOFTED MESH TANPA TUTUP KALENG DATAR!)
// ============================================================================
function createUniformTexture(team, role, dna) {
    const size = 512;
    const canvas = document.createElement('canvas');
    canvas.width = size;
    canvas.height = size;
    const ctx = canvas.getContext('2d');

    const [rB, gB, bB] = dna.skin.base;
    const [rS, gS, bS] = dna.skin.shadow;

    // 1. Kemeja Kerja Gelap Profesional di Bawah Rompi (Navy Gelap / Charcoal)
    const shirtColor = team === 'blue' ? '#17253b' : '#262322';
    ctx.fillStyle = shirtColor;
    ctx.fillRect(0, 0, size, size);

    // 2. Bagian Atas (v > 0.78 -> cy < 0.22*size) adalah Kulit Leher & Pangkal Kerah V-Neck
    const neckGrad = ctx.createLinearGradient(0, 0, 0, size * 0.26);
    neckGrad.addColorStop(0.0, `rgb(${rS-15},${gS-15},${bS-12})`);
    neckGrad.addColorStop(0.5, `rgb(${rB},${gB},${bB})`);
    neckGrad.addColorStop(1.0, `rgb(${rS},${gS},${bS})`);
    ctx.fillStyle = neckGrad;
    ctx.fillRect(0, 0, size, size * 0.23);

    // Bukaan Kerah V-Neck di bagian depan (u = 0.5)
    ctx.beginPath();
    ctx.moveTo(size * 0.44, size * 0.22);
    ctx.lineTo(size * 0.50, size * 0.34);
    ctx.lineTo(size * 0.56, size * 0.22);
    ctx.closePath();
    ctx.fill();

    // Daun Kerah Kemeja (Collar)
    ctx.strokeStyle = '#0f172a';
    ctx.lineWidth = 10;
    ctx.beginPath();
    ctx.moveTo(0, size * 0.23);
    ctx.lineTo(size * 0.44, size * 0.23);
    ctx.lineTo(size * 0.50, size * 0.35);
    ctx.lineTo(size * 0.56, size * 0.23);
    ctx.lineTo(size, size * 0.23);
    ctx.stroke();

    // 3. Rompi Safety Gudang (Terbuka di tengah dada memperlihatkan kemeja gelap, bukan tabung polos!)
    const vestColor = team === 'blue' ? '#0284c7' : '#ea580c';
    ctx.fillStyle = vestColor;
    // Sisi belakang & samping rompi, menyisakan celah resleting depan di sekitar u=0.50
    ctx.fillRect(0, size * 0.26, size * 0.455, size * 0.62);
    ctx.fillRect(size * 0.545, size * 0.26, size * 0.455, size * 0.62);

    // List tepi hitam rompi (Vest binding trim)
    ctx.strokeStyle = '#111827';
    ctx.lineWidth = 6;
    ctx.strokeRect(size * 0.01, size * 0.26, size * 0.445, size * 0.62);
    ctx.strokeRect(size * 0.545, size * 0.26, size * 0.445, size * 0.62);

    // Pita Reflektif Perak 3M (2 Horizontal + 2 Vertikal Bahu)
    ctx.fillStyle = '#e2e8f0';
    ctx.fillRect(0, size * 0.56, size * 0.452, 16);
    ctx.fillRect(size * 0.548, size * 0.56, size * 0.452, 16);
    ctx.fillRect(0, size * 0.72, size * 0.452, 16);
    ctx.fillRect(size * 0.548, size * 0.72, size * 0.452, 16);

    // Strip Reflektif Vertikal Dada
    ctx.fillRect(size * 0.37, size * 0.26, 14, size * 0.30);
    ctx.fillRect(size * 0.60, size * 0.26, 14, size * 0.30);

    // Kartu ID Pekerja (ID Badge) di dada kiri
    ctx.fillStyle = '#f8fafc';
    ctx.fillRect(size * 0.57, size * 0.36, 24, 34);
    ctx.fillStyle = '#0284c7';
    ctx.fillRect(size * 0.57, size * 0.36, 24, 8);

    // Sabuk Kerja Kulit Hitam & Gesper Perak di Pinggang Bawah
    ctx.fillStyle = '#111318';
    ctx.fillRect(0, size * 0.88, size, size * 0.12);
    ctx.fillStyle = '#94a3b8';
    ctx.fillRect(size * 0.47, size * 0.89, size * 0.06, size * 0.08);

    const tex = new THREE.CanvasTexture(canvas);
    tex.encoding = THREE.sRGBEncoding;
    tex.needsUpdate = true;
    return tex;
}

function createAnatomicalTorsoAndNeckGeometry(dna) {
    // Lofted Mesh dari Pinggul (v=0) -> Pinggang -> Dada -> Bahu Miring -> Kerah -> Leher Atas (v=1)
    // Sehingga TIDAK ADA tutup silinder datar sama sekali!
    const segU = 48;
    const bw = dna.shoulderWidth;
    const tb = dna.torsoBulk;
    const nw = dna.headWidth;

    const slices = [
        // [v, y, rx, rz, zOffset]
        [0.00, -0.22, 0.095 * tb, 0.065 * tb,  0.000], // Pinggul bawah
        [0.10, -0.16, 0.097 * tb, 0.067 * tb,  0.000], // Sabuk pinggang
        [0.24, -0.06, 0.089 * tb, 0.061 * tb, -0.002], // Lekuk pinggang
        [0.44,  0.06, 0.110 * bw, 0.076 * tb, -0.006], // Dada / Pektoral
        [0.60,  0.14, 0.134 * bw, 0.071 * tb, -0.002], // Lebar bahu deltoid
        [0.70,  0.18, 0.106 * bw, 0.058 * tb,  0.002], // Kemiringan bahu atas
        [0.77,  0.21, 0.056 * bw, 0.046 * tb,  0.004], // Kerah kemeja / Trapezius mulus
        [0.82,  0.23, 0.039 * nw, 0.039 * nw,  0.004], // Pangkal leher
        [0.92,  0.28, 0.036 * nw, 0.037 * nw,  0.001], // Batang leher manusia
        [1.00,  0.33, 0.038 * nw, 0.040 * nw, -0.002]  // Sambungan rahang bawah
    ];

    const geom = new THREE.BufferGeometry();
    const positions = [];
    const uvs = [];
    const indices = [];

    const numSlices = 28;
    function interpSlice(v) {
        for (let i = 0; i < slices.length - 1; i++) {
            const s0 = slices[i], s1 = slices[i + 1];
            if (v >= s0[0] && v <= s1[0]) {
                const t = (v - s0[0]) / (s1[0] - s0[0] + 1e-8);
                // Smooth cosine interpolation so shoulder-to-neck transition is 100% organic
                const st = 0.5 - 0.5 * Math.cos(t * Math.PI);
                return [
                    s0[1] + (s1[1] - s0[1]) * t,
                    s0[2] + (s1[2] - s0[2]) * st,
                    s0[3] + (s1[3] - s0[3]) * st,
                    s0[4] + (s1[4] - s0[4]) * st
                ];
            }
        }
        const last = slices[slices.length - 1];
        return [last[1], last[2], last[3], last[4]];
    }

    for (let iv = 0; iv <= numSlices; iv++) {
        const v = iv / numSlices;
        const [y, rx, rz, zo] = interpSlice(v);

        for (let iu = 0; iu <= segU; iu++) {
            const u = iu / segU;
            const lon = (u - 0.5) * 2.0 * Math.PI; // 0 = depan (-Z)
            const sLon = Math.sin(lon);
            const cLon = -Math.cos(lon);

            // Penampang anatomis dada (sedikit persegi lembut di bahu/dada, bulat di leher)
            const chestFactor = v < 0.75 ? Math.sin((v / 0.75) * Math.PI) : 0.0;
            const rMod = 1.0 + 0.055 * Math.cos(2.0 * lon) * chestFactor;

            let x = sLon * rx * rMod;
            let z = cLon * rz * rMod + zo;

            positions.push(x, y, z);
            uvs.push(u, v);
        }
    }

    for (let iv = 0; iv < numSlices; iv++) {
        for (let iu = 0; iu < segU; iu++) {
            const a = iv * (segU + 1) + iu;
            const b = a + 1;
            const c = (iv + 1) * (segU + 1) + iu;
            const d = c + 1;
            indices.push(a, b, d);
            indices.push(a, d, c);
        }
    }

    geom.setIndex(indices);
    geom.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geom.setAttribute('uv', new THREE.Float32BufferAttribute(uvs, 2));
    geom.computeVertexNormals();
    return geom;
}

// ============================================================================
// 6. LENGAN & KAKI LOFTED UTUH (TANPA SAMBUNGAN PIPA ATAU BOLA BAHU!)
// ============================================================================
function createLimbTexture(dna, sleeveColorHex) {
    const canvas = document.createElement('canvas');
    canvas.width = 128;
    canvas.height = 256;
    const ctx = canvas.getContext('2d');
    const [rB, gB, bB] = dna.skin.base;
    const [rS, gS, bS] = dna.skin.shadow;

    // Lengan baju di bagian atas (v = 0.0 .. 0.36)
    ctx.fillStyle = sleeveColorHex;
    ctx.fillRect(0, 0, 128, 94);
    ctx.fillStyle = '#0f172a';
    ctx.fillRect(0, 90, 128, 5);

    // Kulit lengan bawah & tangan (v = 0.36 .. 1.0)
    const skinGrad = ctx.createLinearGradient(0, 94, 128, 256);
    skinGrad.addColorStop(0.0, `rgb(${rS},${gS},${bS})`);
    skinGrad.addColorStop(0.5, `rgb(${rB},${gB},${bB})`);
    skinGrad.addColorStop(1.0, `rgb(${rS},${gS},${bS})`);
    ctx.fillStyle = skinGrad;
    ctx.fillRect(0, 95, 128, 161);

    const tex = new THREE.CanvasTexture(canvas);
    tex.encoding = THREE.sRGBEncoding;
    return tex;
}

function createLoftedCurveLimb(spinePoints, segU = 20) {
    // spinePoints: array of { x, y, z, rx, rz }
    const geom = new THREE.BufferGeometry();
    const positions = [];
    const uvs = [];
    const indices = [];
    const numRings = spinePoints.length;

    for (let i = 0; i < numRings; i++) {
        const pt = spinePoints[i];
        const v = i / (numRings - 1);

        // Hitung vektor arah (tangent) untuk mengorientasikan cincin elips secara mulus
        const prev = spinePoints[Math.max(0, i - 1)];
        const next = spinePoints[Math.min(numRings - 1, i + 1)];
        const tx = next.x - prev.x;
        const ty = next.y - prev.y;
        const tz = next.z - prev.z;
        const len = Math.hypot(tx, ty, tz) || 1;
        const dirY = ty / len;
        const dirZ = tz / len;

        for (let iu = 0; iu <= segU; iu++) {
            const u = iu / segU;
            const ang = (u - 0.5) * 2.0 * Math.PI;
            const lx = Math.sin(ang) * pt.rx;
            const lz = -Math.cos(ang) * pt.rz;

            // Rotasi cincin mengikuti tekukan siku/lutut
            const wy = pt.y + lz * dirZ * 0.45;
            const wz = pt.z + lz * (-dirY) * 0.85;
            positions.push(pt.x + lx, wy, wz);
            uvs.push(u, 1.0 - v);
        }
    }

    for (let i = 0; i < numRings - 1; i++) {
        for (let iu = 0; iu < segU; iu++) {
            const a = i * (segU + 1) + iu;
            const b = a + 1;
            const c = (i + 1) * (segU + 1) + iu;
            const d = c + 1;
            indices.push(a, b, d);
            indices.push(a, d, c);
        }
    }

    geom.setIndex(indices);
    geom.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geom.setAttribute('uv', new THREE.Float32BufferAttribute(uvs, 2));
    geom.computeVertexNormals();
    return geom;
}

// ============================================================================
// 7. PERAKITAN PEKERJA REALISTIS (buildHuman)
// ============================================================================
const cardboardMat = new THREE.MeshStandardMaterial({ color: 0xc49a6c, roughness: 0.85 });
const tapeMat = new THREE.MeshStandardMaterial({ color: 0xe5dccb, roughness: 0.6 });

function buildCardboardBox() {
    const boxGroup = new THREE.Group();
    const box = new THREE.Mesh(new THREE.BoxGeometry(0.21, 0.15, 0.17), cardboardMat);
    box.castShadow = true;
    boxGroup.add(box);

    const tape = new THREE.Mesh(new THREE.BoxGeometry(0.212, 0.008, 0.036), tapeMat);
    tape.position.y = 0.073;
    boxGroup.add(tape);

    const label = new THREE.Mesh(
        new THREE.PlaneGeometry(0.065, 0.032),
        new THREE.MeshBasicMaterial({ color: 0xf8fafc })
    );
    label.position.set(-0.038, 0.01, -0.086);
    label.rotation.y = Math.PI;
    boxGroup.add(label);
    return boxGroup;
}

function buildHuman(o = {}) {
    const group = new THREE.Group();
    const team = o.team || 'blue';
    const role = o.role || 'pawn';
    const dna = generateWorkerDNA(o);

    // 1. Torso + Bahu + Kerah + Leher sebagai SATU Mesh Utuh
    const torsoGroup = new THREE.Group();
    torsoGroup.position.y = 0.62;
    group.add(torsoGroup);

    const uniformTex = createUniformTexture(team, role, dna);
    const torsoMat = new THREE.MeshStandardMaterial({
        map: uniformTex,
        roughness: 0.76,
        metalness: 0.04
    });
    const torsoMesh = new THREE.Mesh(createAnatomicalTorsoAndNeckGeometry(dna), torsoMat);
    torsoMesh.castShadow = true;
    torsoMesh.receiveShadow = true;
    torsoGroup.add(torsoMesh);

    // 2. Kepala Pahat Tunggal + Tekstur Wajah 1024x1024
    const headGroup = new THREE.Group();
    headGroup.position.set(0, 0.365, -0.006);
    torsoGroup.add(headGroup);

    const faceTex = createRealisticFaceTexture(dna);
    const headMat = new THREE.MeshStandardMaterial({
        map: faceTex,
        roughness: 0.58,
        metalness: 0.03
    });
    const headMesh = new THREE.Mesh(createSculptedHeadGeometry(dna), headMat);
    headMesh.castShadow = true;
    headMesh.receiveShadow = true;
    headGroup.add(headMesh);

    // 3. Helm Proyek Industri Proporsional (Duduk di atas kubah kepala, TIDAK menutupi alis/mata!)
    const helmetGroup = new THREE.Group();
    helmetGroup.position.set(0, 0.042, 0.002);
    helmetGroup.rotation.x = -0.06; // Sedikit miring ke belakang agar seluruh wajah & alis terbuka jelas
    const helmetColor = role === 'supervisor'
        ? 0xfacc15
        : (team === 'blue' ? 0x0ea5e9 : 0xf97316);
    const helmetMat = new THREE.MeshStandardMaterial({
        color: helmetColor,
        roughness: 0.32,
        metalness: 0.12
    });

    const domeGeom = new THREE.SphereGeometry(0.061 * dna.headWidth, 28, 20, 0, Math.PI * 2, 0, Math.PI * 0.46);
    domeGeom.scale(1.0, 0.92, 1.12);
    const domeMesh = new THREE.Mesh(domeGeom, helmetMat);
    domeMesh.castShadow = true;
    helmetGroup.add(domeMesh);

    // Punggung penguat tengah helm (Hard-hat crown ridge)
    const ridgeGeom = new THREE.BoxGeometry(0.018, 0.014, 0.11);
    const ridgeMesh = new THREE.Mesh(ridgeGeom, helmetMat);
    ridgeMesh.position.set(0, 0.052, 0.0);
    helmetGroup.add(ridgeMesh);

    // Lidah helm depan (Visor brim)
    const brimGeom = new THREE.CylinderGeometry(0.061 * dna.headWidth, 0.068 * dna.headWidth, 0.006, 24, 1, false, Math.PI * 0.72, Math.PI * 0.56);
    brimGeom.scale(1.0, 1.0, 1.22);
    const brimMesh = new THREE.Mesh(brimGeom, helmetMat);
    brimMesh.position.set(0, 0.004, -0.014);
    helmetGroup.add(brimMesh);
    headGroup.add(helmetGroup);

    // 4. Lengan Kiri & Kanan Utuh (Menyatu ke bahu tanpa bola bahu!)
    const sleeveColor = team === 'blue' ? '#17253b' : '#262322';
    const armTex = createLimbTexture(dna, sleeveColor);
    const armMat = new THREE.MeshStandardMaterial({ map: armTex, roughness: 0.65, metalness: 0.03 });
    const bw = dna.shoulderWidth;

    [-1, 1].forEach(side => {
        let armSpine;
        if (role === 'pawn') {
            // Pose anatomis memegang kardus di depan perut
            armSpine = [
                { x: side * 0.118 * bw, y:  0.15, z:  0.000, rx: 0.033, rz: 0.033 },
                { x: side * 0.134 * bw, y:  0.09, z: -0.005, rx: 0.030, rz: 0.030 },
                { x: side * 0.130 * bw, y:  0.00, z: -0.025, rx: 0.026, rz: 0.026 },
                { x: side * 0.112 * bw, y: -0.05, z: -0.085, rx: 0.023, rz: 0.022 },
                { x: side * 0.095,      y: -0.07, z: -0.155, rx: 0.019, rz: 0.018 },
                { x: side * 0.085,      y: -0.07, z: -0.195, rx: 0.016, rz: 0.022 },
                { x: side * 0.080,      y: -0.07, z: -0.215, rx: 0.008, rz: 0.012 }
            ];
        } else if (role === 'supervisor' && side === 1) {
            // Pose memegang tablet scanner
            armSpine = [
                { x: side * 0.118 * bw, y:  0.15, z:  0.000, rx: 0.033, rz: 0.033 },
                { x: side * 0.134 * bw, y:  0.09, z: -0.005, rx: 0.030, rz: 0.030 },
                { x: side * 0.128 * bw, y:  0.00, z: -0.030, rx: 0.026, rz: 0.025 },
                { x: side * 0.105 * bw, y: -0.03, z: -0.095, rx: 0.022, rz: 0.021 },
                { x: side * 0.085,      y: -0.02, z: -0.155, rx: 0.018, rz: 0.022 },
                { x: side * 0.080,      y: -0.02, z: -0.175, rx: 0.009, rz: 0.014 }
            ];
        } else {
            // Pose berdiri natural manusia (sedikit ditekuk rileks di siku)
            armSpine = [
                { x: side * 0.118 * bw, y:  0.15, z:  0.000, rx: 0.033, rz: 0.033 },
                { x: side * 0.136 * bw, y:  0.08, z:  0.002, rx: 0.030, rz: 0.029 },
                { x: side * 0.140 * bw, y: -0.02, z:  0.006, rx: 0.026, rz: 0.025 },
                { x: side * 0.138 * bw, y: -0.11, z: -0.015, rx: 0.022, rz: 0.021 },
                { x: side * 0.132 * bw, y: -0.19, z: -0.032, rx: 0.017, rz: 0.017 },
                { x: side * 0.128 * bw, y: -0.23, z: -0.038, rx: 0.014, rz: 0.022 },
                { x: side * 0.125 * bw, y: -0.25, z: -0.040, rx: 0.007, rz: 0.012 }
            ];
        }
        const armMesh = new THREE.Mesh(createLoftedCurveLimb(armSpine, 20), armMat);
        armMesh.castShadow = true;
        torsoGroup.add(armMesh);
    });

    if (role === 'pawn') {
        const boxProp = buildCardboardBox();
        boxProp.position.set(0, -0.06, -0.18);
        torsoGroup.add(boxProp);
    } else if (role === 'supervisor') {
        const tablet = new THREE.Mesh(
            new THREE.BoxGeometry(0.012, 0.085, 0.062),
            new THREE.MeshStandardMaterial({ color: 0x0f172a, emissive: 0x0284c7, emissiveIntensity: 0.45, roughness: 0.2 })
        );
        tablet.position.set(0.082, -0.01, -0.175);
        tablet.rotation.set(0.3, 0.3, 0);
        torsoGroup.add(tablet);
    }

    // 5. Celana Kargo & Sepatu Safety Kulit Utuh
    const pantsMat = new THREE.MeshStandardMaterial({ color: 0x1e2530, roughness: 0.85, metalness: 0.04 });
    const bootMat = new THREE.MeshStandardMaterial({ color: 0x1c1613, roughness: 0.55, metalness: 0.08 });
    const tb = dna.torsoBulk;

    [-1, 1].forEach(side => {
        const lx = side * 0.050 * tb;
        const legSpine = [
            { x: lx, y: 0.42, z:  0.000, rx: 0.048 * tb, rz: 0.048 * tb },
            { x: lx, y: 0.30, z: -0.004, rx: 0.043 * tb, rz: 0.043 * tb },
            { x: lx, y: 0.21, z: -0.008, rx: 0.036,      rz: 0.036      },
            { x: lx, y: 0.11, z:  0.002, rx: 0.033,      rz: 0.034      },
            { x: lx, y: 0.04, z:  0.004, rx: 0.029,      rz: 0.030      }
        ];
        const legMesh = new THREE.Mesh(createLoftedCurveLimb(legSpine, 20), pantsMat);
        legMesh.castShadow = true;
        group.add(legMesh);

        // Sepatu Safety Boot Anatomis
        const bootGeom = new THREE.SphereGeometry(1, 16, 12);
        bootGeom.scale(0.034, 0.026, 0.058);
        const bootMesh = new THREE.Mesh(bootGeom, bootMat);
        bootMesh.position.set(lx, 0.022, -0.016);
        bootMesh.castShadow = true;
        group.add(bootMesh);
    });

    group.scale.set(dna.heightScale, dna.heightScale, dna.heightScale);
    group.userData.dna = dna;
    group.userData.head = headGroup;
    return group;
}

// ============================================================================
// 8. PEMBUATAN UNIT CATUR GUDANG (DENGAN ALAS TIPIS TANPA PUCK NEON TEBAL!)
// ============================================================================
function createChessPieceMesh(type, team) {
    const root = new THREE.Group();
    const isBlue = team === 'blue';
    const teamColor = isBlue ? 0x0ea5e9 : 0xf97316;
    const metalMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.4, metalness: 0.6 });
    const bodyMat = new THREE.MeshStandardMaterial({ color: teamColor, roughness: 0.45, metalness: 0.2 });

    // Penanda cincin taktis tipis di lantai (bukan piringan mainan tebal!)
    const ringGeom = new THREE.RingGeometry(0.32, 0.37, 32);
    ringGeom.rotateX(-Math.PI / 2);
    const baseRing = new THREE.Mesh(
        ringGeom,
        new THREE.MeshBasicMaterial({ color: teamColor, side: THREE.DoubleSide, transparent: true, opacity: 0.65 })
    );
    baseRing.position.y = 0.005;
    root.add(baseRing);

    if (type === 'pawn') {
        const human = buildHuman({ team, role: 'pawn' });
        root.add(human);
    } else if (type === 'bishop') {
        const human = buildHuman({ team, role: 'supervisor' });
        root.add(human);
    } else if (type === 'knight') {
        const human = buildHuman({ team, role: 'operator' });
        human.position.z = 0.14;
        root.add(human);

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

        const operator = buildHuman({ team, role: 'operator' });
        operator.scale.multiplyScalar(0.90);
        operator.position.set(0, 0.10, -0.12);
        root.add(operator);
    } else if (type === 'queen') {
        const agvDeck = new THREE.Mesh(new THREE.CylinderGeometry(0.38, 0.40, 0.08, 28), metalMat);
        agvDeck.position.y = 0.04;
        root.add(agvDeck);

        const chief = buildHuman({ team, role: 'supervisor' });
        chief.position.y = 0.06;
        root.add(chief);
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

        const commander = buildHuman({ team, role: 'supervisor' });
        commander.position.set(0.15, 0, -0.06);
        root.add(commander);
    }

    root.rotation.y = isBlue ? Math.PI : 0;
    return root;
}

// ============================================================================
// 9. STATE PERMAINAN & ATURAN CATUR FIDE LENGKAP (SKAK, SKAKMAT, STALEMATE)
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
    mesh.userData = { type, team, gridX: gx, gridZ: gz, alive: true, hasMoved: false };
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
    activeMoveAnim = {
        piece, mv,
        sx: piece.position.x, sz: piece.position.z,
        ex: targetPos.x, ez: targetPos.z,
        progress: 0, captured: false
    };
}

function finishMove(m) {
    const piece = m.piece, moveData = m.mv;
    piece.position.set(m.ex, 0.03, m.ez);
    piece.userData.gridX = moveData.x;
    piece.userData.gridZ = moveData.z;
    piece.userData.hasMoved = true;

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
// 10. INTERAKSI KLIK, HIGHLIGHT, KAMERA & ANIMATION LOOP
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
        controls.target.set(-0.5, 0.95, -2.5);
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

    pieces.forEach((p, idx) => {
        if (!p.userData.alive) return;
        const head = p.userData.head;
        if (head) {
            head.rotation.y = Math.sin(elapsed * 1.3 + idx * 1.7) * 0.06;
            head.rotation.x = Math.cos(elapsed * 1.0 + idx) * 0.025;
        }
    });

    if (activeMoveAnim) {
        activeMoveAnim.progress += 0.08;
        const t = Math.min(activeMoveAnim.progress, 1);
        const p = activeMoveAnim.piece;
        p.position.x = activeMoveAnim.sx + (activeMoveAnim.ex - activeMoveAnim.sx) * t;
        p.position.z = activeMoveAnim.sz + (activeMoveAnim.ez - activeMoveAnim.sz) * t;
        p.position.y = 0.03 + Math.sin(t * Math.PI) * 0.25;

        if (t >= 0.7 && !activeMoveAnim.captured) {
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