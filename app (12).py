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
        background: #080c14;
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        color: #f1f5f9;
    }
    #canvas-container {
        width: 100%; height: 100%;
        position: absolute; top: 0; left: 0; z-index: 1;
    }
    /* TOP HUD BAR */
    .hud-top {
        position: absolute; top: 12px; left: 12px; right: 12px; z-index: 10;
        display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between;
        gap: 10px;
        background: rgba(15, 23, 42, 0.82);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 12px;
        padding: 10px 16px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.45);
    }
    .brand {
        display: flex; align-items: center; gap: 10px;
    }
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
        background: rgba(30, 41, 59, 0.7);
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
    .controls {
        display: flex; flex-wrap: wrap; gap: 6px; align-items: center;
    }
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
    .btn-danger { background: rgba(185, 28, 28, 0.8); border-color: #f87171; }
    .btn-danger:hover { background: rgba(220, 38, 38, 0.95); }

    /* SCORE & LEGEND BAR */
    .hud-bottom {
        position: absolute; bottom: 12px; left: 12px; right: 12px; z-index: 10;
        display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center;
        gap: 8px; pointer-events: none;
    }
    .score-card {
        pointer-events: auto;
        background: rgba(15, 23, 42, 0.82);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(148, 163, 184, 0.2);
        padding: 8px 14px; border-radius: 10px;
        font-size: 12px; display: flex; gap: 14px; align-items: center;
    }
    .score-blue { color: #38bdf8; font-weight: 700; }
    .score-orange { color: #fb923c; font-weight: 700; }
    .hint-text {
        font-size: 11px; color: #94a3b8;
    }

    /* GAME OVER MODAL */
    #gameover-modal {
        display: none;
        position: absolute; inset: 0; z-index: 30;
        background: rgba(2, 6, 23, 0.72);
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
    .modal-title {
        font-size: 22px; font-weight: 800; margin-bottom: 10px; color: #facc15;
    }
    .modal-sub {
        font-size: 14px; color: #cbd5e1; margin-bottom: 20px; line-height: 1.5;
    }
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
// 1. INISIALISASI SCENE, KAMERA, PENCAHAYAAN REALISTIS & GUDANG
// ============================================================================
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x090d16);
scene.fog = new THREE.FogExp2(0x090d16, 0.035);

const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 100);
camera.position.set(0, 7.2, -7.8);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
container.appendChild(renderer.domElement);

const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.target.set(0, 0.4, 0);
controls.enableDamping = true;
controls.dampingFactor = 0.07;
controls.maxPolarAngle = Math.PI * 0.48;
controls.minDistance = 1.6;
controls.maxDistance = 18;
controls.update();

// Pencahayaan 3-Titik (Key Light, Fill Light, Rim Light) agar kontur wajah 3D terlihat jelas
const ambientLight = new THREE.AmbientLight(0xdbeafe, 0.65);
scene.add(ambientLight);

const dirLight = new THREE.DirectionalLight(0xfff7ed, 0.95);
dirLight.position.set(6, 12, -6);
dirLight.castShadow = true;
dirLight.shadow.mapSize.width = 2048;
dirLight.shadow.mapSize.height = 2048;
scene.add(dirLight);

const fillLight = new THREE.DirectionalLight(0x93c5fd, 0.45);
fillLight.position.set(-6, 5, 7);
scene.add(fillLight);

// Material Umum Seragam & Kendaraan
const blueVestMat = new THREE.MeshLambertMaterial({ color: 0x0ea5e9 });
const orangeVestMat = new THREE.MeshLambertMaterial({ color: 0xf97316 });
const whiteHelmetMat = new THREE.MeshPhongMaterial({ color: 0x22d3ee, shininess: 70 });
const goldHelmetMat = new THREE.MeshPhongMaterial({ color: 0xfacc15, shininess: 70 });
const pantsMat = new THREE.MeshLambertMaterial({ color: 0x2b3648 });
const bootMat = new THREE.MeshLambertMaterial({ color: 0x1a1614 });
const beltMat = new THREE.MeshLambertMaterial({ color: 0x111111 });
const visorMat = new THREE.MeshPhongMaterial({ color: 0x0f172a, shininess: 90, transparent: true, opacity: 0.78 });
const cardboardMat = new THREE.MeshLambertMaterial({ color: 0xc29562 });
const tapeMat = new THREE.MeshLambertMaterial({ color: 0xdfd3c3 });

// Konversi Koordinat Grid (0..7) ke Posisi Dunia 3D (-3.5..3.5)
const TILE_SIZE = 1.0;
function gridToWorld(gx, gz) {
    return {
        x: (gx - 3.5) * TILE_SIZE,
        z: (gz - 3.5) * TILE_SIZE
    };
}
function inBounds(gx, gz) {
    return gx >= 0 && gx < 8 && gz >= 0 && gz < 8;
}

// Buat Lantai Gudang & Papan Catur 8x8
const boardGroup = new THREE.Group();
scene.add(boardGroup);

const warehouseFloor = new THREE.Mesh(
    new THREE.PlaneGeometry(28, 28),
    new THREE.MeshLambertMaterial({ color: 0x1e2530 })
);
warehouseFloor.rotation.x = -Math.PI / 2;
warehouseFloor.position.y = -0.02;
warehouseFloor.receiveShadow = true;
scene.add(warehouseFloor);

// Bingkai Papan Gudang
const borderMesh = new THREE.Mesh(
    new THREE.BoxGeometry(8.5, 0.08, 8.5),
    new THREE.MeshLambertMaterial({ color: 0x0f172a })
);
borderMesh.position.y = -0.03;
borderMesh.receiveShadow = true;
boardGroup.add(borderMesh);

const tileMeshes = [];
const lightTileMat = new THREE.MeshLambertMaterial({ color: 0x475569 });
const darkTileMat = new THREE.MeshLambertMaterial({ color: 0x1e293b });

for (let gx = 0; gx < 8; gx++) {
    for (let gz = 0; gz < 8; gz++) {
        const isLight = (gx + gz) % 2 === 0;
        const tile = new THREE.Mesh(
            new THREE.BoxGeometry(TILE_SIZE * 0.98, 0.06, TILE_SIZE * 0.98),
            (isLight ? lightTileMat : darkTileMat).clone()
        );
        const pos = gridToWorld(gx, gz);
        tile.position.set(pos.x, 0, pos.z);
        tile.receiveShadow = true;
        tile.userData = { isTile: true, gridX: gx, gridZ: gz, baseColor: isLight ? 0x475569 : 0x1e293b };
        boardGroup.add(tile);
        tileMeshes.push(tile);
    }
}

// ============================================================================
// 2. GENERATOR KARAKTER MANUSIA REALISTIS & WAJAH BERBEDA-BEDA (DNA SYSTEM)
// ============================================================================
let workerIdCounter = 0;

const REALISTIC_SKIN_TONES = [
    { skin: 0xf2ccb7, lip: 0xc97b70, ear: 0xe5b59d }, // Terang hangat
    { skin: 0xe8b896, lip: 0xb86b5e, ear: 0xd9a17c }, // Kuning langsat
    { skin: 0xd99e73, lip: 0xa6584c, ear: 0xc7885c }, // Sawo matang terang
    { skin: 0xc68652, lip: 0x91473b, ear: 0xb37240 }, // Sawo matang
    { skin: 0xa5693f, lip: 0x78382e, ear: 0x91562f }, // Cokelat hangat
    { skin: 0x824f2b, lip: 0x5e2a22, ear: 0x704121 }, // Cokelat gelap
    { skin: 0x5c361e, lip: 0x47201a, ear: 0x4d2b16 }, // Gelap tegas
    { skin: 0xe0ac8b, lip: 0xb36659, ear: 0xcf9674 }  // Olive / Mediterania
];

const HAIR_COLORS = [
    0x14110f, // Hitam pekat
    0x241c15, // Hitam kecokelatan
    0x3b2818, // Cokelat tua
    0x593c23, // Cokelat medium
    0x2e2b29, // Hitam beruban
    0x6e6d6b  // Abu-abu / Pekerja senior
];

const IRIS_COLORS = [
    0x2b1d0e, // Cokelat tua
    0x4a3219, // Cokelat amber
    0x141414, // Hitam
    0x3d4e38, // Hazel
    0x2c3e50  // Abu-abu gelap
];

function createSeededRandom(seed) {
    let s = (seed * 9301 + 49297) % 233280;
    return function () {
        s = (s * 9301 + 49297) % 233280;
        return s / 233280;
    };
}

function generateWorkerDNA(o) {
    workerIdCounter++;
    const seedBase = (o && typeof o.seed === 'number')
        ? o.seed
        : workerIdCounter * 43 + (o && o.team === 'blue' ? 17 : 89);
    const rand = createSeededRandom(seedBase);
    const range = (min, max) => min + rand() * (max - min);

    const palette = REALISTIC_SKIN_TONES[(workerIdCounter + Math.floor(rand() * 3)) % REALISTIC_SKIN_TONES.length];
    const hairColor = HAIR_COLORS[Math.floor(rand() * HAIR_COLORS.length)];
    const irisColor = IRIS_COLORS[Math.floor(rand() * IRIS_COLORS.length)];

    return {
        palette,
        hairColor,
        irisColor,
        // Variasi bentuk fisik tubuh
        heightScale: range(0.94, 1.07),
        shoulderWidth: range(0.92, 1.12),
        torsoBulk: range(0.88, 1.16),
        // Variasi morfologi tulang wajah
        headWidth: range(0.91, 1.09),
        headLength: range(0.93, 1.08),
        jawWidth: range(0.84, 1.16),
        chinProminence: range(0.88, 1.16),
        cheekboneWidth: range(0.92, 1.14),
        noseLength: range(0.86, 1.18),
        noseWidth: range(0.84, 1.22),
        noseBridgeTilt: range(0.16, 0.30),
        eyeSpacing: range(0.019, 0.024),
        eyeSize: range(0.90, 1.08),
        browTilt: range(-0.20, 0.20),
        browThickness: range(0.82, 1.35),
        mouthWidth: range(0.86, 1.16),
        lipFullness: range(0.85, 1.25),
        // 0 = klimis/bersih, 1 = kumis, 2 = janggut dagu (goatee), 3 = brewok penuh
        facialHairType: workerIdCounter % 4,
        hasSideburns: rand() > 0.4,
        wearsGogglesOnEyes: o.role === 'supervisor' ? true : (rand() > 0.65)
    };
}

// Pembuatan kotak kardus dengan pita perekat & stiker barcode seperti di screenshot
function buildCardboardBox() {
    const boxGroup = new THREE.Group();
    const box = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.16, 0.18), cardboardMat);
    box.castShadow = true;
    boxGroup.add(box);

    const tape = new THREE.Mesh(new THREE.BoxGeometry(0.222, 0.01, 0.04), tapeMat);
    tape.position.y = 0.078;
    boxGroup.add(tape);

    // Label putih barcode
    const label = new THREE.Mesh(
        new THREE.PlaneGeometry(0.07, 0.035),
        new THREE.MeshBasicMaterial({ color: 0xf8fafc })
    );
    label.position.set(-0.04, 0.01, -0.091);
    label.rotation.y = Math.PI;
    boxGroup.add(label);

    return boxGroup;
}

function buildHuman(o = {}) {
    const group = new THREE.Group();
    const isBlue = o.team === 'blue';
    const dna = generateWorkerDNA(o);

    // Material kulit manusia dengan pantulan alami (bukan Lambert datar)
    const workerSkinMat = new THREE.MeshPhongMaterial({
        color: dna.palette.skin,
        specular: 0x2a1f1a,
        shininess: 18
    });
    const workerEarMat = new THREE.MeshPhongMaterial({
        color: dna.palette.ear,
        specular: 0x221510,
        shininess: 14
    });
    const workerLipMat = new THREE.MeshPhongMaterial({
        color: dna.palette.lip,
        specular: 0x332222,
        shininess: 22
    });
    const workerHairMat = new THREE.MeshLambertMaterial({ color: dna.hairColor });

    const vestMat = isBlue ? blueVestMat : orangeVestMat;
    const shirtUnderMat = new THREE.MeshLambertMaterial({
        color: isBlue ? 0x0369a1 : 0x9a3412
    });
    const helmetMat = o.role === 'supervisor'
        ? goldHelmetMat
        : (isBlue ? whiteHelmetMat : goldHelmetMat);

    function addPart(parent, pos, radii, rot = [0, 0, 0], mat = workerSkinMat) {
        const geom = new THREE.SphereGeometry(1, 16, 14);
        geom.scale(radii[0], radii[1], radii[2]);
        const mesh = new THREE.Mesh(geom, mat);
        mesh.position.set(pos[0], pos[1], pos[2]);
        if (rot[0] || rot[1] || rot[2]) mesh.rotation.set(rot[0], rot[1], rot[2]);
        mesh.castShadow = true;
        parent.add(mesh);
        return mesh;
    }

    function addCyl(parent, pos, rTop, rBot, height, mat = workerSkinMat, rot = [0, 0, 0]) {
        const geom = new THREE.CylinderGeometry(rTop, rBot, height, 14);
        const mesh = new THREE.Mesh(geom, mat);
        mesh.position.set(pos[0], pos[1], pos[2]);
        if (rot[0] || rot[1] || rot[2]) mesh.rotation.set(rot[0], rot[1], rot[2]);
        mesh.castShadow = true;
        parent.add(mesh);
        return mesh;
    }

    // 1. PINGGUL (PELVIS)
    const pelvis = new THREE.Group();
    pelvis.position.y = 0.52;
    group.add(pelvis);

    addCyl(pelvis, [0, 0.0, 0], 0.095 * dna.torsoBulk, 0.088 * dna.torsoBulk, 0.11, pantsMat);
    addCyl(pelvis, [0, 0.05, 0], 0.098 * dna.torsoBulk, 0.098 * dna.torsoBulk, 0.03, beltMat);

    // 2. TORSO ANATOMIS (V-Taper & Otot Trapezius, tanpa bola bahu balon)
    const chest = new THREE.Group();
    chest.position.y = 0.20;
    pelvis.add(chest);

    addCyl(chest, [0, -0.06, 0], 0.108 * dna.shoulderWidth, 0.094 * dna.torsoBulk, 0.16, shirtUnderMat);
    addPart(chest, [0, 0.04, 0], [0.118 * dna.shoulderWidth, 0.11, 0.078 * dna.torsoBulk], [0, 0, 0], shirtUnderMat);

    // Rompi Safety + Pita Reflektif
    addCyl(chest, [0, 0.0, 0], 0.114 * dna.shoulderWidth, 0.098 * dna.torsoBulk, 0.22, vestMat);
    const stripeMat = new THREE.MeshBasicMaterial({ color: 0xe2e8f0 });
    addCyl(chest, [0, -0.04, 0], 0.116 * dna.shoulderWidth, 0.105 * dna.torsoBulk, 0.022, stripeMat);

    // Otot Trapezius penyambung bahu ke leher
    addPart(chest, [0, 0.12, 0.005], [0.082 * dna.shoulderWidth, 0.035, 0.052], [0, 0, 0], workerSkinMat);

    // 3. KEPALA & STRUKTUR WAJAH MANUSIA REALISTIS
    const head = new THREE.Group();
    head.position.y = 0.25;
    chest.add(head);

    // Leher proporsional
    addCyl(head, [0, -0.085, 0.006], 0.038 * dna.headWidth, 0.044 * dna.shoulderWidth, 0.095, workerSkinMat, [0.06, 0, 0]);

    // Tengkorak (Cranium)
    const hw = 0.058 * dna.headWidth;
    const hl = 0.076 * dna.headLength;
    const hd = 0.065;
    addPart(head, [0, 0.008, 0], [hw, hl, hd], [0, 0, 0], workerSkinMat);

    // Tulang Pipi (Cheekbones Kiri & Kanan)
    const cheekW = 0.044 * dna.cheekboneWidth;
    addPart(head, [-cheekW * 0.55, -0.016, -0.034], [0.026, 0.024, 0.028], [0, 0, 0], workerSkinMat);
    addPart(head, [cheekW * 0.55, -0.016, -0.034], [0.026, 0.024, 0.028], [0, 0, 0], workerSkinMat);

    // Rahang Bawah (Mandible) & Dagu (Chin)
    addPart(head, [0, -0.038, -0.014], [0.046 * dna.jawWidth, 0.036, 0.048], [0.08, 0, 0], workerSkinMat);
    addPart(head, [0, -0.064 * dna.headLength, -0.038 * dna.chinProminence], [0.022 * dna.jawWidth, 0.016, 0.022], [0, 0, 0], workerSkinMat);

    // Tulang Alis (Brow Ridge)
    addPart(head, [0, 0.018, -0.052], [0.045 * dna.headWidth, 0.012, 0.018], [0.1, 0, 0], workerSkinMat);

    // Telinga Kiri & Kanan
    addPart(head, [-hw * 0.98, -0.008, -0.002], [0.009, 0.022, 0.014], [0, -0.15, -0.08], workerEarMat);
    addPart(head, [hw * 0.98, -0.008, -0.002], [0.009, 0.022, 0.014], [0, 0.15, 0.08], workerEarMat);

    // Hidung Anatomis (Batang hidung, ujung hidung, dan 2 cuping hidung)
    const nLen = 0.022 * dna.noseLength;
    const nWid = 0.011 * dna.noseWidth;
    addPart(head, [0, -0.004, -0.058], [nWid * 0.65, nLen, 0.012], [dna.noseBridgeTilt, 0, 0], workerSkinMat);
    addPart(head, [0, -0.020, -0.066 * dna.noseLength], [nWid * 0.95, 0.010, 0.013], [0, 0, 0], workerSkinMat);
    addPart(head, [-nWid * 0.65, -0.023, -0.061], [nWid * 0.55, 0.007, 0.009], [0, 0, 0], workerEarMat);
    addPart(head, [nWid * 0.65, -0.023, -0.061], [nWid * 0.55, 0.007, 0.009], [0, 0, 0], workerEarMat);

    // Mata dengan Kelopak Atas, Iris Berwarna, Pupil & Alis
    const scleraMat = new THREE.MeshPhongMaterial({ color: 0xfaf8f5, shininess: 30 });
    const irisMat = new THREE.MeshBasicMaterial({ color: dna.irisColor });
    const pupilMat = new THREE.MeshBasicMaterial({ color: 0x090909 });

    [-1, 1].forEach(side => {
        const ex = side * dna.eyeSpacing;
        const ey = 0.006;
        const ez = -0.053;
        const eScale = dna.eyeSize;

        const eyeGroup = new THREE.Group();
        eyeGroup.position.set(ex, ey, ez);

        const eyeball = new THREE.Mesh(new THREE.SphereGeometry(0.0085 * eScale, 12, 10), scleraMat);
        eyeball.scale.set(1.1, 0.95, 0.75);
        eyeGroup.add(eyeball);

        const iris = new THREE.Mesh(new THREE.SphereGeometry(0.0048 * eScale, 10, 8), irisMat);
        iris.scale.set(1, 1, 0.4);
        iris.position.set(0, 0, -0.0052 * eScale);
        eyeGroup.add(iris);

        const pupil = new THREE.Mesh(new THREE.SphereGeometry(0.0026 * eScale, 8, 8), pupilMat);
        pupil.scale.set(1, 1, 0.4);
        pupil.position.set(0, 0, -0.0062 * eScale);
        eyeGroup.add(pupil);

        const upperLid = new THREE.Mesh(
            new THREE.SphereGeometry(0.0092 * eScale, 12, 8, 0, Math.PI * 2, 0, Math.PI * 0.48),
            workerSkinMat
        );
        upperLid.scale.set(1.12, 1.0, 0.82);
        upperLid.rotation.x = -0.25;
        eyeGroup.add(upperLid);

        head.add(eyeGroup);

        // Alis sesuai DNA
        addPart(
            head,
            [ex, ey + 0.013, ez - 0.004],
            [0.013, 0.0032 * dna.browThickness, 0.005],
            [0, side * -0.15, side * dna.browTilt],
            workerHairMat
        );
    });

    // Bibir Atas, Belahan Mulut & Bibir Bawah
    const mw = 0.016 * dna.mouthWidth;
    const lf = 0.0042 * dna.lipFullness;
    addPart(head, [0, -0.042, -0.056], [mw, lf * 0.85, 0.007], [0, 0, 0], workerLipMat);
    addPart(head, [0, -0.0445, -0.057], [mw * 0.92, 0.0015, 0.006], [0, 0, 0], pupilMat);
    addPart(head, [0, -0.047, -0.055], [mw * 0.88, lf, 0.0075], [0, 0, 0], workerLipMat);

    // Rambut & Cambang
    addPart(head, [0, 0.012, 0.012], [hw * 1.02, hl * 0.88, hd * 0.96], [0, 0, 0], workerHairMat);
    if (dna.hasSideburns) {
        addPart(head, [-hw * 0.93, -0.012, -0.015], [0.006, 0.020, 0.012], [0, 0, 0], workerHairMat);
        addPart(head, [hw * 0.93, -0.012, -0.015], [0.006, 0.020, 0.012], [0, 0, 0], workerHairMat);
    }

    // Kumis, Goatee, atau Brewok Penuh
    if (dna.facialHairType === 1 || dna.facialHairType === 3) {
        addPart(head, [-0.007, -0.037, -0.058], [0.011, 0.004, 0.006], [0, 0, 0.22], workerHairMat);
        addPart(head, [0.007, -0.037, -0.058], [0.011, 0.004, 0.006], [0, 0, -0.22], workerHairMat);
    }
    if (dna.facialHairType === 2 || dna.facialHairType === 3) {
        addPart(head, [0, -0.063 * dna.headLength, -0.042 * dna.chinProminence], [0.018 * dna.jawWidth, 0.014, 0.018], [0, 0, 0], workerHairMat);
    }
    if (dna.facialHairType === 3) {
        addPart(head, [0, -0.044, -0.020], [0.047 * dna.jawWidth, 0.032, 0.047], [0.08, 0, 0], workerHairMat);
    }

    // Helm Keselamatan
    const helmetGroup = new THREE.Group();
    helmetGroup.position.set(0, 0.034, 0);
    const helmetDome = new THREE.Mesh(
        new THREE.SphereGeometry(0.065 * dna.headWidth, 16, 12, 0, Math.PI * 2, 0, Math.PI * 0.52),
        helmetMat
    );
    helmetGroup.add(helmetDome);
    const brimMesh = new THREE.Mesh(
        new THREE.CylinderGeometry(0.068 * dna.headWidth, 0.072 * dna.headWidth, 0.008, 16, 1, false, Math.PI * 0.65, Math.PI * 0.7),
        helmetMat
    );
    brimMesh.position.set(0, 0.002, -0.012);
    helmetGroup.add(brimMesh);
    head.add(helmetGroup);

    // Kacamata Safety (Sebagian di mata, sebagian di atas helm agar wajah terlihat jelas)
    const goggleMesh = new THREE.Mesh(new THREE.BoxGeometry(0.088 * dna.headWidth, 0.020, 0.035), visorMat);
    if (dna.wearsGogglesOnEyes) {
        goggleMesh.position.set(0, 0.006, -0.050);
    } else {
        goggleMesh.position.set(0, 0.048, -0.052);
        goggleMesh.rotation.x = -0.25;
    }
    head.add(goggleMesh);

    // 4. LENGAN & POSE PEKERJA (Memegang Kardus, Tablet Supervisor, atau Standar)
    const armOffsetX = 0.132 * dna.shoulderWidth;
    const holdingBox = o.role === 'pawn';
    const holdingTablet = o.role === 'supervisor';

    [-1, 1].forEach(side => {
        const shoulderGroup = new THREE.Group();
        shoulderGroup.position.set(side * armOffsetX, 0.07, 0);
        chest.add(shoulderGroup);

        // Bahu deltoid lengan baju yang menyatu mulus
        addPart(shoulderGroup, [0, -0.015, 0], [0.036, 0.048, 0.036], [0, 0, side * -0.12], shirtUnderMat);
        addCyl(shoulderGroup, [side * 0.006, -0.09, 0], 0.031, 0.026, 0.13, workerSkinMat);

        if (holdingBox) {
            // Lengan ditekuk ke depan memegang kardus logistik
            addCyl(shoulderGroup, [side * -0.01, -0.17, -0.07], 0.026, 0.020, 0.13, workerSkinMat, [1.15, 0, side * 0.18]);
            addPart(shoulderGroup, [side * -0.02, -0.19, -0.14], [0.018, 0.022, 0.014], [0, 0, 0], workerSkinMat);
        } else if (holdingTablet && side === 1) {
            // Tangan kiri memegang tablet scanner gudang
            addCyl(shoulderGroup, [0.0, -0.17, -0.06], 0.026, 0.020, 0.13, workerSkinMat, [1.05, 0, -0.15]);
            const tablet = new THREE.Mesh(
                new THREE.BoxGeometry(0.015, 0.09, 0.065),
                new THREE.MeshPhongMaterial({ color: 0x38bdf8, emissive: 0x0284c7, emissiveIntensity: 0.4 })
            );
            tablet.position.set(-0.01, -0.18, -0.13);
            shoulderGroup.add(tablet);
        } else {
            addCyl(shoulderGroup, [side * 0.010, -0.20, -0.02], 0.026, 0.020, 0.13, workerSkinMat, [0.25, 0, 0]);
            addPart(shoulderGroup, [side * 0.012, -0.27, -0.038], [0.018, 0.024, 0.012], [0.2, 0, 0], workerSkinMat);
        }
    });

    if (holdingBox) {
        const boxProp = buildCardboardBox();
        boxProp.position.set(0, -0.09, -0.18);
        chest.add(boxProp);
    }

    // 5. KAKI & SEPATU SAFETY
    [-1, 1].forEach(side => {
        const legX = side * 0.052 * dna.torsoBulk;
        addCyl(pelvis, [legX, -0.15, 0], 0.046 * dna.torsoBulk, 0.038, 0.22, pantsMat);
        addCyl(pelvis, [legX, -0.35, 0], 0.037, 0.030, 0.21, pantsMat);
        addPart(pelvis, [legX, -0.48, -0.018], [0.036, 0.028, 0.062], [0, 0, 0], bootMat);
    });

    group.scale.set(dna.heightScale, dna.heightScale, dna.heightScale);
    group.userData.dna = dna;
    group.userData.head = head;
    return group;
}

// ============================================================================
// 3. PEMBUATAN UNIT CATUR GUDANG (PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING)
// ============================================================================
function createChessPieceMesh(type, team) {
    const root = new THREE.Group();
    const isBlue = team === 'blue';
    const teamColor = isBlue ? 0x0ea5e9 : 0xf97316;
    const metalMat = new THREE.MeshPhongMaterial({ color: 0x334155, shininess: 50 });
    const bodyMat = new THREE.MeshPhongMaterial({ color: teamColor, shininess: 45 });

    // Alas penanda tim di bawah unit
    const baseRing = new THREE.Mesh(
        new THREE.CylinderGeometry(0.36, 0.39, 0.04, 24),
        new THREE.MeshLambertMaterial({ color: teamColor })
    );
    baseRing.position.y = 0.02;
    root.add(baseRing);

    if (type === 'pawn') {
        // PAWN: Staf Operator Logistik membawa kardus
        const human = buildHuman({ team, role: 'pawn' });
        root.add(human);
    } else if (type === 'bishop') {
        // BISHOP: Supervisor Gudang dengan Tablet Scanner & Pallet Stacker
        const human = buildHuman({ team, role: 'supervisor' });
        root.add(human);
    } else if (type === 'knight') {
        // KNIGHT: Operator dengan Hand Pallet / Forklift Taktis
        const human = buildHuman({ team, role: 'operator' });
        human.position.z = 0.14;
        root.add(human);

        const cart = new THREE.Mesh(new THREE.BoxGeometry(0.36, 0.24, 0.26), bodyMat);
        cart.position.set(0, 0.16, -0.14);
        cart.castShadow = true;
        root.add(cart);

        const handle = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 0.38, 10), metalMat);
        handle.position.set(0, 0.42, -0.02);
        root.add(handle);
    } else if (type === 'rook') {
        // ROOK: Heavy Logistics Loader + Operator
        const truckBase = new THREE.Mesh(new THREE.BoxGeometry(0.56, 0.28, 0.56), bodyMat);
        truckBase.position.y = 0.18;
        truckBase.castShadow = true;
        root.add(truckBase);

        const cargoBox = buildCardboardBox();
        cargoBox.scale.set(1.6, 1.6, 1.6);
        cargoBox.position.set(0, 0.44, 0.08);
        root.add(cargoBox);

        const operator = buildHuman({ team, role: 'operator' });
        operator.scale.multiplyScalar(0.88);
        operator.position.set(0, 0.12, -0.12);
        root.add(operator);
    } else if (type === 'queen') {
        // QUEEN: Chief Operations Supervisor + AGV Holo Platform
        const agvDeck = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.44, 0.14, 24), metalMat);
        agvDeck.position.y = 0.09;
        root.add(agvDeck);

        const glowRing = new THREE.Mesh(
            new THREE.CylinderGeometry(0.45, 0.45, 0.04, 24),
            new THREE.MeshBasicMaterial({ color: isBlue ? 0x38bdf8 : 0xfacc15 })
        );
        glowRing.position.y = 0.12;
        root.add(glowRing);

        const chief = buildHuman({ team, role: 'supervisor' });
        chief.position.y = 0.10;
        root.add(chief);
    } else if (type === 'king') {
        // KING: WMS Server Rack (Kabinet Server Hitam seperti di foto) + Commander
        const serverRack = new THREE.Mesh(
            new THREE.BoxGeometry(0.44, 1.05, 0.34),
            new THREE.MeshPhongMaterial({ color: 0x0f172a, shininess: 80 })
        );
        serverRack.position.set(-0.12, 0.54, 0.10);
        serverRack.castShadow = true;
        root.add(serverRack);

        // Lampu LED Indikator Server
        const ledMat = new THREE.MeshBasicMaterial({ color: isBlue ? 0x38bdf8 : 0xf97316 });
        for (let i = 0; i < 4; i++) {
            const led = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.03, 0.02), ledMat);
            led.position.set(-0.12, 0.35 + i * 0.16, -0.08);
            root.add(led);
        }

        const commander = buildHuman({ team, role: 'supervisor' });
        commander.position.set(0.16, 0, -0.08);
        root.add(commander);
    }

    // Orientasi menghadap lawan
    root.rotation.y = isBlue ? Math.PI : 0;
    return root;
}

// ============================================================================
// 4. STATE PERMAINAN & PENEMPATAN BIDAK AWAL
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
    mesh.userData = {
        type,
        team,
        gridX: gx,
        gridZ: gz,
        alive: true,
        hasMoved: false
    };
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

// ============================================================================
// 5. ATURAN CATUR FIDE LENGKAP (SKAK, SKAKMAT, STALEMATE, PROMOSI, ROKADE)
// ============================================================================
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

    // 1. PAWN / STAF LOGISTIK
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
    }

    // 2. KNIGHT / FORKLIFT
    else if (type === 'knight') {
        const jumps = [[1, 2], [2, 1], [-1, 2], [-2, 1], [1, -2], [2, -1], [-1, -2], [-2, -1]];
        jumps.forEach(([dx, dz]) => {
            const nx = gx + dx, nz = gz + dz;
            if (inBounds(nx, nz)) {
                if (isEmpty(nx, nz)) valid.push({ x: nx, z: nz, attack: false });
                else if (isEnemy(nx, nz)) valid.push({ x: nx, z: nz, attack: true, target: getPieceAt(nx, nz) });
            }
        });
    }

    // 3. ROOK & QUEEN (Arah Lurus)
    if (type === 'rook' || type === 'queen') {
        const dirs = [[1, 0], [-1, 0], [0, 1], [0, -1]];
        dirs.forEach(([dx, dz]) => {
            let step = 1;
            while (inBounds(gx + dx * step, gz + dz * step)) {
                const nx = gx + dx * step, nz = gz + dz * step;
                if (isEmpty(nx, nz)) {
                    valid.push({ x: nx, z: nz, attack: false });
                } else {
                    if (isEnemy(nx, nz)) valid.push({ x: nx, z: nz, attack: true, target: getPieceAt(nx, nz) });
                    break;
                }
                step++;
            }
        });
    }

    // 4. BISHOP & QUEEN (Arah Diagonal)
    if (type === 'bishop' || type === 'queen') {
        const dirs = [[1, 1], [1, -1], [-1, 1], [-1, -1]];
        dirs.forEach(([dx, dz]) => {
            let step = 1;
            while (inBounds(gx + dx * step, gz + dz * step)) {
                const nx = gx + dx * step, nz = gz + dz * step;
                if (isEmpty(nx, nz)) {
                    valid.push({ x: nx, z: nz, attack: false });
                } else {
                    if (isEnemy(nx, nz)) valid.push({ x: nx, z: nz, attack: true, target: getPieceAt(nx, nz) });
                    break;
                }
                step++;
            }
        });
    }

    // 5. KING / WMS SERVER (+ Rokade / Castling)
    if (type === 'king') {
        const dirs = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]];
        dirs.forEach(([dx, dz]) => {
            const nx = gx + dx, nz = gz + dz;
            if (inBounds(nx, nz)) {
                if (isEmpty(nx, nz)) valid.push({ x: nx, z: nz, attack: false });
                else if (isEnemy(nx, nz)) valid.push({ x: nx, z: nz, attack: true, target: getPieceAt(nx, nz) });
            }
        });

        // Rokade (Castling) jika Raja & Benteng belum bergerak dan jalur bersih
        if (includeCastling && !piece.userData.hasMoved && !isInCheck(team)) {
            const row = team === 'blue' ? 0 : 7;
            // Kingside
            const rookK = getPieceAt(7, row);
            if (rookK && rookK.userData.type === 'rook' && !rookK.userData.hasMoved) {
                if (isEmpty(5, row) && isEmpty(6, row) && !isSquareAttacked(5, row, team) && !isSquareAttacked(6, row, team)) {
                    valid.push({ x: 6, z: row, attack: false, castlingRook: rookK, rookNewX: 5 });
                }
            }
            // Queenside
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

// ============================================================================
// 6. EKSEKUSI LANGKAH, PARTIKEL LEDAKAN, SKAKMAT & AI BOT
// ============================================================================
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
        piece,
        mv,
        sx: piece.position.x,
        sz: piece.position.z,
        ex: targetPos.x,
        ez: targetPos.z,
        progress: 0,
        captured: false
    };
}

function finishMove(m) {
    const piece = m.piece, moveData = m.mv;
    piece.position.set(m.ex, 0.03, m.ez);
    piece.userData.gridX = moveData.x;
    piece.userData.gridZ = moveData.z;
    piece.userData.hasMoved = true;

    // Jika Rokade (Castling), pindahkan Benteng pendamping
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

    // Promosi Pion otomatis menjadi Queen saat mencapai ujung papan
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

    // Evaluasi Skak, Skakmat (Checkmate), dan Remis (Stalemate)
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

// Bot AI Cerdas (Prioritas makan bidak bernilai tinggi & hindari/atasi skak)
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
// 7. INTERAKSI KLIK / SENTUH & HIGHLIGHT PETAK
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
    if (intersects.length === 0) return;

    let hitTile = null;
    for (let i = 0; i < intersects.length; i++) {
        if (intersects[i].object.userData && intersects[i].object.userData.isTile) {
            hitTile = intersects[i].object;
            break;
        }
    }

    // Jika mengklik langsung model pekerja 3D, cari koordinat petaknya
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

    // Cek apakah petak yang diklik adalah tujuan langkah sah dari bidak terpilih
    if (selectedPiece) {
        const chosenMove = validMoves.find(m => m.x === gx && m.z === gz);
        if (chosenMove) {
            startMove(selectedPiece, chosenMove);
            return;
        }
    }

    // Pilih bidak milik tim yang sedang mendapat giliran
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

// ============================================================================
// 8. FUNGSI UI, PRESET KAMERA (TERMASUK ZOOM WAJAH PEKERJA) & RESET
// ============================================================================
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
        camera.position.set(0, 7.2, -7.8);
        controls.target.set(0, 0.4, 0);
    } else if (mode === 'top') {
        camera.position.set(0, 11.5, -0.01);
        controls.target.set(0, 0, 0);
    } else if (mode === 'closeup') {
        // Kamera menyorot langsung ke barisan wajah pekerja dari dekat (seperti screenshot)
        camera.position.set(-0.5, 1.18, -1.15);
        controls.target.set(-0.5, 0.92, -2.5);
    }
    controls.update();
}

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// ============================================================================
// 9. ANIMATION LOOP (IDLE BREATHING, PERGERAKAN MULUS, PARTIKEL)
// ============================================================================
let clock = new THREE.Clock();

function animate() {
    requestAnimationFrame(animate);
    const elapsed = clock.getElapsedTime();

    // Animasi bernapas & menoleh halus agar karakter terlihat hidup seperti manusia asli
    pieces.forEach((p, idx) => {
        if (!p.userData.alive) return;
        const head = p.userData.head;
        if (head) {
            head.rotation.y = Math.sin(elapsed * 1.4 + idx * 1.7) * 0.08;
            head.rotation.x = Math.cos(elapsed * 1.1 + idx) * 0.03;
        }
    });

    // Animasi perpindahan bidak
    if (activeMoveAnim) {
        activeMoveAnim.progress += 0.08;
        const t = Math.min(activeMoveAnim.progress, 1);
        const p = activeMoveAnim.piece;
        p.position.x = activeMoveAnim.sx + (activeMoveAnim.ex - activeMoveAnim.sx) * t;
        p.position.z = activeMoveAnim.sz + (activeMoveAnim.ez - activeMoveAnim.sz) * t;
        p.position.y = 0.03 + Math.sin(t * Math.PI) * 0.28;

        if (t >= 0.7 && !activeMoveAnim.captured) {
            captureVictim(activeMoveAnim);
        }
        if (t >= 1) {
            const done = activeMoveAnim;
            activeMoveAnim = null;
            finishMove(done);
        }
    }

    // Update partikel ledakan
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