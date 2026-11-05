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
    rows("pb-tbl",[["Net saving / year",money(net,0)],["Lifetime net saving",money(net*life,0)],["ROI over life",pct(roi,0)],["NPV at "+pct(r*100,1),money(npv,0),1]]);
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
  var fns={"landed-cost":landed,"cost-per-good-unit":goodUnit,"scrap-cost":scrap,"break-even":breakEven,"payback":payback};
  function calc(){Object.keys(fns).forEach(function(k){if(document.getElementById("v-"+k))fns[k]();});}
  document.querySelectorAll("input").forEach(function(i){i.addEventListener("input",calc);});
  curSel.addEventListener("change",function(){cur=curSel.value;try{localStorage.setItem("sfc-cur",cur);}catch(e){}calc();});
  calc();
})();
