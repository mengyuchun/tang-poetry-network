"""
唐诗社交网络 — 数据提取脚本
合并 CBDB 赠诗关系与 chinese-poetry 唐诗数据
"""
import sqlite3
import pandas as pd
import json
import os
import glob

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'latest.db')
POETRY_CACHE = os.path.join(os.path.dirname(__file__), '..', 'poetry_cache')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'dist')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 时期划分（按年号大致划分）
TANG_PERIODS = [
    (618, 713, '初唐'), (713, 766, '盛唐'), (766, 836, '中唐'), (836, 907, '晚唐')
]
PERIOD_COLORS = {'初唐': '#61a0a8', '盛唐': '#c23531', '中唐': '#2f4554', '晚唐': '#d48265'}


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
            'poems': representative
        })

    # 通过出生年推断时期
    # 需要从 CBDB 获取出生年
    conn = sqlite3.connect(DB_PATH)
    birth_data = pd.read_sql_query("""
        SELECT c_name_chn, c_birthyear FROM BIOG_MAIN
        WHERE c_dy = 6 AND c_birthyear IS NOT NULL AND c_birthyear > 0
    """, conn)
    conn.close()
    birth_map = dict(zip(birth_data['c_name_chn'], birth_data['c_birthyear']))

    for node in nodes:
        birth = birth_map.get(node['id'])
        node['period'] = get_period(birth)
        node['birth_year'] = int(birth) if birth and birth > 0 else None

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
            'poems': n['poems']
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

    with open(os.path.join(OUTPUT_DIR, 'data.json'), 'w', encoding='utf-8') as f:
        json.dump({'nodes': nodes_out, 'edges': edges_out, 'stats': stats},
                  f, ensure_ascii=False)

    print(f"\n数据已保存: {OUTPUT_DIR}/data.json")
    print(f"  节点: {len(nodes_out)}, 边: {len(edges_out)}")
    print(f"  统计: {stats}")


if __name__ == '__main__':
    main()
