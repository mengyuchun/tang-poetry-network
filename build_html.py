"""
唐诗社交网络 — 构建单文件 HTML（v3 全功能版）
全文搜索 · 时期过滤 · 新手引导 · 弹窗详情 · 加载动画 · URL路由
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
    period_colors = {'初唐': '#61a0a8', '盛唐': '#c23531', '中唐': '#2f4554', '晚唐': '#d48265', '未知': '#999'}

    data_json = json.dumps({'nodes': nodes, 'edges': edges}, ensure_ascii=False)
    colors_json = json.dumps(period_colors, ensure_ascii=False)

    html = '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n'
    html += '<meta charset="UTF-8">\n'
    html += '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
    html += '<title>唐诗社交网络</title>\n'
    html += '<meta name="description" content="1,381位诗人 · 8,259条赠诗关系 · 57,607首唐诗 · 交互式探索">\n'
    html += '<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🏮</text></svg>">\n'
    html += '<style>\n' + CSS + '\n</style>\n</head>\n<body>\n'
    html += LOADING_HTML
    html += HEADER_HTML.format(
        total_poets=stats['total_poets'],
        total_edges=stats['total_edges'],
        total_poems=stats['total_poems'],
        matched_poets=stats['matched_poets']
    )
    html += '\n<script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script>\n'
    html += '<script>\nconst DATA = ' + data_json + ';\n'
    html += 'const PERIOD_COLORS = ' + colors_json + ';\n'
    html += JS + '\n</script>\n</body>\n</html>'

    output_path = os.path.join(DIST_DIR, 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"已生成: {output_path} ({size_mb:.1f} MB)")


CSS = r"""
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: 'STKaiti', 'KaiTi', 'Noto Serif SC', 'SimSun', serif;
    background: #f5f0e8; color: #2c2c2c; overflow: hidden; height: 100vh;
}
body::before {
    content: ''; position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background:
        radial-gradient(ellipse at 20% 50%, rgba(200,180,150,0.15) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 20%, rgba(180,160,130,0.1) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 80%, rgba(190,170,140,0.1) 0%, transparent 50%);
    pointer-events: none; z-index: 0;
}
/* 加载动画 */
.loading {
    position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background: #f5f0e8; z-index: 9999; display: flex;
    flex-direction: column; align-items: center; justify-content: center;
    transition: opacity 0.5s;
}
.loading.hide { opacity: 0; pointer-events: none; }
.loading-text { font-size: 18px; color: #2c2c2c; letter-spacing: 4px; margin-top: 20px; }
.loading-sub { font-size: 13px; color: #999; margin-top: 8px; }
.spinner {
    width: 40px; height: 40px; border: 3px solid rgba(44,44,44,0.1);
    border-top-color: #c23531; border-radius: 50%;
    animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
/* 顶部栏 */
.header {
    position: fixed; top: 0; left: 0; right: 0; height: 56px;
    background: rgba(44,44,44,0.92); display: flex; align-items: center;
    justify-content: space-between; padding: 0 24px; z-index: 100;
    backdrop-filter: blur(8px);
}
.header h1 { color: #f5f0e8; font-size: 20px; font-weight: 400; letter-spacing: 4px; white-space: nowrap; }
/* 搜索框 */
.search-wrap { position: relative; }
.search-box input {
    width: 320px; padding: 6px 12px; border: 1px solid rgba(245,240,232,0.3);
    border-radius: 4px; background: rgba(245,240,232,0.1); color: #f5f0e8;
    font-family: inherit; font-size: 14px; outline: none;
}
.search-box input::placeholder { color: rgba(245,240,232,0.5); }
.search-box input:focus { border-color: #c23531; }
.autocomplete {
    position: absolute; top: 100%; left: 0; width: 400px; max-height: 400px;
    overflow-y: auto; background: rgba(44,44,44,0.95); border-radius: 0 0 4px 4px;
    display: none; z-index: 200; backdrop-filter: blur(8px);
}
.ac-section { padding: 4px 12px; font-size: 10px; color: rgba(245,240,232,0.4); text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid rgba(245,240,232,0.1); }
.ac-item {
    padding: 8px 12px; color: #f5f0e8; font-size: 13px; cursor: pointer;
    display: flex; justify-content: space-between; align-items: center;
    border-bottom: 1px solid rgba(245,240,232,0.05);
}
.ac-item:hover, .ac-item.active { background: rgba(194,53,49,0.3); }
.ac-item .ac-left { display: flex; align-items: center; gap: 6px; flex: 1; min-width: 0; }
.ac-item .ac-period-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.ac-item .ac-name { font-weight: bold; white-space: nowrap; }
.ac-item .ac-context { font-size: 11px; color: rgba(245,240,232,0.6); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.ac-item .ac-right { font-size: 11px; color: rgba(245,240,232,0.5); white-space: nowrap; margin-left: 8px; }
.ac-poem-match { padding: 6px 12px 6px 26px; }
.ac-poem-match .ac-poem-title { font-size: 12px; color: rgba(245,240,232,0.7); }
.ac-poem-match .ac-poem-line { font-size: 12px; color: rgba(245,240,232,0.5); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.ac-highlight { color: #c23531; font-weight: bold; }
/* 快速跳转 */
.quick-nav { display: flex; gap: 6px; margin-left: 12px; }
.quick-btn {
    padding: 3px 10px; background: rgba(245,240,232,0.1); border: 1px solid rgba(245,240,232,0.2);
    border-radius: 3px; color: #f5f0e8; font-size: 12px; cursor: pointer; font-family: inherit;
    transition: all 0.2s;
}
.quick-btn:hover { background: rgba(194,53,49,0.4); border-color: #c23531; }
/* 图例 */
.legend { display: flex; gap: 12px; align-items: center; }
.legend-item {
    display: flex; align-items: center; gap: 4px; color: #f5f0e8; font-size: 12px;
    cursor: pointer; padding: 2px 6px; border-radius: 3px; transition: all 0.2s; user-select: none;
}
.legend-item:hover { background: rgba(245,240,232,0.1); }
.legend-item.inactive { opacity: 0.3; }
.legend-dot { width: 10px; height: 10px; border-radius: 50%; }
/* 统计栏 */
.stats-bar {
    position: fixed; bottom: 0; left: 0; right: 0; height: 36px;
    background: rgba(44,44,44,0.85); display: flex; align-items: center;
    justify-content: center; gap: 32px; color: rgba(245,240,232,0.8);
    font-size: 13px; z-index: 100; backdrop-filter: blur(8px);
}
.stats-bar span { letter-spacing: 1px; }
.legend-help {
    position: fixed; bottom: 36px; left: 0; right: 360px; height: 28px;
    background: rgba(245,240,232,0.85); display: flex; align-items: center;
    justify-content: center; gap: 24px; font-size: 11px; color: #888; z-index: 99;
    border-top: 1px solid rgba(44,44,44,0.1);
}
/* 网络图 */
#graph { position: fixed; top: 56px; left: 0; right: 360px; bottom: 64px; z-index: 1; }
/* 详情面板 */
.panel {
    position: fixed; top: 56px; right: 0; bottom: 36px; width: 360px;
    background: rgba(245,240,232,0.95); border-left: 1px solid rgba(44,44,44,0.15);
    overflow-y: auto; z-index: 50; padding: 20px; backdrop-filter: blur(8px);
}
.panel-empty {
    display: flex; align-items: center; justify-content: center; height: 100%;
    color: #999; font-size: 15px; text-align: center; line-height: 2;
}
.panel-title { font-size: 24px; color: #2c2c2c; margin-bottom: 8px; letter-spacing: 2px; }
.panel-period { display: inline-block; padding: 2px 10px; border-radius: 3px; font-size: 13px; color: #fff; margin-bottom: 12px; }
.panel-stats { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; margin-bottom: 16px; }
.panel-stat {
    text-align: center; padding: 8px; background: rgba(44,44,44,0.05);
    border-radius: 4px; cursor: pointer; transition: all 0.2s;
}
.panel-stat:hover { background: rgba(194,53,49,0.1); transform: scale(1.05); }
.panel-stat-num { font-size: 20px; color: #c23531; font-weight: bold; }
.panel-stat-label { font-size: 12px; color: #888; }
.panel-section { margin-bottom: 16px; }
.panel-section h3 { font-size: 15px; color: #2c2c2c; border-bottom: 1px solid rgba(44,44,44,0.15); padding-bottom: 6px; margin-bottom: 10px; }
.panel-section h3 .view-all { font-size: 11px; color: #c23531; cursor: pointer; font-weight: normal; }
.panel-section h3 .view-all:hover { text-decoration: underline; }
.poem-card { background: rgba(255,255,255,0.6); border: 1px solid rgba(44,44,44,0.1); border-radius: 4px; padding: 12px; margin-bottom: 8px; }
.poem-title { font-size: 14px; font-weight: bold; color: #2c2c2c; margin-bottom: 6px; }
.poem-text { font-size: 13px; color: #555; line-height: 1.8; white-space: pre-line; }
.relation-item { padding: 6px 0; border-bottom: 1px solid rgba(44,44,44,0.08); font-size: 13px; color: #555; cursor: pointer; }
.relation-item:hover { color: #c23531; }
.relation-item b { color: #2c2c2c; }
/* 弹窗 */
.modal-overlay {
    position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.5); z-index: 500; display: none;
    align-items: center; justify-content: center; backdrop-filter: blur(4px);
}
.modal-overlay.show { display: flex; }
.modal {
    background: #f5f0e8; border-radius: 8px; width: 90%; max-width: 700px;
    max-height: 80vh; display: flex; flex-direction: column; box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}
.modal-header {
    padding: 16px 20px; border-bottom: 1px solid rgba(44,44,44,0.15);
    display: flex; justify-content: space-between; align-items: center;
}
.modal-header h2 { font-size: 18px; color: #2c2c2c; }
.modal-close {
    width: 32px; height: 32px; border: none; background: none; font-size: 20px;
    color: #888; cursor: pointer; border-radius: 4px; display: flex;
    align-items: center; justify-content: center;
}
.modal-close:hover { background: rgba(44,44,44,0.1); color: #2c2c2c; }
.modal-search { padding: 8px 20px; border-bottom: 1px solid rgba(44,44,44,0.1); }
.modal-search input {
    width: 100%; padding: 6px 10px; border: 1px solid rgba(44,44,44,0.2);
    border-radius: 4px; font-family: inherit; font-size: 13px; outline: none;
    background: rgba(255,255,255,0.5);
}
.modal-body { padding: 12px 20px; overflow-y: auto; flex: 1; }
.modal-item {
    padding: 8px 0; border-bottom: 1px solid rgba(44,44,44,0.08);
    font-size: 13px; color: #555; cursor: pointer;
}
.modal-item:hover { color: #c23531; }
.modal-item b { color: #2c2c2c; }
.modal-empty { color: #999; text-align: center; padding: 20px; }
/* 引导浮层 */
.onboarding {
    position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.4); z-index: 300; display: none;
    align-items: center; justify-content: center; backdrop-filter: blur(2px);
}
.onboarding.show { display: flex; }
.onboarding-card {
    background: rgba(245,240,232,0.95); border-radius: 12px; padding: 32px 40px;
    text-align: center; max-width: 420px; box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}
.onboarding-card h2 { font-size: 22px; color: #2c2c2c; margin-bottom: 12px; letter-spacing: 2px; }
.onboarding-card p { font-size: 14px; color: #666; line-height: 1.8; margin-bottom: 20px; }
.onboarding-card .hint { font-size: 13px; color: #c23531; margin-bottom: 16px; }
.onboarding-btn {
    padding: 8px 24px; background: #c23531; color: #fff; border: none;
    border-radius: 4px; font-size: 14px; cursor: pointer; font-family: inherit;
}
.onboarding-btn:hover { background: #a02828; }
.tooltip {
    position: absolute; background: rgba(44,44,44,0.9); color: #f5f0e8;
    padding: 6px 12px; border-radius: 4px; font-size: 13px; pointer-events: none;
    z-index: 200; white-space: nowrap; backdrop-filter: blur(4px);
}
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
    <div style="display:flex;align-items:center;gap:16px;">
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
        </div>
    </div>
    <div class="legend" id="legend">
        <div class="legend-item" data-period="初唐"><div class="legend-dot" style="background:#61a0a8"></div>初唐</div>
        <div class="legend-item" data-period="盛唐"><div class="legend-dot" style="background:#c23531"></div>盛唐</div>
        <div class="legend-item" data-period="中唐"><div class="legend-dot" style="background:#2f4554"></div>中唐</div>
        <div class="legend-item" data-period="晚唐"><div class="legend-dot" style="background:#d48265"></div>晚唐</div>
        <div class="legend-item" data-period="未知"><div class="legend-dot" style="background:#999"></div>未知</div>
    </div>
</div>
<div id="graph"></div>
<div class="legend-help">
    <span>节点大小 = 诗作数量</span>
    <span>连线粗细 = 赠诗次数</span>
    <span>拖拽移动 · 滚轮缩放 · 点击探索</span>
</div>
<div class="panel" id="panel">
    <div class="panel-empty" id="panelEmpty">点击节点探索诗人<br>点击连线查看关系<br><br><span style="font-size:12px;color:#bbb">按 Esc 关闭面板 · / 搜索</span></div>
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
        <div class="modal-header">
            <h2 id="modalTitle"></h2>
            <button class="modal-close" onclick="closeModal()">&times;</button>
        </div>
        <div class="modal-search"><input type="text" id="modalSearch" placeholder="搜索..."></div>
        <div class="modal-body" id="modalBody"></div>
    </div>
</div>
<div class="onboarding" id="onboarding">
    <div class="onboarding-card">
        <h2>欢迎探索唐诗社交网络</h2>
        <p>这里汇聚了 <b>1,381</b> 位唐代诗人、<b>8,259</b> 条赠诗关系、<b>57,607</b> 首唐诗。</p>
        <div class="hint">试试搜索「春眠不觉晓」或点击顶部的诗人按钮</div>
        <button class="onboarding-btn" onclick="closeOnboarding()">开始探索</button>
    </div>
</div>
"""

JS = r"""
// ============ 加载完成 ============
window.addEventListener('load', () => {
    setTimeout(() => document.getElementById('loading').classList.add('hide'), 300);
});

// ============ 初始化 ============
const container = document.getElementById('graph');
const width = container.clientWidth, height = container.clientHeight;
const svg = d3.select('#graph').append('svg').attr('width', width).attr('height', height);
const g = svg.append('g');
const zoom = d3.zoom().scaleExtent([0.1, 8]).on('zoom', e => g.attr('transform', e.transform));
svg.call(zoom);

// 数据
const nodeMap = new Map(DATA.nodes.map(n => [n.id, n]));
const edgesFiltered = DATA.edges.filter(e => nodeMap.has(e.source) && nodeMap.has(e.target));
const activePeriods = new Set(Object.keys(PERIOD_COLORS));

// 构建全文搜索索引（诗人名 -> 诗作列表）
const poemIndex = [];
DATA.nodes.forEach(n => {
    (n.poems || []).forEach(p => {
        poemIndex.push({ poet: n.id, title: p.title, text: p.text, period: n.period });
    });
});

function getNodeRadius(d) { return Math.max(3, Math.min(25, 3 + Math.sqrt(d.poemCount || 1) * 1.5)); }

// 力导向
const simulation = d3.forceSimulation(DATA.nodes)
    .force('link', d3.forceLink(edgesFiltered).id(d => d.id).distance(80))
    .force('charge', d3.forceManyBody().strength(-120))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('collision', d3.forceCollide().radius(d => getNodeRadius(d) + 2));

// ============ 边 ============
const link = g.append('g').selectAll('line').data(edgesFiltered).join('line')
    .attr('stroke', 'rgba(44,44,44,0.15)')
    .attr('stroke-width', d => Math.max(0.5, Math.min(3, d.weight * 0.5)))
    .style('cursor', 'pointer')
    .on('click', (e, d) => showEdgeDetail(d))
    .on('mouseover', function(e, d) {
        d3.select(this).attr('stroke', 'rgba(194,53,49,0.7)').attr('stroke-width', Math.max(2, d.weight * 0.8));
        showTooltip(e, (d.source.id||d.source) + ' 赠诗给 ' + (d.target.id||d.target) + ' (' + d.weight + '次)');
    })
    .on('mouseout', function(e, d) {
        d3.select(this).attr('stroke', 'rgba(44,44,44,0.15)').attr('stroke-width', Math.max(0.5, d.weight * 0.5));
        hideTooltip();
    });

// ============ 节点 ============
const node = g.append('g').selectAll('circle').data(DATA.nodes).join('circle')
    .attr('r', d => getNodeRadius(d))
    .attr('fill', d => PERIOD_COLORS[d.period] || '#999')
    .attr('stroke', '#f5f0e8').attr('stroke-width', 1).attr('opacity', 0.85)
    .style('cursor', 'pointer')
    .call(d3.drag().on('start', dragStart).on('drag', dragging).on('end', dragEnd))
    .on('click', (e, d) => showNodeDetail(d))
    .on('mouseover', function(e, d) {
        d3.select(this).attr('stroke', '#c23531').attr('stroke-width', 3)
            .attr('filter', 'drop-shadow(0 0 6px rgba(194,53,49,0.5))');
        showTooltip(e, d.id + ' (' + (d.poemCount||0) + '首诗, ' + d.totalDegree + '条关系)');
        highlightNode(d);
    })
    .on('mouseout', function() {
        d3.select(this).attr('stroke', '#f5f0e8').attr('stroke-width', 1).attr('filter', null);
        hideTooltip(); resetHighlight();
    });

// 标签
const labelThreshold = 5;
const label = g.append('g').selectAll('text')
    .data(DATA.nodes.filter(d => d.totalDegree >= labelThreshold)).join('text')
    .text(d => d.id).attr('font-size', d => d.totalDegree >= 15 ? 12 : 10)
    .attr('fill', '#2c2c2c').attr('text-anchor', 'middle')
    .attr('dy', d => -getNodeRadius(d) - 4)
    .style('pointer-events', 'none').style('font-family', "'STKaiti','KaiTi',serif");

simulation.on('tick', () => {
    link.attr('x1', d => d.source.x).attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x).attr('y2', d => d.target.y);
    node.attr('cx', d => d.x).attr('cy', d => d.y);
    label.attr('x', d => d.x).attr('y', d => d.y);
});

function dragStart(e, d) { if (!e.active) simulation.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; }
function dragging(e, d) { d.fx = e.x; d.fy = e.y; }
function dragEnd(e, d) { if (!e.active) simulation.alphaTarget(0); d.fx = null; d.fy = null; }

// ============ Tooltip ============
const tooltip = document.getElementById('tooltip');
function showTooltip(e, text) {
    tooltip.textContent = text; tooltip.style.display = 'block';
    tooltip.style.left = (e.pageX + 12) + 'px'; tooltip.style.top = (e.pageY - 8) + 'px';
}
function hideTooltip() { tooltip.style.display = 'none'; }

// ============ 高亮 ============
function highlightNode(d) {
    const connected = new Set(); connected.add(d.id);
    edgesFiltered.forEach(e => {
        const sid = e.source.id || e.source, tid = e.target.id || e.target;
        if (sid === d.id) connected.add(tid); if (tid === d.id) connected.add(sid);
    });
    node.attr('opacity', n => connected.has(n.id) ? 1 : 0.08);
    link.attr('stroke', e => {
        const sid = e.source.id || e.source, tid = e.target.id || e.target;
        return (sid === d.id || tid === d.id) ? 'rgba(194,53,49,0.6)' : 'rgba(44,44,44,0.03)';
    }).attr('stroke-width', e => {
        const sid = e.source.id || e.source, tid = e.target.id || e.target;
        return (sid === d.id || tid === d.id) ? Math.max(1.5, e.weight * 0.8) : Math.max(0.3, e.weight * 0.3);
    });
    label.attr('opacity', n => connected.has(n.id) ? 1 : 0.08);
}
function resetHighlight() {
    node.attr('opacity', d => activePeriods.has(d.period) ? 0.85 : 0.05);
    link.attr('stroke', 'rgba(44,44,44,0.15)').attr('stroke-width', d => Math.max(0.5, d.weight * 0.5));
    label.attr('opacity', 1);
}

// ============ 时期过滤 ============
function applyFilter() {
    node.attr('opacity', d => activePeriods.has(d.period) ? 0.85 : 0.05)
        .attr('pointer-events', d => activePeriods.has(d.period) ? 'auto' : 'none');
    link.attr('opacity', d => {
        const sid = d.source.id || d.source, tid = d.target.id || d.target;
        const sn = nodeMap.get(sid), tn = nodeMap.get(tid);
        return (sn && activePeriods.has(sn.period) && tn && activePeriods.has(tn.period)) ? 1 : 0.03;
    });
    label.attr('opacity', d => activePeriods.has(d.period) ? 1 : 0.05);
    document.querySelectorAll('.legend-item').forEach(el =>
        el.classList.toggle('inactive', !activePeriods.has(el.dataset.period)));
}
document.querySelectorAll('.legend-item').forEach(el => {
    el.addEventListener('click', () => {
        const p = el.dataset.period;
        activePeriods.has(p) ? activePeriods.delete(p) : activePeriods.add(p);
        applyFilter();
    });
});

// ============ 全文搜索 ============
const searchInput = document.getElementById('searchInput');
const acEl = document.getElementById('autocomplete');
let acIndex = -1, searchTimer = null;

searchInput.addEventListener('input', function() {
    clearTimeout(searchTimer);
    const q = this.value.trim();
    if (!q) { acEl.style.display = 'none'; resetHighlight(); return; }
    searchTimer = setTimeout(() => doSearch(q), 150);
});

function doSearch(q) {
    const results = [];
    // 1. 搜索诗人名
    const poetMatches = DATA.nodes.filter(n => n.id.includes(q)).slice(0, 5);
    poetMatches.forEach(m => results.push({ type: 'poet', data: m }));

    // 2. 搜索诗题和诗句
    const poemMatches = [];
    for (let i = 0; i < poemIndex.length && poemMatches.length < 8; i++) {
        const p = poemIndex[i];
        if (p.title.includes(q) || p.text.includes(q)) {
            poemMatches.push(p);
        }
    }
    poemMatches.forEach(m => results.push({ type: 'poem', data: m }));

    if (results.length === 0) { acEl.style.display = 'none'; return; }
    acIndex = -1;
    renderAutocomplete(results, q);
    acEl.style.display = 'block';
}

function highlightText(text, q) {
    if (!q) return text;
    const idx = text.indexOf(q);
    if (idx === -1) return text;
    const start = Math.max(0, idx - 10);
    const end = Math.min(text.length, idx + q.length + 20);
    let snippet = (start > 0 ? '...' : '') + text.slice(start, end) + (end < text.length ? '...' : '');
    return snippet.replace(q, '<span class="ac-highlight">' + q + '</span>');
}

function renderAutocomplete(results, q) {
    let html = '';
    let poetSection = false, poemSection = false;
    results.forEach((r, i) => {
        if (r.type === 'poet' && !poetSection) { html += '<div class="ac-section">诗人</div>'; poetSection = true; }
        if (r.type === 'poem' && !poemSection) { html += '<div class="ac-section">诗作</div>'; poemSection = true; }

        if (r.type === 'poet') {
            const m = r.data;
            const color = PERIOD_COLORS[m.period] || '#999';
            html += '<div class="ac-item" data-idx="' + i + '" data-type="poet" data-name="' + m.id + '">' +
                '<div class="ac-left"><span class="ac-period-dot" style="background:' + color + '"></span>' +
                '<span class="ac-name">' + m.id + '</span>' +
                '<span class="ac-context">' + m.period + (m.place ? ' · ' + m.place : '') + '</span></div>' +
                '<span class="ac-right">' + (m.poemCount||0) + '首</span></div>';
        } else {
            const p = r.data;
            html += '<div class="ac-item ac-poem-match" data-idx="' + i + '" data-type="poem" data-poet="' + p.poet + '">' +
                '<div class="ac-left"><span class="ac-name">' + p.poet + '</span>' +
                '<span class="ac-context">《' + p.title + '》' + highlightText(p.text, q) + '</span></div></div>';
        }
    });
    acEl.innerHTML = html;

    acEl.querySelectorAll('.ac-item').forEach(item => {
        item.addEventListener('click', () => {
            if (item.dataset.type === 'poet') {
                searchAndFocus(item.dataset.name);
            } else {
                searchAndFocus(item.dataset.poet);
            }
            acEl.style.display = 'none';
        });
    });
}

searchInput.addEventListener('keydown', function(e) {
    const items = acEl.querySelectorAll('.ac-item');
    if (e.key === 'ArrowDown') { e.preventDefault(); acIndex = Math.min(acIndex + 1, items.length - 1); updateAcActive(items); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); acIndex = Math.max(acIndex - 1, 0); updateAcActive(items); }
    else if (e.key === 'Enter') {
        e.preventDefault();
        if (acIndex >= 0 && items[acIndex]) {
            const it = items[acIndex];
            searchAndFocus(it.dataset.type === 'poet' ? it.dataset.name : it.dataset.poet);
        } else {
            const q = this.value.trim();
            if (q) { const m = DATA.nodes.find(n => n.id === q) || DATA.nodes.find(n => n.id.includes(q)); if (m) searchAndFocus(m.id); }
        }
        acEl.style.display = 'none';
    }
    else if (e.key === 'Escape') { acEl.style.display = 'none'; this.blur(); }
});

function updateAcActive(items) {
    items.forEach((it, i) => it.classList.toggle('active', i === acIndex));
    if (items[acIndex]) items[acIndex].scrollIntoView({ block: 'nearest' });
}

document.addEventListener('click', e => {
    if (!e.target.closest('.search-wrap')) acEl.style.display = 'none';
});

// ============ 键盘快捷键 ============
document.addEventListener('keydown', e => {
    if (e.key === '/' && document.activeElement !== searchInput && !document.querySelector('.modal-overlay.show')) {
        e.preventDefault(); searchInput.focus();
    }
    if (e.key === 'Escape') {
        if (document.querySelector('.modal-overlay.show')) closeModal();
        else if (document.getElementById('onboarding').classList.contains('show')) closeOnboarding();
        else { document.getElementById('panelContent').style.display = 'none';
               document.getElementById('panelEmpty').style.display = 'flex'; resetHighlight(); }
    }
});

// ============ 搜索并聚焦 ============
function searchAndFocus(name) {
    searchInput.value = name;
    acEl.style.display = 'none';
    const match = nodeMap.get(name);
    if (match) {
        highlightNode(match); showNodeDetail(match);
        svg.transition().duration(750).call(zoom.transform,
            d3.zoomIdentity.translate(width/2, height/2).scale(2).translate(-match.x, -match.y));
        // 更新URL
        history.replaceState(null, '', '#' + encodeURIComponent(name));
    }
}

// ============ URL路由 ============
function handleHash() {
    const hash = decodeURIComponent(location.hash.slice(1));
    if (hash && nodeMap.has(hash)) {
        setTimeout(() => searchAndFocus(hash), 500);
    }
}
window.addEventListener('hashchange', handleHash);
handleHash();

// ============ 详情面板 ============
function getRelations(d) {
    const rels = [];
    edgesFiltered.forEach(e => {
        const sid = e.source.id || e.source, tid = e.target.id || e.target;
        if (sid === d.id) rels.push({ name: tid, dir: '赠诗给', weight: e.weight });
        if (tid === d.id) rels.push({ name: sid, dir: '收到赠诗', weight: e.weight });
    });
    rels.sort((a, b) => b.weight - a.weight);
    return rels;
}

function showNodeDetail(d) {
    const panel = document.getElementById('panelContent');
    document.getElementById('panelEmpty').style.display = 'none';
    panel.style.display = 'block';
    const periodColor = PERIOD_COLORS[d.period] || '#999';
    const rels = getRelations(d);
    const poems = d.poems || [];

    let html = '<div class="panel-title">' + d.id + '</div>';
    html += '<div class="panel-period" style="background:' + periodColor + '">' + d.period + '</div>';
    if (d.place) html += '<div style="color:#888;font-size:13px;margin-bottom:12px">\u{1F4CD} ' + d.place + '</div>';
    html += '<div class="panel-stats">';
    html += '<div class="panel-stat" onclick="showPoemsModal(\'' + d.id + '\')"><div class="panel-stat-num">' + (d.poemCount||0) + '</div><div class="panel-stat-label">诗作 \u{1F4D6}</div></div>';
    html += '<div class="panel-stat" onclick="showRelationsModal(\'' + d.id + '\',\'out\')"><div class="panel-stat-num">' + d.outDegree + '</div><div class="panel-stat-label">赠诗 \u{2709}</div></div>';
    html += '<div class="panel-stat" onclick="showRelationsModal(\'' + d.id + '\',\'in\')"><div class="panel-stat-num">' + d.inDegree + '</div><div class="panel-stat-label">被赠 \u{1F4E8}</div></div>';
    html += '</div>';

    if (poems.length > 0) {
        const showCount = Math.min(5, poems.length);
        html += '<div class="panel-section"><h3>代表诗作 ';
        if (poems.length > 5) html += '<span class="view-all" onclick="showPoemsModal(\'' + d.id + '\')">查看全部 ' + poems.length + ' 首 \u{2192}</span>';
        html += '</h3>';
        poems.slice(0, showCount).forEach(p => {
            html += '<div class="poem-card"><div class="poem-title">《' + p.title + '》</div>';
            html += '<div class="poem-text">' + p.text + '</div></div>';
        });
        html += '</div>';
    }

    if (rels.length > 0) {
        html += '<div class="panel-section"><h3>社交关系 (' + rels.length + ') ';
        if (rels.length > 15) html += '<span class="view-all" onclick="showRelationsModal(\'' + d.id + '\',\'all\')">查看全部 \u{2192}</span>';
        html += '</h3>';
        rels.slice(0, 15).forEach(r => {
            html += '<div class="relation-item" onclick="searchAndFocus(\'' + r.name + '\')">';
            html += '<b>' + r.name + '</b> — ' + r.dir + ' ' + r.weight + ' 次</div>';
        });
        html += '</div>';
    }
    panel.innerHTML = html;
    history.replaceState(null, '', '#' + encodeURIComponent(d.id));
}

function showEdgeDetail(d) {
    const panel = document.getElementById('panelContent');
    document.getElementById('panelEmpty').style.display = 'none';
    panel.style.display = 'block';
    const src = d.source.id || d.source, tgt = d.target.id || d.target;
    const srcNode = nodeMap.get(src), tgtNode = nodeMap.get(tgt);

    let html = '<div class="panel-title">' + src + ' \u{2194} ' + tgt + '</div>';
    html += '<div style="color:#888;font-size:13px;margin-bottom:16px">赠诗 ' + d.weight + ' 次</div>';
    [['src', src, srcNode], ['tgt', tgt, tgtNode]].forEach(([key, name, nd]) => {
        const poems = (nd?.poems || []).slice(0, 5);
        html += '<div class="panel-section"><h3>' + name + ' 的诗作</h3>';
        if (poems.length > 0) { poems.forEach(p => {
            html += '<div class="poem-card"><div class="poem-title">《' + p.title + '》</div>';
            html += '<div class="poem-text">' + p.text + '</div></div>';
        }); } else { html += '<div style="color:#999">暂无诗作数据</div>'; }
        html += '</div>';
    });
    panel.innerHTML = html;
}

// ============ 弹窗 ============
let modalData = [], modalType = '';

function showModal(title, data, type) {
    modalData = data; modalType = type;
    document.getElementById('modalTitle').textContent = title;
    renderModalItems(data);
    document.getElementById('modalOverlay').classList.add('show');
    document.getElementById('modalSearch').value = '';
    setTimeout(() => document.getElementById('modalSearch').focus(), 100);
}
function closeModal() { document.getElementById('modalOverlay').classList.remove('show'); }

function renderModalItems(items) {
    const body = document.getElementById('modalBody');
    if (items.length === 0) { body.innerHTML = '<div class="modal-empty">暂无数据</div>'; return; }
    body.innerHTML = items.map(item => {
        if (modalType === 'poems') {
            return '<div class="poem-card"><div class="poem-title">《' + item.title + '》</div>' +
                '<div class="poem-text">' + item.text + '</div></div>';
        } else {
            return '<div class="modal-item" onclick="closeModal();searchAndFocus(\'' + item.name + '\')">' +
                '<b>' + item.name + '</b> — ' + item.dir + ' ' + item.weight + ' 次</div>';
        }
    }).join('');
}

document.getElementById('modalSearch').addEventListener('input', function() {
    const q = this.value.trim();
    if (!q) { renderModalItems(modalData); return; }
    renderModalItems(modalData.filter(item =>
        modalType === 'poems' ? (item.title.includes(q) || item.text.includes(q)) : item.name.includes(q)
    ));
});

document.getElementById('modalOverlay').addEventListener('click', e => {
    if (e.target === document.getElementById('modalOverlay')) closeModal();
});

function showPoemsModal(name) {
    const d = nodeMap.get(name); if (!d) return;
    showModal(name + ' 的诗作 (' + (d.poemCount||0) + '首)', d.poems || [], 'poems');
}
function showRelationsModal(name, dir) {
    const d = nodeMap.get(name); if (!d) return;
    const rels = getRelations(d);
    let filtered = rels, title = name + ' 的社交关系';
    if (dir === 'out') { filtered = rels.filter(r => r.dir === '赠诗给'); title = name + ' 赠诗给...'; }
    if (dir === 'in') { filtered = rels.filter(r => r.dir === '收到赠诗'); title = '赠诗给 ' + name + ' 的人...'; }
    showModal(title + ' (' + filtered.length + '人)', filtered, 'relations');
}

// ============ 引导 ============
function closeOnboarding() { document.getElementById('onboarding').classList.remove('show'); localStorage.setItem('tpn_visited', '1'); }
if (!localStorage.getItem('tpn_visited')) setTimeout(() => document.getElementById('onboarding').classList.add('show'), 500);

// ============ 自适应 ============
window.addEventListener('resize', () => {
    const w = container.clientWidth, h = container.clientHeight;
    svg.attr('width', w).attr('height', h);
    simulation.force('center', d3.forceCenter(w / 2, h / 2));
    simulation.alpha(0.1).restart();
});
"""

if __name__ == '__main__':
    build()
