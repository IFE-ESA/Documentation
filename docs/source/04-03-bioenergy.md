(sec-bioenergy)=
# Bioenergy

In the model, biocoal or biofuel can either be domestically produced from forestry or imported, while other solid biomass fuels can only be sourced domestically from forestry and as a byproduct of the wood/paper industry. Limitations are imposed based on current and projected future use of local resources. The model also includes the production of different kinds of biofuel and biocoal from biomass.

Regional limitations of fuel wood resources felled for direct use for heating in residential buildings are included in the model based on current use. A total of 5.9 TWh/year {cite}`70` is available at a low cost, corresponding to the actual use that, to a large extent, is self-harvesting.

Commercial roundwood felled can be used as raw material in the wood industry (14.23 TWh to sawmills, 12.29 TWh to paper mills {cite}`71`). Biomass can be produced directly from forest resources or as a by-product of sawmills and paper mills. This can consequently be used as chips/pellets in heating plants, fuel for producing heat in industrial facilities, converted to biofuel, or converted to biocoal. The technology data for converting biomass to biofuel or biocoal are presented in {numref}`tab-technology-data-conversion-biomass-biofuel` {cite}`72`.

:::{list-table} Technology data for the conversion of biomass to biofuel or biocoal
:name: tab-technology-data-conversion-biomass-biofuel
:header-rows: 1
:widths: 16 16 16 16 16 16
:column-align: left center center center center center
:header-align: center

* -
  - Efficiency
  - Lifetime (years)
  - Investment cost 2030 (kNOK/MW)
  - Fixed O&M cost (kNOK/MW)
  - Variable O&M cost (kNOK/GWh)
* - Biofuel (1{sup}`st` gen ethanol)
  - 58%
  - 20
  - 8588
  - 751
  - 103
* - Biofuel (biomass gasification to produce methanol)
  - 58%
  - 20
  - 36 169
  - 721
  - 252
* - Jet Biofuel
  - 85%
  - 25
  - 48 148
  - 1279
  - 13
* - Biocoal
  - 25%
  - 30
  - 10 000
  -
  - 41
:::

:::{figure} images/figure-17.png
:name: fig-schematic-overview-biomass-resources-conversion

Schematic overview of biomass resources, conversion processes and end-use.
:::

Various bioenergy products can be produced from domestic raw materials or be imported. In the future, it may be possible to use marine biological resources for the production of various bioenergy products, but this has not been considered here.

Norway has a large biomass reserve related to the forest. In 2025, about 13 million m{sup}`3` were felled for commercial purposes (goes to sawmills and paper mills) {cite}`73`, while fuel wood removals amounted to 2 million m{sup}`3`. All of these logging activities translate to about 37 TWh of forest resources, 26.5 TWh of which are used as inputs to the wood industry. Roundwood harvested that went to sawmills and paper mills amounted to 14.2 TWh and 12.3 TWh, respectively, in 2025. Biomass byproducts from the wood/paper industry currently amount to 0.3 TWh and 6.5 TWh from the paper mills and sawmills, respectively.

Bio resources for energy use (fuelwood from the forest + biomass outputs from wood processing + biomass from the forest) are estimated to be at 17.2 TWh {cite}`71`, {cite}`74`. Roundwood removal is expected to grow by 4 TWh. When timber is felled, there are usually biomass resources left on the felling field that can be used for energy production (GROT). At current felling rates, forestry waste has an estimated energy content of 6 TWh/year. Forestry waste is currently uncollected and unused but can potentially also be utilized in the future. If so, it could add about 7 TWh of bioresources in the future. In addition, collecting manure, straw, and sludge from the agriculture sector can also add 4.8 TWh of bioresources {cite}`74`.

{numref}`tab-summary-norwegian-bioresources-gwh` summarizes the upper limit of potential bioresources available to Norway from 2020 to 2050.

:::{list-table} Summary of Norwegian bioresources, GWh
:name: tab-summary-norwegian-bioresources-gwh
:header-rows: 1
:widths: 38 10 10 10
:column-align: left right right right
:header-align: right

* -
  - 2020
  - 2025
  - 2050
* - Commercial Roundwood
  - 26520{sup}`a`
  - 31069{sup}`d`
  - 35069{sup}`c`
* - Fuelwood
  - 4519{sup}`a`
  - 5880{sup}`b`
  - 5880{sup}`d`
* - Other Biomass directly from forest
  - 0
  - 4499{sup}`d`
  - 8499{sup}`d`
* - GROT + agricultural waste
  - 117
  - 224
  - 11759{sup}`c`
* - Wood to papermills
  - 12287{sup}`a`
  - 12287{sup}`a`
  - 12287{sup}`a`
* - Wood to sawmills
  - 14233{sup}`a`
  - 14233{sup}`a`
  - 14233{sup}`a`
* - Biomass byproduct from papermills
  - 298{sup}`a`
  - 298{sup}`e`
  - 298{sup}`e`
* - Biomass byproduct from sawmills
  - 6541{sup}`a`
  - 6541{sup}`e`
  - 6541{sup}`e`
* - Loss in saw and papermills
  - 50{sup}`d`
  - 50{sup}`e`
  - 50{sup}`e`
:::

*{sup}`a`* {cite}`71`

*{sup}`b`* {cite}`75`

*{sup}`c`* {cite}`74`

*{sup}`d`calculated*

*{sup}`e`assumed unchanged in the base case*

Today's use of biogas is approx. 0.2 TWh, and the potential for increased biogas production in Norway is estimated at 2.7 TWh. A realistic potential is estimated at about 2 TWh and a theoretical one at about 4 TWh {cite}`76`. In {cite}`77`, the potential for biogas is estimated to be at 4 TWh in 2020. *Klimakur* 2030 states the potential for biogas to be between 2.3 and 5 TWh / year {cite}`20`, based on a study by {cite}`78`. This study was used as a basis for dividing the potential into two price classes: 1.2 TWh at a price of 1 NOK/kWh and 1.5 TWh at a price of 2 NOK/kWh {cite}`78`.

In the ”Scen_A_UC” file, the limitation of forest bio-reserve (commercial roundwood removals) is included. The limit is 26.5 TWh in 2018-2020, 31 TWh in 2025, and 35 TWh by 2050, according to the quantity of sustainable felling. Unlike forestry waste, some domestic crop waste is assumed to be currently collected (0.2 TWh). Collection of forestry and agriculture waste was assumed to grow from 0.2 in 2025 to about 11.8 TWh by 2050 (7 TWh GROT, 4.8 TWh agriculture waste).

A limitation of biogas is also added: 0.4 TWh in 2018-2020, increasing to 2.7 TWh in 2030. The production process of biogas is not included in the model yet. Low-cost domestic production of 1{sup}`st` generation ethanol biofuel was assumed to be limited to the current level of crop waste production (0.2 TWh).

The use of municipal waste is limited per region in line with current consumption. It is assumed to remain constant at this level during the modelling horizon due to lack of data. An increased population can argue for increased volumes of waste, but more recycling can reduce the waste available for energy purposes.
