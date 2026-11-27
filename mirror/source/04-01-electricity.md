(sec-electricity)=
# Electricity

(sec-hydropower)=
## Hydropower

Hydropower technologies in IFE-TIMES-Norway are divided into reservoir and run-of-river hydropower. Both categories include representations of existing power plants and investment options for new capacity. Run-of-river plants with a reservoir storage share, referred to as *magasinandel*, of 0.5 or higher are classified as reservoir hydropower. {numref}`tab-hydropower-generation-normal-year-twh` summarises the assumed normal-year generation from existing hydropower plants and the additional generation available through increased precipitation and investments in new capacity.

:::{list-table} Hydropower generation in a normal year, TWh/year.
:name: tab-hydropower-generation-normal-year-twh
:header-rows: 1
:widths: 43 32 23
:column-align: left center center
:header-align: center

* -
  - Total generation in existing plants in a normal year (TWh)
  - Additional generation (TWh)
* - Average generation in 2024
  - 137.7
  -
* - \+ increased precipitation in 2040
  - 140.7
  - 3.0
* - New potential
  - 147.8
  - 10.1
:::

The existing capacities and generation in a normal year are based on information from NVE, and NVE’s «Langsiktig kraftmarkedsanalyse 2030» {cite}`15`. The average annual hydropower generation in 2024 is 137.7 TWh/year. The generation from the existing hydropower plants is assumed to increase further by 3.0 TWh by 2040 due to increased precipitation (from today until 2040) {cite}`27`. This results in an estimated normal-year generation of 140.7 TWh from existing hydropower plants in 2040.

The existing capacities and generation in a normal year are based on information from NVE, and NVE’s *Langsiktig kraftmarkedsanalyse* {cite}`15`. The average annual hydropower generation in 2024 is 137.7 TWh/year. The generation from the existing hydropower plants is assumed to increase further by 3.0 TWh by 2040 due to increased precipitation (from today until 2040) {cite}`27`. This results in an estimated normal-year generation of 140.7 TWh from existing hydropower plants in 2040. The investment potential for new hydropower capacity is based on NVE {cite}`28`. Existing plants combined with the investment potential provide a total normal-year generation of 147.8 TWh.

New hydropower investment options are represented by five technologies in the model: two reservoir hydropower technologies and three run-of-river technologies. Their investment costs are based on levelised costs of electricity ranging from 0.5 to 2 NOK/kWh. The available generation potential for each technology is implemented as a regional activity bound.

The operation of hydropower plants is represented through availability factors. For reservoir hydropower technologies, availability is specified by season. For run-of-river technologies, annual availability is combined with a predefined distribution of generation across the model’s sub-annual time slices.

For new reservoir plants, the operating hours are reduced since new plants seem to increase the capacity more than the generation. The calculation of the availability per season for new reservoir plants is based on the Lysebotn project {cite}`28`, where the capacity is increased by 75% and the generation by 15%, resulting in an average availability of 65.7% of the original availability for existing reservoir plants.

(sec-model-input-based-on-emps-simulations)=
### Model input based on EMPS simulations

The operational hydropower input data is calibrated by using simulations by the EMPS power market model {cite}`29` that is provided by Sintef Energy. The simulations include weekly weather-year data from 2000 to 2015 on unregulated inflow (GWh) and Norwegian hydropower generation (GWh), for each spot-price region.

:::{figure} images/figure-05.png
:name: fig-illustration-unregulated-hydro-inflow-no2

Illustration of unregulated hydro inflow in NO2 for weather years from 2000-2015, where the black line is the average, and the other line colours represent different weather years
:::

First, it is assumed that the unregulated hydro inflow characteristics, as demonstrated in {numref}`fig-illustration-unregulated-hydro-inflow-no2`, correspond to the weekly hydropower generation of the run-of-river plants in IFE-TIMES-Norway. The unregulated hydro inflow data is used to map how the unregulated hydropower generation is distributed within the four modelled seasons and to capture the annual variations in the power generation.

In the deterministic model version, weather-dependent operational hours are not considered in the run-of-river hydropower generation. However, unregulated hydro inflow has been used to map how the run-of-generation is distributed throughout the four seasons. The corresponding results and model input are shown in {numref}`tab-model-input-seasonal-generation-distribution`, and is based on an average of the simulated weather years.

:::{list-table} Model input on seasonal generation distribution of run-of-river plants in the five spot-price regions.
:name: tab-model-input-seasonal-generation-distribution
:header-rows: 1
:widths: 16 16 16 16 16 16
:column-align: left center center center center center
:header-align: center

* -
  - NO1
  - NO2
  - NO3
  - NO4
  - NO5
* - Winter
  - 0.09
  - 0.15
  - 0.19
  - 0.06
  - 0.08
* - Spring
  - 0.18
  - 0.16
  - 0.16
  - 0.07
  - 0.10
* - Summer
  - 0.43
  - 0.39
  - 0.32
  - 0.51
  - 0.48
* - Fall
  - 0.30
  - 0.30
  - 0.33
  - 0.36
  - 0.34
* - Total
  - 1.00
  - 1.00
  - 1.00
  - 1.00
  - 1.00
:::

In contrast, in the stochastic model version, it is assumed that the seasonal distribution and the annual operational hours are weather-dependent. The stochastic scenarios, which are designed to capture weather dependency, consider the seasonal generation for all weather years, which is illustrated for NO2 in {numref}`fig-seasonal-run-river-generation-no2`.

:::{figure} images/figure-06.png
:name: fig-seasonal-run-river-generation-no2

Seasonal run-of-river generation for NO2 for weather years from 2000 to 2015.
:::

In addition, it is assumed that the regulated hydropower generation equals the Norwegian power generation minus the unregulated hydropower inflow. The corresponding weekly generation characteristics for NO2 are illustrated in {numref}`fig-illustration-regulated-hydro-power-generation`.

:::{figure} images/figure-07.png
:name: fig-illustration-regulated-hydro-power-generation

Illustration of regulated hydro power generation in NO2 for weather years from 2000 -2015, where the black line is the average and the other line colours represent different weather years.
:::

For the deterministic model version, this information is used to derive the upper limit for operational hours of the regulated hydropower generation for each spot region, which is based on the average generation over the weather years. See {numref}`tab-upper-limit-operational-hours-regulated` for an overview of the corresponding model inputs. Note, as mentioned above, it is assumed that the operational hours for new regulated hydropower plants are 65.7% of the full-load operational hours of the existing plants.

:::{list-table} Upper limit for operational hours for regulated hydropower generation.
:name: tab-upper-limit-operational-hours-regulated
:header-rows: 1
:widths: 17 14 12 13 11 11
:column-align: left center center center center center
:header-align: center

* -
  - NO1
  - NO2
  - NO3
  - NO4
  - NO5
* - Existing
  - 3633
  - 3700
  - 4056
  - 4492
  - 3428
* - New
  - 2387
  - 2431
  - 2665
  - 2951
  - 2252
:::

For the stochastic model version, it is considered that the operational hours are weather dependent. The stochastic scenarios, which are designed to capture weather dependency, take into account the variation in annual generation from regulated plants for all weather years, as is illustrated for NO2 in {numref}`fig-weather-dependent-operational-hours-existing`.

:::{figure} images/figure-08.png
:name: fig-weather-dependent-operational-hours-existing

Weather-dependent operational hours of existing regulated hydropower plants for NO2 for weather years from 2000 to 2015.
:::

(sec-onshore-wind-power)=
## Onshore wind power

The installed capacities of existing wind power plants {cite}`30` are summarized in {numref}`tab-data-existing-wind-power-plants`, along with their respective capacity factors calculated based on generation data obtained from Statistics Norway (SSB).{numref}`tab-data-existing-wind-power-plants` The total wind power generation in 2024 is 14.5 TWh {cite}`31`. The lifetime for all wind power plants is assumed to be 25 years, and lifetime extension is implemented in the model. The variable operating and maintenance costs are 10 øre/kWh today, and declining to 7.6 øre/kWh in 2050, based on {cite}`21`.

:::{list-table} Data on existing wind power plants.
:name: tab-data-existing-wind-power-plants
:header-rows: 1
:widths: 12 30 30
:column-align: center center center
:header-align: center

* - Region
  - Installed capacity in 2024 (MW)
  - /Capacity factor in 2024
* - NO1
  - 385
  - 0.26
* - NO2
  - 1425
  - 0.37
* - NO3
  - 2108
  - 0.31
* - NO4
  - 1159
  - 0.33
* - NO5
  - \-
  - \-
* - Total
  - 5076
  - 0.33
:::

New wind power plants are modelled as 10 different classes: three levels of investment costs and three levels of full load hours and, in addition, a high cost/high potential alternative. The medium cost class is based on NVE, while lower and high classes are assumed to be 25% lower/higher. The investment cost classes in 2020 are:

- Low: 10436 NOK/kW

- Medium: 13915 NOK/kW

- High: 17394 NOK/kW

For future investments, a technology learning rate of 24% from 2018 to 2035 is used, based on {cite}`21`. The investment costs are interpolated between the specified model periods and extrapolated from 2035.

The full-load operational time for future wind power plants is divided into three classes:

- High (20% higher than the regional average of today),

- Medium (10% higher than the regional average of today),

- Low (regional average of today).

Potential for new wind power is divided into two segments. Investments that are more likely to occur are included based on NVE’s projections from LA25 {cite}`32`.Investments that are more likely to occur are included based on NVE’s projections from LA25 {cite}`28`. This corresponds to an additional 3132 MW capacity beyond the existing capacity of 5076 MW. The potential gives 9.8 TWh of new production as shown by spot price region in {numref}`tab-upper-limit-wind-power-potential`, distributed equally between technology classes 1-9. The tenth class reflects additional theoretical potential besides what is projected by NVE and adds another 4.8 GW (13.8 TWh) of potential with the high cost and medium full-load hours. The total potential is based on Statkraft’s “NetZero low” projection, reaching 30 TWh production in 2050 {cite}`33`. This includes both new installations as well as reinvestments in existing capacity.

:::{list-table} Upper limit of wind power potential by 2050 in a normal year, TWh/year.
:name: tab-upper-limit-wind-power-potential
:header-rows: 1
:widths: 32 10 10 10 10 10 12
:column-align: left center center center center center center
:header-align: center

* -
  - NO1
  - NO2
  - NO3
  - NO4
  - NO5
  - Norway
* - Reinvestments
  - 1.1
  - 5.5
  - 6.0
  - 3.8
  - 0
  - 16.4
* - Concessions (class 1-9)
  - 0.9
  - 3.6
  - 2.9
  - 2.2
  - 0.3
  - 9.9
* - Additional potential (class 10)
  - 0.14
  - 0.17
  - 0.97
  - 0.37
  - 0
  - 1.7
* - Total
  - 2.1
  - 9.3
  - 9.9
  - 6.4
  - 0.3
  - 30
:::

Reinvestment in wind power plants is also implemented in IFE-TIMES-Norway. The investment cost is assumed to be 20% lower than the average cost of new wind power. The percentage is estimated based on a review of license applications, in which costs associated with existing infrastructure, such as roads, power lines, and foundations, are excluded. The possible capacity of reinvestment is restricted to existing wind power plants in 2024. It is assumed that reinvestments are 20% more efficient compared to the existing plants based on technical improvements in wind turbine technology.

(sec-offshore-wind-power)=
## Offshore wind power

To add a detailed representation of offshore wind, five additional regions have been added to the model. The regions are based on the 18 areas proposed by NVE in 2025 as suitable for the development of offshore wind {cite}`34`. The areas are identified as “low risk” for potential conflicts of interest among aquaculture, fisheries, shipping, environmental interests, and petroleum extraction, and considered as technically suitable areas within the North Sea. The 18 areas are presented in {numref}`fig-offshore-wind-areas-proposed-nve`. To reduce the number of regions in the model, the areas have been grouped into five regions with the following clusters: Nordavind: Nordavind C-D, Nordvest: Nordvest A-C, Vestavind1: Vestavind A-D, Vestavind2: Vestavind E (including F), Sørvest: Sørvest A-F + Sønnavind A.

:::{figure} images/figure-09.png
:name: fig-offshore-wind-areas-proposed-nve

Offshore wind areas proposed by NVE {cite}`34` with the grouping into 5 regions.
:::

Currently, offshore wind is only included as a new investment technology in the model. The investment costs and technical parameters vary by region, depending on whether the foundation is bottom-fixed or floating and whether shore connection is AC or DC. The breakdown for the investment costs in 2030 is given in {numref}`tab-break-down-investment-costs-offshore`. The costs are based on estimates provided by AFRY {cite}`35` for NVE {cite}`36`. Differences in depth, terrain, and wave conditions are not included (with the exception of foundation type). The investment costs per MW for the specific offshore regions considered in the model are given in {numref}`tab-annual-capacity-factor-cf-capacity`. Additionally, it is assumed that technology trend multipliers of 0.89 and 0.70 by 2040 and 0.83 and 0.63 by 2050 apply for bottom-fixed and floating investments, respectively. The trend is applied for both investment costs and operation and maintenance costs, based on learning curves from Danish Energy Agency {cite}`37`. These trends lead to slightly lower investment costs for floating foundations by 2050 compared to bottom-fixed investments.

:::{list-table} Break-down for the investment costs for offshore wind power in 2030 (kNOK) {cite}`35`.
:name: tab-break-down-investment-costs-offshore
:header-rows: 1
:widths: 50 17 17
:column-align: left center center
:header-align: center

* -
  - {colspan}`2` 2030
* -
  - Bottom-fixed
  - Floating
* - Capacity of wind farm (MW)
  - 1496
  - 506
* - Turbine
  - 22 465 327
  - 7 380 731
* - Inter Array cables
  - 3 028 248
  - 1 606 034
* - Substructure and foundation
  - 11 213 987
  - 10 142 961
* - Total investment costs (kNOK)
  - 36 707 562
  - 19 129 726
* - Investment costs per MW (kNOK/MW)
  - 24 537
  - 37 806
:::

For all regions, except Sørvest, one technology is defined, EE-WIND_OFF, with a given cost and capacity potential. The cost depends on the foundation type, as given in {numref}`tab-annual-capacity-factor-cf-capacity`. For the Sørvest region, seven technology processes are defined according to the single areas included in the grouping. The reasoning for this split is due to the large capacity potential of this region, as well as the proximity to Europe, making the region particularly favourable for investments. The seven technologies are differentiated by cost according to their distance to shore and the foundation type. This creates different cost classes, in which some capacity is more expensive to invest in than others within the region.

The potential investment capacity in 2030 is limited based on the two areas, Utsira Nord (located in Vestavind 2) and Sørlige Nordsjø II (Located in Sørvest F). The total capacity of the two areas is 2 GW (1.5 GW for Sørlige Nordsjø II and 500 MW for Utsira Nord). As the tender for Sørlige Nordsjø II is finalized, it is assumed that the 1.5 GW will be in operation by 2030, and hence this investment is fixed. By 2035, investment options in the remaining regions are allowed, in which each of the NVE areas was assumed to have a capacity potential of 500 MW in 2035. The total capacity potential sums up to 2 GW in 2030, 11.5 GW in 2035, and 27.5 GW in 2040 (based on the Norwegian target for offshore wind of 30 GW by 2040 {cite}`38`). Production profiles and annual capacity factors for different weather years for each of the offshore areas are provided by NVE. These are further averaged across the areas assigned to the respective regions. The capacity expansion potential, capacity factor, investment cost, and foundation type for each offshore region are given in {numref}`tab-annual-capacity-factor-cf-capacity`.

:::{list-table} Annual capacity factor (CF), capacity expansion potential (MW), investment cost in 2030 (kNOK/MW), fixed OPEX costs in 2030 (kNOK/MW/year), and type of foundation.
:name: tab-annual-capacity-factor-cf-capacity
:header-rows: 1
:widths: 17 10 10 10 12 11 9 14
:column-align: center center center center center center left left
:header-align: center

* - Offshore area
  - CF
  - Capacity 2030
  - Capacity 2035
  - Capacity 2040
  - Inv. cost 2030
  - OPEX 2030
  - Foundation
* - Nordavind
  - 0.494
  - 0
  - 1000
  - 2500
  - 37806
  - 1410
  - Floating
* - Nordvest
  - 0.483
  - 0
  - 1500
  - 3750
  - 37806
  - 1410
  - Floating
* - Vestavind1
  - 0.489
  - 0
  - 2000
  - 5000
  - 37806
  - 1410
  - Floating
* - Vestavind2
  - 0.512
  - 500
  - 1000
  - 2500
  - 37806
  - 1410
  - Floating
* - Sørvest
  -
  -
  -
  -
  -
  -
  -
* - Sørvest A
  - 0.545
  - 0
  - 500
  - 1500
  - 30530
  - 691
  - Bottom fixed
* - Sørvest B
  - 0.543
  - 0
  - 500
  - 1500
  - 29870
  - 656
  - Bottom fixed
* - Sørvest C
  - 0.551
  - 0
  - 500
  - 1500
  - 29582
  - 641
  - Bottom fixed
* - Sørvest D
  - 0.545
  - 0
  - 500
  - 1500
  - 31248
  - 728
  - Bottom fixed
* - Sørvest E
  - 0.561
  - 0
  - 500
  - 1500
  - 29755
  - 650
  - Bottom fixed
* - Sørvest F
  - 0.559
  - 1500
  - 3000
  - 4750
  - 30358
  - 682
  - Bottom fixed
* - Sønnavind A
  - 0.565
  - 0
  - 500
  - 1500
  - 37806
  - 1410
  - Floating
:::

Due to locational restrictions, it is assumed that only Sørvest region can export electricity to Europe. Connections to the UK, Western Denmark, Germany and the Netherlands are currently included in the model. For the remaining areas, the model can invest in one-direct connection to the adjacent spot region in Norway or to the nearby oil & gas region (addressed in {numref}`sec-demand-projection`).

The cost of the transmission cables is determined based on the length of the cable. As several areas are grouped in one region, the assumed length of the cable is based on the maximum distance to the farthest region within the group. The detailed assumptions can be found in the file “Offshore costs”, which can be shared on request. Moreover, the length of each cable is determined using coordinates and Google Maps, and can be viewed here: [{u}`Map`](https://www.google.com/maps/d/u/0/edit?mid=1R7-6WfvyVf4WhRPW8FgDAYxVLEQ_m0A&usp=sharing). For Sørvest, a hub structure is assumed in which all offshore areas connect to one hub, which is further connected to Norway and neighbouring countries. Hence, the cable cost from Sørvest to NO2 is based on the length from the hub to mainland, while each of the seven wind processes defined in the region includes the cost of building a cable from the specific area to the hub. For the remaining regions, the separate offshore areas are assumed to connect directly to shore, and not through a hub, as the areas are more spread out. The capacities of the trade cables are limited to the capacities of the respective offshore wind park, as presented in {numref}`tab-annual-capacity-factor-cf-capacity`. The connection point to mainland for each offshore region, along with the respective investment cost for the cables in 2030 are given in {numref}`tab-investment-cost-export-cable-respective`.

:::{list-table} Investment cost of export cable for the respective trade connections.
:name: tab-investment-cost-export-cable-respective
:header-rows: 1
:widths: 22 18 28 28
:column-align: left center center center
:header-align: center

* - Offshore area
  - Export connection
  - Investment cost [kNOK/MW]
  - Fixed OPEX [kNOK/MW/year]
* - Nordavind
  - NO4
  - 19 836
  - 261
* - Nordvest
  - NO3
  - 19 546
  - 251
* - Vestavind1
  - NO5
  - 6 826
  - 150
* - Vestavind2
  - NO2
  - 6 251
  - 120
* - {rowspan}`2` Sørvest
  - NO2
  - 18 882
  - 229
* - DK1

    DE

    NL

    UK
  - 23 486

    32 652

    31 201

    29 873
  - 383

    688

    639

    595
:::

As offshore wind parks are located outside the Norwegian coast, each park has been modelled as a separate region. This is accomplished by creating a “BookRegion”, as defined in the TIMES documentation {cite}`4`, including both the offshore wind regions, as well as the offshore oil and gas regions. The benefit of having a separate “book” is that definitions given for “AllRegions” in the original model do not apply to the offshore regions. This is convenient as the offshore regions should only include technologies related to offshore wind production, supply technologies (electricity and gas) for the offshore oil and gas demand, as well as the transmission cables. The definition of the technologies and demand projections for the offshore regions is defined in a separate Base Template file named “VT_Offshore”.

Due to the current political decision to allow only radial connections to Norway as a first-phase development {cite}`39`, an additional restriction is included to force investments in transmission cables to Norway before investments are allowed to Europe. This is implemented by limiting the capacity of cables to Europe by the capacity of cables to Norway, through a user constraint. Hence, hybrid cables are allowed, but with the condition that radial connections are established first. This restriction can be disabled or altered based on the regulations implemented when the first offshore wind area in Norway is realized.

Lastly, a line was added in the SysSettings file to allow for negative variable cost components in the objective function. This is a special case that occurs when adding regions without any demand to the model. As the offshore wind regions only produce electricity, their contribution to the objective function will be negative as the revenue exceeds the cost. As the OBJVAR variables is non-negative by default, the model would choose to export the electricity through another region having variable costs in order to realize the revenues. To avoid this, the line in {numref}`tab-line-added-syssettings-allow-negative` was added.

:::{list-table} Line added in SysSettings to allow for negative variable cost components in the objective function.
:name: tab-line-added-syssettings-allow-negative
:header-rows: 1
:widths: 15 15 14 15

* - LimType
  - Attribute
  - UC_N
  - Allregions
* - N
  - UC_RHS
  - OBJVAR
  - -1
:::

(sec-solar-pv)=
## Solar PV

(sec-building-applied-pv)=
### Building applied PV

Building-applied photovoltaic (BAPV) electricity production is included in the model as existing and new technologies. Existing PV installations are segregated into residential and commercial types. Their respective installed capacities in 2024 in the different electricity price regions were obtained from elhub.no {cite}`40` ({numref}`tab-existing-bapv-installations-2024`). While new investments in BAPV are modelled in detail based on different orientations and tilts, the existing PV installations are included with only one profile corresponding to 30° south for residential buildings and 10° east-west for commercial buildings.

:::{list-table} Existing BAPV installations in 2024.
:name: tab-existing-bapv-installations-2024
:header-rows: 2
:widths: 18 28 28
:column-align: center center center
:header-align: center

* - {rowspan}`2` Electricity Price Region
  - {colspan}`2` Installed BAPV Capacity, MW
* - Residential
  - Commercial
* - NO1
  - 124
  - 220
* - NO2
  - 116
  - 183
* - NO3
  - 18
  - 33
* - NO4
  - 3
  - 3
* - NO5
  - 32
  - 34
:::

New BAPV investments are segregated into more categories: single-family houses, multi-family houses, commercial buildings, light industry buildings, and agriculture. The technical potential for BAPV capacity on existing roofs is calculated as described in {cite}`41`. In the report, the area utilization for building-applied PV for eight different building categories: single-family houses, multi-family houses, garages, leisure homes, commercial buildings, industry, agriculture, and storage buildings, is calculated. The area utilizations consider the size of the rooftops and the construction on the roofs to find the average available area of the rooftop that can technically be used for BAPV installation.

The total potential capacity distributed for building categories and spot price regions can be seen in {numref}`tab-overview-technical-potential-building-applied`. In total, there is a technical potential for approximately 45 GW based on the existing rooftops.

:::{list-table} Overview of the technical potential for building-applied PV in the different building categories for the five spot price regions. The technical potential is given in MW.
:name: tab-overview-technical-potential-building-applied
:header-rows: 1
:widths: 36 10 10 10 10 10 11
:column-align: left center center center center center center
:header-align: center

* - Building category
  - NO1
  - NO2
  - NO3
  - NO4
  - NO5
  - Total
* - Single-family house
  - 4 991
  - 3 846
  - 2 405
  - 1 476
  - 1 199
  - 13 917
* - Multi-family house
  - 840
  - 349
  - 266
  - 134
  - 190
  - 1 779
* - Garage
  - 2 807
  - 1 865
  - 1 173
  - 756
  - 542
  - 7 143
* - Leisure homes (cabin)
  - 1 211
  - 984
  - 739
  - 450
  - 466
  - 3 850
* - Commercial
  - 1 597
  - 1 162
  - 796
  - 550
  - 436
  - 4 541
* - Industry
  - 617
  - 563
  - 401
  - 197
  - 147
  - 1 925
* - Storage buildings
  - 904
  - 586
  - 392
  - 254
  - 213
  - 2 349
* - Agriculture
  - 3 253
  - 2 222
  - 2 378
  - 809
  - 619
  - 9 281
* - Total
  - 16 219
  - 11 577
  - 8 550
  - 4 627
  - 3 813
  - 44 785
:::

For simplicity, single-family houses (RESS) include garages, and commercial buildings (COM) include storage buildings, resulting in five different building categories that are considered (single-family house, multi-family house, commercial, industry, and agriculture). The potential for leisure homes is excluded from the base file since this category is significantly different from the single-family houses and does not fit with the other building categories either. Additionally, an in-house sensitivity analysis has shown that including or excluding the potential for leisure homes does not impact the result to any great extent. The potential for leisure homes can therefore be added to a separate scenario file that could optionally be used.

In the report {cite}`41`, the potential is further divided based on orientation and tilt of the rooftops. In total, eight different orientations, North, North-East, East, South-East, South, South-West, West, and North-West, and four different tilts, 10° (flat roofs), 20°, 30°, and 40°, have been used. To reduce the number of technologies and details in the base model, the potential is further aggregated into two different tilts, 10° (flat roofs) and 30°. For the flat roofs (10°), only east-west orientation is considered, meaning that if one panel is placed in the east direction, then one panel is also placed in the west direction. These panels are modelled separately, but to ensure equal capacity investments for the two orientations, a user constraint is added. For roofs with a tilt of 30°, four different orientations are considered: North, East, South, and West. This results in a total number of 30 BAPV technologies (five building categories and six different tilts and orientations in total). The more detailed modelling of BAPV, as described in the report {cite}`41`, is included in a separate scenario file that could be used optionally. This file also includes options for single-oriented PV panels on flat roofs.

In addition to the technical potential based on existing rooftops, an estimation of future building stock is included. The future building area is calculated based on the main alternative of population by SSB {cite}`42`. It is assumed that the ratio rooftop/building area is constant and that the relative tilt and orientation of rooftops are as average today. The new area increase for the different building categories can be seen in {numref}`tab-new-area-increase-bapv-2050`.

:::{list-table} New area increase for BAPV in 2050.
:name: tab-new-area-increase-bapv-2050
:header-rows: 1
:widths: 40 26
:column-align: left center

* - Building category
  - New area increase
* - Single-family house
  - 117%
* - Multi-family house
  - 156%
* - Commercial, industry, agriculture
  - 112%
:::

The investment costs in 2020 are based on costs from Multiconsult {cite}`43`. They provide a cost interval ranging from low to high, in which it is assumed that the medium cost is the average. In the base file, the medium cost is used; however, sensitivity analysis can be performed with the low and high values. The cost of PV in single-family houses includes a 25% VAT. The future costs are calculated based on the development of large-scale solar PV presented by IEA in {cite}`44`. Investment costs are reduced by 42% from 2020 to 2030 and by 57% from 2020 to 2050. The fixed operation and maintenance cost is calculated as 0.5% of investment cost, based on NVE {cite}`45`. An overview of the costs and lifetime inputs for BAPVs in the model is presented in {numref}`tab-costs-lifetime-bapv`.

:::{list-table} Costs and lifetime of BAPV.
:name: tab-costs-lifetime-bapv
:header-rows: 1
:widths: 22 11 10 11 9 10 8 12
:column-align: center center center center center center center center
:header-align: center

* -
  - {colspan}`3` Investment cost
  - {colspan}`3` Operation and maintenance cost
  - Lifetime
* -
  - {colspan}`3` NOK/kW
  - {colspan}`3` NOK/kW
  - years
* -
  - **2018**
  - **2030**
  - **2050**
  - **2018**
  - **2030**
  - **2050**
  -
* - Single-family houses
  - 16 000
  - 9 300
  - 6 900
  - 80
  - 47
  - 35
  - 30
* - Commercial and Multi-family houses
  - 9 500
  - 5 500
  - 4 100
  - 48
  - 28
  - 21
  - 30
:::

PV production profiles are determined based on hourly solar radiation profiles from PVGIS {cite}`46`. The solar radiation data is calculated based on satellite photos and re-analysis with weather models for the northern hemisphere (from 65° North) {cite}`47`. The data is collected from 2005 to 2020 for the cities of Tromsø, Bergen, Trondheim, Kristiansand, and Oslo, representing the five regions of IFE-TIMES-Norway. The solar radiation profiles are differentiated based on the regions, as well as the described tilts and orientations. In total, 30 profiles are collected for the base model.

The solar radiation profiles are further transformed into estimated AC generation data for the five different regions, tilts, and orientations. From this, the annual availability factor (AFA) is calculated. To make the PV production profiles in the 96 time-slice format used in the base model, the hourly profile is averaged based on the respective days belonging to the four different seasons. Hence, an average hourly profile is generated for a representative day for each of the seasons.

As described in Section {numref}`sec-energy-carriers-and-emissions`, not all electricity produced by PV will be used by the producer, but a part will be sold to the grid and used by other consumers. This part will have the same costs as other electricity, which is added as a seasonal flow cost, based on the assumptions presented in {numref}`tab-own-consumption-electricity-produced-pv`.

(sec-solar-power-parks)=
### Solar power parks

PV parks are included as a new technology based on the solar power park concessions applied to NVE {cite}`48`. Four new solar park technologies are added with the technology data given in {numref}`tab-technology-data-solar-parks`. The first three technologies are based on the current concessions to NVE, while the last one represents new potential. In total, 32 of the concessions are included in the base file.

The solar park technologies based on the concessions are divided into three different cost classes. The cost classes are based on the expected investment cost of the projects. The operation and maintenance cost is 2% of the investment cost. Since the concession-applied power plants vary in start year, the investment cost is assumed to be constant until 2030. In 2050, the technology cost is assumed to decrease by 26% from 2030 to 2050, based on IEA {cite}`44`.

The start year of the technology is based on the timeline of the concession, and hence the potential increases from 2020 to 2030. The potential capacity in 2030 is 1171 MW in NO1 and 256 MW in NO2, no concession is applied for in NO3, NO4, and NO5. The annual capacity factor is assumed to be 25% higher than for building-applied PV, based on information from NVE. The production profile of the solar power parks follows the same profile as the south 30-degree tilt profile for BAPV.

Lastly, an additional solar park technology is added with a high cost. This technology represents new potential besides the concessions and currently has no capacity bound. In the base file, the start year is set to 2100. This technology is added as an option to expand the potential for solar parks by changing the start year. The price for this investment is set to a relatively high value to be conservative, due to the lack of references for the investment cost of solar parks in Norway today. The cost is based on the upper level provided by Multiconsult {cite}`43`.

:::{list-table} Technology data for solar parks.
:name: tab-technology-data-solar-parks
:header-rows: 1
:widths: 27 12 12 13 10 12 12
:column-align: left center center center center center center
:header-align: center

* -
  - {colspan}`3` Investment cost
  - {colspan}`2` Operation and maintenance cost
  - Lifetime
* -
  - {colspan}`3` kNOK/MW
  - {colspan}`2` kNOK/MW
  - years
* -
  - **2020**
  - **2030**
  - **2050**
  - **2020**
  - **2050**
  -
* - Low cost, concession
  - 5 500
  - 5 500
  - 4 070
  - 110
  - 81
  - 30
* - Medium cost, concession
  - 6 500
  - 6 500
  - 4 810
  - 130
  - 96
  - 30
* - High cost, concession
  - 7 500
  - 7 500
  - 5 550
  - 150
  - 111
  - 30
* - High cost
  - 8 000
  - 8 000
  - 5 920
  - 160
  - 118
  - 30
:::

(sec-nuclear-power)=
## Nuclear power

Investment options in nuclear power are included in all regions. It is currently modelled as a daynite technology, where the electricity production is assumed to be flat throughout the day. The production is constrained through an availability factor of 0.96. Since the costs and assumptions regarding nuclear power are highly uncertain, nuclear power is excluded from the base model runs by default. This is done by setting START=2100. The cost of nuclear power in the model is modelled according to the low scenario following the Norwegian Nuclear Commission’s estimates {cite}`49`. The costs following both the low and high scenarios are summarized in {numref}`tab-overview-costs-related-nuclear-power`. In the model, the variable O&M costs include the fuel costs and the waste and decommissioning costs. The nuclear power implementation can, however, be used to analyse under what conditions nuclear power will be a cost-efficient solution in the Norwegian energy system. IFE is currently coordinating an ongoing international IEA-ETSAP project to better establish good modelling practices regarding costs and methodology for nuclear power, including Small Modular Reactors (SMRs). Moreover, an internal project, together with nuclear experts at IFE, is ongoing to better understand the technical and economic parameters of nuclear power in Norway.

:::{list-table} Overview of costs related to nuclear power following the low and high cost scenarios from the Norwegian Nuclear Commission {cite}`49`
:name: tab-overview-costs-related-nuclear-power
:header-rows: 1
:widths: 33 33 33
:column-align: left center center
:header-align: center

* -
  - Low
  - High
* - Investment costs [NOK/MW]
  - 109 000
  - 177 000
* - Fuel costs [NOK/GWh]
  - 60
  - 70
* - Waste, decommissioning, etc. [NOK/GWh]
  - 70
  - 200
* - Fixed O&M costs [NOK/MW]
  - 1 610
  - 2 515
* - Other Variable O&M costs [NOK/GWh]
  - 115
  - 187
:::

(sec-combined-cycle-natural-gas-power-plant-with-ccs)=
## Combined cycle natural gas power plant with CCS

Investment options in combined cycle natural gas (CCNG) with CCS are included in regions NO2, NO3, NO4, and NO5. Investment option in NO1 is excluded due to lack of natural gas plants in the region. Since the willingness to invest is highly uncertain, CCNG with CCS is excluded from the base model runs by default by setting START=2100. The efficiency is assumed to be 0.48 with a yearly availability factor of 0.85. The capturing technology is assumed to have an efficiency of 90 %. {numref}`tab-overview-costs-related-combined-cycle` shows an overview of the related costs. Both costs and efficiency are based on {cite}`37`, with 9610 kNOK{sub}`2016`/MEUR{sub}`2020` as the conversion factor combining conversion rate (10,74 NOK{sub}`2020`/EUR{sub}`2020` {cite}`50`) and discount factor (1,118 NOK{sub}`2016`/NOK{sub}`2020` {cite}`7`).

:::{list-table} Overview of costs related to Combined cycle natural gas power plant with CCS
:name: tab-overview-costs-related-combined-cycle
:header-rows: 1
:widths: 39 17 18 25
:column-align: left center center center
:header-align: center

* -
  - 2020
  - 2030
  - 2050
* - Investments cost [NOK{sub}`2016`/MW]
  - 24050
  - 16470
  - 14870
* - Fixed O&M cost [NOK{sub}`2016`/MW]
  - 740
  - 530
  - 480
* - Variable O&M cost [NOK{sub}`2016`/GWh]
  - 54
  -
  - 50
:::

Costs related to transport and storage of captured CO2 is as described in {numref}`sec-ccs-and-daccs`.

(sec-electricity-storage)=
## Electricity storage

The electricity storage technology is included as a new technology in residential and commercial buildings, other/light industry and agriculture, as well as utility-scale storage in the grid. The storage technology represents micro- to small-scale batteries suitable for increasing self-consumption within a day-night cycle. The battery storage is modelled as a *DAYNITE* level storage, which is assumed to only be able to store electricity over a day-night cycle. The C-rate of a battery storage is taken into account with the attribute *NCAP_AFC*. The relation between *DAYNITE* and *SEASONAL* level *NCAP_AFCs* and C-rates are presented in Eq. (1) and (2), respectively. Note that the 24 h used to define the DAYNITE cycle in eq. (1) does not change with the time-slice definition (see detailed explanation [{u}`here`](https://forum.kanors-emr.org/showthread.php?tid=1322&pid=7011#pid7011)).

> $NCAP\_ AFC\sim DAYNITE = \frac{{C_{RATE}}^{- 1}}{24}$ (1)
>
> $NCAP\_ AFC\sim SEASON = \frac{{C_{RATE}}^{- 1}}{8760}$ (2)

Electricity storage-related techno-economic data is presented in {numref}`tab-electricity-storage-technology-data`. Investment costs are based on NREL {cite}`51`, provided as energy (INVCOST_EN) and power (INVCOST_PW) cost of different durations (C-rates). In the base case, the mid projection by NREL is adopted. Fixed O&M costs are assumed to be 2.5% of the investment cost {cite}`51`. For single-family houses, the investment cost is 25% higher due to VAT.

Due to the use of attribute *NCAP_AFC*, the capacity of a battery storage describes its nominal maximum output level, in power terms. Therefore, the investment cost input to the model must be converted to unit of capacity (kNOK/MW) using Eq. (3), where INVCOST_EN corresponds to the energy cost of the battery (kNOK/MWh), and INVCOST_PW corresponds to the power cost of the battery (kNOK/MW).

$INVCOST(kNOK/MW) = INVCOST\_ EN\ (kNOK/MWh)*{C_{RATE}}^{- 1} + INVCOST\_ PW(kNOK/MW)$ (3)

In TIMES-VEDA’s results tab, the nominal maximum output of a battery storage (i.e., *VAR_CAP*) can be converted to storage capacity in terms of energy with Eq. (4). For *DAYNITE* level storage, *G_CYCLE* = 365, while for a *SEASONAL level* storage, *G_CYCLE* = 1. Furthermore, the reader should note that *VAR_CAP* is given in capacity (MW), while energy capacity is given in activity (GWh).

$Energy\ capacity\ (GWh) = VAR\_ CAP(MW)*NCAP\_ AFC*PRC\_ CAPACT/G\_ CYCLE$ (4)

The *VAR_ACT* represents the energy stored in the battery for a specific time slice. The relationship between the energy capacity and the maximum energy stored in the battery throughout the period can be found by multiplying the energy capacity by the number of days in the defined season (in this case 365/4), which is the number of hours one time slice in the model represents (in this case 8760/96). For example, if the energy capacity of the battery calculated using Eq. (4) is 0.01 GWh, the maximum of the *VAR_ACT* attribute for the given period would be 91.25\*0.01 $\leq$ 0.9125 GWh. If the storage is fully utilized for every hour within the time slice, the MAX(VAR_ACT) = 0.9125. *VAR_Fout* and *VAR_Fin* represent the charging/discharging flows. In Eqs. (2) and (3), it is assumed that *PRC_CAPACT = 8.76*.

:::{list-table} Electricity storage technology data.
:name: tab-electricity-storage-technology-data
:header-rows: 1
:widths: 51 9 18 18
:column-align: left right center center

* -
  -
  - Buildings sector
  - Utility scale
* - {colspan}`2` Calendar life (years)
  - 15
  - 15
* - Energy investment cost (NOK/kWh){sup}`1`
  - 2020
  - 2136
  - 1709
* -
  - 2030
  - 1858
  - 1486
* -
  - 2040
  - 1300
  - 1040
* -
  - 2050
  - 929
  - 743
* - Power investment cost (NOK/kW){sup}`1`
  - 2020
  - 3344
  - 2675
* -
  - 2030
  - 3111
  - 2489
* -
  - 2040
  - 2879
  - 2303
* -
  - 2050
  - 2693
  - 2155
* - {colspan}`2` Storage efficiency (%)
  - 90
  - 82
* - {colspan}`2` Duration (h) (${\mathbf{C}_{\mathbf{RATE}}}^{\mathbf{- 1}}\mathbf{)}$
  - 0.5
  - 2
* - {colspan}`2` Availability factor, storage capacity (%)
  - 2{sup}`2`
  - 8
* - {colspan}`2` Availability factor, bound on input/output flows (%)
  - 100
  - 100
* - {colspan}`2` Cycle life (# of cycles)
  - 4500{sup}`3`
  - 4500
* - {colspan}`2` Capacity to activity
  - 8.76
  - 8.76
:::

{sup}`1` Source: {cite}`51`. Used to calculate investment cost in unit of capacity using eq. (3). Building sector cost for single-family houses is 25% higher due to VAT. Conversion rate of 7.43 NOK{sub}`2021`/USD{sub}`2024` is used, based on the average rate of 2024 (year prices are given for) and the discount factor.\
{sup}`2` 2% corresponds to 30 minutes of maximum net output (considering storage efficiency), i.e., C-rate of 2. 8% correspond to c-rate of 0.5. This attribute is assigned to commodity group “ACT”.\
{sup}`3` Maximum number of cycles over the full lifetime of storage process. Source: {cite}`52`

(sec-transmission-grid)=
## Transmission grid

Existing transmission capacities within Norway and to nearby European countries are given in {numref}`tab-existing-transmission-capacity-2022-mw` and {numref}`fig-net-transmission-capacities-between-regions`. In addition, the model allows for investments and expansion of both national and international transmission capacities between the regions. In {numref}`tab-investment-cost-new-transmission-capacity`, the assumed investment cost of new capacity is presented, where the investment cost varies due to the distance and technologies (cable vs. lines), based on project-specific data {cite}`53, p. 130`, {cite}`54`, {cite}`55`, {cite}`56`, {cite}`57`. New international transmission capacities to European countries are based on ENTSO-E’s Ten-year network development plan 2020 {cite}`58`, see {numref}`tab-upper-limit-new-transmission-capacity`. For trade cables between internal regions in Norway, we allow for a 20% increase in capacity. The estimate is uncertain and will be updated based on dialogue with the TSO. To compensate for the coarse representation of the power flow in IFE-TIMES-Norway, availability factors are included on the cables within Norway and to Europe. The factor limits the total flow on the line but is not specified for the direction of the flow. For international trade cables, the factor is based on input from the European power model, EMPIRE. For national trade cables, the factor is based on historical flow values. As new transmission cables typically take 10 years to construct and commission, it is assumed that no new investments will be available before 2035. Trade cables from offshore wind regions are described in Section {numref}`sec-offshore-wind-power`.

:::{list-table} Existing transmission capacity in 2022 (MW)
:name: tab-existing-transmission-capacity-2022-mw
:header-rows: 1
:widths: 16 16 16 16 16 16
:column-align: left center center center center center
:header-align: center

* -
  - NO1
  - NO2
  - NO3
  - NO4
  - NO5
* - NO1
  -
  - 3500
  - 500
  -
  - 3900
* - NO2
  - 3500
  -
  -
  -
  - 600
* - NO3
  - 500
  -
  -
  - 1200
  - 800
* - NO4
  -
  -
  - 1200
  -
  -
* - NO5
  - 3900
  - 600
  - 800
  -
  -
* - SE1
  -
  -
  -
  - 700
  -
* - SE2
  -
  -
  - 1000
  - 300
  -
* - SE3
  - 2145
  -
  -
  -
  -
* - DK1
  -
  - 1632
  -
  -
  -
* - RUS
  -
  -
  -
  - 56
  -
* - DE
  -
  - 1400
  -
  -
  -
* - NL
  -
  - 723
  -
  -
  -
* - UK
  -
  - 1400
  -
  -
  -
:::

:::{list-table} Investment cost for new transmission capacity (NOK/kW)
:name: tab-investment-cost-new-transmission-capacity
:header-rows: 1
:widths: 16 16 16 16 16 16
:column-align: left center center center center center
:header-align: center

* -
  - NO1
  - NO2
  - NO3
  - NO4
  - NO5
* - NO1
  -
  - 841
  - 2049
  -
  - 1216
* - NO2
  - 841
  -
  -
  -
  - 1265
* - NO3
  - 2049
  -
  -
  - 3807
  - 1195
* - NO4
  -
  -
  - 3807
  -
  -
* - NO5
  - 1216
  - 1265
  - 1195
  -
  -
* - SE3
  - 1264
  -
  -
  -
  -
* - DK1
  -
  - 5714
  -
  -
  -
* - DE
  -
  - 8750
  -
  -
  -
* - NL
  -
  - 8570
  -
  -
  -
* - UK
  -
  - 14285
  -
  -
  - 14285
:::

:::{list-table} Upper limit for new transmission capacity (MW)
:name: tab-upper-limit-new-transmission-capacity
:header-rows: 1
:widths: 16 16 16 16 16 16
:column-align: left center center center center center
:header-align: center

* -
  - NO1
  - NO2
  - NO3
  - NO4
  - NO5
* - NO1
  -
  - 700
  - 100
  -
  - 780
* - NO2
  - 700
  -
  -
  -
  - 120
* - NO3
  - 100
  -
  -
  - 240
  - 160
* - NO4
  -
  -
  - 240
  -
  -
* - NO5
  - 780
  - 120
  - 100
  -
  -
* - SE3
  - 1500
  -
  -
  -
  -
* - DK1
  -
  - 2000
  -
  -
  -
* - DE
  -
  - 2000
  -
  -
  -
* - NL
  -
  - 4000
  -
  -
  -
* - UK
  -
  - 2000
  -
  -
  - 1400
:::

:::{figure} images/figure-10.png
:name: fig-net-transmission-capacities-between-regions

Net transmission capacities between regions in 2022, MW {cite}`59`.
:::

(sec-electricity-trade)=
## Electricity trade

IFE-TIMES-Norway needs exogenous input of electricity prices for countries with transmission capacity to Norway. Electricity trade prices can be adjusted based on the premise and assumptions of a research project. By default, the electricity trade prices applied in the model are based on the average seasonal electricity prices from NVE’s “Langsiktig Kraftmarkedsanalyse 2025” {cite}`28`. The prices provided are on an hourly basis, and hence the price data inputs need to be aggregated to representative price profiles for each season considered in IFE-TIMES-Norway. The average prices for some selected countries are presented in {numref}`fig-electricity-prices-export-germany-across`. Notably, NVE prices are assumed to decrease towards 2050. {numref}`fig-electricity-prices-export-germany-across` shows an example of the prices for export to Germany for the assumed price set for 2030 and 2050, representing medium price levels. Further work is planned to create price profiles for Europe that are consistent with assumptions for the Norwegian energy system and with different price levels (e.g., high prices).

```{image} images/figure-11-part1.png
```

:::{figure} images/figure-11.png
:name: fig-electricity-prices-export-germany-across

Electricity prices for export to Germany across all seasons for 2030, 2040, and 2050.
:::
