(sec-industry)=
# Industry

(sec-structure)=
## Structure

The industry sector in IFE-TIMES-Norway primarily represents manufacturing. It also includes agriculture, forestry, fishing and aquaculture, excluding fishing vessels, as well as construction and the extraction of minerals. In official statistics, data centres are classified as part of the tertiary sector. However, because their energy use is more appropriately represented using the modelling structure applied to industrial activities in TIMES, they are included in the industry sector as a separate subsector denoted DATA.

The sector also includes selected fuel-production activities within the energy industries, such as oil refining, the production of fuels for export, and onshore activities associated with offshore O&G extraction. By contrast, facilities that convert Norwegian energy resources into fuels for domestic consumption, including biorefineries and hydrogen-production plants, are represented as energy-conversion technologies. Their production is determined endogenously by the model rather than being driven by a fixed industrial energy-service demand. These facilities are therefore not included in the industry sector.

Offshore O&G extraction is represented separately through five offshore regions in a dedicated module of IFE-TIMES-Norway, which is linked to the representation of offshore wind described in chapter {numref}`sec-offshore-wind-power`. The offshore O&G regions represent the development of energy demand across 38 O&G fields. To limit model complexity, these fields are aggregated into five geographical regions. Further information on the aggregation of individual fields is provided in {cite}`87`.

The representation of industry is based on plant-specific information for approximately 50 of Norway’s largest industrial energy users, supplemented by data for several other major CO₂-emitting facilities. In total, approximately 60 plants are represented individually. The remaining industrial activities are modelled at a more aggregated level. A more detailed description of the industrial-sector representation, including the grouping of plants and subsectors, is provided in {cite}`87`.

The industry sector is divided into the following sub-sectors:

- ALU - Aluminium industry

- MET - Metal industry (other metallurgical production such as ferrosilicon, silicon, manganese, carbides, copper, zinc, iron, steel; all manufacturing using coal and coke as input material are included in metals, although they, in some cases, belong to chemicals in the statistics)

- CHEM - Chemical industry (excl. metallurgical)

- WOOD - Wood industry (production of pulp & paper, and sawmills)

- MIN - Mineral industry (non-metallic mineral products)

- OTHER – Light/other industry (food & tobacco, transport equipment, machinery, textile and leather, etc.)

- PET-ON - Petroleum industry onshore (onshore O&G treatment and refineries)

- PETRO – Petroleum industry offshore (O&G extraction)

- BAT – Battery manufacturing factories

- DATA - Data centres

- NEW – Other new activities not included elsewhere, such as hydrogen, ammonia, or synfuel for export (production of hydrogen, ammonia, biofuels, etc. used in Norway are modelled as processes in the Energy Production Sector of IFE-TIMES-Norway)

- CON – Construction and building industry

- AGR – Agriculture (primary sector, incl. agriculture, forest, fishing with aquaculture but excl. fishing vessels that are included in Transport)

Energy consumption data in 2020 were used as the basis in calibrating the current industry demand in the model. An illustration of the energy and electricity consumption by industrial manufacturing subsector in 2020 is presented in {numref}`fig-total-energy-electricity-sub-sector` {cite}`61`.

:::{figure} images/figure-21.png
:name: fig-total-energy-electricity-sub-sector

Total energy and electricity by sub-sector of manufacturing industry in 2020, TWh/year {cite}`87`.
:::

Demand for non-substitutional electricity, fuels used for heat production, and process materials that emit CO{sub}`2`, such as coke used as a reducing agent in metals manufacturing, are exogenous inputs to IFE-TIMES-Norway. In the model, these are denoted by identifiers ELC, HEAT, and PRC, respectively. While these demands are given as input, the model optimizes the total energy/fuel consumption that generates these demand commodities, including the use of various energy carriers and investments in new technologies.

Energy use in the agricultural sector includes the use of machinery. This is allocated to the AGR sector, although it is mobile energy use, and in the emission account, it is reported as mobile emissions. The same principle is used for energy use by machinery in CON, where all energy use is included in the industry subsector CON. For fishing vessels, the fuel used is included in the transport sector due to the strong similarity with other vessels. Energy use for transport of other industry manufacturing (use of auto diesel in the energy balance {cite}`61`) is included in the transport sector.

(sec-demand-projection)=
## Demand projection

Energy-service demand is calculated outside the energy system model and provided as an exogenous input to IFE-TIMES-Norway. By contrast, energy use by energy carrier, industrial subsector, end-use category, and technology is determined endogenously and reported as model output. In the industry sector, energy-service demand is currently expressed as annual energy demand in GWh/year. Although this functionality is not implemented in the current model version, energy-service demand could alternatively be expressed in terms of physical production, such as tons per year, using assumptions regarding the energy required per unit of output (GWh/ktons).

The allocation of energy carriers across industrial subsectors is based on the Norwegian energy balance {cite}`61`. However, the energy balance does not provide the required distribution among the three industrial end-use categories represented in the model, nor does it show how they are distributed across the different electricity price regions. Energy use is therefore allocated to the energy-service demand type based on available knowledge of energy-consuming activities within each industrial subsector. In addition, energy consumption was distributed across the regions by looking into the consumption data of the largest industrial users (described in more detail in {cite}`87`). Consequently, the allocation by end use for each region is more uncertain than the total energy use assigned to each subsector.

Fuels used to generate process heat were obtained from the energy balance {cite}`61` for each industrial subsector. The upper limits of the share of fossil inputs per subsector are assumed to remain at current levels, while non-fossil resources are allowed to grow. The use of district heating is limited by the share of process heat per subsector that is below 100˚C {cite}`97`.

Non-substitutable electricity represents electricity demand that must be supplied by electricity and cannot be replaced by another energy carrier. The PRC category represents process inputs, including reducing agents such as coal and coke used in metal production, natural gas used in the chemical industry, as well as wood used as a raw material in sawmills and pulp and paper production. Because this category includes several heterogeneous materials and industrial processes, the potential for material substitution must be assessed individually for each subsector.

The emission accounts {cite}`96` are used to estimate the quantities of energy commodities used as material inputs in manufacturing processes (PRC). The main purpose of this representation is to reproduce, as closely as possible, the CO₂ emissions classified as “process emissions“.

Hydrogen production for domestic consumption is not represented as a manufacturing activity. Instead, it is modelled as an energy-sector conversion process that supplies hydrogen to domestic end-use sectors, including industry and road, maritime, aviation, and rail transport. Hydrogen production associated with a potential new export industry is represented separately, with the level of hydrogen production for export estimated exogenously. A scenario that represents significant growth in the hydrogen export industry is estimated by looking into the planned production plants in Norway {cite}`98` and assuming that about 55% of the planned capacity is for exports.

Electricity consumption from data centres in Norway has increased fivefold from 2021 to 2025 {cite}`99` and is expected to grow even further. In the model, current data centre power demands in the different electricity bidding regions were taken from Elhub {cite}`99` and future demand projections used in IFE-TIMES-Norway were mainly taken from Statnett {cite}`100`. Given below are different estimates of power demand growth in Norway’s data centres.

:::{figure} images/figure-22.png
:name: fig-power-demand-projection-data-centres

Power demand projection from data centres, TWh/year {cite}`100`, {cite}`101`, {cite}`102`.
:::

Future industrial energy demand is subject to considerable uncertainty and can strongly influence the Norwegian power balance because of both the electricity consumption of existing industries and ambitions for new industrial activities. The base-case projection assumes that most existing industrial plants continue operating at approximately their current production levels. Announced closures and known investments that increase production capacity are also incorporated into the base projection where relevant {cite}`87`.

In addition to the medium industrial energy-service demand trajectory applied in the base scenario, Low and High Demand trajectories were developed in {cite}`87`. These scenarios represent alternative developments in existing industrial activity, announced projects, and potential new industrial demand. The most notable growths in the High Demand case come from new industries, which include data centres, hydrogen export, and battery production. In the Low Demand case, the most noticeable change is the phase-out of the O&G activities by 2035. The power demand of the three scenarios is presented in {numref}`fig-power-demand-projection-high-medium`.

:::{figure} images/figure-23.png
:name: fig-power-demand-projection-high-medium

Power demand projection in the high, medium and low scenarios and in 2020 per industry subsector {cite}`73`, TWh/year.
:::

O&G extraction is part of the energy sector and is modelled in the offshore file of IFE-TIMES-Norway (VT_Offshore). The description of demand and end-use technologies is included in this chapter due to the similarities with industry.

The energy demand of O&G extraction towards 2050 develops according to the planned decommissioning and new fields that have started or are planned to start production after 2021. New fields included are Bauge, Nova, Fenja, Breidablikk, and Hanz. The energy demand is further split into two: a) demand covered by existing electrification, and b) demand covered by gas today, but with the potential to be electrified in the future. An overview of the existing electrification measures included can be found in {numref}`tab-existing-electrification-shore`. Some of the plants are only partly electrified, and therefore also include demand for electricity that can be met either by new electrification or by gas. Moreover, decided electrification, such as at Melkøya, is fixed in the model. Based on the Ministry of Energy {cite}`104`, it is assumed that not all emissions from the oil and gas sector can be omitted (e.g., due to flaring and back-up generators), corresponding to 0.9 Mt remaining in 2050. This is forced in the model through a user constraint, in which total emissions from offshore O&G activity should be a minimum of 0.9 Mt in 2050.

The demand development for the five grouped regions is presented in {numref}`fig-demand-projections-assumed-base-case`, divided by supply from existing and planned electrification and supply from gas and potential new electrification. All demand is included as electricity demand, in which gas consumption is converted using a rate of 0.35.

:::{list-table} Existing electrification from shore.
:name: tab-existing-electrification-shore
:header-rows: 1
:widths: 50

* - In operation today
* - Utsirahøyden

    Vallhall

    Troll A

    Martin Linge

    Goliat

    Nyhamna processing facility{sup}`1`

    Melkøya LNG facility{sup}`1`

    Kårstø{sup}`1`

    Kollsnes{sup}`1`

    Gasum LNG{sup}`1`

    Stureterminalen{sup}`1`

    Slagentangen (until 2020){sup}`1`
:::

> {sup}`1` Onshore activity

:::{figure} images/figure-24.png
:name: fig-demand-projections-assumed-base-case

Demand projections assumed in the base case for the five offshore regions from 2018 to 2050. Electrification from existing power from shore is marked by the black box. Remaining demand can be covered by gas or new electrification.
:::

(sec-load-profiles)=
## Load profiles

The load profile of all industry sub-sectors, besides Other industry (denoted as OTHER in Chapter {numref}`sec-structure`), is assumed to be flat, i.e., continuous operating time during the entire year. In Other industry, a daily load profile is used, see {numref}`fig-daily-load-profile-other-industry`, assuming no seasonal variation. The profile is equal to that of commercial buildings {cite}`105`, {cite}`106`.

:::{figure} images/figure-25.png
:name: fig-daily-load-profile-other-industry

Daily load profile in other industry.
:::

(sec-demand-technologies)=
## Demand technologies

(sec-heating-technologies-1)=
### Heating technologies

Industrial heat demand is supplied either indirectly through steam, hot-water, or thermal-oil systems, or directly within process equipment. Reliable data on the investment costs, efficiencies, and other technical characteristics of industrial heating and process equipment are limited. Moreover, energy-consuming equipment is often integrated into the production process, making it difficult to isolate the costs attributable specifically to heat generation and energy use.

Industrial heat demand is therefore represented based on the quantities of fuels and energy carriers used to supply heat, as reported in the Norwegian energy balance {cite}`61`. Consequently, the model primarily optimises the cost of meeting industrial heat demand based on the prices of fuels and other energy carriers. It does not generally account for the full investment costs associated with replacing or modifying the underlying process equipment.

For most industrial subsectors, the representation of heat demand includes upper limits on the shares that can be supplied by individual energy carriers. The initial shares are calibrated to the 2020 energy balance {cite}`61`, while maximum allowable shares are specified for future model periods, as presented in {numref}`tab-maximum-share-non-fossil-energy`.

The maximum share of petroleum-based energy carriers is assumed not to increase above its 2020 level. The use of district heating is restricted to the estimated share of process-heat demand below 100 °C {cite}`97`. Electricity can also supply industrial heat, although its use is constrained in subsectors where high temperatures or other process-specific conditions limit electrification. The maximum electricity shares are set at 10% in the chemical industry (CHEM), 100% in the wood-products industry (WOOD), and 50% in mineral extraction and processing (MIN).

Hydrogen is included as a potential substitute for fossil oil and gas used in boilers and process equipment. This substitution option is available in the METallurgical and CHEMical industries with high-temperature process-heat requirements. The model primarily attributes the investment cost of this pathway to electrolyser capacity, as neither conventional process equipment nor the modifications required for low-carbon production are explicitly represented. Hydrogen-based heat is included as an available low-carbon option in the base industry file.

:::{list-table} Maximum share of non-fossil energy carriers for heating (excludes electricity) in 2030 and 2040.
:name: tab-maximum-share-non-fossil-energy
:header-rows: 1
:widths: 15 6 7 11 6 9 7 7 11 7 9
:column-align: left center center center center center center center center center center

* - Sub-sector
  - {colspan}`10` Maximum share
* -
  - {colspan}`5` **2030**
  - {colspan}`5` **2040**
* -
  - **Bio-fuel**
  - **Bio-mass**
  - **Hydrogen**
  - **Bio-gas**
  - **District Heat**
  - **Bio-fuel**
  - **Bio-mass**
  - **Hydrogen**
  - **Bio-gas**
  - **District Heat**
* - ALUminium
  - 20%
  - \-
  - 20%
  - \-
  - 2%
  - 100%
  - \-
  - 100%
  - \-
  - 4%
* - METallurgical
  - 20%
  - 48%
  - 20%
  - 21%
  - 3%
  - 100%
  - 100%
  - 100%
  - 100%
  - 4%
* - CHEMical
  - 20%
  - 44%
  - 20%
  - 21%
  - 7%
  - 100%
  - 100%
  - 100%
  - 100%
  - 21%
* - WOOD
  - 20%
  - 78%
  - \-
  - \-
  - 5%
  - 100%
  - 100%
  - \-
  - \-
  - 13%
* - MINeral
  - 22%
  - 25%
  - \-
  - \-
  - 3%
  - 100%
  - 100%
  - \-
  - \-
  - 7%
* - CONstruction
  - 29%
  - 11%
  - \-
  - \-
  - 7%
  - 100%
  - 100%
  - \-
  - \-
  - 16%
* - AGRiculture
  - 31%
  - 11%
  - \-
  - \-
  - 4%
  - 100%
  - 21%
  - 50%
  - \-
  - 16%
* - Other
  - 22%
  - 21%
  - \-
  - 20%
  - 18%
  - 100%
  - 100%
  - \-
  - 60%
  - 57%
:::

(sec-process-technologies)=
### Process technologies

The process energy demand (PRC), as described in section {numref}`sec-demand-projection`, represents energy carriers and materials used as direct inputs to industrial production processes. These include coal and coke products used in aluminium production and other metallurgical industries, natural gas used particularly in the chemical industry, and timber used as a raw material in wood-processing industries. Although the use of timber is not considered a CO{sub}`2`-emitting activity, it is included in the model to maintain consistency in the biomass balance and to account for biomass by-products generated by these industries.

IFE-TIMES-Norway includes several alternative process technologies that can reduce industrial carbon emissions when they are economically competitive. These technologies provide alternatives to the use of coal, coke, and natural gas as process inputs in the metallurgical and chemical industries. This chapter describes the representation and assumptions applied to these technology options.

A detailed assessment published by the Norwegian Environment Agency (Miljødirektoratet) in 2022 provides an important basis for the industrial emission-reduction technologies represented in the model {cite}`107`. The modelling focuses on identifying technically relevant low-carbon alternatives for industrial processes. However, the costs and future performance of many emerging process technologies remain highly uncertain.

An overview of possible low-carbon technologies in industry is presented below, and more in-depth information on low-carbon solutions in IFE-TIMES-Norway is described in {cite}`87`. The principal low-carbon process options represented in IFE-TIMES-Norway can be grouped into four categories:

- direct electrification of industrial processes;

- hydrogen-based technologies, which may also be regarded as indirect electrification;

- substitution of fossil coal and coke with bio-coal; and

- CCS.

Some new technologies are only included in one or two of the three industry scenarios (high, medium, and low, see chapter {numref}`sec-demand-projection`).

***Bio-coal***

In silicon production, bio-coal can replace a substantial share of the fossil coal and coke used as reducing agents, thereby reducing fossil CO₂ emissions. According to {cite}`107`, biocarbon could account for up to 80% of the coal and coke inputs by 2050, with an even higher substitution share considered technically possible. Elkem has communicated an ambition to increase the share of biocarbon used in its smelters to 40% by 2030 and to achieve carbon-neutral production by 2050 {cite}`108`.

Bio-coal can also reduce fossil CO₂ emissions from manganese production by replacing fossil coal and coke. The feasible substitution share remains uncertain, but a target of 40% has been reported {cite}`107`.

Based on these sources, IFE-TIMES-Norway initially allows biocarbon to replace up to 40% of the fossil coal and coke used as reducing agents in the production of metals other than aluminium. The maximum substitution share increases to 80% in 2040 and 90% in 2050. These values represent model assumptions regarding the future availability and technical applicability of biocarbon rather than projections of its expected use.

Biomass is already used as a fuel in cement kilns, and its contribution could increase further. In IFE-TIMES-Norway, fossil coal used in cement production is assumed to be fully substitutable with bio-coal.

***Hydrogen***

Hydrogen can be used both as a reducing agent and as a fuel for stationary combustion in metal production. According to {cite}`107`, producing the required hydrogen through electrolysis could increase annual electricity consumption by approximately 0.7 TWh. IFE-TIMES-Norway includes the possibility of replacing coal and coke with hydrogen in metallurgical processes other than aluminium production. This option is available for all relevant plants and represents the interest expressed by industrial facilities, including INEOS Tyssedal, in using renewable hydrogen in their production processes. In the base scenario, hydrogen use for this purpose is limited to producing 1 TWh of energy service demand and becomes available from 2035. A higher level of hydrogen use is permitted in the High Industry scenario, with its deployment determined by the relative costs of the available options.

The choice between hydrogen and other low-carbon alternatives, such as bio-coal and CCS, can be determined endogenously by IFE-TIMES-Norway based on cost optimisation. Alternatively, specific technologies can be imposed through scenario assumptions to represent corporate strategies, policy directives, or other considerations not captured by the model’s techno-economic optimisation. The additional investment costs associated with adapting metallurgical processes to hydrogen are highly uncertain and are not included in the current model version. The earliest year in which hydrogen-based production can be introduced varies by industrial process. Metal production plants other than iron have a later possible start year.

CO₂ emissions from fertiliser production can be reduced by replacing fossil-based hydrogen with hydrogen produced through electrolysis. According to {cite}`107`, this could reduce annual CO₂ emissions by more than 70%, corresponding to approximately 0.8 million tonnes of CO₂ per year. At present, Yara International mainly uses natural gas as an input to ammonia production but has considered electrolysis-based production of hydrogen from electricity and water. In fact, in June 2024, they officially opened their pilot 24 MW green hydrogen plant in Porsgrunn, Norway {cite}`109`. To represent this development in the model, the use of hydrogen in fertilizer production was assumed to have an upper limit of 3.3 TWh from 2030 in the base case but is allowed to grow more in the High Industry Demand scenario, depending on cost.

Methanol production at Tjeldbergodden could be decarbonised through a transition from fossil-based production to green methanol {cite}`107`. IFE-TIMES-Norway includes this transition as an alternative technology pathway, with its deployment determined endogenously based on its cost relative to other available options {cite}`87`.

***Direct electrification***

Several ongoing research and demonstration projects indicate significant potential for the direct electrification of industrial processes. However, many of these technologies remain at an early stage of development. They are therefore included only in the High Industry scenario, as described in {cite}`87`.

Conventional aluminium production consumes carbon anodes, resulting in direct CO₂ emissions. One potential method of avoiding these emissions is to replace conventional carbon anodes with inert anodes. Although research on inert-anode technology has been ongoing for several decades, its future commercial availability remains uncertain. The IEA currently classifies the technology as being at the demonstration stage, corresponding to a technology readiness level of TRL 7. The use of inert anodes is estimated to increase electricity consumption by 10–30% per tonne of aluminium produced. If applied to current Norwegian production volumes, this would correspond to an increase in annual electricity consumption of approximately 4.5 TWh {cite}`107`. Because of the uncertainty surrounding the technology, IFE-TIMES-Norway allows inert anodes to be introduced at only one aluminium plant from 2040 and only in the High Industry scenario. In the base model, the technology is assigned a start year of 2100, which effectively prevents its deployment within the model horizon. To include the technology in an analysis, it must be activated through a scenario file by assigning a start year within the analysed period.

Research is also underway on an alternative aluminium production process based on electrolysis of aluminium chloride, AlCl{sub}`3`. This process also generates CO{sub}`2` emissions if it uses fossil-derived CO as input. However, the resulting CO₂ stream has a high concentration and is produced under controlled process conditions, which could facilitate carbon capture. The use of electricity will increase by 10-20% compared to the present production {cite}`107`. Given the uncertainty surrounding this process, IFE-TIMES-Norway allows it to be introduced at only one aluminium plant, starting in 2040, and only in the High Industry scenario. Here, it is assumed that the CO{sub}`2` emitted is fully captured and reused as input to the process.

The production of silicon can, in principle, be directly electrified, and several relevant research projects on this are ongoing. One proposed silicon production process is based on the use of silicon in a hydrometallurgical process, where it is produced with inert anodes. This process doesn’t use carbon, and the electricity use increases by 60% {cite}`107`. However, this process is considered to be too uncertain to include in IFE-TIMES-Norway for now.

Ongoing projects of direct electrification in the non-metallic mineral industry indicate that some processes can be electrified. One example is the electrification of mineral wool production at Rockwool in Moss {cite}`110`. This was used as a basis for the possibility of increased use of electricity for process and heat demand in MIN.

Research is also underway on the electrification of cement kilns. In addition to replacing fossil-fuel combustion, kiln electrification could increase the concentration of CO₂ in the flue gas and thereby facilitate the capture of process emissions. This technology option is included only in one region in the High Industry scenario.

IFE-TIMES-Norway includes three principal options for supplying energy to the offshore O&G regions:

1.  natural gas supplied from the oil and gas fields at a price 60% below the assumed market price;

2.  electricity supplied from mainland Norway through existing cables; and

3.  investment in new electricity cables connecting the oil and gas regions to either mainland Norway or offshore wind regions.

Investment in new cables for electrification from shore or offshore wind regions is not available before 2030, reflecting the assumed construction and implementation time. Each offshore oil and gas region is connected to one mainland electricity bidding zone and one offshore wind region, selected based on geographical proximity. The cost of the trade cables is based on the maximum distance from all O&G fields within the region to the respective spot and offshore wind region. Economies of scale are also included in the cost of the cables, in which the capacity needed to supply the highest demand throughout the period is assumed. Further details on the distance and cost calculation can be found in the file “Offshore costs” (can be shared by request) and the following [{u}`Map`](https://www.google.com/maps/d/u/0/edit?mid=1R7-6WfvyVf4WhRPW8FgDAYxVLEQ_m0A&ll=57.17025823087536%2C5.107310783440706&z=8).

The cost of offshore electrification includes not only investment in transmission cables and any additional electricity supply capacity, but also the modifications required at the platforms to enable electrification. These modifications may include upgrades to platform electrical systems and the replacement or adaptation of equipment such as compressors.

Based on costs provided by industry partners for real-life cases, an investment cost of 37 500 kNOK/MW is assumed for electrification of offshore O&G regions. For electrification of onshore O&G facilities, a lower cost of 15 000 kNOK/MW is assumed due to lower expenses of installation, personnel, transport of material, etc. Actual electrification costs vary considerably among projects. However, because detailed project-specific data are generally unavailable, uniform cost assumptions are applied across offshore projects and across onshore projects, respectively.
