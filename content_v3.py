"""v3 pages: AQL sampling, compressed air leak cost, LTL freight class. Categories updated for the new sections."""

CATEGORY_V3 = {
    "aql-sampling-calculator": "Production & quality",
    "compressed-air-leak-cost-calculator": "Production & quality",
    "freight-class-calculator": "Logistics & trade",
}
RENAME = {"Production": "Production & quality"}
ORDER_V3 = ["Costing", "Production & quality", "Logistics & trade", "Pricing & investment"]

PAGES_V3 = [
    {
        "slug": "aql-sampling-calculator",
        "section": "aql",
        "title": "AQL Sampling Calculator – ISO 2859-1 / ANSI Z1.4 Sample Size",
        "description": "Find the AQL sample size and accept/reject numbers for critical, major and minor defects from lot size and inspection level, then check pass or fail.",
        "nav": "AQL sampling",
        "blurb": "Sample size and accept/reject numbers for a shipment inspection, with a pass/fail check.",
        "guide": [
            ("What AQL inspection decides", """
<p>Checking every unit in a shipment is slow and expensive, so buyers and quality teams inspect a random sample instead. AQL sampling, defined in ISO 2859-1 and its American twin ANSI/ASQ Z1.4, tells you how big that sample must be and how many defective units it may contain before the whole lot is rejected.</p>
<p>The answer depends on three things: the lot size, the inspection level and the Acceptance Quality Limit you agreed for each class of defect. Critical defects make the product unsafe or illegal, major defects make it unlikely to be used or sold, and minor defects are cosmetic or small deviations.</p>"""),
            ("Worked example", """
<p>An order of 1,000 units at general inspection level II gives code letter J, which means a sample of 80 units.</p>
<table><tr><th>Defect class</th><th>AQL</th><th>Accept</th><th>Reject</th></tr>
<tr><td>Critical</td><td class="n">0</td><td class="n">0</td><td class="n">1</td></tr>
<tr><td>Major</td><td class="n">2.5</td><td class="n">5</td><td class="n">6</td></tr>
<tr><td>Minor</td><td class="n">4.0</td><td class="n">7</td><td class="n">8</td></tr></table>
<p>If the inspector finds 2 major and 3 minor defects and nothing critical, every count is within its accept number and the lot passes. Six major defects would fail it even if everything else were perfect.</p>"""),
            ("How the tables work", """
<p>Table 1 of the standard converts lot size and inspection level into a code letter, and each letter has a fixed sample size, from 2 units (A) to 2,000 units (R). Table 2-A then gives the accept and reject numbers for each AQL. Where the table shows an arrow instead of numbers, you move to the nearest plan in the arrow's direction and use that plan's sample size. This calculator follows those arrows for you, which is why different AQLs can produce different sample sizes. In practice inspectors pull the largest sample and check it for all classes.</p>"""),
            ("Common mistakes", """
<ul>
<li><b>Reading AQL as the defect rate you will receive.</b> AQL 2.5 does not mean the lot contains 2.5% defects; it is the worst average quality the plan accepts most of the time.</li>
<li><b>Counting defects per unit wrongly.</b> One unit with two major defects counts as one defective unit unless your agreement says otherwise.</li>
<li><b>Changing the level after seeing results.</b> Agree level II, or level III for a new supplier, before inspection.</li>
</ul>"""),
        ],
        "faq": [
            ("What AQL is standard for consumer goods?", "A common choice is 0 for critical defects, 2.5 for major and 4.0 for minor, at general inspection level II."),
            ("What is the difference between level I, II and III?", "Level II is the default. Level I uses smaller samples when quality history is good; level III uses larger samples for new suppliers or after problems."),
            ("Is ANSI Z1.4 the same as ISO 2859-1?", "The sampling tables are practically the same for normal single sampling, so the sample sizes and accept numbers match."),
            ("What happens when the sample is larger than the lot?", "Inspect every unit. The calculator caps the sample at the lot size and flags it."),
        ],
    },
    {
        "slug": "compressed-air-leak-cost-calculator",
        "section": "air-leak",
        "title": "Compressed Air Leak Cost Calculator – Annual Cost & Payback",
        "description": "Estimate the yearly electricity cost of compressed air leaks from leak count, hole size or flow, compressor power and hours, plus the payback of repairs.",
        "nav": "Air leak cost",
        "blurb": "Yearly electricity lost to compressed air leaks and the payback of fixing them.",
        "guide": [
            ("Why leaks are expensive", """
<p>Compressed air is one of the most expensive utilities in a factory: a compressor turns only a small share of its electricity into useful air power. Leaks waste that air around the clock, often 20–30% of a compressor's output in plants without a leak programme, and they are silent enough to ignore until someone puts a number on them.</p>"""),
            ("Worked example", """
<p>A plant with 20 leaks the size of a 1/16-inch hole, about 4 CFM each at 100 psi, loses 80 CFM. At a typical 20 kW per 100 CFM that is 16 kW of compressor power.</p>
<table><tr><th>Item</th><th>Value</th></tr>
<tr><td>Energy (16 kW × 6,000 h)</td><td class="n">96,000 kWh</td></tr>
<tr><td>Cost at $0.12 per kWh</td><td class="n">$11,520 / year</td></tr>
<tr><td>Cost per leak</td><td class="n">$576 / year</td></tr>
<tr><td>Repair round (20 × $50)</td><td class="n">$1,000</td></tr>
<tr><td><b>Payback</b></td><td class="n"><b>32 days</b></td></tr></table>"""),
            ("Getting the inputs right", """
<ul>
<li><b>Flow per leak:</b> an ultrasonic leak detector gives the best estimate. The presets are typical flows at about 100 psi; at lower pressure, leaks lose less.</li>
<li><b>Specific power:</b> modern rotary screw compressors use roughly 16–22 kW per 100 CFM at full load. Part-load operation makes each leaked CFM more expensive, not less.</li>
<li><b>Hours:</b> use the hours the system is pressurised, not the hours production runs. Many systems stay pressurised over weekends.</li>
</ul>"""),
        ],
        "faq": [
            ("How much does a 1/4-inch air leak cost?", "At 100 psi a 1/4-inch leak passes roughly 60 CFM. At 20 kW per 100 CFM, 6,000 hours and $0.12 per kWh that is about $8,600 a year."),
            ("How do I convert l/s to CFM?", "Multiply litres per second by 2.119. 10 l/s is about 21 CFM."),
            ("What percentage of compressed air is lost to leaks?", "Surveys commonly find 20–30% in plants without a regular leak programme, and under 10% in well-managed systems."),
            ("Should I lower the system pressure too?", "Yes. Leak flow falls with pressure, so reducing pressure by even 1 bar cuts leak losses and compressor energy."),
        ],
    },
    {
        "slug": "freight-class-calculator",
        "section": "freight-class",
        "title": "LTL Freight Class Calculator – 2025 NMFC 13-Tier Density Scale",
        "description": "Calculate pallet density and LTL freight class under the 2025 NMFC density scale (class 50 to 400), compared with the old scale. Inches or centimetres.",
        "nav": "Freight class",
        "blurb": "Density and LTL freight class for a pallet under the 2025 NMFC scale.",
        "guide": [
            ("What changed in July 2025", """
<p>Less-than-truckload carriers in the United States price freight by class: the lower the class, the cheaper the rate per hundredweight. On July 19, 2025 the National Motor Freight Classification moved many more commodities to density-based classes and expanded the density scale from 11 to 13 tiers. The old top band, 30 pounds per cubic foot and denser, was split into three: class 60, class 55 and class 50. Very dense freight can now rate lower than before, while light, bulky freight can rate much higher.</p>"""),
            ("The 2025 density scale", """
<table><tr><th>Density (lb per ft³)</th><th>Class</th></tr>
<tr><td>Under 1</td><td class="n">400</td></tr><tr><td>1 to under 2</td><td class="n">300</td></tr>
<tr><td>2 to under 4</td><td class="n">250</td></tr><tr><td>4 to under 6</td><td class="n">175</td></tr>
<tr><td>6 to under 8</td><td class="n">125</td></tr><tr><td>8 to under 10</td><td class="n">100</td></tr>
<tr><td>10 to under 12</td><td class="n">92.5</td></tr><tr><td>12 to under 15</td><td class="n">85</td></tr>
<tr><td>15 to under 22.5</td><td class="n">70</td></tr><tr><td>22.5 to under 30</td><td class="n">65</td></tr>
<tr><td>30 to under 35</td><td class="n">60</td></tr><tr><td>35 to under 50</td><td class="n">55</td></tr>
<tr><td>50 or more</td><td class="n">50</td></tr></table>"""),
            ("Worked example", """
<p>A standard 48 × 40-inch pallet stacked to 48 inches high and weighing 500 pounds occupies 53.3 cubic feet, so its density is 9.38 pounds per cubic foot: class 100. Adding about 34 pounds would lift the density to 10 and drop the shipment to class 92.5. Measuring and weighing accurately matters, because carriers re-weigh and re-measure and bill the corrected class.</p>"""),
            ("Common mistakes", """
<ul>
<li><b>Measuring the box, not the pallet.</b> Use the outside dimensions of the whole handling unit, including the pallet and any overhang.</li>
<li><b>Forgetting the pallet weight.</b> A wooden pallet adds 30–50 pounds.</li>
<li><b>Assuming density always applies.</b> Some commodities have a fixed class in their NMFC item. Check the item before booking.</li>
</ul>"""),
        ],
        "faq": [
            ("How do I calculate freight density?", "Multiply length, width and height in inches, divide by 1,728 to get cubic feet, then divide the weight in pounds by the cubic feet."),
            ("What freight class is 10 pounds per cubic foot?", "Class 92.5 on the current scale, which covers 10 to under 12 pounds per cubic foot."),
            ("Why did my freight class change in 2025?", "The NMFC moved many items to density-based rating and added classes 55 and 50 for very dense freight, so the same pallet can now rate differently."),
            ("Does freight class apply outside the US?", "The NMFC is used for LTL freight within North America. Other regions usually price by weight or volumetric weight."),
        ],
    },
]
