(sec-ccs-and-daccs)=
# CCS and DACCS

Large point sources in industry plants can be equipped with CCS to reduce emissions. Both fossil and bio-CO{sub}`2` can be captured, but with the present EU ETS scheme {cite}`72`, only fossil CO{sub}`2` is counted. CCS in cement, metal, chemical, and petroleum production is included as a possibility in the SubRES files: SubRES_CCS and SubRES_CCS_Trans, with region-specific data in the Trans-file. Potentials are based on {cite}`76`, {cite}`77`. These files also include CCS in waste incineration in district heating plants (see {numref}`sec-heating-technologies`) and in production of blue hydrogen (see {numref}`sec-with-autothermal-reforming-of-natural-gas-atr`). In some scenarios with moderate technology development, only CCS in waste incineration and planned CCS in cement production are included (SubRES_CCS_NoNew). More information regarding CCS for different industry processes can be found in {cite}`87`.

The cost of CCS is highly uncertain and also largely project-specific. A comprehensive review, comparing investment and operational costs of different reports within Norway, has been carried out to create a better foundation for our assumptions. Process21 {cite}`88` assumed that 3-4 facilities can be operational within 2030 if the right framework conditions are in place, at an estimated investment cost of 11 billion NOK. Operational costs are assumed to be between 0.9-1.2 billion NOK per year, with storage of 1.3-1.6 million tons of CO{sub}`2`. Of these costs, 50% are related to transport and storage (T&S), 30% to energy use, and 20% to capture. Similarly, DNV {cite}`89` estimates the costs of two capture sites, Norcem Brevik (cement) and Fortum Oslo Varme (waste-to-energy), capturing a total of 0.8 Mtpa. The total investment cost for the capture facilities is 7812 MNOK, while T&S is 6405 MNOK. Operational costs are 600 MNOK, in which capture corresponds to about 60% and T&S to about 40%.

Moreover, Vista Analysis and SINTEF {cite}`90` have estimated the investment and operational cost for implementing CCS at specific industry facilities in Norway. Cost of capture is presented for the 19 facilities having the highest investment costs. In total, 46 facilities have been evaluated based on those characterized by the Norwegian Environment Agency as major emission sources for CO{sub}`2`. In contrast to the two other reports, their costs are given for the n{sup}`th` facility and hence assume already learning effects and economies of scale. For the first facility, they assume an increase in investment cost of 65% compared to the n{sup}`th` facility. The assumed investment and operational cost of CO{sub}`2` capture in IFE-TIMES-Norway is based on this report, as the facility specific information allows us to differentiate costs between sectors. The facilities are grouped within cement, metal, aluminium, chemical, petroleum, and waste, and their respective costs are presented in {numref}`tab-capture-rates-investment-costs-90`. We assume the cost of the n{sup}`th` facility in 2035, while the cost of the first facility is assumed for 2025. Electrified cement production gives higher concentrations of CO{sub}`2`, reducing the investment cost for CCS. The relative cost compared to conventional CCS is calculated based on {cite}`91`.

:::{list-table} Capture rates and investment costs {cite}`90` for CCS for different plants.
:name: tab-capture-rates-investment-costs-90
:header-rows: 1
:widths: 26 10 9 12 12 13 14
:column-align: center center center center center center center
:header-align: center

* -
  - {colspan}`3` Capture rates
  - {colspan}`3` Investment costs\
    (NOK/ton CO2)
* - Year:
  - **2025**
  - **2030**
  - **2050**
  - **2020**
  - **2030**
  - **2050**
* - Cement production
  - 0.47
  - 0.47
  - 0.90
  - 8243
  - 4625
  - 4022
* - Cement – electrification process
  -
  - 0.95
  - 0.95
  -
  - 1730
  - 1730
* - Metal production
  - 0.70
  - 0.70
  - 0.80
  - 8243
  - 4625
  - 4022
* - Aluminium production
  - 0.70
  - 0.70
  - 0.80
  - 11677
  - 6551
  - 5697
* - Chemical production
  - 0.70
  - 0.70
  - 0.80
  - 11677
  - 6551
  - 5697
* - Petroleum production
  - 0.70
  - 0.70
  - 0.80
  - 11677
  - 6551
  - 5697
* - Waste incineration
  - 0.67
  - 0.76
  - 0.76
  - 5495
  - 3083
  - 2681
* - Other / Blue hydrogen{sup}`1`
  - 0.95
  - 0.95
  - 0.95
  -
  -
  -
:::

{sup}`1` Cost of ATR technology includes capture cost. Only transport and storage cost of CO2 is included.

For the transport and storage costs, assumptions from DNV are used as they provide the most detailed information about the breakdown of costs {cite}`89`. Costs are differentiated between investments and operations, for both storage and transport, as given in {numref}`tab-investment-operational-energy-cost-transport`. The transport costs are further differentiated based on the distance to the storage site from each of the spot regions, assuming that the storage will be located outside Øygarden. The cost estimates from DNV include the cost of shipping CO{sub}`2` from the capture sites to Øygarden. This is used as the reference cost for NO2, while costs of other regions are scaled based on the kilometre distance to Øygarden. Moreover, CO{sub}`2` is assumed to be further transported by pipeline from Øygarden to the storage site for injection in saline formations. The cost of the pipeline is included in the investment costs.

:::{list-table} Investment and operational (excl. energy) cost of transport and storage of CO2, based on {cite}`89`.
:name: tab-investment-operational-energy-cost-transport
:header-rows: 1
:widths: 26 26 26
:column-align: center center center
:header-align: center

* -
  - CAPEX (NOK/ton CO2)
  - OPEX (NOK/t CO2/y)
* - Storage
  - 6844
  - 209
* - Transport
  - 1163
  -
* - NO1
  -
  - 150
* - NO2
  -
  - 105
* - NO3
  -
  - 72
* - NO4
  -
  - 244
* - NO5
  -
  - 40
:::

Lastly, the potential for CO{sub}`2` storage is limited to 2 Mt in 2035, corresponding to about a doubling of today’s plans for the two capture sites, Norcem Brevik and Fortum Oslo Varme. In 2040, the restriction is set to 10 Mt, based on the projects with licenses in 2030 {cite}`92`. In 2050, all projects with licenses are set to be ready, summing up to 51 Mt. The storage limit is not set to any specific regions, but as a sum of CO{sub}`2` storage capacity for all regions. CCS capacity is linearly interpolated between modelling years and was assumed to remain unchanged after 2050.

Other technical parameters, such as electricity and heat consumption, are based on the Danish Energy Agency’s technology catalogue {cite}`93`. Electricity consumption for CO{sub}`2` capture is assumed to be 0.025 kWh/kg CO{sub}`2` in 2018 and 0.018 kWh/kg CO{sub}`2` in 2050. Heat consumption is assumed to be 0.83 kWh/kg CO{sub}`2` in 2018 and 0.66 kWh/kg CO{sub}`2` in 2050. Moreover, it is assumed that electricity consumption is 0.42 kWh/kg CO{sub}`2` for the transport of CO{sub}`2`.

Direct air capture (DAC) is also included as an alternative for carbon removal. It is included as a possible technology to reduce the remaining emissions in industry, as not all emissions are captured by CCS. This is enabled through a user constraint (UC) by enhancing an upper limit for each industrial subsector, such that e.g., the maximum CO{sub}`2` reduction by DAC in aluminium manufacturing is 20% of the CO{sub}`2` emissions, as CCS can capture up to 80%. The subsectors ALU, MET, CHEM, and MIN have the possibility to use DAC from 2035 in IFE-TIMES-Norway. In addition, general DAC is included, in which emissions from all processes in the model can be removed. For DAC in Industry, it is assumed that waste heat is available, while general DAC is connected to the district heat grid. Otherwise, all model assumptions are the same.

The process is modelled based on technical specifications and cost data from {cite}`94`. The solid sorbent system (Case B) is assumed as it requires temperature levels at 80 °C – 130 °C, which can be met through industrial waste heat. In comparison, liquid solvent systems require heat near 900 °C, for which the report assumes the use of natural gas to obtain the high-temperature heat for the calciner. Moreover, data from case B.1 is used, assuming a heat pump instead of electricity to obtain the necessary temperature. Hence, DAC is modelled as having an input feed of CO{sub}`2`, as well as an auxiliary electricity input. Heat inputs are assumed to be available from industrial processes, presupposing that these are co-located with the DAC plant. Based on the report, it is assumed that DAC entails an electricity consumption of 0.609 kWh/kg (including electricity for the heat pump) and a thermal heat consumption of 1.14 kWh/kg.

The investment cost is estimated at 1589 MUSD for a 1 Mt plant, with OPEX costs at 332 MUSD (2020 values). The operational costs exclude energy costs as these are modelled as separate inputs for the DAC process. In terms of cost reductions, estimates from the International Energy Agency (IEA) are used {cite}`95`. These include cost reductions related to learning by doing (learning rates), economies of scale, and technology spillover. For Solid DAC, it is expected to have a learning rate of about 15%. Notably, feedback from the Norwegian Environment Agency suggests that the uptake proposed by IEA is a bit optimistic, and hence cost reductions from IEA for 2030 are assumed to be realized in 2040. Including all cost reduction factors, the total reduction is assumed to be 62% by 2040 and 80% by 2050. Only reduction in investment costs is assumed, as operational costs are highly dependent on uncertain energy, utilities, and labour market fluctuations. Moreover, a capture rate of 70% is used based on DEA {cite}`93`.
