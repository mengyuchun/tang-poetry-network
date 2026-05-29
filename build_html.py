"""
唐诗社交网络 — 构建单文件 HTML（v4 全功能版）
三视图 · 地理分布 · 统计面板 · 诗人路径 · 趣味功能
"""
import json
import os

DIST_DIR = os.path.join(os.path.dirname(__file__), 'dist')


def build():
    with open(os.path.join(DIST_DIR, 'data.json'), 'r', encoding='utf-8') as f:
        data = json.load(f)

    nodes = data['nodes']
    edges = data['edges']
    stats = data['stats']
    period_dist = data.get('periodDist', {})
    top_poets = data.get('topPoets', [])
    timeline = data.get('timeline', [])
    network_stats = data.get('networkStats', {})
    period_colors = {'初唐': '#61a0a8', '盛唐': '#c23531', '中唐': '#2f4554', '晚唐': '#d48265', '未知': '#999'}

    data_json = json.dumps({'nodes': nodes, 'edges': edges}, ensure_ascii=False)
    colors_json = json.dumps(period_colors, ensure_ascii=False)
    stats_json = json.dumps({
        'periodDist': period_dist, 'topPoets': top_poets,
        'timeline': timeline, 'networkStats': network_stats
    }, ensure_ascii=False)

    html = '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n'
    html += '<meta charset="UTF-8">\n'
    html += '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
    html += '<title>唐诗社交网络</title>\n'
    html += '<meta name="description" content="1,381位诗人 · 8,259条赠诗关系 · 57,607首唐诗 · 交互式探索">\n'
    html += '<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🏮</text></svg>">\n'
    html += '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.css">\n'
    html += '<style>\n' + CSS + '\n</style>\n</head>\n<body>\n'
    html += LOADING_HTML
    html += HEADER_HTML.format(
        total_poets=stats['total_poets'],
        total_edges=stats['total_edges'],
        total_poems=stats['total_poems'],
        matched_poets=stats['matched_poets']
    )
    html += '\n<script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script>\n'
    html += '<script src="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.js"></script>\n'
    html += '<script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>\n'
    html += '<script>\nconst DATA = ' + data_json + ';\n'
    html += 'const PERIOD_COLORS = ' + colors_json + ';\n'
    html += 'const STATS = ' + stats_json + ';\n'
    html += JS + '\n</script>\n</body>\n</html>'

    output_path = os.path.join(DIST_DIR, 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"已生成: {output_path} ({size_mb:.1f} MB)")


CSS = r"""
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'STKaiti','KaiTi','Noto Serif SC','SimSun',serif; background: #f5f0e8; color: #2c2c2c; overflow: hidden; height: 100vh; }
body::before { content:''; position:fixed; top:0; left:0; right:0; bottom:0; background: radial-gradient(ellipse at 20% 50%,rgba(200,180,150,0.15) 0%,transparent 50%), radial-gradient(ellipse at 80% 20%,rgba(180,160,130,0.1) 0%,transparent 50%), radial-gradient(ellipse at 50% 80%,rgba(190,170,140,0.1) 0%,transparent 50%); pointer-events:none; z-index:0; }
.loading { position:fixed; top:0; left:0; right:0; bottom:0; background:#f5f0e8; z-index:9999; display:flex; flex-direction:column; align-items:center; justify-content:center; transition:opacity 0.5s; }
.loading.hide { opacity:0; pointer-events:none; }
.loading-text { font-size:18px; color:#2c2c2c; letter-spacing:4px; margin-top:20px; }
.loading-sub { font-size:13px; color:#999; margin-top:8px; }
.spinner { width:40px; height:40px; border:3px solid rgba(44,44,44,0.1); border-top-color:#c23531; border-radius:50%; animation:spin 0.8s linear infinite; }
@keyframes spin { to { transform:rotate(360deg); } }
.header { position:fixed; top:0; left:0; right:0; height:56px; background:rgba(44,44,44,0.92); display:flex; align-items:center; justify-content:space-between; padding:0 24px; z-index:100; backdrop-filter:blur(8px); }
.header h1 { color:#f5f0e8; font-size:20px; font-weight:400; letter-spacing:4px; white-space:nowrap; }
.header-center { display:flex; align-items:center; gap:16px; }
.header-right { display:flex; align-items:center; gap:12px; }
.search-wrap { position:relative; }
.search-box input { width:280px; padding:6px 12px; border:1px solid rgba(245,240,232,0.3); border-radius:4px; background:rgba(245,240,232,0.1); color:#f5f0e8; font-family:inherit; font-size:14px; outline:none; }
.search-box input::placeholder { color:rgba(245,240,232,0.5); }
.search-box input:focus { border-color:#c23531; }
.autocomplete { position:absolute; top:100%; left:0; width:400px; max-height:400px; overflow-y:auto; background:rgba(44,44,44,0.95); border-radius:0 0 4px 4px; display:none; z-index:200; backdrop-filter:blur(8px); }
.ac-section { padding:4px 12px; font-size:10px; color:rgba(245,240,232,0.4); text-transform:uppercase; letter-spacing:1px; border-bottom:1px solid rgba(245,240,232,0.1); }
.ac-item { padding:8px 12px; color:#f5f0e8; font-size:13px; cursor:pointer; display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(245,240,232,0.05); }
.ac-item:hover, .ac-item.active { background:rgba(194,53,49,0.3); }
.ac-item .ac-left { display:flex; align-items:center; gap:6px; flex:1; min-width:0; }
.ac-item .ac-pd { width:8px; height:8px; border-radius:50%; flex-shrink:0; }
.ac-item .ac-name { font-weight:bold; white-space:nowrap; }
.ac-item .ac-ctx { font-size:11px; color:rgba(245,240,232,0.6); overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.ac-item .ac-right { font-size:11px; color:rgba(245,240,232,0.5); white-space:nowrap; margin-left:8px; }
.ac-highlight { color:#c23531; font-weight:bold; }
.quick-nav { display:flex; gap:4px; }
.quick-btn { padding:3px 8px; background:rgba(245,240,232,0.1); border:1px solid rgba(245,240,232,0.2); border-radius:3px; color:#f5f0e8; font-size:11px; cursor:pointer; font-family:inherit; transition:all 0.2s; }
.quick-btn:hover { background:rgba(194,53,49,0.4); border-color:#c23531; }
.fun-btn { padding:3px 10px; background:rgba(194,53,49,0.3); border:1px solid rgba(194,53,49,0.5); border-radius:3px; color:#f5f0e8; font-size:11px; cursor:pointer; font-family:inherit; transition:all 0.2s; }
.fun-btn:hover { background:rgba(194,53,49,0.6); }
.tabs { display:flex; gap:2px; }
.tab { padding:6px 16px; background:rgba(245,240,232,0.1); border:none; color:rgba(245,240,232,0.6); font-size:13px; cursor:pointer; font-family:inherit; border-radius:4px 4px 0 0; transition:all 0.2s; }
.tab:hover { color:#f5f0e8; background:rgba(245,240,232,0.15); }
.tab.active { color:#f5f0e8; background:rgba(194,53,49,0.6); }
.legend { display:flex; gap:10px; align-items:center; }
.legend-item { display:flex; align-items:center; gap:3px; color:#f5f0e8; font-size:11px; cursor:pointer; padding:2px 5px; border-radius:3px; transition:all 0.2s; user-select:none; }
.legend-item:hover { background:rgba(245,240,232,0.1); }
.legend-item.inactive { opacity:0.3; }
.legend-dot { width:8px; height:8px; border-radius:50%; }
.stats-bar { position:fixed; bottom:0; left:0; right:0; height:36px; background:rgba(44,44,44,0.85); display:flex; align-items:center; justify-content:center; gap:32px; color:rgba(245,240,232,0.8); font-size:13px; z-index:100; backdrop-filter:blur(8px); }
.view { position:fixed; top:56px; left:0; right:360px; bottom:36px; z-index:1; display:none; }
.view.active { display:block; }
#graph { z-index:1; }
#mapView { z-index:1; }
#statsView { overflow-y:auto; padding:24px; background:rgba(245,240,232,0.95); }
.legend-help { position:fixed; bottom:36px; left:0; right:360px; height:28px; background:rgba(245,240,232,0.85); display:flex; align-items:center; justify-content:center; gap:24px; font-size:11px; color:#888; z-index:99; border-top:1px solid rgba(44,44,44,0.1); }
.panel { position:fixed; top:56px; right:0; bottom:36px; width:360px; background:rgba(245,240,232,0.95); border-left:1px solid rgba(44,44,44,0.15); overflow-y:auto; z-index:50; padding:20px; backdrop-filter:blur(8px); }
.panel-close { position:absolute; top:12px; right:12px; width:28px; height:28px; border:none; background:rgba(44,44,44,0.08); color:#888; font-size:16px; cursor:pointer; border-radius:4px; display:flex; align-items:center; justify-content:center; z-index:10; }
.panel-close:hover { background:rgba(44,44,44,0.15); color:#2c2c2c; }
.panel-empty { display:flex; align-items:center; justify-content:center; height:100%; color:#999; font-size:15px; text-align:center; line-height:2; }
.panel-title { font-size:24px; color:#2c2c2c; margin-bottom:8px; letter-spacing:2px; }
.panel-period { display:inline-block; padding:2px 10px; border-radius:3px; font-size:13px; color:#fff; margin-bottom:12px; }
.panel-stats { display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; margin-bottom:16px; }
.panel-stat { text-align:center; padding:8px; background:rgba(44,44,44,0.05); border-radius:4px; cursor:pointer; transition:all 0.2s; }
.panel-stat:hover { background:rgba(194,53,49,0.1); transform:scale(1.05); }
.panel-stat-num { font-size:20px; color:#c23531; font-weight:bold; }
.panel-stat-label { font-size:12px; color:#888; }
.panel-section { margin-bottom:16px; }
.panel-section h3 { font-size:15px; color:#2c2c2c; border-bottom:1px solid rgba(44,44,44,0.15); padding-bottom:6px; margin-bottom:10px; }
.panel-section h3 .view-all { font-size:11px; color:#c23531; cursor:pointer; font-weight:normal; }
.panel-section h3 .view-all:hover { text-decoration:underline; }
.poem-card { background:rgba(255,255,255,0.6); border:1px solid rgba(44,44,44,0.1); border-radius:4px; padding:12px; margin-bottom:8px; }
.poem-title { font-size:14px; font-weight:bold; color:#2c2c2c; margin-bottom:6px; }
.poem-text { font-size:13px; color:#555; line-height:1.8; white-space:pre-line; }
.relation-item { padding:6px 0; border-bottom:1px solid rgba(44,44,44,0.08); font-size:13px; color:#555; cursor:pointer; }
.relation-item:hover { color:#c23531; }
.relation-item b { color:#2c2c2c; }
/* 路径查找 */
.path-finder { background:rgba(44,44,44,0.05); border-radius:8px; padding:16px; margin-bottom:20px; }
.path-finder h3 { font-size:15px; margin-bottom:12px; color:#2c2c2c; }
.path-inputs { display:flex; gap:8px; align-items:center; margin-bottom:12px; }
.path-inputs input { flex:1; padding:6px 10px; border:1px solid rgba(44,44,44,0.2); border-radius:4px; font-family:inherit; font-size:13px; outline:none; }
.path-inputs input:focus { border-color:#c23531; }
.path-inputs span { color:#888; font-size:13px; }
.path-btn { padding:6px 16px; background:#c23531; color:#fff; border:none; border-radius:4px; font-size:13px; cursor:pointer; font-family:inherit; }
.path-btn:hover { background:#a02828; }
.path-result { margin-top:12px; }
.path-step { display:flex; align-items:center; gap:8px; padding:6px 0; font-size:13px; }
.path-step .path-node { color:#c23531; font-weight:bold; cursor:pointer; }
.path-step .path-node:hover { text-decoration:underline; }
.path-step .path-arrow { color:#999; }
.path-step .path-edge { color:#888; font-size:11px; }
.path-examples { font-size:11px; color:#999; margin-top:8px; }
.path-examples span { color:#c23531; cursor:pointer; }
.path-examples span:hover { text-decoration:underline; }
/* 统计面板 */
.stats-grid { display:grid; grid-template-columns:1fr 1fr; gap:20px; }
.stats-card { background:rgba(255,255,255,0.6); border:1px solid rgba(44,44,44,0.1); border-radius:8px; padding:16px; }
.stats-card h3 { font-size:15px; color:#2c2c2c; margin-bottom:12px; border-bottom:1px solid rgba(44,44,44,0.1); padding-bottom:8px; }
.stats-card canvas { max-height:300px; }
.stats-summary { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:20px; }
.stats-summary-item { text-align:center; padding:16px; background:rgba(255,255,255,0.6); border:1px solid rgba(44,44,44,0.1); border-radius:8px; }
.stats-summary-num { font-size:28px; color:#c23531; font-weight:bold; }
.stats-summary-label { font-size:12px; color:#888; margin-top:4px; }
.modal-overlay { position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.5); z-index:500; display:none; align-items:center; justify-content:center; backdrop-filter:blur(4px); }
.modal-overlay.show { display:flex; }
.modal { background:#f5f0e8; border-radius:8px; width:90%; max-width:700px; max-height:80vh; display:flex; flex-direction:column; box-shadow:0 20px 60px rgba(0,0,0,0.3); }
.modal-header { padding:16px 20px; border-bottom:1px solid rgba(44,44,44,0.15); display:flex; justify-content:space-between; align-items:center; }
.modal-header h2 { font-size:18px; color:#2c2c2c; }
.modal-close { width:32px; height:32px; border:none; background:none; font-size:20px; color:#888; cursor:pointer; border-radius:4px; display:flex; align-items:center; justify-content:center; }
.modal-close:hover { background:rgba(44,44,44,0.1); color:#2c2c2c; }
.modal-search { padding:8px 20px; border-bottom:1px solid rgba(44,44,44,0.1); }
.modal-search input { width:100%; padding:6px 10px; border:1px solid rgba(44,44,44,0.2); border-radius:4px; font-family:inherit; font-size:13px; outline:none; background:rgba(255,255,255,0.5); }
.modal-body { padding:12px 20px; overflow-y:auto; flex:1; }
.modal-item { padding:8px 0; border-bottom:1px solid rgba(44,44,44,0.08); font-size:13px; color:#555; cursor:pointer; }
.modal-item:hover { color:#c23531; }
.modal-item b { color:#2c2c2c; }
.modal-empty { color:#999; text-align:center; padding:20px; }
.onboarding { position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.4); z-index:300; display:none; align-items:center; justify-content:center; backdrop-filter:blur(2px); }
.onboarding.show { display:flex; }
.onboarding-card { background:rgba(245,240,232,0.95); border-radius:12px; padding:32px 40px; text-align:center; max-width:420px; box-shadow:0 20px 60px rgba(0,0,0,0.3); }
.onboarding-card h2 { font-size:22px; color:#2c2c2c; margin-bottom:12px; letter-spacing:2px; }
.onboarding-card p { font-size:14px; color:#666; line-height:1.8; margin-bottom:20px; }
.onboarding-card .hint { font-size:13px; color:#c23531; margin-bottom:16px; }
.onboarding-btn { padding:8px 24px; background:#c23531; color:#fff; border:none; border-radius:4px; font-size:14px; cursor:pointer; font-family:inherit; }
.onboarding-btn:hover { background:#a02828; }
.tooltip { position:absolute; background:rgba(44,44,44,0.9); color:#f5f0e8; padding:6px 12px; border-radius:4px; font-size:13px; pointer-events:none; z-index:200; white-space:nowrap; backdrop-filter:blur(4px); }
/* Leaflet 覆盖 */
.leaflet-container { background:#f5f0e8 !important; }
"""

LOADING_HTML = """
<div class="loading" id="loading">
    <div class="spinner"></div>
    <div class="loading-text">唐 诗 社 交 网 络</div>
    <div class="loading-sub">正在加载 57,607 首唐诗...</div>
</div>
"""

HEADER_HTML = """
<div class="header">
    <h1>唐 诗 社 交 网 络</h1>
    <div class="header-center">
        <div class="search-wrap">
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="搜索诗人、诗题、诗句... (按 / 聚焦)">
            </div>
            <div class="autocomplete" id="autocomplete"></div>
        </div>
        <div class="quick-nav">
            <button class="quick-btn" onclick="searchAndFocus('李白')">李白</button>
            <button class="quick-btn" onclick="searchAndFocus('杜甫')">杜甫</button>
            <button class="quick-btn" onclick="searchAndFocus('白居易')">白居易</button>
            <button class="quick-btn" onclick="searchAndFocus('王維')">王维</button>
            <button class="quick-btn" onclick="searchAndFocus('李商隱')">李商隐</button>
            <button class="fun-btn" onclick="randomPoet()">🎲 随机</button>
        </div>
    </div>
    <div class="header-right">
        <div class="tabs">
            <button class="tab active" data-tab="network">🕸️ 网络图</button>
            <button class="tab" data-tab="map">🗺️ 地图</button>
            <button class="tab" data-tab="stats">📊 统计</button>
        </div>
        <div class="legend" id="legend">
            <div class="legend-item" data-period="初唐"><div class="legend-dot" style="background:#61a0a8"></div>初唐</div>
            <div class="legend-item" data-period="盛唐"><div class="legend-dot" style="background:#c23531"></div>盛唐</div>
            <div class="legend-item" data-period="中唐"><div class="legend-dot" style="background:#2f4554"></div>中唐</div>
            <div class="legend-item" data-period="晚唐"><div class="legend-dot" style="background:#d48265"></div>晚唐</div>
        </div>
    </div>
</div>
<div class="view active" id="graph"></div>
<div class="view" id="mapView"></div>
<div class="view" id="statsView"></div>
<div class="legend-help">
    <span>节点大小 = 诗作数量</span>
    <span>连线粗细 = 赠诗次数</span>
    <span>拖拽移动 · 滚轮缩放 · 点击探索</span>
</div>
<div class="panel" id="panel">
    <button class="panel-close" onclick="closePanel()" title="关闭面板 (Esc)">×</button>
    <div class="panel-empty" id="panelEmpty">
        <div>
            <div class="path-finder">
                <h3>🔍 诗人关系路径</h3>
                <div class="path-inputs">
                    <input type="text" id="pathFrom" placeholder="诗人A">
                    <span>→</span>
                    <input type="text" id="pathTo" placeholder="诗人B">
                    <button class="path-btn" onclick="findPath()">查找</button>
                </div>
                <div id="pathResult" class="path-result"></div>
                <div class="path-examples">
                    试试: <span onclick="setPath('李白','杜甫')">李白→杜甫</span>
                    <span onclick="setPath('王維','李商隱')">王维→李商隐</span>
                    <span onclick="setPath('白居易','元稹')">白居易→元稹</span>
                </div>
            </div>
            <div style="color:#bbb;font-size:12px;text-align:center">
                点击节点探索诗人 · 点击连线查看关系<br>
                按 Esc 关闭面板 · / 搜索 · Tab 切换视图
            </div>
        </div>
    </div>
    <div id="panelContent" style="display:none"></div>
</div>
<div class="stats-bar">
    <span>{total_poets} 位诗人</span>
    <span>{total_edges} 条赠诗关系</span>
    <span>{total_poems} 首唐诗</span>
    <span>{matched_poets} 位诗人有作品</span>
</div>
<div class="tooltip" id="tooltip" style="display:none"></div>
<div class="modal-overlay" id="modalOverlay">
    <div class="modal">
        <div class="modal-header"><h2 id="modalTitle"></h2><button class="modal-close" onclick="closeModal()">&times;</button></div>
        <div class="modal-search"><input type="text" id="modalSearch" placeholder="搜索..."></div>
        <div class="modal-body" id="modalBody"></div>
    </div>
</div>
<div class="onboarding" id="onboarding">
    <div class="onboarding-card">
        <h2>欢迎探索唐诗社交网络</h2>
        <p>这里汇聚了 <b>1,381</b> 位唐代诗人、<b>8,259</b> 条赠诗关系、<b>57,607</b> 首唐诗。</p>
        <div class="hint">试试搜索「春眠不觉晓」或探索诗人关系路径</div>
        <button class="onboarding-btn" onclick="closeOnboarding()">开始探索</button>
    </div>
</div>
"""

JS = r"""
// ============ 加载 ============
window.addEventListener('load', () => setTimeout(() => document.getElementById('loading').classList.add('hide'), 300));

// ============ 数据 ============
const nodeMap = new Map(DATA.nodes.map(n => [n.id, n]));
const edgesFiltered = DATA.edges.filter(e => nodeMap.has(e.source) && nodeMap.has(e.target));
const activePeriods = new Set(Object.keys(PERIOD_COLORS));
const poemIndex = [];
DATA.nodes.forEach(n => (n.poems||[]).forEach(p => poemIndex.push({poet:n.id, title:p.title, text:p.text, period:n.period})));

// ============ Tab 切换 ============
let currentTab = 'network';
document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        currentTab = tab.dataset.tab;
        document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
        document.getElementById(currentTab === 'network' ? 'graph' : currentTab === 'map' ? 'mapView' : 'statsView').classList.add('active');
        document.querySelector('.legend-help').style.display = currentTab === 'network' ? 'flex' : 'none';
        document.querySelector('.legend').style.display = currentTab === 'network' ? 'flex' : 'none';
        if (currentTab === 'map' && !mapInitialized) initMap();
        if (currentTab === 'stats' && !statsInitialized) initStats();
    });
});

// ============ 网络图 (D3.js) ============
const container = document.getElementById('graph');
const width = container.clientWidth, height = container.clientHeight;
const svg = d3.select('#graph').append('svg').attr('width', width).attr('height', height);
const g = svg.append('g');
const zoom = d3.zoom().scaleExtent([0.1, 8]).on('zoom', e => g.attr('transform', e.transform));
svg.call(zoom);

function getNodeRadius(d) { return Math.max(3, Math.min(25, 3 + Math.sqrt(d.poemCount||1) * 1.5)); }

const simulation = d3.forceSimulation(DATA.nodes)
    .force('link', d3.forceLink(edgesFiltered).id(d => d.id).distance(80))
    .force('charge', d3.forceManyBody().strength(-120))
    .force('center', d3.forceCenter(width/2, height/2))
    .force('collision', d3.forceCollide().radius(d => getNodeRadius(d) + 2));

const link = g.append('g').selectAll('line').data(edgesFiltered).join('line')
    .attr('stroke','rgba(44,44,44,0.15)').attr('stroke-width', d => Math.max(0.5, Math.min(3, d.weight*0.5)))
    .style('cursor','pointer')
    .on('click', (e,d) => showEdgeDetail(d))
    .on('mouseover', function(e,d) { d3.select(this).attr('stroke','rgba(194,53,49,0.7)').attr('stroke-width',Math.max(2,d.weight*0.8)); showTooltip(e,(d.source.id||d.source)+' 赠诗给 '+(d.target.id||d.target)+' ('+d.weight+'次)'); })
    .on('mouseout', function(e,d) { d3.select(this).attr('stroke','rgba(44,44,44,0.15)').attr('stroke-width',Math.max(0.5,d.weight*0.5)); hideTooltip(); });

const node = g.append('g').selectAll('circle').data(DATA.nodes).join('circle')
    .attr('r', d => getNodeRadius(d)).attr('fill', d => PERIOD_COLORS[d.period]||'#999')
    .attr('stroke','#f5f0e8').attr('stroke-width',1).attr('opacity',0.85).style('cursor','pointer')
    .call(d3.drag().on('start',dragStart).on('drag',dragging).on('end',dragEnd))
    .on('click', (e,d) => showNodeDetail(d))
    .on('mouseover', function(e,d) { d3.select(this).attr('stroke','#c23531').attr('stroke-width',3).attr('filter','drop-shadow(0 0 6px rgba(194,53,49,0.5))'); showTooltip(e,d.id+' ('+(d.poemCount||0)+'首诗, '+d.totalDegree+'条关系)'); highlightNode(d); })
    .on('mouseout', function() { d3.select(this).attr('stroke','#f5f0e8').attr('stroke-width',1).attr('filter',null); hideTooltip(); resetHighlight(); });

const labelThreshold = 5;
const label = g.append('g').selectAll('text').data(DATA.nodes.filter(d => d.totalDegree >= labelThreshold)).join('text')
    .text(d => d.id).attr('font-size', d => d.totalDegree >= 15 ? 12 : 10)
    .attr('fill','#2c2c2c').attr('text-anchor','middle').attr('dy', d => -getNodeRadius(d)-4)
    .style('pointer-events','none').style('font-family',"'STKaiti','KaiTi',serif");

simulation.on('tick', () => {
    link.attr('x1',d=>d.source.x).attr('y1',d=>d.source.y).attr('x2',d=>d.target.x).attr('y2',d=>d.target.y);
    node.attr('cx',d=>d.x).attr('cy',d=>d.y);
    label.attr('x',d=>d.x).attr('y',d=>d.y);
});

function dragStart(e,d) { if(!e.active) simulation.alphaTarget(0.3).restart(); d.fx=d.x; d.fy=d.y; }
function dragging(e,d) { d.fx=e.x; d.fy=e.y; }
function dragEnd(e,d) { if(!e.active) simulation.alphaTarget(0); d.fx=null; d.fy=null; }

// ============ 地图 (Leaflet.js) ============
let mapInitialized = false, map, mapMarkers;
function initMap() {
    mapInitialized = true;
    map = L.map('mapView').setView([34, 110], 4);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap', maxZoom: 18
    }).addTo(map);
    mapMarkers = L.layerGroup().addTo(map);
    const geoNodes = DATA.nodes.filter(n => n.lng && n.lat);
    geoNodes.forEach(n => {
        const color = PERIOD_COLORS[n.period] || '#999';
        const r = Math.max(3, Math.min(12, 3 + Math.sqrt(n.poemCount||1)*0.8));
        const circle = L.circleMarker([n.lat, n.lng], {
            radius: r, fillColor: color, color: '#fff', weight: 1, fillOpacity: 0.8
        });
        circle.bindTooltip(n.id + ' (' + (n.poemCount||0) + '首)', {direction:'top', offset:[0,-r]});
        circle.on('click', () => {
            const poems = (n.poems || []).slice(0, 3);
            let popupHtml = '<div style="font-family:STKaiti,KaiTi,serif;min-width:200px">';
            popupHtml += '<div style="font-size:16px;font-weight:bold;margin-bottom:4px">' + n.id + '</div>';
            popupHtml += '<div style="font-size:12px;color:#888;margin-bottom:8px">' + n.period + (n.place ? ' · ' + n.place : '') + '</div>';
            popupHtml += '<div style="font-size:12px;margin-bottom:8px">诗作: ' + (n.poemCount||0) + ' · 赠诗: ' + n.outDegree + ' · 被赠: ' + n.inDegree + '</div>';
            if (poems.length > 0) {
                popupHtml += '<div style="border-top:1px solid #eee;padding-top:6px;margin-top:4px">';
                poems.forEach(p => {
                    popupHtml += '<div style="font-size:11px;color:#555;margin-bottom:4px"><b>《' + p.title + '》</b></div>';
                    const lines = p.text.split('\n').slice(0, 2).join('<br>');
                    popupHtml += '<div style="font-size:11px;color:#888;margin-bottom:6px">' + lines + '</div>';
                });
                popupHtml += '</div>';
            }
            popupHtml += '<div style="margin-top:8px"><a href="javascript:void(0)" onclick="switchTab(\'network\');searchAndFocus(\'' + n.id + '\')" style="color:#c23531;font-size:12px">在网络图中查看 →</a></div>';
            popupHtml += '</div>';
            circle.bindPopup(popupHtml, {maxWidth: 300}).openPopup();
        });
        circle.addTo(mapMarkers);
    });
}

function switchTab(tab) {
    document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.dataset.tab === tab));
    currentTab = tab;
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    document.getElementById(tab === 'network' ? 'graph' : tab === 'map' ? 'mapView' : 'statsView').classList.add('active');
    document.querySelector('.legend-help').style.display = tab === 'network' ? 'flex' : 'none';
    document.querySelector('.legend').style.display = tab === 'network' ? 'flex' : 'none';
    if (tab === 'map' && !mapInitialized) initMap();
    if (tab === 'stats' && !statsInitialized) initStats();
}

// ============ 统计 (Chart.js) ============
let statsInitialized = false;
function initStats() {
    statsInitialized = true;
    const sv = document.getElementById('statsView');
    const pd = STATS.periodDist;
    const tp = STATS.topPoets;
    const ns = STATS.networkStats;
    const periods = ['初唐','盛唐','中唐','晚唐','未知'];
    const pColors = periods.map(p => PERIOD_COLORS[p] || '#999');

    sv.innerHTML = `
    <div class="stats-summary">
        <div class="stats-summary-item"><div class="stats-summary-num">${DATA.nodes.length}</div><div class="stats-summary-label">诗人总数</div></div>
        <div class="stats-summary-item"><div class="stats-summary-num">${edgesFiltered.length}</div><div class="stats-summary-label">赠诗关系</div></div>
        <div class="stats-summary-item"><div class="stats-summary-num">${poemIndex.length}</div><div class="stats-summary-label">收录诗作</div></div>
        <div class="stats-summary-item"><div class="stats-summary-num">${ns.avgDegree}</div><div class="stats-summary-label">平均连接度</div></div>
    </div>
    <div class="stats-grid">
        <div class="stats-card"><h3>📊 朝代分布</h3><canvas id="chartPeriod"></canvas></div>
        <div class="stats-card"><h3>🏆 最具影响力诗人 TOP 20</h3><canvas id="chartTop"></canvas></div>
    </div>`;

    new Chart(document.getElementById('chartPeriod'), {
        type: 'doughnut',
        data: { labels: periods, datasets: [{ data: periods.map(p => pd[p]||0), backgroundColor: pColors, borderWidth: 0 }] },
        options: { responsive: true, plugins: { legend: { position: 'bottom' } } }
    });

    new Chart(document.getElementById('chartTop'), {
        type: 'bar',
        data: {
            labels: tp.map(p => p.id),
            datasets: [
                { label: '赠诗', data: tp.map(p => p.outDegree), backgroundColor: 'rgba(194,53,49,0.7)' },
                { label: '被赠', data: tp.map(p => p.inDegree), backgroundColor: 'rgba(47,69,84,0.7)' }
            ]
        },
        options: {
            indexAxis: 'y', responsive: true, scales: { x: { stacked: true }, y: { stacked: true } },
            plugins: { legend: { position: 'bottom' } }
        }
    });
}

// ============ 路径查找 (BFS) ============
function findPath() {
    const from = document.getElementById('pathFrom').value.trim();
    const to = document.getElementById('pathTo').value.trim();
    if (!from || !to) { document.getElementById('pathResult').innerHTML = '<div style="color:#999">请输入两位诗人</div>'; return; }
    if (!nodeMap.has(from)) { document.getElementById('pathResult').innerHTML = '<div style="color:#c23531">找不到「'+from+'」</div>'; return; }
    if (!nodeMap.has(to)) { document.getElementById('pathResult').innerHTML = '<div style="color:#c23531">找不到「'+to+'」</div>'; return; }
    if (from === to) { document.getElementById('pathResult').innerHTML = '<div style="color:#999">两位诗人相同</div>'; return; }

    // 构建邻接表
    const adj = new Map();
    edgesFiltered.forEach(e => {
        const s = e.source.id || e.source, t = e.target.id || e.target;
        if (!adj.has(s)) adj.set(s, []); if (!adj.has(t)) adj.set(t, []);
        adj.get(s).push({node: t, edge: e}); adj.get(t).push({node: s, edge: e});
    });

    // BFS
    const queue = [[from]]; const visited = new Set([from]);
    let found = null;
    while (queue.length > 0 && !found) {
        const path = queue.shift();
        const curr = path[path.length - 1];
        for (const {node: next} of (adj.get(curr) || [])) {
            if (visited.has(next)) continue;
            visited.add(next);
            const newPath = [...path, next];
            if (next === to) { found = newPath; break; }
            queue.push(newPath);
        }
    }

    if (!found) { document.getElementById('pathResult').innerHTML = '<div style="color:#999">未找到关系路径</div>'; return; }

    // 显示路径
    let html = '<div style="font-size:13px;color:#2c2c2c;margin-bottom:8px">关系链 (' + (found.length-1) + ' 步):</div>';
    for (let i = 0; i < found.length; i++) {
        const n = nodeMap.get(found[i]);
        html += '<div class="path-step"><span class="path-node" onclick="searchAndFocus(\''+found[i]+'\')">'+found[i]+'</span>';
        if (n) html += '<span style="font-size:11px;color:#999">('+(n.poemCount||0)+'首)</span>';
        if (i < found.length - 1) html += '<span class="path-arrow"> → </span>';
        html += '</div>';
    }
    document.getElementById('pathResult').innerHTML = html;

    // 高亮路径
    const pathSet = new Set(found);
    const pathEdges = new Set();
    for (let i = 0; i < found.length - 1; i++) {
        const a = found[i], b = found[i+1];
        edgesFiltered.forEach(e => {
            const s = e.source.id || e.source, t = e.target.id || e.target;
            if ((s===a && t===b) || (s===b && t===a)) pathEdges.add(e);
        });
    }
    node.attr('opacity', n => pathSet.has(n.id) ? 1 : 0.08);
    link.attr('stroke', e => pathEdges.has(e) ? '#c23531' : 'rgba(44,44,44,0.03)')
        .attr('stroke-width', e => pathEdges.has(e) ? 3 : 0.3);
    label.attr('opacity', n => pathSet.has(n.id) ? 1 : 0.08);
}

function setPath(a, b) { document.getElementById('pathFrom').value = a; document.getElementById('pathTo').value = b; findPath(); }

// ============ 趣味功能 ============
function randomPoet() {
    const withPoems = DATA.nodes.filter(n => n.poemCount > 0);
    const pick = withPoems[Math.floor(Math.random() * withPoems.length)];
    if (pick) searchAndFocus(pick.id);
}

// ============ Tooltip ============
const tooltip = document.getElementById('tooltip');
function showTooltip(e, text) { tooltip.textContent = text; tooltip.style.display = 'block'; tooltip.style.left = (e.pageX+12)+'px'; tooltip.style.top = (e.pageY-8)+'px'; }
function hideTooltip() { tooltip.style.display = 'none'; }

// ============ 高亮 ============
function highlightNode(d) {
    const connected = new Set(); connected.add(d.id);
    edgesFiltered.forEach(e => { const s=e.source.id||e.source, t=e.target.id||e.target; if(s===d.id) connected.add(t); if(t===d.id) connected.add(s); });
    node.attr('opacity', n => connected.has(n.id) ? 1 : 0.08);
    link.attr('stroke', e => { const s=e.source.id||e.source, t=e.target.id||e.target; return (s===d.id||t===d.id) ? 'rgba(194,53,49,0.6)' : 'rgba(44,44,44,0.03)'; })
        .attr('stroke-width', e => { const s=e.source.id||e.source, t=e.target.id||e.target; return (s===d.id||t===d.id) ? Math.max(1.5,e.weight*0.8) : Math.max(0.3,e.weight*0.3); });
    label.attr('opacity', n => connected.has(n.id) ? 1 : 0.08);
}
function resetHighlight() {
    node.attr('opacity', d => activePeriods.has(d.period) ? 0.85 : 0.05);
    link.attr('stroke','rgba(44,44,44,0.15)').attr('stroke-width', d => Math.max(0.5,d.weight*0.5));
    label.attr('opacity', 1);
}

// ============ 时期过滤 ============
function applyFilter() {
    node.attr('opacity', d => activePeriods.has(d.period) ? 0.85 : 0.05).attr('pointer-events', d => activePeriods.has(d.period) ? 'auto' : 'none');
    link.attr('opacity', d => { const s=d.source.id||d.source, t=d.target.id||d.target; const sn=nodeMap.get(s), tn=nodeMap.get(t); return (sn&&activePeriods.has(sn.period)&&tn&&activePeriods.has(tn.period)) ? 1 : 0.03; });
    label.attr('opacity', d => activePeriods.has(d.period) ? 1 : 0.05);
    document.querySelectorAll('.legend-item').forEach(el => el.classList.toggle('inactive', !activePeriods.has(el.dataset.period)));
}
document.querySelectorAll('.legend-item').forEach(el => {
    el.addEventListener('click', () => { const p=el.dataset.period; activePeriods.has(p) ? activePeriods.delete(p) : activePeriods.add(p); applyFilter(); });
});

// ============ 搜索 ============
const searchInput = document.getElementById('searchInput');
const acEl = document.getElementById('autocomplete');
let acIndex = -1, searchTimer = null;

searchInput.addEventListener('input', function() { clearTimeout(searchTimer); const q=this.value.trim(); if(!q){acEl.style.display='none';resetHighlight();return;} searchTimer=setTimeout(()=>doSearch(q),150); });

function doSearch(q) {
    const results = [];
    DATA.nodes.filter(n => n.id.includes(q)).slice(0,5).forEach(m => results.push({type:'poet',data:m}));
    const pm = [];
    for (let i=0; i<poemIndex.length && pm.length<8; i++) { const p=poemIndex[i]; if(p.title.includes(q)||p.text.includes(q)) pm.push(p); }
    pm.forEach(m => results.push({type:'poem',data:m}));
    if (results.length === 0) { acEl.style.display = 'none'; return; }
    acIndex = -1; renderAC(results, q); acEl.style.display = 'block';
}

function hl(text, q) { if(!q) return text; const i=text.indexOf(q); if(i===-1) return text; const s=Math.max(0,i-10), e=Math.min(text.length,i+q.length+20); return (s>0?'...':'')+text.slice(s,e).replace(q,'<span class="ac-highlight">'+q+'</span>')+(e<text.length?'...':''); }

function renderAC(results, q) {
    let html = '', ps=false, ms=false;
    results.forEach((r,i) => {
        if(r.type==='poet'&&!ps){html+='<div class="ac-section">诗人</div>';ps=true;}
        if(r.type==='poem'&&!ms){html+='<div class="ac-section">诗作</div>';ms=true;}
        if(r.type==='poet'){const m=r.data;const c=PERIOD_COLORS[m.period]||'#999';html+='<div class="ac-item" data-idx="'+i+'" data-type="poet" data-name="'+m.id+'"><div class="ac-left"><span class="ac-pd" style="background:'+c+'"></span><span class="ac-name">'+m.id+'</span><span class="ac-ctx">'+m.period+(m.place?' · '+m.place:'')+'</span></div><span class="ac-right">'+(m.poemCount||0)+'首</span></div>';}
        else{const p=r.data;html+='<div class="ac-item" data-idx="'+i+'" data-type="poem" data-poet="'+p.poet+'"><div class="ac-left"><span class="ac-name">'+p.poet+'</span><span class="ac-ctx">《'+p.title+'》'+hl(p.text,q)+'</span></div></div>';}
    });
    acEl.innerHTML = html;
    acEl.querySelectorAll('.ac-item').forEach(item => item.addEventListener('click', () => { searchAndFocus(item.dataset.type==='poet'?item.dataset.name:item.dataset.poet); acEl.style.display='none'; }));
}

searchInput.addEventListener('keydown', function(e) {
    const items = acEl.querySelectorAll('.ac-item');
    if(e.key==='ArrowDown'){e.preventDefault();acIndex=Math.min(acIndex+1,items.length-1);updAC(items);}
    else if(e.key==='ArrowUp'){e.preventDefault();acIndex=Math.max(acIndex-1,0);updAC(items);}
    else if(e.key==='Enter'){e.preventDefault();if(acIndex>=0&&items[acIndex]){const it=items[acIndex];searchAndFocus(it.dataset.type==='poet'?it.dataset.name:it.dataset.poet);}else{const q=this.value.trim();if(q){const m=DATA.nodes.find(n=>n.id===q)||DATA.nodes.find(n=>n.id.includes(q));if(m)searchAndFocus(m.id);}}acEl.style.display='none';}
    else if(e.key==='Escape'){acEl.style.display='none';this.blur();}
});
function updAC(items){items.forEach((it,i)=>it.classList.toggle('active',i===acIndex));if(items[acIndex])items[acIndex].scrollIntoView({block:'nearest'});}
document.addEventListener('click', e => { if(!e.target.closest('.search-wrap')) acEl.style.display='none'; });

// ============ 关闭面板 ============
function closePanel() {
    document.getElementById('panelContent').style.display = 'none';
    document.getElementById('panelEmpty').style.display = 'flex';
    resetHighlight();
}

// ============ 键盘 ============
document.addEventListener('keydown', e => {
    if(e.key==='/' && document.activeElement!==searchInput && !document.querySelector('.modal-overlay.show')){e.preventDefault();searchInput.focus();}
    if(e.key==='Escape'){
        if(document.querySelector('.modal-overlay.show'))closeModal();
        else if(document.getElementById('onboarding').classList.contains('show'))closeOnboarding();
        else{closePanel();}
    }
    if(e.key==='Tab' && document.activeElement===document.body){e.preventDefault();const tabs=['network','map','stats'];const idx=tabs.indexOf(currentTab);switchTab(tabs[(idx+1)%tabs.length]);}
});

// ============ 搜索聚焦 ============
function searchAndFocus(name) {
    searchInput.value=name; acEl.style.display='none';
    const match=nodeMap.get(name);
    if(match){highlightNode(match);showNodeDetail(match);svg.transition().duration(750).call(zoom.transform,d3.zoomIdentity.translate(width/2,height/2).scale(2).translate(-match.x,-match.y));history.replaceState(null,'','#'+encodeURIComponent(name));}
}

// ============ URL路由 ============
function handleHash(){const h=decodeURIComponent(location.hash.slice(1));if(h&&nodeMap.has(h))setTimeout(()=>searchAndFocus(h),500);}
window.addEventListener('hashchange',handleHash);handleHash();

// ============ 详情面板 ============
function getRelations(d){const r=[];edgesFiltered.forEach(e=>{const s=e.source.id||e.source,t=e.target.id||e.target;if(s===d.id)r.push({name:t,dir:'赠诗给',weight:e.weight});if(t===d.id)r.push({name:s,dir:'收到赠诗',weight:e.weight});});r.sort((a,b)=>b.weight-a.weight);return r;}

function showNodeDetail(d) {
    const panel=document.getElementById('panelContent');document.getElementById('panelEmpty').style.display='none';panel.style.display='block';
    const pc=PERIOD_COLORS[d.period]||'#999';const rels=getRelations(d);const poems=d.poems||[];
    let h='<div class="panel-title">'+d.id+'</div><div class="panel-period" style="background:'+pc+'">'+d.period+'</div>';
    if(d.place)h+='<div style="color:#888;font-size:13px;margin-bottom:12px">\u{1F4CD} '+d.place+'</div>';
    h+='<div class="panel-stats"><div class="panel-stat" onclick="showPoemsModal(\''+d.id+'\')"><div class="panel-stat-num">'+(d.poemCount||0)+'</div><div class="panel-stat-label">诗作 \u{1F4D6}</div></div>';
    h+='<div class="panel-stat" onclick="showRelationsModal(\''+d.id+'\',\'out\')"><div class="panel-stat-num">'+d.outDegree+'</div><div class="panel-stat-label">赠诗 \u{2709}</div></div>';
    h+='<div class="panel-stat" onclick="showRelationsModal(\''+d.id+'\',\'in\')"><div class="panel-stat-num">'+d.inDegree+'</div><div class="panel-stat-label">被赠 \u{1F4E8}</div></div></div>';
    if(poems.length>0){h+='<div class="panel-section"><h3>代表诗作 ';if(poems.length>5)h+='<span class="view-all" onclick="showPoemsModal(\''+d.id+'\')">查看全部 '+poems.length+' 首 \u{2192}</span>';h+='</h3>';poems.slice(0,5).forEach(p=>{h+='<div class="poem-card"><div class="poem-title">《'+p.title+'》</div><div class="poem-text">'+p.text+'</div></div>';});h+='</div>';}
    if(rels.length>0){h+='<div class="panel-section"><h3>社交关系 ('+rels.length+') ';if(rels.length>15)h+='<span class="view-all" onclick="showRelationsModal(\''+d.id+'\',\'all\')">查看全部 \u{2192}</span>';h+='</h3>';rels.slice(0,15).forEach(r=>{h+='<div class="relation-item" onclick="searchAndFocus(\''+r.name+'\')"><b>'+r.name+'</b> — '+r.dir+' '+r.weight+' 次</div>';});h+='</div>';}
    panel.innerHTML=h;history.replaceState(null,'','#'+encodeURIComponent(d.id));
}

function showEdgeDetail(d) {
    const panel=document.getElementById('panelContent');document.getElementById('panelEmpty').style.display='none';panel.style.display='block';
    const s=d.source.id||d.source,t=d.target.id||d.target;const sn=nodeMap.get(s),tn=nodeMap.get(t);
    let h='<div class="panel-title">'+s+' \u{2194} '+t+'</div><div style="color:#888;font-size:13px;margin-bottom:16px">赠诗 '+d.weight+' 次</div>';
    [['src',s,sn],['tgt',t,tn]].forEach(([k,n,nd])=>{const ps=(nd?.poems||[]).slice(0,5);h+='<div class="panel-section"><h3>'+n+' 的诗作</h3>';if(ps.length>0){ps.forEach(p=>{h+='<div class="poem-card"><div class="poem-title">《'+p.title+'》</div><div class="poem-text">'+p.text+'</div></div>';});}else{h+='<div style="color:#999">暂无诗作数据</div>';}h+='</div>';});
    panel.innerHTML=h;
}

// ============ 弹窗 ============
let md=[],mt='';
function showModal(t,d,tp){md=d;mt=tp;document.getElementById('modalTitle').textContent=t;renderMI(d);document.getElementById('modalOverlay').classList.add('show');document.getElementById('modalSearch').value='';setTimeout(()=>document.getElementById('modalSearch').focus(),100);}
function closeModal(){document.getElementById('modalOverlay').classList.remove('show');}
function renderMI(items){const b=document.getElementById('modalBody');if(items.length===0){b.innerHTML='<div class="modal-empty">暂无数据</div>';return;}b.innerHTML=items.map(i=>{if(mt==='poems')return '<div class="poem-card"><div class="poem-title">《'+i.title+'》</div><div class="poem-text">'+i.text+'</div></div>';return '<div class="modal-item" onclick="closeModal();searchAndFocus(\''+i.name+'\')"><b>'+i.name+'</b> — '+i.dir+' '+i.weight+' 次</div>';}).join('');}
document.getElementById('modalSearch').addEventListener('input',function(){const q=this.value.trim();if(!q){renderMI(md);return;}renderMI(md.filter(i=>mt==='poems'?(i.title.includes(q)||i.text.includes(q)):i.name.includes(q)));});
document.getElementById('modalOverlay').addEventListener('click',e=>{if(e.target===document.getElementById('modalOverlay'))closeModal();});
function showPoemsModal(n){const d=nodeMap.get(n);if(!d)return;showModal(n+' 的诗作 ('+(d.poemCount||0)+'首)',d.poems||[],'poems');}
function showRelationsModal(n,dir){const d=nodeMap.get(n);if(!d)return;const r=getRelations(d);let f=r,t=n+' 的社交关系';if(dir==='out'){f=r.filter(r=>r.dir==='赠诗给');t=n+' 赠诗给...';}if(dir==='in'){f=r.filter(r=>r.dir==='收到赠诗');t='赠诗给 '+n+' 的人...';}showModal(t+' ('+f.length+'人)',f,'relations');}

// ============ 引导 ============
function closeOnboarding(){document.getElementById('onboarding').classList.remove('show');localStorage.setItem('tpn_visited','1');}
if(!localStorage.getItem('tpn_visited'))setTimeout(()=>document.getElementById('onboarding').classList.add('show'),500);

// ============ 自适应 ============
window.addEventListener('resize',()=>{const w=container.clientWidth,h=container.clientHeight;svg.attr('width',w).attr('height',h);simulation.force('center',d3.forceCenter(w/2,h/2));simulation.alpha(0.1).restart();});
"""

if __name__ == '__main__':
    build()
