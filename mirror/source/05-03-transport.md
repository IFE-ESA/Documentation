(sec-transport)=
# Transport

(sec-structure-2)=
## Structure

Road transport is divided into six categories, which are listed and briefly described in

{numref}`tab-description-transport-demand-types`. The energy-service demand for all road transport categories is expressed in “million vehicle km/year”.

{numref}`tab-description-transport-demand-types` also presents the non-road transport categories, including rail, maritime, and air transport. Transport activities not covered by these categories are grouped under Other transport. Unlike road transport, the energy-service demand for non-road transport is expressed in GWh/year.

:::{list-table} Description of the different transport demand types.
:name: tab-description-transport-demand-types
:header-rows: 1
:widths: 18 12 68
:column-align: center center left
:header-align: center

* - Type
  - Name in TIMES
  - Description
* - Cars
  - TCAR
  - Vehicles transporting up to 9 persons including driver. Taxis and ambulances are also included in this group.
* - Vans
  - TVAN
  - Vehicles designed for carriage of goods with gross vehicle weight below 3.5 tons. Corresponds to Norwegian Public Roads Administration's vehicle group N1. In addition, motorhomes and combined cars (an outdated government definition of vehicles designed for both person and goods transport) are included.
* - {rowspan}`3` Trucks
  - TTRUCK-S
  - Trucks with registered total gross weight including trailer between 3.5 and 50 tons, all distances (S as in Small).
* - TTRUCK-LS
  - Trucks with registered total gross weight including trailer above 50 tons and for short haulage (< 300km) (LS as in Large and Short)
* - TTRUCK-LL
  - Trucks with registered total gross weight including trailer above 50 tons and for long haulage (> 300km) (LL as in Large and Long).
* - Bus
  - TBUS
  - Vehicles transporting 10 persons or more.
* - Rail
  - TRAIL
  - Railway transport.
* - Aviation
  - TAIR
  - Aircraft used for domestic aviation
* - Passenger ships
  - TSEA1
  - Passenger ships, including ferries.
* - Fishing ships
  - TSEA2
  - Fishing ships.
* - Other maritime vessels
  - TSEA3
  - Maritime freight, supply, and other coastal vessels. These are further subdivided into 5 vessel segments, namely, Containers, Bulk carriers, Cargo ships, Tankers and Other. In TIMES, these are respectively named as CONT, BULK, CARGO, TANK, and OTH.
* - Other transport
  - TOTH
  - Other transport vehicles used in public services, commerce, and defence.
:::

Heavy-duty truck demand is divided into three segments because vehicle size and daily mileage are important determinants of energy consumption and the feasibility of alternative propulsion systems. If electrified, the three segments may also have different requirements for fast-charging infrastructure.

{numref}`tab-distribution-trucks-daily-mileage-vehicles` presents the classification of the segments according to daily mileage {cite}`121`. The colour coding used follows the mileage distribution: yellow and orange represent short-distance trucks (TTRUCK-S), red represents long-distance trucks (TTRUCK-LS), and purple represents long-haul trucks and tractor units (TTRUCK-LL).

Engines with a rated power above 500 hp are typically used in tractor units with semi-trailers and in trucks performing particularly demanding operations. Examples include road trains with a maximum length of 24 m and a maximum gross vehicle weight of 60 tonnes, vehicles transporting materials to and from construction sites, and other special-purpose vehicles.

:::{list-table} Distribution of trucks' daily mileage for vehicles 5 years old and newer {cite}`121`.
:name: tab-distribution-trucks-daily-mileage-vehicles
:header-rows: 1
:widths: 12 11 11 11 9 9 11 12
:column-align: center center center center center center center center
:header-align: center

* - Engine power (HP)
  - Up to 100 km
  - 100-200 km
  - 200-300 km
  - 300-400 km
  - 400-500 km
  - 500 km and over
  - Total
* - 100-199
  - 0.1%
  - 0.1%
  - 0.0%
  - 0.0%
  - 0.0%
  - 0.0%
  - 0.2%
* - 200-299
  - 2.5%
  - 2.2%
  - 1.1%
  - 0.6%
  - 0.2%
  - 0.2%
  - 6.8%
* - 300-399
  - 2.8%
  - 2.8%
  - 1.1%
  - 0.7%
  - 0.2%
  - 0.2%
  - 7.8%
* - 400-499
  - 4.7%
  - 4.4%
  - 2.9%
  - 1.0%
  - 0.6%
  - 2.2%
  - 15.8%
* - 500-599
  - 12.4%
  - 8.3%
  - 6.6%
  - 4.1%
  - 5.3%
  - 17.6%
  - 54.3%
* - 600-699
  - 2.1%
  - 1.1%
  - 0.9%
  - 0.6%
  - 0.8%
  - 2.7%
  - 8.2%
* - 700+
  - 2.0%
  - 0.9%
  - 0.7%
  - 0.5%
  - 0.7%
  - 2.4%
  - 7.2%
* - Total
  - 26.6%
  - 19.8%
  - 13.2%
  - 7.5%
  - 7.6%
  - 25.3%
  - 100.0%
:::

*Yellow-orange for TTRUCK-S, red for TTRUCK-LS, and purple for TTRUCK-LL*

The transport demand overview, its forecast, and fleet composition for Norway are prepared by the Norwegian Institute of Transport Economics (TØI) using their Freight Transport model (GTM, based on its Norwegian Acronym) and their stock-flow cohort model of the Norwegian vehicle fleet (BIG, based on its Norwegian Acronym).

The transport categories in IFE-TIMES-Norway are designed to facilitate the transfer of data from TØI’s projections, particularly from the BIG model. This model provides a detailed breakdown of the heavy-duty vehicle fleet by vehicle type (distinguishing between trucks and tractor units) and by vehicle size. In BIG, vehicle-size categories are defined according to registered gross vehicle weight, including trailers. {numref}`tab-million-vehicle-km-distribution-across` presents the distribution of the heavy-duty vehicle fleet across these categories in 2018 {cite}`122`.

:::{list-table} Million vehicle-km distribution across vehicle registered total gross weight for different vehicle types for year 2018 based on data from BIG {cite}`122`.
:name: tab-million-vehicle-km-distribution-across
:header-rows: 1
:widths: 30 10 10 10 10
:column-align: center center center center center
:header-align: center

* - Registered total gross weight including trailer
  - Trucks
  - Tractor units
  - Total
  - Share of total
* - 3.5-7.5 ton
  - 38
  - 0
  - 38
  - 2%
* - 7.5-12 ton
  - 97
  - 0
  - 97
  - 4%
* - 12-20 ton
  - 130
  - 2
  - 132
  - 6%
* - 20-30 ton
  - 105
  - 13
  - 118
  - 5%
* - 30-40 ton
  - 49
  - 10
  - 59
  - 3%
* - 40-50 ton
  - 113
  - 14
  - 127
  - 5%
* - 50-60 ton
  - 147
  - 41
  - 188
  - 8%
* - 60 + ton
  - 1066
  - 478
  - 1544
  - 67%
* - Sum
  - 1743
  - 558
  - 2302
  - 100%
:::

In IFE-TIMES-Norway, vehicles with a registered gross weight above 50 tonnes, including trailers, are assumed to correspond to vehicles with engine ratings above 500 hp. Although this mapping is not exact, it provides a transparent and practical link between the vehicle categories in IFE-TIMES-Norway and the BIG model. The total vehicle-km travelled by vehicles above the 50-tonne threshold is divided equally between the short-distance and long-haul segments. Projections from TØI indicate a shift in the fleet composition towards fewer small trucks and a larger share of heavy trucks, as illustrated in {numref}`fig-development-demand-three-types-trucks`.

:::{figure} images/figure-36.png
:name: fig-development-demand-three-types-trucks

Development in demand for three types of trucks, 2018, 2030, and 2050 (bill. vehicle-km / year).
:::

The demand for sea transport is divided into three groups: Group 1 corresponds to passenger ships, Group 2 to fishing vessels, and Group 3 to freight, service, and other vessels. The demands for these groups are split based on emission estimates for different ship types presented in DNV-GL’s 2021 report {cite}`123`. The shares of emissions from the different ship types are used in conjunction with energy demand data reported by Statistics Norway, SSB Table 11561 {cite}`61`. Namely, the emission shares corresponding to Groups 1 and 3 are used to split up the fuel consumption values corresponding to domestic navigation (12.2.4 Domestic Navigation in Table 11561 in SSB) from the Statistics, while the energy demands for fishing ships correspond to the values reported in the statistics (Fishing 12.3.2 in Table 11561 in SSB). In SSB, the energy demand from the fishing industry also includes electricity consumption; however, this is excluded from the transport sector of the model and assigned to fishing farms or other onshore infrastructure (AGR in Industry).

:::{list-table} Comparison of CO{sub}`2` emissions from the maritime sector based on bunkering and Automatic Identification System (AIS) data (compensated for fishing vessels without AIS equipment with 240 kton). Also shown is how the different ship types are aggregated in IFE-TIMES-Norway.
:name: tab-comparison-co2-emissions-maritime-sector
:header-rows: 1
:widths: 26 11 14 12 14
:column-align: left center center center center
:header-align: center

* -
  - Grouping
  - DNV GL, 2020\
    (kton CO{sub}`2`)
  - Share of emissions, from total
  - Share of emissions, excl. fishing
* - Passenger ships
  - {rowspan}`2` 1
  - 338
  - 8%
  - 11%
* - High-speed ferries
  - 465
  - 11%
  - 15%
* - Fishing vessels
  - 2
  - 891
  - 22%
  -
* - Offshore vessels
  - {rowspan}`5` 3
  - 1018
  - 25%
  - 32%
* - Other special use vessels
  - 265
  - 6%
  - 8%
* - Aquaculture
  - 194
  - 5%
  - 6%
* - Freight ships
  - 499
  - 12%
  - 16%
* - Wet & dry bulk
  - 413
  - 10%
  - 13%
:::

Further disaggregation is provided in the different vessel segments under Group 3 based on estimates from Energikart {cite}`124`. Five ship categories are defined corresponding to Containers, Bulk, Cargo, Tanker, and Other ships (aggregating passenger and offshore supply, coastal sideport, and special use vessels). The transport demands from Group 3 are divided based on the corresponding shares of energy consumption estimated from the Energikart data, as present in {numref}`tab-estimated-shares-energy-consumption-vessel`.

:::{list-table} Estimated shares of energy consumption by vessel segment in group 3, based on estimates from Energikart {cite}`124`.
:name: tab-estimated-shares-energy-consumption-vessel
:header-rows: 1
:widths: 28 28 17
:column-align: center center center
:header-align: center

* - Vessel segments, group 3
  - Name in TIMES
  - Shares
* - Container
  - TSEA3-CONT
  - 1.05%
* - Bulk
  - TSEA3-BULK
  - 16.80%
* - Cargo
  - TSEA3-CARGO
  - 2.97%
* - Tanker
  - TSEA3-TANK
  - 69.84%
* - Other
  - TSEA3-OTH
  - 9.34%
:::

(sec-demand)=
## Demand

The demand towards 2050 is based upon the projections made in the national transport plan (NTP) 2025-2036 {cite}`125`, {cite}`126`, {cite}`127`and is shown in {numref}`fig-relative-change-demand-default-scenario`. These projections present estimates for 2020 as the base year, with projected estimates for 2030 and 2060.

Road transport in the model was calibrated using 2025 data on road traffic volumes {cite}`128` and energy carrier consumption in {cite}`129`. Non-road transport demands are still calibrated with 2020 Statistics and will be updated next.

Annual growth rates from the NTP were used to estimate demands from 2030 to 2050. Since data for light freight and vans is not provided in the new projections, data from the BIG model {cite}`130` is used to estimate the shares and demand values for this segment’s transport demands.

The total heavy freight transport is based on data from NTP 2025-2036 and is divided into the three truck classes of IFE-TIMES-Norway as described in the previous section. The division of data per region and the relative development from 2020 to 2050 is based on county data of NTP 2025-2036 {cite}`127`.

:::{figure} images/figure-37.png
:name: fig-relative-change-demand-default-scenario

The relative change in demand for the default scenario (NTP) in 2020, 2030, and 2050.
:::

Energy use of domestic air transport in the base year is divided into the five NO regions based on population in 2020. Development in passenger-km in NTP 2025-2036 {cite}`126` is then used to estimate the demand projection of air transport to 2050.

The projection of passenger sea transport is likewise based on the development of passenger-km in NTP 2025-2036 {cite}`126`. For the two other sea transport categories, the total development of freight transport by sea is used {cite}`125`.

The projection of rail transport is 50% based on the development of passenger transport and 50% on freight transport. The remaining category is assumed to develop according to the increase in population of Statistics Norway 2020 (MMMM alternative). The demand projection of non-road transport is presented in {numref}`fig-energy-demand-non-road-transport`.

:::{figure} images/figure-38.png
:name: fig-energy-demand-non-road-transport

Energy demand of non-road transport in 2020, 2030, and 2050, TWh/year.
:::

(sec-road-transport-technologies)=
## Road Transport Technologies

(sec-available-powertrains)=
### Available powertrains

In IFE-TIMES-Norway, various technologies or powertrains can be used to satisfy transport demand. The road transport powertrains considered in the model include internal combustion engine (ICE), plug-in hybrid with ICE, battery electric, fuel cell electric, and gas-powered ICE. A more detailed description of each powertrain is presented in {numref}`tab-description-powertrains-how-they-defined`.

:::{list-table} Description of powertrains, how they are defined in IFE-TIMES-Norway, and input commodities.
:name: tab-description-powertrains-how-they-defined
:header-rows: 1
:widths: 16 52 14 15

* - Power trains
  - Description of powertrain
  - Powertrain definition in TIMES
  - Commodity used
* - ICE
  - Within this category is aggregated ICE using petrol and diesel. In addition, hybrid vehicles, which are not plug-in are included here. They can use fossil fuel, biofuel,, or a mix
  - XXX-ICE
  - FOS

    BIO-FUEL
* - Plug-in hybrid
  - In similarity with ICE powertrain, both petrol and diesel engines are considered. In addition, a share of energy can be supplied by electricity.
  - XXX-PLUG
  - FOS

    BIO-FUEL

    ELC-LV
* - Battery
  - Battery electric vehicles are modelled to be charged by electricity provided from charging infrastructure
  - XXX-ELC
  - ELC-CAR
* - Fuel cell
  - Fuel cell and battery hybrid system entirely powered by hydrogen. Hydrogen production and handling are modelled separately in IFE-TIMES-Norway.
  - XXX-H2
  - H2
* - Gas-powered ICE
  - Based on liquid or compressed biogas used in ICE for urban buses.
  - XXX-GAS
  - GAS
:::

Each powertrain can use one or more energy commodities as inputs. For selected commodities, minimum or maximum shares are imposed to reflect blending requirements, technical limitations, or policy assumptions. {numref}`tab-share-commodities-certain-powertrains` provides an overview of these constraints.

Biofuels accounted for approximately 14% of the road-transport fuel demand in 2025 {cite}`128`. In IFE-TIMES-Norway, this volumetric share is simplified and represented as an equivalent share of road-transport energy demand covered by biofuels. Norwegian regulations require a minimum biofuel share of 19%, including a sub-requirement of 12.5% advanced biofuels {cite}`131`. Because advanced biofuels may be double-counted towards the regulatory obligation, the physical share of liquid biofuels required to meet the mandate is estimated to be approximately 16–19% {cite}`132`.

In the model, the biofuel share in road transport is fixed at 14% in 2025 to reflect the observed data. From 2030, a minimum share of 19% and a maximum share of 50% are applied. The maximum share is subsequently allowed to increase to 100% by 2050, while the minimum share remains at 19%. The lower bound therefore represents a continuation of the assumed biofuel mandate, whereas the upper bound allows the model to increase biofuel use when it is economically competitive.

The share of electricity used by plug-in hybrid vehicles depends on several factors, including driving patterns, charging availability, battery capacity, and user behaviour, and is therefore difficult to estimate. IFE-TIMES-Norway assumes that electricity supplies 30% of the energy used by plug-in hybrid vehicles, based on measured data from [www.spritmonitor.de](http://www.spritmonitor.de) {cite}`133`. This share is assumed to remain constant throughout the model horizon to 2050.

:::{list-table} Share of commodities for certain powertrains.
:name: tab-share-commodities-certain-powertrains
:header-rows: 1
:widths: 38 8 10 10 10 10
:column-align: left center center center center center
:header-align: center

* -
  -
  - 2018
  - 2025
  - 2030
  - 2050
* - {rowspan}`2` BIO-FUEL input for ICE
  - Max
  - 14%
  - 14%
  - 50%
  - 100%
* - Min
  - 14%
  - 14%
  - 19%
  - 19%
* - Electricity input in plug-in hybrid
  - Max
  - 30%
  - 30%
  - 30%
  - 30%
:::

Given the specific characteristics of the Norwegian transport sector and the current state of technological development, not all powertrains are considered suitable for every road-transport segment. {numref}`fig-matrix-powertrains-applied-road-transport` presents the powertrain options available for each road-transport demand category.

Battery-electric powertrains are defined in the model for large trucks used in long-haul transport. However, this option is generally not enabled in the reference scenarios because its technical feasibility remains uncertain under the assumed operating requirements. It can nevertheless be activated in alternative scenarios to assess the potential effects of future technological development.

:::{list-table}
:header-rows: 1
:widths: 29 10 16 12 11 19
:column-align: left center center center center center
:header-align: center

* -
  - ICE
  - Plug-in hybrid
  - Battery
  - Fuel cell
  - Gas-powered ICE
* - Car
  -
  -
  -
  -
  -
* - Van
  -
  -
  -
  -
  -
* - Small truck
  -
  -
  -
  -
  -
* - Large truck, short haulage
  -
  -
  -
  -
  -
* - Large truck, long haulage
  -
  -
  -
  -
  -
* - Bus
  -
  -
  -
  -
  -
:::

:::{figure} images/figure-39.png
:name: fig-matrix-powertrains-applied-road-transport

Matrix of powertrains applied for the different road transport demand. (Green: included; Blank: not considered; Beige: optional)
:::

The deployment of selected van and bus technologies is constrained in certain model scenarios to represent a more realistic development of the vehicle fleet. The applied constraints are presented in {numref}`tab-upper-market-share-limitations-vans`.

Battery-electric vehicles have high drivetrain efficiencies and relatively low energy and maintenance costs. However, limited driving range remains a constraint for some heavy-duty applications and may restrict their initial penetration in these segments. Based on the technical performance demonstrated in Norwegian pilot projects, the initial market share of battery-electric heavy-duty vehicles is limited to approximately 1% {cite}`121`. This limit is subsequently relaxed over time to represent the expected development of battery and charging technologies.

Hydrogen fuel-cell powertrains are assumed to become available for investment from 2030. The assumed development in the market shares of different truck powertrains is presented in {numref}`tab-upper-market-share-limitations-vans`.

:::{list-table} Upper market share limitations on vans and buses.
:name: tab-upper-market-share-limitations-vans
:header-rows: 2
:widths: 50 9 1 9 11 9
:column-align: center center center left center center
:header-align: center

* - {rowspan}`2` Technology
  - {colspan}`2`
  - {colspan}`3` Market share
* -
  - {colspan}`2`
  - **2030**
  - **2040**
* - Battery electric vans
  -
  - {colspan}`2`
  - 100%
  - 100%
* - Biogas buses
  -
  - {colspan}`2`
  - 50%
  - 100%
* - Battery electric Small truck
  -
  - {colspan}`2`
  - 100%
  - 100%
* - Battery electric Large truck, short haulage
  -
  - {colspan}`2`
  - 100%
  - 100%
* - Battery electric Large truck, long haulage
  -
  - {colspan}`2`
  - 0%
  - 0%
:::

(sec-existing-stock)=
### Existing stock

The existing fleet of road vehicles is modelled to follow 2025 data on road traffic volumes {cite}`128` and fuel consumption {cite}`129`, which linearly decreases to zero during a time span equivalent to the vehicle’s lifetime.

The regional distribution of transport demand is assumed to remain constant throughout the model horizon, based on the distribution presented in {numref}`tab-distribution-transport-demand-existing-stock`. The table also shows the regional distribution of the existing stock of battery-electric vehicles. Compared with the overall vehicle fleet, battery-electric vehicles have a higher concentration in southern Norway.

:::{list-table} Distribution of transport demand and existing stock of battery vehicles over regions.
:name: tab-distribution-transport-demand-existing-stock
:header-rows: 1
:widths: 12 29 33
:column-align: left center center
:header-align: center

* -
  - Transport demand
  - Battery vehicle distribution
* - NO1
  - 39%
  - 42%
* - NO2
  - 23%
  - 22%
* - NO3
  - 14%
  - 13%
* - NO4
  - 9%
  - 5%
* - NO5
  - 16%
  - 17%
* - Total
  - 100%
  - 100%
:::

(sec-input-values)=
### Input values

Where possible, technology data are obtained from *Klimakur 2030* {cite}`20`. This source provides a common methodological basis for assessing greenhouse-gas mitigation measures in Norway and supports a consistent set of input assumptions across the transport segments represented in IFE-TIMES-Norway.

However, *Klimakur 2030* primarily provides data for ICE and battery-electric powertrains. Data for other powertrains must therefore be supplemented with information from additional sources. When combining data from different sources, emphasis is placed on maintaining consistent relative differences among powertrains rather than directly applying absolute values that may have been developed using different assumptions. Complementary technology parameters are therefore generally estimated relative to the corresponding ICE powertrain.

Truck investment costs are an exception to this approach. For trucks, cost assumptions are based directly on data provided by the Institute of Transport Economics (TØI).

(sec-fuel-consumption)=
### Fuel consumption

This section describes the stock and new processes/powertrains available to the different road transport segments. Fuel-consumption data in 2025 {cite}`114`, along with 2025 passenger volumes {cite}`128`, were used to calibrate the performance efficiencies of the different powertrains.

***Passenger cars (TCAR)***

The statistics of cars sold during 2017 and 2018 show an approximately even split between small and compact cars and medium, large, and luxury cars {cite}`134`. The energy consumption for TCAR-ICE and TCAR-ELC in 2025 is based on the average value for a small and a large representative car in *Klimakur* 2030 – teknisk notat {cite}`20` and adjusted so that the road traffic volumes and fuel consumption data from SSB match {cite}`128`, {cite}`129`.

The chosen representative cars are the VW Golf for a small car and the VW Tiguan for a large car. Golf is available both with ICE and battery, while the Tiguan is available only with ICE. The study, however, decomposes each car and sets an imaginary battery propulsion for the VW Tiguan. The weakness of *Klimakur* 2030 report is that it does not include other relevant powertrains such as plug-in hybrid and hydrogen cars. To have a complete and consistent dataset, relative relationships between different powertrains and years are taken from an extensive analysis of drivetrains made in the modelling program Autonomie by Argonne National Laboratory {cite}`135`.

When applying trends from {cite}`135`, the fuel consumption relationship between powertrains and development over time is based on a midsize car, at low technology development and at high cost prediction. In addition, the energy consumption is based on the average value from the two driving cycles used in the simulation: Urban Dynamometer Driving Schedule and Highway Federal Emissions Test. The energy demand for fuel cell vehicles is interpreted to be very optimistic; thus, the fuel consumption of fuel cell cars in the start year and in the future is instead taken from the Danish Technological Institute {cite}`133`. An overview of the values used is shown in {numref}`tab-energy-consumption-passenger-cars-tcar`.

:::{list-table} Energy consumption for passenger cars (TCAR).
:name: tab-energy-consumption-passenger-cars-tcar
:header-rows: 2
:widths: 17 11 28 12 30
:column-align: center center center center center
:header-align: center

* - {rowspan}`2` Name in TIMES
  - {colspan}`2` Start year
  - {colspan}`2` 2050
* - **kWh/km**
  - **Source**
  - **kWh/km**
  - **Source**
* - TCAR-ICE
  - 0.57
  - Average small and big car from {cite}`20`
  - 0.39
  - 31% improvement from 2020 {cite}`135`
* - TCAR-ICE_0
  - 0.65
  - 15% increase from new investment*
  -
  -
* - TCAR-ELC
  - 0.19
  - Average small and big car from {cite}`20`
  - 0.167
  - 12% improvement from 2020 {cite}`135`
* - TCAR-ELC_0
  - 0.18
  - Same as new investment*
  -
  -
* - TCAR-PLUG
  - 0.42
  - Relative improvement from ICE according to {cite}`135`
  - 0.32
  - 24% improvement from 2020 {cite}`135`
* - TCAR-PLUG_0
  - 0.54
  - 15% increase from new investment*
  -
  -
* - TCAR-H2
  - 0.33
  - {cite}`133`
  - 0.28
  - {cite}`133`
:::

*\*Adjusted afterward so that 2025 SSB road traffic volumes and fuel consumption of road vehicles tally*

***Vans (TVAN)***

Compared with passenger cars, relatively little literature is available on the energy consumption and technical characteristics of vans. However, the two vehicle categories are comparable in size, as both have a maximum gross vehicle weight (GVW) of 3.5 tonnes. Moreover, small vans with a maximum payload of 1 tonne accounted for 71% of the total vehicle-kilometres travelled by vans in Norway in 2019 {cite}`136`.

The energy-consumption assumptions for ICE and battery-electric vans are based on the average values for light and heavy vans reported in *Klimakur 2030* {cite}`20`. In that study, light vans are defined as vehicles with a gross vehicle weight below 1.7 tonnes, while heavy vans have a gross vehicle weight between 1.7 and 3.5 tonnes. Although these categories do not correspond exactly to the classification used by SSB, they are considered sufficiently comparable for the representation of vans in IFE-TIMES-Norway.

{numref}`tab-energy-consumption-vans-tvan` presents the final energy-consumption assumptions applied to the different van powertrains (TVAN) in IFE-TIMES-Norway.

:::{list-table} Energy consumption for vans (TVAN).
:name: tab-energy-consumption-vans-tvan
:header-rows: 2
:widths: 17 11 28 12 30
:column-align: center center center center center
:header-align: center

* - {rowspan}`2` Name in TIMES
  - {colspan}`2` Start year
  - {colspan}`2` 2050
* - **kWh/km**
  - **Source**
  - **kWh/km**
  - **Source**
* - TVAN-ICE
  - 0.7
  - Average of light and heavy van from {cite}`20`
  - 0.622
  - Same improvement as for TCAR-ICE
* - TVAN-ICE_0
  - 0.73
  - 25% increase from new investment*
  -
  -
* - TVAN-ELC
  - 0.23
  - Average of light and heavy van from {cite}`20`
  - 0.21
  - Same improvement over time as for

    TCAR-ELC
* - TVAN-ELC_0
  - 0.22
  - Same as new investment*
  -
  -
* - TVAN-PLUG
  - 0.52
  - Same relative improvement as for TCAR-PLUG relative to TCAR-ICE
  - 0.46
  - Same improvement over time as for

    TCAR-PLUG
* - TVAN-PLUG_0
  - 0.58
  - Same as new investment*
  -
  -
* - TVAN-H2
  - 0.41
  - Same relative improvement as for TCAR-H2 relative to TCAR-ICE
  - 0.37
  - Same improvement over time as for

    TCAR-H2
:::

*\*Adjusted afterward so that 2025 SSB road traffic volumes and fuel consumption of road vehicles tally*

***Trucks (TTRUCK-S, TTRUCK-LS and TTRUCK-LL)***

For trucks and tractor units, it is challenging to find a complete dataset that represents the fuel consumption for all the powertrains used and adapted to Norwegian conditions. Several factors make the Norwegian usage pattern unique, for example: (a) higher max GVW in comparison with the EU and the USA, as the default max GVW is 50 tons and, in some exceptions, up to 60 tons; and (b) a mountainous landscape with few highways results in low average speed with frequent up and downhills.

The efficiency of ICE vehicles is based on empirical data from almost 900000 working days in trucks with engines between 200 and 700+ horsepower. This data was gathered in the LIMCO project {cite}`137` led by TØI and shared with IFE. The received data was then weighted against how the daily mileage is distributed in the national fleet ({numref}`tab-distribution-trucks-daily-mileage-vehicles`) and for each truck type as defined previously.

Experience with zero-emission heavy-duty vehicles remains limited, resulting in considerable uncertainty and variation in estimates of energy consumption. For example, relative improvement in fuel consumption versus ICE for a battery truck from *Klimakur* 2030 {cite}`20` is similar to the fuel cell truck presented by Fulton et.al. {cite}`138`. To include the difference in energy loss between battery and fuel cell technology, their relative advantage versus ICE are based on Fulton et.al. {cite}`138`. A shortcoming in the work of Fulton et.al. is the lack of electric long-haul trucks, such as the Tesla Semi. To estimate the improved energy efficiency of such a truck in Norway, the relative improvement for a short-haul truck from fuel-cell to battery is used as a reference.

It shall be noted that for long-haul vehicles in {cite}`138` with electric and hydrogen powertrains, the advantage over ICE is notably reduced. This is because at steady long-haul driving, the efficiency of ICE increases, while the possibility to regenerate power in electric driveline decreases.

Two long-term trends in goods transport can contribute to reducing the emissions per transported ton of goods and the cost of transport: (a) the emissions and cost per ton of goods are reduced if more goods are transported per vehicle, which encourages the use of bigger vehicles, and (b) the steady increase in the energy efficiency of the vehicles. The first trend forces the energy consumption per vehicle up as the average vehicle becomes heavier, and the second trend decreases the energy consumption per vehicle. As there is uncertainty about how the future heavy-duty market will develop with contradicting trends regarding the fuel consumption per vehicle, the energy efficiency for trucks is set constant from the start year until 2050.

The values used in IFE-TIMES-Norway, based on the sources and assumptions mentioned above, is shown in {numref}`tab-energy-consumption-trucks-ttruck`.

:::{list-table} Energy consumption for trucks (TTRUCK).
:name: tab-energy-consumption-trucks-ttruck
:header-rows: 2
:widths: 20 11 67
:column-align: center center center
:header-align: center

* - {rowspan}`2` Name in TIMES
  - {colspan}`2` Start year
* - **kWh/km**
  - **Source**
* - TTRUCK-S-ICE
  - 3.37
  - Aggregated data from LIMCO {cite}`20`, {cite}`139`
* - TTRUCK-S-ICE_0
  - 3.94
  - 10% increase from new investment*
* - TTRUCK-S-ELC
  - 1.48
  - Relative improvement from ICE in a short-haul truck {cite}`138`
* - TTRUCK-S-ELC_0
  - 1.41
  - Same as new investment*
* - TTRUCK-S-H2
  - 2.49
  - Relative improvement from ICE in a short-haul truck {cite}`138`
* - TTRUCK-LS-ICE
  - 4.83
  - Aggregated data from LIMCO {cite}`139`
* - TTRUCK-LS-ICE_0
  - 5.31
  - 10% increase from new investment*
* - TTRUCK-LS-ELC
  - 2.13
  - Relative improvement from ICE in a short-haul truck {cite}`138`
* - TTRUCK-LS-ELC_0
  - 2.06
  - Same as new investment*
* - TTRUCK-LS-H2
  - 3.57
  - Relative improvement from ICE in a short-haul truck {cite}`138`
* - TTRUCK-LL-ICE
  - 4.19
  - Aggregated data from LIMCO {cite}`139`
* - TTRUCK-LL-ICE_0
  - 4.61
  - 10% increase from new investment
* - TTRUCK-LL-ELC
  - 1.84
  - Relative improvement from H{sub}`2` to ELC short-haul truck according to {cite}`138`
* - TTRUCK-LL-ELC_0
  - 1.75
  - Same as new investment*
* - TTRUCK-LL-H2
  - 3.10
  - Relative improvement from ICE in a long-haul truck {cite}`138`
:::

*\*Adjusted afterward so that 2025 SSB road traffic volumes and fuel consumption of road vehicles tally*

***Buses (TBUS)***

TØI has closely monitored the development of Norway’s public transport system and its experience with zero-emission technologies. Their work {cite}`121`, {cite}`140` provides energy-consumption data for the full range of bus technologies operating between 2016 and 2019. They also provide projections for technologies available in the short to medium term, including more efficient ICE buses and more mature battery-electric buses in 2025.

Because buses account for a relatively small share of total transport-sector energy consumption, no further development in their energy efficiency is assumed beyond 2025. The 2025 energy-consumption values are therefore retained for the remaining model periods. An overview of the values used is in the model shown in {numref}`tab-energy-consumption-buses-tbus`.

:::{list-table} Energy consumption for buses (TBUS).
:name: tab-energy-consumption-buses-tbus
:header-rows: 2
:widths: 17 11 28 12 28
:column-align: center center center center center
:header-align: center

* - {rowspan}`2` Name in TIMES
  - {colspan}`2` Start year
  - {colspan}`2` 2025
* - **kWh/km**
  - **Source**
  - **kWh/km**
  - **Source**
* - TBUS-ICE
  - 4.20
  - {cite}`121`
  - 4.10
  - {cite}`121`
* - TBUS-ICE_0
  - 4.83
  - 15% increase from new investment*
  -
  -
* - TBUS-GAS
  - 5.38
  - Increase relative to ICE Euro IV according to {cite}`140`
  - 5.25
  - Increase relative to ICE Euro IV according to {cite}`140`
* - TBUS-GAS_0
  - 4.32
  - 15% increase from new investment*
  -
  -
* - TBUS-ELC
  - 2.30
  - {cite}`121`
  - 2.10
  - {cite}`121`
* - TBUS-ELC_0
  - 2.18
  - Same as new investment*
  -
  -
* - TBUS-H2
  - 3.33
  - {cite}`121`
  - 3.33
  - {cite}`121`
:::

*\*Adjusted afterward so that 2025 SSB road traffic volumes and fuel consumption of road vehicles tally*

***CO{sub}`2` emissions in start year***

Road transport CO{sub}`2` emissions in 2025 in the model were compared against the SSB emissions data in 2024 {cite}`141` (2025 data is not yet available for detailed subsectors). The existing stock of vehicles is modelled to match the 2025 SSB fuel consumption data (not emissions), and thus small mismatches in numbers can be expected as a result of the fuel emissions factors assumed in the model. As shown in {numref}`tab-comparison-road-transport-co2-emissions`, modelled 2025 road transport CO{sub}`2` emissions are lower than 2024 data. Nonetheless, 2025 SSB emissions data is only 6.8 Mill. ton. (only available as a lumped value, not segregated into road transport subsectors), which is very close to the modelled 2025 value.

:::{list-table} Comparison of Road transport CO{sub}`2` emissions from SSB {cite}`141` and from IFE-TIMES-Norway.
:name: tab-comparison-road-transport-co2-emissions
:header-rows: 1
:widths: 5 23 27 21 20
:column-align: left left center center center
:header-align: center

* - {colspan}`2`
  - **SSB (2024)**
  - **SSB (2025)**
  - **IFE-TIMES-Norway (2025)**
* - {colspan}`2`
  - **Mill. ton CO2**
  - **Mill. ton CO2**
  - **Mill. ton CO2**
* - {colspan}`2` Car
  - **3.28**
  -
  - **3.13**
* - {colspan}`2` Light transport
  - **1.34**
  -
  - **1.12**
* - {colspan}`2` Heavy transport
  - **2.69**
  -
  - **2.48**
* -
  - TTRUCK-S
  -
  -
  - 0.42
* -
  - TTRUCK-LS
  -
  -
  - 0.85
* -
  - TTRUCK-LL
  -
  -
  - 0.74
* -
  - BUS
  -
  -
  - 0.47
* - {colspan}`2` {u}`Total emission from road transport except 2 wheelers`
  - **7.31**
  -
  - **6.73**
* - {colspan}`2` 2-wheelers
  - **0.12**
  -
  -
* - {colspan}`2` {u}`Total emission from road transport`
  - **7.43**
  - **6.8**
  - **6.73**
:::

(sec-maintenance-costs)=
### Maintenance costs

The maintenance costs (see {numref}`tab-maintenance-costs-nok-km`) are based on values specified in *Klimakur 2030* {cite}`20` for ICE and battery powertrains and adapted to gas, plug-in, and fuel cell vehicles. In *Klimakur 2030* they are maintained constant until 2030, and in IFE-TIMES-Norway, they are also assumed constant until 2050. The only exception to the rule is fuel cell vehicles, and this is explained in more detail below.

The maintenance cost for gas buses is assumed to be the same as for ICE. For plug-in vehicles, an average maintenance cost between ICE and battery vehicles is assumed, motivated by decreasing wear of the brake system, but a remaining complex powertrain with many rotating parts. For fuel cell vehicles, the maintenance cost is equal to that of plug-in vehicles in the start year. Nevertheless, maintenance costs based on fuel cell technology remain a novel technology and might require closer follow-up in the near term. In the long term, the maintenance level is assumed to be comparable with EVs.

In *Klimakur 2030*, the maintenance costs for heavy-duty trucks are not differentiated between battery and ICE powertrains, no differentiation is made in IFE-TIMES-Norway.

:::{list-table} Maintenance costs in NOK/km.
:name: tab-maintenance-costs-nok-km
:header-rows: 1
:widths: 22 14 10 14 15 10 10
:column-align: left right center center center center center
:header-align: center

* -
  - Year
  - ICE
  - Plug-in hybrid
  - Battery
  - Fuel cell
  - Gas
* - TCAR
  - Start year
  - 0.62
  - 0.62
  - 0.28
  - 0.45
  -
* -
  - 2030
  -
  -
  -
  - 0.28
  -
* - TVAN
  - Start year
  - 0.65
  - 0.65
  - 0.28
  - 0.46
  -
* -
  - 2030
  -
  -
  -
  - 0.28
  -
* - TTRUCK-S
  - Start year
  - 0.98
  -
  - 0.98
  - 0.98
  -
* - TTRUCK-LS
  - Start year
  - 0.98
  -
  - 0.98
  - 0.98
  -
* - TTRUCK-LL
  - Start year
  - 0.79
  -
  - 0.79
  - 0.79
  -
* - TBUS
  - Start year
  - 2.20
  -
  - 1.60
  - 1.90
  - 2.20
* -
  - 2030
  -
  -
  -
  - 1.60
  -
:::

(sec-investment-cost)=
### Investment cost

The VAT and purchase fees are included only for cars, as it is expected to account for the cost exposed to the buyer of the vehicle.

***Passenger cars (TCAR)***

In the TØI report “360 graders analyse av potensialet for nullutslippskjøretøy" {cite}`134`, the car sales are divided into several car type segments and the cost of each segment (small, compact, medium size, large and luxury). The two largest segments of cars sold are compact and medium-size cars, standing for 43% and 27% of the sales, respectively.

The purchase prices of ICE and EV vehicles are based on *Klimakur 2030* {cite}`20`. The costs are, as with fuel consumption, based on a representative car, and the costs used in IFE-TIMES-Norway are an average value between a small and a large car. For more detailed information about the representative cars, see Section {numref}`sec-fuel-consumption`.

For powertrains other than ICE and battery, the costs are taken from {cite}`134`, based on weighted purchase cost from all the car segments.

*Klimakur 2030* provides cost development between 2020 and 2030, while costs in 2019 and 2025 can be obtained from {cite}`134`. The costs from {cite}`134` are adjusted to the start year and 2030, respectively.

The summary of the costs used for TCAR in IFE-TIMES-Norway, excluding VAT and fees, is shown in {numref}`tab-investment-costs-tcar-exclusive-taxes`. The VAT of 25% is assumed to be paid for both ICE and plug-in vehicles, while a one-time fee for the vehicle registration tax is assumed to be on average 91160 NOK for ICE and 2877 NOK for plug-in vehicles, respectively. These average values are based on estimates by {cite}`134`, which provides differentiated registration tax figures and market shares for different vehicle classes and fuel options. To include these values in TIMES, we added the fees to the vehicle cost and then converted them to inputs for TIMES, dividing the resulting cost estimate by the vehicle's average annual mileage. 

:::{list-table} Investment costs for TCAR, exclusive of taxes and fees.
:name: tab-investment-costs-tcar-exclusive-taxes
:header-rows: 2
:widths: 17 11 28 12 28
:column-align: center center center center center
:header-align: center

* - {rowspan}`2` Name in TIMES
  - {colspan}`2` Start year
  - {colspan}`2` 2030
* - **NOK**
  - **Source**
  - **NOK**
  - **Source**
* - TCAR-ICE
  - 229,100
  - Average small and large car {cite}`20`
  - 241,643
  - Average small and large car {cite}`20`
* - TCAR-ELC
  - 480,500
  - Average small and large car {cite}`20`
  - 248,489
  - Average small and large car {cite}`20`
* - TCAR-PLUG
  - 306,381
  - Trend relative to ICE from {cite}`134`
  - 287,546
  - Trend relative to ICE from {cite}`134`
* - TCAR-H2
  - 765,167
  - Trend relative to ICE from {cite}`134`
  - 370,661
  - Trend relative to ICE from {cite}`134`
:::

***Vans (TVAN)***

*Klimakur 2030* {cite}`20` provides costs for a large and small van for both ICE and battery powertrains. For other powertrains, the same relative cost trends as for TCAR are applied based on the similarities between TVAN and TCAR discussed in Section {numref}`sec-fuel-consumption`. The summary of the costs for TVAN in IFE-TIMES-Norway is shown in {numref}`tab-investment-costs-tvan-exclusive-taxes`.

The vehicle registration fee is indicated to be 24 000 NOK for small vans and 69 000 for large vans for ICE vans {cite}`20`. In IFE-TIMES-Norway, an average of 46 500 NOK per ICE vehicle is used. For plug-in vehicles, the fee is assumed to be so low that it could be neglected.

:::{list-table} Investment costs for TVAN exclusive taxes and fees.
:name: tab-investment-costs-tvan-exclusive-taxes
:header-rows: 2
:widths: 17 11 28 12 30
:column-align: center center center center center
:header-align: center

* - {rowspan}`2` Name in TIMES
  - {colspan}`2` Start year
  - {colspan}`2` 2030
* - **NOK**
  - **Source**
  - **NOK**
  - **Source**
* - TVAN-ICE
  - 230,500
  - Average small and large van {cite}`20`
  - 236,240
  - Average small and large van {cite}`20`
* - TVAN-ELC
  - 506,000
  - Average small and large van {cite}`20`
  - 268,780
  - Average small and large van {cite}`20`
* - TVAN-PLUG
  - 308,254
  - Trend relative to ICE from {cite}`134`
  - 281,116
  - Trend relative to ICE from {cite}`134`
* - TVAN-H2
  - 769,842
  - Trend relative to ICE from {cite}`134`
  - 362,373
  - Trend relative to ICE from {cite}`134`
:::

Moreover, a subsidy for electric vans is applied in 2018 of 3274 kNOK/Mkm/y based on ENOVA support in 2021. The subsidy is assumed to be 0 by 2025 due to the fast uptake of electric vehicles in Norway.

***Trucks (TTRUCK-S, TTRUCK-LS and TTRUCK-LL)***

The investment costs for 2020 and 2030 are based on data received from TØI. They have built up the dataset through cost decomposition of different parts of the vehicle. In addition, a premium cost is added for novel powertrains. This additional cost can, to some extent, be assigned to R&D. The costs of 2020 are quality-checked by a known truck OEM.

In IFE-TIMES-Norway, it is assumed that continued development of investment costs for new drivetrains (fuel cells and batteries) also continues after 2030, while investments in ICE and GAS powertrains are assumed to be constant. Fulton et.al. {cite}`138` predict that by 2050 the fuel cell and battery truck investment costs will reach almost parity with ICE, and their relative cost differences are applied.

A simplification has been made by assuming the same investment cost for TTRUCK-LS and TTRUCK-LL, where it would be reasonable to assume that trucks that drive longer would need larger batteries and hydrogen tanks, thus be more expensive relative to ICE. As battery and fuel cell trucks are still in their infancy, it is hard to find such a distinction in the literature. It should be noted that battery vehicles are not included for TTRUCK-LL by default due to the uncertainty of its technical feasibility.

:::{figure} images/figure-40.png
:name: fig-investment-cost-development-ttruck-s

Investment cost development for TTRUCK-S.
:::

:::{figure} images/figure-41.png
:name: fig-investment-cost-development-ttruck-ls

Investment cost development for TTRUCK-LS & LL.
:::

By 2020, large-scale deployment of battery and hydrogen powertrains is still lacking; however, strong activity within this field is noted, with announcements of several models being introduced. Therefore, the starting year at which they can be deployed in the model has been adjusted, as presented in {numref}`tab-starting-year-investment-battery-hydrogen`.

:::{list-table} Starting year for investment in battery- and hydrogen-powered trucks and tractor units.
:name: tab-starting-year-investment-battery-hydrogen
:header-rows: 1
:widths: 61 20
:column-align: center center
:header-align: center

* - Type of truck and powertrain
  - Starting year
* - TTRUCK-S-ELC &TTRUCK-LS-ELC
  - 2022
* - (TTRUCK-LL-ELC)
  - 2100/2025
* - TTRUCK-S-H2
  - 2025
* - TTRUCK-LS-H2 & TTRUCK-LL-H2
  - 2025
:::

Currently, subsidies are added for electric and hydrogen trucks based on the old support scheme from ENOVA. The subsidy is assumed to be the same for the two fuels (1MNOK per vehicle). It is assumed that subsidies will be removed by 2028 as the fleet for zero-emission trucks develops.

***Buses (TBUS)***

The investment cost for buses until 2025 is based on the TØI report “Klima-og miljøvennlig transport frem mot 2025” {cite}`142`. The cost trend of ICE buses and the relative cost to ICE for the other powertrains in 2050 is based on the cost development of urban buses from Fulton et.al. {cite}`138` from UCDavis. The summary of the costs for TBUS in IFE-TIMES-Norway is shown in {numref}`tab-investment-costs-tbus-exclusive-taxes`.

:::{list-table} Investment costs for TBUS exclusive taxes and fees.
:name: tab-investment-costs-tbus-exclusive-taxes
:header-rows: 1
:widths: 18 17 58
:column-align: center center center
:header-align: center

* - Name in TIMES
  - NOK
  - Source
* - {colspan}`3` Start year
* - TBUS-ICE
  - 2,000,000
  - {cite}`142`
* - TBUS-GAS
  - 2,200,000
  - {cite}`142`
* - TBUS-ELC
  - 4,500,000
  - {cite}`142`
* - TBUS-H2
  - 8,000,000
  - {cite}`142`
* - {colspan}`3` 2025
* - TBUS-ICE
  - 2,000,000
  - {cite}`142`{cite}`122`
* - TBUS-GAS
  - 2,200,000
  - {cite}`142`{cite}`122`
* - TBUS-ELC
  - 3,000,000
  - {cite}`142`{cite}`122`
* - TBUS-H2
  - 4,000,000
  - {cite}`142`{cite}`122`
* - {colspan}`3` 2050
* - TBUS-ICE
  - 2,116,000
  - Relative change from 2025 according to {cite}`138`
* - TBUS-GAS
  - 2,435,000
  - Trend relative to ICE from {cite}`138`
* - TBUS-ELC
  - 2,116,000
  - Trend relative to ICE from {cite}`138`
* - TBUS-H2
  - 2,290,000
  - Trend relative to ICE from {cite}`138`
:::

(sec-lifetime-and-annual-mileage)=
### Lifetime and annual mileage

Vehicle lifetime and annual mileage are two related input parameters in IFE-TIMES-Norway. In practice, vehicles generally travel longer annual distances during their first years of operation, after which their annual mileage declines considerably with age. At the same time, vehicles from a given registration year are gradually retired from the fleet.

IFE-TIMES-Norway simplifies these age-dependent patterns by assuming a constant annual mileage throughout each vehicle’s lifetime. All vehicles within a given vehicle category are also assigned the same technical lifetime. Consequently, vehicles of the same type and vintage are retired from the model fleet simultaneously rather than being gradually phased out.

To derive representative fixed values for vehicle lifetime and annual mileage, data from Statistics Norway were used to analyse the cumulative distribution of annual vehicle-kilometres by vehicle age, as illustrated in {numref}`fig-accumulated-traffic-volume-each-vehicle`.

For each vehicle category in IFE-TIMES-Norway, the assumed lifetime corresponds to the vehicle age at which approximately 90% of the total annual vehicle-kilometres are accounted for. This approach provides a simplified representation of the gradual decline in annual mileage and the continuous retirement of vehicles as they age.

:::{figure} images/figure-42.png
:name: fig-accumulated-traffic-volume-each-vehicle

Accumulated traffic volume of each vehicle type depending on age, based on data from {cite}`139`.
:::

The Statistics Norway (SSB) dataset used to determine vehicle lifetimes provides both total annual vehicle-kilometres and average annual mileage per vehicle. These data are used to estimate the number of vehicles within each vehicle-age interval. For each vehicle category, the representative annual mileage is calculated by dividing the total vehicle-kilometres by the corresponding number of vehicles. The calculation includes only vehicles and vehicle-kilometres within the lifetime assumed for that category in IFE-TIMES-Norway. The resulting annual mileage per vehicle is shown in {numref}`tab-lifetime-annual-mileage-used-ife`.

The SSB dataset distinguishes between tractor units and all other trucks. IFE-TIMES-Norway instead classifies trucks according to their typical daily mileage and operating characteristics. Both conventional trucks and tractor units may therefore be assigned to either the long-distance (TTRUCK-LS) or long-haul (TTRUCK-LL) segment.

To derive representative parameters for TTRUCK-LL, vehicles in this segment are assumed to have a slightly higher annual mileage and a somewhat shorter lifetime than the average tractor unit. This reflects the assumption that tractor units with lower annual mileage are assigned to TTRUCK-LS. The inverse adjustment is applied when deriving the parameters for TTRUCK-S and TTRUCK-LS from the SSB category covering trucks other than tractor units. The resulting assumptions for trucks are also shown in {numref}`tab-lifetime-annual-mileage-used-ife`.

The simplification of vehicle lifetime and average annual mileage has shortcomings, such as underestimating usage of newly invested vehicles (new technology) and overestimating usage of vehicles at the end of their lifetime in IFE-TIMES-Norway (old technology). In addition, the model omits usage of old and very old vehicles that are past their lifetimes set in IFE-TIMES-Norway.

:::{list-table} Lifetime and annual mileage used in IFE-TIMES-Norway.
:name: tab-lifetime-annual-mileage-used-ife
:header-rows: 1
:widths: 20 17 22
:column-align: center center center
:header-align: center

* - Vehicle type
  - Lifetime (years)
  - Average annual mileage (km)
* - TCAR
  - 17
  - 13 200
* - TVAN
  - 15
  - 15 300
* - TTRUCK-S
  - 15
  - 30 000
* - TTRUCK-LS
  - 13
  - 35 000
* - TTRUCK-LL
  - 6
  - 90 000
* - TBUS
  - 10
  - 41 800
:::

(sec-implementation-rates)=
### Implementation rates

By default, TIMES selects investments based on the available technology with the lowest total lifetime cost. Once a new technology becomes the least-cost option, the model may therefore shift all new capacity additions to that technology within a single model period. For vehicle sales, such an immediate transition between powertrains is considered unrealistic. Constraints are therefore imposed on the growth in new capacity for individual powertrains using the NCAP growth user constraint.

The calibration of the growth constraint is inspired by analyses conducted by TØI using its stock-flow vehicle fleet model {cite}`130`. In practice, the market share of a new technology typically develops through successive stages of adoption. Initial uptake is driven by early adopters, followed by more rapid adoption among the majority of consumers and, finally, slower uptake among late adopters. This results in an S-shaped market-adoption curve, as illustrated in {numref}`fig-zero-emission-vehicles-share-new`. By contrast, the growth constraint functionality in TIMES is based on a constant year-to-year growth limitation value, which provides an exponential growth of market share over time.

To make the best possible approximation for the growth constraint, the initial investment in the new technology is allowed to take a relatively large share of the total new investments, and the annual growth rate is selected to fit best where the new technology share of new investments increases most rapidly. The representative growth rate is calculated as the average annual increase in the share of zero-emission technologies as their combined share of new vehicle investments rises from 10% to 90% for the three technologies shown in {numref}`fig-zero-emission-vehicles-share-new`. The growth constraint is adopted for both electric and hydrogen powertrains, while it is assumed that the growth for individual technologies and vehicle types can be twice as fast. It is especially relevant for trucks, as they are subdivided into several subcategories and are the most relevant pretendent for both battery and fuel cell technology in road transport.

:::{figure} images/figure-43.png
:name: fig-zero-emission-vehicles-share-new

The zero-emission vehicles share of new investment and fleet in the fast decarbonization scenario presented in {cite}`130`.
:::

The growth constraint is also applied to conventional vehicle technologies to prevent unrealistic fluctuations in their shares of new vehicle investments. For technologies with an existing stock, the constraint becomes active two years after the stock is introduced through the TIMES STOCK or PASTI parameter. Before the constraint takes effect, the model can calibrate the typical level of new investment in each technology based on the existing fleet. For technologies without an existing stock, an initial investment allowance, referred to as a seed value, is specified. The seed value allows an emerging technology to enter the market before the growth constraint is applied. It is sized to represent 10% of the total new vehicle investment required within one model period.

(sec-ev-charging)=
## EV Charging

(sec-charging-infrastructure-for-evs)=
### Charging infrastructure for EVs

All electric vehicles depend on available charging infrastructure, which brings an additional cost to the system in comparison with current well-established petrol filling station infrastructure. For private vehicles and vans, three different charging types are included: residential, commercial, and fast charging. Both residential and commercial charging occur with slow chargers. Commercial charging is defined as slow charging close to commercial buildings, with the intention to represent that the car is charged at work. The typical usage pattern over a day is shown in {numref}`fig-daily-usage-pattern-ev-charging`. In the base case, it is assumed that passenger cars charge 75% of the time at residential buildings, 15% of the time at commercial buildings, and 10% of the time by fast charging. For vans, it is assumed that charging occurs at home or at commercial buildings (50% each), using the same type of charger.

:::{figure} images/figure-44.png
:name: fig-daily-usage-pattern-ev-charging

Daily usage pattern for EV charging, disaggregated for different charging locations. Derived from {cite}`143`.
:::

Battery-electric vehicles (BEVs) are considerably more energy efficient than internal-combustion-engine (ICE) vehicles. Consequently, they generate less waste heat that can be used for cabin heating. Heating the cabin in cold weather must therefore draw energy from the battery, resulting in greater seasonal variation in BEV energy consumption than in the fuel consumption of comparable ICE vehicles.

The charging profiles applied in IFE-TIMES-Norway are adjusted to account for these seasonal differences in electricity consumption. The relationship between ambient temperature and the additional energy required by BEVs is illustrated in Figure 47 and represented mathematically by Equations (5) and (6), based on {cite}`144`, {cite}`145`. In the model, the best-case scenario is assumed.

The worst-case increase in energy demand is expressed as:

$y_{WC} = - 0,0478*T + 0,8233$ (5)

And the best-case increase is expressed as:

$y_{BC} = - 0,0276*T + 0,475$ (6)

{numref}`tab-seasonal-average-temperature-relative-seasonal` presents the average seasonal temperatures assumed for each Norwegian electricity bidding zone. It also reports the corresponding seasonal energy-consumption factors after adjusting for differences in ambient temperature. These factors express electricity consumption relative to the reference condition of 17 °C used under standard vehicle-testing conditions. A value above 1 therefore indicates additional energy use compared with the reference condition.

Because the average temperature in every Norwegian bidding zone is below 17 °C in all four representative seasons, the applied energy-consumption factors are greater than 1 throughout the year. {numref}`tab-seasonal-average-temperature-relative-seasonal` also presents the annual weighting assigned to each season.

The temperature adjustment affects the seasonal distribution of electric-vehicle charging demand. As illustrated in {numref}`fig-total-ev-charging-demand-time`, total charging demand is higher during winter than during the other seasons because electric vehicles require more energy under colder conditions.

:::{list-table} Seasonal average temperature and relative seasonal energy use.
:name: tab-seasonal-average-temperature-relative-seasonal
:header-rows: 1
:widths: 12 25 40 18
:column-align: left center center center
:header-align: center

* - Season
  - Average temperature (°C)
  - Relative seasonal energy use\
    (compared to normal temperature)
  - Annual share
* - FA
  - 8.46
  - 1.23
  - 0.246
* - SP
  - 6.60
  - 1.27
  - 0.253
* - SU
  - 15.54
  - 1.03
  - 0.206
* - WI
  - -0.02
  - 1.48
  - 0.295
:::

:::{figure} images/figure-45.png
:name: fig-increase-energy-demand-function-outside

Increase in energy demand as a function of outside temperature and estimated worst and best case based on {cite}`144`, {cite}`145`.
:::

:::{figure} images/figure-46.png
:name: fig-total-ev-charging-demand-time

Total EV charging demand by time slices
:::

For heavy-duty vehicles, both slow and fast charging are considered. Both profiles are shown in {numref}`fig-slow-fast-charging-profiles-data` and the share between slow and fast charging for each truck type is shown {numref}`tab-share-energy-supplied-electric-trucks`. As the majority of trucks below a total GVW of 50 tons drive short distances, they are assumed to mainly utilize slow chargers. TTRUCK-LS (total GVW ≥50 ton & \<300 km/day) are assumed to entirely depend on slow chargers. On the other hand, TTRUCK-LL (total GVW ≥50 ton & \>300 km/day) are assumed to depend equally on slow and fast chargers.

:::{figure} images/figure-47.png
:name: fig-slow-fast-charging-profiles-data

Slow and fast charging profiles based on data gathered within the Limco project {cite}`137`.
:::

:::{list-table} Share of energy supplied to electric trucks from slow and fast chargers.
:name: tab-share-energy-supplied-electric-trucks
:header-rows: 1
:widths: 21 25 20
:column-align: center center center
:header-align: center

* -
  - Slow charging
  - Fast charging
* - TTRUCK-S
  - 75%
  - 25%
* - TTRUCK-LS
  - 100%
  -
* - TTRUCK-LL
  - 50%
  - 50%
:::

The investment costs of electric-vehicle charging infrastructure are primarily based on data from *Klimakur* 2030 {cite}`20`. Residential and commercial charging is represented by installations rated below 11 kW, with an assumed average rated power of 7 kW. Public fast charging is represented by 50 kW chargers in the base year. These are gradually replaced by 150 kW chargers by 2025.

Available cost data for heavy-duty vehicle charging are limited. *Klimakur* 2030 provides an investment cost for a 50-kW charger, which is used to represent slow charging for heavy-duty vehicles. This cost is supplemented by a grid-connection cost. The first chargers installed at a logistics centre or similar facility may be accommodated without substantial grid reinforcement. However, larger-scale deployment is assumed to require additional investment in the local electricity grid.

Data on fast-charging infrastructure for heavy-duty trucks are particularly uncertain. In IFE-TIMES-Norway, the cost and technical performance of heavy-duty fast charging are assumed to be more comparable to those of a 350-kW high-power charger than to those of pantograph charging systems currently used by electric buses operating on fixed routes. Because buses account for a relatively small share of road-transport activity, buses and trucks are assumed to share the same charging infrastructure in the model. Bus charging demand is represented using a flat temporal profile.

The main charging unit, whether installed onboard the vehicle or externally, converts alternating current to direct current and transforms electricity between the required voltage levels. Electricity is also consumed by the charger’s control and auxiliary systems. Empirical studies indicate that low-power onboard chargers have an efficiency of approximately 80% {cite}`146`, {cite}`147`. Manufacturers of fast chargers report efficiencies of approximately 90% under favourable operating conditions, typically at around 25 °C. However, efficiency may be considerably lower at low ambient temperatures {cite}`148`.

Slow chargers are typically installed to serve individual vehicles over extended periods, such as 8–12 hours. Their average utilisation is reduced by days when vehicles require only partial charging or are not in operation. Fast chargers can serve multiple vehicles but are used for shorter charging sessions. They must be sized to accommodate peak demand, even though demand may be substantially lower during recurring off-peak periods, particularly at night.

The annual utilisation rate of fast chargers is fixed at 30%. This assumption is informed by observed seasonal variation in vehicle passage counts at Hanestad and Gol {cite}`149`. For slow chargers, the annual utilisation rate is set to 25%, corresponding to an average of six hours of charging per day. Charger lifetimes are based on preliminary assumptions and should be reviewed when more robust data become available. Charger assumptions are collated in {numref}`tab-type-chargers-used-ife-times`.

:::{list-table} Type of chargers used in IFE-TIMES-Norway and their characteristics. Based on {cite}`20`, {cite}`146`, {cite}`148` and own assumptions.
:name: tab-type-chargers-used-ife-times
:header-rows: 1
:widths: 21 12 12 13 12 14 14
:column-align: center center center center center center center
:header-align: center

* -
  - **Year**
  - {colspan}`3` **Light-duty**
  - {colspan}`2` **Heavy-duty**
* - **Type of charger**
  -
  - Residential
  - Commercial
  - Fast charging
  - Slow charging
  - Fast charging
* - **Commodity used**
  -
  - ELC-LV-RES
  - ELC-LV-COM
  - ELC-LV-COM
  - ELC-LV-COM
  - ELC-LV-COM
* - **Efficiency**
  -
  - 80%
  - 80%
  - 90%
  - 90%
  - 90%
* - {rowspan}`2` **Equipment and installation cost (NOK/kW)**
  - **2018**
  - {rowspan}`2` 2857
  - {rowspan}`2` 2857
  - 7000
  - {rowspan}`2` 5000
  - {rowspan}`2` 3400
* - **2025**
  - 3000
* - {rowspan}`2` **Grid connection fee (NOK/kW)**
  - **2018**
  - {rowspan}`2`
  - {rowspan}`2`
  - 5000
  - {rowspan}`2` 2000
  - {rowspan}`2` 1000
* - **2025**
  - 2000
* - **Lifetime (years)**
  -
  - 15
  - 15
  - 15
  - 15
  - 15
* - **Utilisation factor**
  -
  - 25%
  - 25%
  - 30%
  - 25%
  - 30%
:::

(sec-flexible-ev-charging)=
### Flexible EV charging

Flexible EV charging of personal vehicles can be activated in both where and when EVs are charged.

Charging-location flexibility allows the model to allocate charging demand among residential, commercial, and public fast-charging infrastructure. Up to 90% of passenger-vehicle charging demand may be supplied by chargers in residential buildings, while up to 50% may be supplied by chargers in commercial buildings. The share allocated to public fast charging is fixed at 10% and is not flexible. These limits are implemented using upper bounds on FLO_MARK.

Temporal flexibility allows for either 50% or 90% flexibility in terms of when EVs are charging in either residential or commercial buildings, based on the charging profile of {numref}`fig-daily-usage-pattern-ev-charging`. Flexibility is available from 2025 onwards and is modelled through an UP and LO bound on FLO_FR. The UP bound is a 50/90% increase from the original profile, while the lower bound is a 50/90% decrease from the original profile. Flexible charging is currently only activated in residential and commercial charging of personal vehicles, while charging of vans and trucks remains inflexible.

(sec-non-road-transport)=
## Non-road transport

(sec-modelling-of-rail-and-other-transport)=
### Modelling of rail and other transport

Energy use in rail transport and other transport is modelled as a share of different energy carriers. In rail transport, the existing stock is represented by the energy demand and is assumed to decrease linearly within a lifetime of 20 years. In the regions NO1, NO2 and NO5, the railway can use 100% electricity. In NO3 and NO4, electricity consumption was assumed to be at 32% and 16%, respectively, to match the railway consumption data in SSB. It is assumed that the railway network in regions NO3 and NO4 can be fully electrified by 2040. When electricity-based railways are not available, locomotives are assumed to be powered by diesel engines that can use a mix of fossil and biofuel. Existing rail transport stock can be replaced by diesel engines, electric, and fuel-cell-powered locomotives. Fuel cell-powered locomotives are also given as an investment option that could be switched on in the model in more technologically-leaning scenarios. The techno-economic assumptions related to rail transport technologies are presented in *{numref}`tab-investment-cost-type-locomotive`.*

:::{list-table} Investment cost per type of locomotive.
:name: tab-investment-cost-type-locomotive
:header-rows: 1
:widths: 31 10 10 12 10
:column-align: left center center center left
:header-align: center

* - Type of locomotive
  - Diesel engine
  - Electric
  - Hydrogen fuel cell
  - Source
* - Power output (MW)
  - {colspan}`3` 3
  - {cite}`150`
* - Operational availability (%)
  - {colspan}`3` 91.7
  - {cite}`151`
* - {colspan}`4` CAPEX (kNOK/locomotive)
  - {rowspan}`4` {cite}`152`
* - 2020
  - 94 969
  - 129 633
  - 153 734
* - 2030
  - 94 969
  - 129 633
  - 153 734
* - 2050
  - 94 969
  - 129 633
  - 153 734
:::

(sec-modelling-of-maritime-transport)=
### Modelling of Maritime Transport

Energy demand and emissions from the maritime sector in 2025 from SSB were used as the basis for calibration of current sea transport demand. In the model, these were divided among passenger transport, fishing, and goods transport. To estimate the potential for decarbonisation, it is crucial to disaggregate the subsector into these groups since maritime transport varies greatly in ship designs and sizes as well as operation patterns. These varying parameters affect how well different zero-emission fuels and technologies can penetrate the different ship segments. Thus, the maritime transport demands in the model are divided based on the assumptions presented in Section 5.3.1.

The main fuels used in the maritime sector today are liquid fuels, marine gas oil (MGO) and marine diesel oil (MDO), and gas-based fossil fuels, liquefied natural gas (LNG). A minimum demand of 6% biofuel blended in petroleum oil is added from 2023 {cite}`132`, {cite}`153`. Alternative propulsion fuels considered in IFE-TIMES-Norway are batteries and hydrogen for short-distance trips and ammonia for deep-sea trips. Liquid hydrogen is also a potential fuel for use in the maritime sector, but as it largely overlaps with the usage of ammonia, the latter is chosen to represent hydrogen derivatives in deep-sea shipping.

The technology options in IFE-TIMES-Norway and the max share of each technology are shown in {numref}`tab-maximum-shares-assumed-each-propulsion`. Due to the immaturity of hydrogen and ammonia as maritime fuels, they are only available from 2030. The max market share of each technology for passenger vessels is based on work developed in HyInfra project {cite}`154`, while for the other two ship categories, they are based on best guesses when considering the ship sizes and trip lengths. The max share remains constant after 2040.

:::{list-table} Maximum shares assumed for each propulsion option to serve the maritime demand. Linear interpolation is used for years between inputs.
:name: tab-maximum-shares-assumed-each-propulsion
:header-rows: 2
:widths: 9 20 9 10 12 12 12 12
:column-align: center center center center center center center center
:header-align: center

* - {rowspan}`2` **Group**
  - {rowspan}`2` **Type of vessel**
  - {rowspan}`2` **Year**
  - {colspan}`5` **Fuel used/propulsion system**
* - **ICE**
  - **LNG**
  - **Battery**
  - **H{sub}`2`**
  - **Ammonia**
* - {rowspan}`4` 1
  - {rowspan}`4` Passenger vessels
  - 2018
  - {rowspan}`4` no limits
  - 0%
  - 0%
  -
  -
* - 2025
  -
  -
  - 0%
  - 0%
* - 2030
  - 86%
  - 49%
  - 13%
  - 38%
* - 2040
  - 86%
  - 49%
  - 13%
  - 38%
* - {rowspan}`4` 2
  - {rowspan}`4` Fishing vessels
  - 2018
  - {rowspan}`4` no limits
  - 0%
  - 0%
  -
  -
* - 2025
  -
  -
  - 0%
  - 0%
* - 2030
  -
  - 5%
  - 5%
  - 5%
* - 2040
  - 50%
  - 25%
  - 25%
  - 50%
* - {rowspan}`4` 3
  - {rowspan}`4` Freight, service & other vessels
  - 2018
  - {rowspan}`4` no limits
  - 0%
  - 0%
  -
  -
* - 2025
  -
  -
  - 0%
  - 0%
* - 2030
  -
  - 50%*
  - 5%
  - 5%
* - 2040
  - 90%
  - 80%*
  - 10%
  - 90%
:::

*\*In group 3, battery electric propulsion is only assigned to the “Other” vessel segment, corresponding to short-haul coastal ships and supply vessels.*

The current fossil fuels are consumed onboard in large and highly efficient (~45-50%) internal combustion engines (ICE). For future fuels, ammonia is also assumed to be consumed in ICE, while hydrogen is consumed in PEM fuel cells. For both of these new fuels, the energy efficiency is assumed to be similar to conventional ICE. On the other hand, systems based on battery systems are assumed to have efficiency of 80%.

As an intent to represent the investment costs related to energy consumption by the maritime sector, a typical ship type was selected for group 1 based on energy consumption {cite}`155` and 3 based on the largest emissions or energy consumption ({numref}`tab-investment-costs-representative-ship-technology`). A representative size and its investment costs were identified, as well as the fleet size of the specific vessel. Thereafter, based on assumed energy consumption for the specific vessel type, a cost per demand in GWh was identified. The assumptions and results can be seen in {numref}`tab-investment-costs-representative-ship-technology`.

Fishing vessel size varies greatly, and with that also their costs and energy demand. It was not possible to identify how the energy demand is distributed among the different sizes of the vessels, thereby impeding the coupling of investment costs to energy demand. Thereby, they are assigned the same investment cost as passenger vessels per annual energy consumption. Even higher values could be expected, as not all fishing vessels can work constantly throughout the year; for example, ferries or offshore vessels, and thereby a lower energy demand per vessel.

:::{list-table} Investment costs for representative ship technology for maritime demand group 1 and 3.
:name: tab-investment-costs-representative-ship-technology
:header-rows: 1
:widths: 45 22 29
:column-align: left center center
:header-align: center

* - Group
  - 1
  - 3
* - Type of vessel
  - Passenger vessels
  - Other vessels
* - Example design
  - Roll-on/Roll-off Ferry (Ro Ro ferry)
  - Platform Supply Vessel (Offshore vessel)
* - Size {cite}`135`
  - 1900 GT (PBE 70)
  - 5080 DWT
* - Fleet size {cite}`135`
  - 203
  - 122
* - Annual energy consumption (GWh)
  - 856
  - 987
* - Specific energy consumption (GWh/ship)
  - 4.2
  - 8.1
* - CAPEX (kNOK/ship)
  - 100 000 {cite}`136`
  - 180 000 {cite}`137`
* - CAPEX (kNOK/(GWh/year))
  - 23 728
  - 22 260
:::

Regarding investment in propulsion systems using other fuels in groups 1 and 2, DNV-GL estimates that investment in an LNG ship is 20% more expensive {cite}`156`. For the other fuels and propulsion systems, it is very hard to obtain their additional investment costs; their costs are consequently assumed to be 50% higher than for a conventional ICE system today. By 2030, their extra costs are assumed to be reduced to 20% higher than ICE. For group 3, an additional scaling of the investment costs is estimated to characterize the differences between the five different vessel segments and their available propulsion options. To this end, the differences in costs reported from the MarE-fuel project were used {cite}`157`. The cost scaling for the different vessel segments in sea freight transport is presented in {numref}`fig-differences-investment-costs-ship-type`. More information about cost estimates can be found in {cite}`158`.

:::{figure} images/figure-48.png
:name: fig-differences-investment-costs-ship-type

Differences in investment costs by ship type and propulsion option compared to assumptions considering one reference ship type and fixed 20% higher cost scaling. Disaggregated cost estimates derived from {cite}`157`.
:::

The lifetime of all ships in groups 1 and 2 is assumed to be 25 years. Even if ships can live considerably longer, their capacity factors, on average, are assumed to be higher for newer vessels, and that older ships, to a large degree, are sold to other countries. With the ship’s long lifetime, it is usual to make retrofits and consider their second-hand life. In this simplified approximation to the maritime demand, these aspects are omitted. Based on data from {cite}`157`, additional differentiation is provided for the lifetime of the vessels in group 3. Under these assumptions, containers, bulk carriers, cargo ships, tankers, and other ships have expected lifetimes of 25, 28, 35, 25, and 33 years, respectively.

(sec-aviation)=
### Aviation

The demand estimates for aviation correspond to energy demands for domestic transport. The energy demand data in the base model correspond to the values reported in the 2025 energy balances from SSB and projected towards 2050 based on NTP projected transport demand estimates. Air transport uses fossil fuels in the base year, with a share of 1.4% biofuels in 2025 {cite}`61`. Norway plans to adopt the RefuelEU aviation regulations from 2027. This entails increasing the blend of sustainable fuels in aircraft to 70% by 2050 {cite}`159`.

Electricity can be used in air transport after 2035; its market share is assumed to reach a maximum of 20% by 2040. Air transport using electricity is assumed to be twice as effective as fossil fuels or biofuels. Hydrogen aircraft are also included as an investment option that could be switched on in technologically rich scenarios {cite}`61`. When included in the modelling scenario, a gradual rollout of hydrogen-based aircraft is assumed, enabling shares of the aviation demand of up to 10% in the start year 2035, 20% in 2040, and 40% in 2050 {cite}`160`. The use of synthetic jet fuel (e-kerosene) is also available in aviation as a fuel option starting in 2030, competing with fossil jet fuels and biofuels.

The investment costs for aircraft were obtained from the EU reference scenario 2020 techno-economic assumptions of the PRIMES-TREMOVE transport model {cite}`152`. 344,146,718 annual person-km per aircraft was assumed {cite}`161`.For conventional aircraft, battery electric aircraft, and hydrogen fuel cell aircraft, the capital costs associated with a 22% reduction in specific energy consumption relative to 2015, the cost associated with 350 km of battery range, and the capital costs associated with energy consumption of 2304 toe/Mvkm were used, respectively. Each aircraft was assumed to have 170 seats and a lifetime of 20 years, and fuel consumption information from {cite}`162` was used to convert person-km demand to final energy consumption demand in GWh. The START years for TAIR-ICE and TAIR-ELC are 2018 and 2035, respectively. TAIR-H2 is only activated by 2035 in scenarios that assume a mature hydrogen economy in Norway.

:::{list-table} Investment costs for TAIR exclusive taxes and fees.
:name: tab-investment-costs-tair-exclusive-taxes
:header-rows: 1
:widths: 18 31 44
:column-align: center center center
:header-align: center

* - Name in TIMES
  - NOK/GWh of final energy consumption
  - Source
* - {colspan}`3` Start year
* - TAIR-ICE
  - 13,149,145
  - {rowspan}`3` {cite}`152`
* - TAIR-ELC
  - 36,138,219
* - TAIR-H2
  - 16,777,981
* - {colspan}`3` 2050
* - TAIR-ICE
  - 9,958,543
  -
* - TAIR-ELC
  - 31,826,273
  -
* - TAIR-H2
  - 15,912,020
  -
:::
