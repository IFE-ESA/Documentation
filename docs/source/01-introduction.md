(sec-introduction)=
# Introduction

IFE-TIMES-Norway is a long-term optimisation model of the Norwegian energy system implemented using TIMES, The Integrated MARKAL-EFOM System, through the VEDA interface. Development of the Norwegian energy system model TIMES-Norway began in 2017 as a collaboration between the Norwegian Water Resources and Energy Directorate (NVE) and the Institute for Energy Technology (IFE). Since then, the model has been further developed and updated through several research and analysis projects.

The development initiated in 2017 involved restructuring and updating earlier versions of TIMES-Norway that had been implemented using a different user interface, ANSWER. The first version of TIMES-Norway was completed in 2009 and was based on MARKAL-Norway, which had been under development since 1990. MARKAL is the predecessor of the TIMES modelling framework. NVE and IFE subsequently developed TIMES-Norway in different directions to address their respective modelling needs. The version developed and maintained by IFE is referred to as IFE-TIMES-Norway.

The TIMES modelling framework has been developed over several decades within the Energy Technology Systems Analysis Program (ETSAP), an International Energy Agency (IEA) Technology Collaboration Programme {cite}`1`. TIMES has a modular structure and is implemented using the General Algebraic Modelling System (GAMS). GAMS translates the TIMES model database into a linear programming matrix and submits it to an optimisation solver. The solver identifies a cost-optimal solution and generates the corresponding model results. The IFE-TIMES-Norway model utilizes the VEDA user interface, which is developed and maintained by KanOrs {cite}`2`.

TIMES is a bottom-up modelling framework that provides a detailed techno-economic representation of resources, energy carriers, conversion technologies and energy demand. A TIMES model identifies the combination of investments and operational decisions that minimises the total discounted cost of supplying energy services across the modelled regions and time horizon, subject to the specified technical, economic, environmental, and policy constraints. The total energy system cost includes investments in energy-supply and end-use technologies, operation and maintenance costs, the cost of electricity imported from countries outside the model, and revenues from electricity exports {cite}`3`, {cite}`4`, {cite}`5`.

IFE-TIMES-Norway is a technology-rich model of the Norwegian energy system divided into five regions corresponding to the current electricity market spot price areas. The model provides operational and investment decisions from the starting year, 2018, towards 2050, with model periods for every fifth year from 2020 within this model horizon. To capture operational variations in energy generation and end-use, each model period is divided into 96 sub-annual time slices. These consist of four seasons, each represented by a 24-hour day. Different sub annual time slice levels are also optionally available.

The model contains a detailed representation of energy end use, with demands for energy services divided into numerous categories within the industrial, building, and transport sectors. Note that energy services refer to the services provided by consuming a fuel and not the fuel consumption itself. For example, the heating demand in buildings is an energy service while the fuel used to heat the building is not. Each energy service demand category can be met by existing and new technologies using different energy carriers such as electricity, bioenergy, district heating, hydrogen, and fossil fuels. Other input data include fuel prices: electricity prices in countries with transmission capacity to Norway, profiles for renewable resources, technical resource potentials, and technology-specific characteristics such as costs, efficiencies, lifetime, availability, and learning curves.

This report describes the status of IFE-TIMES-Norway by September 2026 and is an update of the report from 2024 {cite}`6`. It is primarily intended for modellers familiar with the TIMES vocabulary, and the objective is to describe the model’s current structure, assumptions, input data, and technological representation. A schematic view of general TIMES inputs and outputs is presented in {numref}`fig-schematic-times-inputs-outputs`. How this is applied to IFE-TIMES-Norway is presented in {numref}`fig-schematic-ife-times-norway`.

:::{figure} images/figure-01.png
:name: fig-schematic-times-inputs-outputs

Schematic of TIMES inputs and outputs.
:::

:::{figure} images/figure-02.png
:name: fig-schematic-ife-times-norway

Schematic of IFE-TIMES-Norway.
:::
