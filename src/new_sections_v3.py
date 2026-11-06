"""v3: AQL sampling, compressed air leak cost, LTL freight class + generic UI helpers (selects, preset chips, sticky mobile result)."""


def f(id_, label, unit, value, step="any", full=False):
    cls = "f full" if full else "f"
    return (f'<div class="{cls}"><label for="{id_}">{label} <span class="u">{unit}</span></label>'
            f'<input id="{id_}" type="number" step="{step}" value="{value}" inputmode="decimal"></div>')


def sel(id_, label, unit, options, value, full=False):
    cls = "f full" if full else "f"
    opts = "".join(f'<option value="{v}"' + (' selected' if str(v) == str(value) else '') + f'>{t}</option>' for v, t in options)
    return f'<div class="{cls}"><label for="{id_}">{label} <span class="u">{unit}</span></label><select id="{id_}">{opts}</select></div>'


def chips(target, items, note=""):
    btns = "".join(f'<button type="button" data-v="{v}">{t}</button>' for v, t in items)
    return f'<div class="f full"><div class="presets" data-for="{target}"><span>{note}</span>{btns}</div></div>'


def result(prefix, kicker, pill=True):
    return (f'<div class="result" aria-live="polite"><div class="kicker">{kicker}</div><div class="big" id="{prefix}-out">–</div>'
            f'<div class="sub" id="{prefix}-sub"></div><div class="bar" id="{prefix}-bar"></div><div class="legend" id="{prefix}-leg"></div>'
            f'<table class="bd" id="{prefix}-tbl"></table>' + (f'<div id="{prefix}-pill"></div>' if pill else "") + '</div>')


def notes(how, title2, body2):
    return (f'<div class="ad">AD SLOT · 728×90 / responsive</div><div class="notes"><div><h2>How it works</h2>'
            f'<code class="fx">{how}</code></div><div><h2>{title2}</h2><p>{body2}</p></div></div>')


AQLS_CRIT = [(0, "0 – no defects allowed"), (0.065, "0.065"), (0.10, "0.10"), (0.25, "0.25")]
AQLS = [(0.065, "0.065"), (0.10, "0.10"), (0.15, "0.15"), (0.25, "0.25"), (0.40, "0.40"), (0.65, "0.65"), (1.0, "1.0"),
        (1.5, "1.5"), (2.5, "2.5"), (4.0, "4.0"), (6.5, "6.5")]

SECTIONS = {
    "aql": (
        '<h1>AQL Sampling Calculator (ISO 2859-1 / ANSI Z1.4)</h1>'
        '<p class="lede">How many units to pull from a shipment and how many defects you can accept, for critical, major and minor defects. Enter what you found to get a pass or fail.</p>'
        '<div class="grid"><div class="fields">'
        + f("aq-lot", "Lot size", "units in the order", 1000, "1")
        + sel("aq-level", "Inspection level", "", [("1", "I – reduced"), ("2", "II – normal"), ("3", "III – tightened")], "2")
        + sel("aq-crit", "Critical AQL", "", AQLS_CRIT, 0)
        + sel("aq-major", "Major AQL", "", AQLS, 2.5)
        + sel("aq-minor", "Minor AQL", "", AQLS, 4.0, full=True)
        + f("aq-fc", "Critical found", "defects", 0, "1")
        + f("aq-fM", "Major found", "defects", 2, "1")
        + f("aq-fm", "Minor found", "defects", 3, "1", full=True)
        + '</div>' + result("aq", "Sample size") + '</div>'
        + notes("1. Lot size + level  → code letter (Table 1)\n2. Code letter      → sample size\n3. Code letter + AQL → accept / reject numbers\n   (arrows move to the nearest plan, Table 2-A)\nPass if defects found ≤ accept number",
                "Choosing the AQL",
                "Common import inspections use 0 for critical defects, 2.5 for major and 4.0 for minor. Agree the AQLs and the defect list with your supplier before production, not at the inspection.")),
    "air-leak": (
        '<h1>Compressed Air Leak Cost Calculator</h1>'
        '<p class="lede">What your compressed air leaks cost each year in electricity, and how fast a leak repair round pays back.</p>'
        '<div class="grid"><div class="fields">'
        + f("al-n", "Number of leaks", "", 20, "1")
        + f("al-cfm", "Flow per leak", "CFM (1 l/s = 2.12 CFM)", 4.0)
        + chips("al-cfm", [("1.0", '1/32″'), ("4.0", '1/16″'), ("16", '1/8″'), ("63", '1/4″')], "Hole size at ~100 psi:")
        + f("al-kw", "Compressor specific power", "kW per 100 CFM", 20)
        + f("al-hrs", "Operating hours", "per year", 6000, "1")
        + f("al-elec", "Electricity price", "per kWh", 0.12)
        + f("al-fix", "Repair cost", "per leak", 50)
        + '</div>' + result("al", "Leak cost per year") + '</div>'
        + notes("Leak flow   = leaks × CFM per leak\nPower       = leak flow × kW per 100 CFM ÷ 100\nEnergy      = power × operating hours\nCost / year = energy × electricity price\nPayback     = repair cost ÷ cost per day",
                "Where the presets come from",
                "The hole-size presets are typical flows at about 100 psi (7 bar) for a rounded orifice, based on US Department of Energy compressed air leak tables. Measured flows from an ultrasonic survey are always better than estimates.")),
    "freight-class": (
        '<h1>LTL Freight Class Calculator (2025 NMFC Density Scale)</h1>'
        '<p class="lede">Density-based freight class for a pallet or crate under the 13-tier NMFC scale in force since July 19, 2025, compared with the old 11-tier scale.</p>'
        '<div class="grid"><div class="fields">'
        + sel("fc-unit", "Units", "", [("in", "inches & pounds"), ("cm", "centimetres & kilograms")], "in", full=True)
        + f("fc-l", "Length", "per piece", 48)
        + f("fc-w", "Width", "per piece", 40)
        + f("fc-h", "Height", "per piece, incl. pallet", 48)
        + f("fc-wt", "Weight", "per piece, incl. pallet", 500)
        + f("fc-n", "Pieces", "identical pallets / crates", 1, "1", full=True)
        + '</div>' + result("fc", "Freight class (2025 scale)") + '</div>'
        + notes("Cubic feet = L × W × H (inches) ÷ 1,728\nDensity    = weight (lb) ÷ cubic feet\nClass      = density band on the NMFC scale",
                "Density only applies to some items",
                "The density scale classifies freight that is rated by density in the NMFC. Some commodities have their own item class, and fragile or hard-to-stow freight can be rated differently. Confirm the NMFC item with your carrier before booking.")),
}

JS = r"""
  // ---- AQL (ISO 2859-1 Table 1 + Table 2-A, normal single sampling)
  var AQ_LOT=[8,15,25,50,90,150,280,500,1200,3200,10000,35000,150000,500000,Infinity];
  var AQ_CODE={"1":"AABCCDEFGHJKLMN","2":"ABCDEFGHJKLMNPQ","3":"BCDEFGHJKLMNPQR"};
  var AQ_LET="ABCDEFGHJKLMNPQR",AQ_N=[2,3,5,8,13,20,32,50,80,125,200,315,500,800,1250,2000];
  var AQ_COL={"0.065":4,"0.1":5,"0.15":6,"0.25":7,"0.4":8,"0.65":9,"1":10,"1.5":11,"2.5":12,"4":13,"6.5":14};
  var AQ_D={14:[0,1],17:[1,2],18:[2,3],19:[3,4],20:[5,6],21:[7,8],22:[10,11],23:[14,15],24:[21,22]};
  function aqPlan(row,aql,lot){
    if(!aql)return {n:Math.min(AQ_N[row],lot),ac:0,re:1,l:AQ_LET[row]};
    var c=AQ_COL[String(aql)],d=row+c;
    if(d<=13)row+=14-d;else if(d===15)row-=1;else if(d===16)row+=1;else if(d>=25)row-=d-24;
    row=Math.max(0,Math.min(15,row));var ar=AQ_D[row+c]||[0,1];
    return {n:Math.min(AQ_N[row],lot),ac:ar[0],re:ar[1],l:AQ_LET[row],all:AQ_N[row]>=lot};
  }
  function aql(){
    var lot=Math.max(Math.round(g("aq-lot")),2),lv=document.getElementById("aq-level").value,i=0;
    while(lot>AQ_LOT[i])i++;
    var row=AQ_LET.indexOf(AQ_CODE[lv][i]);
    var cls=[["Critical",parseFloat(document.getElementById("aq-crit").value),g("aq-fc")],["Major",parseFloat(document.getElementById("aq-major").value),g("aq-fM")],["Minor",parseFloat(document.getElementById("aq-minor").value),g("aq-fm")]];
    var mx=0,fail=[],rws=[];
    cls.forEach(function(c){var p=aqPlan(row,c[1],lot);mx=Math.max(mx,p.n);
      rws.push([c[0]+" (AQL "+(c[1]||0)+")","inspect "+num(p.n)+" · accept ≤ "+p.ac+" · reject ≥ "+p.re]);
      if(c[2]>=p.re)fail.push(c[0].toLowerCase()+" "+num(c[2])+" ≥ "+p.re);});
    document.getElementById("aq-out").textContent=num(mx)+" units";
    document.getElementById("aq-sub").textContent="Code letter "+AQ_LET[row]+" · level "+["","I","II","III"][+lv]+" · "+pct(mx/lot*100)+" of the lot"+(mx>=lot?" (inspect all)":"");
    bar("aq-bar","aq-leg",[["Sampled",mx,C1],["Not sampled",Math.max(lot-mx,0),C3]]);
    rows("aq-tbl",rws.concat([["Pull the largest sample and check it for all three classes",num(mx)+" units",1]]));
    if(fail.length)pill("aq-pill","no","Fail: "+fail.join(", "));else pill("aq-pill","ok","Pass: all defect counts within limits");
  }
  // ---- compressed air leaks
  function airLeak(){
    var n=g("al-n"),q=g("al-cfm"),kw=g("al-kw")/100,h=g("al-hrs"),e=g("al-elec"),fx=g("al-fix");
    var flow=n*q,pw=flow*kw,kwh=pw*h,cost=kwh*e,rep=n*fx,pb=cost>0?rep/(cost/365):NaN;
    document.getElementById("al-out").textContent=money(cost,0);
    document.getElementById("al-sub").textContent=money(n>0?cost/n:NaN,0)+" per leak per year · "+num(kwh)+" kWh wasted";
    bar("al-bar","al-leg",[["Repair cost",rep,C2],["First-year saving after repair",Math.max(cost-rep,0),C1]]);
    rows("al-tbl",[["Total leak flow",num(flow,1)+" CFM ("+num(flow/2.119,1)+" l/s)"],["Compressor power wasted",num(pw,1)+" kW"],["Energy per year",num(kwh)+" kWh"],
      ["Cost per year",money(cost,0)],["Repair round ("+num(n)+" leaks)",money(rep,0)],["Payback of repairs",isFinite(pb)?num(Math.ceil(pb))+" days":"–",1]]);
    if(pb<=90)pill("al-pill","ok","Repairs pay back in "+num(Math.ceil(pb))+" days");else if(isFinite(pb))pill("al-pill","warn","Payback "+num(Math.ceil(pb))+" days");else pill("al-pill","warn","Enter leaks and flow");
  }
  // ---- LTL freight class (NMFC full density scale)
  var FC_NEW=[[1,400],[2,300],[4,250],[6,175],[8,125],[10,100],[12,92.5],[15,85],[22.5,70],[30,65],[35,60],[50,55],[Infinity,50]];
  var FC_OLD=[[1,400],[2,300],[4,250],[6,175],[8,125],[10,100],[12,92.5],[15,85],[22.5,70],[30,65],[Infinity,60]];
  function fcClass(d,t){for(var i=0;i<t.length;i++)if(d<t[i][0])return {c:t[i][1],i:i};return {c:t[t.length-1][1],i:t.length-1};}
  function freight(){
    var m=document.getElementById("fc-unit").value==="cm",k=m?1/2.54:1,wk=m?2.20462:1;
    var L=g("fc-l")*k,W=g("fc-w")*k,H=g("fc-h")*k,wt=g("fc-wt")*wk,n=Math.max(Math.round(g("fc-n")),1);
    var cuft=L*W*H/1728*n,tw=wt*n,d=cuft>0?tw/cuft:NaN,a=fcClass(d,FC_NEW),o=fcClass(d,FC_OLD);
    document.getElementById("fc-out").textContent="Class "+a.c;
    document.getElementById("fc-sub").textContent=num(d,2)+" lb per cubic foot · "+num(cuft,1)+" ft³ · "+num(tw)+" lb";
    var nxt=a.i<FC_NEW.length-1?FC_NEW[a.i][0]:NaN,need=isFinite(nxt)?nxt*cuft-tw:NaN;
    bar("fc-bar","fc-leg",[["Density",Math.min(d,60),C1],["To 60 pcf",Math.max(60-d,0),C3]]);
    rows("fc-tbl",[["Total volume",num(cuft,1)+" ft³ ("+num(cuft*0.0283168,2)+" m³)"],["Total weight",num(tw)+" lb ("+num(tw/2.20462)+" kg)"],["Density",num(d,2)+" pcf"],
      ["Class on pre-July 2025 scale","Class "+o.c],[isFinite(nxt)?"Weight to reach "+num(nxt,1)+" pcf (class "+FC_NEW[a.i+1][1]+")":"Densest band reached",isFinite(need)?"+"+num(Math.ceil(need))+" lb":"–"],["Freight class (2025 scale)","Class "+a.c,1]]);
    if(a.c!==o.c)pill("fc-pill","warn","Changed from class "+o.c+" under the old scale");else pill("fc-pill","ok","Same class as the old scale");
  }
"""

FNS = '"aql":aql,"air-leak":airLeak,"freight-class":freight,'

# UI helpers appended after the toolbar code (selects in state, preset chips, sticky result bar on phones)
UI_JS = r"""
  // ---- selects take part in calc, URL state and reset
  if(sheet){sheet.querySelectorAll("select").forEach(function(s){defaults[s.id]=s.value;
    var v=q.get(s.id);if(v!==null&&Array.prototype.some.call(s.options,function(o){return o.value===v;}))s.value=v;
    s.addEventListener("change",calc);});}
  var _stateUrl=stateUrl;stateUrl=function(){var u=_stateUrl(),p=new URLSearchParams(u.split("?")[1]||"");
    if(sheet)sheet.querySelectorAll("select").forEach(function(s){if(s.value!==defaults[s.id])p.set(s.id,s.value);});
    var s=p.toString();return location.pathname+(s?"?"+s:"");};
  var resetBtn=document.querySelector('.tools button[data-a="reset"]');
  if(resetBtn)resetBtn.addEventListener("click",function(){if(sheet)sheet.querySelectorAll("select").forEach(function(s){s.value=defaults[s.id];});calc();});
  // ---- preset chips fill an input
  document.querySelectorAll(".presets").forEach(function(box){var t=document.getElementById(box.getAttribute("data-for"));
    box.addEventListener("click",function(e){var v=e.target.getAttribute&&e.target.getAttribute("data-v");if(v&&t){t.value=v;calc();}});});
  // ---- sticky result bar on phones while the result panel is off screen
  if(res&&"IntersectionObserver" in window){
    var sb=document.createElement("button");sb.type="button";sb.className="stick";sb.setAttribute("aria-label","Jump to result");
    document.body.appendChild(sb);
    function upd(){sb.innerHTML='<span>'+res.querySelector(".kicker").textContent+'</span><b>'+res.querySelector(".big").textContent+'</b><i>Result ↓</i>';}
    ["input","change","click"].forEach(function(ev){document.addEventListener(ev,function(){setTimeout(upd,0);});});upd();
    new IntersectionObserver(function(es){sb.classList.toggle("on",!es[0].isIntersecting&&window.innerWidth<761);}).observe(res);
    sb.addEventListener("click",function(){res.scrollIntoView({behavior:"smooth",block:"start"});});
  }
"""

UI_CSS = """
.presets{display:flex;flex-wrap:wrap;gap:6px;align-items:center;font-size:.8rem;color:var(--muted)}
.presets span{margin-right:2px}
.presets button{font:600 .8rem var(--mono);padding:5px 9px;border:1px solid var(--line);border-radius:999px;background:var(--panel);color:var(--ink);cursor:pointer}
.presets button:hover{border-color:var(--accent)}
select{width:100%;font-family:var(--body)}
.stick{position:fixed;left:12px;right:12px;bottom:max(12px,env(safe-area-inset-bottom,0px));z-index:20;display:none;align-items:center;gap:10px;
  padding:10px 14px;border:1px solid var(--ink);border-radius:10px;background:var(--panel);color:var(--ink);box-shadow:0 6px 24px rgba(0,0,0,.18);font:inherit;text-align:left;cursor:pointer}
.stick.on{display:flex}
.stick span{font:600 .7rem var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);flex:0 1 auto;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.stick b{font:600 1.15rem var(--mono);color:var(--accent);margin-left:auto;white-space:nowrap}
.stick i{font-style:normal;font-size:.75rem;color:var(--muted);white-space:nowrap}
@media print{.stick{display:none!important}}
.menu{position:relative;margin:16px 0 0}
.menu summary{list-style:none;cursor:pointer;display:inline-flex;align-items:center;gap:8px;font:600 .95rem/1 var(--display);letter-spacing:.04em;text-transform:uppercase;
  padding:11px 14px;border:1px solid var(--ink);border-radius:6px;background:var(--panel)}
.menu summary::-webkit-details-marker{display:none}
.menu summary::after{content:"▾";color:var(--accent)}
.menu[open] summary::after{content:"▴"}
.menu-panel{position:absolute;z-index:30;left:0;right:0;margin-top:6px;background:var(--panel);border:1px solid var(--ink);border-radius:8px;padding:14px 16px;
  display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px 20px;box-shadow:0 10px 30px rgba(0,0,0,.15)}
.menu-panel h3{font:700 .78rem var(--display);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:0 0 4px}
.menu-panel a{display:block;padding:5px 0;color:var(--ink);text-decoration:none}
.menu-panel a:hover,.menu-panel a[aria-current="page"]{color:var(--accent)}
.finder{width:100%;margin:6px 0 4px;padding:11px 12px;font-size:1rem}
.cards a[hidden]{display:none}
@media (max-width:420px){.fields{grid-template-columns:1fr 1fr}}
@media (max-width:340px){.fields{grid-template-columns:1fr}}
"""
