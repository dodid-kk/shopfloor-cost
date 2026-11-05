"""v2 additions: four new calculator pages and the category of every page."""

CATEGORY = {
    "landed-cost-calculator": "Costing", "cost-per-good-unit-calculator": "Costing",
    "machine-hour-rate-calculator": "Costing", "scrap-cost-calculator": "Costing",
    "oee-calculator": "Production", "takt-time-calculator": "Production",
    "margin-markup-calculator": "Pricing & investment", "break-even-calculator": "Pricing & investment",
    "equipment-payback-calculator": "Pricing & investment",
}
CATEGORY_ORDER = ["Costing", "Production", "Pricing & investment"]

NEW_PAGES = [
    {
        "slug": "machine-hour-rate-calculator",
        "section": "machine-hour-rate",
        "title": "Machine Hour Rate Calculator – Cost per Machine Hour | EverySolver",
        "description": "Calculate the hourly cost of a machine from depreciation, interest, floor space, maintenance and energy, with or without the operator. Free.",
        "nav": "Machine hour rate",
        "blurb": "Hourly cost of a machine for quoting, with or without the operator.",
        "guide": [
            ("What the machine hour rate is for", """
<p>Job shops quote work in machine hours. If the hourly rate is too low, every job loses a little money and nobody notices until the year-end figures arrive. If it is too high, you lose quotes you could have won. The machine hour rate collects every cost of owning and running a machine and divides it by the hours it actually runs.</p>
<p>It is also the right number for make-or-buy decisions: compare it, plus operator and material, with the subcontractor's price.</p>"""),
            ("Worked example", """
<p>The default values describe a $250,000 machining centre with a $25,000 residual value after 10 years, running two 8-hour shifts on 250 days at 75% utilisation.</p>
<table><tr><th>Item</th><th>Per year</th></tr>
<tr><td>Running hours (8 × 2 × 250 × 75%)</td><td class="n">3,000 h</td></tr>
<tr><td>Depreciation (225,000 ÷ 10)</td><td class="n">$22,500</td></tr>
<tr><td>Interest on average capital (6%)</td><td class="n">$8,250</td></tr>
<tr><td>Floor space (20 m² × $120)</td><td class="n">$2,400</td></tr>
<tr><td>Maintenance</td><td class="n">$6,000</td></tr>
<tr><td>Fixed cost per hour (39,150 ÷ 3,000)</td><td class="n">$13.05</td></tr>
<tr><td>Energy per hour (15 kW × 60% × $0.18)</td><td class="n">$1.62</td></tr>
<tr><td><b>Machine rate</b></td><td class="n"><b>$14.67 / h</b></td></tr></table>
<p>Adding a burdened operator cost of $38 an hour gives $52.67 an hour for quoting.</p>"""),
            ("What to leave out", """
<ul>
<li><b>Tooling and consumables</b> that vary strongly by job are better charged to the job directly.</li>
<li><b>General overhead</b> such as office staff and sales is usually added as a separate overhead rate on top of the machine rate.</li>
<li><b>Interest</b> is included because money tied up in the machine could earn a return elsewhere. Some companies leave it out; be consistent across machines.</li>
</ul>"""),
        ],
        "faq": [
            ("How do I calculate machine hour rate?", "Add yearly depreciation, interest on capital, floor space and maintenance, divide by running hours, then add energy cost per hour. Add the operator's burdened hourly cost if you quote labour and machine together."),
            ("Should I use available hours or running hours?", "Running hours. Dividing by available hours makes the rate look cheaper than it is because the machine does not earn during idle time."),
            ("What utilisation should I assume?", "Use your own history. Job shops often run 50–75% of scheduled time; dedicated production cells can exceed 85%."),
            ("Why is interest on average capital (price + residual) ÷ 2?", "The capital tied up falls from the full price to the residual value over the machine's life, so the average is the midpoint."),
        ],
    },
    {
        "slug": "oee-calculator",
        "section": "oee",
        "title": "OEE Calculator – Availability, Performance, Quality & Losses",
        "description": "Calculate OEE from planned time, downtime, ideal cycle time and counts. See availability, performance, quality and minutes lost to each loss.",
        "nav": "OEE",
        "blurb": "Availability, performance and quality from one shift, with the minutes lost to each.",
        "guide": [
            ("What OEE measures", """
<p>Overall Equipment Effectiveness compares what a machine produced with what it could have produced in the time it was scheduled to run. It multiplies three ratios: <b>availability</b> (was it running?), <b>performance</b> (was it running at full speed?) and <b>quality</b> (were the parts good?). A machine that runs all shift at full speed with no rejects scores 100%.</p>
<p>The single number is useful for tracking, but the value is in the breakdown. Turning each loss into minutes shows where an improvement project will pay most.</p>"""),
            ("Worked example", """
<p>The defaults use a classic shift: 420 minutes of planned production, 47 minutes of breakdowns, an ideal cycle of 1 second, 19,271 parts made and 18,848 good.</p>
<table><tr><th>Factor</th><th>Value</th></tr>
<tr><td>Availability (373 ÷ 420)</td><td class="n">88.8%</td></tr>
<tr><td>Performance (19,271 s ÷ 22,380 s)</td><td class="n">86.1%</td></tr>
<tr><td>Quality (18,848 ÷ 19,271)</td><td class="n">97.8%</td></tr>
<tr><td><b>OEE</b></td><td class="n"><b>74.8%</b></td></tr></table>
<p>Of the 420 minutes, about 314 were fully productive. Breakdowns cost 47 minutes, slow cycles and small stops about 52, and defects about 7. Speed loss is the biggest item here, which is easy to miss if you only track downtime.</p>"""),
            ("Getting the inputs right", """
<ul>
<li><b>Planned production time</b> excludes planned stops such as breaks and scheduled maintenance, but includes changeovers, which are a loss.</li>
<li><b>Ideal cycle time</b> is the fastest the machine can run the part, from the nameplate or the best sustained rate you have seen. Using a slow standard hides speed losses and can push performance above 100%.</li>
<li><b>Counts</b> must cover the same period as the time figures.</li>
</ul>"""),
        ],
        "faq": [
            ("What is a good OEE score?", "85% is the widely quoted world-class benchmark. Many discrete manufacturers run between 40% and 60%. Track your own trend first."),
            ("Why is my performance above 100%?", "The ideal cycle time is set too slow. Use the true fastest cycle the machine can sustain."),
            ("Are changeovers availability losses?", "Yes, in standard OEE changeovers count as downtime. Planned breaks and scheduled maintenance are excluded from planned production time instead."),
            ("What is the difference between OEE and TEEP?", "OEE measures against planned production time. TEEP measures against all calendar time, so it also captures unscheduled shifts and weekends."),
        ],
    },
    {
        "slug": "takt-time-calculator",
        "section": "takt-time",
        "title": "Takt Time Calculator – Line Balance, Stations & Bottleneck",
        "description": "Calculate takt time from available time and demand, the number of stations or operators needed, line balance and whether the bottleneck keeps up.",
        "nav": "Takt time",
        "blurb": "Pace needed to meet demand, stations required and a bottleneck check.",
        "guide": [
            ("Takt time in one sentence", """
<p>Takt time is the available production time divided by customer demand: the rhythm at which one finished unit must leave the line. If demand is 1,200 units and you have 860 minutes, a unit has to come off the line every 43 seconds.</p>
<p>It turns a sales forecast into a design target for the line. Every station's cycle time must be at or below takt, and the total work content divided by takt tells you the minimum number of stations or operators.</p>"""),
            ("Worked example", """
<p>Two 8-hour shifts with 50 minutes of breaks each give 860 minutes, or 51,600 seconds, a day. Demand is 1,200 units and each unit needs 210 seconds of work in total.</p>
<table><tr><th>Item</th><th>Value</th></tr>
<tr><td>Takt time (51,600 ÷ 1,200)</td><td class="n">43.0 s</td></tr>
<tr><td>Stations needed (210 ÷ 43, rounded up)</td><td class="n">5</td></tr>
<tr><td>Line balance efficiency (210 ÷ (5 × 43))</td><td class="n">97.7%</td></tr>
<tr><td>Max output with a 45 s bottleneck</td><td class="n">1,146 / day</td></tr></table>
<p>The bottleneck station is 2 seconds slower than takt, so the line falls 54 units a day short. Moving a few seconds of work to another station fixes it without overtime.</p>"""),
            ("Using takt time well", """
<ul>
<li>Recalculate takt when demand changes; a fixed line speed that ignores demand builds inventory or misses orders.</li>
<li>Leave headroom. Running every station at exactly takt means any small stop causes a shortfall, so many lines plan for 85–95% of takt.</li>
<li>Takt time is a demand figure. It does not change when the machine gets faster; cycle time does.</li>
</ul>"""),
        ],
        "faq": [
            ("How do you calculate takt time?", "Divide the net available production time by customer demand for the same period. Subtract breaks and planned stops from the shift time first."),
            ("What is the difference between takt time and cycle time?", "Takt time is the pace demand requires. Cycle time is how long a station or process actually takes. Cycle time must be at or below takt."),
            ("How many operators do I need?", "Total work content per unit divided by takt time, rounded up. Balance the work so no station exceeds takt."),
            ("What is line balance efficiency?", "Total work content divided by the number of stations times takt. 100% means no station waits; 85–95% is a realistic target."),
        ],
    },
    {
        "slug": "margin-markup-calculator",
        "section": "pricing",
        "title": "Margin & Markup Calculator – Selling Price from Cost and Fees",
        "description": "Find the selling price that hits your target gross margin after channel and payment fees, and see the equivalent markup. Free margin vs markup calculator.",
        "nav": "Margin & markup",
        "blurb": "Selling price for a target margin after fees, and the markup it implies.",
        "guide": [
            ("Margin and markup are different numbers", """
<p>Markup is profit as a share of cost. Margin is profit as a share of the selling price. On the same sale the markup is always the larger number: a part that costs $10 and sells for $15 has a 50% markup but only a 33% margin. Business plans and accountants usually speak in margin, while sales teams often quote markup, and the gap between them quietly eats profit.</p>"""),
            ("Worked example", """
<p>A part with a full unit cost of $18.40 and a 35% target margin needs a price of $18.40 ÷ (1 − 0.35) = $28.31. That is a markup of 53.8% on cost.</p>
<table><tr><th>Markup on cost</th><th>Margin on price</th></tr>
<tr><td class="n">25%</td><td class="n">20.0%</td></tr><tr><td class="n">35%</td><td class="n">25.9%</td></tr>
<tr><td class="n">50%</td><td class="n">33.3%</td></tr><tr><td class="n">100%</td><td class="n">50.0%</td></tr></table>
<p>Selling through a marketplace or distributor that takes 15% of the price changes the formula to cost ÷ (1 − margin − fee). With the same cost and margin the price becomes $36.80.</p>"""),
            ("Which cost to start from", """
<p>Start from the full cost of the unit: landed cost for bought-in goods, or material plus conversion cost adjusted for yield for parts you make. The other calculators on this site give you those figures. Starting from the supplier price or the material cost alone sets a price that looks profitable and is not.</p>"""),
        ],
        "faq": [
            ("How do I convert markup to margin?", "Margin = markup ÷ (1 + markup). A 50% markup is a 33.3% margin."),
            ("How do I convert margin to markup?", "Markup = margin ÷ (1 − margin). A 40% margin needs a 66.7% markup."),
            ("How do marketplace fees change the price?", "Fees charged as a percentage of the price must come out of the price too, so divide cost by (1 − margin − fee percentage)."),
            ("What margin should a manufacturer target?", "It varies widely by industry. Gross margins of 25–40% are common for discrete manufacturers; compare with your own overhead and the margin your market accepts."),
        ],
    },
]

CONTACT = """
<h1>Contact</h1>
<p>Found an error in a formula, need a calculator that is not here, or want to suggest an improvement? Please open a short request on our public tracker. No account details or personal data are needed beyond what GitHub itself asks for.</p>
<p><a href="https://github.com/dodid-kk/shopfloor-cost/issues/new?title=Calculator%20request%3A%20&labels=request">Request a calculator or report an error →</a></p>
<p>Requests that come up more than once are added first. Corrections to formulas are checked and published within a few days.</p>
"""
