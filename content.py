"""Long-form guide text for each calculator page (English). Kept separate from build.py so it is easy to edit.

Each entry: slug, section id in sections.json, <title>, meta description, nav label, card blurb,
guide sections (list of (h2, html)), faq (list of (q, a)).
"""

PAGES = [
    {
        "slug": "landed-cost-calculator",
        "section": "landed-cost",
        "title": "Landed Cost Calculator (CIF & FOB Duty) – Free | EverySolver",
        "description": "Calculate the landed cost per unit of imported goods: freight, insurance, duty on CIF or FOB value, customs and broker fees. Free, no sign-up.",
        "nav": "Landed cost",
        "blurb": "True cost of an imported part after freight, insurance, duty and fees.",
        "guide": [
            ("What landed cost means", """
<p>Landed cost is the total amount you pay to get one unit of a product from the supplier's factory onto your own shop floor. The supplier's invoice price is only the first line. Freight, cargo insurance, import duty, customs brokerage, port charges and the truck from the port all add to it, and for low-value or bulky parts they can add 20–40% on top of the purchase price.</p>
<p>If you quote your own selling price from the supplier price alone, every one of those costs comes straight out of your margin. Landed cost is the number that belongs in your bill of materials and your pricing sheet.</p>"""),
            ("Worked example", """
<p>The default values above describe a typical small shipment: 5,000 parts at $4.20 each on FOB terms, sea freight of $1,850, insurance at 0.5% of the goods value, a 6.5% duty rate, $320 of broker and customs fees and $410 of port and inland handling.</p>
<table><tr><th>Step</th><th>Amount</th></tr>
<tr><td>Goods (5,000 × $4.20)</td><td class="n">$21,000.00</td></tr>
<tr><td>Freight</td><td class="n">$1,850.00</td></tr>
<tr><td>Insurance (0.5% of goods)</td><td class="n">$105.00</td></tr>
<tr><td>Duty base, CIF</td><td class="n">$22,955.00</td></tr>
<tr><td>Duty (6.5%)</td><td class="n">$1,492.08</td></tr>
<tr><td>Fees + handling</td><td class="n">$730.00</td></tr>
<tr><td><b>Landed cost</b></td><td class="n"><b>$25,177.08</b></td></tr></table>
<p>That is about $5.04 per unit, roughly 20% more than the $4.20 on the invoice. Switch the duty basis to FOB and the duty falls to $1,365, because freight and insurance are no longer taxed.</p>"""),
            ("CIF or FOB: which duty basis applies", """
<p>Countries disagree on what the duty is charged on. The European Union, the United Kingdom, South Korea, China, Japan, Australia and most other countries charge duty on the <b>CIF value</b>: the goods plus the cost of insurance and freight to the border. The United States and Canada charge duty on the <b>FOB value</b>, so international freight and insurance stay out of the duty base.</p>
<p>The difference grows with freight cost. Heavy, cheap items shipped by air can carry freight equal to half their value, and on a CIF basis you pay duty on that freight too.</p>"""),
            ("Common mistakes", """
<ul>
<li><b>Using the wrong duty rate.</b> The rate depends on the HS code and the country of origin. Free-trade agreements can cut it to zero, but only with a valid certificate of origin.</li>
<li><b>Forgetting fixed fees on small shipments.</b> A $300 broker fee is 1% of a $30,000 container but 15% of a $2,000 air parcel.</li>
<li><b>Ignoring VAT or GST.</b> Import VAT is usually recoverable for registered businesses, so this calculator leaves it out. If you cannot reclaim it, add it to the other costs.</li>
<li><b>Spreading freight by unit count only.</b> If one shipment mixes large and small parts, allocate freight by weight or volume instead.</li>
</ul>"""),
        ],
        "faq": [
            ("Does landed cost include VAT?", "Usually not. Registered businesses can reclaim import VAT or GST, so it is a cash-flow item rather than a cost. If your business cannot reclaim it, add it to the handling field."),
            ("Where do I find the duty rate?", "Look up your product's HS code in the destination country's tariff schedule, for example the US HTS, the EU TARIC database or your national customs portal. Your customs broker can confirm it."),
            ("What is the difference between FOB and CIF?", "FOB is the value of the goods loaded on the ship at the origin port. CIF adds the cost of insurance and freight to the destination. Most countries charge duty on CIF; the US and Canada use FOB."),
            ("Should freight be split by quantity or by weight?", "For a single product, by quantity is fine. For mixed shipments, split freight by weight or volume so heavy parts carry their real share."),
        ],
    },
    {
        "slug": "cost-per-good-unit-calculator",
        "section": "cost-per-good-unit",
        "title": "Cost per Good Unit Calculator (Yield & Scrap) – Free | EverySolver",
        "description": "See the real unit cost after yield losses. Spread material, labor and overhead of rejected parts over the good units you can ship. Free calculator.",
        "nav": "Cost per good unit",
        "blurb": "Unit cost after yield losses, with the scrap cost hidden in every good part.",
        "guide": [
            ("Why the standard cost is too low", """
<p>A standard cost sheet usually adds material, labor and overhead for one unit and stops there. But no line runs at 100% yield. Every part that fails inspection used the same material, machine time and labor as a good one, and that cost has to be recovered from the parts you actually ship.</p>
<p>The cost per good unit puts that hidden cost back where it belongs. It is the figure to use when you quote prices, compare suppliers or decide whether a yield project is worth funding.</p>"""),
            ("Worked example", """
<p>With the default values, a batch of 12,000 units costs $2.80 of material and $1.65 of labor and overhead per unit started, and first-pass yield is 91.5%.</p>
<table><tr><th>Step</th><th>Amount</th></tr>
<tr><td>Cost of units started (12,000 × $4.45)</td><td class="n">$53,400.00</td></tr>
<tr><td>Good units (91.5%)</td><td class="n">10,980</td></tr>
<tr><td>Rejected units</td><td class="n">1,020</td></tr>
<tr><td>Salvage (1,020 × $0.15)</td><td class="n">−$153.00</td></tr>
<tr><td><b>Cost per good unit</b></td><td class="n"><b>$4.849</b></td></tr></table>
<p>The perfect-run cost is $4.45, so poor yield adds about 9% to every unit you sell.</p>"""),
            ("How yield changes unit cost", """
<p>The multiplier is simply 1 ÷ yield. At 80% each good part carries 1.25 parts' worth of cost; at 90%, 1.11; at 95%, 1.05; at 99%, 1.01. The curve is steep at low yields, which is why the first few points of improvement on an immature process are worth far more than the last few on a mature one.</p>
<table><tr><th>Yield</th><th>Cost multiplier</th></tr>
<tr><td>80%</td><td class="n">1.250</td></tr><tr><td>90%</td><td class="n">1.111</td></tr>
<tr><td>95%</td><td class="n">1.053</td></tr><tr><td>99%</td><td class="n">1.010</td></tr></table>"""),
            ("Common mistakes", """
<ul>
<li><b>Using final yield instead of first-pass yield.</b> If rejects are reworked and later pass, use the rework calculator for that cost and keep only true scrap here.</li>
<li><b>Applying yield to purchased parts that are not consumed.</b> If a rejected assembly can be stripped and its components reused, enter their value as salvage.</li>
<li><b>Multi-step lines.</b> Rolled throughput yield is the product of each step's yield. Three steps at 97% give 91.3%, not 97%.</li>
</ul>"""),
        ],
        "faq": [
            ("What is first-pass yield?", "The share of units that pass every inspection the first time, without rework. It is the honest measure of a process because rework hides losses."),
            ("How do I calculate yield for a multi-step process?", "Multiply the yield of each step. This is called rolled throughput yield. Enter the result as the first-pass yield."),
            ("Should overhead be included?", "Yes, if the rejected unit consumed machine time. Overhead that does not change with output, such as rent, is already spread over good units by your costing system."),
            ("What counts as salvage value?", "Anything you recover from a rejected unit: scrap metal sold by weight, reusable components, or a rebate from the material supplier."),
        ],
    },
    {
        "slug": "scrap-cost-calculator",
        "section": "scrap-cost",
        "title": "Scrap & Rework Cost Calculator – Yearly Quality Loss | EverySolver",
        "description": "Turn scrap and rework rates into a yearly money figure and see the saving from a lower target scrap rate. Free cost of poor quality calculator.",
        "nav": "Scrap & rework",
        "blurb": "Yearly money lost to scrap and rework, and the saving from a better rate.",
        "guide": [
            ("Put quality losses in money", """
<p>A scrap rate of 3% sounds small in a production meeting. A loss of $90,000 a year does not. This calculator turns scrap and rework percentages into a yearly cost so that an improvement project can be compared with any other investment.</p>
<p>It covers the two most visible parts of the cost of poor quality: parts thrown away and parts fixed by hand. Inspection labor, warranty claims and lost customers come on top.</p>"""),
            ("Worked example", """
<p>The defaults describe a line making 40,000 units a month at a full cost of $6.40 each, with 3.2% scrap, $0.40 salvage per scrapped part, 4.5% rework and $1.90 of labor per reworked part.</p>
<table><tr><th>Item</th><th>Per year</th></tr>
<tr><td>Scrapped units (40,000 × 3.2% × 12)</td><td class="n">15,360</td></tr>
<tr><td>Scrap loss (15,360 × ($6.40 − $0.40))</td><td class="n">$92,160</td></tr>
<tr><td>Rework loss (21,600 × $1.90)</td><td class="n">$41,040</td></tr>
<tr><td><b>Total quality loss</b></td><td class="n"><b>$133,200</b></td></tr></table>
<p>Cutting scrap to the 1.5% target saves $48,960 a year, which is the budget ceiling for the project that gets you there.</p>"""),
            ("Which unit cost to use", """
<p>Use the cost the part has absorbed at the step where it is rejected. A casting scrapped at incoming inspection costs its purchase price. The same casting scrapped after machining, plating and assembly carries all of that work. If your rejects happen at several stations, run the calculator once per station or use a weighted average.</p>"""),
            ("Common mistakes", """
<ul>
<li><b>Counting rework as free because the part is eventually shipped.</b> Rework uses labor, machine time and floor space, and it delays orders.</li>
<li><b>Using material cost only.</b> That understates the loss, often by half.</li>
<li><b>Setting a target that ignores the cause.</b> A target is useful only with a plan; use the saving to size what you can spend on fixtures, training or inspection.</li>
</ul>"""),
        ],
        "faq": [
            ("What is the cost of poor quality?", "All costs that would disappear if every part were made right the first time: scrap, rework, extra inspection, warranty and returns. This calculator covers scrap and rework."),
            ("Is a 3% scrap rate high?", "It depends on the process. Machining lines often run below 1%, while new products and complex assemblies can exceed 5%. Compare with your own trend rather than an industry average."),
            ("Should I include material I can sell as scrap?", "Yes, enter it as salvage value per scrapped unit. It reduces the loss."),
            ("How do I justify a quality project?", "Use the yearly saving at target as the benefit, then compare it with the project cost in the equipment payback calculator."),
        ],
    },
    {
        "slug": "break-even-calculator",
        "section": "break-even",
        "title": "Break-Even Calculator for Manufacturers – Units & Margin of Safety",
        "description": "Find the break-even volume, units needed for a target profit and the margin of safety for a product. Free contribution margin calculator.",
        "nav": "Break-even",
        "blurb": "Units per month before a product makes money, and how safe your forecast is.",
        "guide": [
            ("The break-even point", """
<p>Every unit you sell earns its contribution: the selling price minus the costs that rise with each unit. Contribution first pays the fixed costs that you carry whatever happens, such as rent, salaried staff and equipment leases. The break-even point is the volume where total contribution exactly covers those fixed costs. Below it you lose money; above it each extra unit adds its full contribution to profit.</p>"""),
            ("Worked example", """
<p>With fixed costs of $28,000 a month, a price of $24 and a variable cost of $13.50, each unit contributes $10.50.</p>
<table><tr><th>Item</th><th>Value</th></tr>
<tr><td>Break-even (28,000 ÷ 10.50)</td><td class="n">2,667 units</td></tr>
<tr><td>Units for $8,000 profit</td><td class="n">3,429 units</td></tr>
<tr><td>Profit at 3,500 expected sales</td><td class="n">$8,750</td></tr>
<tr><td>Margin of safety</td><td class="n">23.8%</td></tr></table>
<p>Sales could fall by almost a quarter before the product stops paying for itself.</p>"""),
            ("Fixed or variable?", """
<p>Variable costs change with each unit: material, purchased parts, packaging, piece-rate labor, sales commission and outbound shipping. Fixed costs stay flat within a normal range of output: rent, salaried staff, insurance, leases and depreciation. Some costs are mixed. Electricity has a fixed base charge and a variable part, and overtime turns fixed labor into variable labor at high volume. Split mixed costs as well as you can; the result is only as good as that split.</p>"""),
            ("Using the result", """
<ul>
<li><b>Pricing:</b> raising the price by $1 here lifts contribution by almost 10% and cuts break-even by about 230 units.</li>
<li><b>Make or buy:</b> buying a part instead of making it often turns fixed costs into variable ones, which lowers break-even but also lowers profit at high volume.</li>
<li><b>Forecast risk:</b> a margin of safety under 20% means a normal bad month can push the product into a loss.</li>
</ul>"""),
        ],
        "faq": [
            ("What is contribution margin?", "Selling price minus variable cost per unit. As a percentage of price it is the contribution margin ratio."),
            ("What is a good margin of safety?", "Above 20% is comfortable for most products. Below 10% means small forecast errors turn profit into loss."),
            ("Does break-even include depreciation?", "Yes, depreciation of equipment used for the product is a fixed cost. For a cash break-even, leave it out."),
            ("Can I use this for a whole factory?", "Yes, if you use average price and average variable cost for the product mix. Results become less reliable when the mix changes a lot."),
        ],
    },
    {
        "slug": "equipment-payback-calculator",
        "section": "payback",
        "title": "Equipment Payback, ROI, NPV & IRR Calculator for Machines | EverySolver",
        "description": "Check whether a new machine or automation cell pays for itself: simple payback, lifetime ROI, NPV and IRR with a cumulative cash flow chart. Free.",
        "nav": "Equipment payback",
        "blurb": "Payback period, ROI, NPV and IRR for a new machine or automation cell.",
        "guide": [
            ("Three ways to judge an investment", """
<p><b>Simple payback</b> answers how long until the savings have repaid the purchase price. It is easy to explain and favoured by plant managers, but it ignores what happens after the payback date.</p>
<p><b>ROI over the useful life</b> compares total net savings with the investment. It shows whether the machine earns its cost several times over or only just covers it.</p>
<p><b>IRR</b> is the discount rate at which NPV is exactly zero. Finance teams like it because it can be compared directly with the company's hurdle rate.</p>
<p><b>NPV</b> discounts each year's saving back to today at your cost of capital. A positive NPV means the machine earns more than the money would earn elsewhere at that rate. It is the strictest of the three.</p>"""),
            ("Worked example", """
<p>The defaults describe an automation cell costing $185,000 installed, saving $52,000 of labor and $14,000 of scrap a year, and adding $9,500 of power and maintenance, over a 7-year life at an 8% discount rate.</p>
<table><tr><th>Item</th><th>Value</th></tr>
<tr><td>Net saving per year</td><td class="n">$56,500</td></tr>
<tr><td>Simple payback</td><td class="n">3.3 years</td></tr>
<tr><td>Lifetime net saving</td><td class="n">$395,500</td></tr>
<tr><td>ROI over 7 years</td><td class="n">114%</td></tr>
<tr><td>NPV at 8%</td><td class="n">about $109,000</td></tr>
<tr><td>IRR</td><td class="n">23.6%</td></tr></table>
<p>An IRR of 23.6% means the machine returns the same as an investment earning 23.6% a year, well above an 8% cost of capital.</p>"""),
            ("What to include", """
<ul>
<li><b>Investment:</b> purchase price, freight, installation, utilities hook-up, guarding, tooling, programming and training.</li>
<li><b>Savings:</b> labor hours actually removed (not just freed up), scrap and rework avoided, energy saved, and subcontracting brought in-house.</li>
<li><b>Added costs:</b> power, consumables, maintenance contracts, spare parts and software licences.</li>
</ul>
<p>Labor savings are only real if the hours are removed or redeployed to work that earns money. If the operator stays and simply watches the machine, the saving is zero.</p>"""),
            ("Typical approval thresholds", """
<p>Many manufacturers approve projects that pay back in two to three years, and automation projects are often held to the same bar. Strategic investments, such as capacity for a new customer, may be approved on a longer payback if the NPV is positive. Use the discount rate your finance team uses for capital requests, often between 8% and 12%.</p>"""),
        ],
        "faq": [
            ("What is a good payback period for a machine?", "Under 2–3 years is the usual target for cost-saving equipment. Longer paybacks need a strong NPV or a strategic reason."),
            ("What discount rate should I use?", "Your company's weighted cost of capital or the hurdle rate finance sets for projects, typically 8–12%."),
            ("Why can payback be good but NPV negative?", "If the useful life is short, the machine may repay its cost but earn too little afterwards to beat the discount rate."),
            ("Does this include tax and depreciation?", "No. It is a pre-tax cash view, which is the usual first screen. Ask finance for the after-tax version before approval."),
        ],
    },
]

ABOUT = """
<h1>About EverySolver</h1>
<p>EverySolver is a growing set of free calculators that solve real work problems in plain numbers. The first section covers manufacturing and cost, for people who make and buy physical products: plant managers, cost accountants, buyers, importers and small makers. Each one answers a single cost question in plain numbers and shows the formula it uses, so you can check the result or rebuild it in a spreadsheet.</p>
<p>The calculators were written by someone who spent more than a decade developing production equipment and later worked in cost management, and kept rebuilding the same spreadsheets for every new project. The aim is to save you that time.</p>
<h2>How the numbers work</h2>
<p>All calculations run in your browser. Nothing you type is sent to a server or stored, except your currency choice, which your browser remembers for the next visit.</p>
<p>The results are estimates for planning. Duty rates, tax rules and accounting conventions vary by country and company, so confirm important figures with your customs broker, accountant or finance team.</p>
"""

PRIVACY = """
<h1>Privacy Policy</h1>
<p><i>Last updated: {date}</i></p>
<p>This site does not ask for or store personal information. Calculator inputs are processed in your browser and are not sent to us.</p>
<h2>Local storage</h2>
<p>The site saves your selected currency in your browser's local storage so that it is remembered on your next visit. You can clear it at any time in your browser settings.</p>
<h2>Advertising and cookies</h2>
<p>We may show advertising provided by Google AdSense. Third-party vendors, including Google, use cookies to serve ads based on a user's prior visits to this website or other websites. Google's use of advertising cookies enables it and its partners to serve ads to users based on their visit to this site and/or other sites on the Internet.</p>
<p>Users may opt out of personalised advertising by visiting <a href="https://www.google.com/settings/ads">Google Ads Settings</a>. You can also opt out of some third-party vendors' use of cookies for personalised advertising at <a href="https://www.aboutads.info/choices/">aboutads.info</a>.</p>
<h2>Analytics</h2>
<p>We may use privacy-friendly, aggregate visit statistics to understand which calculators are useful. These do not identify individual visitors.</p>
<h2>Hosting</h2>
<p>The site is hosted as static files. The hosting provider may keep standard server logs, such as IP addresses and request times, for security and operations.</p>
<h2>Contact</h2>
<p>Questions about this policy: <a href="mailto:contact@everysolver.com">contact@everysolver.com</a>.</p>
<h2>Changes</h2>
<p>If this policy changes, the date above will be updated.</p>
"""
