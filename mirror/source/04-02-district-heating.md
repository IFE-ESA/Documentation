(sec-district-heating)=
# District heating

(sec-background)=
## Background

District heating has been modelled as a system with several heating plant alternatives in each electricity spot area. To better cover the diversity of different district heating systems, two sizes are introduced – large and small/local district heating grids. This facilitates the incorporation of different specific investment costs and assumptions on technologies available for different system sizes.

In a model like IFE-TIMES-Norway, all buildings have the same costs and availability to use different technologies, if no restrictions are applied. Therefore, a market share is often used to better represent the actual possibilities and/or different costs or efficiencies of various technologies.

(sec-production-statistics)=
## Production Statistics

The capacities of existing district heating plants in the model were inferred from the 2023 production data given in {cite}`60`. From {numref}`fig-production-district-heat-type-fuel` It can be seen that the production of district heat has almost doubled in recent years relative to 2009, but has remained relatively unchanged since 2021 at around 7-8 TWh. Fossil use has steadily decreased through the years, while use of waste incineration and bioenergy has increased noticeably. Ambient heat and electricity remained relatively unchanged.

:::{figure} images/figure-12.png
:name: fig-production-district-heat-type-fuel

Production of district heat by type of fuel used, TWh/year
:::

To distribute the different technologies in the different IFE-TIMES-Norway onshore regions, information at the plant level was taken from {cite}`60`, where most of the district heating companies report data. Most of the district heating is produced in NO1, 4.7 TWh in 2023 (60% of total), and the second largest district heat producer is NO3 (17% of total), see {numref}`fig-district-heating-production-market-spot` and {numref}`tab-district-heat-production-2023-type`.

:::{list-table} District heat production in 2023 by type of fuel used for the different regions, GWh
:name: tab-district-heat-production-2023-type
:header-rows: 1
:widths: 9 9 9 9 11 9 9 10 9 9
:column-align: left right right right right right right right right right
:header-align: center

* -
  - OIL
  - GAS + BIOGAS
  - WASTE
  - BIOMASS
  - BIOOIL
  - WASTE HEAT
  - ELECTRIC BOILER
  - HEAT PUMP
  - TOTAL
* - NO1
  - 38
  - 89
  - 1515
  - 1703
  - 214
  - 9
  - 504
  - 658
  - 4729.8
* - NO2
  - 10
  - 79
  - 312
  - 269
  - 1
  - 102
  - 16
  - 24
  - 813.4
* - NO3
  - 38
  - 78
  - 755
  - 140
  - 8
  - 102
  - 180
  - 24
  - 1325.7
* - NO4
  - 9
  - 15
  - 156
  - 178
  - 1
  - 109
  - 102
  - 30
  - 600.3
* - NO5
  - 0
  - 0
  - 342
  - 0
  - 22
  - 0
  - 20
  - 0
  - 382.8
* - TOTAL
  - 95
  - 261
  - 3079
  - 2291
  - 245
  - 323
  - 822
  - 736
  - 7852.0
:::

:::{figure} images/figure-13.png
:name: fig-district-heating-production-market-spot

District heating production per market spot price area in 2023 {cite}`60`, GWh/year
:::

Only one site produces more than 1 TWh/year (Oslo), and two others produce more than 300 GWh/year (Trondheim and Bergen). The number of plants delivering more than 100 GWh/year was 11 in 2023 (Hamar, Tromsø, Trondheim, Kristiansand, Ålesund, Lillestrøm, Stavanger, Oslo, Drammen, Mo I Rana, Bergen, Fredrikstad). In total, these 11 plants produced 4.8 TWh/year in 2023 out of the total of 7.9 TWh/year. If it is assumed that only smaller plants do not report to [{u}`fjernkontrollen.no`](https://ifecloud.sharepoint.com/sites/ESYS/Delte%20dokumenter/TIMES%20VEDA/Documentation/fjernkontrollen.no) {cite}`60`, the production from plants with an annual capacity of less than 100 GWh/year can be estimated to be at 3.1 TWh, produced by 90-100 plants. The 100 GWh/year threshold is used to define large and small/local district heating systems in the IFE-TIMES-Norway model, wherein large grids produce more than 100 GWh/year, and small/local district heating systems produce less than 100 GWh/year.

(sec-heating-technologies)=
## Heating technologies

In the model, representatives of different district heating plant technologies produce heat distributed to a district heat grid; and the heat from the grid is transferred to the end-use sectors of Building and Industry via representatives of heat exchangers. Losses in the district heating network from 2014 to 2023 averaged 11% {cite}`61`. The different types of existing and potential new investments in district heating boilers and CHP are presented in {numref}`tab-input-parameters-district-heating-plants`, including their respective costs {cite}`62` and efficiencies. Efficiencies were calculated using the 2023 SSB fuel consumption data for district heating and district heat production data {cite}`63`. The cost of CHP is reduced by 4% in 2035 due to technology learning, based on {cite}`64`.

:::{list-table} Input parameters for district heating plants
:name: tab-input-parameters-district-heating-plants
:header-rows: 1
:widths: 33 31 18 15
:column-align: left center center center
:header-align: center

* - Technology
  - Investment Cost (2020), NOK/kW
  - Efficiency / COP
  - Lifetime
* - Gas boiler
  -
  -
  -
* - *large*
  - 747
  - 93%
  - 25
* - *small*
  - 747
  - 93%
  - 25
* - Waste boiler
  - 21649
  - 76%[^2]
  - 25
* - Biomass boiler
  -
  -
  -
* - *large*
  - 5475
  - 89%
  - 25
* - *small*
  - 8585
  - 89%
  - 25
* - Bio-oil boiler
  -
  -
  -
* - *large*
  - 1908
  - 88%
  - 20
* - *small*
  - 1908
  - 88%
  - 20
* - Heat recovery (high-temperature excess heat)
  -
  -
  -
* - *large*
  - 2116
  - 100%
  - 25
* - *small*
  - 3609
  - 100%
  - 25
* - Electric boiler
  -
  -
  -
* - *large*
  - 871
  - 99%
  - 25
* - *small*
  - 1867
  - 99%
  - 25
* - Excess heat heat pump
  -
  -
  -
* - *large*
  - 8336
  - 5.1
  - 25
* - *small*
  - 15428
  - 4.1
  - 25
* - Seawater heat pump
  -
  -
  -
* - *large*
  - 10998
  - 3.01
  - 25
* - *small*
  - 5972
  - 3.7
  - 25
* - Waste CHP (power output)
  - 149000
  - 4
  - 20
:::

Municipal waste can only be used in large district heating plants, and, by default, it is assumed that the volumes of today will be constant until 2050. The municipal waste must be used since it is not allowed to deposit waste anymore.

The heat delivered by the heat pumps using waste heat is restricted by the waste heat potential. In IFE-TIMES-Norway, it is assumed that this technology can deliver 658 GWh/year in 2025 in NO1, as given by {cite}`60`, and grows proportionally with the expected growth in the total number of heat pumps sold in Norway {cite}`65`. On the other hand, 250 GWh/year and 50 GWh/year were individually assumed for NO2-4 and NO5, respectively, in 2025. The potential is expected to double by 2030, reaching 2.9 TWh for all of Norway. High-temperature excess heat recovery is limited to the current levels (0.32 TWh /year). Seawater heat pumps currently have a total upper-limit capacity of 91 MW, and are assumed to grow to 240 MW, following the expected growth in the total number of brine-to-water heat pumps in the country {cite}`65`.

CCS in waste incineration in district heating plants with CHP is included as a possibility in SubRES files: SubRES_CCS and SubRES_CCS_Trans, with region-specific data in the Trans file. The start year is set to 2028 for NO1, due to the plans for carbon capture at Klemetsrud. The remaining regions have a start year of 2030.

(sec-estimate-of-maximum-potential)=
## Estimate of maximum potential

End-use of district heating was 7.0 TWh in 2023, and of this, commercial services used 3.8 TWh, dwellings 1.9 TWh, and industry 1.0 TWh (see {numref}`fig-use-district-heating-end-use`) {cite}`63`. These were used to calibrate the current consumption of district heat in the different end-use sectors in the model. In IFE-TIMES-Norway, both services and households, which constitute 81% of district heat utilization, are included in the Buildings sector.

:::{figure} images/figure-14.png
:name: fig-use-district-heating-end-use

Use of district heating per end-use sector in 2023, GWh
:::

As for future development of district heating use, one way to estimate the maximum potential for district heating is to assume that all commercial buildings and dwellings in areas with sufficiently high density can be connected to a district heating system (large or small/local). SSB publishes data on people living in “tettbygde strøk” (densely populated areas), and the definition of these areas is “at least 200 people live in an area of houses with less than 50 m apart”. With this definition, 18% of people in Norway live in areas that cannot be connected to local or large district heating systems. The share differs in the five Norwegian spot price regions, see {numref}`tab-population-densely-sparsely-populated-areas`.

:::{list-table} Population in densely and sparsely populated areas {cite}`66`, {cite}`67`.
:name: tab-population-densely-sparsely-populated-areas
:header-rows: 1
:widths: 19 28 33
:column-align: center center center
:header-align: center

* - Spot price area
  - Densely populated area
  - Sparsely populated area
* - NO1
  - 86 %
  - 14 %
* - NO2
  - 84 %
  - 16 %
* - NO3
  - 74 %
  - 26 %
* - NO4
  - 72 %
  - 28 %
* - NO5
  - 80 %
  - 20 %
* - Norway
  - 82 %
  - 18 %
:::

It was also assumed that “large” systems are applicable in cities and “small/local” systems otherwise. The estimate of people living in “cities” is not well founded but is based on different statistics and knowledge of district heating grids of today. The estimate is calculated using the number of inhabitants in the centre of cities in the different regions divided by their respective number of inhabitants, see the resulting share in {numref}`tab-share-large-district-heating-systems`.

:::{list-table} Share of large district heating systems per electricity price area
:name: tab-share-large-district-heating-systems
:header-rows: 1
:widths: 12 25 26 35
:column-align: center center center center
:header-align: center

* -
  - Electricity price area
  - mill. Persons in «cities»
  - Share living in «cities»
* - East
  - NO1
  - 1.47
  - 65 %
* - South
  - NO2
  - 0.61
  - 50 %
* - Middle
  - NO3
  - 0.28
  - 38 %
* - North
  - NO4
  - 0.18
  - 37 %
* - West
  - NO5
  - 0.30
  - 47 %
* - Norway
  -
  - 2.83
  - 53 %
:::

The maximum share of connections to the large or local district heating grids per type of dwelling and commercial building is presented in {numref}`tab-share-maximum-connection-large-small`. In this table, “buildings” refers to both multi-family houses and commercial buildings. The share is calculated by considering the “share living in cities” and the share of “densely populated area”, e.g., for NO1 the share of buildings connected to large district heating grids is 86 % \* 65 % = 56 %.

:::{list-table} Share of maximum connection to large and small/local district heating grids per region
:name: tab-share-maximum-connection-large-small
:header-rows: 1
:widths: 14 17 18 17 19
:column-align: center center center center center
:header-align: center

* - El. price area
  - Single-family houses
  - Buildings with point source heating
  - {colspan}`2` Buildings with waterborne heating
* -
  -
  -
  - **Large**
  - **Local**
* - NO1
  - 0%
  - 0%
  - 56 %
  - 30 %
* - NO2
  - 0%
  - 0%
  - 42 %
  - 42 %
* - NO3
  - 0%
  - 0%
  - 28 %
  - 46 %
* - NO4
  - 0%
  - 0%
  - 27 %
  - 46 %
* - NO5
  - 0%
  - 0%
  - 38 %
  - 42 %
* - Norway
  - 0%
  - 0%
  - 44 %
  - 38 %
:::

Another assumption made, based on information from major Norwegian district heating companies, is that single-family houses cannot be connected to a district heating system. This is a simplification and is not true in all cases, but as a model assumption it is justified since it is often not profitable to connect single-family dwellings to a district heating grid. On the other hand, it is assumed that all multifamily houses within densely populated areas would be able to connect to a heat grid, but this is probably a minor overestimation.

Buildings with a water-borne heating system can be connected to a district heating grid. In principle, buildings with point-source heating could also be connected if they invest in a water-borne heating system first, but as this is considered a very large investment often done for other reasons than pure techno-economic, it is not included as a possibility. The basic assumption is that the share of water-borne heating is 58% in existing commercial buildings and 90% in new commercial buildings, 38% in existing multifamily houses and 88% in new multifamily houses. In single-family houses, the share of water-borne heating is 12% in both existing and new dwellings. However, this has no influence on the use of district heating, since it is assumed that they cannot be connected to a district heating grid.

:::{figure} images/figure-15.png
:name: fig-share-water-borne-heating-wbh

Share of water-borne heating (WBH) and point source heating in buildings.
:::

With these possible maximum shares for connection with local or large district heating grids, a total upper potential for commercial buildings and dwellings can be calculated to 8-11 TWh in 2030–2050.

:::{list-table} Maximum potential of use of large and small/local district heating in 2030 (GWh/year).
:name: tab-maximum-potential-use-large-small
:header-rows: 1
:widths: 10 11 18 13 13 15 12
:column-align: center center center right right right right
:header-align: center

* - El. price area
  - Single-family houses
  - Buildings with point source heating
  - {colspan}`2` Multi-family houses with central heating
  - {colspan}`2` Commercial buildings with central heating
* -
  -
  -
  - **Large**
  - **Local**
  - **Large**
  - **Local**
* - NO1
  - 0
  - 0
  - 610
  - 333
  - 2 788
  - 1520
* - NO2
  - 0
  - 0
  - 114
  - 113
  - 362
  - 358
* - NO3
  - 0
  - 0
  - 58
  - 96
  - 392
  - 646
* - NO4
  - 0
  - 0
  - 25
  - 43
  - 169
  - 290
* - NO5
  - 0
  - 0
  - 79
  - 90
  - 151
  - 171
* - Norway
  - 0
  - 0
  - 887
  - 674
  - 3 862
  - 2 985
:::

In {numref}`fig-use-district-heating-2023-calculated`, the use of district heating in 2023 is compared with the maximum potential in 2030 based on the above calculations. The potential in industry, construction, and others is assumed to increase at a similar rate as in commercial buildings. In total, the potential in 2030 will be 10 TWh compared to the use of district heating in 2023 of 7 TWh.

:::{figure} images/figure-16.png
:name: fig-use-district-heating-2023-calculated

Use of district heating in 2023 and calculated maximum potential in 2030 per end-use sector (GWh/year).
:::

(sec-thermal-storage-in-district-heating)=
## Thermal storage in district heating

Thermal storage in district heating has been modelled using large thermal storage tanks, typically sized around 3000 m{sup}`3`. DAYNITE level storage, which can only store heat over a day-night cycle, were included in both “large” and “local” district heating systems. Seasonal storage is only considered in “large” district heating systems. See eq. (1), eq. (2) and eq. (4) in Section {numref}`sec-electricity-storage` for the modelling methodology used. For the investment cost, eq. (5) is used as the cost data for thermal storage is not given per energy and power term (as for battery).

$INVCOST\ (kNOK/MW) = INVCOST\ (kNOK/MWh)*C_{rate}^{- 1}$ (5)

Two DAYNITE heat storage technologies are added, one with 4 hours storage capacity and one with 12 hours capacity. The same parameters apply for both storage technologies, but the input and output commodities differ. Information about technology characteristics and costs can be found in {numref}`tab-parameters-cost-thermal-storage-tanks`. A round-trip storage efficiency of 98% is assumed, with a 0.2% energy loss per day during storage. The seasonal storage is based on a storage capacity of 500 hours; the efficiency is 80% and the daily storage loss is 0.2%.

:::{list-table} Parameters and cost for thermal storage tanks in district heating.
:name: tab-parameters-cost-thermal-storage-tanks
:header-rows: 1
:widths: 20 14 19 11 10 10 13
:column-align: left center center center center center center
:header-align: center

* -
  - Investment cost (NOK/kWh)
  - Fixed O&M (kNOK/GWh)
  - Efficiency (%)
  - Storage loss (%/day)
  - Lifetime

    (years)
  - NCAP_AFC
* - Daily storage,\
    4 hours
  - 31{sup}`1`
  - 0.29% of CAPEX{sup}`1`
  - 98 %{sup}`1`
  - 0.2 %{sup}`1`
  - 40{sup}`1`
  - 0.17
* - Daily storage,\
    12 hours
  - 31{sup}`1`
  - 0.29% of CAPEX{sup}`1`
  - 98 %{sup}`1`
  - 0.2 %{sup}`1`
  - 40{sup}`1`
  - 0.50
* - Seasonal storage
  - 7.15{sup}`2`
  - 0.29% of CAPEX{sup}`1`
  - 80 %
  - 0.2 %{sup}`1`
  - 40{sup}`1`
  - 0.06
:::

{sup}`1` Capital Costs (CAPEX) based on Large-scale hot water tanks from DEA Technology data catalogue (3 M€2015/GWh) {cite}`68`. Input cost to TIMES converted using eq. (5).\
{sup}`2` Costs based on BTES storage from {cite}`69`.

If seasonal storage is used in combination with waste incineration, the efficiency increases. This is modelled as a new technology, EH_WASTE2, that allows for a higher efficiency during summer (0.94 throughout all seasons) when seasonal storage is used.

[^2]: 94% in winter, spring, and fall and 21% in summer (cooling to air of unneeded heat in the summer is modelled as a lower efficiency) - average of 76%.
