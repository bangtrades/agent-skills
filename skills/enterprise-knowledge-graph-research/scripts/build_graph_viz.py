#!/usr/bin/env python3
"""Build a self-contained, dependency-free HTML explorer for a compiled graph."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


PAGE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<style>
:root{color-scheme:dark;--bg:#091018;--panel:#111b27;--line:#27384b;--text:#e8eef5;--muted:#92a5ba;--accent:#5dd6c0}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:14px/1.45 ui-sans-serif,system-ui,-apple-system,sans-serif}
header{height:64px;display:flex;align-items:center;gap:16px;padding:12px 18px;border-bottom:1px solid var(--line);background:#0d1621}
h1{font-size:17px;margin:0;white-space:nowrap}.meta{color:var(--muted);font-size:12px}
input,select{background:#0a131d;color:var(--text);border:1px solid var(--line);border-radius:6px;padding:8px 10px}
input{min-width:250px}.layout{display:grid;grid-template-columns:minmax(0,1fr) 360px;height:calc(100vh - 64px)}
.graph{position:relative;min-width:0}canvas{width:100%;height:100%;display:block}.hint{position:absolute;left:14px;bottom:12px;color:var(--muted);font-size:12px}
aside{border-left:1px solid var(--line);background:var(--panel);overflow:auto;padding:18px}h2{font-size:18px;margin:0 0 6px}h3{font-size:13px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin:20px 0 8px}
.pill{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:3px 8px;margin:0 6px 6px 0;font-size:12px}.summary{color:#c8d5e2}.body{white-space:pre-wrap;color:#bcc9d6}
.source{display:block;color:var(--accent);overflow-wrap:anywhere;margin-bottom:7px}.empty{color:var(--muted)}
@media(max-width:900px){.layout{grid-template-columns:1fr}.graph{height:58vh}aside{border-left:0;border-top:1px solid var(--line)}}
</style>
</head>
<body>
<header>
  <div><h1>__TITLE__</h1><div class="meta" id="meta"></div></div>
  <input id="search" type="search" placeholder="Search name, summary, or ID" aria-label="Search graph">
  <select id="track" aria-label="Filter by track"><option value="">All tracks</option></select>
  <select id="type" aria-label="Filter by type"><option value="">All types</option></select>
</header>
<main class="layout">
  <section class="graph"><canvas id="canvas" aria-label="Knowledge graph visualization"></canvas><div class="hint">Click a node for evidence and relations. Visualization contains: __SENSITIVITY__.</div></section>
  <aside id="details"><p class="empty">Select a node.</p></aside>
</main>
<script>
const entities=__ENTITIES__;
const edges=__EDGES__;
const nodes=Object.values(entities).sort((a,b)=>a.id.localeCompare(b.id));
const byId=Object.fromEntries(nodes.map(n=>[n.id,n]));
const palette=['#5dd6c0','#ffbd69','#78a9ff','#d98cff','#ff758f','#8bd450','#f18f01','#4cc9f0','#c5a3ff','#fb7185','#94a3b8'];
const tracks=[...new Set(nodes.map(n=>n.track))].sort();
const types=[...new Set(nodes.map(n=>n.type))].sort();
const colors=Object.fromEntries(tracks.map((t,i)=>[t,palette[i%palette.length]]));
const canvas=document.getElementById('canvas'),ctx=canvas.getContext('2d'),details=document.getElementById('details');
const search=document.getElementById('search'),track=document.getElementById('track'),type=document.getElementById('type');
tracks.forEach(v=>track.add(new Option(v,v)));types.forEach(v=>type.add(new Option(v,v)));
document.getElementById('meta').textContent=`${nodes.length} entities · ${edges.length} directed relations`;
let visible=[],positions={},selected=null;
function escapeHtml(v){const d=document.createElement('div');d.textContent=v??'';return d.innerHTML}
function resize(){const r=canvas.getBoundingClientRect(),dpr=window.devicePixelRatio||1;canvas.width=Math.max(1,r.width*dpr);canvas.height=Math.max(1,r.height*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);layout();draw()}
function filtered(){const q=search.value.trim().toLowerCase();return nodes.filter(n=>(!track.value||n.track===track.value)&&(!type.value||n.type===type.value)&&(!q||`${n.id} ${n.name} ${n.summary}`.toLowerCase().includes(q)))}
function layout(){visible=filtered();positions={};const r=canvas.getBoundingClientRect(),cx=r.width/2,cy=r.height/2;const grouped=Object.groupBy?Object.groupBy(visible,n=>n.track):visible.reduce((a,n)=>((a[n.track]??=[]).push(n),a),{});const groups=Object.entries(grouped).sort();groups.forEach(([t,group],gi)=>{const base=Math.min(r.width,r.height)*(0.16+0.33*(gi+1)/Math.max(1,groups.length));group.forEach((n,i)=>{const angle=2*Math.PI*(i/group.length)+gi*0.47;positions[n.id]={x:cx+Math.cos(angle)*base,y:cy+Math.sin(angle)*base};});});}
function draw(){const r=canvas.getBoundingClientRect();ctx.clearRect(0,0,r.width,r.height);const ids=new Set(visible.map(n=>n.id));ctx.globalAlpha=.24;ctx.strokeStyle='#5d7085';ctx.lineWidth=.6;for(const e of edges){if(!ids.has(e.source)||!ids.has(e.target))continue;const a=positions[e.source],b=positions[e.target];ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke()}ctx.globalAlpha=1;for(const n of visible){const p=positions[n.id],active=selected===n.id;ctx.beginPath();ctx.arc(p.x,p.y,active?7:4.2,0,Math.PI*2);ctx.fillStyle=colors[n.track]||'#94a3b8';ctx.fill();if(active){ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke()}}}
function show(id){selected=id;const n=byId[id];if(!n){details.innerHTML='<p class="empty">Select a node.</p>';draw();return}const outgoing=edges.filter(e=>e.source===id),incoming=edges.filter(e=>e.target===id);const rel=[...outgoing.map(e=>`→ ${e.predicate} · ${e.target}`),...incoming.map(e=>`← ${e.predicate} · ${e.source}`)];const sources=(n.sources||[]).map(s=>{const uri=escapeHtml(s.uri);return `<span class="source">${escapeHtml(s.title)}<br><small>${uri} · ${escapeHtml(s.accessed)} · ${escapeHtml(s.source_class)} · ${escapeHtml(s.sensitivity)}</small></span>`}).join('');details.innerHTML=`<h2>${escapeHtml(n.name)}</h2><div class="pill">${escapeHtml(n.id)}</div><div class="pill">${escapeHtml(n.track)}</div><div class="pill">${escapeHtml(n.type)}</div><div class="pill">${escapeHtml(n.confidence)}</div><div class="pill">${escapeHtml(n.sensitivity)}</div><p class="summary">${escapeHtml(n.summary)}</p><h3>Relations</h3>${rel.length?rel.map(x=>`<div>${escapeHtml(x)}</div>`).join(''):'<p class="empty">None</p>'}<h3>Sources</h3>${sources||'<p class="empty">Graph-derived or unsourced.</p>'}<h3>Entity note</h3><div class="body">${escapeHtml(n.body||'')}</div>`;location.hash=encodeURIComponent(id);draw()}
function refresh(){layout();if(selected&&!visible.some(n=>n.id===selected))selected=null;show(selected)}
[search,track,type].forEach(el=>el.addEventListener(el===search?'input':'change',refresh));
canvas.addEventListener('click',ev=>{const r=canvas.getBoundingClientRect(),x=ev.clientX-r.left,y=ev.clientY-r.top;let hit=null,dist=14;for(const n of visible){const p=positions[n.id],d=Math.hypot(p.x-x,p.y-y);if(d<dist){dist=d;hit=n.id}}if(hit)show(hit)});
window.addEventListener('resize',resize);resize();const initial=decodeURIComponent(location.hash.slice(1));if(byId[initial])show(initial);
</script>
</body>
</html>'''


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--include-sensitivity",
        default="public",
        help="comma-separated classifications to embed; default: public",
    )
    args = parser.parse_args(argv)
    root = args.root.expanduser().resolve()
    graph = root / "context" / "graph"
    entity_path, edge_path = graph / "entities.json", graph / "edges.json"
    if not entity_path.exists() or not edge_path.exists():
        parser.error("compile the graph before building the explorer")
    config = json.loads((root / "graph-config.json").read_text(encoding="utf-8"))
    entities = json.loads(entity_path.read_text(encoding="utf-8"))
    edges = json.loads(edge_path.read_text(encoding="utf-8"))
    allowed = {value.strip() for value in args.include_sensitivity.split(",") if value.strip()}
    invalid = allowed - set(config.get("sensitivities", []))
    if invalid:
        parser.error(f"unknown sensitivity: {', '.join(sorted(invalid))}")
    entities = {key: value for key, value in entities.items() if value.get("sensitivity") in allowed}
    edges = [edge for edge in edges if edge["source"] in entities and edge["target"] in entities]
    title = config.get("project", {}).get("title", "Enterprise Knowledge Graph")
    page = (
        PAGE.replace("__TITLE__", html.escape(title))
        .replace("__SENSITIVITY__", html.escape(", ".join(sorted(allowed)) or "none"))
        .replace("__ENTITIES__", json.dumps(entities, ensure_ascii=False).replace("</", "<\\/"))
        .replace("__EDGES__", json.dumps(edges, ensure_ascii=False).replace("</", "<\\/"))
    )
    output = args.output.expanduser().resolve() if args.output else root / "outputs" / "knowledge-graph.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(page, encoding="utf-8")
    print(f"Wrote {output} with {len(entities)} entities and {len(edges)} edges ({', '.join(sorted(allowed))})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
