"""v4 pages: CBM & container loading, air freight chargeable weight, Cpk."""

CATEGORY_V4 = {
    "cbm-container-calculator": "Logistics & trade",
    "air-freight-chargeable-weight-calculator": "Logistics & trade",
    "cpk-calculator": "Production & quality",
}

PAGES_V4 = [
    {
        "slug": "cbm-container-calculator",
        "section": "cbm",
        "title": "CBM Calculator & Container Loading – 20ft, 40ft, 40ft HC Fill",
        "description": "Calculate shipment CBM and weight from carton size and count, see how full a 20ft, 40ft or 40ft high-cube container would be, and when LCL is cheaper.",
        "nav": "CBM & container",
        "blurb": "Shipment cubic metres, container fill and the LCL vs FCL decision.",
        "guide": [
            ("Why CBM drives the sea freight bill", """
<p>Ocean freight is sold by space. A full container (FCL) has a fixed price whatever you put in it, while less-than-container (LCL) cargo is billed per cubic metre or per tonne, whichever is larger. Knowing the cubic metres of a shipment before you book tells you which container to ask for, whether LCL or FCL is cheaper, and how many cartons you can add to fill the space you are already paying for.</p>"""),
            ("Worked example", """
<p>250 cartons of 60 × 40 × 40 cm weighing 18 kg each:</p>
<table><tr><th>Item</th><th>Value</th></tr>
<tr><td>CBM per carton (0.6 × 0.4 × 0.4)</td><td class="n">0.096 m³</td></tr>
<tr><td>Total volume</td><td class="n">24.00 m³</td></tr>
<tr><td>Total weight</td><td class="n">4,500 kg</td></tr>
<tr><td>20ft fill (28 m³ loadable)</td><td class="n">86%</td></tr>
<tr><td>Cartons that would fit by volume</td><td class="n">about 291</td></tr>
<tr><td>LCL charge basis</td><td class="n">24.00 revenue tons</td></tr></table>
<p>The load fits one 20ft container with room for about 40 more cartons. At 24 m³ a full 20ft is almost always cheaper than paying LCL rates on 24 revenue tons.</p>"""),
            ("LCL or FCL?", """
<p>LCL is billed per revenue ton: the larger of the volume in cubic metres and the weight in tonnes. It also carries consolidation and terminal fees on both ends. As a rule of thumb, once a shipment passes 13–15 m³ a 20ft container usually costs the same or less, and it is handled less, which means less damage. Ask for both quotes around that size.</p>"""),
            ("Common mistakes", """
<ul>
<li><b>Planning to the internal volume.</b> A 20ft has about 33 m³ inside, but real loads rarely exceed 25–28 m³.</li>
<li><b>Ignoring weight limits.</b> Dense goods such as tiles or metal parts hit the payload limit, or national road limits, long before the container is full.</li>
<li><b>Forgetting pallets.</b> Palletised cargo loses 10–20% of the usable space.</li>
</ul>"""),
        ],
        "faq": [
            ("How do I calculate CBM?", "Multiply length × width × height in metres for one carton, then multiply by the number of cartons. In centimetres, divide the product by 1,000,000."),
            ("How many CBM fit in a 20ft container?", "About 33 m³ inside, and about 25–28 m³ of cartons in practice."),
            ("How many CBM fit in a 40ft high-cube?", "About 76 m³ inside and roughly 65–68 m³ of cartons in practice."),
            ("What is a revenue ton?", "The LCL billing unit: the greater of the cargo volume in cubic metres and its weight in metric tonnes."),
        ],
    },
    {
        "slug": "air-freight-chargeable-weight-calculator",
        "section": "air-chargeable",
        "title": "Air Freight Chargeable Weight Calculator – Volumetric Weight 6000 / 5000",
        "description": "Calculate volumetric (dimensional) weight and the chargeable weight for air cargo (IATA 6000) and express couriers (5000), in cm/kg or inches/pounds.",
        "nav": "Air chargeable weight",
        "blurb": "Volumetric and chargeable weight for airlines and express couriers.",
        "guide": [
            ("Actual weight versus volumetric weight", """
<p>Air carriers charge for whichever is larger: what a shipment weighs or how much space it takes. The space is converted into a "volumetric" weight by dividing the volume by a fixed divisor. Airlines use the IATA divisor of 6,000 cm³ per kg (166 in³ per lb). Express couriers such as DHL, FedEx and UPS usually use 5,000 (139 in³ per lb), which makes the same box heavier on paper.</p>"""),
            ("Worked example", """
<p>Four cartons of 60 × 50 × 45 cm, each weighing 12 kg:</p>
<table><tr><th>Item</th><th>Airline (6000)</th><th>Courier (5000)</th></tr>
<tr><td>Actual weight</td><td class="n">48 kg</td><td class="n">48 kg</td></tr>
<tr><td>Volumetric weight</td><td class="n">90 kg</td><td class="n">108 kg</td></tr>
<tr><td><b>Chargeable weight</b></td><td class="n"><b>90 kg</b></td><td class="n"><b>108 kg</b></td></tr></table>
<p>The cartons are billed at almost twice their real weight. Repacking into smaller cartons with less void fill would cut the bill directly.</p>"""),
            ("Ways to lower chargeable weight", """
<ul>
<li>Right-size cartons and remove empty space; each centimetre counts in all three dimensions.</li>
<li>Combine small parcels into one consolidated shipment so the airline divisor applies instead of the courier divisor.</li>
<li>For heavy but compact goods, volumetric weight rarely matters; focus on the actual weight instead.</li>
</ul>"""),
        ],
        "faq": [
            ("How do I calculate volumetric weight?", "Multiply length × width × height in centimetres and divide by 6,000 for airlines or 5,000 for express couriers. In inches, divide by 166 or 139 to get pounds."),
            ("What is chargeable weight?", "The greater of the actual gross weight and the volumetric weight, usually rounded up to the next half kilogram."),
            ("Why do couriers use 5000 instead of 6000?", "A smaller divisor gives a higher volumetric weight, reflecting the higher handling cost of small parcels in express networks."),
            ("Is chargeable weight calculated per piece or per shipment?", "Airlines usually calculate it on the whole shipment. Couriers may calculate per package, so check your contract."),
        ],
    },
    {
        "slug": "cpk-calculator",
        "section": "cpk",
        "title": "Cpk Calculator – Process Capability Cp, Cpk & PPM Out of Spec",
        "description": "Calculate Cp, Cpk, Cpu, Cpl and expected ppm out of specification from spec limits and mean and standard deviation, or paste raw measurements.",
        "nav": "Cpk",
        "blurb": "Cp, Cpk and expected defects per million from your measurements.",
        "guide": [
            ("What Cp and Cpk tell you", """
<p>Process capability compares the spread of a process with the tolerance a drawing allows. <b>Cp</b> asks whether the process could fit inside the tolerance if it were perfectly centred: tolerance width divided by six standard deviations. <b>Cpk</b> also checks where the process actually sits, taking the nearer of the two limits. A process can have a good Cp and a poor Cpk simply because it runs off centre, and that is usually the cheapest problem to fix.</p>"""),
            ("Worked example", """
<p>A shaft diameter has limits of 9.90 to 10.10 mm. The process runs at a mean of 10.02 mm with a standard deviation of 0.025 mm.</p>
<table><tr><th>Index</th><th>Value</th></tr>
<tr><td>Cp (0.20 ÷ 0.15)</td><td class="n">1.33</td></tr>
<tr><td>Cpu ((10.10 − 10.02) ÷ 0.075)</td><td class="n">1.07</td></tr>
<tr><td>Cpl ((10.02 − 9.90) ÷ 0.075)</td><td class="n">1.60</td></tr>
<tr><td><b>Cpk</b></td><td class="n"><b>1.07</b></td></tr>
<tr><td>Expected out of spec</td><td class="n">about 690 ppm</td></tr></table>
<p>The spread is acceptable but the mean sits 0.02 mm high. Re-centring the process to 10.00 mm would raise Cpk to 1.33 without any new equipment.</p>"""),
            ("Using the result correctly", """
<ul>
<li><b>Check stability first.</b> Capability only predicts the future if the process is in statistical control. Plot a control chart before quoting Cpk.</li>
<li><b>Use enough data.</b> At least 30 measurements, ideally 100 or more from several shifts, gives a reliable estimate.</li>
<li><b>Normal data only.</b> The ppm estimate assumes a normal distribution. Skewed characteristics such as flatness or runout need a different method.</li>
</ul>"""),
        ],
        "faq": [
            ("What is a good Cpk value?", "1.33 is the common minimum for production, which means about 63 ppm out of spec for a centred process. 1.67 is often required for safety-critical or newly approved parts."),
            ("What is the difference between Cpk and Ppk?", "Cpk uses short-term, within-subgroup variation; Ppk uses the overall standard deviation of all data. With a single set of pasted values this calculator gives the overall figure, which is effectively Ppk."),
            ("Can Cpk be negative?", "Yes. A negative Cpk means the process mean lies outside the specification limits."),
            ("How many measurements do I need?", "Thirty is a practical minimum; 100 or more across shifts and material lots gives a much more reliable estimate."),
        ],
    },
]
