# 唐诗社交网络 | Tang Poetry Network

> 1,381 位诗人 · 8,259 条赠诗关系 · 57,607 首唐诗 · 交互式探索

用数据揭示唐代诗人的社交网络 —— 谁给谁写过诗？两位诗人之间有怎样的关系链？

🏮 **在线体验：** https://mengyuchun.github.io/tang-poetry-network/

## 功能一览

### 三视图
| 🕸️ 网络图 | 🗺️ 地图 | 📊 统计 |
|:---:|:---:|:---:|
| D3.js 力导向图 | Leaflet.js 地理分布 | Chart.js 交互图表 |
| 拖拽探索关系 | 诗人籍贯标注 | 朝代分布 · TOP 20 |

### 核心功能
- **🔍 全文搜索** — 搜索诗人名、诗题、诗句（如「春眠不觉晓」）
- **🔗 诗人关系路径** — 输入两位诗人，找到最短关系链（如李白→杜甫）
- **📅 每日一诗** — 每天推荐一位诗人及其代表作
- **🎲 随机诗人** — 随机跳转探索
- **🌙 深色模式** — 一键切换
- **📷 截图分享** — 一键保存当前视图为图片
- **⌨️ 快捷键** — `/` 搜索 · `Tab` 切换视图 · `Esc` 关闭

### 视觉设计
- 水墨古风配色（深色模式支持）
- 节点大小 = 诗作数量
- 连线粗细 = 赠诗次数
- 核心诗人节点脉冲发光（李白、杜甫、白居易等）
- 按时期着色：初唐(青) · 盛唐(红) · 中唐(靛) · 晚唐(橙)

## 使用

**零依赖，下载即用：**

1. 下载 [`index.html`](index.html)（约 12MB，含全部数据）
2. 双击打开（或拖入浏览器）
3. 开始探索

> 需要联网加载 D3.js、Leaflet.js、Chart.js（CDN），数据已内嵌。

## 数据来源

| 数据源 | 内容 | 来源 |
|--------|------|------|
| CBDB | 8,259 条唐代赠诗关系 | Harvard University |
| chinese-poetry | 57,607 首唐诗全文 | 开源社区 |

## 数据发现

**社交之王：** 白居易拥有 306 条赠诗关系，是唐代文人网络中最活跃的节点。

**诗作之王：** 白居易存诗 3,009 首，杜甫 1,489 首，李白 1,207 首。

**李白的朋友圈：** 李白赠诗给杜甫、贺知章、高适、孟浩然等人。

**关系路径示例：**
- 李白 → 杜甫（直接关系）
- 王维 → 李商隐（需通过中间人连接）

## 快捷键

| 按键 | 功能 |
|------|------|
| `/` | 聚焦搜索框 |
| `Tab` | 切换视图（网络/地图/统计） |
| `Esc` | 关闭面板/弹窗 |
| `↑` `↓` | 搜索结果导航 |
| `Enter` | 选择搜索结果 |

## 技术栈

- **D3.js v7** — 力导向网络图
- **Leaflet.js** — 交互式地图
- **Chart.js** — 统计图表
- **html2canvas** — 截图功能
- **单文件 HTML** — 数据内嵌，零依赖

## 本地开发

```bash
# 需要 CBDB 数据库 (latest.db) 和 conda 环境
conda activate data_env

# 提取数据（需要 latest.db）
python extract_data.py

# 构建 HTML
python build_html.py

# 输出在 dist/index.html
```

## 效果演示


<img width="3071" height="1919" alt="首页引导" src="https://github.com/user-attachments/assets/a481a359-3975-497c-8c8d-1d04d9a12dda" />
1. **网络图全景** — 缩小到能看到整体结构，核心诗人清晰可见
<img width="3058" height="1644" alt="网络图" src="https://github.com/user-attachments/assets/b3f05d2c-3020-4b15-ab82-a73fb1fd179e" /> 
2. **搜索「诗人名」或「诗句」** — 展示全文搜索结果
<img width="3071" height="1640" alt="搜索功能" src="https://github.com/user-attachments/assets/377acc90-42ac-4c2d-988a-9cefc93773f6" />
3. **李白→杜甫关系路径** — 展示两位诗人直接的直接或间接关系
<img width="3072" height="1752" alt="唐诗社交网络_2026-05-29" src="https://github.com/user-attachments/assets/f8ab1f20-5d68-4c53-9d9d-3b00e4c32a2f" />
4. **统计面板** — 展示图表和数据
<img width="3049" height="1639" alt="统计图" src="https://github.com/user-attachments/assets/96929d99-6aac-47a0-b371-dffc3a0b2755" />
5. **地图视图** — 展示地理分布
<img width="3071" height="1639" alt="地图" src="https://github.com/user-attachments/assets/ace52569-1712-4976-ba39-addeb0fd0f90" />
6. **深色模式** — 暗色主题效果


## License

MIT

---

如果觉得有趣，请给个 Star ⭐
