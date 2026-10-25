import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Warehouse Logistics Chess 3D - Blender PBR Edition",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Fullscreen bersih tanpa margin bawaan Streamlit
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding: 0 !important; margin: 0 !important; max-width: 100% !important;}
    .stApp {background-color: #070b12; overflow: hidden;}
    iframe {display: block; border: none; width: 100vw !important; height: 100vh !important;}
</style>
""", unsafe_allow_html=True)

game_html = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Warehouse Logistics Chess 3D</title>
    <style>
        * { box-sizing: border-box; user-select: none; }
        body {
            margin: 0; padding: 0; overflow: hidden;
            background-color: #070b12;
            font-family: 'Segoe UI', Roboto, Helvetica, sans-serif;
            color: #f8fafc;
        }
        #canvas-container { width: 100vw; height: 100vh; display: block; }
        
        /* HUD & UI Overlay */
        #hud-top {
            position: absolute; top: 20px; left: 24px; right: 24px;
            display: flex; justify-content: space-between; align-items: flex-start;
            pointer-events: none; z-index: 10;
        }
        .brand-box {
            background: rgba(15, 23, 42, 0.85);
            border-left: 5px solid #f59e0b;
            padding: 12px 20px; border-radius: 8px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.6);
            backdrop-filter: blur(8px);
            border-top: 1px solid rgba(255,255,255,0.08);
        }
        .brand-box h1 {
            margin: 0; font-size: 20px; font-weight: 800;
            letter-spacing: 1.5px; text-transform: uppercase;
            background: linear-gradient(90deg, #f59e0b, #38bdf8);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .brand-box p { margin: 4px 0 0 0; font-size: 12px; color: #94a3b8; }

        .controls-box {
            pointer-events: auto;
            display: flex; gap: 10px;
        }
        .btn {
            background: rgba(30, 41, 59, 0.9);
            border: 1px solid #475569; color: #e2e8f0;
            padding: 10px 16px; border-radius: 6px; cursor: pointer;
            font-weight: 600; font-size: 13px; transition: all 0.2s;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        }
        .btn:hover { background: #334155; border-color: #38bdf8; color: #fff; transform: translateY(-1px); }

        #hud-bottom {
            position: absolute; bottom: 24px; left: 50%;
            transform: translateX(-50%);
            background: rgba(15, 23, 42, 0.9);
            border: 1px solid rgba(255,255,255,0.12);
            padding: 14px 32px; border-radius: 12px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.7);
            display: flex; align-items: center; gap: 20px;
            z-index: 10; backdrop-filter: blur(10px);
        }
        .shift-badge {
            padding: 6px 14px; border-radius: 6px; font-weight: 800;
            font-size: 14px; text-transform: uppercase; letter-spacing: 1px;
        }
        .shift-blue { background: rgba(2, 132, 199, 0.25); color: #38bdf8; border: 1px solid #0284c7; }
        .shift-orange { background: rgba(217, 119, 6, 0.25); color: #fbbf24; border: 1px solid #d97706; }

        #action-log {
            font-size: 14px; color: #cbd5e1; font-weight: 500;
        }

        /* Legend Card */
        #legend-panel {
            position: absolute; top: 105px; left: 24px;
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(255,255,255,0.08);
            padding: 12px 16px; border-radius: 8px;
            font-size: 12px; color: #cbd5e1;
            pointer-events: none; backdrop-filter: blur(6px);
        }
        #legend-panel div { margin: 4px 0; }
        .key-role { color: #f59e0b; font-weight: bold; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>

    <div id="hud-top">
        <div class="brand-box">
            <h1>Warehouse Tactical Chess 3D</h1>
            <p>Blender PBR Procedural Graphics • Warehouse Operations Edition</p>
        </div>
        <div class="controls-box">
            <button class="btn" onclick="setCameraView('perspective')">🎥 Kamera Bebas</button>
            <button class="btn" onclick="setCameraView('top')">📐 Denah Atas (Layout)</button>
            <button class="btn" onclick="resetGame()">🔄 Reset Shift</button>
        </div>
    </div>

    <div id="legend-panel">
        <div><span class="key-role">Pion:</span> Operator Picker (Bawa Kardus)</div>
        <div><span class="key-role">Benteng:</span> Heavy Forklift (Reach Truck)</div>
        <div><span class="key-role">Kuda:</span> Electric Hand Pallet Jack</div>
        <div><span class="key-role">Gajah:</span> QC Checker (Barcode Scanner)</div>
        <div><span class="key-role">Menteri:</span> Warehouse Ops Supervisor</div>
        <div><span class="key-role">Raja:</span> Main WMS Server Rack</div>
    </div>

    <div id="hud-bottom">
        <div id="turn-badge" class="shift-badge shift-blue">SHIFT BIRU (DIVISI INBOUND)</div>
        <div id="action-log">Pilih unit operasional untuk memulai pergerakan...</div>
    </div>

    <div id="canvas-container"></div>

    <script>
        // ============================================================================
        // 1. ENGINE INITIALIZATION (BLENDER CYCLES/EEVEE PBR TONE MAPPING)
        // ============================================================================
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x090d16);
        scene.fog = new THREE.FogExp2(0x090d16, 0.018);

        const camera = new THREE.PerspectiveCamera(42, window.innerWidth / window.innerHeight, 0.1, 200);
        camera.position.set(0, 13, 14);

        const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.toneMappingExposure = 1.15;
        renderer.outputEncoding = THREE.sRGBEncoding;
        container.appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.maxPolarAngle = Math.PI / 2 - 0.04;
        controls.minDistance = 6;
        controls.maxDistance = 28;
        controls.target.set(0, 0.5, 0);

        // ============================================================================
        // 2. PROCEDURAL TEXTURES (EPOXY FLOOR, HAZARD STRIPES, WOOD PALLET)
        // ============================================================================
        function createHazardTexture() {
            const canvas = document.createElement('canvas');
            canvas.width = 256; canvas.height = 256;
            const ctx = canvas.getContext('2d');
            ctx.fillStyle = '#eab308';
            ctx.fillRect(0, 0, 256, 256);
            ctx.fillStyle = '#0f172a';
            for (let i = -256; i < 512; i += 64) {
                ctx.beginPath();
                ctx.moveTo(i, 0); ctx.lineTo(i + 32, 0);
                ctx.lineTo(i - 224, 256); ctx.lineTo(i - 256, 256);
                ctx.closePath(); ctx.fill();
            }
            const tex = new THREE.CanvasTexture(canvas);
            tex.wrapS = THREE.RepeatWrapping; tex.wrapT = THREE.RepeatWrapping;
            tex.repeat.set(12, 1);
            return tex;
        }

        function createTileTexture(isDark, coordText) {
            const canvas = document.createElement('canvas');
            canvas.width = 256; canvas.height = 256;
            const ctx = canvas.getContext('2d');
            ctx.fillStyle = isDark ? '#1e293b' : '#334155';
            ctx.fillRect(0, 0, 256, 256);
            
            // Garis safety border tipis di tiap ubin lantai epoxy
            ctx.strokeStyle = isDark ? '#334155' : '#475569';
            ctx.lineWidth = 6;
            ctx.strokeRect(8, 8, 240, 240);

            // Titik marka gudang di sudut
            ctx.fillStyle = 'rgba(250, 204, 21, 0.25)';
            ctx.fillRect(14, 14, 12, 4); ctx.fillRect(14, 14, 4, 12);

            if (coordText) {
                ctx.fillStyle = 'rgba(148, 163, 184, 0.35)';
                ctx.font = 'bold 26px monospace';
                ctx.fillText(coordText, 22, 236);
            }
            return new THREE.CanvasTexture(canvas);
        }

        // ============================================================================
        // 3. LIGHTING (INDUSTRIAL HIGH-BAY WAREHOUSE LIGHTING)
        // ============================================================================
        const hemiLight = new THREE.HemisphereLight(0xdbeafe, 0x0f172a, 0.55);
        scene.add(hemiLight);

        const mainSpot = new THREE.DirectionalLight(0xfffbeb, 1.35);
        mainSpot.position.set(10, 22, 12);
        mainSpot.castShadow = true;
        mainSpot.shadow.mapSize.width = 2048;
        mainSpot.shadow.mapSize.height = 2048;
        mainSpot.shadow.camera.near = 2;
        mainSpot.shadow.camera.far = 45;
        const d = 8.5;
        mainSpot.shadow.camera.left = -d; mainSpot.shadow.camera.right = d;
        mainSpot.shadow.camera.top = d; mainSpot.shadow.camera.bottom = -d;
        mainSpot.shadow.bias = -0.0005;
        scene.add(mainSpot);

        const rimLight1 = new THREE.PointLight(0x38bdf8, 1.4, 25);
        rimLight1.position.set(-9, 8, 9);
        scene.add(rimLight1);

        const rimLight2 = new THREE.PointLight(0xf59e0b, 1.4, 25);
        rimLight2.position.set(9, 8, -9);
        scene.add(rimLight2);

        // ============================================================================
        // 4. WAREHOUSE ENVIRONMENT & EPOXY BOARD
        // ============================================================================
        const boardGroup = new THREE.Group();
        scene.add(boardGroup);

        // Lantai Dasar Gudang Luas
        const warehouseFloor = new THREE.Mesh(
            new THREE.PlaneGeometry(60, 60),
            new THREE.MeshStandardMaterial({ color: 0x0b111e, roughness: 0.4, metalness: 0.1 })
        );
        warehouseFloor.rotation.x = -Math.PI / 2;
        warehouseFloor.position.y = -0.35;
        warehouseFloor.receiveShadow = true;
        scene.add(warehouseFloor);

        // Platform Papan Catur dengan Lis Hazard Kuning-Hitam
        const hazardMat = new THREE.MeshStandardMaterial({ map: createHazardTexture(), roughness: 0.3 });
        const platformBase = new THREE.Mesh(
            new THREE.BoxGeometry(10.6, 0.35, 10.6),
            new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.2, metalness: 0.5 })
        );
        platformBase.position.y = -0.2;
        platformBase.receiveShadow = true;
        boardGroup.add(platformBase);

        // Lis Hazard di 4 Sisi Papan
        const borderThickness = 0.25;
        const borderN = new THREE.Mesh(new THREE.BoxGeometry(10.2, 0.12, borderThickness), hazardMat);
        borderN.position.set(0, -0.02, -4.95); boardGroup.add(borderN);
        const borderS = borderN.clone(); borderS.position.set(0, -0.02, 4.95); boardGroup.add(borderS);
        const borderW = new THREE.Mesh(new THREE.BoxGeometry(borderThickness, 0.12, 10.2), hazardMat);
        borderW.position.set(-4.95, -0.02, 0); boardGroup.add(borderW);
        const borderE = borderW.clone(); borderE.position.set(4.95, -0.02, 0); boardGroup.add(borderE);

        // Pembuatan 64 Petak Lantai Epoxy Gudang
        const tileSize = 1.2;
        const offset = 3.5 * tileSize;
        const tiles = [];
        const cols = ['A','B','C','D','E','F','G','H'];

        for (let x = 0; x < 8; x++) {
            tiles[x] = [];
            for (let z = 0; z < 8; z++) {
                const isDark = (x + z) % 2 === 1;
                const label = (z === 7) ? cols[x] : (x === 0 ? String(8 - z) : '');
                const tex = createTileTexture(isDark, label);
                
                const tileMat = new THREE.MeshStandardMaterial({
                    map: tex,
                    roughness: isDark ? 0.18 : 0.25, // Efek lantai epoxy glossy
                    metalness: 0.15
                });
                const tile = new THREE.Mesh(new THREE.BoxGeometry(tileSize, 0.1, tileSize), tileMat);
                tile.position.set(x * tileSize - offset, 0, z * tileSize - offset);
                tile.receiveShadow = true;
                tile.userData = { gridX: x, gridZ: z, isDark: isDark, baseMat: tileMat };
                boardGroup.add(tile);
                tiles[x][z] = tile;
            }
        }

        // Dekorasi Rak Gudang (Selective Pallet Racking) di Sekeliling Papan
        function createStorageRack(xPos, zPos, rotY) {
            const rack = new THREE.Group();
            const uprightMat = new THREE.MeshStandardMaterial({ color: 0x1d4ed8, metalness: 0.6, roughness: 0.3 });
            const beamMat = new THREE.MeshStandardMaterial({ color: 0xea580c, metalness: 0.4, roughness: 0.3 });
            const boxMat = new THREE.MeshStandardMaterial({ color: 0xb48352, roughness: 0.8 });

            // Tiang Biru
            [-1.8, 0, 1.8].forEach(lx => {
                [-0.4, 0.4].forEach(lz => {
                    const post = new THREE.Mesh(new THREE.BoxGeometry(0.1, 3.8, 0.1), uprightMat);
                    post.position.set(lx, 1.9, lz);
                    post.castShadow = true;
                    rack.add(post);
                });
            });

            // Balok Oranye & Kardus Palet
            [0.8, 2.0, 3.2].forEach(ly => {
                const beamF = new THREE.Mesh(new THREE.BoxGeometry(3.7, 0.1, 0.08), beamMat);
                beamF.position.set(0, ly, 0.4); rack.add(beamF);
                const beamB = beamF.clone(); beamB.position.set(0, ly, -0.4); rack.add(beamB);

                // Kardus di atas rak
                [-1.1, -0.2, 0.9].forEach(bx => {
                    const box = new THREE.Mesh(new THREE.BoxGeometry(0.65, 0.55, 0.7), boxMat);
                    box.position.set(bx, ly + 0.35, 0);
                    box.castShadow = true;
                    rack.add(box);
                });
            });

            rack.position.set(xPos, -0.35, zPos);
            rack.rotation.y = rotY;
            scene.add(rack);
        }

        createStorageRack(-7.5, -2.5, Math.PI / 2);
        createStorageRack(-7.5, 2.5, Math.PI / 2);
        createStorageRack(7.5, -2.5, -Math.PI / 2);
        createStorageRack(7.5, 2.5, -Math.PI / 2);

        // ============================================================================
        // 5. HIGH-DETAIL BLENDER-STYLE PROCEDURAL 3D CHARACTERS
        // ============================================================================
        const animatedParts = []; // Menyimpan lampu sirine forklift & hologram server untuk berputar

        const sharedMats = {
            skin: new THREE.MeshStandardMaterial({ color: 0xf1c27d, roughness: 0.5 }),
            darkMetal: new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.8, roughness: 0.25 }),
            chrome: new THREE.MeshStandardMaterial({ color: 0xe2e8f0, metalness: 0.9, roughness: 0.1 }),
            rubber: new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.9 }),
            cardboard: new THREE.MeshStandardMaterial({ color: 0xc29361, roughness: 0.75 }),
            wood: new THREE.MeshStandardMaterial({ color: 0x855832, roughness: 0.85 }),
            hiVisVest: new THREE.MeshStandardMaterial({ color: 0xa3e635, roughness: 0.3, emissive: 0x3f6212, emissiveIntensity: 0.2 }),
            silverStrip: new THREE.MeshStandardMaterial({ color: 0xffffff, metalness: 0.9, roughness: 0.1, emissive: 0x94a3b8, emissiveIntensity: 0.3 }),
            laserRed: new THREE.MeshBasicMaterial({ color: 0xff0044 }),
            beaconAmber: new THREE.MeshStandardMaterial({ color: 0xf59e0b, emissive: 0xff8800, emissiveIntensity: 1.5 })
        };

        function createPalletMesh() {
            const pGroup = new THREE.Group();
            for (let i = -0.25; i <= 0.25; i += 0.25) {
                const slat = new THREE.Mesh(new THREE.BoxGeometry(0.65, 0.06, 0.14), sharedMats.wood);
                slat.position.set(0, 0.03, i);
                pGroup.add(slat);
            }
            return pGroup;
        }

        function createUnitMesh(type, team) {
            const root = new THREE.Group();
            const isBlue = team === 'blue';
            const teamMat = new THREE.MeshStandardMaterial({
                color: isBlue ? 0x0284c7 : 0xd97706,
                roughness: 0.3, metalness: 0.25
            });
            const teamAccent = new THREE.MeshStandardMaterial({
                color: isBlue ? 0x38bdf8 : 0xfbbf24,
                roughness: 0.2, metalness: 0.4
            });

            // Alas Stand Karakter (Base Pedestal)
            const pedestal = new THREE.Mesh(new THREE.CylinderGeometry(0.44, 0.48, 0.08, 24), sharedMats.darkMetal);
            pedestal.position.y = 0.04;
            pedestal.castShadow = true; pedestal.receiveShadow = true;
            root.add(pedestal);

            const ring = new THREE.Mesh(new THREE.TorusGeometry(0.45, 0.025, 12, 24), teamAccent);
            ring.rotation.x = Math.PI / 2;
            ring.position.y = 0.08;
            root.add(ring);

            // Arah hadap: Tim Biru menghadap ke Utara (-Z), Tim Oranye menghadap ke Selatan (+Z)
            const dirGroup = new THREE.Group();
            dirGroup.rotation.y = isBlue ? 0 : Math.PI;
            root.add(dirGroup);

            // ------------------------------------------------------------------------
            // 1. PION: OPERATOR PICKER (MEMBAWA KARDUS & HARD HAT)
            // ------------------------------------------------------------------------
            if (type === 'pawn') {
                // Kaki
                [-0.1, 0.1].forEach(lx => {
                    const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.06, 0.38, 12), sharedMats.darkMetal);
                    leg.position.set(lx, 0.27, 0); leg.castShadow = true; dirGroup.add(leg);
                });
                // Badan + Rompi Safety
                const torso = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.15, 0.42, 16), sharedMats.hiVisVest);
                torso.position.set(0, 0.62, 0); torso.castShadow = true; dirGroup.add(torso);
                
                // Strip Reflektif Rompi
                const strip = new THREE.Mesh(new THREE.CylinderGeometry(0.183, 0.175, 0.06, 16), sharedMats.silverStrip);
                strip.position.set(0, 0.58, 0); dirGroup.add(strip);

                // Kepala
                const head = new THREE.Mesh(new THREE.SphereGeometry(0.14, 16, 16), sharedMats.skin);
                head.position.set(0, 0.96, 0); head.castShadow = true; dirGroup.add(head);

                // Helm Safety (Hard Hat)
                const helmet = new THREE.Mesh(new THREE.SphereGeometry(0.155, 16, 12, 0, Math.PI * 2, 0, Math.PI / 1.8), teamAccent);
                helmet.position.set(0, 0.98, 0); dirGroup.add(helmet);
                const brim = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, 0.02, 16), teamAccent);
                brim.position.set(0, 0.98, -0.03); dirGroup.add(brim);

                // Lengan & Kardus Logistik di Depan Dada
                [-0.2, 0.2].forEach(ax => {
                    const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.045, 0.35, 10), teamMat);
                    arm.position.set(ax, 0.62, -0.12);
                    arm.rotation.x = Math.PI / 3;
                    dirGroup.add(arm);
                });
                const box = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.26, 0.28), sharedMats.cardboard);
                box.position.set(0, 0.58, -0.26); box.castShadow = true; dirGroup.add(box);
            }

            // ------------------------------------------------------------------------
            // 2. BENTENG: HEAVY FORKLIFT / REACH TRUCK (DENGAN SIRINE PUTAR)
            // ------------------------------------------------------------------------
            else if (type === 'rook') {
                // 4 Roda Karet
                [[-0.28, -0.25], [0.28, -0.25], [-0.28, 0.25], [0.28, 0.25]].forEach(([wx, wz]) => {
                    const wheel = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.13, 0.1, 16), sharedMats.rubber);
                    wheel.rotation.z = Math.PI / 2;
                    wheel.position.set(wx, 0.2, wz);
                    dirGroup.add(wheel);
                });

                // Sasis Body Forklift
                const chassis = new THREE.Mesh(new THREE.BoxGeometry(0.52, 0.32, 0.65), teamMat);
                chassis.position.set(0, 0.34, 0.05); chassis.castShadow = true; dirGroup.add(chassis);

                // Counterweight Belakang
                const weight = new THREE.Mesh(new THREE.CylinderGeometry(0.26, 0.26, 0.34, 16), sharedMats.darkMetal);
                weight.position.set(0, 0.35, 0.25); dirGroup.add(weight);

                // Kabin Roll-Cage (4 Tiang Pelindung)
                [[-0.2, -0.15], [0.2, -0.15], [-0.2, 0.22], [0.2, 0.22]].forEach(([px, pz]) => {
                    const pillar = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.5, 8), sharedMats.darkMetal);
                    pillar.position.set(px, 0.72, pz); dirGroup.add(pillar);
                });
                const roof = new THREE.Mesh(new THREE.BoxGeometry(0.46, 0.05, 0.44), sharedMats.darkMetal);
                roof.position.set(0, 0.96, 0.03); dirGroup.add(roof);

                // Lampu Rotary Beacon (Menyala)
                const beacon = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.06, 0.1, 12), sharedMats.beaconAmber);
                beacon.position.set(0, 1.03, 0.15);
                dirGroup.add(beacon);
                animatedParts.push({ mesh: beacon, type: 'pulse' });

                // Tiang Hidrolik Depan (Mast) & Garpu Baja
                [-0.14, 0.14].forEach(mx => {
                    const mast = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.95, 0.06), sharedMats.darkMetal);
                    mast.position.set(mx, 0.56, -0.32); dirGroup.add(mast);

                    const fork = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.03, 0.38), sharedMats.chrome);
                    fork.position.set(mx, 0.16, -0.48); dirGroup.add(fork);
                });
            }

            // ------------------------------------------------------------------------
            // 3. KUDA: ELECTRIC HAND PALLET JACK DENGAN TUMPUKAN KARGO
            // ------------------------------------------------------------------------
            else if (type === 'knight') {
                // Unit Mesin Penggerak Belakang
                const driveUnit = new THREE.Mesh(new THREE.BoxGeometry(0.44, 0.45, 0.32), teamMat);
                driveUnit.position.set(0, 0.3, 0.22); driveUnit.castShadow = true; dirGroup.add(driveUnit);

                // Stang Kemudi (Tiller Arm)
                const tiller = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.5, 8), sharedMats.darkMetal);
                tiller.position.set(0, 0.68, 0.28);
                tiller.rotation.x = -Math.PI / 5;
                dirGroup.add(tiller);
                const handle = new THREE.Mesh(new THREE.BoxGeometry(0.24, 0.05, 0.