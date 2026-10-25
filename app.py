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
mainSpot.castShadow = true
