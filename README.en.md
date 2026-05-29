# Tang Poetry Network

> 1,381 poets · 8,259 gift-poem relationships · 57,607 poems · Interactive exploration

Visualize the social network of Tang Dynasty poets through their gift-poem relationships. Who wrote poems to whom? What's the shortest path between any two poets? What stories does the data tell?

🏮 **Live Demo:** https://mengyuchun.github.io/tang-poetry-network/

## Features

### Three Views
| 🕸️ Network | 🗺️ Map | 📊 Statistics |
|:---:|:---:|:---:|
| D3.js force graph | Amap (Chinese tiles) | Chart.js charts |
| Drag to explore | Timeline animation | Distribution · TOP 20 |

### Core Features
- **📖 Poet Story** — Select a poet, auto-generate a data story (word frequency, place names, imagery analysis)
- **🔍 Full-text Search** — Search by poet name, poem title, or poem content
- **🔗 Poet Connection Path** — Find the shortest relationship chain between any two poets
- **📅 Daily Poet** — Daily recommendation of a poet and their representative works
- **🎲 Random Poet** — Random exploration
- **🌙 Dark Mode** — One-click toggle
- **📷 Screenshot** — Save current view as PNG
- **🗺️ Timeline Animation** — Slide time window to watch geographic distribution change
- **⌨️ Keyboard Shortcuts** — `/` search · `Tab` switch view · `Esc` close

### Poet Story Page
Click any poet → "📖 View Story" → Auto-generates:

| Section | Content |
|---------|---------|
| Life Timeline | Birth/death year visualization |
| Data Overview | Poem count, sent/received |
| Social Network | Top 10 sent/received |
| Representative Poems | First 5 full text |
| Top Words | jieba segmentation TOP 10 |
| Place Names | Tang dynasty place dictionary |
| Imagery | Moon, wind, flower, snow, wine... |
| Data Insight | Auto-generated narrative |

## Usage

**Zero dependencies, just download and open:**

1. Download [`index.html`](index.html) (~13MB, all data embedded)
2. Double-click to open (or drag into browser)
3. Start exploring

> Requires internet for D3.js, Leaflet.js, Chart.js (CDN). Data is embedded.

## Data Sources

| Source | Content | Origin |
|--------|---------|--------|
| CBDB | 8,259 Tang gift-poem relationships + birth/death years + gender + coordinates | Harvard University |
| chinese-poetry | 57,607 Tang poems (full text) | Open source community |

## Keyboard Shortcuts

| Key | Function |
|-----|----------|
| `/` | Focus search box |
| `Tab` | Switch view (Network/Map/Stats) |
| `Esc` | Close panel/modal/story |
| `↑` `↓` | Navigate search results |
| `Enter` | Select search result |

## Local Development

```bash
# Requires CBDB database (latest.db) and conda environment
conda activate data_env
pip install -r requirements.txt

# Extract data (requires latest.db)
python extract_data.py

# Build HTML
python build_html.py

# Output in dist/index.html
```

## Tech Stack

- **D3.js v7** — Force-directed network graph
- **Leaflet.js** — Interactive map (Amap Chinese tiles)
- **Chart.js** — Statistics charts
- **html2canvas** — Screenshot feature
- **jieba** — Chinese text segmentation (text analysis)
- **Single HTML file** — Data embedded, zero dependencies

## License

MIT

---

If you find this interesting, please give it a Star ⭐
