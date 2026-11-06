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
    var mx=0,fail=[],rws=[],plans=cls.map(function(c){var p=aqPlan(row,c[1],lot);mx=Math.max(mx,p.n);return p;});
    cls.forEach(function(c,k){var p=plans[k];
      rws.push([c[0]+" · AQL "+(c[1]||0)+(p.n!==mx?" · sample "+num(p.n):""),"accept "+p.ac+" / reject "+p.re]);
      if(c[2]>=p.re)fail.push(c[0].toLowerCase()+" "+num(c[2])+" ≥ "+p.re);});
    document.getElementById("aq-out").textContent=num(mx)+" units";
    document.getElementById("aq-sub").textContent="Code letter "+AQ_LET[row]+" · level "+["","I","II","III"][+lv]+" · "+pct(mx/lot*100)+" of the lot"+(mx>=lot?" (inspect all)":"");
    bar("aq-bar","aq-leg",[["Sampled",mx,C1],["Not sampled",Math.max(lot-mx,0),C3]]);
    rows("aq-tbl",rws.concat([["Sample to pull (check all classes)",num(mx)+" units",1]]));
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

  // ---- CBM & container fit
  var CB_CT=[["20ft",28,28200],["40ft",58,26700],["40ft HC",68,26500]];
  function cbm(){
    var m=document.getElementById("cb-unit").value==="in",k=m?0.0254:0.01,wk=m?0.453592:1,n=Math.max(Math.round(g("cb-n")),0);
    var c=g("cb-l")*k*g("cb-w")*k*g("cb-h")*k,v=c*n,kg=g("cb-wt")*wk*n,rt=Math.max(v,kg/1000);
    var fit=null;CB_CT.forEach(function(t){if(!fit&&v<=t[1]&&kg<=t[2])fit=t;});
    document.getElementById("cb-out").textContent=num(v,2)+" m³";
    document.getElementById("cb-sub").textContent=num(kg)+" kg · "+num(c,3)+" m³ per carton · "+num(v*35.3147,0)+" ft³";
    var best=fit||CB_CT[2];
    bar("cb-bar","cb-leg",[["Used ("+best[0]+")",Math.min(v,best[1]),C1],["Free",Math.max(best[1]-v,0),C3]]);
    var rws=CB_CT.map(function(t){var ct=Math.floor(t[1]/c);return [t[0]+" ("+t[1]+" m³ loadable)",pct(v/t[1]*100,0)+" full · max ~"+num(ct)+" cartons"];});
    rows("cb-tbl",rws.concat([["LCL charge basis (W/M)",num(rt,2)+" revenue tons"],["Containers needed if 40ft HC",num(Math.ceil(v/68))+" × 40ft HC",1]]));
    if(v<15)pill("cb-pill","warn","Under 15 m³: LCL is usually cheaper than a full container");
    else if(fit)pill("cb-pill","ok","Fits one "+fit[0]+" container ("+pct(v/fit[1]*100,0)+" full)");
    else pill("cb-pill","no","More than one 40ft HC: split the load or use several containers");
  }
  // ---- air chargeable weight
  function airChg(){
    var m=document.getElementById("ac-unit").value==="in",dv=document.getElementById("ac-div").value==="5000"?(m?139:5000):(m?166:6000);
    var n=Math.max(Math.round(g("ac-n")),1),vol=g("ac-l")*g("ac-w")*g("ac-h")*n/dv,act=g("ac-wt")*n,u=m?"lb":"kg",step=m?1:0.5;
    var chg=Math.ceil(Math.max(vol,act)/step)*step,isVol=vol>act;
    document.getElementById("ac-out").textContent=num(chg,1)+" "+u;
    document.getElementById("ac-sub").textContent=(isVol?"Volumetric":"Actual")+" weight applies · "+(act>0?num(vol/act,2)+"× volume-to-weight ratio":"");
    bar("ac-bar","ac-leg",[["Actual weight",act,C2],["Extra billed for volume",Math.max(vol-act,0),C1]]);
    rows("ac-tbl",[["Actual weight",num(act,1)+" "+u],["Volumetric weight (÷"+dv+")",num(vol,1)+" "+u],["Volume",m?num(g("ac-l")*g("ac-w")*g("ac-h")*n/1728,2)+" ft³":num(g("ac-l")*g("ac-w")*g("ac-h")*n/1e6,3)+" m³"],
      ["Chargeable weight",num(chg,1)+" "+u,1]]);
    if(isVol)pill("ac-pill","warn","Billed for volume: "+num(chg-act,1)+" "+u+" more than the actual weight");else pill("ac-pill","ok","Billed on actual weight");
  }
  // ---- Cpk
  function ncdf(z){var t=1/(1+0.3275911*Math.abs(z)/Math.SQRT2),e=1-(((((1.061405429*t-1.453152027)*t)+1.421413741)*t-0.284496736)*t+0.254829592)*t*Math.exp(-z*z/2);return z>=0?(1+e)/2:(1-e)/2;}
  function cpk(){
    var ta=document.getElementById("cp-data");
    if(ta&&!ta._b){ta._b=1;ta.addEventListener("input",function(){calc();});}
    var lsl=g("cp-lsl"),usl=g("cp-usl"),mu=g("cp-mean"),sd=g("cp-sd"),src="entered";
    var xs=(ta&&ta.value||"").split(/[\s,;]+/).map(parseFloat).filter(isFinite);
    if(xs.length>=2){mu=xs.reduce(function(a,b){return a+b;},0)/xs.length;sd=Math.sqrt(xs.reduce(function(a,b){return a+(b-mu)*(b-mu);},0)/(xs.length-1));src=xs.length+" measurements";}
    var cp=(usl-lsl)/(6*sd),cu=(usl-mu)/(3*sd),cl=(mu-lsl)/(3*sd),k=Math.min(cu,cl);
    var pu=1-ncdf((usl-mu)/sd),pl=ncdf((lsl-mu)/sd),ppm=(pu+pl)*1e6;
    document.getElementById("cp-out").textContent=isFinite(k)?k.toFixed(2):"–";
    document.getElementById("cp-sub").textContent="Cp "+(isFinite(cp)?cp.toFixed(2):"–")+" · about "+num(ppm,ppm<10?2:0)+" ppm out of spec · from "+src;
    bar("cp-bar","cp-leg",[["Below LSL",pl*1e6,C1],["Above USL",pu*1e6,C2]]);
    rows("cp-tbl",[["Mean",num(mu,4)],["Standard deviation",num(sd,4)],["Cp",cp.toFixed(2)],["Cpu (upper)",cu.toFixed(2)],["Cpl (lower)",cl.toFixed(2)],
      ["Expected out of spec",num(ppm,ppm<10?2:0)+" ppm ("+pct(ppm/1e4,ppm<100?3:2)+")",1]]);
    if(!(sd>0)||usl<=lsl)pill("cp-pill","no","Check limits and standard deviation");
    else if(k>=1.67)pill("cp-pill","ok","Highly capable (Cpk ≥ 1.67)");else if(k>=1.33)pill("cp-pill","ok","Capable (Cpk ≥ 1.33)");
    else if(k>=1)pill("cp-pill","warn","Marginal: "+(cu<cl?"mean is too close to USL":"mean is too close to LSL"));else pill("cp-pill","no","Not capable: expect "+num(ppm)+" ppm out of spec");
  }
  var fns={"cbm":cbm,"air-chargeable":airChg,"cpk":cpk,"aql":aql,"air-leak":airLeak,"freight-class":freight,"machine-hour-rate":machineRate,"oee":oee,"takt-time":takt,"pricing":pricing,"landed-cost":landed,"cost-per-good-unit":goodUnit,"scrap-cost":scrap,"break-even":breakEven,"payback":payback};
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
    tb.innerHTML='<button type="button" data-a="link">Copy link</button><button type="button" data-a="copy">Copy for Excel</button><button type="button" data-a="print">Print / PDF</button><button type="button" data-a="reset">Reset</button><span class="toast" role="status"></span>';
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
    ["input","change","click"].forEach(function(ev){document.addEventListener(ev,function(){setTimeout(upd,0);});});setTimeout(upd,0);
    var mn=document.querySelector("details.menu");if(mn)mn.addEventListener("toggle",function(){sb.style.visibility=mn.open?"hidden":"";});
    new IntersectionObserver(function(es){sb.classList.toggle("on",!es[0].isIntersecting&&window.innerWidth<761);}).observe(res);
    sb.addEventListener("click",function(){res.scrollIntoView({behavior:"smooth",block:"start"});});
  }
  calc();
})();
