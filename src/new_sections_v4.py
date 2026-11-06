"""v4: CBM & container fit, air freight chargeable weight, Cpk / process capability."""
from new_sections_v3 import f, notes, result, sel

SECTIONS = {
    "cbm": (
        '<h1>CBM &amp; Container Loading Calculator</h1>'
        '<p class="lede">Total cubic metres and weight of a carton shipment, how full a 20ft, 40ft or 40ft high-cube container would be, and whether LCL is the better choice.</p>'
        '<div class="grid"><div class="fields">'
        + sel("cb-unit", "Units", "", [("cm", "centimetres & kilograms"), ("in", "inches & pounds")], "cm", full=True)
        + f("cb-l", "Carton length", "", 60)
        + f("cb-w", "Carton width", "", 40)
        + f("cb-h", "Carton height", "", 40)
        + f("cb-wt", "Carton weight", "gross", 18)
        + f("cb-n", "Number of cartons", "", 250, "1", full=True)
        + '</div>' + result("cb", "Total volume") + '</div>'
        + notes("Carton CBM = L × W × H (m)\nTotal CBM  = carton CBM × cartons\nFill %     = total CBM ÷ loadable CBM\nLCL charge = max(CBM, tonnes)  (W/M, 1 m³ = 1,000 kg)",
                "Loadable, not internal, volume",
                "A 20ft container has about 33 m³ inside, but cartons rarely fill more than 25–28 m³ once you allow for gaps, pallets and door clearance. This calculator uses 28, 58 and 68 m³ as practical loads for 20ft, 40ft and 40ft high-cube.")),
    "air-chargeable": (
        '<h1>Air Freight Chargeable Weight Calculator</h1>'
        '<p class="lede">Volumetric (dimensional) weight and the chargeable weight an airline or courier will bill, for the IATA 6000 divisor and the express 5000 divisor.</p>'
        '<div class="grid"><div class="fields">'
        + sel("ac-unit", "Units", "", [("cm", "centimetres & kilograms"), ("in", "inches & pounds")], "cm")
        + sel("ac-div", "Carrier type", "", [("6000", "Airline (IATA 6000 / 166)"), ("5000", "Express courier (5000 / 139)")], "6000")
        + f("ac-l", "Length", "per piece", 60)
        + f("ac-w", "Width", "per piece", 50)
        + f("ac-h", "Height", "per piece", 45)
        + f("ac-wt", "Actual weight", "per piece", 12)
        + f("ac-n", "Pieces", "", 4, "1", full=True)
        + '</div>' + result("ac", "Chargeable weight") + '</div>'
        + notes("Volumetric weight = L × W × H ÷ divisor\n  (cm³ ÷ 6000 or 5000 → kg; in³ ÷ 166 or 139 → lb)\nChargeable weight = max(actual, volumetric)\nRounded up to the next 0.5 kg (1 lb)",
                "Why light boxes cost more",
                "Aircraft run out of space before they run out of payload, so carriers bill bulky cargo by volume. A shipment is volumetric when it is lighter than 167 kg per cubic metre for airlines (200 kg for couriers). Smaller cartons and less void fill often cut the bill more than lighter packaging.")),
    "cpk": (
        '<h1>Cpk &amp; Process Capability Calculator</h1>'
        '<p class="lede">Cp, Cpk and the expected parts per million outside specification, from the process mean and standard deviation or from pasted measurements.</p>'
        '<div class="grid"><div class="fields">'
        + f("cp-lsl", "Lower spec limit", "LSL", 9.90)
        + f("cp-usl", "Upper spec limit", "USL", 10.10)
        + f("cp-mean", "Process mean", "x̄", 10.02)
        + f("cp-sd", "Standard deviation", "σ", 0.025)
        + '<div class="f full"><label for="cp-data">Or paste measurements <span class="u">overrides mean and σ</span></label>'
          '<textarea id="cp-data" rows="3" placeholder="10.01 10.03 9.99 10.04 …  (spaces, commas or new lines)"></textarea></div>'
        + '</div>' + result("cp", "Cpk") + '</div>'
        + notes("Cp  = (USL − LSL) ÷ 6σ\nCpu = (USL − mean) ÷ 3σ\nCpl = (mean − LSL) ÷ 3σ\nCpk = min(Cpu, Cpl)\nPPM = normal tail beyond each limit × 1,000,000",
                "What the numbers mean",
                "Cp shows how wide the process is compared with the tolerance; Cpk also accounts for how far the mean sits from the centre. A Cpk of 1.33 is the usual minimum for production parts and 1.67 for safety or new-part approval.")),
}

JS = r"""
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
"""

FNS = '"cbm":cbm,"air-chargeable":airChg,"cpk":cpk,'

CSS = """
textarea{width:100%;font:.95rem var(--mono);color:var(--ink);background:var(--panel);border:1px solid var(--line);border-radius:4px;padding:8px 10px;resize:vertical}
textarea:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
"""
