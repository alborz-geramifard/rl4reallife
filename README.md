# Reinforcement Learning for Real Life workshop series (2019–2022)

Archive site for the four editions of the **RL for Real Life** workshop (ICML 2019, virtual 2020, ICML 2021, NeurIPS 2022), rebuilt from the original Google Sites pages.

- `2019.html` … `2022.html` – one page per edition; `index.html` redirects to 2022
- `data/rl4reallife.json` – all content (intro, schedule, talks, panels, papers, call for papers, committees, organizers, links)
- `assets/people/` – speaker, panelist and organizer photos; `assets/venues/` – hero images
- `tools/build.py` – regenerates the HTML from the JSON

```sh
python3 tools/build.py
python3 -m http.server 8791   # preview at http://127.0.0.1:8791/
```

Paper PDFs are linked to their original locations (OpenReview, arXiv, Google Drive); they are not stored in this repo.
