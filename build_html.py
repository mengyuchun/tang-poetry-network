"""
唐诗社交网络 — 构建单文件 HTML
将数据和代码合并为一个零依赖的 HTML 文件
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
    html += '<style>\n'
    html += CSS
    html += '\n</style>\n</head>\n<body>\n'
    html += HEADER_HTML.format(
        total_poets=stats['total_poets'],
        total_edges=stats['total_edges'],
        total_poems=stats['total_poems'],
        matched_poets=stats['matched_poets']
    )
    html += '\n<script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script>\n'
    html += '<script>\n'
    html += 'const DATA = ' + data_json + ';\n'
    html += 'const PERIOD_COLORS = ' + colors_json + ';\n'
    html += JS
    html += '\n</script>\n</body>\n</html>'

    output_path = os.path.join(DIST_DIR, 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"已生成: {output_path} ({size_mb:.1f} MB)")


CSS = """
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
.header {
    position: fixed; top: 0; left: 0; right: 0; height: 56px;
    background: rgba(44,44,44,0.92); display: flex; align-items: center;
    justify-content: space-between; padding: 0 24px; z-index: 100;
    backdrop-filter: blur(8px);
}
.header h1 { color: #f5f0e8; font-size: 20px; font-weight: 400; letter-spacing: 4px; }
.search-box { display: flex; align-items: center; gap: 8px; }
.search-box input {
    width: 240px; padding: 6px 12px; border: 1px solid rgba(245,240,232,0.3);
    border-radius: 4px; background: rgba(245,240,232,0.1); color: #f5f0e8;
    font-family: inherit; font-size: 14px; outline: none;
}
.search-box input::placeholder { color: rgba(245,240,232,0.5); }
.search-box input:focus { border-color: #c23531; }
.legend { display: flex; gap: 16px; align-items: center; }
.legend-item { display: flex; align-items: center; gap: 4px; color: #f5f0e8; font-size: 13px; }
.legend-dot { width: 10px; height: 10px; border-radius: 50%; }
.stats-bar {
    position: fixed; bottom: 0; left: 0; right: 0; height: 36px;
    background: rgba(44,44,44,0.85); display: flex; align-items: center;
    justify-content: center; gap: 32px; color: rgba(245,240,232,0.8);
    font-size: 13px; z-index: 100; backdrop-filter: blur(8px);
}
.stats-bar span { letter-spacing: 1px; }
#graph { position: fixed; top: 56px; left: 0; right: 360px; bottom: 36px; z-index: 1; }
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
.panel-stat { text-align: center; padding: 8px; background: rgba(44,44,44,0.05); border-radius: 4px; }
.panel-stat-num { font-size: 20px; color: #c23531; font-weight: bold; }
.panel-stat-label { font-size: 12px; color: #888; }
.panel-section { margin-bottom: 16px; }
.panel-section h3 { font-size: 15px; color: #2c2c2c; border-bottom: 1px solid rgba(44,44,44,0.15); padding-bottom: 6px; margin-bottom: 10px; }
.poem-card { background: rgba(255,255,255,0.6); border: 1px solid rgba(44,44,44,0.1); border-radius: 4px; padding: 12px; margin-bottom: 8px; }
.poem-title { font-size: 14px; font-weight: bold; color: #2c2c2c; margin-bottom: 6px; }
.poem-text { font-size: 13px; color: #555; line-height: 1.8; white-space: pre-line; }
.relation-item { padding: 6px 0; border-bottom: 1px solid rgba(44,44,44,0.08); font-size: 13px; color: #555; cursor: pointer; }
.relation-item:hover { color: #c23531; }
.relation-item b { color: #2c2c2c; }
.tooltip {
    position: absolute; background: rgba(44,44,44,0.9); color: #f5f0e8;
    padding: 6px 12px; border-radius: 4px; font-size: 13px; pointer-events: none;
    z-index: 200; white-space: nowrap; backdrop-filter: blur(4px);
}
"""

HEADER_HTML = """
<div class="header">
    <h1>唐 诗 社 交 网 络</h1>
    <div class="search-box">
        <input type="text" id="searchInput" placeholder="搜索诗人...">
    </div>
    <div class="legend">
        <div class="legend-item"><div class="legend-dot" style="background:#61a0a8"></div>初唐</div>
        <div class="legend-item"><div class="legend-dot" style="background:#c23531"></div>盛唐</div>
        <div class="legend-item"><div class="legend-dot" style="background:#2f4554"></div>中唐</div>
        <div class="legend-item"><div class="legend-dot" style="background:#d48265"></div>晚唐</div>
        <div class="legend-item"><div class="legend-dot" style="background:#999"></div>未知</div>
    </div>
</div>
<div id="graph"></div>
<div class="panel" id="panel">
    <div class="panel-empty" id="panelEmpty">点击节点探索诗人<br>点击连线查看关系</div>
    <div id="panelContent" style="display:none"></div>
</div>
<div class="stats-bar">
    <span>{total_poets} 位诗人</span>
    <span>{total_edges} 条赠诗关系</span>
    <span>{total_poems} 首唐诗</span>
    <span>{matched_poets} 位诗人有作品</span>
</div>
<div class="tooltip" id="tooltip" style="display:none"></div>
"""

JS = r"""
// 初始化 SVG
const container = document.getElementById('graph');
const width = container.clientWidth;
const height = container.clientHeight;

const svg = d3.select('#graph').append('svg').attr('width', width).attr('height', height);

// 缩放
const g = svg.append('g');
const zoom = d3.zoom().scaleExtent([0.1, 8])
    .on('zoom', (e) => g.attr('transform', e.transform));
svg.call(zoom);

// 数据处理
const nodeMap = new Map(DATA.nodes.map(n => [n.id, n]));
const edgesFiltered = DATA.edges.filter(e => nodeMap.has(e.source) && nodeMap.has(e.target));

// 力导向模拟
function getNodeRadius(d) { return Math.max(3, Math.min(25, 3 + Math.sqrt(d.poemCount || 1) * 1.5)); }

const simulation = d3.forceSimulation(DATA.nodes)
    .force('link', d3.forceLink(edgesFiltered).id(d => d.id).distance(80))
    .force('charge', d3.forceManyBody().strength(-120))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('collision', d3.forceCollide().radius(d => getNodeRadius(d) + 2));

// 边
const link = g.append('g').selectAll('line').data(edgesFiltered).join('line')
    .attr('stroke', 'rgba(44,44,44,0.2)')
    .attr('stroke-width', d => Math.max(0.5, Math.min(3, d.weight * 0.5)))
    .on('click', (e, d) => showEdgeDetail(d))
    .on('mouseover', (e, d) => showTooltip(e, (d.source.id||d.source) + ' → ' + (d.target.id||d.target)))
    .on('mouseout', hideTooltip);

// 节点
const node = g.append('g').selectAll('circle').data(DATA.nodes).join('circle')
    .attr('r', d => getNodeRadius(d))
    .attr('fill', d => PERIOD_COLORS[d.period] || '#999')
    .attr('stroke', '#f5f0e8').attr('stroke-width', 1).attr('opacity', 0.85)
    .style('cursor', 'pointer')
    .call(d3.drag().on('start', dragStart).on('drag', dragging).on('end', dragEnd))
    .on('click', (e, d) => showNodeDetail(d))
    .on('mouseover', (e, d) => { showTooltip(e, d.id + ' (' + (d.poemCount||0) + '首)'); highlightNode(d); })
    .on('mouseout', () => { hideTooltip(); resetHighlight(); });

// 节点标签
const labelThreshold = 5;
const label = g.append('g').selectAll('text')
    .data(DATA.nodes.filter(d => d.totalDegree >= labelThreshold)).join('text')
    .text(d => d.id)
    .attr('font-size', d => d.totalDegree >= 15 ? 12 : 10)
    .attr('fill', '#2c2c2c').attr('text-anchor', 'middle')
    .attr('dy', d => -getNodeRadius(d) - 4)
    .style('pointer-events', 'none')
    .style('font-family', "'STKaiti', 'KaiTi', serif");

simulation.on('tick', () => {
    link.attr('x1', d => d.source.x).attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x).attr('y2', d => d.target.y);
    node.attr('cx', d => d.x).attr('cy', d => d.y);
    label.attr('x', d => d.x).attr('y', d => d.y);
});

// 拖拽
function dragStart(e, d) { if (!e.active) simulation.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; }
function dragging(e, d) { d.fx = e.x; d.fy = e.y; }
function dragEnd(e, d) { if (!e.active) simulation.alphaTarget(0); d.fx = null; d.fy = null; }

// Tooltip
const tooltip = document.getElementById('tooltip');
function showTooltip(e, text) {
    tooltip.textContent = text; tooltip.style.display = 'block';
    tooltip.style.left = (e.pageX + 12) + 'px'; tooltip.style.top = (e.pageY - 8) + 'px';
}
function hideTooltip() { tooltip.style.display = 'none'; }

// 高亮
let highlightedNode = null;
function highlightNode(d) {
    highlightedNode = d;
    const connected = new Set(); connected.add(d.id);
    edgesFiltered.forEach(e => {
        const sid = e.source.id || e.source, tid = e.target.id || e.target;
        if (sid === d.id) connected.add(tid); if (tid === d.id) connected.add(sid);
    });
    node.attr('opacity', n => connected.has(n.id) ? 1 : 0.1);
    link.attr('stroke', e => {
        const sid = e.source.id || e.source, tid = e.target.id || e.target;
        return (sid === d.id || tid === d.id) ? 'rgba(194,53,49,0.6)' : 'rgba(44,44,44,0.05)';
    });
    label.attr('opacity', n => connected.has(n.id) ? 1 : 0.1);
}
function resetHighlight() {
    highlightedNode = null; node.attr('opacity', 0.85);
    link.attr('stroke', 'rgba(44,44,44,0.2)'); label.attr('opacity', 1);
}

// 搜索
document.getElementById('searchInput').addEventListener('input', function() {
    const q = this.value.trim();
    if (!q) { resetHighlight(); return; }
    const match = DATA.nodes.find(n => n.id === q) || DATA.nodes.find(n => n.id.includes(q));
    if (match) {
        highlightNode(match);
        svg.transition().duration(750).call(zoom.transform,
            d3.zoomIdentity.translate(width/2, height/2).scale(2).translate(-match.x, -match.y));
    }
});

// 详情面板
function showNodeDetail(d) {
    const panel = document.getElementById('panelContent');
    document.getElementById('panelEmpty').style.display = 'none';
    panel.style.display = 'block';
    const periodColor = PERIOD_COLORS[d.period] || '#999';

    // 关联的诗人
    const relations = [];
    edgesFiltered.forEach(e => {
        const sid = e.source.id || e.source, tid = e.target.id || e.target;
        if (sid === d.id) relations.push({ name: tid, dir: '赠诗给', weight: e.weight });
        if (tid === d.id) relations.push({ name: sid, dir: '收到赠诗', weight: e.weight });
    });
    relations.sort((a, b) => b.weight - a.weight);

    let html = '<div class="panel-title">' + d.id + '</div>';
    html += '<div class="panel-period" style="background:' + periodColor + '">' + d.period + '</div>';
    if (d.place) html += '<div style="color:#888;font-size:13px;margin-bottom:12px">📍 ' + d.place + '</div>';
    html += '<div class="panel-stats">';
    html += '<div class="panel-stat"><div class="panel-stat-num">' + (d.poemCount||0) + '</div><div class="panel-stat-label">诗作</div></div>';
    html += '<div class="panel-stat"><div class="panel-stat-num">' + d.outDegree + '</div><div class="panel-stat-label">赠诗</div></div>';
    html += '<div class="panel-stat"><div class="panel-stat-num">' + d.inDegree + '</div><div class="panel-stat-label">被赠</div></div>';
    html += '</div>';

    if (d.poems && d.poems.length > 0) {
        html += '<div class="panel-section"><h3>代表诗作</h3>';
        d.poems.forEach(p => {
            html += '<div class="poem-card"><div class="poem-title">《' + p.title + '》</div>';
            html += '<div class="poem-text">' + p.text + '</div></div>';
        });
        html += '</div>';
    }

    if (relations.length > 0) {
        html += '<div class="panel-section"><h3>社交关系 (' + relations.length + ')</h3>';
        relations.slice(0, 20).forEach(r => {
            html += '<div class="relation-item" onclick="searchAndFocus(\'' + r.name + '\')">';
            html += '<b>' + r.name + '</b> — ' + r.dir + ' ' + r.weight + ' 次</div>';
        });
        html += '</div>';
    }
    panel.innerHTML = html;
}

function showEdgeDetail(d) {
    const panel = document.getElementById('panelContent');
    document.getElementById('panelEmpty').style.display = 'none';
    panel.style.display = 'block';
    const src = d.source.id || d.source, tgt = d.target.id || d.target;
    const srcNode = nodeMap.get(src), tgtNode = nodeMap.get(tgt);
    const srcPoems = (srcNode?.poems || []).slice(0, 3);
    const tgtPoems = (tgtNode?.poems || []).slice(0, 3);

    let html = '<div class="panel-title">' + src + ' ↔ ' + tgt + '</div>';
    html += '<div style="color:#888;font-size:13px;margin-bottom:16px">赠诗 ' + d.weight + ' 次</div>';
    html += '<div class="panel-section"><h3>' + src + ' 的诗作</h3>';
    if (srcPoems.length > 0) { srcPoems.forEach(p => {
        html += '<div class="poem-card"><div class="poem-title">《' + p.title + '》</div>';
        html += '<div class="poem-text">' + p.text + '</div></div>';
    }); } else { html += '<div style="color:#999">暂无诗作数据</div>'; }
    html += '</div>';
    html += '<div class="panel-section"><h3>' + tgt + ' 的诗作</h3>';
    if (tgtPoems.length > 0) { tgtPoems.forEach(p => {
        html += '<div class="poem-card"><div class="poem-title">《' + p.title + '》</div>';
        html += '<div class="poem-text">' + p.text + '</div></div>';
    }); } else { html += '<div style="color:#999">暂无诗作数据</div>'; }
    html += '</div>';
    panel.innerHTML = html;
}

function searchAndFocus(name) {
    document.getElementById('searchInput').value = name;
    const match = DATA.nodes.find(n => n.id === name);
    if (match) {
        highlightNode(match); showNodeDetail(match);
        svg.transition().duration(750).call(zoom.transform,
            d3.zoomIdentity.translate(width/2, height/2).scale(2).translate(-match.x, -match.y));
    }
}

// 自适应窗口
window.addEventListener('resize', () => {
    const w = container.clientWidth, h = container.clientHeight;
    svg.attr('width', w).attr('height', h);
    simulation.force('center', d3.forceCenter(w / 2, h / 2));
    simulation.alpha(0.1).restart();
});
"""

if __name__ == '__main__':
    build()
