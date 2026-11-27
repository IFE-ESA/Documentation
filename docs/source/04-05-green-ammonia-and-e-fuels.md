(sec-green-ammonia-and-e-fuels)=
# Green ammonia and e-fuels

Various pathways for alternative-fuel production based on renewable energy are emerging as part of the decarbonization efforts in hard-to-abate sectors. These alternative fuel pathways are expected to play a role especially in the transport sector, where high-density fuels are needed. To better represent some of these potential options in specific segments of the transport sector, the model includes processes to represent the production – and eventual use – of ammonia based on green hydrogen and the production of synthetic jet fuel, or e-kerosene, as a potential fuel replacement in aviation.

(sec-green-ammonia)=
## Green ammonia

The option of producing green ammonia (NH{sub}`3`) via Haber-Bosch synthesis for consumption in the maritime sector is included in the model. Ammonia production is modelled as a new process, which uses both hydrogen – produced in centralized plants (H2-CENT) – and electricity as input commodities, each having input shares of 95% and 5%, respectively. Electricity consumption represents both the required inputs for air separation, which provides the nitrogen feed for ammonia production, and auxiliary electricity consumption in the production plant. The production output has an 82% efficiency and an assumed availability factor of 92%. In addition to the input shares and overall output efficiency, the investment costs (including investment costs for air separation) and operation and maintenance costs are gathered from the Danish Energy Agency’s Technology data catalogue for renewable fuels {cite}`85`. The parameters and cost assumptions specified for the ammonia production process are presented in {numref}`tab-values-used-model-green-ammonia`.

:::{list-table} Values used to model green ammonia production, calculated based on {cite}`85`.
:name: tab-values-used-model-green-ammonia
:header-rows: 1
:widths: 39 14 15 15 15
:column-align: left center center center center
:header-align: center

* -
  - {colspan}`4` Values
* - Year:
  - **2020**
  - **2030**
  - **2040**
  - **2050**
* - Investment costs (kNOK/GWh)

    (incl. costs for air separation)
  - 2145
  - 1717
  - 1405
  - 1066
* - Fixed O&M (% of inv. Costs)
  - {colspan}`4` 3%
* - Variable costs (kNOK/GWh)
  - {colspan}`4` 0.2
* - Lifetime (years)
  - {colspan}`4` 30
* - Efficiency
  - {colspan}`4` 82%
* - Aux. electricity (input shares)
  - {colspan}`4` 5%
:::

(sec-synthetic-jet-fuel-e-kerosene)=
## Synthetic jet fuel (E-kerosene)

The production of e-kerosene is modelled as a new process representing a Fischer-Tropsch synthesis plant, available from 2030. The required inputs are green hydrogen (from centralized production, i.e., H2-CENT), electricity, and CO{sub}`2` from direct air capture. The output of this process provides a representation of the total e-fuel liquid volumes. An additional process is included to define the share that is upgraded to e-kerosene, which can be used as a commodity to cover energy demands in aviation. There is also a possibility to export the synthetic fuel, but this is not included in the base version of the model. A representation of the process and commodity flows is presented in {numref}`fig-simplified-res-diagram-synthetic-jet`.

:::{figure} images/figure-20.png
:name: fig-simplified-res-diagram-synthetic-jet

Simplified RES diagram of the synthetic jet fuel production system in IFE-TIMES-Norway.
:::

The technical specifications and cost data used to model the production of e-kerosene come from the DEA’s Technical Data for Renewable Fuels {cite}`86`. A summary of the data assumptions is presented in {numref}`tab-values-used-model-e-kerosene`.

:::{list-table} Values used to model e-kerosene production, calculated based on {cite}`86`.
:name: tab-values-used-model-e-kerosene
:header-rows: 1
:widths: 46 28 24
:column-align: left center center

* -
  - {colspan}`2` Values
* - Year:
  - **2030**
  - **2050**
* - Investment costs (kNOK/MW)
  - 18716
  - 10528
* - Fixed O&M
  - 898
  - 526
* - Variable costs
  - 299
  - 150
* - Lifetime (years)
  - {colspan}`2` 25
* - Lead time (years)
  - {colspan}`2` 2
* - Input shares (per GWh of e-fuel output)
  - {colspan}`2`
* - Hydrogen (GWh)
  - 1.42
  - 1.33
* - Electricity (GWh)
  - 0.01
  - 0.01
* - CO2 consumption (kt/GWh e-fuel output)
  - 0.309
  - 0.262
* - Availability factor
  - {colspan}`2` 91.3%
* - Kerosene upgrading, efficiency
  - {colspan}`2` 60%
:::
