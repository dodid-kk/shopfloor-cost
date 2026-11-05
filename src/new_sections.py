"""New calculator sections (markup) and logic, merged into sections.json / calc.js by patch step in build_sections.py."""

def f(id_, label, unit, value, step="any", full=False):
    cls = "f full" if full else "f"
    return (f'<div class="{cls}"><label for="{id_}">{label} <span class="u">{unit}</span></label>'
            f'<input id="{id_}" type="number" step="{step}" value="{value}" inputmode="decimal"></div>')


def result(prefix, kicker, svg=False, pill=True):
    chart = (f'<svg id="{prefix}-svg" viewBox="0 0 320 120" width="100%" role="img" aria-label="Chart" style="margin-top:14px;max-width:100%"></svg>'
             if svg else f'<div class="bar" id="{prefix}-bar"></div><div class="legend" id="{prefix}-leg"></div>')
    return (f'<div class="result" aria-live="polite"><div class="kicker">{kicker}</div><div class="big" id="{prefix}-out">–</div>'
            f'<div class="sub" id="{prefix}-sub"></div>{chart}<table class="bd" id="{prefix}-tbl"></table>'
            + (f'<div id="{prefix}-pill"></div>' if pill else "") + '</div>')


def notes(how, title2, body2):
    return (f'<div class="ad">AD SLOT · 728×90 / responsive</div><div class="notes"><div><h2>How it works</h2>'
            f'<code class="fx">{how}</code></div><div><h2>{title2}</h2><p>{body2}</p></div></div>')


SECTIONS = {
    "machine-hour-rate": (
        '<h1>Machine Hour Rate Calculator</h1>'
        '<p class="lede">Work out what one hour of a machine really costs: depreciation, interest on capital, floor space, maintenance and power. Use it to quote jobs and to compare in-house work with subcontracting.</p>'
        '<div class="grid"><div class="fields">'
        + f("mh-price", "Machine price", "installed", 250000)
        + f("mh-resid", "Residual value", "at end of life", 25000)
        + f("mh-life", "Useful life", "years", 10, "1")
        + f("mh-int", "Interest rate", "% / year", 6)
        + f("mh-hrs", "Hours per shift", "h", 8)
        + f("mh-shifts", "Shifts per day", "", 2, "1")
        + f("mh-days", "Working days", "per year", 250, "1")
        + f("mh-util", "Utilisation", "% of available time", 75)
        + f("mh-area", "Floor space", "m² or ft²", 20)
        + f("mh-rent", "Space cost", "per m² (or ft²) / year", 120)
        + f("mh-maint", "Maintenance", "per year", 6000)
        + f("mh-kw", "Connected load", "kW", 15)
        + f("mh-load", "Average load", "% of connected", 60)
        + f("mh-elec", "Electricity price", "per kWh", 0.18)
        + f("mh-wage", "Operator cost", "per hour, burdened", 38, full=True)
        + '</div>' + result("mh", "Machine rate per hour", pill=False) + '</div>'
        + notes("Running hours = hours × shifts × days × utilisation\nDepreciation  = (price − residual) ÷ life\nInterest      = (price + residual) ÷ 2 × rate\nFixed / hour  = (depreciation + interest + space\n                + maintenance) ÷ running hours\nEnergy / hour = kW × load × price per kWh\nRate          = fixed / hour + energy / hour",
                "Why utilisation matters",
                "Fixed costs are spread over the hours the machine actually runs. Halving utilisation doubles the fixed cost per hour, which is why an idle machine is expensive even when it is paid off.")),
    "oee": (
        '<h1>OEE Calculator</h1>'
        '<p class="lede">Overall Equipment Effectiveness from one shift of data: availability, performance and quality, plus how many minutes each loss cost you.</p>'
        '<div class="grid"><div class="fields">'
        + f("oe-planned", "Planned production time", "minutes", 420)
        + f("oe-down", "Unplanned downtime", "minutes", 47)
        + f("oe-ideal", "Ideal cycle time", "seconds per unit", 1.0)
        + f("oe-total", "Total units produced", "units", 19271, "1")
        + f("oe-good", "Good units", "units", 18848, "1", full=True)
        + '</div>' + result("oe", "OEE") + '</div>'
        + notes("Run time     = planned time − downtime\nAvailability = run time ÷ planned time\nPerformance  = ideal cycle × total count ÷ run time\nQuality      = good count ÷ total count\nOEE          = availability × performance × quality",
                "What is a good OEE?",
                "85% is the commonly quoted world-class benchmark, and many plants run between 40% and 60%. The trend on your own line matters more than the benchmark; the loss breakdown shows where to start.")),
    "takt-time": (
        '<h1>Takt Time Calculator</h1>'
        '<p class="lede">The pace a line must run to meet customer demand, the number of stations or operators it needs, and whether your bottleneck can keep up.</p>'
        '<div class="grid"><div class="fields">'
        + f("tk-shift", "Shift length", "minutes", 480)
        + f("tk-breaks", "Breaks & meetings", "minutes per shift", 50)
        + f("tk-shifts", "Shifts per day", "", 2, "1")
        + f("tk-demand", "Customer demand", "units per day", 1200, "1")
        + f("tk-work", "Total work content", "seconds per unit", 210)
        + f("tk-bottle", "Bottleneck cycle time", "seconds", 45)
        + '</div>' + result("tk", "Takt time") + '</div>'
        + notes("Available time = (shift − breaks) × shifts\nTakt time      = available time ÷ demand\nStations       = work content ÷ takt (round up)\nMax output     = available time ÷ bottleneck cycle",
                "Takt vs cycle time",
                "Takt time is set by the customer; cycle time is how fast your process actually runs. If any station's cycle time is longer than takt, that station is a bottleneck and the line cannot meet demand without overtime, an extra shift or rebalancing.")),
    "pricing": (
        '<h1>Margin &amp; Markup Price Calculator</h1>'
        '<p class="lede">Set a selling price from your unit cost and target margin, including marketplace or distributor fees, and see the markup that gets you there.</p>'
        '<div class="grid"><div class="fields">'
        + f("pr-cost", "Unit cost", "landed / full cost", 18.40)
        + f("pr-margin", "Target gross margin", "% of price", 35)
        + f("pr-fee", "Channel fee", "% of price", 0)
        + f("pr-pay", "Payment fee", "% of price", 0)
        + f("pr-fixed", "Fixed fee per order", "per unit", 0, full=True)
        + '</div>' + result("pr", "Selling price") + '</div>'
        + notes("Price  = (cost + fixed fee) ÷ (1 − margin − fees)\nMarkup = (price − cost) ÷ cost\nMargin = profit ÷ price",
                "Margin is not markup",
                "A 35% markup on cost gives only a 25.9% margin on price. Quoting a markup when the business plan assumes a margin is one of the most common pricing mistakes in small manufacturers.")),
}

JS = r"""
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
"""

FNS = '"machine-hour-rate":machineRate,"oee":oee,"takt-time":takt,"pricing":pricing,'
