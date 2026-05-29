"""
唐诗社交网络 — 数据提取脚本
合并 CBDB 赠诗关系与 chinese-poetry 唐诗数据
"""
import sqlite3
import pandas as pd
import json
import os
import glob
import re
from collections import Counter
import jieba

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'latest.db')
POETRY_CACHE = os.path.join(os.path.dirname(__file__), '..', 'poetry_cache')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'dist')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 时期划分（按年号大致划分）
TANG_PERIODS = [
    (618, 713, '初唐'), (713, 766, '盛唐'), (766, 836, '中唐'), (836, 907, '晚唐')
]
PERIOD_COLORS = {'初唐': '#61a0a8', '盛唐': '#c23531', '中唐': '#2f4554', '晚唐': '#d48265'}

# 停用词（常见虚词和无意义词）
STOP_WORDS = set('的了在是我有和人这中大为上个国不以到说时要就出会也年对自其')
STOP_WORDS.update(['一个', '不能', '可以', '不知', '何人', '何处', '今日', '昨日', '明日',
                    '万里', '千里', '百年', '千秋', '万古', '无人', '不知', '不见', '不得',
                    '何以', '如此', '当年', '此时', '此地', '此中', '君不', '不见'])

# 唐代常见地名
TANG_PLACES = [
    '长安', '洛阳', '成都', '杭州', '苏州', '扬州', '金陵', '南京', '江陵', '荆州',
    '岳阳', '洞庭', '蜀道', '蜀中', '江南', '江北', '岭南', '关中', '中原', '河北',
    '河南', '山东', '山西', '陕西', '甘肃', '凉州', '敦煌', '西域', '天山', '黄河',
    '长江', '淮河', '汉水', '渭水', '泰山', '华山', '衡山', '嵩山', '峨眉', '庐山',
    '黄山', '天台', '终南', '太行', '武陵', '桃花源', '赤壁', '姑苏', '会稽', '越州',
    '温州', '福州', '泉州', '广州', '桂林', '昆明', '大理', '吐蕃', '南诏', '高丽',
    '新罗', '日本', '蓬莱', '瀛洲', '瑶池', '昆仑', '崆峒', '青城', '峨嵋', '巫山',
    '三峡', '瞿塘', '潇湘', '九嶷', '苍梧', '南海', '西湖', '太湖', '鄱阳', '洪州',
    '宣州', '池州', '润州', '常州', '湖州', '越州', '衢州', '歙州', '袁州', '吉州',
    '潭州', '衡州', '永州', '柳州', '连州', '潮州', '崖州', '儋州', '雷州', '琼州',
]

# 唐诗意象词
IMAGERY_WORDS = [
    '月', '风', '花', '雪', '雨', '云', '霜', '露', '烟', '霞',
    '山', '水', '江', '河', '湖', '海', '溪', '泉', '潭', '瀑',
    '酒', '茶', '琴', '棋', '书', '剑', '笛', '箫', '笙', '鼓',
    '春', '夏', '秋', '冬', '朝', '暮', '夜', '晓', '昏', '晨',
    '松', '竹', '梅', '兰', '菊', '荷', '桃', '柳', '桂', '枫',
    '雁', '鹤', '莺', '燕', '蝉', '蝶', '马', '龙', '凤', '虎',
    '梦', '泪', '愁', '恨', '思', '情', '心', '魂', '影', '声',
    '天', '地', '日', '星', '光', '影', '色', '香', '寒', '暖',
]


def analyze_poems(poems):
    """分析诗作的高频词、地名、意象"""
    if not poems:
        return {'topWords': [], 'places': [], 'imagery': []}

    all_text = '\n'.join(p.get('text', '') for p in poems)

    # 分词
    words = jieba.lcut(all_text)
    # 过滤：去掉停用词、单字（保留意象词中的单字）、数字
    filtered = []
    for w in words:
        w = w.strip()
        if len(w) == 0:
            continue
        if w in STOP_WORDS:
            continue
        if len(w) == 1 and w not in IMAGERY_WORDS:
            continue
        if re.match(r'^\d+$', w):
            continue
        filtered.append(w)

    # 高频词 TOP 10
    word_counts = Counter(filtered).most_common(10)
    top_words = [{'word': w, 'count': c} for w, c in word_counts]

    # 地名匹配
    place_counts = Counter()
    for place in TANG_PLACES:
        cnt = all_text.count(place)
        if cnt > 0:
            place_counts[place] = cnt
    places = [{'place': p, 'count': c} for p, c in place_counts.most_common(10)]

    # 意象词匹配
    imagery_counts = Counter()
    for word in IMAGERY_WORDS:
        cnt = all_text.count(word)
        if cnt > 0:
            imagery_counts[word] = cnt
    imagery = [{'word': w, 'count': c} for w, c in imagery_counts.most_common(10)]

    return {'topWords': top_words, 'places': places, 'imagery': imagery}


def load_poems():
    """加载唐诗数据"""
    poems_by_author = {}
    for fpath in sorted(glob.glob(os.path.join(POETRY_CACHE, 'poet.tang.*.json'))):
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                for p in json.load(f):
                    name = p.get('author', '')
                    if not name:
                        continue
                    if name not in poems_by_author:
                        poems_by_author[name] = []
                    poems_by_author[name].append({
                        'title': p.get('title', ''),
                        'paragraphs': p.get('paragraphs', [])
                    })
        except Exception as e:
            print(f"  跳过 {fpath}: {e}")
    return poems_by_author


def load_cbdb_edges():
    """从 CBDB 提取唐代赠诗关系"""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("""
        SELECT b1.c_name_chn AS source, b2.c_name_chn AS target,
               b1.c_birthyear AS src_birth, b2.c_birthyear AS tgt_birth,
               b1.c_deathyear AS src_death, b2.c_deathyear AS tgt_death,
               a.c_text_title
        FROM ASSOC_DATA a
        JOIN BIOG_MAIN b1 ON a.c_personid = b1.c_personid
        JOIN BIOG_MAIN b2 ON a.c_assoc_id = b2.c_personid
        WHERE a.c_assoc_code = 437
          AND b1.c_dy = 6
          AND b1.c_personid != b2.c_personid
    """, conn)

    # 获取诗人地理坐标
    all_ids = set()
    for _, row in df.iterrows():
        pass  # 先用名字匹配，坐标后续补充

    # 补充坐标
    poet_coords = pd.read_sql_query("""
        SELECT b.c_name_chn, a.x_coord, a.y_coord, a.c_name_chn AS place_name
        FROM BIOG_MAIN b
        JOIN ADDR_CODES a ON b.c_index_addr_id = a.c_addr_id
        WHERE b.c_dy = 6 AND a.x_coord IS NOT NULL
    """, conn)
    conn.close()

    # 去重（同一对诗人可能有多条赠诗记录）
    edge_counts = df.groupby(['source', 'target']).size().reset_index(name='weight')
    # 合并 c_text_title
    edge_titles = df.groupby(['source', 'target'])['c_text_title'].apply(
        lambda x: [t for t in x if pd.notna(t)][:3]
    ).reset_index()
    edges = edge_counts.merge(edge_titles, on=['source', 'target'], how='left')

    return edges, poet_coords


def get_period(birth_year):
    """根据出生年判断时期"""
    if pd.isna(birth_year) or birth_year <= 0:
        return '未知'
    for start, end, name in TANG_PERIODS:
        if start <= birth_year < end:
            return name
    return '未知'


def build_nodes(edges, poems_by_author, poet_coords):
    """构建节点数据"""
    # 统计每个诗人的出度和入度
    out_deg = edges.groupby('source')['weight'].sum().to_dict()
    in_deg = edges.groupby('target')['weight'].sum().to_dict()

    all_poets = set(edges['source']) | set(edges['target'])

    # 坐标映射
    coord_map = {}
    for _, row in poet_coords.iterrows():
        name = row['c_name_chn']
        if name not in coord_map:
            coord_map[name] = {
                'x': row['x_coord'], 'y': row['y_coord'],
                'place': row['place_name']
            }

    nodes = []
    for name in all_poets:
        poem_count = len(poems_by_author.get(name, []))
        out_d = out_deg.get(name, 0)
        in_d = in_deg.get(name, 0)

        # 保存全部诗作
        poet_poems = poems_by_author.get(name, [])
        representative = []
        for p in poet_poems:
            text = '\n'.join(p['paragraphs'])
            representative.append({'title': p['title'], 'text': text})

        coord = coord_map.get(name, {})
        period = '未知'  # 简化：后续通过关系推断

        # 文本分析（仅对有诗作的诗人）
        text_analysis = analyze_poems(representative) if poem_count > 0 else None

        nodes.append({
            'id': name,
            'poem_count': poem_count,
            'out_degree': int(out_d),
            'in_degree': int(in_d),
            'total_degree': int(out_d + in_d),
            'period': period,
            'lng': coord.get('x'),
            'lat': coord.get('y'),
            'place': coord.get('place'),
            'poems': representative,
            'textAnalysis': text_analysis
        })

    # 获取生卒年和性别
    conn = sqlite3.connect(DB_PATH)
    bio_data = pd.read_sql_query("""
        SELECT c_name_chn, c_birthyear, c_deathyear, c_death_age, c_female
        FROM BIOG_MAIN
        WHERE c_dy = 6
    """, conn)
    conn.close()
    bio_map = {}
    for _, row in bio_data.iterrows():
        bio_map[row['c_name_chn']] = {
            'birth': row['c_birthyear'],
            'death': row['c_deathyear'],
            'age': row['c_death_age'],
            'female': row['c_female']
        }

    for node in nodes:
        bio = bio_map.get(node['id'], {})
        birth = bio.get('birth')
        node['period'] = get_period(birth)
        node['birth_year'] = int(birth) if birth and birth > 0 else None
        node['death_year'] = int(bio['death']) if bio.get('death') and bio['death'] > 0 else None
        node['death_age'] = int(bio['age']) if bio.get('age') and bio['age'] > 0 else None
        node['female'] = bool(bio.get('female'))

    return nodes


def main():
    print("加载唐诗数据...")
    poems_by_author = load_poems()
    print(f"  诗人数: {len(poems_by_author)}, 诗作数: {sum(len(v) for v in poems_by_author.values())}")

    print("提取 CBDB 赠诗关系...")
    edges, poet_coords = load_cbdb_edges()
    print(f"  边数: {len(edges)}")

    print("构建节点数据...")
    nodes = build_nodes(edges, poems_by_author, poet_coords)
    print(f"  节点数: {len(nodes)}")

    # 统计有诗作的节点
    with_poems = [n for n in nodes if n['poem_count'] > 0]
    print(f"  有诗作的节点: {len(with_poems)}")

    # 保存 JSON
    # 节点
    nodes_out = []
    for n in nodes:
        nodes_out.append({
            'id': n['id'],
            'poemCount': n['poem_count'],
            'outDegree': n['out_degree'],
            'inDegree': n['in_degree'],
            'totalDegree': n['total_degree'],
            'period': n['period'],
            'lng': n['lng'],
            'lat': n['lat'],
            'place': n['place'],
            'birthYear': n.get('birth_year'),
            'deathYear': n.get('death_year'),
            'deathAge': n.get('death_age'),
            'female': n.get('female', False),
            'poems': n['poems'],
            'textAnalysis': n.get('textAnalysis')
        })

    # 边
    edges_out = []
    for _, row in edges.iterrows():
        titles = row.get('c_text_title', [])
        if isinstance(titles, list):
            titles = [t for t in titles if t]
        else:
            titles = []
        edges_out.append({
            'source': row['source'],
            'target': row['target'],
            'weight': int(row['weight']),
            'titles': titles
        })

    # 统计信息
    stats = {
        'total_poets': len(nodes),
        'total_edges': len(edges_out),
        'total_poems': sum(len(v) for v in poems_by_author.values()),
        'matched_poets': len(with_poems)
    }

    # 朝代分布统计
    period_dist = {}
    for n in nodes_out:
        p = n['period']
        period_dist[p] = period_dist.get(p, 0) + 1

    # TOP 20 最具影响力诗人（按总连接度）
    top_poets = sorted(nodes_out, key=lambda x: x['totalDegree'], reverse=True)[:20]
    top_poets_out = [{'id': p['id'], 'period': p['period'], 'poemCount': p['poemCount'],
                      'outDegree': p['outDegree'], 'inDegree': p['inDegree'],
                      'totalDegree': p['totalDegree']} for p in top_poets]

    # 诗人时间线（有出生年的诗人）
    timeline = []
    for n in nodes_out:
        if n['birthYear'] and n['birthYear'] > 600 and n['birthYear'] < 910:
            real_death = n.get('deathYear')
            est_death = n['birthYear'] + max(30, min(90, n['poemCount'] // 10 + 40)) if not real_death else None
            timeline.append({'id': n['id'], 'birthYear': n['birthYear'],
                           'deathYear': real_death or est_death,
                           'estimated': real_death is None,
                           'period': n['period'], 'poemCount': n['poemCount']})
    timeline.sort(key=lambda x: x['birthYear'])

    # 网络统计
    degrees = [n['totalDegree'] for n in nodes_out]
    isolated = sum(1 for d in degrees if d == 0)
    avg_degree = sum(degrees) / len(degrees) if degrees else 0

    network_stats = {
        'avgDegree': round(avg_degree, 1),
        'isolatedNodes': isolated,
        'maxDegree': max(degrees) if degrees else 0,
        'density': round(len(edges_out) * 2 / (len(nodes_out) * (len(nodes_out) - 1)), 6) if len(nodes_out) > 1 else 0
    }

    with open(os.path.join(OUTPUT_DIR, 'data.json'), 'w', encoding='utf-8') as f:
        json.dump({
            'nodes': nodes_out, 'edges': edges_out, 'stats': stats,
            'periodDist': period_dist, 'topPoets': top_poets_out,
            'timeline': timeline[:500], 'networkStats': network_stats
        }, f, ensure_ascii=False)

    print(f"\n数据已保存: {OUTPUT_DIR}/data.json")
    print(f"  节点: {len(nodes_out)}, 边: {len(edges_out)}")
    print(f"  统计: {stats}")
    print(f"  朝代分布: {period_dist}")
    print(f"  网络统计: {network_stats}")


if __name__ == '__main__':
    main()
