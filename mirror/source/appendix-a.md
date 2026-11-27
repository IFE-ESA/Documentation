# **Appendix A – Basis for input values for electrolyzer**

Hydrogen from electrolyser is assumed to be produced in each region either centralized or distributed manner. The costs are provided both for alkaline and PEM electrolyser and necessary compressor unit to compress it to 250 bar pressure.

The centralized unit is based on costs expected from a 20 MW{sub}`el` installed capacity while costs for the decentralized unit are based on a 3 MW{sub}`el` size electrolyser.

The costs are composed from three parts: electrolyser, compressor skid and other costs. The costs of electrolyser is taken from {cite}`163` and represents costs for the electrolyser and necessary auxiliaries such as:

- Transformer(s), rectifier(s), control panel with PLC;

- Water demineralizer/deionizer;

- Electrolyser stack(s);

- Gas analysers, separators and separating vessels;

- Scrubber or gas purifier system & recirculating pump;

An important distinction between PEM and Alkaline electrolysers is the output pressure. The traditional Alkaline electrolysers work usually at atmospheric pressure, while some electrolyser designs provide self-pressurization up to 30 bar. On the other side PEM systems can self-pressurize the hydrogen for up to 80 bar in commercial products {cite}`164`. In TIMES, the cost of Alkaline electrolyser is included a dry piston compressor which provides 15 bar output pressure, while the output pressure for PEM is assumed to be 55 bar.

The costs for compressor is based on a cost per installed kW capacity based on data from {cite}`165` and refined in {cite}`84`. The required compressor capacity to reach the set pressure is based on adiabatic compression defined as

:::{list-table}
:widths: 26 61 9

* -
  - $$W = \left\lbrack \frac{\gamma}{\gamma - 1} \right\rbrack*P_{0}*V_{0}*\left\lbrack \left( \frac{P}{P_{0}} \right)^{\frac{\gamma - 1}{\gamma}} - 1 \right\rbrack.$$
  - (A-1)
:::

Where *P{sub}`0`* is the initial pressure (Pa), *V{sub}`0`* is the initial specific volume (m{sup}`3`/kg), *P* is the end pressure (Pa), and *γ*=1,41 is the adiabatic coefficient {cite}`166`. In addition, a mechanical efficiency of 70% is added and a compressor redundancy is set to 3 x 50%.

The other cost consists of {cite}`167`:

1.  Engineering costs

2.  Distributed Control System (DCS) and Energy Management Unit (EMU)

3.  Interconnection, commissioning, and start-up costs

The other costs are expected to follow scale of economy; hence they are assumed to be 45% and 36% of CAPEX for 3 MW{sub}`el` and 20 MW{sub}`el` electrolyzer unit respectively.

Civil work costs are not included, which are here defined as construction of foundation, industrial buildings, lighting, water supply, fencing, security. Neither cost of land nor the option to extend the technical lifetime of the electrolyzer by only replacing the stack has been included in the model.

The development of costs is expected to decrease with time and are usually correlated with increased production volumes of the equipment. The reduction in price of electrolyser is presented in {cite}`164` as a span between a max and minimum costs per kW{sub}`el`. As current investment costs are based on a separate publication and are differentiated on size of the plant, only the trends of future costs are used. In IFE-TIMES-Norway the cost development is based on the trend of the average costs. All the electrolyser costs and expected reduction is shown in Table A-1.

:::{list-table} Cost span of electrolysers from {cite}`164` and price reduction for the average cost.
:name: tab-cost-span-electrolysers-164-price
:header-rows: 1
:widths: 18 15 10 10 12 10 10 12

* -
  -
  - {colspan}`3` Alkaline
  - {colspan}`3` PEM
* -
  -
  - Today
  - 2030
  - Long-term
  - Today
  - 2030
  - Long-term
* - Upper
  - USD{sub}`2019`/kW{sub}`el`
  - 1400
  - 850
  - 700
  - 1800
  - 1500
  - 900
* - Lower
  - USD{sub}`2019`/kW{sub}`el`
  - 500
  - 400
  - 200
  - 1100
  - 650
  - 200
* - Average
  - USD{sub}`2019`/kW{sub}`el`
  - 950
  - 625
  - 450
  - 1450
  - 1075
  - 550
* - Price reduction average price
  - \-
  - 0%
  - 34%
  - 53%
  - 0%
  - 26%
  - 62%
:::

The cost development of compressor is based on cost decrease factors presented in {cite}`83` where it is assumed that at production of 5 000 hydrogen refuelling stations (HRS) the hydrogen compressor could decrease with 53% and at production volume of 10 000 hydrogen refuelling stations (HRS) the decrease will be 60%. These production volumes are assumed to occur in 2030 and 2050 respectively and to represent also the reduction in compressor costs for middle and large-scale hydrogen production unit. It shall be noted that there are big technological differences between a compressor serving light-duty vehicle HRS (as referred to in the source) and large-scale hydrogen production unit, in addition prediction in future cost development is in general connected to large uncertainties.

In Table A-2 the cost used for each component (electrolyser, compressor and other costs) are presented, while Table A-3 summarises the cost breakdown for the central compressor.

:::{list-table} The cost for the different electrolysers for different years shown in NOK per kW{sub}`H2`. Compressor for decentralized production is added to the total electrolyser cost.
:name: tab-cost-electrolysers-years-shown-nok
:header-rows: 1
:widths: 10 10 22 10 10 10
:column-align: center center center center center center
:header-align: center

* -
  -
  -
  - 2018
  - 2030
  - 2050
* - {rowspan}`6` 20 MW el
  - {rowspan}`3` PEM
  - Electrolyser -
  - 12769
  - 8383
  - 3985
* - Other costs
  - 4597
  - 3018
  - 1435
* - **Total costs**
  - **17366**
  - **11401**
  - **5419**
* - {rowspan}`3` Alkaline
  - Electrolyser -
  - 8572
  - 5515
  - 3600
* - Other costs -
  - 3086
  - 1985
  - 1296
* - **Total costs**
  - **11658**
  - **7500**
  - **4896**
* - {rowspan}`8` 3 MW el
  - {rowspan}`4` PEM
  - Electrolyser -
  - 13585
  - 8918
  - 4239
* - Compressor
  - 2431
  - 1142
  - 972
* - Other costs
  - 7207
  - 4527
  - 2345
* - **Total costs**
  - **23222**
  - **14588**
  - **7557**
* - {rowspan}`4` Alkaline
  - Electrolyser -
  - 10158
  - 6535
  - 4266
* - Compressor
  - 3474
  - 1633
  - 1389
* - Other costs
  - 6134
  - 3676
  - 2545
* - **Total costs**
  - **19765**
  - **11843**
  - **8201**
:::

:::{list-table} The cost of centralized (large-scale) compression for different years shown in NOK per kW{sub}`H2`.
:name: tab-cost-centralized-large-scale-compression
:header-rows: 1
:widths: 15 9 9 7
:column-align: center center center center
:header-align: center

* -
  - 2018
  - 2030
  - 2050
* - Compressor
  - 2702
  - 1270
  - 1081
* - Other
  - 973
  - 457
  - 389
* - Total costs
  - **3674**
  - **1727**
  - **1470**
:::

The efficiency consists of two parts: i) the actual efficiency of the electrolyser and ii) the electricity required to compress the hydrogen up to previously mentioned pressure and including the mechanical inefficiency. The values of efficiency for each part and the summarized value of efficiency used in IFE-TIMES-Norway is shown in Table A-4. An interval of efficiency of the electrolyser is provided by {cite}`164` and in IFE-TIMES-Norway is used the middle value.

:::{list-table} Efficiency of electrolyzer, compression stage and the summarized efficiency used in IFE-TIMES-Norway
:name: tab-efficiency-electrolyzer-compression-stage-summarized
:header-rows: 1
:widths: 26 10 10 10 10 10 10 10
:column-align: center center center center center center center center
:header-align: center

* -
  -
  - {colspan}`3` Alkaline
  - {colspan}`3` PEM
* -
  -
  - Today
  - 2030
  - Long-term
  - Today
  - 2030
  - Long-term
* - {rowspan}`3` Efficiency of electrolyzer
  - Upper
  - 70%
  - 71%
  - 80%
  - 60%
  - 68%
  - 74%
* - Lower
  - 63%
  - 65%
  - 70%
  - 56%
  - 63%
  - 67%
* - Middle
  - 67%
  - 68%
  - 75%
  - 58%
  - 66%
  - 71%
* - Energy lost during compression as share of the energy in the compressed hydrogen
  - kWhel/ kWhH2
  - 4.4%
  - 4.4%
  - 4.4%
  - 1.9%
  - 1.9%
  - 1.9%
* - Summarized
  -
  - 64%
  - 66%
  - 72%
  - 57%
  - 64%
  - 69%
:::

The yearly OPEX costs for each component and a complete cost for the entire electrolyzer unit are shown in Table A-5.

:::{list-table} Assumed OPEX costs
:name: tab-assumed-opex-costs
:header-rows: 1
:widths: 32 18
:column-align: center center
:header-align: center

* - Equipment
  - Share of CAPEX
* - Electrolyzer
  - 3%
* - H2 compressor
  - 6%
:::

An expected range of lifetime of the electrolyzer today and in future is presented in {cite}`164`, the range and a middle value, which is used in IFE-TIMES-Norway, is shown in Table A-6.

:::{list-table} Assumed lifetime of electrolyzer stack in hours, differentiated by electrolyzer type and time of production {cite}`164`.
:name: tab-assumed-lifetime-electrolyzer-stack-hours
:header-rows: 1
:widths: 11 11 12 14 9 12 12
:column-align: center center center center center center center
:header-align: center

* -
  - {colspan}`3` Alkaline
  - {colspan}`3` PEM
* -
  - **Today**
  - **2030**
  - **Long-term**
  - **Today**
  - **2030**
  - **Long-term**
* - Upper
  - 90 000
  - 100 000
  - 150 000
  - 90 000
  - 90 000
  - 150 000
* - Lower
  - 60 000
  - 90 000
  - 100 000
  - 30 000
  - 60 000
  - 100 000
* - Middle
  - 75 000
  - 95 000
  - 125 000
  - 60 000
  - 75 000
  - 125 000
:::
