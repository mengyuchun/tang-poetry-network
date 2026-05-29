# 唐诗社交网络 | Tang Poetry Network

> 1,381 位诗人 · 8,259 条赠诗关系 · 57,607 首唐诗 · 交互式探索

用数据揭示唐代诗人的社交网络 —— 谁给谁写过诗？两位诗人之间有怎样的关系链？诗人一生写了哪些诗？

🏮 **在线体验：** https://mengyuchun.github.io/tang-poetry-network/

## 功能一览

### 三视图
| 🕸️ 网络图 | 🗺️ 地图 | 📊 统计与洞察 |
|:---:|:---:|:---:|
| D3.js 力导向图 | 高德中文地图 | Chart.js 交互图表 |
| 拖拽探索关系 | 时间线动画 | 朝代分布 · TOP 20 |

### 核心功能
- **📖 诗人故事** — 选择一位诗人，自动生成数据故事（高频词、地名、意象分析）
- **🔍 全文搜索** — 搜索诗人名、诗题、诗句（如「春眠不觉晓」）
- **🔗 诗人关系路径** — 输入两位诗人，找到最短关系链
- **📅 每日一诗** — 每天推荐一位诗人及代表作
- **🎲 随机诗人** — 随机跳转探索
- **🌙 深色模式** — 一键切换
- **📷 截图分享** — 一键保存当前视图为图片
- **🗺️ 时间线动画** — 滑动时间窗口，观看诗人地理分布随时代变化
- **⌨️ 快捷键** — `/` 搜索 · `Tab` 切换视图 · `Esc` 关闭

### 视觉设计
- 水墨古风配色（深色模式支持）
- 节点大小 = 关系数量
- 连线带箭头，指示赠诗方向
- 点击节点：🔴红色=赠出，🔵蓝色=收到
- 核心诗人节点脉冲发光
- 按时期着色：初唐(青) · 盛唐(红) · 中唐(靛) · 晚唐(橙)

### 诗人故事页面
点击任意诗人 → 「📖 查看故事」→ 自动生成：

| 模块 | 内容 |
|------|------|
| 生命时间线 | 生卒年可视化 |
| 数据概览 | 诗作数、赠出、收到 |
| 社交网络 | 赠出/收到 TOP 10 |
| 代表诗作 | 前 5 首全文 |
| 高频词 | jieba 分词 TOP 10 |
| 诗中地名 | 唐代地名词典匹配 |
| 高频意象 | 月、风、花、雪、酒... |
| 数据洞察 | 自动生成描述文字 |

### 演示预览
-<img width="3071" height="1919" alt="首页引导" src="https://github.com/user-attachments/assets/a481a359-3975-497c-8c8d-1d04d9a12dda" />
-1. **网络图全景** — 缩小到能看到整体结构，核心诗人清晰可见
 -<img width="3058" height="1644" alt="网络图" src="https://github.com/user-attachments/assets/b3f05d2c-3020-4b15-ab82-a73fb1fd179e" />
-2.**诗人及其社会关系、作品** — 点击可查看诗人作品、社交网络连接及全部作品
-<img width="3058" height="1644" alt="白居易" src="https://github.com/user-attachments/assets/4b779f9c-f75c-47f4-840b-c2c2bd142409" />
-3. **搜索「诗人名」或「诗句」** — 展示全文搜索结果
-<img width="958" height="802" alt="搜索栏" src="https://github.com/user-attachments/assets/0e02a969-4fbd-44b0-b1a8-5bebc766c415" />
-4. **李白→杜甫关系路径** — 展示两位诗人直接的直接或间接关系
-<img width="3071" height="1640" alt="搜索功能" src="https://github.com/user-attachments/assets/377acc90-42ac-4c2d-988a-9cefc93773f6" />
 -6. **统计面板** — 展示图表和数据
-<img width="3049" height="1639" alt="统计图" src="https://github.com/user-attachments/assets/96929d99-6aac-47a0-b371-dffc3a0b2755" />
-7. **地图视图** — 展示地理分布
-<img width="3071" height="1639" alt="地图" src="https://github.com/user-attachments/assets/ace52569-1712-4976-ba39-addeb0fd0f90" />
-8. **深色模式** — 暗色主题效果

## 使用

**零依赖，下载即用：**

1. 下载 [`index.html`](index.html)（约 13MB，含全部数据）
2. 双击打开（或拖入浏览器）
3. 开始探索

> 需要联网加载 D3.js、Leaflet.js、Chart.js（CDN），数据已内嵌。

## 数据来源

| 数据源 | 内容 | 来源 |
|--------|------|------|
| CBDB | 8,259 条唐代赠诗关系 + 生卒年 + 性别 + 地理坐标 | Harvard University |
| chinese-poetry | 57,607 首唐诗全文 | 开源社区 |

## 快捷键

| 按键 | 功能 |
|------|------|
| `/` | 聚焦搜索框 |
| `Tab` | 切换视图（网络/地图/统计） |
| `Esc` | 关闭面板/弹窗/故事 |
| `↑` `↓` | 搜索结果导航 |
| `Enter` | 选择搜索结果 |

## 本地开发

```bash
# 需要 CBDB 数据库 (latest.db) 和 conda 环境
conda activate data_env
pip install -r requirements.txt

# 提取数据（需要 latest.db）
python extract_data.py

# 构建 HTML
python build_html.py

# 输出在 dist/index.html
```

## 技术栈

- **D3.js v7** — 力导向网络图
- **Leaflet.js** — 交互式地图（高德中文瓦片）
- **Chart.js** — 统计图表
- **html2canvas** — 截图功能
- **jieba** — 中文分词（文本分析）
- **单文件 HTML** — 数据内嵌，零依赖

## License

MIT

---

如果觉得有趣，请给个 Star ⭐
