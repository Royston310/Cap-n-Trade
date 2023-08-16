# -*- coding: utf-8 -*-


# Cap-and-Trade
### Does it work and how should it be implemnted


# Introduction

Industry till last decade was purely driven by monetary gains. This lead to immense cost cutting and adoption of unsustainable and harmful processes to the environment.

However, the growing awareness and support toward more sustainable policies to encourage industries limit their carbon footprint has pushed governments to adopt policies. The major greenhouse gas reduction policy approaches under consideration fall into three main categories: carbon pricing, technology subsidies, and performance standards.

These aims to penalise industries for their footprint and regulate pollution.

Many countries are ideating and implementing such policies with the European Union being the leader for this change.

## Carbon Pricing
The phrase put a price on carbon has now become well known with momentum growing among countries and business to put a price on carbon pollution as a means of bringing down emissions and drive investment into cleaner options.

So what is meant by putting a price on carbon, and why do modern world really want to implement these prices?

There are several paths governments can take to price carbon, all leading to the same result. They begin to capture what are known as the external costs of carbon emissions – costs that the public pays for in other ways, such as damage to crops and health care costs from heat waves and droughts or to property from flooding and sea level rise – and tie them to their sources through a price on carbon.

A price on carbon helps shift the burden for the damage back to those who are responsible for it, and who can reduce it. Instead of dictating who should reduce emissions where and how, a carbon price gives an economic signal and polluters decide for themselves whether to discontinue their polluting activity, reduce emissions, or continue polluting and pay for it. In this way, the overall environmental goal is achieved in the most flexible and least-cost way to society. The carbon price also stimulates clean technology and market innovation, fuelling new, low-carbon drivers of economic growth.

#### There are two main types of carbon pricing:
1) Cap-and-Trade System

2) Carbon Taxes


**Cap-and-Trade system** – system limits overall greenhouse gas emissions and enables low-emission companies to sell surplus allowances to higher polluters. A market price for greenhouse gas emissions is established by a cap and trade system by generating supply and demand for emissions allowances. The cap aids in ensuring that the necessary emission cuts will occur in order to keep all emitters collectively within their pre-allocated carbon budget.

**Carbon Tax** - By establishing a tax rate on greenhouse gas emissions or, more frequently, on the carbon content of fossil fuels, a carbon tax immediately establishes a price on carbon. A carbon tax differs from a cap and trade because the carbon price is pre-determined, but the emission reduction result is not.


## Cap and Trade

European Union uses a Cap and Tax model to impose carbon tax. The government sets a upper limit or capacity of carbon emmissions an industry can do based on demand, importance to economy and many other factors. The rights of these emissions are then sold and traded among the players in the industry. The players can use these rights or trade them to other players in case of excess.

The goal is to gradually decrease the overall emissions of the industry by encouraging industries to switch to environmentally friendly processes.


---
# Motivation
Through this project, we wish to understand
1. Does cap-and-trade reduce carbon emissions
2. What are the factors and policies that ensure competitive markets
3. What is the extent of restrictions an industry can sustain

The decisions expected from the government are:
1. Capacity allocated to a industry
2. What should be the price of unit carbon emission

The decisions ecxpected from the manufacturers are:
1. Purchasing of carbon emission rights
2. Extent of expenditure on innovation

### Anticipated Behaviour
If the governments sets a limit lower than required the industries would decline and the sector would become incompetant and decline. On the other hand, high capacities would bring little change and innovation.

As rights are traded the prices would gradually increase as industries demands would keep growing in a thriving economy. As manufacturers need to produce to a break even point to survive, larger players might push smaller players out of the market. This brings the question that is regulation on allocation necessary or is open market better.

---
## Model
These decisions have huge impact on the economy and modelling such systems allow us to anticipate them.

The agents in this model are
1. Government or Regulatory body
2. Manufacturers in the Industry

Every period the government would determine the
1. capacity for that period
3. reitrate price for carbon emissions

while, every period manufacturers would
1. decide quality of emissions to purchase based on budget
2. percentage of profits to be used on innovation

Quality produced is directly proportional to Emissions

The manufacturers would try to meet the demand in every period. If they fail to produce break even point they would go bankrupt and exit the market.

Open markets would periodically drive up the emission prices until smaller players exit the market. Government would require to control.
"""

import math
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def innovation_func(x : int):
    return math.log(x/50 + 1)/10
    # return 1/(1+math.exp(-x/1000 + 0))

n = 10000
x_coords = list(range(n))
y_coords = list(innovation_func(x) for x in x_coords)

plt.figure(figsize=(10, 5))
sns.lineplot(x=x_coords, y=y_coords)
plt.grid()
plt.title('Innovation Function', fontdict={'fontsize':20})
plt.xlabel('Expenditure on Innovation', fontdict={'fontsize':15})
plt.ylabel('production efficency improvement', fontdict={'fontsize':15})
plt.show()

def demand_curve(x : int):
    return 25 - x/100

n = 2500
x_coords = list(range(n))
y_coords = list(demand_curve(x) for x in range(n))

plt.figure(figsize=(10, 5))
sns.lineplot(x=x_coords, y=y_coords)
plt.grid()
plt.title('Demand Curve', fontdict={'fontsize':20})
plt.xlabel('Quantity Produced', fontdict={'fontsize':15})
plt.ylabel('Market Price', fontdict={'fontsize':15})
plt.show()

class Manufacturer:
    # Percentage of revenue retained for production
    percentage_retained = 0.10

    # Efficiency of the plant
    a = 1.00
    e = 1.00
    exp_innov = 0

    unit_inv = 5

    wt_carbon = 0.75
    wt_innov = 1.25

    def __init__(self, production_target : int):
        self.production_target = production_target
        # Initial supply is the optimal levels before carbon policies were implemented

        self.supply = production_target


    def production_cycle(self, market_price : float, del_c : float, allocated_quota : int):
        self.revenue = int(market_price * self.supply)
        self.working_capital = int(self.revenue * self.percentage_retained)

        self.supply = int(allocated_quota/(self.a * self.e))

        self.carbon_emm = allocated_quota
        self.carbon_exp = 0

        while (self.supply < self.production_target) and (self.working_capital > 0):

            # Gain by marginally investing in innovation
            del_e = innovation_func(self.exp_innov + self.unit_inv) - innovation_func(self.exp_innov)
            del_innov = (allocated_quota * del_e)/(self.a * (self.e - del_e) * self.e)

            # Gain by marginally investing in carbon bond
            del_carbon = del_c/(self.a * self.e)

            if self.wt_carbon * del_carbon > self.wt_innov * del_innov:
                allocated_quota += del_carbon
                self.carbon_emm += del_carbon
                self.carbon_exp += self.unit_inv
            else:
                self.e -= del_e
                self.exp_innov += self.unit_inv

            self.working_capital -= self.unit_inv
            self.supply = int(allocated_quota/(self.a * self.e))

class Government:
    # amount of carbon credits per unit investment
    del_c = 0.5
    percent_reduction_del_c = 0.05

    # decrease in allocation quota
    del_q = 0.025

    acceptable_p_reduce = -0.2
    acceptable_c_growth = 0.00
    to_reduce = True
    look_back = 6

    supply_data = []
    carbon_emm_data = []

    sw_wt_prod = 1.5
    sw_wt_carb = 1

    def market_regulation(self, total_supply : int, total_carbon_emm : int):

        self.supply_data.append(total_supply)
        self.carbon_emm_data.append(total_carbon_emm)

        if len(self.supply_data) > self.look_back:

            percent_del_p = (self.supply_data[-1] - self.supply_data[-(self.look_back+1)])/self.supply_data[-(self.look_back+1)]
            if percent_del_p < self.acceptable_p_reduce:
                self.to_reduce = False
            else:
                self.to_reduce = True

            del_exp_c = self.carbon_emm_data[-1] - self.carbon_emm_data[-2]
            if del_exp_c > self.acceptable_c_growth:
                self.del_c = self.del_c * (1 - self.percent_reduction_del_c)

        self.social_welfare = self.sw_wt_prod*total_supply - self.sw_wt_carb*total_carbon_emm

def visulaise_dict(data : dict, title : str = '', ylabel : str = ''):
    df = pd.DataFrame(data)
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df)
    plt.title(title, fontdict={'fontsize':20})
    plt.xlabel('Time', fontdict={'fontsize':15})
    plt.ylabel(ylabel, fontdict={'fontsize':15})
    plt.grid()
    plt.show()

NUM_MANUFACTURERS = 5
NUM_PERIODS = 40

policy_social_welfare_data = {f'Allocation Policy {num}' : None for num in range(3)}
policy_market_price_data = {f'Allocation Policy {num}' : None for num in range(3)}

"""When everyone is given less than requested"""

# INITIALISE THE ENVIRONMENT

government = Government()

manufacturers = []
total_production_target = 0
for num in range(NUM_MANUFACTURERS):
    production_target = 100*num + 100 # range [100, 500]
    total_production_target += production_target

    manufacturer = Manufacturer(
        production_target = production_target,
    )
    manufacturers.append(manufacturer)


# Initial Market Conditions
market_price = demand_curve(total_production_target)


# Data Collection
supply_data = {f'Manufacturer {num}' : [] for num in range(len(manufacturers))}
innovation_data = {f'Manufacturer {num}' : [] for num in range(len(manufacturers))}
carbon_emm_data = {f'Manufacturer {num}' : [] for num in range(len(manufacturers))}
carbon_exp_data = {f'Manufacturer {num}' : [] for num in range(len(manufacturers))}

market_price_data = []
carbon_prod_data = []
social_welfare_data = []


# ALLOCATION POLICY
# Everyone is allocated less than what they demanded
allocation_arr = [max(int(manufacturer.production_target * (1 - government.del_q)), 0) for manufacturer in manufacturers]
for num, manufacturer in enumerate(manufacturers):
    manufacturer.allocated_quota = allocation_arr[num]


# SIMULATION
for period in range(NUM_PERIODS):

    market_price_data.append(market_price)
    carbon_prod_data.append(government.del_c)

    # ALLOCATION CHANGE
    if government.to_reduce:
        allocation_arr = [max(int(allocation_arr[num] * (1 - government.del_q)), 0) for num in range(NUM_MANUFACTURERS)]

    # PRODUCTION CYCLE
    total_supply = 0
    total_carbon_emm = 0

    for num, manufacturer in enumerate(manufacturers):
        manufacturer.production_cycle(
            market_price = market_price,
            del_c = government.del_c,
            allocated_quota = allocation_arr[num],
        )

        total_supply += manufacturer.supply
        total_carbon_emm += manufacturer.carbon_emm

        # Extracting data
        supply_data[f'Manufacturer {num}'].append(manufacturer.supply)
        innovation_data[f'Manufacturer {num}'].append(manufacturer.exp_innov)
        carbon_emm_data[f'Manufacturer {num}'].append(manufacturer.carbon_emm)
        carbon_exp_data[f'Manufacturer {num}'].append(manufacturer.carbon_exp)

    # MARKET CORRECTION
    market_price = demand_curve(total_supply)

    # REGULATORY ACTION
    government.market_regulation(
        total_supply = total_supply,
        total_carbon_emm = total_carbon_emm,
    )

    social_welfare_data.append(government.social_welfare)

visulaise_dict(supply_data, 'Supply', 'Production')
visulaise_dict(innovation_data, 'Innovation Spending', 'Innovation Expenditure')
visulaise_dict(carbon_emm_data, 'Carbon Emissions', 'Emission')
visulaise_dict(carbon_exp_data, 'Periodic Carbon Permit Spending', 'Carbon Expenditure')

plt.figure(figsize=(10, 5))
plt.plot(market_price_data)
plt.title('Market Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.grid()
plt.show()


plt.figure(figsize=(10, 5))
plt.plot(carbon_prod_data)
plt.title('Carbon credits per unit investment')
plt.xlabel('Time')
plt.ylabel('Delta Carbon')
plt.grid()
plt.show()
plt.show()

plt.figure(figsize=(10, 5))
plt.plot(social_welfare_data)
plt.title('Social Welfare')
plt.xlabel('Time')
plt.ylabel('Social Welfare')
plt.grid()
plt.show()
plt.show()

policy_social_welfare_data['Allocation Policy 0'] = social_welfare_data
policy_market_price_data['Allocation Policy 0'] = market_price_data
max(social_welfare_data), max(market_price_data)

"""When smaller manufacturer demands are satisfied first"""

# INITIALISE THE ENVIRONMENT

government = Government()

manufacturers = []
total_production_target = 0
for num in range(NUM_MANUFACTURERS):
    production_target = 100*num + 100 # range [100, 500]
    total_production_target += production_target

    manufacturer = Manufacturer(
        production_target = production_target,
    )
    manufacturers.append(manufacturer)


# Initial Market Conditions
market_price = demand_curve(total_production_target)


# Data Collection
supply_data = {f'Manufacturer {num}' : [] for num in range(len(manufacturers))}
innovation_data = {f'Manufacturer {num}' : [] for num in range(len(manufacturers))}
carbon_emm_data = {f'Manufacturer {num}' : [] for num in range(len(manufacturers))}
carbon_exp_data = {f'Manufacturer {num}' : [] for num in range(len(manufacturers))}

market_price_data = []
carbon_prod_data = []
social_welfare_data = []


# SIMULATION
num_red = 0
for period in range(NUM_PERIODS):

    market_price_data.append(market_price)
    carbon_prod_data.append(government.del_c)

    # ALLOCATION POLICY
    # Smaller players are given more
    if government.to_reduce:
        num_red += 1
        allocation_arr = [int(max(100 + 100*num*(1.5*((1-government.del_q)**num_red) - 0.5), 0)) for num in range(NUM_MANUFACTURERS)]

    # PRODUCTION CYCLE
    total_supply = 0
    total_carbon_emm = 0

    for num, manufacturer in enumerate(manufacturers):
        manufacturer.production_cycle(
            market_price = market_price,
            del_c = government.del_c,
            allocated_quota = allocation_arr[num],
        )

        total_supply += manufacturer.supply
        total_carbon_emm += manufacturer.carbon_emm

        # Extracting data
        supply_data[f'Manufacturer {num}'].append(manufacturer.supply)
        innovation_data[f'Manufacturer {num}'].append(manufacturer.exp_innov)
        carbon_emm_data[f'Manufacturer {num}'].append(manufacturer.carbon_emm)
        carbon_exp_data[f'Manufacturer {num}'].append(manufacturer.carbon_exp)

    # MARKET CORRECTION
    market_price = demand_curve(total_supply)

    # REGULATORY ACTION
    government.market_regulation(
        total_supply = total_supply,
        total_carbon_emm = total_carbon_emm,
    )

    social_welfare_data.append(government.social_welfare)

visulaise_dict(supply_data, 'Supply', 'Production')
visulaise_dict(innovation_data, 'Innovation Spending', 'Innovation Expenditure')
visulaise_dict(carbon_emm_data, 'Carbon Emissions', 'Emission')
visulaise_dict(carbon_exp_data, 'Periodic Carbon Permit Spending', 'Carbon Expenditure')

plt.figure(figsize=(10, 5))
plt.plot(market_price_data)
plt.title('Market Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.grid()
plt.show()


plt.figure(figsize=(10, 5))
plt.plot(carbon_prod_data)
plt.title('Carbon credits per unit investment')
plt.xlabel('Time')
plt.ylabel('Delta Carbon')
plt.grid()
plt.show()
plt.show()

plt.figure(figsize=(10, 5))
plt.plot(social_welfare_data)
plt.title('Social Welfare')
plt.xlabel('Time')
plt.ylabel('Social Welfare')
plt.grid()
plt.show()
plt.show()

policy_social_welfare_data['Allocation Policy 1'] = social_welfare_data
policy_market_price_data['Allocation Policy 1'] = market_price_data
max(social_welfare_data), max(market_price_data)

"""Largest players are satisfied completely"""

# INITIALISE THE ENVIRONMENT

government = Government()

manufacturers = []
total_production_target = 0
for num in range(NUM_MANUFACTURERS):
    production_target = 100*num + 100 # range [100, 500]
    total_production_target += production_target

    manufacturer = Manufacturer(
        production_target = production_target,
    )
    manufacturers.append(manufacturer)


# Initial Market Conditions
market_price = demand_curve(total_production_target)


# Data Collection
supply_data = {f'Manufacturer {num}' : [] for num in range(len(manufacturers))}
innovation_data = {f'Manufacturer {num}' : [] for num in range(len(manufacturers))}
carbon_emm_data = {f'Manufacturer {num}' : [] for num in range(len(manufacturers))}
carbon_exp_data = {f'Manufacturer {num}' : [] for num in range(len(manufacturers))}

market_price_data = []
carbon_prod_data = []
social_welfare_data = []


# SIMULATION
num_red = 0
for period in range(NUM_PERIODS):

    market_price_data.append(market_price)
    carbon_prod_data.append(government.del_c)

    # ALLOCATION POLICY
    # Larger players are given more
    if government.to_reduce:
        num_red += 1
        allocation_arr = [int(max(100*num + 100*(3*((1-government.del_q)**num_red)-2), 0)) for num in range(NUM_MANUFACTURERS)]

    # PRODUCTION CYCLE
    total_supply = 0
    total_carbon_emm = 0

    for num, manufacturer in enumerate(manufacturers):
        manufacturer.production_cycle(
            market_price = market_price,
            del_c = government.del_c,
            allocated_quota = allocation_arr[num],
        )

        total_supply += manufacturer.supply
        total_carbon_emm += manufacturer.carbon_emm

        # Extracting data
        supply_data[f'Manufacturer {num}'].append(manufacturer.supply)
        innovation_data[f'Manufacturer {num}'].append(manufacturer.exp_innov)
        carbon_emm_data[f'Manufacturer {num}'].append(manufacturer.carbon_emm)
        carbon_exp_data[f'Manufacturer {num}'].append(manufacturer.carbon_exp)

    # MARKET CORRECTION
    market_price = demand_curve(total_supply)

    # REGULATORY ACTION
    government.market_regulation(
        total_supply = total_supply,
        total_carbon_emm = total_carbon_emm,
    )

    social_welfare_data.append(government.social_welfare)

visulaise_dict(supply_data, 'Supply', 'Production')
visulaise_dict(innovation_data, 'Innovation Spending', 'Innovation Expenditure')
visulaise_dict(carbon_emm_data, 'Carbon Emissions', 'Emission')
visulaise_dict(carbon_exp_data, 'Periodic Carbon Permit Spending', 'Carbon Expenditure')

plt.figure(figsize=(10, 5))
plt.plot(market_price_data)
plt.title('Market Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.grid()
plt.show()


plt.figure(figsize=(10, 5))
plt.plot(carbon_prod_data)
plt.title('Carbon credits per unit investment')
plt.xlabel('Time')
plt.ylabel('Delta Carbon')
plt.grid()
plt.show()
plt.show()

plt.figure(figsize=(10, 5))
plt.plot(social_welfare_data)
plt.title('Social Welfare')
plt.xlabel('Time')
plt.ylabel('Social Welfare')
plt.grid()
plt.show()
plt.show()

policy_social_welfare_data['Allocation Policy 2'] = social_welfare_data
policy_market_price_data['Allocation Policy 2'] = market_price_data
max(social_welfare_data), max(market_price_data)

visulaise_dict(policy_social_welfare_data, 'Social Welfare', 'social welfare')
visulaise_dict(policy_market_price_data, 'Market Price', 'price')



