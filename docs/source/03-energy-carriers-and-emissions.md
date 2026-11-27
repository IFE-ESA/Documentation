(sec-energy-carriers-and-emissions)=
# Energy carriers and emissions

(sec-overview-of-carriers)=
## Overview of carriers

Electricity commodities are defined in the Power file, commodities in district heating in the DistHeating file, and other commodities in the Fuels file. Internal commodities such as heating commodities are included in the end-use files (Buildings or Industry).

The commodities produced in IFE-TIMES-Norway are electricity, district heat, hydrogen, ammonia, synfuel, and some bioenergy products. The Power file includes onshore electricity generation, while offshore wind power generation is modelled in the offshore file. All electricity generation is described in the power chapter (Section {numref}`sec-electricity`). Production of district heat is included in the file DistHeating and is described in the district heating chapter (Section {numref}`sec-district-heating`).

Bioenergy is used across all sectors, and the production of some bioenergy products is included in the Fuels file. In the same file, modelling of hydrogen, ammonia, and synfuels is included.

The main electricity commodities are:

- ELC-HV (high voltage)

- ELC-LV (low voltage)

- ELC-REG (electricity from regulated hydropower)

- ELC-RUN (electricity from run-of-river)

- ELC-WIND (electricity from wind power)

- ELC-HV-off (electricity from offshore wind power for use by offshore oil & gas processes)

- ELC-NUC (electricity from nuclear power)

- ELC-LV-xxx

  - ELC-LV-COM (electricity to commercial buildings)

  - ELC-LV-IND (electricity to district heating plants, local electrolyzers, air, rail, sea, other mobile transport)

  - ELC-LV-IND-OTH (electricity to other/light industry)

  - ELC-LV-RESM (electricity to multi-family houses)

  - ELC-LV-RESS (electricity to single-family houses)

  - ELC-LV-AGR (electricity used in the agricultural sector)

  - ELC-LV-CON (electricity used in the construction sector)

- ELC-PV-xxx

  - 36 commodities differed by subsector, orientation, and tilt.

- Transport:

  - ELC-CAR (electricity for battery-powered cars, output from charger, defined in transport file)

  - ELC-VAN (electricity for battery-powered vans, output from charger, defined in transport file)

  - ELC-HD-COM (electricity for battery-powered trucks, output from slow charger, defined in transport file)

  - ELC-HD-FAST (electricity for battery-powered trucks, output from fast charger, defined in transport file)

Electricity produced locally in single-family houses can only be used in single-family houses or sold to the low-voltage grid. Similarly, electricity produced locally in multi-family houses or non-residential buildings can only be used by multi-family houses or non-residential buildings or sold to the low-voltage grid. The grid losses are assumed to be 2% in the high-voltage grid and 7% in the low-voltage grid {cite}`15`, which are both defined in the Power file.

The district heating commodities are:

- LTH-DH1-GRID (district heat from large-scale plants to large-scale grid)

- LTH-DH2-GRID (district heat from small-scale plants to small-scale grid)

- LTH-GRID1-EX (district heat from large-scale grid to heat exchanger in end-use sector)

- LTH-GRID2-EX (district heat from small-scale grid to heat exchanger in end-use sector)

(sec-grid-fee)=
## Grid fee

A grid fee is added to the low-voltage grid, based on Elvia for commercial customers in 2021 {cite}`16`. The fee is divided into an energy and a power part and varies between regions, as shown in {numref}`tab-grid-fees-demand-sector-region`. The regional variation is based on statistics from NVE {cite}`17`. The fee is increased due to increased investments and prices. Based on information from NVE and Elvia, the prices are assumed to increase by 5% until 2030, and the investment costs are assumed to increase by 3% annually. The grid fees are included in the file “Power”. Electricity tax and VAT are defined in the file “Scen_A_Taxes”.

:::{list-table} Grid fees per demand sector, region, and year.
:name: tab-grid-fees-demand-sector-region
:header-rows: 1
:widths: 8 13 7 7 7 7 7 7 7 7 7 7
:column-align: left left center center center center center center center center center center

* -
  -
  - {colspan}`5` Energy fee (øre/kWh)
  - {colspan}`5` Power fee (NOK/kW/month)
* - Year
  - **Season**
  - **NO1**
  - **NO2**
  - **NO3**
  - **NO4**
  - **NO5**
  - **NO1**
  - **NO2**
  - **NO3**
  - **NO4**
  - **NO5**
* - {colspan}`12` Single residential buildings
* - 2022
  - Winter
  - 7.0
  - 8.6
  - 8.9
  - 8.2
  - 7.9
  - 360
  - 442
  - 457
  - 419
  - 408
* -
  - Spring
  - 3.9
  - 4.8
  - 5.0
  - 4.5
  - 4.4
  - 201
  - 247
  - 255
  - 234
  - 228
* -
  - Summer
  - 3.9
  - 4.8
  - 5.0
  - 4.5
  - 4.4
  - 66
  - 81
  - 84
  - 77
  - 75
* -
  - Fall
  - 3.9
  - 4.8
  - 5.0
  - 4.5
  - 4.4
  - 201
  - 247
  - 255
  - 234
  - 228
* - 2030
  - Winter
  - 7.4
  - 9.0
  - 9.3
  - 8.6
  - 8.3
  - 455
  - 558
  - 578
  - 530
  - 515
* -
  - Spring
  - 4.1
  - 5.0
  - 5.2
  - 4.8
  - 4.6
  - 254
  - 312
  - 323
  - 296
  - 288
* -
  - Summer
  - 4.1
  - 5.0
  - 5.2
  - 4.8
  - 4.6
  - 83
  - 102
  - 106
  - 97
  - 94
* -
  - Fall
  - 4.1
  - 5.0
  - 5.2
  - 4.8
  - 4.6
  - 254
  - 312
  - 323
  - 296
  - 288
* - 2050
  - Winter
  - 7.4
  - 9.0
  - 9.3
  - 8.6
  - 8.3
  - 814
  - 1000
  - 1035
  - 949
  - 923
* -
  - Spring
  - 4.1
  - 5.0
  - 5.2
  - 4.8
  - 4.6
  - 455
  - 558
  - 578
  - 530
  - 515
* -
  - Summer
  - 4.1
  - 5.0
  - 5.2
  - 4.8
  - 4.6
  - 149
  - 183
  - 190
  - 174
  - 169
* -
  - Fall
  - 4.1
  - 5.0
  - 5.2
  - 4.8
  - 4.6
  - 455
  - 558
  - 578
  - 530
  - 515
* - {colspan}`12` Multifamily buildings
* - 2022
  - Winter
  - 7.0
  - 8.6
  - 8.9
  - 8.2
  - 7.9
  - 360
  - 442
  - 457
  - 419
  - 408
* -
  - Spring
  - 3.9
  - 4.8
  - 5.0
  - 4.5
  - 4.4
  - 201
  - 247
  - 255
  - 234
  - 228
* -
  - Summer
  - 3.9
  - 4.8
  - 5.0
  - 4.5
  - 4.4
  - 66
  - 81
  - 84
  - 77
  - 75
* -
  - Fall
  - 3.9
  - 4.8
  - 5.0
  - 4.5
  - 4.4
  - 201
  - 247
  - 255
  - 234
  - 228
* - 2030
  - Winter
  - 7.4
  - 9.0
  - 9.3
  - 8.6
  - 8.3
  - 455
  - 558
  - 578
  - 530
  - 515
* -
  - Spring
  - 4.1
  - 5.0
  - 5.2
  - 4.8
  - 4.6
  - 254
  - 312
  - 323
  - 296
  - 288
* -
  - Summer
  - 4.1
  - 5.0
  - 5.2
  - 4.8
  - 4.6
  - 83
  - 102
  - 106
  - 97
  - 94
* -
  - Fall
  - 4.1
  - 5.0
  - 5.2
  - 4.8
  - 4.6
  - 254
  - 312
  - 323
  - 296
  - 288
* - 2050
  - Winter
  - 7.4
  - 9.0
  - 9.3
  - 8.6
  - 8.3
  - 814
  - 1000
  - 1035
  - 949
  - 923
* -
  - Spring
  - 4.1
  - 5.0
  - 5.2
  - 4.8
  - 4.6
  - 455
  - 558
  - 578
  - 530
  - 515
* -
  - Summer
  - 4.1
  - 5.0
  - 5.2
  - 4.8
  - 4.6
  - 149
  - 183
  - 190
  - 174
  - 169
* -
  - Fall
  - 4.1
  - 5.0
  - 5.2
  - 4.8
  - 4.6
  - 455
  - 558
  - 578
  - 530
  - 515
* - {colspan}`12` Commercial buildings
* - 2022
  - Winter
  - 7.0
  - 8.6
  - 8.9
  - 8.2
  - 7.9
  - 360
  - 442
  - 457
  - 419
  - 408
* -
  - Spring
  - 3.9
  - 4.8
  - 5.0
  - 4.5
  - 4.4
  - 201
  - 247
  - 255
  - 234
  - 228
* -
  - Summer
  - 3.9
  - 4.8
  - 5.0
  - 4.5
  - 4.4
  - 66
  - 81
  - 84
  - 77
  - 75
* -
  - Fall
  - 3.9
  - 4.8
  - 5.0
  - 4.5
  - 4.4
  - 201
  - 247
  - 255
  - 234
  - 228
* - 2030
  - Winter
  - 7.4
  - 9.0
  - 9.3
  - 8.6
  - 8.3
  - 455
  - 558
  - 578
  - 530
  - 515
* -
  - Spring
  - 4.1
  - 5.0
  - 5.2
  - 4.8
  - 4.6
  - 254
  - 312
  - 323
  - 296
  - 288
* -
  - Summer
  - 4.1
  - 5.0
  - 5.2
  - 4.8
  - 4.6
  - 83
  - 102
  - 106
  - 97
  - 94
* -
  - Fall
  - 4.1
  - 5.0
  - 5.2
  - 4.8
  - 4.6
  - 254
  - 312
  - 323
  - 296
  - 288
* - 2050
  - Winter
  - 7.4
  - 9.0
  - 9.3
  - 8.6
  - 8.3
  - 814
  - 1000
  - 1035
  - 949
  - 923
* -
  - Spring
  - 4.1
  - 5.0
  - 5.2
  - 4.8
  - 4.6
  - 455
  - 558
  - 578
  - 530
  - 515
* -
  - Summer
  - 4.1
  - 5.0
  - 5.2
  - 4.8
  - 4.6
  - 149
  - 183
  - 190
  - 174
  - 169
* -
  - Fall
  - 4.1
  - 5.0
  - 5.2
  - 4.8
  - 4.6
  - 455
  - 558
  - 578
  - 530
  - 515
* - {colspan}`12` Industry, Agriculture, Construction
* - 2022
  - Winter
  - 7.0
  - 8.6
  - 8.9
  - 8.2
  - 7.9
  - 360
  - 442
  - 457
  - 419
  - 408
* -
  - Spring
  - 3.9
  - 4.8
  - 5.0
  - 4.5
  - 4.4
  - 201
  - 247
  - 255
  - 234
  - 228
* -
  - Summer
  - 3.9
  - 4.8
  - 5.0
  - 4.5
  - 4.4
  - 66
  - 81
  - 84
  - 77
  - 75
* -
  - Fall
  - 3.9
  - 4.8
  - 5.0
  - 4.5
  - 4.4
  - 201
  - 247
  - 255
  - 234
  - 228
* - 2030
  - Winter
  - 7.4
  - 9.0
  - 9.3
  - 8.6
  - 8.3
  - 455
  - 558
  - 578
  - 530
  - 515
* -
  - Spring
  - 4.1
  - 5.0
  - 5.2
  - 4.8
  - 4.6
  - 254
  - 312
  - 323
  - 296
  - 288
* -
  - Summer
  - 4.1
  - 5.0
  - 5.2
  - 4.8
  - 4.6
  - 83
  - 102
  - 106
  - 97
  - 94
* -
  - Fall
  - 4.1
  - 5.0
  - 5.2
  - 4.8
  - 4.6
  - 254
  - 312
  - 323
  - 296
  - 288
* - 2050
  - Winter
  - 7.4
  - 9.0
  - 9.3
  - 8.6
  - 8.3
  - 814
  - 1000
  - 1035
  - 949
  - 923
* -
  - Spring
  - 4.1
  - 5.0
  - 5.2
  - 4.8
  - 4.6
  - 455
  - 558
  - 578
  - 530
  - 515
* -
  - Summer
  - 4.1
  - 5.0
  - 5.2
  - 4.8
  - 4.6
  - 149
  - 183
  - 190
  - 174
  - 169
* -
  - Fall
  - 4.1
  - 5.0
  - 5.2
  - 4.8
  - 4.6
  - 455
  - 558
  - 578
  - 530
  - 515
:::

The grid fee for the electricity produced by PV has been estimated based on discussions with NVE in 2020 concerning the future structure of grid tariffs. It is assumed that the firm part of the grid fee will be ca. 80% and that locally produced electricity must pay this fee. Due to lower distribution losses, ca. 20% of the grid fee is deducted. Not all electricity produced by PV can be used by the producer, but a part will be transformed to the grid and used by other consumers. This part will have the same costs as other electricity. This cost is added as a seasonal flow cost, based on the assumptions in {numref}`tab-own-consumption-electricity-produced-pv`.

:::{list-table} Own consumption of electricity produced by PV.
:name: tab-own-consumption-electricity-produced-pv
:header-rows: 1
:widths: 19 24 28
:column-align: center center center
:header-align: center

* -
  - Residential
  - Commercial
* - Winter
  - 96%
  - 100%
* - Spring
  - 64%
  - 100%
* - Summer
  - 26%
  - 50%
* - Fall
  - 48%
  - 100%
:::

(sec-energy-prices)=
## Energy prices

The commodities defined in the Fuels file are shown in {numref}`tab-definitions-fuel-commodities-prices-without`. Prices for energy commodities are specified exogenously, meaning that they are provided as model inputs rather than determined endogenously by the model. Some commodities, including biofuels, can be supplied through both domestic production and imports. Emissions associated with the use of the fuel commodities are also defined in the same file.

In the base case, the energy price development is based on information from the power system model EMPIRE {cite}`18`. Alternative price trajectories can be specified in the relevant scenario files. The price development from EMPIRE is presented in {numref}`tab-increase-fossil-fuels-biofuels-prices`. The price of biocoal is assumed to change by the same absolute amount as the price of fossil coal.

The prices of fossil fuels are divided into three components: the underlying production cost, the CO₂ tax, and other applicable taxes. This separation facilitates analyses of alternative taxation levels and structures. The production-cost component is defined in the Fuels file, the CO₂ tax is specified in Scen_CO2, and taxes other than the CO₂ tax are defined in the Scen_A_Taxes scenario file.

The taxes are based on Norwegian tax rates for 2024 {cite}`19`, adjusted to 2021 price levels using the consumer price index. Most of the energy production costs are based on *Klimakur* 2030 {cite}`20`. These values were mainly reported in 2019NOK and have been adjusted to 2021NOK. Municipal waste is associated with a disposal fee, which is represented as a negative fuel cost for waste incineration {cite}`21`. Nonetheless, a substantial share of the cost associated with waste incineration arises from CO₂ taxation. This component is represented through the model’s general CO₂-tax assumptions rather than being included directly in the disposal fee.

A general value-added tax of 25% is applied to costs in single-family houses. Investment costs for residential technologies are specified inclusive of VAT. For energy carriers consumed in single-family houses, VAT is represented as a flow-delivery cost in the Scen_A_Taxes scenario file. Flow-delivery costs also account for the higher unit costs associated with supplying relatively small quantities of wood chips and pellets to the residential and commercial sectors compared with deliveries to industry. The electricity consumption tax is likewise represented as a flow-delivery cost in Scen_A_Taxes. Based on Norwegian tax rates in 2024, the applied rates are 0.58 øre/kWh for industry, 16.44 øre/kWh for the commercial sector, and an estimated 42.7 øre/kWh for the residential sector, including VAT.

:::{list-table} Definitions of fuel commodities and prices, without VAT (2021NOK/MWh){cite}`22`
:name: tab-definitions-fuel-commodities-prices-without
:header-rows: 1
:widths: 13 15 9 9 9 14 27
:column-align: left left center center center center left
:header-align: center

* - {colspan}`2` Output Commodity
  - Cost (NOK/MWh)
  -
  -
  - Other taxes (NOK/MWh)
  - Comments/references (base year)
* -
  -
  - **2018**
  - **2030**
  - **2050**
  -
  -
* - BIO-COAL
  - Biocoal
  - 1000
  - 1102
  - 1167
  - \-
  - Assumption
* - BIO-FOR
  - Biomass-forest
  - 145
  - 173
  - 245
  - \-
  - Statistics Norway
* - BIO-FUEL
  - Biomass-based fuel in transport
  - 1513
  - 1513
  - 1513
  - 297 (TBUS, TTRUCK, TVAN)

    675 (TCAR)
  - Hydrotreated Vegetable Oil (HVO) Freight on Board Q2 2025 {cite}`23`;\
    other taxes = “veibruksavgift”
* - BIO-GAS1
  - Biogas, cost class I
  - 1000
  - 1190
  - 1686
  - \-
  - Estimated from Clean Carbon report 2019
* - BIO-GAS2
  - Biogas, cost class II
  - 2000
  - 2000
  - 2000
  - \-
  - Estimated from Clean Carbon report 2019
* - BIO-WASTE
  - Biomass - residues
  - 105
  - 124
  - 176
  - \-
  - Assumption: cheaper than forest
* - BIO-WOOD
  - Biomass – wood
  - 50
  - 50
  - 50
  -
  - "selvhogst"
* - COAL
  - Coal and coal products (fossil)
  - 285
  - 387
  - 452
  - 0
  - Statistics Norway, industry coal 2019
* - FOS
  - Fossil fuel in transport (based on diesel)
  - 706
  - 861
  - 993
  - 265 (TBUS, TTRUCK, TVAN)

    442 (TCAR)
  - *Klimakur* 2030;\
    other taxes = “veibruksavgift”
* - GAS
  - Gas (based on LPG)
  - 358
  - 417
  - 474
  - 0
  - *Klimakur* 2030
* - LNG
  - Liquid natural gas for maritime
  - 617
  - 717
  - 816
  - 239
  - *Klimakur* 2030;\
    other taxes = grunnavgift mineralolje
* - MGO
  - Marine gas oil
  - 460
  - 615
  - 747
  - 239
  - Rotterdam Bunker Prices {cite}`24`;\
    other taxes = grunnavgift mineralolje
* - OIL
  - Oil (based on light distillate)
  - 565
  - 690
  - 796
  - 239
  - Light fuel oil without VAT;\
    other taxes = grunnavgift mineralolje
* - WASTE
  - Municipal waste
  - -273
  - -273
  - -273
  -
  - NVE
:::

:::{list-table} Increase in fossil fuels and biofuels prices based on EMPIRE[^1].
:name: tab-increase-fossil-fuels-biofuels-prices
:header-rows: 1
:widths: 10 10 10 10 10 10 10

* -
  - 2020-2025
  - 2025-2030
  - 2030-2035
  - 2035-2040
  - 2040-2045
  - 2045-2050
* - Gas
  - 8 %
  - 8 %
  - 6 %
  - 3 %
  - 2 %
  - 2 %
* - Coal
  - 16 %
  - 17 %
  - 6 %
  - 4 %
  - 3 %
  - 3 %
* - Bio
  - 9 %
  - 9 %
  - 9 %
  - 9 %
  - 9 %
  - 9 %
* - Oil
  - 12 %
  - 9 %
  - 4 %
  - 6 %
  - 2 %
  - 2 %
:::

(sec-co2)=
## CO{sub}`2`

IFE-TIMES-Norway accounts for energy-related CO₂ emissions from both onshore and offshore activities. Other greenhouse gases are not currently represented. The model also excludes non-energy-related CO₂ emissions from processes such as fermentation in breweries and bakeries. CO₂ emissions are calculated endogenously based on the model’s use of technologies and energy commodities. The model includes competing technologies that use different energy carriers, as well as carbon capture and storage (CCS) options. This enables the model to identify cost-optimal investment and operational decisions subject to specified CO₂ prices, emission constraints, and other scenario assumptions. This is described in further detail in chapters {numref}`sec-ccs-and-daccs` and {numref}`sec-demand-technologies`.

At present, all CO₂ emissions are represented using a single generic CO₂ commodity. The model therefore does not distinguish between emissions covered by the EU Emissions Trading System (EU ETS) and emissions outside the EU ETS. Further development is planned to introduce this distinction.

The emissions factors for commodity consumption currently applied in the model are presented in {numref}`tab-emission-factors-ton-co2-mwh` {cite}`25`.

:::{list-table} Emission factors (ton CO{sub}`2`/MWh)
:name: tab-emission-factors-ton-co2-mwh
:header-rows: 1
:widths: 17 12 12 10 10 12 12 10

* -
  - FOS
  - OIL
  - COAL
  - GAS
  - WASTE
  - MGO
  - LNG
* - Emissions,\
    ton CO2/MWh
  - 0.26
  - 0.26
  - 0.32
  - 0.21
  - 0.25
  - 0.26
  - 0.20
:::

CO{sub}`2` taxes are included in scenario files and are easily changed. The Medium taxes presented in {numref}`tab-co2-tax-pathways-2018-2050` are used in the base version of the model. These taxes are based on the medium emission pathway of the government {cite}`26` in 2025, discounted to 2021NOK {cite}`7`. A cap on CO{sub}`2` emissions can also be included in analyses with IFE-TIMES-Norway, but this is not used in the base version.

:::{list-table} CO{sub}`2` tax pathways 2018-2050 (NOK/t CO{sub}`2`) {cite}`26`
:name: tab-co2-tax-pathways-2018-2050
:header-rows: 1
:widths: 20 8 8 8 8 8 8

* - Year
  - 2018
  - 2020
  - 2025
  - 2030
  - 2035
  - 2050
* - Medium
  - 500
  - 590
  - 1200
  - 2929
  - 2929
  - 2929
:::

[^1]: Fuel prices are provided by EMPIRE in the FlexBuild project and are based on the projections from the EU reference scenario. A 20% reduction in prices are assumed due to technology development.
