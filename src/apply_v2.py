"""One-off migration to v2: add 4 calculators, IRR, share/copy/print/reset toolbar. Run once from the project root."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from new_sections import FNS, JS, SECTIONS  # noqa: E402

src = Path(__file__).parent
secs = json.loads((src / "sections.json").read_text(encoding="utf-8"))
secs.update(SECTIONS)
for k in secs:  # numeric keypad on phones
    secs[k] = secs[k].replace('type="number" step="any" value', 'type="number" step="any" inputmode="decimal" value') \
        if 'inputmode' not in secs[k] else secs[k]
(src / "sections.json").write_text(json.dumps(secs, ensure_ascii=False), encoding="utf-8")

js = (src / "calc.js").read_text(encoding="utf-8")


def rep(old, new):
    global js
    assert js.count(old) == 1, old[:80]
    js = js.replace(old, new)


rep('  var fns={', JS + '  var fns={' + FNS)
# IRR row for payback
rep('    rows("pb-tbl",[["Net saving / year",money(net,0)],',
    '    var irr=NaN;if(net>0&&net*life>inv){var lo=-0.99,hi=10;for(var it=0;it<200;it++){var md=(lo+hi)/2,v=-inv;for(var t=1;t<=life;t++)v+=net/Math.pow(1+md,t);if(v>0)lo=md;else hi=md;}irr=(lo+hi)/2*100;}\n'
    '    rows("pb-tbl",[["Net saving / year",money(net,0)],["IRR",pct(irr,1)],')
# state in URL + toolbar
rep('  calc();\n', r'''  // ---- shareable state: inputs <-> URL query
  var sheet=document.querySelector(".sheet");
  var defaults={};
  if(sheet){sheet.querySelectorAll("input").forEach(function(i){defaults[i.id]=i.value;});}
  var q=new URLSearchParams(location.search);
  q.forEach(function(v,k){var el=document.getElementById(k);if(el&&el.tagName==="INPUT"&&isFinite(parseFloat(v)))el.value=v;});
  if(q.get("basis")==="fob"||q.get("basis")==="cif"){var bb=document.querySelector('#lc-basis button[data-b="'+q.get("basis")+'"]');if(bb)bb.click();}
  if(q.get("cur")&&SYM[q.get("cur")]){cur=q.get("cur");curSel.value=cur;}
  function stateUrl(){var p=new URLSearchParams();
    if(sheet)sheet.querySelectorAll("input").forEach(function(i){if(i.value!==defaults[i.id])p.set(i.id,i.value);});
    if(document.getElementById("lc-basis")&&basis!=="cif")p.set("basis",basis);
    if(cur!=="USD")p.set("cur",cur);
    var s=p.toString();return location.pathname+(s?"?"+s:"");}
  var _calc=calc;calc=function(){_calc();try{history.replaceState(null,"",stateUrl());}catch(e){}};
  document.querySelectorAll("input").forEach(function(i){i.removeEventListener("input",_calc);i.addEventListener("input",calc);});
  curSel.addEventListener("change",function(){calc();});
  document.querySelectorAll("#lc-basis button").forEach(function(b){b.addEventListener("click",function(){setTimeout(calc,0);});});
  // ---- toolbar
  var res=sheet&&sheet.querySelector(".result");
  if(res){
    var tb=document.createElement("div");tb.className="tools";
    tb.innerHTML='<button type="button" data-a="link">Copy link</button><button type="button" data-a="copy">Copy results</button><button type="button" data-a="print">Print / PDF</button><button type="button" data-a="reset">Reset</button><span class="toast" role="status"></span>';
    res.appendChild(tb);
    var toast=tb.querySelector(".toast");
    function say(t){toast.textContent=t;setTimeout(function(){toast.textContent="";},2200);}
    function copy(t){if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(function(){say("Copied");},function(){say("Copy failed");});}
      else{var ta=document.createElement("textarea");ta.value=t;document.body.appendChild(ta);ta.select();try{document.execCommand("copy");say("Copied");}catch(e){say("Copy failed");}ta.remove();}}
    tb.addEventListener("click",function(e){var a=e.target.getAttribute&&e.target.getAttribute("data-a");if(!a)return;
      if(a==="link")copy(location.origin+stateUrl());
      if(a==="copy"){var h=sheet.querySelector("h1").textContent,lines=[h,res.querySelector(".kicker").textContent+": "+res.querySelector(".big").textContent,res.querySelector(".sub").textContent];
        sheet.querySelectorAll(".fields .f").forEach(function(f){var l=f.querySelector("label"),i=f.querySelector("input");if(l&&i)lines.push(l.childNodes[0].textContent.trim()+"\t"+i.value);});
        res.querySelectorAll("table.bd tr").forEach(function(tr){lines.push(Array.prototype.map.call(tr.cells,function(c){return c.textContent;}).join("\t"));});
        lines.push(location.origin+stateUrl());copy(lines.join("\n"));}
      if(a==="print")window.print();
      if(a==="reset"){Object.keys(defaults).forEach(function(k){document.getElementById(k).value=defaults[k];});var cb=document.querySelector('#lc-basis button[data-b="cif"]');if(cb)cb.click();calc();say("Reset to example");}
    });
  }
  calc();
''')
(src / "calc.js").write_text(js, encoding="utf-8")

css = (src / "style.css").read_text(encoding="utf-8")
if ".tools{" not in css:
    css += """
.tools{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px;align-items:center}
.tools button{font:600 .82rem var(--body);padding:7px 11px;border:1px solid var(--line);border-radius:4px;background:var(--panel);color:var(--ink);cursor:pointer}
.tools button:hover{border-color:var(--accent)}
.toast{font-size:.82rem;color:var(--good)}
.crumbs{font-size:.85rem;color:var(--muted);margin:14px 0 0}
.crumbs a{color:var(--muted)}
.reviewed{font-size:.85rem;color:var(--muted);margin:16px 0 0}
.cat{margin-top:22px}
.cat h2{font:700 1rem var(--display);text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin:0 0 4px}
@media print{
  header.top .cur,.site-nav,.crumbs,.ad,.tools,article.guide,footer{display:none!important}
  body{background:#fff}.sheet{border:none;padding:0}
  .print-url{display:block!important;font-size:.8rem;color:#555;margin-top:12px}
}
.print-url{display:none}
"""
    (src / "style.css").write_text(css, encoding="utf-8")
print("v2 applied:", sorted(secs))
