import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Warehouse Logistics Chess 3D",
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
<title>Warehouse Logistics Chess 3D</title>
<style>
    * { box-sizing: border-box; user-select: none; }
    body { margin: 0; padding: 0; overflow: hidden; background: #070b12; font-family: 'Segoe UI', sans-serif; color: #f8fafc; }
    #canvas-container { width: 100vw; height: 100vh; display: block; }
    #hud-top { position: absolute; top: 16px; left: 20px; right: 20px; display: flex; justify-content: space-between; align-items: flex-start; pointer-events: none; z-index: 10; flex-wrap: wrap; gap: 10px; }
    .brand-box { background: rgba(15, 23, 42, 0.88); border-left: 5px solid #f59e0b; padding: 10px 18px; border-radius: 8px; box-shadow: 0 10px 25px rgba(0,0,0,0.6); backdrop-filter: blur(8px); }
    .brand-box h1 { margin: 0; font-size: 18px; font-weight: 800; letter-spacing: 1px; text-transform: uppercase; color: #f59e0b; }
    .brand-box p { margin: 3px 0 0 0; font-size: 12px; color: #94a3b8; }
    .controls-box { pointer-events: auto; display: flex; gap: 8px; flex-wrap: wrap; }
    .btn { background: rgba(30, 41, 59, 0.92); border: 1px solid #475569; color: #e2e8f0; padding: 8px 14px; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 12px; transition: 0.2s; }
    .btn:hover { background: #334155; border-color: #38bdf8; color: #fff; }
    .btn.active { background: #0284c7; border-color: #38bdf8; color: #fff; }
    #legend-panel { position: absolute; top: 92px; left: 20px; background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255,255,255,0.08); padding: 10px 14px; border-radius: 8px; font-size: 11px; color: #cbd5e1; pointer-events: none; line-height: 1.6; }
    .key-role { color: #f59e0b; font-weight: bold; }
    #hud-bottom { position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); background: rgba(15, 23, 42, 0.92); border: 1px solid rgba(255,255,255,0.12); padding: 12px 24px; border-radius: 10px; box-shadow: 0 12px 30px rgba(0,0,0,0.7); display: flex; align-items: center; gap: 16px; z-index: 10; white-space: nowrap; }
    .shift-badge { padding: 5px 12px; border-radius: 6px; font-weight: 800; font-size: 12px; text-transform: uppercase; }
    .shift-blue { background: rgba(2, 132, 199, 0.25); color: #38bdf8; border: 1px solid #0284c7; }
    .shift-orange { background: rgba(217, 119, 6, 0.25); color: #fbbf24; border: 1px solid #d97706; }
    #action-log { font-size: 13px; color: #e2e8f0; }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>
    <div id="hud-top">
        <div class="brand-box">
            <h1>Warehouse Tactical Chess 3D</h1>
            <p>Blender PBR Procedural Graphics • Warehouse Operations</p>
        </div>
        <div class="controls-box">
            <button id="btn-ai" class="btn active" onclick="toggleAI()">🤖 Mode: vs AI Bot</button>
            <button class="btn" onclick="setCameraView('perspective')">🎥 Kamera 3D</button>
            <button class="btn" onclick="setCameraView('top')">📐 Denah Atas</button>
            <button class="btn" onclick="resetGame()">🔄 Reset Shift</button>
        </div>
    </div>

    <div id="legend-panel">
        <div><span class="key-role">Pion:</span> Operator Picker (Bawa Kardus)</div>
        <div><span class="key-role">Benteng:</span> Heavy Forklift (Reach Truck)</div>
        <div><span class="key-role">Kuda:</span> Electric Hand Pallet Jack</div>
        <div><span class="key-role">Gajah:</span> QC Checker (Barcode Laser)</div>
        <div><span class="key-role">Menteri:</span> Warehouse Ops Supervisor</div>
        <div><span class="key-role">Raja:</span> Main WMS Server Rack</div>
    </div>

    <div id="hud-bottom">
        <div id="turn-badge" class="shift-badge shift-blue">SHIFT BIRU (INBOUND)</div>
        <div id="action-log">Klik unit Biru untuk memulai operasional...</div>
    </div>

    <div id="canvas-container"></div>

<script>
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x090d16);
scene.fog = new THREE.FogExp2(0x090d16, 0.018);

const camera = new THREE.PerspectiveCamera(42, window.innerWidth / window.innerHeight, 0.1, 200);
camera.position.set(0, 13, 14);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.15;
container.appendChild(renderer.domElement);

const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.maxPolarAngle = Math.PI / 2 - 0.04;
controls.minDistance = 6;
controls.maxDistance = 28;

// LIGHTING
scene.add(new THREE.HemisphereLight(0xdbeafe, 0x0f172a, 0.6));
const mainSpot = new THREE.DirectionalLight(0xfffbeb, 1.3);
mainSpot.position.set(10, 22, 12);
mainSpot.castShadow = true;
mainSpot.shadow.mapSize.set(2048, 2048);
const d = 8.5;
Object.assign(mainSpot.shadow.camera, { left: -d, right: d, top: d, bottom: -d, near: 2, far: 45 });
scene.add(mainSpot);

const rim1 = new THREE.PointLight(0x38bdf8, 1.4, 25); rim1.position.set(-9, 8, 9); scene.add(rim1);
const rim2 = new THREE.PointLight(0xf59e0b, 1.4, 25); rim2.position.set(9, 8, -9); scene.add(rim2);

// TEXTURES
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
    ctx.strokeStyle = isDark ? '#334155' : '#475569'; ctx.lineWidth = 6; ctx.strokeRect(8,8,240,240);
    ctx.fillStyle = 'rgba(250, 204, 21, 0.25)'; ctx.fillRect(14,14,12,4); ctx.fillRect(14,14,4,12);
    if (lbl) { ctx.fillStyle = 'rgba(148,163,184,0.4)'; ctx.font = 'bold 28px monospace'; ctx.fillText(lbl, 20, 236); }
    return new THREE.CanvasTexture(c);
}

// BOARD & WAREHOUSE FLOOR
const boardGroup = new THREE.Group(); scene.add(boardGroup);
const floor = new THREE.Mesh(new THREE.PlaneGeometry(60,60), new THREE.MeshStandardMaterial({ color: 0x0b111e, roughness: 0.4 }));
floor.rotation.x = -Math.PI/2; floor.position.y = -0.35; floor.receiveShadow = true; scene.add(floor);

const base = new THREE.Mesh(new THREE.BoxGeometry(10.6, 0.35, 10.6), new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.2, metalness: 0.5 }));
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
            new THREE.MeshStandardMaterial({ map: makeTileTex(isDark, lbl), roughness: isDark ? 0.18 : 0.26, metalness: 0.15 })
        );
        tile.position.set(x * tileSize - offset, 0, z * tileSize - offset);
        tile.receiveShadow = true;
        tile.userData = { gridX: x, gridZ: z };
        boardGroup.add(tile);
        tiles[x][z] = tile;
    }
}

// SELECTIVE PALLET RACKING DECORATION
function buildRack(xPos, zPos, rotY) {
    const r = new THREE.Group();
    const uMat = new THREE.MeshStandardMaterial({ color: 0x1d4ed8, metalness: 0.6, roughness: 0.3 });
    const bMat = new THREE.MeshStandardMaterial({ color: 0xea580c, metalness: 0.4, roughness: 0.3 });
    const cMat = new THREE.MeshStandardMaterial({ color: 0xb48352, roughness: 0.8 });
    [-1.8, 0, 1.8].forEach(lx => [-0.4, 0.4].forEach(lz => {
        const p = new THREE.Mesh(new THREE.BoxGeometry(0.1, 3.6, 0.1), uMat);
        p.position.set(lx, 1.8, lz); p.castShadow = true; r.add(p);
    }));
    [0.8, 1.9, 3.0].forEach(ly => {
        [-0.4, 0.4].forEach(bz => {
            const bm = new THREE.Mesh(new THREE.BoxGeometry(3.7, 0.09, 0.08), bMat);
            bm.position.set(0, ly, bz); r.add(bm);
        });
        [-1.1, 0, 1.1].forEach(bx => {
            const bxMesh = new THREE.Mesh(new THREE.BoxGeometry(0.65, 0.5, 0.65), cMat);
            bxMesh.position.set(bx, ly + 0.3, 0); bxMesh.castShadow = true; r.add(bxMesh);
        });
    });
    r.position.set(xPos, -0.35, zPos); r.rotation.y = rotY; scene.add(r);
}
buildRack(-7.5, -2.3, Math.PI/2); buildRack(-7.5, 2.3, Math.PI/2);
buildRack(7.5, -2.3, -Math.PI/2); buildRack(7.5, 2.3, -Math.PI/2);

// MATERIALS & 3D PROCEDURAL CHARACTERS
const animatedParts = [];
const mats = {
    skin: new THREE.MeshStandardMaterial({ color: 0xf1c27d, roughness: 0.5 }),
    darkMetal: new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.8, roughness: 0.25 }),
    chrome: new THREE.MeshStandardMaterial({ color: 0xe2e8f0, metalness: 0.9, roughness: 0.1 }),
    rubber: new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.9 }),
    cardboard: new THREE.MeshStandardMaterial({ color: 0xc29361, roughness: 0.75 }),
    wood: new THREE.MeshStandardMaterial({ color: 0x855832, roughness: 0.85 }),
    vest: new THREE.MeshStandardMaterial({ color: 0xa3e635, roughness: 0.3, emissive: 0x3f6212, emissiveIntensity: 0.2 }),
    silver: new THREE.MeshStandardMaterial({ color: 0xffffff, metalness: 0.9, roughness: 0.1 }),
    amber: new THREE.MeshStandardMaterial({ color: 0xf59e0b, emissive: 0xff8800, emissiveIntensity: 1.3 })
};

function createUnitMesh(type, team) {
    const root = new THREE.Group();
    const isBlue = team === 'blue';
    const tMat = new THREE.MeshStandardMaterial({ color: isBlue ? 0x0284c7 : 0xd97706, roughness: 0.3, metalness: 0.25 });
    const tAcc = new THREE.MeshStandardMaterial({ color: isBlue ? 0x38bdf8 : 0xfbbf24, roughness: 0.2, metalness: 0.4 });

    const ped = new THREE.Mesh(new THREE.CylinderGeometry(0.44, 0.48, 0.08, 20), mats.darkMetal);
    ped.position.y = 0.04; ped.castShadow = true; root.add(ped);
    const ring = new THREE.Mesh(new THREE.TorusGeometry(0.45, 0.025, 10, 20), tAcc);
    ring.rotation.x = Math.PI/2; ring.position.y = 0.08; root.add(ring);

    const dir = new THREE.Group();
    dir.rotation.y = isBlue ? 0 : Math.PI;
    root.add(dir);

    if (type === 'pawn') {
        [-0.1, 0.1].forEach(lx => {
            const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.065, 0.055, 0.36, 10), mats.darkMetal);
            leg.position.set(lx, 0.26, 0); dir.add(leg);
        });
        const torso = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.15, 0.42, 14), mats.vest);
        torso.position.set(0, 0.6, 0); torso.castShadow = true; dir.add(torso);
        const head = new THREE.Mesh(new THREE.SphereGeometry(0.14, 14, 14), mats.skin);
        head.position.set(0, 0.94, 0); dir.add(head);
        const hat = new THREE.Mesh(new THREE.SphereGeometry(0.155, 14, 10, 0, Math.PI*2, 0, Math.PI/1.8), tAcc);
        hat.position.set(0, 0.96, 0); dir.add(hat);
        const box = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.25, 0.26), mats.cardboard);
        box.position.set(0, 0.58, -0.24); box.castShadow = true; dir.add(box);
    } else if (type === 'rook') {
        [[-0.27,-0.24],[0.27,-0.24],[-0.27,0.24],[0.27,0.24]].forEach(([wx,wz]) => {
            const w = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 0.1, 14), mats.rubber);
            w.rotation.z = Math.PI/2; w.position.set(wx, 0.19, wz); dir.add(w);
        });
        const body = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.32, 0.62), tMat);
        body.position.set(0, 0.33, 0.05); body.castShadow = true; dir.add(body);
        [[-0.19,-0.14],[0.19,-0.14],[-0.19,0.2],[0.19,0.2]].forEach(([px,pz]) => {
            const p = new THREE.Mesh(new THREE.CylinderGeometry(0.022, 0.022, 0.48, 8), mats.darkMetal);
            p.position.set(px, 0.7, pz); dir.add(p);
        });
        const roof = new THREE.Mesh(new THREE.BoxGeometry(0.44, 0.05, 0.42), mats.darkMetal);
        roof.position.set(0, 0.94, 0.03); dir.add(roof);
        const beacon = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.055, 0.09, 10), mats.amber);
        beacon.position.set(0, 1.0, 0.14); dir.add(beacon);
        animatedParts.push({ mesh: beacon, type: 'pulse' });
        [-0.13, 0.13].forEach(mx => {
            const mast = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.9, 0.05), mats.darkMetal);
            mast.position.set(mx, 0.54, -0.3); dir.add(mast);
            const fork = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.03, 0.36), mats.chrome);
            fork.position.set(mx, 0.15, -0.45); dir.add(fork);
        });
    } else if (type === 'knight') {
        const drv = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.42, 0.3), tMat);
        drv.position.set(0, 0.29, 0.2); drv.castShadow = true; dir.add(drv);
        const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.48, 8), mats.darkMetal);
        arm.position.set(0, 0.65, 0.26); arm.rotation.x = -Math.PI/5; dir.add(arm);
        const c1 = new THREE.Mesh(new THREE.BoxGeometry(0.44, 0.28, 0.4), mats.cardboard);
        c1.position.set(0, 0.26, -0.14); c1.castShadow = true; dir.add(c1);
        const c2 = new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.24, 0.32), mats.cardboard);
        c2.position.set(0.02, 0.52, -0.14); c2.rotation.y = 0.2; dir.add(c2);
    } else if (type === 'bishop') {
        const body = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.22, 0.64, 14), tMat);
        body.position.set(0, 0.4, 0); body.castShadow = true; dir.add(body);
        const vest = new THREE.Mesh(new THREE.CylinderGeometry(0.19, 0.21, 0.34, 14), mats.vest);
        vest.position.set(0, 0.46, 0); dir.add(vest);
        const head = new THREE.Mesh(new THREE.SphereGeometry(0.14, 14, 14), mats.skin);
        head.position.set(0, 0.86, 0); dir.add(head);
        const hat = new THREE.Mesh(new THREE.SphereGeometry(0.155, 14, 10, 0, Math.PI*2, 0, Math.PI/1.8), mats.silver);
        hat.position.set(0, 0.88, 0); dir.add(hat);
        const laser = new THREE.Mesh(new THREE.ConeGeometry(0.1, 0.34, 10), new THREE.MeshBasicMaterial({ color: 0xff0055, transparent: true, opacity: 0.45 }));
        laser.rotation.x = Math.PI/2; laser.position.set(0.2, 0.6, -0.38); dir.add(laser);
    } else if (type === 'queen') {
        const body = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.25, 0.76, 16), tMat);
        body.position.set(0, 0.45, 0); body.castShadow = true; dir.add(body);
        const collar = new THREE.Mesh(new THREE.TorusGeometry(0.19, 0.03, 10, 16), mats.amber);
        collar.rotation.x = Math.PI/2; collar.position.set(0, 0.76, 0); dir.add(collar);
        const head = new THREE.Mesh(new THREE.SphereGeometry(0.15, 14, 14), mats.skin);
        head.position.set(0, 0.96, 0); dir.add(head);
        const hat = new THREE.Mesh(new THREE.SphereGeometry(0.165, 14, 10, 0, Math.PI*2, 0, Math.PI/1.8), mats.amber);
        hat.position.set(0, 0.98, 0); dir.add(hat);
        const pad = new THREE.Mesh(new THREE.BoxGeometry(0.26, 0.18, 0.03), new THREE.MeshStandardMaterial({ color: 0x38bdf8, emissive: 0x0284c7, emissiveIntensity: 0.8 }));
        pad.rotation.x = -Math.PI/4; pad.position.set(0, 0.64, -0.25); dir.add(pad);
    } else if (type === 'king') {
        const cab = new THREE.Mesh(new THREE.BoxGeometry(0.54, 1.0, 0.54), mats.darkMetal);
        cab.position.set(0, 0.58, 0); cab.castShadow = true; dir.add(cab);
        for (let sy = 0.25; sy <= 0.9; sy += 0.15) {
            const led = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.045, 0.56), new THREE.MeshStandardMaterial({ color: isBlue ? 0x38bdf8 : 0xfbbf24, emissive: isBlue ? 0x0284c7 : 0xd97706, emissiveIntensity: 1.2 }));
            led.position.set(0, sy, 0); dir.add(led);
        }
        const holo = new THREE.Mesh(new THREE.OctahedronGeometry(0.19, 0), new THREE.MeshStandardMaterial({ color: isBlue ? 0x38bdf8 : 0xfbbf24, emissive: isBlue ? 0x38bdf8 : 0xf59e0b, wireframe: true }));
        holo.position.set(0, 1.3, 0); dir.add(holo);
        animatedParts.push({ mesh: holo, type: 'spin' });
    }
    return root;
}

// CHESS LOGIC & AI BOT
let pieces = [], selectedPiece = null, validMoves = [], currentTurn = 'blue', isAnimating = false, vsAI = true, highlights = [];
const names = { pawn: 'Operator Picker', rook: 'Heavy Forklift', knight: 'Electric Pallet Jack', bishop: 'QC Checker', queen: 'Warehouse Supervisor', king: 'Main WMS Server' };
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

function showHighlights(moves, piece) {
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
    for (let i = 0; i < 16; i++) {
        const p = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.14, 0.16), i % 2 === 0 ? mats.cardboard : mats.amber);
        p.position.copy(pos); p.position.y += 0.4; scene.add(p);
        const vx = (Math.random()-0.5)*0.22, vz = (Math.random()-0.5)*0.22; let vy = Math.random()*0.2 + 0.06;
        const tick = () => {
            p.position.x += vx; p.position.y += vy; p.position.z += vz; vy -= 0.012;
            p.rotation.x += 0.15; p.scale.multiplyScalar(0.93);
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
        prog += 0.07;
        if (prog < 1) {
            piece.position.x = sx + (ex - sx) * prog;
            piece.position.z = sz + (ez - sz) * prog;
            piece.position.y = 0.05 + Math.sin(prog * Math.PI) * 0.65;
            requestAnimationFrame(step);
        } else {
            piece.position.set(ex, 0.05, ez);
            piece.userData.gridX = moveData.x; piece.userData.gridZ = moveData.z; piece.userData.hasMoved = true;
            let msg = `${names[piece.userData.type]} menuju zona ${cols[moveData.x]}${8 - moveData.z}.`;

            if (moveData.attack && moveData.target) {
                const v = moveData.target; v.userData.alive = false; scene.remove(v);
                triggerExplosion(piece.position);
                msg = `💥 EPIC! ${names[piece.userData.type]} mengeliminasi ${names[v.userData.type]}!`;
                if (v.userData.type === 'king') {
                    updateHUD(`🏆 OVERRIDE SELESAI! Tim ${currentTurn.toUpperCase()} menguasai WMS Server!`);
                    isAnimating = false; return;
                }
            }

            if (piece.userData.type === 'pawn' && (moveData.z === 0 || moveData.z === 7)) {
                const tm = piece.userData.team; scene.remove(piece);
                pieces = pieces.filter(p => p !== piece);
                spawnUnit('queen', tm, moveData.x, moveData.z);
                msg = `⭐ PROMOSI! Operator diangkat menjadi Warehouse Supervisor!`;
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
    selectedPiece = null; validMoves = []; currentTurn = 'blue'; isAnimating = false;
    const row = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook'];
    for (let i = 0; i < 8; i++) {
        spawnUnit(row[i], 'orange', i, 0); spawnUnit('pawn', 'orange', i, 1);
        spawnUnit('pawn', 'blue', i, 6); spawnUnit(row[i], 'blue', i, 7);
    }
    updateHUD("Shift Baru Dimulai! Pilih unit Biru untuk melangkah.");
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
    camera.position.set(0, mode === 'top' ? 19 : 13, mode === 'top' ? 0.01 : 14);
    controls.target.set(0, 0, 0); controls.update();
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
        selectedPiece = unit; validMoves = getValidMoves(unit); showHighlights(validMoves, unit);
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
    animatedParts.forEach(p => {
        if (p.type === 'spin') { p.mesh.rotation.y = t * 1.8; p.mesh.rotation.x = t * 0.9; }
        else if (p.type === 'pulse') { p.mesh.material.emissiveIntensity = 1.0 + Math.sin(t * 8) * 0.6; }
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
