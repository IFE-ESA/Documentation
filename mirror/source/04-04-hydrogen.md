(sec-hydrogen)=
# Hydrogen

Hydrogen can be produced and used in many different ways, and many of them are still only at a developing stage. In IFE-TIMES-Norway, the technologies which are considered relevant for Norway are included and illustrated in {numref}`fig-schematic-hydrogen-system-ife-times`. Production of hydrogen can either be centralized or decentralized. The commodity H2-CENT is assumed to be low-pressure hydrogen available directly after production (electrolyser) and can be used in industrial processes and for ammonia production. For storage and usage in the transport segment (H2-TRA), it needs to be compressed into the commodity H2-COMP, which is assumed to have a compression level of 250 bar. The hydrogen is, in addition, both distributed and handled by filling infrastructure, which might increase the pressure further. As distributed production is more expensive compared to centralized production, a user constraint is added to force a minimum share of 20% local hydrogen production (3 MW) to represent small-scale, on-site production closer to demand. The share is determined based on dialogue with hydrogen experts at IFE. In the figure, green boxes represent the source from which hydrogen is produced, while yellow boxes represent the process of production, compression, and transport. Blue hydrogen can be produced from autothermal reforming with CCS.

:::{figure} images/figure-18.png
:name: fig-schematic-hydrogen-system-ife-times

Schematic of the hydrogen system in IFE-TIMES-Norway.
:::

(sec-with-electrolyser)=
## With electrolyser

Hydrogen from electrolysers is assumed to be produced in each region either at large scale (centralized) or small scale (distributed), and cost-wise are represented by 20 MW{sub}`el` and 3 MW{sub}`el` installed capacity, respectively. The costs {cite}`79` are provided for both alkaline and Proton Exchange Membrane (PEM) electrolysers and comprise three parts: electrolyser, compressor skid, and other costs. The other costs cover engineering, control systems, interconnection, commissioning, and start-up costs.

Aggregated investment costs are shown in {numref}`tab-investment-costs-opex-electrolysers`, while efficiency and lifetime of the electrolysers are presented in {numref}`tab-efficiency-lifetime-small-large-electrolysers`. The lifetime for electrolysers is usually presented in operational hours, and its end of lifetime is based on when its efficiency drops below a set threshold due to the degradation of the fuel cell. In IFE-TIMES-Norway, a fixed lifetime in years is based on the plant’s capacity factor of 95%.

A distinction between PEM and Alkaline electrolysers is made by allowing hourly (Daynite) variation in the operation of PEM electrolysers, while Alkaline is only allowed to vary between seasons.

The yearly operational expenses (OPEX) incorporate the cost related both to the electrolyser type and the compressor {cite}`80`and are shown in {numref}`tab-investment-costs-opex-electrolysers`. The noticeable difference between large- and small-scale electrolysers is because small-scale electrolysers include a compressor to provide high-pressure hydrogen to the commodity H2-TRA.

In addition to CAPEX and OPEX, large-scale and distributed electrolysers are distinguished by their electricity source: large-scale electrolysers are assumed to draw power from the high-voltage grid, whereas distributed electrolysers depend on the low-voltage distribution grid, for which a grid tariff is included in addition to electricity costs.

In Appendix A, a more detailed explanation is provided of how costs and technical values have been selected for the electrolysers and references to publications used in the selection process.

:::{list-table} Investment costs and OPEX for the different electrolysers
:name: tab-investment-costs-opex-electrolysers
:header-rows: 1
:widths: 14 10 13 12 14 12 10 10
:column-align: center center center center center center center center
:header-align: center

* -
  -
  - {colspan}`3` Investment costs\
    (NOK/kWel)
  - {colspan}`3` Fixed OPEX\
    (NOK/kWH2)
* -
  -
  - **2018**
  - **2030**
  - **2050**
  - **2018**
  - **2030**
  - **2050**
* - {rowspan}`2` 20 MW el
  - PEM
  - 17 366
  - 11401
  - 5419
  - 383
  - 251
  - 120
* - Alkaline
  - 11658
  - 7 500
  - 4896
  - 257
  - 165
  - 108
* - {rowspan}`2` 3 MW el
  - PEM
  - 23222
  - 14588
  - 7557
  - 553
  - 336
  - 186
* - Alkaline
  - 19765
  - 11843
  - 8201
  - 513
  - 294
  - 211
:::

:::{list-table} Efficiency and lifetime of small and large electrolysers. Small electrolysers include compression to 250 bars.
:name: tab-efficiency-lifetime-small-large-electrolysers
:header-rows: 1
:widths: 18 10 10 10 15 17 15
:column-align: center center center center center center center
:header-align: center

* -
  - {colspan}`3` Efficiency (%)
  - {colspan}`3` Lifetime (h)
* -
  - **2018**
  - **2030**
  - **2050**
  - **2018**
  - **2030**
  - **2050**
* - Alkaline 3 MW
  - 64
  - 66
  - 72
  - 75000
  - 95000
  - 125000
* - Alkaline 20 MW
  - 67
  - 68
  - 75
  - 75000
  - 95000
  - 125000
* - PEM 3 MW
  - 57
  - 64
  - 69
  - 60000
  - 75000
  - 125000
* - PEM 20 MW
  - 58
  - 66
  - 71
  - 60000
  - 75000
  - 125000
:::

(sec-with-autothermal-reforming-of-natural-gas-atr)=
## With autothermal reforming of natural gas (ATR)

Production of hydrogen from autothermal reforming of natural gas (ATR) is allowed in NO2, NO3, NO4, and NO5, as these are the regions with available gas infrastructure. Natural gas is used as the input commodity, with an efficiency of 74%. Consequently, 1.36 units of natural gas are needed to produce 1 unit of blue hydrogen. Moreover, the share of electricity used as input is 4%. The capture rate is assumed to be 95%. ATR is used instead of SMR (Steam methane reforming) due to superior cost and CO{sub}`2` capture rate. ATR combines hydrogen production and heating in a single reactor, resulting in a single concentrated stream of CO{sub}`2` that makes carbon capture integration easier (and cheaper). The input parameters for producing hydrogen through ATR with CO{sub}`2` capture are based on the report Hydrogen4EU {cite}`81`. The total costs and technology parameters are summarized in {numref}`tab-cost-technology-parameters-atr-ccs`.

:::{list-table} Cost and technology parameters of ATR with CCS.
:name: tab-cost-technology-parameters-atr-ccs
:header-rows: 1
:widths: 47 17 15 15
:column-align: left center center center
:header-align: center

* -
  - 2018
  - 2030
  - 2050
* - Total plant cost (TPC) [kNOK/MW H2]
  - 8000
  - 7000
  - 7000
* - Fixed O&M [kNOK/MW H2]
  - 240
  - 210
  - 210
* - Variable O&M [kNOK/GWh]
  - 1908
  - 252
  - 252
* - Efficiency [%]
  - 74%
  - 74%
  - 74%
* - Electricity input [%]
  - 4%
  - 4%
  - 4%
* - Lifetime [years]
  - 25
  - 25
  - 25
* - CO{sub}`2` capture rate [%]
  - 95%
  - 95%
  - 95%
:::

(sec-storage)=
## Storage

The storage of hydrogen is assumed to be at 250 bars. Cost for such storage is taken from {cite}`82` and is 6300 NOK/kg, which corresponds to 189 000 kNOK/GWh.

Storage within a day is available both for centralized and compressed hydrogen commodity (H2-COMP) and for local hydrogen production for transport (H2-TRA). Seasonal storage is only enabled in connection with centralized compression units.

(sec-hydrogen-refuelling-station-hrs)=
## Hydrogen refuelling station (HRS)

Necessary infrastructure for hydrogen-filling provides additional cost to hydrogen production, and in certain studies, accounts for about half the total hydrogen cost for the customer. HRSs are needed at the end of the supply chain in order to facilitate the usage of the produced hydrogen. Costs for HRS can vary greatly depending on size, pressure, degree of utilization, and design.

For the decentralized electrolysers, the cost of HRS is included as part of the electrolyser cost, given as a variable O&M cost. The cost development towards 2050 is given in {numref}`tab-variable-o-m-costs-decentralized`.

:::{list-table} Variable O&M costs for the decentralized electrolysers.
:name: tab-variable-o-m-costs-decentralized
:header-rows: 1
:column-align: center center center left center left
:header-align: center

* -
  - {colspan}`2` 2018
  - {colspan}`2` 2030
  - 2050
* - HRS cost [kNOK/GWh]
  - 1200
  - {colspan}`2` 720
  - {colspan}`2` 660
:::

For centralized electrolysers, the HRS cost is included in the distribution process. In {cite}`83`, the cheapest 700 bar solution costs almost 40 NOK/kg H{sub}`2`, and the most expensive 350 bar solution costs slightly above 35 NOK/kg H{sub}`2`. At the same time, {cite}`84` shows that a large-scale (1000 kg/day) 700 bar HRS can be as low as 32 NOK/kg H{sub}`2`, while if either HRS is smaller or has a lower utilization rate, costs increase. Based on available literature, an average cost of 40 NOK/kg H{sub}`2` is assumed for the start year. This corresponds to 1200 kNOK/GWh (as given in {numref}`tab-variable-o-m-costs-decentralized`). In IFE-TIMES-Norway, the HRS cost is combined with the cost of transport (described in Section {numref}`sec-hydrogen-transport-and-trading`) to represent the overall distribution cost.

:::{list-table} Cost for HRS from different sources
:name: tab-cost-hrs-sources
:header-rows: 2
:widths: 17 7 25 36
:column-align: left left center center
:header-align: center

* - {rowspan}`2` {colspan}`2`
  - Light-duty vehicles
  - Heavy-duty vehicles
* - {cite}`84`
  - {cite}`83`
* - {colspan}`2` Pressure (bar)
  - 700
  - 350 & 700
* - {colspan}`2` Currency
  - USD{sub}`2017`
  - NOK{sub}`2018`
* - {rowspan}`2` Cost per kg{sub}`H2`
  - Max
  - 7
  - 66
* - Min
  - 3.8
  - 32
:::

In addition, a reduction in cost is expected over time. In {cite}`83`, cost reduction is connected to the increase in HRS globally. With an increase from 375 HRS in operation globally in 2018 to approximately 5 000 and 10 000 stations, the costs may decrease by 40% and 45%, respectively. In IFE-TIMES-Norway, it is assumed that there will be 5 000 and 10 000 HRS stations globally by 2030 and 2040, respectively.

(sec-hydrogen-transport-and-trading)=
## Hydrogen transport and trading

Hydrogen can, in theory, be transported over both long and short distances. In practice, cost-effective long-distance transport of hydrogen is a relatively immature technology. It is expensive, and large-scale demand volume is needed to motivate building hydrogen pipelines or alternative transport solutions for liquefied hydrogen. The latter has notable cost and energy efficiency penalties.

Therefore, trade in hydrogen has only been added for adjacent geographical areas within Norway, and the costs for it are based on the distance between the main cities within each region. The distance between regions and costs of transport are shown in {numref}`tab-distance-between-regions-transport-costs`. The cost calculations are based on transport of hydrogen in a 40-foot tube trailer by truck and a total daily delivery of 2000 kg of hydrogen transported in several tube trailers.

:::{list-table} Distance between regions and transport costs used in trading of hydrogen.
:name: tab-distance-between-regions-transport-costs
:header-rows: 1
:widths: 7 14 7 14 11 18
:column-align: center center center center center center
:header-align: center

* - {colspan}`2` From
  - {colspan}`2` To
  - Distance (km)
  - Transport costs (NOK/kg{sub}`H2`)
* - {rowspan}`3` NO1
  - {rowspan}`3` Oslo
  - NO2
  - Kristiansand
  - 320
  - 17
* - NO3
  - Trondheim
  - 490
  - 24
* - NO5
  - Bergen
  - 460
  - 23
* - {rowspan}`2` NO2
  - {rowspan}`2` Kristiansand
  - NO1
  - Oslo
  - 320
  - 17
* - NO5
  - Bergen
  - 470
  - 24
* - {rowspan}`3` NO3
  - {rowspan}`3` Trondheim
  - NO1
  - Oslo
  - 490
  - 24
* - NO4
  - Tromsø
  - 1100
  - 51
* - NO5
  - Bergen
  - 700
  - 34
* - NO4
  - Tromsø
  - NO3
  - Trondheim
  - 1100
  - 51
* - {rowspan}`3` NO5
  - {rowspan}`3` Bergen
  - NO1
  - Oslo
  - 460
  - 23
* - NO2
  - Kristiansand
  - 470
  - 24
* - NO3
  - Trondheim
  - 700
  - 34
:::

The hydrogen used in the transport sector can either be produced centrally and then distributed or be produced locally, as illustrated in {numref}`fig-illustration-how-distances-distribution-within`. The costs of distributing hydrogen within a region will depend on the geographical size of the region. The distance and its respective cost of distribution are estimated using a simple method based on the distance between regions shown in {numref}`tab-distance-between-regions-transport-costs`. As a first step, a distance (D) is calculated as the average between a region of interest and all adjacent regions. The main cities in each region are assumed to be roughly at the centre of the region, and that D can be simplified as the distance between centre points between two circular regions, as shown in {numref}`fig-illustration-how-distances-distribution-within`. In the second step, it is assumed that the regions have approximately the same size and that initial large-scale production of hydrogen will be close to the main city of each region. A part of the hydrogen demand for road transport will be relatively close to the production site and defined as an average distance of D/6 (short distance), while another part of the demand will be at an average distance of D/3 (long distance), as shown in {numref}`fig-illustration-how-distances-distribution-within`. The average distance between regions, the short and long distances of distribution, and costs for distribution in IFE-TIMES-Norway are presented in {numref}`tab-values-used-calculate-distribution-costs`. These are based on a 40-foot tube trailer that distributes 500 kg per day.

:::{figure} images/figure-19.png
:name: fig-illustration-how-distances-distribution-within

Illustration of how distances of distribution within regions are developed.
:::

:::{list-table} Values used to calculate distribution costs for each region and the distribution costs.
:name: tab-values-used-calculate-distribution-costs
:header-rows: 2
:widths: 9 17 21 12 12 12 14
:column-align: center center center center center center center
:header-align: center

* - {rowspan}`2` {colspan}`2` Region
  - {rowspan}`2` Average distance to other regions, D (km)
  - {colspan}`2` Long transport within region
  - {colspan}`2` Short transport within region
* - **D/3**
  - **NOK/kg**
  - **D/6**
  - **NOK/kg**
* - NO1
  - **Oslo**
  - 423
  - 141
  - 9
  - 71
  - 6
* - NO2
  - **Kristiansand**
  - 395
  - 132
  - 9
  - 66
  - 6
* - NO3
  - **Trondheim**
  - 763
  - 254
  - 14
  - 127
  - 9
* - NO4
  - **Tromsø**
  - 1100
  - 367
  - 19
  - 183
  - 11
* - NO5
  - **Bergen**
  - 497
  - 166
  - 10
  - 83
  - 7
:::

As the hydrogen demand is expected to increase over time, it is assumed that several large-scale production sites will become available in each region, and the distance of distribution will consequently be reduced. This development is modelled by assuming that, in 2030, only 50% of hydrogen for transport can be supplied through short-distance transport; this increases to 100% by 2050. This variable is set exogenous, but is strongly dependent on the model results, which makes it a central parameter for sensitivity analysis of the hydrogen supply chain for the transport sector. The distribution costs of hydrogen are defined in such a detailed manner to be able to analyse the role of locally produced hydrogen.
