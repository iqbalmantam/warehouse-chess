import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="WAREHOUSE COMMAND: UNREAL-BLOOM GLTF ENGINE",
    page_icon="🎮",
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
<title>Warehouse Command: GLTF Skeletal & Bloom Engine</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=Rajdhani:wght@600;700&display=swap" rel="stylesheet">
<style>
    * { box-sizing: border-box; user-select: none; }
    body { margin: 0; padding: 0; overflow: hidden; background: #020408; font-family: 'Rajdhani', sans-serif; color: #f8fafc; }
    #canvas-container { width: 100vw; height: 100vh; display: block; }

    /* LOADING SCREEN AAA */
    #loading-overlay {
        position: fixed; inset: 0; background: radial-gradient(circle at center, #0f172a 0%, #020617 100%);
        z-index: 100; display: flex; flex-direction: column; align-items: center; justify-content: center;
        transition: opacity 0.6s ease;
    }
    #loading-overlay.hidden { opacity: 0; pointer-events: none; }
    .loader-title { font-family: 'Orbitron', sans-serif; font-size: 26px; font-weight: 900; letter-spacing: 4px; color: #38bdf8; margin-bottom: 8px; }
    .loader-sub { font-size: 14px; color: #94a3b8; letter-spacing: 1.5px; margin-bottom: 24px; }
    .progress-wrap { width: 340px; height: 8px; background: #1e293b; border-radius: 4px; overflow: hidden; border: 1px solid rgba(56,189,248,0.4); }
    #progress-bar { width: 10%; height: 100%; background: linear-gradient(90deg, #f59e0b, #38bdf8); transition: width 0.25s; }

    /* CINEMATIC LETTERBOX */
    .cine-bar { position: fixed; left: 0; right: 0; height: 0px; background: #000; z-index: 25; transition: height 0.35s ease; pointer-events: none; }
    #cine-top { top: 0; border-bottom: 1px solid rgba(245, 158, 11, 0.45); }
    #cine-bot { bottom: 0; border-top: 1px solid rgba(245, 158, 11, 0.45); }
    body.combat-mode #cine-top, body.combat-mode #cine-bot { height: 72px; }

    #combat-banner {
        position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%) scale(0.5);
        font-family: 'Orbitron', sans-serif; font-size: 40px; font-weight: 900;
        color: #fff; text-transform: uppercase; letter-spacing: 4px;
        text-shadow: 0 0 25px #ef4444, 0 0 55px #f59e0b;
        opacity: 0; pointer-events: none; z-index: 30; transition: 0.25s; white-space: nowrap;
    }
    #combat-banner.show { opacity: 1; transform: translate(-50%, -50%) scale(1); }

    /* TOP BAR */
    #top-bar {
        position: absolute; top: 0; left: 0; right: 0; height: 64px;
        background: linear-gradient(180deg, rgba(5, 9, 18, 0.95) 0%, rgba(5, 9, 18, 0.7) 100%);
        border-bottom: 1px solid rgba(56, 189, 248, 0.3);
        display: flex; justify-content: space-between; align-items: center;
        padding: 0 22px; z-index: 10; backdrop-filter: blur(10px);
    }
    .brand-cluster { display: flex; align-items: center; gap: 12px; }
    .brand-emblem {
        width: 38px; height: 38px; border-radius: 6px;
        background: linear-gradient(135deg, #f59e0b, #ea580c);
        display: flex; align-items: center; justify-content: center;
        font-family: 'Orbitron', sans-serif; font-weight: 900; font-size: 17px; color: #020617;
    }
    .brand-title h1 { margin: 0; font-family: 'Orbitron', sans-serif; font-size: 15px; font-weight: 800; letter-spacing: 2px; }
    .brand-title span { font-size: 11px; color: #38bdf8; letter-spacing: 1px; display: block; font-weight: 700; }

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

    #unit-inspector {
        position: absolute; top: 80px; left: 18px; width: 270px;
        background: rgba(8, 13, 24, 0.92); border: 1px solid rgba(56, 189, 248, 0.3);
        border-left: 4px solid #38bdf8; border-radius: 8px; padding: 12px 15px; z-index: 10; backdrop-filter: blur(8px);
    }
    .panel-tag { font-family: 'Orbitron', sans-serif; font-size: 9px; color: #64748b; letter-spacing: 1.5px; }
    #insp-name { font-family: 'Orbitron', sans-serif; font-size: 14px; font-weight: 800; margin: 2px 0; color: #fff; }
    #insp-role { font-size: 12px; color: #f59e0b; font-weight: 700; margin-bottom: 6px; }
    #insp-weapon { font-size: 11.5px; color: #38bdf8; margin-bottom: 8px; font-weight: 600; }
    .roster-mini { margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.1); font-size: 11px; color: #cbd5e1; line-height: 1.6; }
    .badge-cls { display: inline-block; width: 64px; color: #fbbf24; font-weight: 700; }

    #ops-panel {
        position: absolute; top: 80px; right: 18px; width: 255px;
        background: rgba(8, 13, 24, 0.92); border: 1px solid rgba(245, 158, 11, 0.3);
        border-right: 4px solid #f59e0b; border-radius: 8px; padding: 12px 15px; z-index: 10;
    }
    #move-history { max-height: 145px; overflow-y: auto; display: flex; flex-direction: column; gap: 4px; margin-top: 6px; }
    .log-entry { background: rgba(15, 23, 42, 0.85); padding: 4px 8px; border-radius: 4px; border-left: 2px solid #475569; font-size: 11px; }
    .log-entry.combat { border-left-color: #ef4444; background: rgba(127, 29, 29, 0.35); color: #fca5a5; font-weight: 700; }

    #bottom-ticker {
        position: absolute; bottom: 16px; left: 50%; transform: translateX(-50%);
        background: rgba(5, 9, 18, 0.95); border: 1px solid rgba(56, 189, 248, 0.35);
        padding: 8px 24px; border-radius: 24px; display: flex; align-items: center; gap: 10px; z-index: 10; font-size: 13px; font-weight: 600;
    }
    .pulse-dot { width: 8px; height: 8px; border-radius: 50%; background: #22c55e; box-shadow: 0 0 10px #22c55e; }
</style>

<!-- THREE.JS + GLTF LOADER + SKELETON UTILS + UNREAL BLOOM POST-PROCESSING -->
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
        <div class="loader-title">LOADING BLENDER .GLB ASSETS</div>
        <div id="loader-status" class="loader-sub">Mengunduh Model Manusia Motion-Capture & Shader Unreal Bloom...</div>
        <div class="progress-wrap"><div id="progress-bar"></div></div>
    </div>

    <div id="cine-top" class="cine-bar"></div>
    <div id="cine-bot" class="cine-bar"></div>
    <div id="combat-banner">⚔️ CRITICAL KNOCKOUT!</div>

    <div id="top-bar">
        <div class="brand-cluster">
            <div class="brand-emblem">WC</div>
            <div class="brand-title">
                <h1>WAREHOUSE COMMAND</h1>
                <span>Blender .GLB Skeletal Motion-Capture + Unreal Bloom Engine</span>
            </div>
        </div>

        <div class="versus-hud">
            <div class="team-score blue"><span>INBOUND</span><span id="score-blue" class="score-pill">16</span></div>
            <div id="turn-banner" class="turn-blue">SHIFT BIRU AKTIF</div>
            <div class="team-score orange"><span id="score-orange" class="score-pill">16</span><span>OUTBOUND</span></div>
        </div>

        <div class="toolbar">
            <button id="btn-ai" class="t-btn active" onclick="toggleAI()">🤖 vs AI Bot</button>
            <button class="t-btn" onclick="demoCombat()">🔥 Demo Duel Sinematik</button>
            <button class="t-btn" onclick="setCameraView('closeup')">🔍 Zoom Karakter Asli</button>
            <button class="t-btn" onclick="setCameraView('perspective')">🎥 Kamera Taktis</button>
            <button class="t-btn" onclick="resetGame()">🔄 Reset</button>
        </div>
    </div>

    <div id="unit-inspector">
        <div class="panel-tag">BLENDER .GLB SKELETAL UNIT</div>
        <h2 id="insp-name">FIELD OPERATOR (.GLB)</h2>
        <div id="insp-role">Motion-Captured Human • Pion</div>
        <div id="insp-weapon">⚡ Aksi: Sprint Tackle & Close Combat</div>
        <div class="roster-mini">
            <div><span class="badge-cls">PION</span> Operator Manusia Asli (.GLB)</div>
            <div><span class="badge-cls">BENTENG</span> Heavy Forklift + Driver (.GLB)</div>
            <div><span class="badge-cls">KUDA</span> Hover Pallet Cruiser + Pilot</div>
            <div><span class="badge-cls">GAJAH</span> Tactical Sniper Specialist (.GLB)</div>
            <div><span class="badge-cls">MENTERI</span> Heavy Loader Mech (Bisa Meninju!)</div>
            <div><span class="badge-cls">RAJA</span> Quantum WMS Server Core</div>
        </div>
    </div>

    <div id="ops-panel">
        <div class="panel-tag">COMBAT TELEMETRY LOG</div>
        <div id="move-history"></div>
    </div>

    <div id="bottom-ticker">
        <div class="pulse-dot"></div>
        <div id="action-log">Memuat aset 3D Blender...</div>
    </div>

    <div id="canvas-container"></div>

<script>
// ============================================================================
// 1. RENDERER & UNREAL ENGINE BLOOM POST-PROCESSING PIPELINE
// ============================================================================
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x03060c);
scene.fog = new THREE.FogExp2(0x03060c, 0.015);

const camera = new THREE.PerspectiveCamera(38, window.innerWidth / window.innerHeight, 0.1, 200);
camera.position.set(0, 10.8, 13.5);

const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 0.9;
renderer.outputEncoding = THREE.sRGBEncoding;
container.appendChild(renderer.domElement);

// Post-Processing Composer dengan UnrealBloomPass (Efek Cahaya Game AAA)
const renderScene = new THREE.RenderPass(scene, camera);
const bloomPass = new THREE.UnrealBloomPass(
    new THREE.Vector2(window.innerWidth, window.innerHeight),
    0.42, // Strength (lembut, tidak silau)
    0.35, // Radius
    0.82  // Threshold (hanya bagian neon/laser/sirine yang berpendar)
);
const composer = new THREE.EffectComposer(renderer);
composer.addPass(renderScene);
composer.addPass(bloomPass);

const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.06;
controls.maxPolarAngle = Math.PI / 2 - 0.03;
controls.minDistance = 2.4;
controls.maxDistance = 24;
controls.target.set(0, 0.6, 0);

// STUDIO THREE-POINT LIGHTING
scene.add(new THREE.HemisphereLight(0xbae6fd, 0x090d16, 0.75));
const dirLight = new THREE.DirectionalLight(0xfff7ed, 1.5);
dirLight.position.set(8, 18, 10);
dirLight.castShadow = true;
dirLight.shadow.mapSize.set(2048, 2048);
const d = 8.2;
Object.assign(dirLight.shadow.camera, { left: -d, right: d, top: d, bottom: -d, near: 2, far: 40 });
dirLight.shadow.bias = -0.0005;
scene.add(dirLight);

const blueRim = new THREE.PointLight(0x38bdf8, 1.4, 25); blueRim.position.set(-9, 5, 8); scene.add(blueRim);
const orangeRim = new THREE.PointLight(0xf59e0b, 1.4, 25); orangeRim.position.set(9, 5, -8); scene.add(orangeRim);

// ============================================================================
// 2. WAREHOUSE ARENA & TACTICAL EPOXY BOARD
// ============================================================================
function makeTileTex(isDark, lbl) {
    const c = document.createElement('canvas'); c.width = 256; c.height = 256;
    const ctx = c.getContext('2d');
    ctx.fillStyle = isDark ? '#090f1d' : '#131d31'; ctx.fillRect(0,0,256,256);
    ctx.strokeStyle = isDark ? '#162238' : '#243554'; ctx.lineWidth = 8; ctx.strokeRect(4,4,248,248);
    ctx.fillStyle = 'rgba(56, 189, 248, 0.3)';
    ctx.fillRect(14,14,16,3); ctx.fillRect(14,14,3,16);
    if (lbl) {
        ctx.fillStyle = 'rgba(148,163,184,0.55)';
        ctx.font = 'bold 28px Orbitron, monospace'; ctx.fillText(lbl, 18, 234);
    }
    return new THREE.CanvasTexture(c);
}

const boardGroup = new THREE.Group(); scene.add(boardGroup);
const floor = new THREE.Mesh(new THREE.PlaneGeometry(80, 80), new THREE.MeshStandardMaterial({ color: 0x04070e, roughness: 0.75 }));
floor.rotation.x = -Math.PI/2; floor.position.y = -0.35; floor.receiveShadow = true; scene.add(floor);

const base = new THREE.Mesh(new THREE.BoxGeometry(10.5, 0.35, 10.5), new THREE.MeshStandardMaterial({ color: 0x080d1a, roughness: 0.35, metalness: 0.6 }));
base.position.y = -0.2; base.receiveShadow = true; boardGroup.add(base);

const tileSize = 1.2, offset = 3.5 * tileSize, tiles = [], cols = ['A','B','C','D','E','F','G','H'];
for (let x = 0; x < 8; x++) {
    tiles[x] = [];
    for (let z = 0; z < 8; z++) {
        const isDark = (x + z) % 2 === 1;
        const lbl = (z === 7) ? cols[x] : (x === 0 ? String(8 - z) : '');
        const tile = new THREE.Mesh(
            new THREE.BoxGeometry(tileSize * 0.985, 0.1, tileSize * 0.985),
            new THREE.MeshStandardMaterial({ map: makeTileTex(isDark, lbl), roughness: 0.4, metalness: 0.2 })
        );
        tile.position.set(x * tileSize - offset, 0, z * tileSize - offset);
        tile.receiveShadow = true; tile.userData = { gridX: x, gridZ: z };
        boardGroup.add(tile); tiles[x][z] = tile;
    }
}

// Rak Gudang Industri di Kiri & Kanan
function buildRack(xPos, zPos, rotY) {
    const r = new THREE.Group();
    const uMat = new THREE.MeshStandardMaterial({ color: 0x1d4ed8, roughness: 0.35, metalness: 0.5 });
    const bMat = new THREE.MeshStandardMaterial({ color: 0xea580c, roughness: 0.35, metalness: 0.4 });
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
// 3. REAL BLENDER .GLB ASSET LOADER (SOLDIER.GLB & ROBOTEXPRESSIVE.GLB)
// ============================================================================
let soldierAsset = null;
let mechAsset = null;
const mixers = [];
const animatedParts = [];

const mats = {
    blackSteel: new THREE.MeshStandardMaterial({ color: 0x0f172a, metalness: 0.8, roughness: 0.25 }),
    chrome: new THREE.MeshStandardMaterial({ color: 0xf8fafc, metalness: 0.95, roughness: 0.1 }),
    rubber: new THREE.MeshStandardMaterial({ color: 0x090d16, roughness: 0.9 }),
    cardboard: new THREE.MeshStandardMaterial({ color: 0xb48352, roughness: 0.75 }),
    gold: new THREE.MeshStandardMaterial({ color: 0xf59e0b, metalness: 0.85, roughness: 0.2 }),
    neonBlue: new THREE.MeshStandardMaterial({ color: 0x38bdf8, emissive: 0x0284c7, emissiveIntensity: 2.2 }),
    neonOrange: new THREE.MeshStandardMaterial({ color: 0xfbbf24, emissive: 0xd97706, emissiveIntensity: 2.2 }),
    laserRed: new THREE.MeshStandardMaterial({ color: 0xef4444, emissive: 0xdc2626, emissiveIntensity: 2.8 })
};

const gltfLoader = new THREE.GLTFLoader();

function loadAllBlenderAssets() {
    const pBar = document.getElementById('progress-bar');
    const pStatus = document.getElementById('loader-status');

    // 1. Unduh Model Manusia Motion-Capture Asli (Soldier.glb dari repo resmi Three.js)
    const soldierURL = 'https://raw.githubusercontent.com/mrdoob/three.js/r128/examples/models/gltf/Soldier.glb';
    // 2. Unduh Model Heavy Loader Mech dengan Animasi Punch/Combat (RobotExpressive.glb)
    const mechURL = 'https://raw.githubusercontent.com/mrdoob/three.js/r128/examples/models/gltf/RobotExpressive/RobotExpressive.glb';

    Promise.all([
        new Promise(res => gltfLoader.load(soldierURL, g => { pBar.style.width = '55%'; res(g); }, undefined, () => res(null))),
        new Promise(res => gltfLoader.load(mechURL, g => { pBar.style.width = '100%'; res(g); }, undefined, () => res(null)))
    ]).then(([sGltf, mGltf]) => {
        soldierAsset = sGltf;
        mechAsset = mGltf;
        pStatus.innerText = "Aset 3D Blender siap! Memulai simulasi...";
        setTimeout(() => {
            document.getElementById('loading-overlay').classList.add('hidden');
            resetGame();
        }, 300);
    });
}

// Fungsi Kloning Karakter Manusia .GLB Asli + Kostumisasi Seragam Tim & Animasi Tulang
function spawnRealHumanGLB(team, scaleVal, tintColorHex, helmetColorHex) {
    const wrapper = new THREE.Group();
    if (!soldierAsset) return { wrapper, setAnim: () => {} };

    const clonedScene = THREE.SkeletonUtils.clone(soldierAsset.scene);
    clonedScene.scale.set(scaleVal, scaleVal, scaleVal);
    // Model Soldier.glb menghadap +Z secara default, putar agar sesuai arah
    clonedScene.rotation.y = Math.PI;

    clonedScene.traverse(child => {
        if (child.isMesh) {
            child.castShadow = true;
            child.receiveShadow = true;
            // Beri aksen warna tim pada material seragam asli tanpa merusak tekstur detailnya
            child.material = child.material.clone();
            child.material.color.lerp(new THREE.Color(tintColorHex), 0.35);
        }
    });
    wrapper.add(clonedScene);

    // Pasang Helm Safety / Topi Taktis di atas kepala agar pembeda kelas makin jelas
    if (helmetColorHex) {
        const badgeRing = new THREE.Mesh(
            new THREE.CylinderGeometry(0.14, 0.14, 0.03, 16),
            new THREE.MeshStandardMaterial({ color: helmetColorHex, emissive: helmetColorHex, emissiveIntensity: 0.8 })
        );
        badgeRing.position.set(0, 1.05 * scaleVal, 0);
        wrapper.add(badgeRing);
    }

    // Setup AnimationMixer untuk menggerakkan tulang (Idle, Walk, Run)
    const mixer = new THREE.AnimationMixer(clonedScene);
    const clips = soldierAsset.animations;
    const actions = {
        Idle: mixer.clipAction(THREE.AnimationClip.findByName(clips, 'Idle') || clips[0]),
        Walk: mixer.clipAction(THREE.AnimationClip.findByName(clips, 'Walk') || clips[3]),
        Run:  mixer.clipAction(THREE.AnimationClip.findByName(clips, 'Run')  || clips[1])
    };
    actions.Idle.play();
    mixers.push(mixer);

    let currentAct = actions.Idle;
    function setAnim(name) {
        const next = actions[name];
        if (next && next !== currentAct) {
            currentAct.fadeOut(0.18);
            next.reset().fadeIn(0.18).play();
            currentAct = next;
        }
    }

    return { wrapper, setAnim };
}

// Fungsi Kloning Heavy Loader Mech (.GLB) yang Punya Animasi PUNCH / MENINJU Asli!
function spawnRealMechGLB(team) {
    const wrapper = new THREE.Group();
    if (!mechAsset) return { wrapper, setAnim: () => {} };

    const cloned = THREE.SkeletonUtils.clone(mechAsset.scene);
    cloned.scale.set(0.24, 0.24, 0.24);

    const tint = team === 'blue' ? 0x0284c7 : 0xea580c;
    cloned.traverse(c => {
        if (c.isMesh) {
            c.castShadow = true; c.receiveShadow = true;
            c.material = c.material.clone();
            if (c.material.name && c.material.name.includes('Main')) {
                c.material.color.setHex(tint);
            }
        }
    });
    wrapper.add(cloned);

    const mixer = new THREE.AnimationMixer(cloned);
    const clips = mechAsset.animations;
    const actions = {
        Idle:  mixer.clipAction(THREE.AnimationClip.findByName(clips, 'Idle')),
        Run:   mixer.clipAction(THREE.AnimationClip.findByName(clips, 'Running')),
        Punch: mixer.clipAction(THREE.AnimationClip.findByName(clips, 'Punch')),
        Jump:  mixer.clipAction(THREE.AnimationClip.findByName(clips, 'Jump'))
    };
    if (actions.Idle) actions.Idle.play();
    mixers.push(mixer);

    let cur = actions.Idle;
    function setAnim(name) {
        const next = actions[name];
        if (next && next !== cur) {
            if (cur) cur.fadeOut(0.15);
            next.reset().fadeIn(0.15).play();
            cur = next;
        }
    }
    return { wrapper, setAnim };
}

// ============================================================================
// 4. PEMBANGUN 6 UNIT LOGISTIK DENGAN SILUET & GERAKAN SANGAT BERBEDA
// ============================================================================
function createUnitMesh(type, team) {
    const root = new THREE.Group();
    const isBlue = team === 'blue';
    const teamColor = isBlue ? 0x0284c7 : 0xea580c;
    const glowMat = isBlue ? mats.neonBlue : mats.neonOrange;
    const teamMat = new THREE.MeshStandardMaterial({ color: teamColor, roughness: 0.3, metalness: 0.5 });

    // Base Neon Ring (Berpendar dengan Unreal Bloom!)
    const ring = new THREE.Mesh(new THREE.TorusGeometry(0.46, 0.02, 12, 32), glowMat);
    ring.rotation.x = Math.PI / 2; ring.position.y = 0.02;
    root.add(ring);

    const dir = new THREE.Group();
    dir.rotation.y = isBlue ? 0 : Math.PI;
    root.add(dir);

    // 1. PION: MANUSIA ASLI (.GLB) + PETI KARGO DI DEPAN
    if (type === 'pawn') {
        const human = spawnRealHumanGLB(team, 0.58, isBlue ? 0x38bdf8 : 0xfbbf24, null);
        dir.add(human.wrapper);

        // Peti Kargo Taktis di samping kaki
        const crate = new THREE.Mesh(new THREE.BoxGeometry(0.24, 0.22, 0.24), mats.cardboard);
        crate.position.set(0.22, 0.12, -0.15); crate.castShadow = true;
        dir.add(crate);

        root.userData.setAnim = human.setAnim;
    }

    // 2. BENTENG: HEAVY ARMORED FORKLIFT + MANUSIA ASLI (.GLB) DI DALAM KABIN
    else if (type === 'rook') {
        const vehicle = new THREE.Group();
        dir.add(vehicle);

        // 4 Roda Tebal
        [[-0.32, 0.16, -0.24], [0.32, 0.16, -0.24], [-0.3, 0.13, 0.28], [0.3, 0.13, 0.28]].forEach(([wx, wy, wz]) => {
            const w = new THREE.Mesh(new THREE.CylinderGeometry(wy, wy, 0.12, 20), mats.rubber);
            w.rotation.z = Math.PI/2; w.position.set(wx, wy, wz); vehicle.add(w);
        });

        const chassis = new THREE.Mesh(new THREE.BoxGeometry(0.58, 0.28, 0.7), teamMat);
        chassis.position.set(0, 0.26, 0.05); chassis.castShadow = true; vehicle.add(chassis);

        // Operator Manusia .GLB Mengemudi Forklift
        const driver = spawnRealHumanGLB(team, 0.45, isBlue ? 0x0284c7 : 0xd97706, null);
        driver.wrapper.position.set(0, 0.32, 0.05);
        vehicle.add(driver.wrapper);

        // Roll-Cage & Sirine Neon
        const roof = new THREE.Mesh(new THREE.BoxGeometry(0.52, 0.04, 0.48), mats.blackSteel);
        roof.position.set(0, 1.05, 0.05); vehicle.add(roof);
        const beacon = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.06, 0.09, 12), glowMat);
        beacon.position.set(0, 1.11, 0.18); vehicle.add(beacon);

        // Garpu Baja Hidrolik
        const forkPivot = new THREE.Group();
        forkPivot.position.set(0, 0.14, -0.34);
        vehicle.add(forkPivot);
        [-0.18, 0.18].forEach(fx => {
            const mast = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.96, 0.06), mats.blackSteel);
            mast.position.set(fx, 0.45, 0); vehicle.add(mast);
            const blade = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.03, 0.46), mats.chrome);
            blade.position.set(fx, 0, -0.22); forkPivot.add(blade);
        });

        root.userData.forkPivot = forkPivot;
        root.userData.setAnim = driver.setAnim;
    }

    // 3. KUDA: HOVER PALLET CRUISER + PILOT MANUSIA (.GLB)
    else if (type === 'knight') {
        const speeder = new THREE.Group();
        dir.add(speeder);

        // Thruster Hover Neon di Bawah Palet
        const deck = new THREE.Mesh(new THREE.BoxGeometry(0.48, 0.1, 0.78), mats.blackSteel);
        deck.position.set(0, 0.14, 0); speeder.add(deck);
        const neonTrim = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.04, 0.8), glowMat);
        neonTrim.position.set(0, 0.11, 0); speeder.add(neonTrim);

        // Kargo Depan & Stang
        const cowl = new THREE.Mesh(new THREE.ConeGeometry(0.24, 0.45, 6), teamMat);
        cowl.rotation.x = -Math.PI/2; cowl.position.set(0, 0.34, -0.25); speeder.add(cowl);

        // Pilot Manusia .GLB di Belakang
        const pilot = spawnRealHumanGLB(team, 0.52, isBlue ? 0x38bdf8 : 0xfbbf24, null);
        pilot.wrapper.position.set(0, 0.18, 0.16);
        speeder.add(pilot.wrapper);

        animatedParts.push({ mesh: speeder, type: 'hover', baseY: 0.04 });
        root.userData.setAnim = pilot.setAnim;
    }

    // 4. GAJAH: TACTICAL QC SNIPER (.GLB) + LASER CANNON + FLOATING DRONE
    else if (type === 'bishop') {
        const sniper = spawnRealHumanGLB(team, 0.63, 0xffffff, 0xef4444);
        dir.add(sniper.wrapper);

        // Meriam Laser Kalibrasi di Samping Bahu
        const laserPod = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.06, 0.55, 12), mats.blackSteel);
        laserPod.rotation.x = Math.PI/2; laserPod.position.set(0.2, 0.78, -0.15);
        const tip = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.15, 12), mats.laserRed);
        tip.position.y = -0.3; laserPod.add(tip);
        dir.add(laserPod);

        root.userData.setAnim = sniper.setAnim;
    }

    // 5. MENTERI (QUEEN): HEAVY WAREHOUSE LOADER MECH (.GLB DENGAN ANIMASI PUNCH ASLI!)
    else if (type === 'queen') {
        const mech = spawnRealMechGLB(team);
        dir.add(mech.wrapper);
        root.userData.setAnim = mech.setAnim;
        root.userData.isMech = true;
    }

    // 6. RAJA (KING): QUANTUM WMS SERVER CITADEL + PENGAWAL
    else if (type === 'king') {
        const citadel = new THREE.Group();
        dir.add(citadel);

        const tower = new THREE.Mesh(new THREE.BoxGeometry(0.5, 1.05, 0.5), mats.blackSteel);
        tower.position.y = 0.55; tower.castShadow = true; citadel.add(tower);

        for (let i = 0; i < 6; i++) {
            const blade = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.03, 0.52), glowMat);
            blade.position.set(0, 0.2 + i * 0.14, 0); citadel.add(blade);
        }

        const core = new THREE.Mesh(new THREE.OctahedronGeometry(0.22, 1), glowMat);
        core.position.y = 1.35; citadel.add(core);
        animatedParts.push({ mesh: core, type: 'spin' });
    }

    return root;
}

// ============================================================================
// 5. EPIC MOTION-CAPTURE COMBAT ENGINE (LARI SUNGGUHAN -> PUKULAN -> RAGDOLL)
// ============================================================================
let pieces = [], selectedPiece = null, validMoves = [], currentTurn = 'blue', isAnimating = false, vsAI = true, highlights = [];

const unitSpecs = {
    pawn:   { name: 'FIELD OPERATOR (.GLB)', role: 'Motion-Capture Human • Pion', wpn: '⚡ Tactical Sprint & Close Takedown' },
    rook:   { name: 'ARMORED FORKLIFT', role: 'Heavy Juggernaut • Benteng', wpn: '⚡ Hydraulic Fork Lift & Throw' },
    knight: { name: 'HOVER PALLET CRUISER', role: 'High-Speed Raider • Kuda', wpn: '⚡ Supersonic Hover Ram' },
    bishop: { name: 'QC LASER SPECIALIST', role: 'Precision Marksman • Gajah', wpn: '⚡ High-Energy Red Laser Beam' },
    queen:  { name: 'HEAVY LOADER MECH (.GLB)', role: 'Exoskeleton Commander • Menteri', wpn: '⚡ Heavy Hydraulic Fist Punch' },
    king:   { name: 'QUANTUM WMS SERVER', role: 'Central Mainframe • Raja', wpn: '⚡ EMP Shockwave' }
};
const weights = { pawn: 10, knight: 30, bishop: 30, rook: 50, queen: 90, king: 900 };

function showCombatBanner(text) {
    const b = document.getElementById('combat-banner');
    b.innerText = text;
    b.classList.add('show');
    setTimeout(() => b.classList.remove('show'), 1100);
}

function spawnImpactFX(pos, isRed = false) {
    const ringGeo = new THREE.RingGeometry(0.1, 0.25, 28);
    const ringMat = new THREE.MeshBasicMaterial({ color: isRed ? 0xef4444 : 0x38bdf8, side: THREE.DoubleSide, transparent: true, opacity: 0.95 });
    const ring = new THREE.Mesh(ringGeo, ringMat);
    ring.rotation.x = -Math.PI / 2; ring.position.set(pos.x, 0.08, pos.z);
    scene.add(ring);

    let sc = 1;
    const expand = () => {
        sc += 0.4; ring.scale.set(sc, sc, sc); ringMat.opacity -= 0.06;
        if (ringMat.opacity > 0) requestAnimationFrame(expand); else scene.remove(ring);
    };
    expand();

    for (let i = 0; i < 24; i++) {
        const p = new THREE.Mesh(new THREE.BoxGeometry(0.11, 0.11, 0.11), i % 2 === 0 ? mats.neonOrange : mats.laserRed);
        p.position.set(pos.x, pos.y + 0.55, pos.z); scene.add(p);
        const vx = (Math.random() - 0.5) * 0.34, vz = (Math.random() - 0.5) * 0.34;
        let vy = Math.random() * 0.28 + 0.08;
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

    const startX = attacker.position.x, startZ = attacker.position.z;
    const endX = targetX * tileSize - offset, endZ = targetZ * tileSize - offset;
    const dx = endX - startX, dz = endZ - startZ;
    const dist = Math.hypot(dx, dz) || 1;
    const dirX = dx / dist, dirZ = dz / dist;

    const duelX = endX - dirX * 0.72;
    const duelZ = endZ - dirZ * 0.72;

    const angleToDef = Math.atan2(dx, dz);
    attacker.children[1].rotation.y = angleToDef + Math.PI;
    defender.children[1].rotation.y = angleToDef;

    // Kamera Close-Up Action
    camera.position.set(endX + dirZ * 2.5 - dirX * 1.1, 2.0, endZ - dirX * 2.5 - dirZ * 1.1);
    controls.target.set((duelX + endX) * 0.5, 0.65, (duelZ + endZ) * 0.5);
    controls.update();

    // Aktifkan Animasi LARI Motion-Capture Asli!
    if (attacker.userData.setAnim) attacker.userData.setAnim('Run');

    let p1 = 0;
    const phase1Run = () => {
        p1 += 0.055;
        if (p1 < 1) {
            attacker.position.x = startX + (duelX - startX) * p1;
            attacker.position.z = startZ + (duelZ - startZ) * p1;
            requestAnimationFrame(phase1Run);
        } else {
            attacker.position.set(duelX, 0.05, duelZ);
            // Jika Mech (Menteri), mainkan animasi PUNCH asli!
            if (attacker.userData.isMech && attacker.userData.setAnim) {
                attacker.userData.setAnim('Punch');
            }
            phase2Climax();
        }
    };

    let p2 = 0;
    let laserBeam = null;
    if (attacker.userData.type === 'bishop') {
        laserBeam = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, 1.3, 12), mats.laserRed);
        laserBeam.rotation.x = Math.PI / 2;
        laserBeam.position.set((duelX + endX)*0.5, 0.78, (duelZ + endZ)*0.5);
        laserBeam.lookAt(endX, 0.78, endZ);
        scene.add(laserBeam);
    }

    const phase2Climax = () => {
        p2 += 0.05;
        if (attacker.userData.forkPivot) {
            attacker.userData.forkPivot.position.y = 0.14 + Math.min(0.65, p2 * 0.85);
            defender.position.y = 0.05 + Math.min(0.75, p2 * 0.9);
        }
        if (Math.abs(p2 - 0.5) < 0.03) spawnImpactFX(defender.position, false);

        if (p2 < 1.0) {
            requestAnimationFrame(phase2Climax);
        } else {
            if (laserBeam) scene.remove(laserBeam);
            if (attacker.userData.forkPivot) attacker.userData.forkPivot.position.y = 0.14;
            if (attacker.userData.setAnim) attacker.userData.setAnim('Idle');

            showCombatBanner("💥 CRITICAL KNOCKOUT!");
            spawnImpactFX(defender.position, true);
            phase3FlyAway();
        }
    };

    let p3 = 0;
    const phase3FlyAway = () => {
        p3 += 0.06;
        defender.position.x = endX + dirX * (p3 * 3.0);
        defender.position.z = endZ + dirZ * (p3 * 3.0);
        defender.position.y = 0.2 + Math.sin(p3 * Math.PI) * 1.7;
        defender.rotation.x += 0.24;
        defender.scale.multiplyScalar(0.94);

        attacker.position.x = duelX + (endX - duelX) * Math.min(1, p3 * 1.5);
        attacker.position.z = duelZ + (endZ - duelZ) * Math.min(1, p3 * 1.5);

        if (p3 < 1.0) {
            requestAnimationFrame(phase3FlyAway);
        } else {
            defender.userData.alive = false;
            scene.remove(defender);
            attacker.position.set(endX, 0.05, endZ);
            attacker.children[1].rotation.y = attacker.userData.team === 'blue' ? 0 : Math.PI;

            setTimeout(() => {
                document.body.classList.remove('combat-mode');
                camera.position.set(0, 10.8, 13.5);
                controls.target.set(0, 0.6, 0);
                controls.update();
                onComplete();
            }, 300);
        }
    };

    phase1Run();
}

// ============================================================================
// 6. CHESS RULES & GAMEPLAY CONTROLLERS
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
            new THREE.MeshBasicMaterial({ color: m.attack ? 0xef4444 : 0x22c55e, transparent: true, opacity: 0.5, side: THREE.DoubleSide })
        );
        mk.rotation.x = -Math.PI/2; mk.position.set(m.x * tileSize - offset, 0.065, m.z * tileSize - offset);
        scene.add(mk); highlights.push(mk);
    });
}

function executeMove(piece, moveData) {
    isAnimating = true; clearHighlights();
    const uName = unitSpecs[piece.userData.type].name;
    const coord = `${cols[moveData.x]}${8 - moveData.z}`;

    if (moveData.attack && moveData.target) {
        const victim = moveData.target;
        const vName = unitSpecs[victim.userData.type].name;
        updateHUD(`⚔️ DUEL MOTION-CAPTURE: ${uName} menyerang ${vName}!`);

        playEpicCombatSequence(piece, victim, moveData.x, moveData.z, () => {
            piece.userData.gridX = moveData.x;
            piece.userData.gridZ = moveData.z;
            piece.userData.hasMoved = true;

            addBattleLog(`${uName} 💥 KO ${vName} (${coord})`, true);
            updateScoreUI();

            if (victim.userData.type === 'king') {
                updateHUD(`🏆 VICTORY! Tim ${currentTurn.toUpperCase()} menguasai Quantum WMS Server!`);
                isAnimating = false; return;
            }

            currentTurn = currentTurn === 'blue' ? 'orange' : 'blue';
            selectedPiece = null; validMoves = []; isAnimating = false;
            updateHUD(`💥 ${uName} memenangkan pertarungan di zona ${coord}!`);
            if (vsAI && currentTurn === 'orange') setTimeout(runAIBot, 450);
        });
        return;
    }

    // Berjalan dengan Animasi Langkah Kaki Motion-Capture Asli!
    const sx = piece.position.x, sz = piece.position.z;
    const ex = moveData.x * tileSize - offset, ez = moveData.z * tileSize - offset;
    const walkAngle = Math.atan2(ex - sx, ez - sz);
    piece.children[1].rotation.y = walkAngle + Math.PI;

    if (piece.userData.setAnim) piece.userData.setAnim('Run');

    let prog = 0;
    const step = () => {
        prog += 0.05;
        if (prog < 1) {
            piece.position.x = sx + (ex - sx) * prog;
            piece.position.z = sz + (ez - sz) * prog;
            requestAnimationFrame(step);
        } else {
            if (piece.userData.setAnim) piece.userData.setAnim('Idle');
            piece.children[1].rotation.y = piece.userData.team === 'blue' ? 0 : Math.PI;
            piece.position.set(ex, 0.05, ez);
            piece.userData.gridX = moveData.x; piece.userData.gridZ = moveData.z; piece.userData.hasMoved = true;

            addBattleLog(`${uName} ➔ ${coord}`, false);
            currentTurn = currentTurn === 'blue' ? 'orange' : 'blue';
            selectedPiece = null; validMoves = []; isAnimating = false;
            updateHUD(`${uName} bergerak menuju ${coord}.`);
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

    // Utamakan memilih Mech (Menteri) atau Operator .GLB agar terlihat aksi pukulannya
    const atk = blueUnits.find(p => p.userData.type === 'queen') || blueUnits[0];
    const def = orangeUnits[Math.floor(Math.random() * orangeUnits.length)];
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
    addBattleLog("Engine .GLB Blender + Unreal Bloom Aktif.");
    updateHUD("Karakter Manusia Motion-Capture (.GLB) siap! Klik '🔍 Zoom Karakter Asli' atau '🔥 Demo Duel Sinematik'.");
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
        camera.position.set(-1.2, 2.1, 5.8); controls.target.set(-0.6, 0.65, 3.6);
    } else {
        camera.position.set(0, 10.8, 13.5); controls.target.set(0, 0.6, 0);
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
loadAllBlenderAssets();

function animate() {
    requestAnimationFrame(animate);
    const delta = clock.getDelta();
    const elapsed = clock.getElapsedTime();

    // Update semua Skeletal Animation Mixer (.GLB Motion Capture!)
    mixers.forEach(m => m.update(delta));

    animatedParts.forEach(p => {
        if (p.type === 'spin') { p.mesh.rotation.y = elapsed * 2.2; p.mesh.rotation.x = elapsed * 1.1; }
        else if (p.type === 'hover') { p.mesh.position.y = p.baseY + Math.sin(elapsed * 3.5) * 0.05; }
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
