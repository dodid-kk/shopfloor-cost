(function(){
  var SYM={USD:"$",EUR:"€",GBP:"£",JPY:"¥",KRW:"₩"};
  var cur="USD";
  try{var s=localStorage.getItem("sfc-cur");if(s&&SYM[s])cur=s;}catch(e){}
  var curSel=document.getElementById("cur");if(!curSel)return;curSel.value=cur;
  function dec(){return (cur==="JPY"||cur==="KRW")?0:2;}
  function money(v,d){if(!isFinite(v))return "–";var dd=d===undefined?dec():d;
    return (v<0?"−":"")+SYM[cur]+Math.abs(v).toLocaleString("en-US",{minimumFractionDigits:dd,maximumFractionDigits:dd});}
  function num(v,d){if(!isFinite(v))return "–";return v.toLocaleString("en-US",{maximumFractionDigits:d||0});}
  function pct(v,d){return isFinite(v)?v.toFixed(d===undefined?1:d)+"%":"–";}
  function g(id){var v=parseFloat(document.getElementById(id).value);return isFinite(v)?v:0;}
  function rows(id,list){document.getElementById(id).innerHTML=list.map(function(r){
    return '<tr'+(r[2]?' class="tot"':'')+'><td>'+r[0]+'</td><td>'+r[1]+'</td></tr>';}).join("");}
  function bar(id,legId,parts){var tot=parts.reduce(function(a,p){return a+Math.max(p[1],0);},0)||1;
    document.getElementById(id).innerHTML=parts.map(function(p){return '<i style="width:'+(Math.max(p[1],0)/tot*100)+'%;background:'+p[2]+'"></i>';}).join("");
    document.getElementById(legId).innerHTML=parts.map(function(p){return '<span><b style="background:'+p[2]+'"></b>'+p[0]+' '+pct(Math.max(p[1],0)/tot*100,0)+'</span>';}).join("");}
  function pill(id,cls,txt){document.getElementById(id).innerHTML='<span class="pill '+cls+'">'+txt+'</span>';}
  var C1="var(--accent)",C2="var(--bar2)",C3="var(--bar3)",C4="var(--muted)";

  var basis="cif";
  document.querySelectorAll("#lc-basis button").forEach(function(b){b.addEventListener("click",function(){
    basis=b.dataset.b;document.querySelectorAll("#lc-basis button").forEach(function(x){x.setAttribute("aria-pressed",x===b);});calc();});});

  function landed(){
    var price=g("lc-price"),q=g("lc-qty"),fr=g("lc-freight"),ins=g("lc-ins")/100,du=g("lc-duty")/100,fees=g("lc-fees"),oth=g("lc-other");
    var goods=price*q,insurance=goods*ins,base=basis==="cif"?goods+fr+insurance:goods,duty=base*du;
    var total=goods+fr+insurance+duty+fees+oth,per=q>0?total/q:NaN;
    document.getElementById("lc-out").textContent=money(per,cur==="JPY"||cur==="KRW"?0:3);
    document.getElementById("lc-sub").textContent="Total "+money(total)+" · "+pct((total/goods-1)*100)+" above the purchase price";
    bar("lc-bar","lc-leg",[["Goods",goods,C2],["Freight + ins.",fr+insurance,C3],["Duty",duty,C1],["Fees + handling",fees+oth,C4]]);
    rows("lc-tbl",[["Goods ("+num(q)+" × "+money(price)+")",money(goods)],["Freight",money(fr)],["Insurance",money(insurance)],
      ["Duty on "+(basis==="cif"?"CIF":"FOB")+" value "+money(base),money(duty)],["Customs & broker fees",money(fees)],["Port, handling, inland",money(oth)],["Total landed cost",money(total),1]]);
  }
  function goodUnit(){
    var m=g("cg-mat"),c=g("cg-conv"),st=g("cg-start"),y=Math.min(Math.max(g("cg-yield"),0),100)/100,sv=g("cg-salv");
    var good=st*y,rej=st-good,gross=st*(m+c),salv=rej*sv,net=gross-salv,per=good>0?net/good:NaN,ideal=m+c,hidden=(per-ideal)*good;
    document.getElementById("cg-out").textContent=money(per,cur==="JPY"||cur==="KRW"?0:3);
    document.getElementById("cg-sub").textContent=pct((per/ideal-1)*100)+" above the cost of a perfect run";
    bar("cg-bar","cg-leg",[["Good parts",good*ideal,C2],["Scrap (net of salvage)",rej*ideal-salv,C1]]);
    rows("cg-tbl",[["Good units",num(good)],["Rejected units",num(rej)],["Cost of units started",money(gross)],["Salvage recovered","−"+money(salv)],
      ["Cost per started unit",money(ideal,3)],["Scrap cost carried by good parts",money(hidden),1]]);
  }
  function scrap(){
    var v=g("sc-vol"),c=g("sc-cost"),s=g("sc-scrap")/100,sv=g("sc-salv"),r=g("sc-rw")/100,rc=g("sc-rwc"),t=g("sc-target")/100;
    var sl=v*s*(c-sv)*12,rl=v*r*rc*12,tot=sl+rl,after=v*t*(c-sv)*12,save=sl-after;
    document.getElementById("sc-out").textContent=money(tot,0);
    document.getElementById("sc-sub").textContent=money(tot/12,0)+" per month · "+pct(tot/(v*c*12)*100)+" of production cost";
    bar("sc-bar","sc-leg",[["Scrap",sl,C1],["Rework",rl,C2]]);
    rows("sc-tbl",[["Scrapped units / year",num(v*s*12)],["Scrap loss / year",money(sl,0)],["Reworked units / year",num(v*r*12)],["Rework loss / year",money(rl,0)],
      ["Scrap loss at target "+pct(t*100),money(after,0)],["Saving from reaching target",money(save,0),1]]);
    if(save>0)pill("sc-pill","ok","Reaching target saves "+money(save,0)+" a year");else pill("sc-pill","warn","Target is not below the current scrap rate");
  }
  function breakEven(){
    var f=g("be-fixed"),p=g("be-price"),vc=g("be-var"),t=g("be-target"),ex=g("be-sales");
    var cm=p-vc,el=document.getElementById("be-out");
    if(cm<=0){el.textContent="Never";document.getElementById("be-sub").textContent="Price must be higher than variable cost";
      document.getElementById("be-bar").innerHTML="";document.getElementById("be-leg").innerHTML="";rows("be-tbl",[]);pill("be-pill","no","Each sale loses money");return;}
    var be=Math.ceil(f/cm),tv=Math.ceil((f+t)/cm),profit=ex*cm-f,ms=ex>0?(ex-be)/ex*100:NaN;
    el.textContent=num(be)+" units";
    document.getElementById("be-sub").textContent=money(be*p,0)+" revenue per month · "+pct(cm/p*100)+" contribution margin";
    bar("be-bar","be-leg",[["Variable cost",vc,C2],["Contribution",cm,C1]]);
    rows("be-tbl",[["Contribution per unit",money(cm)],["Units for target profit",num(tv)],["Revenue for target profit",money(tv*p,0)],
      ["Profit at expected sales",money(profit,0)],["Margin of safety",pct(ms),1]]);
    if(ms>=20)pill("be-pill","ok","Comfortable: "+pct(ms,0)+" above break-even");else if(ms>=0)pill("be-pill","warn","Thin margin: "+pct(ms,0)+" above break-even");else pill("be-pill","no","Expected sales are below break-even");
  }
  function payback(){
    var inv=g("pb-inv"),life=Math.max(Math.round(g("pb-life")),1),net=g("pb-labor")+g("pb-qual")-g("pb-op"),r=g("pb-rate")/100;
    var pb=net>0?inv/net:Infinity,roi=(net*life-inv)/inv*100,npv=-inv;
    for(var y=1;y<=life;y++)npv+=net/Math.pow(1+r,y);
    var out=document.getElementById("pb-out");
    out.textContent=isFinite(pb)?pb.toFixed(1)+" years":"No payback";
    document.getElementById("pb-sub").textContent=money(net,0)+" net saving per year over "+life+" years";
    var irr=NaN;if(net>0&&net*life>inv){var lo=-0.99,hi=10;for(var it=0;it<200;it++){var md=(lo+hi)/2,v=-inv;for(var t=1;t<=life;t++)v+=net/Math.pow(1+md,t);if(v>0)lo=md;else hi=md;}irr=(lo+hi)/2*100;}
    rows("pb-tbl",[["Net saving / year",money(net,0)],["IRR",pct(irr,1)],["Lifetime net saving",money(net*life,0)],["ROI over life",pct(roi,0)],["NPV at "+pct(r*100,1),money(npv,0),1]]);
    if(!isFinite(pb)||pb>life)pill("pb-pill","no","Does not pay back within its life");else if(npv<0)pill("pb-pill","warn","Pays back, but NPV is negative");else if(pb<=3)pill("pb-pill","ok","Strong case: payback under 3 years");else pill("pb-pill","warn","Pays back in "+pb.toFixed(1)+" years");
    // chart: cumulative cash
    var pts=[-inv];for(var k=1;k<=life;k++)pts.push(-inv+net*k);
    var mn=Math.min.apply(null,pts.concat([0])),mx=Math.max.apply(null,pts.concat([0])),W=320,H=120,L=8,R=8,T=12,B=22;
    var x=function(i){return L+i*(W-L-R)/life;},yy=function(v){return T+(mx-v)/((mx-mn)||1)*(H-T-B);};
    var s='<line x1="'+L+'" x2="'+(W-R)+'" y1="'+yy(0)+'" y2="'+yy(0)+'" stroke="var(--muted)" stroke-dasharray="3 3" stroke-width="1"/>';
    var bw=(W-L-R)/(life+1)*0.6;
    pts.forEach(function(v,i){var y0=yy(0),y1=yy(v);s+='<rect x="'+(x(i)-bw/2+ (i===0?bw/2:0) - (i===life?bw/2:0))+'" y="'+Math.min(y0,y1)+'" width="'+bw+'" height="'+Math.max(Math.abs(y1-y0),1)+'" fill="'+(v<0?"var(--bar3)":"var(--accent)")+'"/>';
      s+='<text x="'+x(i)+'" y="'+(H-6)+'" font-size="9" text-anchor="'+(i===0?"start":i===life?"end":"middle")+'" fill="var(--muted)" font-family="var(--mono)">'+(i===0?"Y0":"Y"+i)+'</text>';});
    document.getElementById("pb-svg").innerHTML=s;
  }

  function machineRate(){
    var price=g("mh-price"),res=g("mh-resid"),life=Math.max(g("mh-life"),1),r=g("mh-int")/100;
    var hrs=g("mh-hrs")*g("mh-shifts")*g("mh-days")*g("mh-util")/100;
    var dep=(price-res)/life,intr=(price+res)/2*r,space=g("mh-area")*g("mh-rent"),mt=g("mh-maint");
    var fixed=(dep+intr+space+mt)/(hrs||NaN),energy=g("mh-kw")*g("mh-load")/100*g("mh-elec"),rate=fixed+energy,withOp=rate+g("mh-wage");
    document.getElementById("mh-out").textContent=money(rate)+" / h";
    document.getElementById("mh-sub").textContent=money(withOp)+" / h with operator · "+num(hrs)+" running hours a year";
    bar("mh-bar","mh-leg",[["Depreciation",dep/hrs,C2],["Interest",intr/hrs,C3],["Space + maint.",(space+mt)/hrs,C4],["Energy",energy,C1]]);
    rows("mh-tbl",[["Depreciation / year",money(dep,0)],["Interest on capital / year",money(intr,0)],["Space / year",money(space,0)],["Maintenance / year",money(mt,0)],
      ["Fixed cost per running hour",money(fixed)],["Energy per hour",money(energy)],["Machine rate (no operator)",money(rate),1]]);
  }
  function oee(){
    var pl=g("oe-planned"),dn=Math.min(g("oe-down"),pl),ic=g("oe-ideal"),tot=g("oe-total"),good=Math.min(g("oe-good"),tot);
    var run=pl-dn,A=pl>0?run/pl:NaN,P=run>0?(ic*tot/60)/run:NaN,Q=tot>0?good/tot:NaN,O=A*P*Q;
    var full=good*ic/60,perfLoss=run-ic*tot/60,qLoss=(tot-good)*ic/60;
    document.getElementById("oe-out").textContent=pct(O*100);
    document.getElementById("oe-sub").textContent="Availability "+pct(A*100)+" · Performance "+pct(P*100)+" · Quality "+pct(Q*100);
    bar("oe-bar","oe-leg",[["Fully productive",full,C2],["Downtime",dn,C1],["Speed loss",Math.max(perfLoss,0),C3],["Quality loss",qLoss,C4]]);
    rows("oe-tbl",[["Run time",num(run,1)+" min"],["Fully productive time",num(full,1)+" min"],["Lost to downtime",num(dn,1)+" min"],["Lost to slow cycles",num(perfLoss,1)+" min"],
      ["Lost to defects",num(qLoss,1)+" min"],["Good units lost vs. ideal",num(Math.max(pl*60/ic-good,0)),1]]);
    if(P>1.05)pill("oe-pill","no","Performance above 100%: check the ideal cycle time");
    else if(O>=0.85)pill("oe-pill","ok","World-class range (85%+)");else if(O>=0.6)pill("oe-pill","warn","Typical range: "+pct(O*100,0));else pill("oe-pill","no","Low OEE: biggest loss is "+[["downtime",dn],["speed",perfLoss],["quality",qLoss]].sort(function(a,b){return b[1]-a[1];})[0][0]);
  }
  function takt(){
    var avail=(g("tk-shift")-g("tk-breaks"))*g("tk-shifts")*60,d=g("tk-demand"),wc=g("tk-work"),bn=g("tk-bottle");
    var t=d>0?avail/d:NaN,st=t>0?Math.ceil(wc/t):NaN,maxOut=bn>0?Math.floor(avail/bn):NaN,bal=st>0?wc/(st*t)*100:NaN;
    document.getElementById("tk-out").textContent=num(t,1)+" s";
    document.getElementById("tk-sub").textContent="One unit every "+num(t,1)+" seconds · "+num(d)+" units in "+num(avail/60)+" minutes";
    bar("tk-bar","tk-leg",[["Bottleneck cycle",Math.min(bn,t),C2],[bn>t?"Over takt":"Spare",Math.abs(t-bn),bn>t?C1:C3]]);
    rows("tk-tbl",[["Available time per day",num(avail/60)+" min"],["Stations / operators needed",num(st)],["Line balance efficiency",pct(bal)],
      ["Max output at bottleneck",num(maxOut)+" / day"],["Gap to demand",num(maxOut-d)+" / day",1]]);
    if(bn>t)pill("tk-pill","no","Bottleneck is "+num(bn-t,1)+" s slower than takt");else pill("tk-pill","ok","Bottleneck keeps up with takt");
  }
  function pricing(){
    var c=g("pr-cost"),m=g("pr-margin")/100,fe=(g("pr-fee")+g("pr-pay"))/100,fx=g("pr-fixed"),den=1-m-fe,el=document.getElementById("pr-out");
    if(den<=0){el.textContent="–";document.getElementById("pr-sub").textContent="Margin plus fees must be below 100%";rows("pr-tbl",[]);pill("pr-pill","no","Impossible target");return;}
    var p=(c+fx)/den,fees=p*fe,profit=p-c-fees-fx,mk=c>0?(p-c)/c*100:NaN;
    el.textContent=money(p);
    document.getElementById("pr-sub").textContent="Markup on cost "+pct(mk)+" · profit "+money(profit)+" per unit";
    bar("pr-bar","pr-leg",[["Cost",c,C2],["Fees",fees+fx,C3],["Profit",profit,C1]]);
    rows("pr-tbl",[["Unit cost",money(c)],["Channel + payment fees",money(fees)],["Fixed fee",money(fx)],["Gross profit",money(profit)],["Margin on price",pct(profit/p*100)],
      ["Same markup "+pct(m*100,0)+" would give a margin of",pct(m/(1+m)*100),1]]);
    pill("pr-pill","ok","Charge "+money(p)+" to keep "+pct(m*100,0)+" after fees");
  }
  var fns={"machine-hour-rate":machineRate,"oee":oee,"takt-time":takt,"pricing":pricing,"landed-cost":landed,"cost-per-good-unit":goodUnit,"scrap-cost":scrap,"break-even":breakEven,"payback":payback};
  function calc(){Object.keys(fns).forEach(function(k){if(document.getElementById("v-"+k))fns[k]();});}
  document.querySelectorAll("input").forEach(function(i){i.addEventListener("input",calc);});
  curSel.addEventListener("change",function(){cur=curSel.value;try{localStorage.setItem("sfc-cur",cur);}catch(e){}calc();});
  // ---- shareable state: inputs <-> URL query
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
})();
