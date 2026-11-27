(sec-buildings)=
# Buildings

(sec-structure-1)=
## Structure

The building sector of TIMES-Norway is divided in residential single-family (SFH) and multi-family houses (MFH) and in non-residential/commercial buildings (COM) for each of the model regions. All buildings are divided in existing and new buildings. The existing buildings have a stock of equipment in the start year and new buildings are those built after 2018. The end-use demand is divided in space heating (SH), domestic hot water (DHW) and specific electricity use (ElSpec; such as appliances, lighting, motors, fans etc.). Space heating is further divided in central heating (HC) and point source heating (H).

A schematic overview of the systems in residential and commercial buildings is presented in {numref}`fig-schematic-overview-end-use-sectors`, {numref}`fig-end-use-technologies-residential-sector` and {numref}`fig-schematic-overview-energy-system-commercial`. Here hot water is denoted “W” and electricity specific demand is denoted “E”. Oil boiler is only available before 2020. Demand for hot water is added to demand for space heating in buildings with central heating, while for buildings with point source heating it is modelled as a separate demand.

:::{figure} images/figure-26.png
:name: fig-schematic-overview-end-use-sectors

Schematic overview of the end-use sectors in residential sector (E=Electricity specific, H=point source heating, HC=Central heating, W=domestic hot water).
:::

:::{figure} images/figure-27.png
:name: fig-end-use-technologies-residential-sector

End-use technologies in residential sector.
:::

:::{figure} images/figure-28.png
:name: fig-schematic-overview-energy-system-commercial

Schematic overview of the energy system in commercial buildings.
:::

Heating is divided in central heating (water borne system) and “point source” heating based on data from the FlexBuild project {cite}`67`, {cite}`111`. The assumptions regarding the share of point source and central heating in the building sectors are presented in {numref}`tab-share-point-source-central-heating`.

:::{list-table} Share of point source and central heating in the building sectors.
:name: tab-share-point-source-central-heating
:header-rows: 1
:widths: 40 25 23
:column-align: left center center
:header-align: center

* -
  - Point sources
  - Central heating
* - Multi-family houses, existing
  - 62 %
  - 38 %
* - Multi-family houses, new
  - 12 %
  - 88 %
* - Single-family houses, existing
  - 88 %
  - 12 %
* - Single-family houses, new
  - 88 %
  - 12 %
* - Commercial buildings, existing
  - 37 %
  - 63 %
* - Commercial buildings, new
  - 10 %
  - 90 %
:::

District heating and ground source heat pumps are connected directly to heating demand in order to get the same profile as the demand (if a building has district heat it cannot have any other heating source when modelled as this). Biomass boilers are modelled on a seasonal level since they normally are more difficult to operate on an hourly level with rapid on/off.

(sec-demand-projection-1)=
## Demand projection

This section describes the energy service demand projections for the building sector, which is calculated using a excel building model, developed inhouse. A detailed description of the calculation is presented in {cite}`87`, in which also different demand projections can be developed by the model. In the following, a summary of this work is presented for the base demand projection.

The energy service demand of buildings is calculated as an area multiplied by end-use demand per $m^{2}$. The area is divided in existing unchanged buildings, existing buildings with energy upgrade renovation and new building area, which is also given for each of the three building subsectors SFH, MFH and COM. The area is new building area is based on population development and some additional parameters. Common for all calculations are assumptions of demolition rate and renovation rate with energy upgrading. For commercial buildings, it is assumed that the area per capita is constant. The area and energy service demand are calculated for 11 different types of commercial buildings, that is further aggregated to COM. The area calculation of dwellings also includes assumptions of share of MFH vs. SFH, area per dwelling, and persons per household. The most important assumptions are presented in {numref}`tab-key-statistics-assumptions-used-demand`. In addition to this, a low demand scenario in buildings is also available for use in the model, based on projections by Rosenberg et al. {cite}`87`, with slightly lower renovation rate assumptions towards 2035 (a renovation rate of 1.5% is assumed up to 2030 based on {cite}`112`), and default assumptions (2% renovation rate) towards 2060.

The energy service demand is divided by end-use and is an important premise for analyses of future energy demand. The input used for the present calculations are based on publications from NVE {cite}`113`, Statistics Norway {cite}`114` and building regulations of 2017 {cite}`115`. The energy by end-use for the types of dwellings used here are mainly based on {cite}`113`, {cite}`116`. For more information, see {cite}`87`.

:::{list-table} Key statistics and assumptions used in demand projection of buildings {cite}`87`.
:name: tab-key-statistics-assumptions-used-demand
:header-rows: 1
:widths: 38 12 15 15 17
:column-align: left center center center center
:header-align: center

* -
  - Common / Average
  - Single-family houses (SFH)
  - Multi-family houses (MFH)
  - Commercial buildings (COM)
* - Population (mill.)\
    2020\
    2030\
    2050\
    Annual growth
  - 5.368\
    5.661\
    6.034\
    0.39%
  -
  -
  -
* - Persons per household, 2018-2022\
    2020\
    2030\
    2050
  - 2.12\
    2.03\
    2.00
  -
  -
  - \-
* - Share of new dwellings (number of dwellings)
  -
  - 38%
  - 62%
  - \-
* - Area per new dwelling (m{sup}`2`/dwelling)\
    2018-2022\
    2030\
    2050
  - 126.3\
    127.3\
    127.3
  - 178.9\
    180\
    180
  - 94.1\
    95\
    95
  -
* - Renovation rate with energy upgrading (% per year)
  -
  - 0.2%
  - 0.2%
  - 0.3%
* - Demolition rate (% per year)
  -
  - 0.7%
  - 0.4%
  - 0.5%
* - Area (mill. m{sup}`2`)\
    2020\
    2030\
    2050
  -
  - 273\
    277\
    291
  - 49\
    58\
    69
  -
* - Energy demand by end-use, kWh/$\mathbf{m}^{\mathbf{2}}$
  -
  -
  -
  -
* - Existing, unchanged area, kWh/$\mathbf{m}^{\mathbf{2}}$\
    Space Heating (SH)\
    Domestic Hot Water (DHW) El.spec.\
    Total
  -
  - 107\
    28\
    23\
    158
  - 90\
    35\
    30\
    156
  - 125\
    15\
    177\
    317
* - Existing, renovated area, kWh/$\mathbf{m}^{\mathbf{2}}$\
    SH Space Heating (SH)\
    Domestic Hot Water (DHW)\
    El.spec.\
    Total
  -
  - 85\
    28\
    23\
    137
  - 72\
    35\
    30
  - 100\
    15\
    177\
    292
* - New area, kWh/$\mathbf{m}^{\mathbf{2}}$\
    SH Space Heating (SH)\
    Domestic Hot Water (DHW)\
    El.spec.\
    Total
  -
  - 51\
    29\
    29\
    109
  - 33\
    31\
    32\
    95
  - 45\
    11\
    93\
    149
:::

The energy service demand from 2010 to 2050 is based on the described assumptions presented in {numref}`tab-energy-service-demand-building-sector`. The energy service demand will be almost constant at 88 TWh. This is despite an increase in area of 14% in dwellings and of 12% in commercial buildings. For more information, see {cite}`87`.

:::{list-table} Energy service demand by building sector and end-use in 2020- 2050, TWh/year {cite}`87`.
:name: tab-energy-service-demand-building-sector
:header-rows: 1
:widths: 23 31 12 10 10 10
:column-align: left left center center center center
:header-align: center

* - Energy service demand
  -
  - 2020
  - 2030
  - 2040
  - 2050
* - Single-family (SFH)
  - Space heating (SH)
  - 30.8
  - 30
  - 29
  - 28.0
* -
  - Domestic Hot Water (DHW)
  - 8.1
  - 8
  - 8
  - 8.6
* -
  - Electricity specific
  - 6.7
  - 7
  - 7
  - 7.5
* -
  - Total
  - 45.7
  - 45
  - 45
  - 44.1
* -
  -
  -
  -
  -
  -
* - Multi-family (MFH)
  - Space heating (SH)
  - 4.6
  - 5
  - 5
  - 5.0
* -
  - Domestic Hot Water (DHW)
  - 1.8
  - 2
  - 2
  - 2.4
* -
  - Electricity specific
  - 1.5
  - 2
  - 2
  - 2.2
* -
  - Total
  - 8.0
  - 9
  - 9
  - 9.5
* -
  -
  -
  -
  -
  -
* - Commercial (COM)
  - Space heating (SH)
  - 13.8
  - 14
  - 13
  - 12.9
* -
  - Domestic Hot Water (DHW)
  - 1.7
  - 2
  - 2
  - 1.8
* -
  - Electricity specific
  - 19.5
  - 20
  - 20
  - 19.5
* -
  - Total
  - 35.0
  - 35
  - 35
  - 34.2
* -
  -
  -
  -
  -
  -
* - All
  - Space heating (SH)
  - 49.2
  - 48
  - 47
  - 46.0
* -
  - Domestic Hot Water (DHW)
  - 11.6
  - 12
  - 13
  - 12.8
* -
  - Electricity specific
  - 27.8
  - 28
  - 29
  - 29.1
* -
  - Total
  - 88.7
  - 88.7
  - 88.6
  - 87.9
:::

The energy service demand of dwellings in 2050 per region and end-use is presented in {numref}`fig-energy-service-demand-dwellings-2050`. The dominating region and dwelling type is SFH in NO1 and most energy use in multi-family houses is in NO1.

:::{figure} images/figure-29.png
:name: fig-energy-service-demand-dwellings-2050

Energy service demand in dwellings in 2050 per region and end-use, TWh/year. DHW = Domestic Hot Water, PS = Point Source heating, C-H = Central Heating, ElSpec = Appliances, lighting, cooling, new = new buildings (after 2020), ex = existing buildings (built before 2020)
:::

The energy service demand of dwellings in 2050 per region and end-use is presented in {numref}`fig-energy-service-demand-end-use`. The dominating region NO1 and the highest end-use demand is for electricity specific purposes (appliances, air conditioning, lighting etc.).

:::{figure} images/figure-30.png
:name: fig-energy-service-demand-end-use

Energy service demand by end-use and region of commercial buildings in 2050, TWh/year. DHW = Domestic Hot Water, PS = Point Source heating, C-H = Central Heating, ElSpec = Appliances, lighting, cooling, new = new buildings (after 2020), ex = existing buildings (built before 2020)
:::

Energy efficiency is included in the energy service demand projection as a fixed decrease of 20% of renovated existing buildings and as a part of the building code for new buildings. An alternative methodology is to keep the energy service demand of renovated buildings unchanged and instead add a possibility to invest in energy efficiency measures in IFE-TIMES-Norway. This will be considered in future developments.

(sec-load-profiles-1)=
## Load profiles

The load profiles, the sub-annual hourly load variations, are based on input from {cite}`105`, {cite}`106`. In the base model, we assume that the load profiles are the same for all years and for existing and new buildings. The heating profiles differs between regions and for central heating/ point source heating. The profile for non-substitutional electricity is the same for all residential buildings and all non-residential buildings. Examples of load profiles in region NO1 is presented in {numref}`fig-load-profile-residential-single-family`, {numref}`fig-load-profile-residential-multifamily-house` and {numref}`fig-load-profile-commercial-buildings-model`.

:::{figure} images/figure-31.png
:name: fig-load-profile-residential-single-family

Load profile for residential single-family house in model region NO1.
:::

:::{figure} images/figure-32.png
:name: fig-load-profile-residential-multifamily-house

Load profile for residential multifamily house in model region NO1.
:::

:::{figure} images/figure-33.png
:name: fig-load-profile-commercial-buildings-model

Load profile for commercial buildings in model region NO1.
:::

(sec-demand-technologies-1)=
## Demand technologies

(sec-heating-equipment)=
### Heating equipment

The investment and operational costs, annual full load hours, efficiencies, life times and technology learning rates are based on {cite}`64` and presented in {numref}`tab-technology-data-heating-equipment-buildings`. Equipment in the residential sector includes 25% VAT.

Existing oil boilers have 2 years lifetime, and it cannot be invested in new oil boilers, and oil boilers can consequently not be used from 2020. Stock of existing heating equipment is calculated based on energy use in 2018 and full load hours from {cite}`64`.

The efficiency and the availability of heat output of air-air heat pumps and air-water heat pumps depends on the outdoor temperature {cite}`117` and is therefore modelled on seasonal level for each of the five regions, see {numref}`fig-temperature-dependent-cop-heat-output`.

:::{list-table} Technology data of heating equipment in buildings.
:name: tab-technology-data-heating-equipment-buildings
:header-rows: 1
:widths: 24 10 10 7 10 10 10 12
:column-align: left center center center center center center center
:header-align: center

* - Description
  - Efficiency /COP
  - Market Share
  - LIFE
  - INVCOST
  - INVCOST 2035
  - FIXOM
  - VAROM
* -
  -
  -
  - years
  - NOK/ kW
  - NOK/kW
  - NOK/ kW
  - NOK/ MWh
* - {colspan}`8` Residential Multi-family
* - {colspan}`8` Central heating
* - Biomass boiler
  - 0.81
  -
  - 15
  - 8 850
  - 8 670
  - 1050
  - 10
* - Electric boiler
  - 0.98
  -
  - 20
  - 1 700
  - 1 700
  - 600
  - 1.5
* - Solar collector
  - 1.00
  - 0.10
  - 25
  - 6 400
  - 4 500
  - 60
  -
* - District heat exchanger
  - 0.99
  -
  - 50
  - 1 000
  - 1 000
  - \-
  - \-
* - Heat pump water-water
  - 3.0
  - 0.56
  - 20
  - 17 530
  - 14 020
  - 56
  - 21
* - Heat pump air-water
  -
  - 0.39
  - 15
  - 7 600
  - 6 100
  - 56
  - 21
* - {colspan}`8` Point sources
* - Direct electric heating
  - 1.00
  -
  - 25
  - 2 300
  - 2300
  - 34
  - 14
* - Electric water heater
  - 0.98
  -
  - 20
  - 2 700
  - 2700
  - 0
  -
* - {colspan}`8` Residential Single-family

    Central heating
* - Biomass boiler
  - 0.81
  -
  - 15
  - 14 400
  - 14 100
  - 1050
  - 10
* - Electric boiler
  - 0.98
  -
  - 20
  - 4 500
  - 4 500
  - 600
  - 1.5
* - Solar collector
  - 1.00
  - 0.10
  - 25
  - 12 000
  - 8 400
  - 60
  -
* - Heat pump water-water
  - 3.0
  - 0.28
  - 20
  - 26 000
  - 20 800
  - 56
  - 21
* - Heat pump air-water
  -
  - 0.36
  - 15
  - 20 100
  - 16 100
  - 56
  - 21
* - {colspan}`8` Point sources
* - Heat pump air-air
  -
  - 0.27
  - 15
  - 7 700
  - 6 200
  - 42
  -
* - Wood stove
  - 0.4
  - 0.5
  - 25
  - 3 400
  - 3 400
  - 50
  -
* - Direct electric heating
  - 1.00
  -
  - 25
  - 2 300
  - 2 300
  - 34
  - 14
* - Electric water heater
  - 0.98
  -
  - 20
  - 3 300
  - 3 300
  - 0
  -
* - {colspan}`8` Commercial
* - {colspan}`8` Central heating
* - Biomass boiler
  - 0.84
  -
  - 15
  - 8 850
  - 8 670
  - 583
  - 8
* - Electric boiler
  - 0.98
  -
  - 20
  - 1 700
  - 1 700
  - 36
  - 1.2
* - Solar collector
  - 1.00
  - 0.05
  - 25
  - 6 400
  - 4 500
  - 32
  -
* - District heat exchanger
  - 0.99
  -
  - 50
  - 1 000
  - 900
  - 0
  -
* - Heat pump water-water
  - 3.0
  - 0.3
  - 20
  - 17 530
  - 14 020
  - 45
  - 17
* - Heat pump air-water
  -
  - 0.4
  - 15
  - 7 600
  - 6 100
  - 45
  - 17
* - {colspan}`8` Point sources
* - Direct electric heating
  - 1.00
  -
  - 25
  - 1400
  - 1100
  - 21
  - 11
* - Electric water heater
  - 0.98
  -
  - 25
  - 2700
  - 2700
  - 67
  - 9
:::

:::{figure} images/figure-34.png
:name: fig-temperature-dependent-cop-heat-output

Temperature dependent COP and heat output of nominal capacity for air-water and air-air heat pumps.
:::

A maximum market share is added for heat pumps, as illustrated in {numref}`tab-market-share-heat-pumps`, and district heating as mentioned in chapter {numref}`sec-estimate-of-maximum-potential`. NVE has estimated coverage and prevalence for three types of heat pumps in three types of buildings and these estimations are provided in {numref}`tab-market-share-heat-pumps`.

:::{list-table} Market share of heat pumps.
:name: tab-market-share-heat-pumps
:header-rows: 1
:widths: 23 25 12 17 20
:column-align: left left center center center

* -
  - **Heat pump type**
  - **Air-to-air**
  - **Air-to-water**
  - **Water-to-water**
* - **Coverage**
  - Old buildings
  - 40 %
  - 65 %
  - 80 %
* -
  - New buildings
  - 50 %
  - 75 %
  - 90 %
* - **Prevalence**
  - Single-family houses
  - 90 %
  - 90 %
  - 21 %
* -
  - Multi-family houses
  - 0 %
  - 60 %
  - 70 %
* -
  - Commercial
  - 0 %
  - 80 %
  - 70 %
* - **Max market share**
  - Existing dwellings
  - 27 %
  - 54 %
  - 26 %
* -
  - New dwellings
  - 34 %
  - 62 %
  - 30 %
* -
  - Existing commercial
  - \-
  - 52 %
  - 56 %
* -
  - New commercial
  - \-
  - 60 %
  - 63 %
:::

Wood stoves can only be used in winter hours 16-24, fall and spring hours 18-22, in order to reflect actual use of wood firing, see {numref}`fig-illustration-available-share-capacity-wood`. The efficiency of wood stoves is lower than the theoretical values, to reflect that not all produced heat is useful (some is used for extra comfort, part of the time the temperature is above the needed comfort temperature etc.). It is assumed that wood stoves only can cover 50 % of heat demand, since it has to be operated manually and is a point source unable to heat all the rooms in the building.

:::{figure} images/figure-35.png
:name: fig-illustration-available-share-capacity-wood

Illustration of available share of capacity for wood stoves per season and time of day (hour).
:::

(sec-flexible-water-heaters)=
## Flexible water heaters

Flexible water heaters are included in the model as a Scenario file, which means that it needs to be activated in runs where such flexibility is desired (start year 2100 in base and 2022 in Scen_Flex-VVB).

The storage tanks are modelled with a flexible and a non-flexible share. The non-flexible part needs to deliver at least 70% of the total hot water demand, both for new and existing buildings. This is an uncertain share, based both on minimum demand of temperature level of the tank (due to avoiding legionella problems) and work done by {cite}`118`. This is modelled as a normal electric water heater, with low-voltage electricity as input and hot water as output commodity. The investment cost corresponds to the average cost of several existing hot water tanks in the market. The flexible part of the storage tank can deliver up to 30% of the demand and is modelled using the same approach as for battery and thermal storage (see eq. 1 and eq. 5)). The relationship between power output and energy content, the c-rate, is set to 0.28, also defined by existing storage tanks. The additional cost of installing a flexible hot water tank compared to a conventional one is around 3000-5000 NOK {cite}`119`. As model input, an average cost of 4000 NOK is assumed for an average capacity of 13 kWh. Information regarding technical parameters and investment costs for the conventional hot water tank and the flexible part is presented in {numref}`tab-parameters-costs-non-flexible-flexible`. In IFE-TIMES-Norway, flexible hot water tanks can only be installed in new tanks, meaning that existing water heaters cannot be retrofitted to be flexible.

:::{list-table} Parameters and costs for non-flexible and flexible part of hot-water tank (without VAT).
:name: tab-parameters-costs-non-flexible-flexible
:header-rows: 1
:widths: 32 20 13 10 9 13
:column-align: center center center center center center
:header-align: center

* -
  - Investment cost
  - Efficiency
  - Storage loss
  - c-rate
  - Share of demand
* - Hot water tank – non-flexible
  - 2 371 kNOK/MW
  - 98%
  -
  -
  - 70% (min)
* - Hot water tank – flexible
  - 244 NOK/kWh
  - 98%
  - 3.3%
  - 0.28
  - 30% (max)
:::

(sec-energy-efficiency)=
## Energy efficiency

In the base model of IFE-TIMES-Norway, energy efficiency is included in the demand projection by assuming an annual renovation rate of 0.2% in households and of 0.3% in commercial buildings and a reduction in energy use by 20% when renovation, as described in {cite}`87`.

Another possibility is to analyse energy efficiency measures as individual technology options. This is done by modelling energy efficiency measures as technology options in two sets of SubRES files. One set contains all details, based on information from a study by NVE and Multiconsult {cite}`120`. The detailed description of energy efficiency measures includes 460 measures in households and 3335 measures in commercial buildings, which is heavy to work with. A simplified set of energy efficiency measures is thus modelled as well. In this set, some measures are deleted (Energy monitoring system (EOS), energy management system (SD), Energy efficient lighting, energy savings by lighting control, Reduced indoor temperature at nights and weekends) and in commercial buildings are some of the measures aggregated to two building standards instead of 3 or 4. The commercial buildings are also aggregated to one type of building instead of 11 types. In total, this reduces the number of measures to 320 in households and 75 in commercial buildings. The energy efficiency potential is reduced from 16 TWh to 14 TWh in 2025 in commercial buildings (-13%) and from 20 TWh to 17 TWh in 2025 in households (-15%), when using the simplified measures compared to the detailed measures. An overview of the included measures and the belonging energy saving potential is presented in {numref}`tab-overview-energy-saving-potential-energy`.

It is assumed that the measures are implemented in the order of lowest LCOE in both sets of energy efficiency measures, see description in {cite}`120`. The full potential can be implemented from 2030 with a linear increase from zero in 2025.

When using these SubRES files, the demand projection cannot include the basic assumptions of annual energy renovation rates with associated energy reductions. Thus, the file Scen_EnEff-SubRES must be used in combination with the SubRES files, in order not to include energy saving possibilities twice. In this scenario file, a hurdle rate for energy efficiency measures is added, but can easily be changed or inactivated in different analyses. Use of 20% hurdle rate is in accordance with results from Behaviour analyses in December 2023. If this rate is used, the implementation of energy efficiency measures is reduced to 13.4 TWh in 2030 (with simplified measures) and to 17.6 TWh with detailed measures (-24%) compared to the total potential of 31 TWh (all simplified measures) and 36 TWh (all detailed measures).

:::{list-table} Overview and energy saving potential of energy efficiency measures in IFE-TIMES-Norway (Det = Detailed measures, Sim = Simplified measures)
:name: tab-overview-energy-saving-potential-energy
:header-rows: 1
:widths: 7 9 23 7 6 6 6 7 6 6 6 6
:column-align: center center center center center center center center center center center center
:header-align: center

* - **Type**
  - {colspan}`2` **Measure**
  - {colspan}`7` **Number of**
  - {colspan}`2` **Potential\
    (TWh/year)**
* -
  - **Name**
  - **Description**
  - {colspan}`2` **Measures**
  - {colspan}`2` **TEK**
  - **Heat. syst.**
  - {colspan}`2` **Sub-sectors**
  - {colspan}`2` **2030**
* -
  -
  -
  - **Det**
  - **Sim**
  - **Det**
  - **Sim**
  -
  - **Det**
  - **Sim**
  - **Det**
  - **Sim**
* - SFH
  - CSV01
  - Insulation wall
  - 30
  - 30
  - 3
  - 3
  - 2
  -
  -
  - 6.1
  - 6.1
* -
  - CSV02
  - Insulation roof
  - 30
  - 30
  - 3
  - 3
  - 2
  -
  -
  - 2.5
  - 2.5
* -
  - CSV03
  - Insulation floor
  - 30
  - 30
  - 3
  - 3
  - 2
  -
  -
  - 1.1
  - 1.1
* -
  - CSV04
  - New windows and doors
  - 30
  - 30
  - 3
  - 3
  - 2
  -
  -
  - 3.4
  - 3.4
* -
  - CSV05
  - Night & weekend reduction of heating
  - 30
  - 0
  - 4
  - \-
  - 2
  -
  -
  - 1.2
  - \-
* -
  - CSV06
  - Better heat recovery ventilation
  - 40
  - 40
  - 4
  - 4
  - 2
  -
  -
  - 1.1
  - 1.1
* -
  - CSV07
  - EOS
  - 20
  - 0
  - 4
  - \-
  -
  -
  -
  - 0.7
  - \-
* -
  - CSV08
  - Energy efficient lighting
  - 20
  - 0
  - \-
  - \-
  -
  -
  -
  - 0.8
  - \-
* - MFH
  - CSV01
  - Insulation wall
  - 30
  - 30
  - 3
  - 3
  - 2
  -
  -
  - 1.0
  - 1.0
* -
  - CSV02
  - Insulation roof
  - 30
  - 30
  - 3
  - 3
  - 2
  -
  -
  - 0.2
  - 0.2
* -
  - CSV03
  - Insulation floor
  - 30
  - 30
  - 3
  - 3
  - 2
  -
  -
  - 0.1
  - 0.1
* -
  - CSV04
  - New windows and doors
  - 30
  - 30
  - 3
  - 3
  - 2
  -
  -
  - 0.3
  - 0.3
* -
  - CSV05
  - Night & weekend reduction of heating
  - 30
  - 0
  - 4
  - \-
  - 2
  -
  -
  - 0.1
  - \-
* -
  - CSV06
  - Better heat recovery ventilation
  - 40
  - 40
  - 4
  - 4
  - 2
  -
  -
  - 0.7
  - 0.7
* -
  - CSV07
  - EOS
  - 20
  - 0
  - 4
  - \-
  -
  -
  -
  - 0.1
  - \-
* -
  - CSV08
  - Energy efficient lighting
  - 20
  - 0
  - \-
  - \-
  -
  -
  -
  - 0.2
  - \-
* - COM
  - CSV01
  - Insulation wall
  - 330
  -
  - 3
  - 1
  - 2
  - 11
  - 1
  - 1.4
  - 1.4
* -
  - CSV02
  - Insulation roof
  - 330
  -
  - 3
  - 1
  - 2
  - 11
  - 1
  - 1.2
  - 1.2
* -
  - CSV03
  - Insulation floor
  - 330
  -
  - 3
  - 1
  - 2
  - 11
  - 1
  - 0.7
  - 0.7
* -
  - CSV04
  - New windows and doors
  - 330
  -
  - 3
  - 1
  - 2
  - 11
  - 1
  - 1.2
  - 1.2
* -
  - CSV05
  - Night & weekend reduction of heating
  - 330
  -
  - 3
  - \-
  - 2
  - 11
  - 1
  - 0.7
  - \-
* -
  - CSV06
  - Better heat recovery ventilation
  - 440
  -
  - 4
  - 2
  - 2
  - 11
  - 1
  - 4.0
  - 4.0
* -
  - CSV07
  - EOS
  - 220
  -
  - 4
  - \-
  -
  - 11
  - 1
  - 0.3
  - \-
* -
  - CSV08
  - Energy efficient lighting
  - 220
  -
  - 4
  - \-
  -
  - 11
  - 1
  - 1.2
  - \-
* -
  - CSV09
  - System for lighting control
  - 200
  -
  - 4
  - \-
  -
  - 10
  - 1
  - 0.6
  - \-
* -
  - CSV10
  - Better specific fan power (SFP)
  - 220
  -
  - 4
  - 1
  -
  - 11
  - 1
  - 1.9
  - 1.9
* -
  - CSV12
  - Demand controlled ventilation (DCV)
  - 220
  -
  - 4
  - 2
  -
  - 11
  - 1
  - 3.0
  - 3.0
* -
  - CSV13
  -
  - 165
  -
  - 3
  - \-
  -
  - 11
  - 1
  - 0.2
  - \-
* -
  -
  -
  -
  -
  -
  -
  -
  -
  -
  -
  -
* -
  -
  -
  -
  -
  -
  -
  -
  -
  -
  -
  -
* -
  - RESS
  - Sum
  - 210
  - 160
  -
  -
  -
  -
  -
  - 17.0
  - 14.2
* -
  - RESM
  - Sum
  - 210
  - 160
  -
  -
  -
  -
  -
  - 2.6
  - 2.3
* -
  - COM
  - Sum
  - 3335
  - 75
  -
  -
  -
  -
  -
  - 16.3
  - 13.5
* -
  - Total
  - Sum
  - 3755
  - 395
  -
  -
  -
  -
  -
  - 36.0
  - 30.0
:::
