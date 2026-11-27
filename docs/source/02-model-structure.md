(sec-model-structure)=
# Model structure

The model input and design are structured in several Excel files, each of which is described in the following chapters. An overview of the main content of these files is presented in {numref}`tab-overview-model-files-main-content`.

The overall model characteristics such as base year, time periods, regions, time-slices, discount rate (incl. year for discounting), units, etc. are defined in the SysSettings file. The present data used within this file are:

- Regions: NO1, NO2, NO3, NO4, NO5 (The five Norwegian electricity spot price regions); five offshore regions: Nordavind, Nordvest, Vestavind1, Vestavind2 and Sørvest; and five Oil & Gas (O&G) regions: P1, P2, P3, P4 and P5 (see {numref}`fig-regions-included-ife-times-norway`)

- Start year: 2018

- Time slices (see {numref}`fig-time-slice-tree-ife-times`)

  - 4 Seasons (Fall, Spring, Summer, Winter)

  - 24 hours per day (DayNite: 01, 02, 03, …, 24)

- Discount rate: 4%

- Discount year: 2018

- Currency: kNOK2021

- Activity unit: GWh

- Capacity unit: MW

- Commodity unit: GWh

:::{figure} images/figure-03.png
:name: fig-regions-included-ife-times-norway

Regions included in IFE-TIMES-Norway, NO1 to NO5 and offshore regions.
:::

All monetary values in IFE-TIMES-Norway are expressed in thousands of 2021 Norwegian Kroner (kNOK2021). The year 2021 was selected as the common price year because a substantial share of the cost data currently used in the model originates from around this period. Costs reported for other years, including taxes and selected technology costs, are generally converted to 2021 price levels using the consumer price index {cite}`7`. Some costs obtained from the literature cannot be converted because their original price year is not specified. These values are therefore included without adjustment. In many cases, they represent approximate estimates and are subject to considerable uncertainty. When new technologies are added to the model, the associated costs are converted to kNOK2021 whenever sufficient information on the original price year is available.

The modelling periods are often defined as presented in {numref}`fig-time-slice-tree-ife-times`, consisting of 5-year periods after the initial two periods of 2018 and 2020. Nonetheless, both the modelling periods and time-slice levels can be changed within the model. Temporal resolution can be adapted to the needs of individual studies.

In the standard model configuration, each year is divided into four representative seasons of equal duration, with each season assigned a weight corresponding to 25% of the year. Winter represents December to February, spring represents March to May, summer represents June to August, and autumn represents September to November.

Each representative season is further divided into 24 hourly time slices. The standard temporal structure therefore comprises a total of (4 x 24) 96 sub-annual time slices per model year, calculated as four representative seasons multiplied by 24 hours.

:::{figure} images/figure-04.png
:name: fig-time-slice-tree-ife-times

Time slice tree of IFE-TIMES-Norway (base version)
:::

An overview of the different files included in IFE-TIMES-Norway is presented in {numref}`tab-overview-model-files-main-content`. The model consists of seven basic files representing the end-use sectors: buildings, industry, and transportation, as well as the energy sectors: power, offshore power, and district heating. In addition, all fuels are defined in “Fuels”. The Power file includes hydro, onshore wind, and photovoltaics (PV), while combined heat and power plants are included in the DistHeating file. No stock gas power or other thermal power plants are included in the model, aside from the option to invest in gas power plant with carbon capture. Offshore wind power and offshore oil and gas extraction are included in the offshore file.

Different scenario files are developed. Some are project-specific and should only be activated when they are relevant for the analysis. Meanwhile, other scenario files should always be activated in the “Base run”. These scenario files start with the name “Scen_A_xxx”, and include energy taxes, CO{sub}`2` prices, minimum requirements for zero-emission trucks (EU), electricity trade prices, biomass balance, and other user-specific constraints. This is described in more detail in the sector chapters. SubRES files can only include new technologies not included in base year templates. In IFE-TIMES-Norway, CCS technologies are included as SubRES files. Electricity trade parameters are defined in the Trades files.

Profiles are collected in the scenario file “Scen_xxTimeslice”, where xx depends on the time resolution being utilized for a study. By default, xx is 96, which pertains to 96 sub-annual time slices per model year. Demand profiles, hydropower inflow, onshore and offshore wind capacity factors, solar capacity factors, EV charging profiles, heat pump efficiencies, and district heating utilization are all included here.

:::{list-table} Overview of model files and main content in IFE-TIMES-Norway.
:name: tab-overview-model-files-main-content
:header-rows: 1
:widths: 43 56

* - Model files
  - Content
* - SysSettings
  - Starting year, time periods, time slices, regions, discount rate, units, exchange rates, etc.
* - VT_Norway_Power
  - Electricity generation technologies (except offshore wind and CHP)

    Production potentials/limitations/costs
* - VT_Norway_Offshore
  - Offshore wind technologies

    Production potentials/limitations/costs

    Offshore oil and gas extraction

    Demand for gas and electricity in offshore O&G
* - VT_Norway_DistHeating
  - District heating technologies

    Production potentials/limitations/costs
* - VT_Norway_Fuels
  - Fuel definitions, prices, potentials (waste, wood)\
    Technology-specific delivery costs\
    Hydrogen, ammonia, e-fuel & bioenergy production technologies\
    CO{sub}`2` emissions
* - VT_Norway_Industry
  - Annual demand\
    Demand technologies incl. potentials/limitations
* - VT_Norway_Buildings
  - Annual demand\
    Demand technologies incl. potentials/limitations
* - VT_Norway_Transport
  - Annual demand\
    Demand technologies incl. potentials/limitations
* - Trades
  - Power trade links & parameters (existing and new)
* - Scen_96Timeslice
  - Time-slice profiles of demand, resources, electricity trade prices
* - Scen_A_CO2_Medium
  - CO{sub}`2` prices
* - Scen_A_Taxes
  - Energy related taxes of 2024
* - Scen_A_UC
  - User constraints (limitations) on Norwegian bioenergy, building applied PV production on flat roofs, local electrolysers, minimum sales of ZEVs, heat pump growth, offshore transmission and emissions in O&G sector, O&G electrification, relationship CCS/DACCS in industry
* - Scen_A_FLO_MARK_wind
  - Limitation on total amount of O&G demand that can be supplied from offshore wind (< 90%)
* - Scen_xxx
  - Different scenario files with e.g. alternative demand, technology sensitivities, CO{sub}`2` prices, etc.
* - SubRES_xxx
  - New technologies in different SubRES files, e.g. CCS
:::

This report describes IFE-TIMES-Norway according to the functions and components represented in the model. Consequently, the chapter structure does not always correspond directly to the organisation of the model input files. For example, time-series profiles are documented together with the technologies to which they apply, rather than in a separate chapter corresponding to the Base_Profiles scenario file in which the profiles are defined. This function-based structure is intended to provide a more coherent description of the relationships between technologies, parameters, and model assumptions.

Investment costs in IFE-TIMES-Norway are intended to represent the total installed cost of a technology. Where data are available, this includes the cost of the technology itself, land acquisition, site preparation, supporting infrastructure, and other costs required for installation and commissioning. However, sufficiently detailed data are not available for all technologies, and some cost components may therefore be omitted or represented only approximately. For technologies requiring substantial construction time, financing costs incurred during the construction period are also included where possible. These costs represent the cost of capital, including interest accrued before the technology becomes operational.

The TIMES modelling framework can be applied using a deterministic or a stochastic formulation, where the stochastic approach can consider both short-term and long-term uncertainty {cite}`8`. IFE-TIMES-Norway is currently in use in several projects using stochastic programming in order to consider the short-term uncertainty of various parameters, such as weather-dependent renewable electricity supply and heat demand. As illustrated in {cite}`9`, {cite}`10`, {cite}`11`, {cite}`12`, a two-stage stochastic model can be used to provide investment decisions that explicitly value flexibility by considering a set of operational situations that can occur due to the short-term uncertainty of weather-dependent supply and demand.

The stochastic modelling approach is further described in {cite}`13` and {cite}`14`. The following citation in {cite}`13` captures the main aspects:

 “The stochastic approach is designed such that the first-stage variables, investments, are set before knowing the outcome of the uncertain parameters, like European electricity prices. The second-stage variables, operation of the energy system, are done in each scenario when the realisation of the electricity price is known. Consequently, the investments are identical for all scenarios, whereas the operational decisions are dependent on the realisation of the electricity price. The TIMES model minimises the investment costs and the average of the operational costs for all scenarios. This gives investment decisions that recognise the expected operational cost and ensure feasibility across all the model-specified realisations of electricity prices.”
