# Tang Poetry Network

> 1,381 poets · 8,259 gift-poem relationships · 57,607 poems · Interactive exploration

Visualize the social network of Tang Dynasty poets through their gift-poem relationships. Who wrote poems to whom? What was Li Bai's social circle like? What's the shortest path between any two poets?

Built with data from [CBDB (China Biographical Database)](https://projects.iq.harvard.edu/cbdb) and [chinese-poetry](https://github.com/chinese-poetry/chinese-poetry).

## ✨ Features

### Three Views
- **🕸️ Network** — D3.js force-directed graph, drag to explore relationships
- **🗺️ Map** — Leaflet.js geographic distribution of poets' hometowns
- **📊 Statistics** — Chart.js interactive charts (era distribution, top 20 influential poets)

### Interactive
- **Full-text search** — Search by poet name, poem title, or poem content
- **Poet connection path** — Find the shortest relationship chain between any two poets
- **Era filtering** — Click legend to toggle Early/High/Mid/Late Tang
- **Detail modals** — Click numbers to view complete poem lists or social connections
- **Random poet** — 🎲 button for random exploration
- **URL routing** — Share links to specific poets

### Design
- Chinese ink-wash aesthetic
- Node size = poem count
- Edge thickness = gift-poem frequency
- Color-coded by era: Early Tang (cyan) · High Tang (red) · Mid Tang (navy) · Late Tang (orange)

## 🚀 Usage

**Zero dependencies, just download and open:**

1. Download [`index.html`](index.html)
2. Double-click to open (or drag into browser)
3. Start exploring

> Requires internet for D3.js, Leaflet.js, Chart.js (CDN). Data is embedded.

**Live demo:** https://mengyuchun.github.io/tang-poetry-network/

## 📊 Data Sources

| Source | Content | Origin |
|--------|---------|--------|
| CBDB | 8,259 Tang gift-poem relationships | Harvard University |
| chinese-poetry | 57,607 Tang poems (full text) | Open source community |

## 🔍 Discoveries

**Social King:** Bai Juyi has 306 gift-poem relationships — the most connected node in the Tang literary network.

**Poetry King:** Bai Juyi has 3,009 surviving poems, Du Fu has 1,489, Li Bai has 1,207.

**Li Bai's Circle:** Li Bai exchanged poems with Du Fu, He Zhizhang, Gao Shi, Meng Haoran, and many others.

## 🛠 Tech Stack

- **D3.js v7** — Force-directed network graph
- **Leaflet.js** — Interactive map
- **Chart.js** — Statistics charts
- **Single HTML file** — Data embedded, zero dependencies

## 📜 License

MIT

---

If you find this interesting, please give it a Star ⭐
