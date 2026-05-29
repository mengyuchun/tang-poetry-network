"""
唐诗社交网络 — 构建单文件 HTML（v5 全功能版）
深色模式 · 节点脉冲 · 截图分享 · 每日一诗 · 面板动画 · 全部功能
"""
import json, os

DIST_DIR = os.path.join(os.path.dirname(__file__), 'dist')

def build():
    with open(os.path.join(DIST_DIR, 'data.json'), 'r', encoding='utf-8') as f:
        data = json.load(f)
    nodes, edges, stats = data['nodes'], data['edges'], data['stats']
    period_dist = data.get('periodDist', {})
    top_poets = data.get('topPoets', [])
    timeline = data.get('timeline', [])
    network_stats = data.get('networkStats', {})
    period_colors = {'初唐':'#61a0a8','盛唐':'#c23531','中唐':'#2f4554','晚唐':'#d48265','未知':'#999'}

    data_json = json.dumps({'nodes':nodes,'edges':edges}, ensure_ascii=False)
    colors_json = json.dumps(period_colors, ensure_ascii=False)
    stats_json = json.dumps({'periodDist':period_dist,'topPoets':top_poets,'timeline':timeline,'networkStats':network_stats}, ensure_ascii=False)

    html = '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n'
    html += '<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width,initial-scale=1.0">\n'
    html += '<title>唐诗社交网络</title>\n'
    html += '<meta name="description" content="1,381位诗人 · 8,259条赠诗关系 · 57,607首唐诗 · 交互式探索">\n'
    html += '<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🏮</text></svg>">\n'
    html += '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.css">\n'
    html += '<style>\n' + CSS + '\n</style>\n</head>\n<body>\n'
    html += LOADING_HTML
    html += HEADER_HTML.format(total_poets=stats['total_poets'],total_edges=stats['total_edges'],total_poems=stats['total_poems'],matched_poets=stats['matched_poets'])
    html += '\n<script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script>\n'
    html += '<script src="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.js"></script>\n'
    html += '<script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>\n'
    html += '<script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>\n'
    html += '<script>\nconst DATA=' + data_json + ';\nconst PERIOD_COLORS=' + colors_json + ';\nconst STATS=' + stats_json + ';\n'
    html += JS + '\n</script>\n</body>\n</html>'
    output_path = os.path.join(DIST_DIR, 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"已生成: {output_path} ({os.path.getsize(output_path)/1024/1024:.1f} MB)")


CSS = r"""
:root { --bg:#f5f0e8; --bg2:rgba(245,240,232,0.95); --text:#2c2c2c; --text2:#555; --text3:#888; --accent:#c23531; --border:rgba(44,44,44,0.15); --card:rgba(255,255,255,0.6); --header:rgba(44,44,44,0.92); --headerText:#f5f0e8; --shadow:rgba(0,0,0,0.1); }
body.dark { --bg:#1a1a2e; --bg2:rgba(26,26,46,0.95); --text:#e0d8c8; --text2:#b0a898; --text3:#787068; --accent:#e74c3c; --border:rgba(224,216,200,0.15); --card:rgba(40,40,60,0.6); --header:rgba(20,20,35,0.95); --headerText:#e0d8c8; --shadow:rgba(0,0,0,0.3); }
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:'STKaiti','KaiTi','Noto Serif SC','SimSun',serif; background:var(--bg); color:var(--text); overflow:hidden; height:100vh; transition:background 0.3s,color 0.3s; }
body::before { content:''; position:fixed; top:0; left:0; right:0; bottom:0; background: radial-gradient(ellipse at 20% 50%,rgba(200,180,150,0.12) 0%,transparent 50%), radial-gradient(ellipse at 80% 20%,rgba(180,160,130,0.08) 0%,transparent 50%), radial-gradient(ellipse at 50% 80%,rgba(190,170,140,0.08) 0%,transparent 50%); pointer-events:none; z-index:0; }
body.dark::before { background: radial-gradient(ellipse at 20% 50%,rgba(100,80,120,0.1) 0%,transparent 50%), radial-gradient(ellipse at 80% 20%,rgba(80,60,100,0.08) 0%,transparent 50%); }
.loading { position:fixed; top:0; left:0; right:0; bottom:0; background:var(--bg); z-index:9999; display:flex; flex-direction:column; align-items:center; justify-content:center; transition:opacity 0.5s; }
.loading.hide { opacity:0; pointer-events:none; }
.loading-text { font-size:18px; color:var(--text); letter-spacing:4px; margin-top:20px; }
.loading-sub { font-size:13px; color:var(--text3); margin-top:8px; }
.spinner { width:40px; height:40px; border:3px solid var(--border); border-top-color:var(--accent); border-radius:50%; animation:spin 0.8s linear infinite; }
@keyframes spin { to { transform:rotate(360deg); } }
.header { position:fixed; top:0; left:0; right:0; height:56px; background:var(--header); display:flex; align-items:center; justify-content:space-between; padding:0 20px; z-index:100; backdrop-filter:blur(8px); }
.header h1 { color:var(--headerText); font-size:18px; font-weight:400; letter-spacing:3px; white-space:nowrap; }
.header-center { display:flex; align-items:center; gap:12px; }
.header-right { display:flex; align-items:center; gap:10px; }
.search-wrap { position:relative; }
.search-box input { width:260px; padding:6px 10px; border:1px solid rgba(245,240,232,0.25); border-radius:4px; background:rgba(245,240,232,0.08); color:var(--headerText); font-family:inherit; font-size:13px; outline:none; transition:all 0.2s; }
.search-box input::placeholder { color:rgba(245,240,232,0.4); }
.search-box input:focus { border-color:var(--accent); background:rgba(245,240,232,0.12); }
.autocomplete { position:absolute; top:100%; left:0; width:380px; max-height:400px; overflow-y:auto; background:var(--header); border-radius:0 0 4px 4px; display:none; z-index:200; }
.ac-section { padding:4px 12px; font-size:10px; color:rgba(245,240,232,0.35); text-transform:uppercase; letter-spacing:1px; border-bottom:1px solid rgba(245,240,232,0.08); }
.ac-item { padding:7px 12px; color:var(--headerText); font-size:12px; cursor:pointer; display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(245,240,232,0.04); }
.ac-item:hover, .ac-item.active { background:rgba(194,53,49,0.3); }
.ac-item .ac-left { display:flex; align-items:center; gap:6px; flex:1; min-width:0; }
.ac-item .ac-pd { width:7px; height:7px; border-radius:50%; flex-shrink:0; }
.ac-item .ac-name { font-weight:bold; white-space:nowrap; }
.ac-item .ac-ctx { font-size:10px; color:rgba(245,240,232,0.5); overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.ac-item .ac-right { font-size:10px; color:rgba(245,240,232,0.4); white-space:nowrap; margin-left:8px; }
.ac-highlight { color:var(--accent); font-weight:bold; }
.quick-nav { display:flex; gap:4px; }
.quick-btn { padding:3px 7px; background:rgba(245,240,232,0.08); border:1px solid rgba(245,240,232,0.15); border-radius:3px; color:var(--headerText); font-size:11px; cursor:pointer; font-family:inherit; transition:all 0.2s; }
.quick-btn:hover { background:rgba(194,53,49,0.35); border-color:var(--accent); }
.fun-btn { padding:3px 9px; background:rgba(194,53,49,0.25); border:1px solid rgba(194,53,49,0.4); border-radius:3px; color:var(--headerText); font-size:11px; cursor:pointer; font-family:inherit; transition:all 0.2s; }
.fun-btn:hover { background:rgba(194,53,49,0.5); }
.icon-btn { padding:4px 10px; background:rgba(245,240,232,0.08); border:1px solid rgba(245,240,232,0.15); border-radius:4px; color:var(--headerText); font-size:11px; cursor:pointer; font-family:inherit; display:flex; align-items:center; gap:3px; transition:all 0.2s; white-space:nowrap; }
.icon-btn:hover { background:rgba(245,240,232,0.15); }
.tabs { display:flex; gap:2px; }
.tab { padding:5px 14px; background:rgba(245,240,232,0.08); border:none; color:rgba(245,240,232,0.5); font-size:12px; cursor:pointer; font-family:inherit; border-radius:4px 4px 0 0; transition:all 0.2s; }
.tab:hover { color:var(--headerText); background:rgba(245,240,232,0.12); }
.tab.active { color:var(--headerText); background:rgba(194,53,49,0.55); }
.legend { display:flex; gap:8px; align-items:center; }
.legend-item { display:flex; align-items:center; gap:3px; color:var(--headerText); font-size:11px; cursor:pointer; padding:2px 5px; border-radius:3px; transition:all 0.2s; user-select:none; }
.legend-item:hover { background:rgba(245,240,232,0.08); }
.legend-item.inactive { opacity:0.3; }
.legend-dot { width:8px; height:8px; border-radius:50%; }
.stats-bar { position:fixed; bottom:0; left:0; right:0; height:32px; background:var(--header); display:flex; align-items:center; justify-content:center; gap:28px; color:rgba(245,240,232,0.7); font-size:12px; z-index:100; }
.view { position:fixed; top:56px; left:0; right:360px; bottom:32px; z-index:1; display:none; }
.view.active { display:block; }
#graph { z-index:1; }
#statsView { overflow-y:auto; padding:20px; background:var(--bg); }
.legend-help { position:fixed; bottom:32px; left:0; right:360px; height:26px; background:var(--bg2); display:flex; align-items:center; justify-content:center; gap:20px; font-size:10px; color:var(--text3); z-index:99; border-top:1px solid var(--border); }
.panel { position:fixed; top:56px; right:0; bottom:32px; width:360px; background:var(--bg2); border-left:1px solid var(--border); overflow-y:auto; z-index:50; padding:20px; transform:translateX(0); transition:transform 0.3s ease; }
.panel.hidden { transform:translateX(100%); }
.panel-close { position:absolute; top:10px; right:10px; width:26px; height:26px; border:none; background:var(--border); color:var(--text3); font-size:15px; cursor:pointer; border-radius:4px; display:flex; align-items:center; justify-content:center; z-index:10; transition:all 0.2s; }
.panel-close:hover { background:var(--accent); color:#fff; }
.panel-toggle { position:fixed; top:70px; right:360px; width:24px; height:48px; background:var(--bg2); border:1px solid var(--border); border-right:none; border-radius:4px 0 0 4px; cursor:pointer; z-index:51; display:flex; align-items:center; justify-content:center; font-size:12px; color:var(--text3); transition:all 0.3s; }
.panel-toggle:hover { color:var(--accent); }
.panel.hidden + .panel-toggle { right:0; }
.panel-empty { display:flex; align-items:center; justify-content:center; height:100%; color:var(--text3); font-size:14px; text-align:center; line-height:2; }
.panel-title { font-size:22px; color:var(--text); margin-bottom:6px; letter-spacing:2px; }
.panel-period { display:inline-block; padding:2px 10px; border-radius:3px; font-size:12px; color:#fff; margin-bottom:10px; }
.panel-stats { display:grid; grid-template-columns:1fr 1fr 1fr; gap:6px; margin-bottom:14px; }
.panel-stat { text-align:center; padding:6px; background:var(--border); border-radius:4px; cursor:pointer; transition:all 0.2s; }
.panel-stat:hover { background:rgba(194,53,49,0.15); transform:scale(1.03); }
.panel-stat-num { font-size:18px; color:var(--accent); font-weight:bold; }
.panel-stat-label { font-size:11px; color:var(--text3); }
.panel-section { margin-bottom:14px; }
.panel-section h3 { font-size:14px; color:var(--text); border-bottom:1px solid var(--border); padding-bottom:5px; margin-bottom:8px; }
.view-all { font-size:10px; color:var(--accent); cursor:pointer; font-weight:normal; }
.view-all:hover { text-decoration:underline; }
.poem-card { background:var(--card); border:1px solid var(--border); border-radius:4px; padding:10px; margin-bottom:6px; }
.poem-title { font-size:13px; font-weight:bold; color:var(--text); margin-bottom:4px; }
.poem-text { font-size:12px; color:var(--text2); line-height:1.8; white-space:pre-line; }
.relation-item { padding:5px 0; border-bottom:1px solid var(--border); font-size:12px; color:var(--text2); cursor:pointer; }
.relation-item:hover { color:var(--accent); }
.relation-item b { color:var(--text); }
.path-finder { background:var(--border); border-radius:8px; padding:14px; margin-bottom:16px; }
.path-finder h3 { font-size:14px; margin-bottom:10px; color:var(--text); }
.path-inputs { display:flex; gap:6px; align-items:center; margin-bottom:10px; position:relative; }
.path-input-wrap { flex:1; position:relative; }
.path-input-wrap input { width:100%; padding:5px 8px; border:1px solid var(--border); border-radius:4px; font-family:inherit; font-size:12px; outline:none; background:var(--card); color:var(--text); }
.path-input-wrap input:focus { border-color:var(--accent); }
.path-ac { position:absolute; top:100%; left:0; width:100%; max-height:180px; overflow-y:auto; background:var(--header); border-radius:0 0 4px 4px; display:none; z-index:210; }
.path-ac-item { padding:5px 8px; color:var(--headerText); font-size:11px; cursor:pointer; display:flex; justify-content:space-between; }
.path-ac-item:hover, .path-ac-item.active { background:rgba(194,53,49,0.3); }
.path-ac-item .ac-pd { width:6px; height:6px; border-radius:50%; margin-right:5px; display:inline-block; }
.path-inputs .path-sep { color:var(--text3); font-size:12px; flex-shrink:0; }
.path-btn { padding:5px 14px; background:var(--accent); color:#fff; border:none; border-radius:4px; font-size:12px; cursor:pointer; font-family:inherit; }
.path-btn:hover { opacity:0.85; }
.path-result { margin-top:10px; }
.path-step { display:flex; align-items:center; gap:6px; padding:4px 0; font-size:12px; }
.path-node { color:var(--accent); font-weight:bold; cursor:pointer; }
.path-node:hover { text-decoration:underline; }
.path-arrow { color:var(--text3); }
.path-examples { font-size:10px; color:var(--text3); margin-top:6px; }
.path-examples span { color:var(--accent); cursor:pointer; }
.path-examples span:hover { text-decoration:underline; }
.stats-grid { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
.stats-card { background:var(--card); border:1px solid var(--border); border-radius:8px; padding:14px; }
.stats-card h3 { font-size:14px; color:var(--text); margin-bottom:10px; border-bottom:1px solid var(--border); padding-bottom:6px; }
.stats-card canvas { max-height:280px; }
.stats-summary { display:grid; grid-template-columns:repeat(4,1fr); gap:10px; margin-bottom:16px; }
.stats-summary-item { text-align:center; padding:12px; background:var(--card); border:1px solid var(--border); border-radius:8px; }
.stats-summary-num { font-size:24px; color:var(--accent); font-weight:bold; }
.stats-summary-label { font-size:11px; color:var(--text3); margin-top:3px; }
.modal-overlay { position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.5); z-index:500; display:none; align-items:center; justify-content:center; backdrop-filter:blur(4px); }
.modal-overlay.show { display:flex; }
.modal { background:var(--bg); border-radius:8px; width:90%; max-width:700px; max-height:80vh; display:flex; flex-direction:column; box-shadow:0 20px 60px rgba(0,0,0,0.3); }
.modal-header { padding:14px 18px; border-bottom:1px solid var(--border); display:flex; justify-content:space-between; align-items:center; }
.modal-header h2 { font-size:16px; color:var(--text); }
.modal-close { width:28px; height:28px; border:none; background:none; font-size:18px; color:var(--text3); cursor:pointer; border-radius:4px; display:flex; align-items:center; justify-content:center; }
.modal-close:hover { background:var(--border); color:var(--text); }
.modal-search { padding:6px 18px; border-bottom:1px solid var(--border); }
.modal-search input { width:100%; padding:5px 8px; border:1px solid var(--border); border-radius:4px; font-family:inherit; font-size:12px; outline:none; background:var(--card); color:var(--text); }
.modal-body { padding:10px 18px; overflow-y:auto; flex:1; }
.modal-item { padding:6px 0; border-bottom:1px solid var(--border); font-size:12px; color:var(--text2); cursor:pointer; }
.modal-item:hover { color:var(--accent); }
.modal-item b { color:var(--text); }
.modal-empty { color:var(--text3); text-align:center; padding:16px; }
.onboarding { position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.45); z-index:300; display:none; align-items:center; justify-content:center; backdrop-filter:blur(2px); }
.onboarding.show { display:flex; }
.onboarding-card { background:var(--bg2); border-radius:12px; padding:28px 36px; text-align:center; max-width:400px; box-shadow:0 20px 60px rgba(0,0,0,0.3); }
.onboarding-card h2 { font-size:20px; color:var(--text); margin-bottom:10px; letter-spacing:2px; }
.onboarding-card p { font-size:13px; color:var(--text2); line-height:1.8; margin-bottom:16px; }
.onboarding-card .hint { font-size:12px; color:var(--accent); margin-bottom:14px; }
.onboarding-btn { padding:7px 22px; background:var(--accent); color:#fff; border:none; border-radius:4px; font-size:13px; cursor:pointer; font-family:inherit; }
.onboarding-btn:hover { opacity:0.85; }
.tooltip { position:absolute; background:var(--header); color:var(--headerText); padding:5px 10px; border-radius:4px; font-size:12px; pointer-events:none; z-index:200; white-space:nowrap; }
.leaflet-container { background:var(--bg) !important; }
/* 地图时间线 */
.map-timeline { position:absolute; bottom:40px; left:50%; transform:translateX(-50%); z-index:1000; background:var(--bg2); border:1px solid var(--border); border-radius:8px; padding:12px 20px; display:flex; align-items:center; gap:12px; box-shadow:0 4px 20px var(--shadow); min-width:500px; }
.map-timeline label { font-size:12px; color:var(--text); white-space:nowrap; }
.map-timeline input[type=range] { flex:1; height:4px; -webkit-appearance:none; background:var(--border); border-radius:2px; outline:none; }
.map-timeline input[type=range]::-webkit-slider-thumb { -webkit-appearance:none; width:16px; height:16px; background:var(--accent); border-radius:50%; cursor:pointer; }
.map-timeline .year-display { font-size:20px; font-weight:bold; color:var(--accent); min-width:60px; text-align:center; }
.map-timeline .period-display { font-size:11px; color:var(--text3); }
.map-timeline button { padding:3px 10px; background:var(--accent); color:#fff; border:none; border-radius:3px; font-size:11px; cursor:pointer; font-family:inherit; }
.map-timeline button:hover { opacity:0.85; }
.map-timeline .count-display { font-size:11px; color:var(--text3); }
/* 洞察页面 */
.insights-container { padding:24px; overflow-y:auto; height:100%; }
.insight-card { background:var(--card); border:1px solid var(--border); border-radius:8px; padding:20px; margin-bottom:16px; }
.insight-card h3 { font-size:16px; color:var(--text); margin-bottom:12px; border-bottom:1px solid var(--border); padding-bottom:8px; }
.insight-card p { font-size:13px; color:var(--text2); line-height:1.8; margin-bottom:10px; }
.insight-card .highlight { color:var(--accent); font-weight:bold; }
.insight-card .data-row { display:flex; justify-content:space-between; padding:4px 0; font-size:12px; color:var(--text2); border-bottom:1px solid var(--border); }
.insight-card .data-row:last-child { border-bottom:none; }
.insight-card .data-label { color:var(--text); }
.insight-card .insight-btn { padding:6px 14px; background:var(--accent); color:#fff; border:none; border-radius:4px; font-size:12px; cursor:pointer; font-family:inherit; margin-top:8px; }
.insight-card .insight-btn:hover { opacity:0.85; }
.insight-grid { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
.insight-stat { text-align:center; padding:16px; background:var(--border); border-radius:8px; }
.insight-stat .num { font-size:28px; color:var(--accent); font-weight:bold; }
.insight-stat .label { font-size:11px; color:var(--text3); margin-top:4px; }
/* 节点脉冲 */
@keyframes pulse { 0%,100%{filter:drop-shadow(0 0 4px rgba(194,53,49,0.3))} 50%{filter:drop-shadow(0 0 12px rgba(194,53,49,0.7))} }
.famous-pulse { animation: pulse 2s ease-in-out infinite; }
/* 深色模式图表 */
body.dark .stats-card canvas { filter: brightness(0.9); }
/* 诗人故事页面 */
.story-overlay { position:fixed; top:0; left:0; right:0; bottom:0; background:var(--bg); z-index:600; overflow-y:auto; display:none; }
.story-overlay.show { display:block; }
.story-container { max-width:800px; margin:0 auto; padding:40px 24px; }
.story-close { position:fixed; top:16px; right:24px; width:36px; height:36px; background:var(--border); border:none; border-radius:50%; font-size:18px; color:var(--text3); cursor:pointer; z-index:610; display:flex; align-items:center; justify-content:center; }
.story-close:hover { background:var(--accent); color:#fff; }
.story-header { text-align:center; margin-bottom:32px; }
.story-header h1 { font-size:32px; color:var(--text); letter-spacing:4px; margin-bottom:8px; }
.story-header .story-subtitle { font-size:14px; color:var(--text3); }
.story-header .story-bio { font-size:13px; color:var(--text2); margin-top:8px; line-height:1.8; }
.story-timeline { position:relative; padding:20px 0; margin-bottom:32px; }
.story-timeline-bar { height:4px; background:var(--border); border-radius:2px; position:relative; margin:0 40px; }
.story-timeline-fill { position:absolute; top:0; left:0; height:100%; background:var(--accent); border-radius:2px; }
.story-timeline-label { position:absolute; top:-20px; font-size:11px; color:var(--text3); }
.story-timeline-label.left { left:0; }
.story-timeline-label.right { right:0; }
.story-timeline-label.center { left:50%; transform:translateX(-50%); }
.story-section { margin-bottom:28px; }
.story-section h2 { font-size:18px; color:var(--text); border-bottom:2px solid var(--accent); padding-bottom:6px; margin-bottom:14px; display:inline-block; }
.story-stats { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:28px; }
.story-stat { text-align:center; padding:14px; background:var(--card); border:1px solid var(--border); border-radius:8px; }
.story-stat .num { font-size:24px; color:var(--accent); font-weight:bold; }
.story-stat .label { font-size:11px; color:var(--text3); margin-top:3px; }
.story-rel-grid { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
.story-rel-card { background:var(--card); border:1px solid var(--border); border-radius:8px; padding:14px; }
.story-rel-card h4 { font-size:14px; color:var(--text); margin-bottom:10px; }
.story-rel-item { display:flex; justify-content:space-between; padding:4px 0; font-size:12px; color:var(--text2); border-bottom:1px solid var(--border); cursor:pointer; }
.story-rel-item:hover { color:var(--accent); }
.story-rel-item:last-child { border-bottom:none; }
.story-word-cloud { display:flex; flex-wrap:wrap; gap:8px; margin-top:10px; }
.story-word-tag { padding:4px 10px; background:var(--border); border-radius:12px; font-size:12px; color:var(--text2); }
.story-word-tag .cnt { color:var(--accent); margin-left:4px; }
.story-place-list { display:flex; flex-wrap:wrap; gap:8px; margin-top:10px; }
.story-place-tag { padding:4px 10px; background:rgba(194,53,49,0.1); border:1px solid rgba(194,53,49,0.2); border-radius:12px; font-size:12px; color:var(--accent); }
.story-place-tag .cnt { margin-left:4px; }
.story-imagery-list { display:flex; flex-wrap:wrap; gap:8px; margin-top:10px; }
.story-imagery-tag { padding:4px 10px; background:rgba(47,69,84,0.1); border:1px solid rgba(47,69,84,0.2); border-radius:12px; font-size:12px; color:#2f4554; }
body.dark .story-imagery-tag { color:#61a0a8; border-color:rgba(97,160,168,0.3); background:rgba(97,160,168,0.1); }
.story-imagery-tag .cnt { margin-left:4px; }
.story-insight { background:var(--card); border:1px solid var(--border); border-radius:8px; padding:16px; font-size:13px; color:var(--text2); line-height:1.8; }
.story-actions { text-align:center; margin-top:32px; display:flex; gap:12px; justify-content:center; }
.story-btn { padding:8px 20px; border:1px solid var(--border); border-radius:4px; font-size:13px; cursor:pointer; font-family:inherit; background:var(--card); color:var(--text); transition:all 0.2s; }
.story-btn:hover { border-color:var(--accent); color:var(--accent); }
.story-btn.primary { background:var(--accent); color:#fff; border-color:var(--accent); }
.story-btn.primary:hover { opacity:0.85; }
"""

LOADING_HTML = '<div class="loading" id="loading"><div class="spinner"></div><div class="loading-text">唐 诗 社 交 网 络</div><div class="loading-sub">正在加载 57,607 首唐诗...</div></div>'

HEADER_HTML = """
<div class="header">
    <h1 style="cursor:pointer" onclick="goHome()" title="回到首页">唐 诗 社 交 网 络</h1>
    <div class="header-center">
        <div class="search-wrap">
            <div class="search-box"><input type="text" id="searchInput" placeholder="搜索诗人、诗题、诗句... (/)"></div>
            <div class="autocomplete" id="autocomplete"></div>
        </div>
        <div class="quick-nav">
            <button class="quick-btn" onclick="searchAndFocus('李白')">李白</button>
            <button class="quick-btn" onclick="searchAndFocus('杜甫')">杜甫</button>
            <button class="quick-btn" onclick="searchAndFocus('白居易')">白居易</button>
            <button class="fun-btn" onclick="randomPoet()">🎲 随机</button>
            <button class="fun-btn" onclick="showDailyPoet()">📅 每日</button>
        </div>
    </div>
    <div class="header-right">
        <div class="tabs">
            <button class="tab active" data-tab="network">🕸️ 网络图</button>
            <button class="tab" data-tab="map">🗺️ 地图</button>
            <button class="tab" data-tab="stats">📊 统计与洞察</button>
        </div>
        <div class="legend" id="legend">
            <div class="legend-item" data-period="初唐"><div class="legend-dot" style="background:#61a0a8"></div>初唐</div>
            <div class="legend-item" data-period="盛唐"><div class="legend-dot" style="background:#c23531"></div>盛唐</div>
            <div class="legend-item" data-period="中唐"><div class="legend-dot" style="background:#2f4554"></div>中唐</div>
            <div class="legend-item" data-period="晚唐"><div class="legend-dot" style="background:#d48265"></div>晚唐</div>
        </div>
        <button class="icon-btn" onclick="toggleDark()" title="深色模式">🌙 暗色</button>
        <button class="icon-btn" onclick="takeScreenshot()" title="截图分享">📷 截图</button>
    </div>
</div>
<div class="view active" id="graph"></div>
<div class="view" id="mapView">
    <div class="map-timeline" id="mapTimeline" onclick="L.DomEvent.stopPropagation(event)" onmousedown="L.DomEvent.stopPropagation(event)" onmouseup="L.DomEvent.stopPropagation(event)" onpointerdown="L.DomEvent.stopPropagation(event)" onpointerup="L.DomEvent.stopPropagation(event)">
        <label>⏱️ 时间线</label>
        <button id="playBtn" onclick="mapTimelineToggle()">▶ 播放</button>
        <input type="range" id="yearSlider" min="618" max="907" value="750" step="1">
        <span class="year-display" id="yearDisplay">750</span>
        <span class="period-display" id="periodDisplay">盛唐</span>
        <span class="count-display" id="countDisplay">0 位诗人</span>
    </div>
</div>
<div class="view" id="statsView"></div>
<div class="legend-help">
    <span>节点大小 = 关系数量</span><span>箭头方向 = 赠诗方向</span><span>🔴 赠出 · 🔵 收到</span><span>拖拽 · 缩放 · 点击探索</span>
</div>
<div class="panel" id="panel">
    <button class="panel-close" onclick="closePanel()" title="关闭 (Esc)">×</button>
    <div class="panel-empty" id="panelEmpty">
        <div>
            <div class="path-finder">
                <h3>🔍 诗人关系路径</h3>
                <div class="path-inputs">
                    <div class="path-input-wrap">
                        <input type="text" id="pathFrom" placeholder="诗人A" autocomplete="off">
                        <div class="path-ac" id="pathFromAc"></div>
                    </div>
                    <span class="path-sep">→</span>
                    <div class="path-input-wrap">
                        <input type="text" id="pathTo" placeholder="诗人B" autocomplete="off">
                        <div class="path-ac" id="pathToAc"></div>
                    </div>
                    <button class="path-btn" onclick="findPath()">查找</button>
                </div>
                <div id="pathResult" class="path-result"></div>
                <div class="path-examples">
                    试试: <span onclick="setPath('李白','杜甫')">李白→杜甫</span>
                    <span onclick="setPath('王維','李商隱')">王维→李商隐</span>
                    <span onclick="setPath('白居易','元稹')">白居易→元稹</span>
                </div>
            </div>
            <div style="color:var(--text3);font-size:11px;text-align:center">
                点击节点探索诗人 · 按 Esc 关闭面板 · / 搜索
            </div>
        </div>
    </div>
    <div id="panelContent" style="display:none"></div>
</div>
<button class="panel-toggle" id="panelToggle" onclick="togglePanel()" title="切换面板">◀</button>
<div class="stats-bar">
    <span>{total_poets} 位诗人</span><span>{total_edges} 条赠诗关系</span><span>{total_poems} 首唐诗</span><span>{matched_poets} 位诗人有作品</span>
</div>
<div class="tooltip" id="tooltip" style="display:none"></div>
<div class="modal-overlay" id="modalOverlay">
    <div class="modal">
        <div class="modal-header"><h2 id="modalTitle"></h2><button class="modal-close" onclick="closeModal()">×</button></div>
        <div class="modal-search"><input type="text" id="modalSearch" placeholder="搜索..."></div>
        <div class="modal-body" id="modalBody"></div>
    </div>
</div>
<div class="story-overlay" id="storyOverlay">
    <button class="story-close" onclick="closeStory()">×</button>
    <div class="story-container" id="storyContent"></div>
</div>
<div class="onboarding" id="onboarding">
    <div class="onboarding-card">
        <h2>欢迎探索唐诗社交网络</h2>
        <p><b>1,381</b> 位诗人 · <b>8,259</b> 条赠诗关系 · <b>57,607</b> 首唐诗</p>
        <div class="hint">试试搜索「春眠不觉晓」或探索诗人关系路径</div>
        <button class="onboarding-btn" onclick="closeOnboarding()">开始探索</button>
    </div>
</div>
"""

JS = r"""
// ============ 初始化 ============
window.addEventListener('load', () => setTimeout(() => document.getElementById('loading').classList.add('hide'), 300));

// 深色模式
function toggleDark() { document.body.classList.toggle('dark'); localStorage.setItem('tpn_dark', document.body.classList.contains('dark') ? '1' : '0'); }
if (localStorage.getItem('tpn_dark') === '1') document.body.classList.add('dark');

// 面板开关
function togglePanel() { const p = document.getElementById('panel'); p.classList.toggle('hidden'); document.getElementById('panelToggle').textContent = p.classList.contains('hidden') ? '▶' : '◀'; }
function closePanel() { document.getElementById('panelContent').style.display = 'none'; document.getElementById('panelEmpty').style.display = 'flex'; resetHighlight(); }

// 回到首页
function goHome() {
    switchTab('network');
    closePanel();
    resetHighlight();
    searchInput.value = '';
    history.replaceState(null, '', location.pathname);
    svg.transition().duration(750).call(zoom.transform, d3.zoomIdentity.translate(width/2, height/2).scale(1));
}

// 数据
const nodeMap = new Map(DATA.nodes.map(n => [n.id, n]));
const edgesFiltered = DATA.edges.filter(e => nodeMap.has(e.source) && nodeMap.has(e.target));
const activePeriods = new Set(Object.keys(PERIOD_COLORS));
const poemIndex = [];
DATA.nodes.forEach(n => (n.poems||[]).forEach(p => poemIndex.push({poet:n.id, title:p.title, text:p.text, period:n.period})));
const famousPoets = new Set(['李白','杜甫','白居易','王維','李商隱','杜牧','韓愈','柳宗元','劉禹錫','元稹','孟浩然','王昌齡','高適','岑參','韋應物','溫庭筠','賀知章','張九齡','王之渙','駱賓王']);

// ============ Tab ============
let currentTab = 'network';
document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => switchTab(tab.dataset.tab));
});
function switchTab(tab) {
    document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.dataset.tab === tab));
    currentTab = tab;
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    const viewId = tab === 'network' ? 'graph' : tab === 'map' ? 'mapView' : 'statsView';
    document.getElementById(viewId).classList.add('active');
    document.querySelector('.legend-help').style.display = tab === 'network' ? 'flex' : 'none';
    document.querySelector('.legend').style.display = tab === 'network' ? 'flex' : 'none';
    if (tab === 'map' && !mapInitialized) initMap();
    if (tab === 'stats' && !statsInitialized) initStats();
}

// ============ 网络图 ============
const container = document.getElementById('graph');
const width = container.clientWidth, height = container.clientHeight;
const svg = d3.select('#graph').append('svg').attr('width', width).attr('height', height);
// 箭头标记
const defs = svg.append('defs');
defs.append('marker').attr('id','arrow-default').attr('viewBox','0 0 10 10').attr('refX',10).attr('refY',5).attr('markerWidth',6).attr('markerHeight',6).attr('orient','auto')
    .append('path').attr('d','M 0 0 L 10 5 L 0 10 z').attr('fill','rgba(44,44,44,0.25)');
defs.append('marker').attr('id','arrow-out').attr('viewBox','0 0 10 10').attr('refX',10).attr('refY',5).attr('markerWidth',7).attr('markerHeight',7).attr('orient','auto')
    .append('path').attr('d','M 0 0 L 10 5 L 0 10 z').attr('fill','#e74c3c');
defs.append('marker').attr('id','arrow-in').attr('viewBox','0 0 10 10').attr('refX',10).attr('refY',5).attr('markerWidth',7).attr('markerHeight',7).attr('orient','auto')
    .append('path').attr('d','M 0 0 L 10 5 L 0 10 z').attr('fill','#3498db');
const g = svg.append('g');
const zoom = d3.zoom().scaleExtent([0.1, 8]).on('zoom', e => g.attr('transform', e.transform));
svg.call(zoom);

function getNodeRadius(d) { return Math.max(4, Math.min(30, 4 + Math.sqrt(d.totalDegree||1) * 1.2)); }

const simulation = d3.forceSimulation(DATA.nodes)
    .force('link', d3.forceLink(edgesFiltered).id(d => d.id).distance(80))
    .force('charge', d3.forceManyBody().strength(-120))
    .force('center', d3.forceCenter(width/2, height/2))
    .force('collision', d3.forceCollide().radius(d => getNodeRadius(d) + 2));

const link = g.append('g').selectAll('line').data(edgesFiltered).join('line')
    .attr('stroke','rgba(44,44,44,0.15)').attr('stroke-width', d => Math.max(0.5, Math.min(3, d.weight*0.5)))
    .attr('marker-end','url(#arrow-default)')
    .style('cursor','pointer')
    .on('click', (e,d) => showEdgeDetail(d))
    .on('mouseover', function(e,d) { d3.select(this).attr('stroke','rgba(194,53,49,0.7)').attr('stroke-width',Math.max(2,d.weight*0.8)); showTooltip(e,(d.source.id||d.source)+' 赠诗给 '+(d.target.id||d.target)+' ('+d.weight+'次)'); })
    .on('mouseout', function(e,d) { d3.select(this).attr('stroke','rgba(44,44,44,0.15)').attr('stroke-width',Math.max(0.5,d.weight*0.5)).attr('marker-end','url(#arrow-default)'); hideTooltip(); });

const node = g.append('g').selectAll('circle').data(DATA.nodes).join('circle')
    .attr('r', d => getNodeRadius(d)).attr('fill', d => PERIOD_COLORS[d.period]||'#999')
    .attr('stroke','#f5f0e8').attr('stroke-width',1).attr('opacity',0.85).style('cursor','pointer')
    .classed('famous-pulse', d => famousPoets.has(d.id))
    .call(d3.drag().on('start',dragStart).on('drag',dragging).on('end',dragEnd))
    .on('click', (e,d) => showNodeDetail(d))
    .on('mouseover', function(e,d) { d3.select(this).attr('stroke','#c23531').attr('stroke-width',3); let tip=d.id; if(d.birthYear)tip+=' ('+d.birthYear+'-'+(d.deathYear||'?')+')'; tip+=' | '+(d.poemCount||0)+'首诗 | '+d.totalDegree+'条关系'; showTooltip(e,tip); highlightNode(d); })
    .on('mouseout', function() { d3.select(this).attr('stroke','#f5f0e8').attr('stroke-width',1); hideTooltip(); resetHighlight(); });

const label = g.append('g').selectAll('text').data(DATA.nodes.filter(d => d.totalDegree >= 5)).join('text')
    .text(d => d.id).attr('font-size', d => d.totalDegree >= 15 ? 11 : 9)
    .attr('fill','var(--text)').attr('text-anchor','middle').attr('dy', d => -getNodeRadius(d)-3)
    .style('pointer-events','none').style('font-family',"'STKaiti','KaiTi',serif");

simulation.on('tick', () => {
    link.attr('x1',d=>d.source.x).attr('y1',d=>d.source.y).attr('x2',d=>d.target.x).attr('y2',d=>d.target.y);
    node.attr('cx',d=>d.x).attr('cy',d=>d.y);
    label.attr('x',d=>d.x).attr('y',d=>d.y);
});

function dragStart(e,d) { if(!e.active) simulation.alphaTarget(0.3).restart(); d.fx=d.x; d.fy=d.y; }
function dragging(e,d) { d.fx=e.x; d.fy=e.y; }
function dragEnd(e,d) { if(!e.active) simulation.alphaTarget(0); d.fx=null; d.fy=null; }

// ============ 地图 ============
let mapInitialized = false, map;
let mapMarkers = L.layerGroup();
let mapGeoNodes = [];
function initMap() {
    mapInitialized = true;
    map = L.map('mapView').setView([34, 110], 4);
    L.tileLayer('https://webrd0{s}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}', { subdomains:['1','2','3','4'], attribution:'&copy; 高德地图', maxZoom:18 }).addTo(map);
    mapMarkers.addTo(map);
    mapGeoNodes = DATA.nodes.filter(n => n.lng && n.lat);
    updateMapMarkers(618, 907);

    // 时间线滑动条事件
    const slider = document.getElementById('yearSlider');
    slider.addEventListener('input', function() { updateMapMarkers(618, parseInt(this.value)); });
}

function updateMapMarkers(minYear, maxYear) {
    mapMarkers.clearLayers();
    const active = mapGeoNodes.filter(n => {
        if (!n.birthYear || n.birthYear <= 0) return false;
        const death = n.deathYear || (n.birthYear + 60); // 无死亡年则估算60岁
        return n.birthYear <= maxYear && death >= maxYear; // 在当前年份还活着
    });
    active.forEach(n => {
        const color = PERIOD_COLORS[n.period] || '#999';
        const r = Math.max(3, Math.min(12, 3 + Math.sqrt(n.totalDegree||1)*0.6));
        const circle = L.circleMarker([n.lat, n.lng], { radius:r, fillColor:color, color:'#fff', weight:1, fillOpacity:0.8 });
        circle.bindTooltip(n.id+' ('+(n.poemCount||0)+'首)', {direction:'top', offset:[0,-r]});
        circle.on('click', () => {
            const poems = (n.poems||[]).slice(0,3);
            let h = '<div style="font-family:STKaiti,KaiTi,serif;min-width:180px">';
            h += '<div style="font-size:15px;font-weight:bold;margin-bottom:3px">'+n.id+'</div>';
            let bio = [n.period];
            if(n.birthYear) bio.push(n.birthYear+'-'+(n.deathYear||'?'));
            if(n.deathAge) bio.push('享年'+n.deathAge);
            if(n.place) bio.push(n.place);
            h += '<div style="font-size:11px;color:#888;margin-bottom:6px">'+bio.join(' · ')+'</div>';
            h += '<div style="font-size:11px;margin-bottom:6px">诗作:'+(n.poemCount||0)+' · 赠诗:'+n.outDegree+' · 被赠:'+n.inDegree+'</div>';
            if(poems.length>0){h+='<div style="border-top:1px solid #eee;padding-top:5px">';poems.forEach(p=>{h+='<div style="font-size:10px;color:#555;margin-bottom:3px"><b>《'+p.title+'》</b></div>';h+='<div style="font-size:10px;color:#888;margin-bottom:4px">'+p.text.split('\n').slice(0,2).join('<br>')+'</div>';});h+='</div>';}
            h += '<div style="margin-top:6px"><a href="javascript:void(0)" onclick="switchTab(\'network\');searchAndFocus(\''+n.id+'\')" style="color:#c23531;font-size:11px">在网络图中查看 →</a></div></div>';
            circle.bindPopup(h, {maxWidth:280}).openPopup();
        });
        circle.addTo(mapMarkers);
    });

    // 更新显示
    const year = maxYear;
    document.getElementById('yearDisplay').textContent = year;
    let period = '未知';
    if (year >= 618 && year < 713) period = '初唐';
    else if (year >= 713 && year < 766) period = '盛唐';
    else if (year >= 766 && year < 836) period = '中唐';
    else if (year >= 836 && year <= 907) period = '晚唐';
    document.getElementById('periodDisplay').textContent = period;
    document.getElementById('countDisplay').textContent = active.length + ' 位诗人';
}

let mapTimelinePlaying = false, mapTimelineInterval = null, mapTimelineYear = 618;
function mapTimelineToggle() {
    const btn = document.getElementById('playBtn');
    if (mapTimelinePlaying) {
        // 暂停
        clearInterval(mapTimelineInterval);
        mapTimelinePlaying = false;
        btn.textContent = '▶ 继续';
    } else {
        // 播放
        mapTimelinePlaying = true;
        btn.textContent = '⏸ 暂停';
        const slider = document.getElementById('yearSlider');
        if (mapTimelineYear >= 907) mapTimelineYear = 618; // 重新开始
        mapTimelineInterval = setInterval(() => {
            slider.value = mapTimelineYear;
            updateMapMarkers(618, mapTimelineYear);
            mapTimelineYear += 3;
            if (mapTimelineYear > 907) {
                clearInterval(mapTimelineInterval);
                mapTimelinePlaying = false;
                btn.textContent = '▶ 重播';
            }
        }, 100);
    }
}
function mapTimelinePlay() { mapTimelineYear = 618; mapTimelinePlaying = false; mapTimelineToggle(); }

// 用户拖动滑块时同步内部年份
document.addEventListener('DOMContentLoaded', () => {
    const slider = document.getElementById('yearSlider');
    if (slider) {
        slider.addEventListener('mousedown', () => { if (mapTimelinePlaying) { clearInterval(mapTimelineInterval); } });
        slider.addEventListener('mouseup', () => { mapTimelineYear = parseInt(slider.value); if (mapTimelinePlaying) { mapTimelineToggle(); mapTimelineToggle(); } });
    }
});

// ============ 统计与洞察 ============
let statsInitialized = false;
function initStats() {
    statsInitialized = true;
    const sv = document.getElementById('statsView');
    const pd = STATS.periodDist, tp = STATS.topPoets, ns = STATS.networkStats;
    const periods = ['初唐','盛唐','中唐','晚唐','未知'];
    const pColors = periods.map(p => PERIOD_COLORS[p]||'#999');

    const topByPoems = DATA.nodes.filter(n => n.poemCount > 0).sort((a,b) => b.poemCount - a.poemCount).slice(0, 20);
    const poemBins = [0,1,5,10,50,100,500,1000,3000];
    const poemDist = poemBins.map((b,i) => { const next = poemBins[i+1] || 99999; return DATA.nodes.filter(n => n.poemCount >= b && n.poemCount < next).length; });
    const weightBins = [1,2,3,5,10,20,50];
    const weightDist = weightBins.map((b,i) => { const next = weightBins[i+1] || 999; return edgesFiltered.filter(e => e.weight >= b && e.weight < next).length; });
    const degreeBins = [0,1,2,5,10,20,50,100,200];
    const degreeDist = degreeBins.map((b,i) => { const next = degreeBins[i+1] || 999; return DATA.nodes.filter(n => n.totalDegree >= b && n.totalDegree < next).length; });

    // 洞察计算
    const adj = new Map();
    edgesFiltered.forEach(e => { const s=e.source.id||e.source, t=e.target.id||e.target; if(!adj.has(s))adj.set(s,[]); if(!adj.has(t))adj.set(t,[]); adj.get(s).push(t); adj.get(t).push(s); });
    const connectedNodes = DATA.nodes.filter(n => n.totalDegree > 0).map(n => n.id);
    let totalDist = 0, distCount = 0;
    for (let i = 0; i < Math.min(100, connectedNodes.length); i++) {
        const start = connectedNodes[Math.floor(Math.random() * connectedNodes.length)];
        const visited = new Map(); visited.set(start, 0); const queue = [start];
        while (queue.length > 0) { const curr = queue.shift(); for (const next of (adj.get(curr) || [])) { if (!visited.has(next)) { visited.set(next, visited.get(curr) + 1); queue.push(next); } } }
        visited.forEach((dist, node) => { if (node !== start && dist > 0) { totalDist += dist; distCount++; } });
    }
    const avgPath = distCount > 0 ? (totalDist / distCount).toFixed(1) : 'N/A';
    const busiest = DATA.nodes.filter(n => n.totalDegree > 0).sort((a,b) => b.totalDegree - a.totalDegree).slice(0, 5);
    const lonelyPoets = DATA.nodes.filter(n => n.poemCount >= 50 && n.totalDegree <= 3).sort((a,b) => b.poemCount - a.poemCount).slice(0, 5);
    const geoByPeriod = {};
    ['初唐','盛唐','中唐','晚唐'].forEach(p => {
        const nodes = DATA.nodes.filter(n => n.period === p && n.lng && n.lat);
        if (nodes.length > 0) geoByPeriod[p] = { lng: (nodes.reduce((s,n) => s + n.lng, 0) / nodes.length).toFixed(1), lat: (nodes.reduce((s,n) => s + n.lat, 0) / nodes.length).toFixed(1), count: nodes.length };
    });

    // 一次性构建全部 HTML
    sv.innerHTML = '<div class="stats-summary">'
        + '<div class="stats-summary-item"><div class="stats-summary-num">'+DATA.nodes.length+'</div><div class="stats-summary-label">诗人总数</div></div>'
        + '<div class="stats-summary-item"><div class="stats-summary-num">'+edgesFiltered.length+'</div><div class="stats-summary-label">赠诗关系</div></div>'
        + '<div class="stats-summary-item"><div class="stats-summary-num">'+poemIndex.length+'</div><div class="stats-summary-label">收录诗作</div></div>'
        + '<div class="stats-summary-item"><div class="stats-summary-num">'+ns.avgDegree+'</div><div class="stats-summary-label">平均连接度</div></div>'
        + '<div class="stats-summary-item"><div class="stats-summary-num">'+ns.maxDegree+'</div><div class="stats-summary-label">最大连接度</div></div>'
        + '<div class="stats-summary-item"><div class="stats-summary-num">'+topByPoems[0]?.id+'</div><div class="stats-summary-label">诗作最多</div></div>'
        + '<div class="stats-summary-item"><div class="stats-summary-num">'+tp[0]?.id+'</div><div class="stats-summary-label">关系最多</div></div>'
        + '<div class="stats-summary-item"><div class="stats-summary-num">'+avgPath+'</div><div class="stats-summary-label">平均距离</div></div>'
        + '</div><div class="stats-grid">'
        + '<div class="stats-card"><h3>📊 朝代分布</h3><canvas id="chartPeriod"></canvas></div>'
        + '<div class="stats-card"><h3>🏆 社交影响力 TOP 20</h3><canvas id="chartTop"></canvas></div>'
        + '<div class="stats-card"><h3>📝 诗作数量 TOP 20</h3><canvas id="chartPoems"></canvas></div>'
        + '<div class="stats-card"><h3>📈 诗作数量分布</h3><canvas id="chartPoemDist"></canvas></div>'
        + '<div class="stats-card"><h3>🔗 连接度分布</h3><canvas id="chartDegree"></canvas></div>'
        + '<div class="stats-card"><h3>📊 赠诗次数分布</h3><canvas id="chartWeight"></canvas></div>'
        + '</div>'
        + '<div class="insight-card"><h3>👑 唐代社交之王</h3><p>这些诗人拥有最广泛的社交网络，是唐代文人圈的核心节点。</p>'
        + busiest.map(n => '<div class="data-row"><span class="data-label"><b>' + n.id + '</b> (' + n.period + ')</span><span>' + n.totalDegree + ' 条关系 · ' + (n.poemCount||0) + ' 首诗</span></div>').join('')
        + '<button class="insight-btn" onclick="searchAndFocus(\'' + busiest[0].id + '\')">探索 ' + busiest[0].id + ' 的网络</button></div>'
        + '<div class="insight-card"><h3>🏔️ 最「孤独」的高产诗人</h3><p>写了大量诗作，但在赠诗关系网络中却很少出现。</p>'
        + lonelyPoets.map(n => '<div class="data-row"><span class="data-label"><b>' + n.id + '</b> (' + n.period + ')</span><span>' + (n.poemCount||0) + ' 首诗 · 仅 ' + n.totalDegree + ' 条关系</span></div>').join('') + '</div>'
        + '<div class="insight-card"><h3>🌍 诗歌地理中心迁移</h3><p>从初唐到晚唐，诗歌的地理中心如何移动？</p>'
        + Object.entries(geoByPeriod).map(([p, d]) => '<div class="data-row"><span class="data-label"><b>' + p + '</b></span><span>中心: (' + d.lat + '°N, ' + d.lng + '°E) · ' + d.count + ' 位诗人</span></div>').join('')
        + '<button class="insight-btn" onclick="switchTab(\'map\');mapTimelinePlay()">观看时间线动画</button></div>'
        + '<div style="margin-top:24px;padding:16px;background:var(--card);border:1px solid var(--border);border-radius:8px;text-align:center">'
        + '<div style="font-size:14px;color:var(--text);margin-bottom:8px">关于本项目</div>'
        + '<div style="font-size:12px;color:var(--text2);line-height:1.8">'
        + '数据来源：<a href="https://projects.iq.harvard.edu/cbdb" target="_blank" style="color:var(--accent)">CBDB 中国历代人物传记资料库</a>（Harvard University）+ <a href="https://github.com/chinese-poetry/chinese-poetry" target="_blank" style="color:var(--accent)">chinese-poetry</a>（全唐诗）<br>'
        + '技术栈：D3.js · Leaflet.js · Chart.js · html2canvas<br>'
        + '项目地址：<a href="https://github.com/mengyuchun/tang-poetry-network" target="_blank" style="color:var(--accent)">GitHub</a> · License: MIT<br>'
        + '方法论：平均距离通过 BFS 算法在连通分量中采样计算。地理中心为诗人籍贯坐标的算术平均值。局限性：赠诗关系仅记录有文献记载的交往。<br>'
        + '<span style="color:var(--text3)">如果觉得有趣，请给个 Star ⭐</span></div></div>';

    // 初始化图表（HTML 已全部渲染完毕）
    new Chart(document.getElementById('chartPeriod'), { type:'doughnut', data:{labels:periods,datasets:[{data:periods.map(p=>pd[p]||0),backgroundColor:pColors,borderWidth:0}]}, options:{responsive:true,plugins:{legend:{position:'bottom'}}} });
    new Chart(document.getElementById('chartTop'), { type:'bar', data:{labels:tp.map(p=>p.id),datasets:[{label:'赠诗',data:tp.map(p=>p.outDegree),backgroundColor:'rgba(194,53,49,0.7)'},{label:'被赠',data:tp.map(p=>p.inDegree),backgroundColor:'rgba(47,69,84,0.7)'}]}, options:{indexAxis:'y',responsive:true,scales:{x:{stacked:true},y:{stacked:true}},plugins:{legend:{position:'bottom'}}} });
    new Chart(document.getElementById('chartPoems'), { type:'bar', data:{labels:topByPoems.map(p=>p.id),datasets:[{label:'诗作数',data:topByPoems.map(p=>p.poemCount),backgroundColor:'rgba(97,160,168,0.7)'}]}, options:{indexAxis:'y',responsive:true,plugins:{legend:{display:false}}} });
    new Chart(document.getElementById('chartPoemDist'), { type:'bar', data:{labels:poemBins.map((b,i)=>{const n=poemBins[i+1];return n?b+'-'+n:b+'+';}),datasets:[{label:'诗人数',data:poemDist,backgroundColor:'rgba(194,53,49,0.6)'}]}, options:{responsive:true,plugins:{legend:{display:false}},scales:{y:{type:'logarithmic'}}} });
    new Chart(document.getElementById('chartDegree'), { type:'bar', data:{labels:degreeBins.map((b,i)=>{const n=degreeBins[i+1];return n?b+'-'+n:b+'+';}),datasets:[{label:'节点数',data:degreeDist,backgroundColor:'rgba(47,69,84,0.6)'}]}, options:{responsive:true,plugins:{legend:{display:false}},scales:{y:{type:'logarithmic'}}} });
    new Chart(document.getElementById('chartWeight'), { type:'bar', data:{labels:weightBins.map((b,i)=>{const n=weightBins[i+1];return n?b+'-'+n:b+'+';}),datasets:[{label:'关系数',data:weightDist,backgroundColor:'rgba(212,130,101,0.6)'}]}, options:{responsive:true,plugins:{legend:{display:false}},scales:{y:{type:'logarithmic'}}} });
}

// ============ 路径输入自动补全 ============
function setupPathAc(inputId, acId) {
    const input = document.getElementById(inputId);
    const ac = document.getElementById(acId);
    let idx = -1;
    input.addEventListener('input', function() {
        const q = this.value.trim();
        if (!q) { ac.style.display = 'none'; return; }
        const matches = DATA.nodes.filter(n => n.id.includes(q)).slice(0, 8);
        if (matches.length === 0) { ac.style.display = 'none'; return; }
        idx = -1;
        ac.innerHTML = matches.map((m, i) => {
            const c = PERIOD_COLORS[m.period] || '#999';
            return '<div class="path-ac-item" data-idx="' + i + '" data-name="' + m.id + '"><span><span class="ac-pd" style="background:' + c + '"></span>' + m.id + '</span><span style="font-size:10px;color:rgba(245,240,232,0.4)">' + (m.poemCount || 0) + '首</span></div>';
        }).join('');
        ac.style.display = 'block';
        ac.querySelectorAll('.path-ac-item').forEach(item => {
            item.addEventListener('click', () => { input.value = item.dataset.name; ac.style.display = 'none'; });
        });
    });
    input.addEventListener('keydown', function(e) {
        const items = ac.querySelectorAll('.path-ac-item');
        if (e.key === 'ArrowDown') { e.preventDefault(); idx = Math.min(idx + 1, items.length - 1); items.forEach((it, i) => it.classList.toggle('active', i === idx)); if (items[idx]) items[idx].scrollIntoView({ block: 'nearest' }); }
        else if (e.key === 'ArrowUp') { e.preventDefault(); idx = Math.max(idx - 1, 0); items.forEach((it, i) => it.classList.toggle('active', i === idx)); if (items[idx]) items[idx].scrollIntoView({ block: 'nearest' }); }
        else if (e.key === 'Enter') { e.preventDefault(); if (idx >= 0 && items[idx]) { input.value = items[idx].dataset.name; ac.style.display = 'none'; } else { findPath(); ac.style.display = 'none'; } }
        else if (e.key === 'Escape') { ac.style.display = 'none'; }
    });
    input.addEventListener('blur', () => setTimeout(() => ac.style.display = 'none', 200));
}
setupPathAc('pathFrom', 'pathFromAc');
setupPathAc('pathTo', 'pathToAc');

// ============ 路径查找 ============
function findPath() {
    const from = document.getElementById('pathFrom').value.trim();
    const to = document.getElementById('pathTo').value.trim();
    if (!from||!to) { document.getElementById('pathResult').innerHTML='<div style="color:var(--text3)">请输入两位诗人</div>'; return; }
    if (!nodeMap.has(from)) { document.getElementById('pathResult').innerHTML='<div style="color:var(--accent)">找不到「'+from+'」</div>'; return; }
    if (!nodeMap.has(to)) { document.getElementById('pathResult').innerHTML='<div style="color:var(--accent)">找不到「'+to+'」</div>'; return; }
    if (from===to) { document.getElementById('pathResult').innerHTML='<div style="color:var(--text3)">两位诗人相同</div>'; return; }
    const adj = new Map();
    edgesFiltered.forEach(e => { const s=e.source.id||e.source, t=e.target.id||e.target; if(!adj.has(s))adj.set(s,[]); if(!adj.has(t))adj.set(t,[]); adj.get(s).push(t); adj.get(t).push(s); });
    const queue = [[from]], visited = new Set([from]);
    let found = null;
    while (queue.length > 0 && !found) {
        const path = queue.shift(), curr = path[path.length-1];
        for (const next of (adj.get(curr)||[])) {
            if (visited.has(next)) continue; visited.add(next);
            const np = [...path, next]; if (next===to) { found=np; break; } queue.push(np);
        }
    }
    if (!found) { document.getElementById('pathResult').innerHTML='<div style="color:var(--text3)">未找到关系路径</div>'; return; }
    let h = '<div style="font-size:12px;color:var(--text);margin-bottom:6px">关系链 ('+(found.length-1)+' 步):</div>';
    found.forEach((n,i) => { const nd=nodeMap.get(n); h+='<div class="path-step"><span class="path-node" onclick="searchAndFocus(\''+n+'\')">'+n+'</span>'; if(nd)h+='<span style="font-size:10px;color:var(--text3)">('+(nd.poemCount||0)+'首)</span>'; if(i<found.length-1)h+='<span class="path-arrow"> → </span>'; h+='</div>'; });
    document.getElementById('pathResult').innerHTML = h;
    const pathSet = new Set(found), pathEdges = new Set();
    for (let i=0;i<found.length-1;i++) { const a=found[i],b=found[i+1]; edgesFiltered.forEach(e=>{const s=e.source.id||e.source,t=e.target.id||e.target;if((s===a&&t===b)||(s===b&&t===a))pathEdges.add(e);}); }
    node.attr('opacity', n => pathSet.has(n.id)?1:0.08);
    link.attr('stroke', e => pathEdges.has(e)?'var(--accent)':'rgba(44,44,44,0.03)').attr('stroke-width', e => pathEdges.has(e)?3:0.3).attr('marker-end', e => pathEdges.has(e)?'url(#arrow-out)':'url(#arrow-default)');
    label.attr('opacity', n => pathSet.has(n.id)?1:0.08);
}
function setPath(a,b) { document.getElementById('pathFrom').value=a; document.getElementById('pathTo').value=b; findPath(); }

// ============ 趣味功能 ============
function randomPoet() { const wp=DATA.nodes.filter(n=>n.poemCount>0); const p=wp[Math.floor(Math.random()*wp.length)]; if(p)searchAndFocus(p.id); }

function showDailyPoet() {
    const today = new Date(); const seed = today.getFullYear()*10000+(today.getMonth()+1)*100+today.getDate();
    const wp = DATA.nodes.filter(n => n.poemCount >= 10);
    const pick = wp[seed % wp.length];
    if (pick) {
        const poems = (pick.poems||[]).slice(0,3);
        let h = '<div style="text-align:center;margin-bottom:12px"><div style="font-size:20px;font-weight:bold;color:var(--text)">'+pick.id+'</div>';
        h += '<div style="font-size:12px;color:var(--text3)">'+pick.period+' · '+(pick.poemCount||0)+'首诗</div></div>';
        if(poems.length>0){poems.forEach(p=>{h+='<div class="poem-card"><div class="poem-title">《'+p.title+'》</div><div class="poem-text">'+p.text+'</div></div>';});}
        showModal('📅 每日一诗 · '+today.toLocaleDateString('zh-CN'), [], 'daily');
        document.getElementById('modalBody').innerHTML = h;
    }
}

// ============ 截图分享 ============
function takeScreenshot() {
    const btn = event.target; btn.textContent = '⏳';
    html2canvas(document.body, { backgroundColor: getComputedStyle(document.body).getPropertyValue('--bg').trim(), scale: 2, useCORS: true }).then(canvas => {
        const link = document.createElement('a');
        link.download = '唐诗社交网络_' + new Date().toISOString().slice(0,10) + '.png';
        link.href = canvas.toDataURL('image/png');
        link.click();
        btn.textContent = '📷';
    }).catch(() => { btn.textContent = '📷'; alert('截图失败，请尝试使用浏览器截图功能'); });
}

// ============ Tooltip ============
const tooltip = document.getElementById('tooltip');
function showTooltip(e, text) { tooltip.textContent = text; tooltip.style.display = 'block'; tooltip.style.left = (e.pageX+10)+'px'; tooltip.style.top = (e.pageY-6)+'px'; }
function hideTooltip() { tooltip.style.display = 'none'; }

// ============ 高亮 ============
function highlightNode(d) {
    const c = new Set(); c.add(d.id);
    edgesFiltered.forEach(e => { const s=e.source.id||e.source, t=e.target.id||e.target; if(s===d.id)c.add(t); if(t===d.id)c.add(s); });
    node.attr('opacity', n => c.has(n.id)?1:0.08);
    link.attr('stroke', e => { const s=e.source.id||e.source, t=e.target.id||e.target; if(s===d.id) return '#e74c3c'; if(t===d.id) return '#3498db'; return 'rgba(44,44,44,0.03)'; })
        .attr('stroke-width', e => { const s=e.source.id||e.source, t=e.target.id||e.target; return (s===d.id||t===d.id)?Math.max(2,e.weight*1):Math.max(0.3,e.weight*0.3); })
        .attr('marker-end', e => { const s=e.source.id||e.source, t=e.target.id||e.target; if(s===d.id) return 'url(#arrow-out)'; if(t===d.id) return 'url(#arrow-in)'; return 'url(#arrow-default)'; });
    label.attr('opacity', n => c.has(n.id)?1:0.08);
}
function resetHighlight() {
    node.attr('opacity', d => activePeriods.has(d.period)?0.85:0.05);
    link.attr('stroke','rgba(44,44,44,0.15)').attr('stroke-width', d => Math.max(0.5,d.weight*0.5)).attr('marker-end','url(#arrow-default)');
    label.attr('opacity', 1);
}

// ============ 时期过滤 ============
function applyFilter() {
    node.attr('opacity', d => activePeriods.has(d.period)?0.85:0.05).attr('pointer-events', d => activePeriods.has(d.period)?'auto':'none');
    link.attr('opacity', d => { const s=d.source.id||d.source, t=d.target.id||d.target; const sn=nodeMap.get(s),tn=nodeMap.get(t); return(sn&&activePeriods.has(sn.period)&&tn&&activePeriods.has(tn.period))?1:0.03; });
    label.attr('opacity', d => activePeriods.has(d.period)?1:0.05);
    document.querySelectorAll('.legend-item').forEach(el => el.classList.toggle('inactive', !activePeriods.has(el.dataset.period)));
}
document.querySelectorAll('.legend-item').forEach(el => {
    el.addEventListener('click', () => { const p=el.dataset.period; activePeriods.has(p)?activePeriods.delete(p):activePeriods.add(p); applyFilter(); });
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
    if (results.length===0) { acEl.style.display='none'; return; }
    acIndex=-1; renderAC(results,q); acEl.style.display='block';
}

function hl(text, q) { if(!q)return text; const i=text.indexOf(q); if(i===-1)return text; const s=Math.max(0,i-10),e=Math.min(text.length,i+q.length+20); return(s>0?'...':'')+text.slice(s,e).replace(q,'<span class="ac-highlight">'+q+'</span>')+(e<text.length?'...':''); }

function renderAC(results, q) {
    let html='',ps=false,ms=false;
    results.forEach((r,i) => {
        if(r.type==='poet'&&!ps){html+='<div class="ac-section">诗人</div>';ps=true;}
        if(r.type==='poem'&&!ms){html+='<div class="ac-section">诗作</div>';ms=true;}
        if(r.type==='poet'){const m=r.data;const c=PERIOD_COLORS[m.period]||'#999';html+='<div class="ac-item" data-idx="'+i+'" data-type="poet" data-name="'+m.id+'"><div class="ac-left"><span class="ac-pd" style="background:'+c+'"></span><span class="ac-name">'+m.id+'</span><span class="ac-ctx">'+m.period+(m.place?' · '+m.place:'')+'</span></div><span class="ac-right">'+(m.poemCount||0)+'首</span></div>';}
        else{const p=r.data;html+='<div class="ac-item" data-idx="'+i+'" data-type="poem" data-poet="'+p.poet+'"><div class="ac-left"><span class="ac-name">'+p.poet+'</span><span class="ac-ctx">《'+p.title+'》'+hl(p.text,q)+'</span></div></div>';}
    });
    acEl.innerHTML=html;
    acEl.querySelectorAll('.ac-item').forEach(item => item.addEventListener('click', () => { searchAndFocus(item.dataset.type==='poet'?item.dataset.name:item.dataset.poet); acEl.style.display='none'; }));
}

searchInput.addEventListener('keydown', function(e) {
    const items=acEl.querySelectorAll('.ac-item');
    if(e.key==='ArrowDown'){e.preventDefault();acIndex=Math.min(acIndex+1,items.length-1);updAC(items);}
    else if(e.key==='ArrowUp'){e.preventDefault();acIndex=Math.max(acIndex-1,0);updAC(items);}
    else if(e.key==='Enter'){e.preventDefault();if(acIndex>=0&&items[acIndex]){const it=items[acIndex];searchAndFocus(it.dataset.type==='poet'?it.dataset.name:it.dataset.poet);}else{const q=this.value.trim();if(q){const m=DATA.nodes.find(n=>n.id===q)||DATA.nodes.find(n=>n.id.includes(q));if(m)searchAndFocus(m.id);}}acEl.style.display='none';}
    else if(e.key==='Escape'){acEl.style.display='none';this.blur();}
});
function updAC(items){items.forEach((it,i)=>it.classList.toggle('active',i===acIndex));if(items[acIndex])items[acIndex].scrollIntoView({block:'nearest'});}
document.addEventListener('click', e => { if(!e.target.closest('.search-wrap'))acEl.style.display='none'; });

// ============ 键盘 ============
document.addEventListener('keydown', e => {
    if(e.key==='/'&&document.activeElement!==searchInput&&!document.querySelector('.modal-overlay.show')){e.preventDefault();searchInput.focus();}
    if(e.key==='Escape'){if(document.querySelector('.modal-overlay.show'))closeModal();else if(document.getElementById('onboarding').classList.contains('show'))closeOnboarding();else closePanel();}
    if(e.key==='Tab'&&document.activeElement===document.body){e.preventDefault();const tabs=['network','map','stats'];switchTab(tabs[(tabs.indexOf(currentTab)+1)%tabs.length]);}
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
    // 确保面板可见
    document.getElementById('panel').classList.remove('hidden');
    document.getElementById('panelToggle').textContent = '◀';
    const pc=PERIOD_COLORS[d.period]||'#999';const rels=getRelations(d);const poems=d.poems||[];
    let h='<div class="panel-title">'+d.id+'</div><div class="panel-period" style="background:'+pc+'">'+d.period+'</div>';
    // 生卒年信息
    let bioInfo = [];
    if(d.birthYear) bioInfo.push((d.female?'♀ ':'')+'生于 '+d.birthYear+'年');
    if(d.deathYear) bioInfo.push('卒于 '+d.deathYear+'年');
    if(d.deathAge) bioInfo.push('享年 '+d.deathAge+'岁');
    if(d.place) bioInfo.push('\u{1F4CD} '+d.place);
    if(bioInfo.length > 0) h+='<div style="color:var(--text3);font-size:12px;margin-bottom:10px">'+bioInfo.join(' · ')+'</div>';
    h+='<div class="panel-stats"><div class="panel-stat" onclick="showPoemsModal(\''+d.id+'\')"><div class="panel-stat-num">'+(d.poemCount||0)+'</div><div class="panel-stat-label">诗作</div></div>';
    h+='<div class="panel-stat" onclick="showRelationsModal(\''+d.id+'\',\'out\')"><div class="panel-stat-num" style="color:#e74c3c">'+d.outDegree+'</div><div class="panel-stat-label">赠出 🔴</div></div>';
    h+='<div class="panel-stat" onclick="showRelationsModal(\''+d.id+'\',\'in\')"><div class="panel-stat-num" style="color:#3498db">'+d.inDegree+'</div><div class="panel-stat-label">收到 🔵</div></div></div>';
    // 故事按钮
    h+='<div style="margin-bottom:14px"><button class="story-btn primary" onclick="showStory(\''+d.id+'\')">📖 查看 '+d.id+' 的故事</button></div>';
    if(poems.length>0){h+='<div class="panel-section"><h3>代表诗作 ';if(poems.length>5)h+='<span class="view-all" onclick="showPoemsModal(\''+d.id+'\')">全部 '+poems.length+' 首 →</span>';h+='</h3>';poems.slice(0,5).forEach(p=>{h+='<div class="poem-card"><div class="poem-title">《'+p.title+'》</div><div class="poem-text">'+p.text+'</div></div>';});h+='</div>';}
    if(rels.length>0){h+='<div class="panel-section"><h3>社交关系 ('+rels.length+') ';if(rels.length>15)h+='<span class="view-all" onclick="showRelationsModal(\''+d.id+'\',\'all\')">全部 →</span>';h+='</h3>';rels.slice(0,15).forEach(r=>{h+='<div class="relation-item" onclick="searchAndFocus(\''+r.name+'\')"><b>'+r.name+'</b> — '+r.dir+' '+r.weight+'次</div>';});h+='</div>';}
    panel.innerHTML=h;history.replaceState(null,'','#'+encodeURIComponent(d.id));
}

function showEdgeDetail(d) {
    const panel=document.getElementById('panelContent');document.getElementById('panelEmpty').style.display='none';panel.style.display='block';
    document.getElementById('panel').classList.remove('hidden');document.getElementById('panelToggle').textContent='◀';
    const s=d.source.id||d.source,t=d.target.id||d.target;const sn=nodeMap.get(s),tn=nodeMap.get(t);
    let h='<div class="panel-title">'+s+' → '+t+'</div><div style="color:var(--text3);font-size:12px;margin-bottom:12px"><span style="color:#e74c3c">'+s+'</span> 赠诗给 <span style="color:#3498db">'+t+'</span> · '+d.weight+' 次</div>';
    [['src',s,sn],['tgt',t,tn]].forEach(([k,n,nd])=>{const ps=(nd?.poems||[]).slice(0,5);h+='<div class="panel-section"><h3>'+n+' 的诗作</h3>';if(ps.length>0){ps.forEach(p=>{h+='<div class="poem-card"><div class="poem-title">《'+p.title+'》</div><div class="poem-text">'+p.text+'</div></div>';});}else{h+='<div style="color:var(--text3)">暂无诗作</div>';}h+='</div>';});
    panel.innerHTML=h;
}

// ============ 弹窗 ============
let md=[],mt='';
function showModal(t,d,tp){md=d;mt=tp;document.getElementById('modalTitle').textContent=t;if(d.length>0)renderMI(d);document.getElementById('modalOverlay').classList.add('show');document.getElementById('modalSearch').value='';setTimeout(()=>document.getElementById('modalSearch').focus(),100);}
function closeModal(){document.getElementById('modalOverlay').classList.remove('show');}
function renderMI(items){const b=document.getElementById('modalBody');if(items.length===0)return;b.innerHTML=items.map(i=>{if(mt==='poems')return '<div class="poem-card"><div class="poem-title">《'+i.title+'》</div><div class="poem-text">'+i.text+'</div></div>';return '<div class="modal-item" onclick="closeModal();searchAndFocus(\''+i.name+'\')"><b>'+i.name+'</b> — '+i.dir+' '+i.weight+'次</div>';}).join('');}
document.getElementById('modalSearch').addEventListener('input',function(){const q=this.value.trim();if(!q){renderMI(md);return;}renderMI(md.filter(i=>mt==='poems'?(i.title.includes(q)||i.text.includes(q)):i.name.includes(q)));});
document.getElementById('modalOverlay').addEventListener('click',e=>{if(e.target===document.getElementById('modalOverlay'))closeModal();});
function showPoemsModal(n){const d=nodeMap.get(n);if(!d)return;showModal(n+' 的诗作 ('+(d.poemCount||0)+'首)',d.poems||[],'poems');}
function showRelationsModal(n,dir){const d=nodeMap.get(n);if(!d)return;const r=getRelations(d);let f=r,t=n+' 的社交关系';if(dir==='out'){f=r.filter(r=>r.dir==='赠诗给');t=n+' 赠诗给...';}if(dir==='in'){f=r.filter(r=>r.dir==='收到赠诗');t='赠诗给 '+n+' 的人...';}showModal(t+' ('+f.length+'人)',f,'relations');}

// ============ 诗人故事 ============
function showStory(name) {
    const d = nodeMap.get(name);
    if (!d) return;

    const rels = getRelations(d);
    const outRels = rels.filter(r => r.dir === '赠诗给').slice(0, 10);
    const inRels = rels.filter(r => r.dir === '收到赠诗').slice(0, 10);
    const ta = d.textAnalysis;
    const poems = (d.poems || []).slice(0, 5);

    // 生命时间线
    const birth = d.birthYear || '?';
    const death = d.deathYear || '?';
    const age = d.deathAge || '';
    const lifeSpan = (d.birthYear && d.deathYear) ? d.deathYear - d.birthYear : 60;
    const lifePercent = Math.min(100, Math.max(10, lifeSpan / 80 * 100));

    let h = '<div class="story-header">';
    h += '<h1>' + name + '</h1>';
    h += '<div class="story-subtitle">' + d.period;
    if (d.female) h += ' · ♀';
    if (d.place) h += ' · ' + d.place;
    h += '</div>';
    h += '<div class="story-bio">';
    if (d.birthYear) h += '生于 ' + d.birthYear + ' 年';
    if (d.deathYear) h += '，卒于 ' + d.deathYear + ' 年';
    if (d.deathAge) h += '，享年 ' + d.deathAge + ' 岁';
    h += '</div></div>';

    // 时间线
    h += '<div class="story-timeline"><div class="story-timeline-bar">';
    h += '<div class="story-timeline-fill" style="width:' + lifePercent + '%"></div>';
    h += '<span class="story-timeline-label left">' + birth + ' 出生</span>';
    if (d.birthYear && d.deathYear) {
        const mid = Math.round((d.birthYear + d.deathYear) / 2);
        h += '<span class="story-timeline-label center">' + mid + '</span>';
    }
    h += '<span class="story-timeline-label right">' + death + ' 去世</span>';
    h += '</div></div>';

    // 数据概览
    h += '<div class="story-stats">';
    h += '<div class="story-stat"><div class="num">' + (d.poemCount || 0) + '</div><div class="label">首诗</div></div>';
    h += '<div class="story-stat"><div class="num">' + d.outDegree + '</div><div class="label">赠出</div></div>';
    h += '<div class="story-stat"><div class="num">' + d.inDegree + '</div><div class="label">收到</div></div>';
    h += '<div class="story-stat"><div class="num">' + rels.length + '</div><div class="label">社交关系</div></div>';
    h += '</div>';

    // 社交网络
    if (rels.length > 0) {
        h += '<div class="story-section"><h2>社交网络</h2><div class="story-rel-grid">';
        if (outRels.length > 0) {
            h += '<div class="story-rel-card"><h4 style="color:#e74c3c">赠出诗给</h4>';
            outRels.forEach(r => {
                h += '<div class="story-rel-item" onclick="closeStory();searchAndFocus(\'' + r.name + '\')"><span>' + r.name + '</span><span>' + r.weight + ' 次</span></div>';
            });
            h += '</div>';
        }
        if (inRels.length > 0) {
            h += '<div class="story-rel-card"><h4 style="color:#3498db">收到赠诗</h4>';
            inRels.forEach(r => {
                h += '<div class="story-rel-item" onclick="closeStory();searchAndFocus(\'' + r.name + '\')"><span>' + r.name + '</span><span>' + r.weight + ' 次</span></div>';
            });
            h += '</div>';
        }
        h += '</div></div>';
    }

    // 代表诗作
    if (poems.length > 0) {
        h += '<div class="story-section"><h2>代表诗作</h2>';
        poems.forEach(p => {
            h += '<div class="poem-card"><div class="poem-title">《' + p.title + '》</div><div class="poem-text">' + p.text + '</div></div>';
        });
        if ((d.poemCount || 0) > 5) {
            h += '<div style="text-align:center;margin-top:8px"><button class="story-btn" onclick="closeStory();showPoemsModal(\'' + d.id + '\')">查看全部 ' + d.poemCount + ' 首 →</button></div>';
        }
        h += '</div>';
    }

    // 文本分析
    if (ta) {
        if (ta.topWords && ta.topWords.length > 0) {
            h += '<div class="story-section"><h2>高频词</h2><div class="story-word-cloud">';
            ta.topWords.forEach(w => {
                h += '<span class="story-word-tag">' + w.word + '<span class="cnt">' + w.count + '</span></span>';
            });
            h += '</div></div>';
        }

        if (ta.places && ta.places.length > 0) {
            h += '<div class="story-section"><h2>诗中地名</h2><div class="story-place-list">';
            ta.places.forEach(p => {
                h += '<span class="story-place-tag">' + p.place + '<span class="cnt">' + p.count + ' 次</span></span>';
            });
            h += '</div></div>';
        }

        if (ta.imagery && ta.imagery.length > 0) {
            h += '<div class="story-section"><h2>高频意象</h2><div class="story-imagery-list">';
            ta.imagery.forEach(w => {
                h += '<span class="story-imagery-tag">' + w.word + '<span class="cnt">' + w.count + ' 次</span></span>';
            });
            h += '</div></div>';
        }
    }

    // 数据洞察
    h += '<div class="story-section"><h2>数据洞察</h2><div class="story-insight">';
    h += '<p>' + name + '是' + d.period + '诗人';
    if (d.poemCount > 0) h += '，共有 <b>' + d.poemCount + '</b> 首诗作传世';
    if (rels.length > 0) h += '，与 <b>' + rels.length + '</b> 位诗人有赠诗关系';
    h += '。</p>';
    if (d.outDegree > 0 && d.inDegree > 0) {
        const ratio = (d.outDegree / d.inDegree).toFixed(1);
        h += '<p>赠出与收到的比例为 ' + ratio + ':1';
        if (ratio > 1.5) h += '，说明 ' + name + ' 是一位主动社交的诗人';
        else if (ratio < 0.7) h += '，说明 ' + name + ' 受到其他诗人的广泛关注';
        else h += '，说明 ' + name + ' 的社交关系较为均衡';
        h += '。</p>';
    }
    if (ta && ta.places && ta.places.length > 0) {
        h += '<p>在诗作中提及最多的地名是 <b>' + ta.places[0].place + '</b>（' + ta.places[0].count + ' 次）';
        if (ta.places.length > 1) h += '，其次是 <b>' + ta.places[1].place + '</b>（' + ta.places[1].count + ' 次）';
        h += '。</p>';
    }
    if (ta && ta.topWords && ta.topWords.length > 0) {
        h += '<p>诗作中出现最多的词语是 <b>' + ta.topWords[0].word + '</b>（' + ta.topWords[0].count + ' 次）';
        if (ta.topWords.length > 1) h += '和 <b>' + ta.topWords[1].word + '</b>（' + ta.topWords[1].count + ' 次）';
        h += '。</p>';
    }
    h += '</div>';

    // 操作按钮
    h += '<div class="story-actions">';
    h += '<button class="story-btn primary" onclick="closeStory();searchAndFocus(\'' + d.id + '\')">在网络图中探索</button>';
    h += '<button class="story-btn" onclick="shareStory(\'' + d.id + '\')">分享此页面</button>';
    h += '</div>';

    document.getElementById('storyContent').innerHTML = h;
    document.getElementById('storyOverlay').classList.add('show');
    history.replaceState(null, '', '#story/' + encodeURIComponent(name));
}

function closeStory() {
    document.getElementById('storyOverlay').classList.remove('show');
    history.replaceState(null, '', location.pathname);
}

function shareStory(name) {
    const url = location.origin + location.pathname + '#story/' + encodeURIComponent(name);
    navigator.clipboard.writeText(url).then(() => alert('链接已复制！')).catch(() => {});
}

// URL 路由支持 story
function handleStoryHash() {
    const hash = location.hash;
    if (hash.startsWith('#story/')) {
        const name = decodeURIComponent(hash.slice(7));
        if (nodeMap.has(name)) setTimeout(() => showStory(name), 500);
    }
}
handleStoryHash();

// ============ 引导 ============
function closeOnboarding(){document.getElementById('onboarding').classList.remove('show');localStorage.setItem('tpn_visited','1');}
if(!localStorage.getItem('tpn_visited'))setTimeout(()=>document.getElementById('onboarding').classList.add('show'),500);

// ============ 自适应 ============
window.addEventListener('resize',()=>{const w=container.clientWidth,h=container.clientHeight;svg.attr('width',w).attr('height',h);simulation.force('center',d3.forceCenter(w/2,h/2));simulation.alpha(0.1).restart();});
"""

if __name__ == '__main__':
    build()
