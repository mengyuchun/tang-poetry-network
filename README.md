# 唐诗社交网络 | Tang Poetry Network

> 1,381 位诗人 · 8,259 条赠诗关系 · 57,607 首唐诗 · 交互式探索

用数据揭示唐代诗人的社交网络 —— 谁给谁写过诗？李白的朋友圈是什么样的？杜甫和谁关系最密切？

基于 [CBDB（中国历代人物传记资料库）](https://projects.iq.harvard.edu/cbdb) 的赠诗关系数据与 [chinese-poetry](https://github.com/chinese-poetry/chinese-poetry) 的唐诗全文，打造了一个水墨古风的交互式网络图。

## 使用

**零依赖，下载即用：**

1. 下载 [`index.html`](dist/index.html)
2. 双击打开（或拖入浏览器）
3. 开始探索

> 需要联网加载 D3.js（约 100KB），数据已内嵌在文件中。

## 功能

- **交互式网络图** — 拖拽、缩放、探索诗人关系
- **搜索诗人** — 输入名字，自动定位并高亮
- **点击节点** — 查看诗人时期、代表诗作、社交关系
- **点击连线** — 查看两位诗人的赠诗关系和各自作品
- **水墨古风** — 宣纸纹理背景、楷体字体、传统配色

## 数据来源

| 数据源 | 内容 | 来源 |
|--------|------|------|
| CBDB | 8,259 条唐代赠诗关系 | Harvard University |
| chinese-poetry | 57,607 首唐诗全文 | 开源社区 |

两个数据集通过诗人姓名匹配，共有 **1,381 位诗人** 同时出现在关系数据和诗作数据中。

## 发现

探索数据过程中的一些有趣发现：

**谁写的序最多？**
- 白居易：306 条赠诗关系（社交之王）
- 杜甫：248 条（人缘极好）
- 刘禹锡：201 条
- 李白：164 条

**谁的诗最多？**
- 白居易：3,009 首
- 杜甫：1,489 首
- 李白：1,207 首

**李白的朋友圈：**
李白赠诗给杜甫、贺知章、高适、孟浩然等人，也收到了来自杜甫、韩愈等人的赠诗。

**杜甫的社交网络：**
杜甫与 248 位诗人有赠诗关系，是唐代文人网络中最活跃的节点之一。

## 技术

- **D3.js v7** — 力导向网络图
- **单文件 HTML** — 数据内嵌，零依赖
- **水墨风格** — CSS 模拟宣纸纹理

## 数据处理

如需重新生成数据（需要 CBDB 数据库）：

```bash
conda activate data_env
python extract_data.py    # 从 CBDB + chinese-poetry 提取数据
python build_html.py      # 生成单文件 HTML
```

## 致谢

- [CBDB（China Biographical Database）](https://projects.iq.harvard.edu/cbdb) — Harvard University, Peking University, Academia Sinica
- [chinese-poetry](https://github.com/chinese-poetry/chinese-poetry) — 全唐诗数据
- [D3.js](https://d3js.org/) — 数据可视化库

## License

MIT

---

如果觉得有趣，请给个 Star ⭐
