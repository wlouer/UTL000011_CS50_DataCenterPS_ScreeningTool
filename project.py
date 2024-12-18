import pandas as pd
import numpy as np
from math import comb
import matplotlib.pyplot as plt
import seaborn as sns


def get_user_inputs():
    '''Function solicits input from the user (peak_demand, number_units, unit_capacity, unit_reliability, unit_outage_wks)
    
    returns a dataframe with the project characteristics
    
    '''
    #  get/validate peak demand
    while True:
        try:
            peak_demand = float(input('Enter peak load for the facility in kW:\n'))
            if peak_demand <= 0:
                print('Peak demand must be a positive number.')
                continue
            break
        except ValueError:
            print('Invalid Input.  Please enter a valid number for peak demand in kW.')


    #  get/validate unit reliability
    while True:
        try: 
            unit_reliability = float(input('Enter the estimated reliability of each unit in percent (0-100):\n'))
            if unit_reliability  <=0 or unit_reliability >=100:
                print('Reliability must be between 0 and 100 percent.')
                continue
            break
        except ValueError:
            print('Invalid Input.  Please enter a valid number for reliability.\n')
   
    #  get/validate outage hours
    while True:
        try: 
            outage_hours = float(input('Enter the estimated scheduled outage hours for each unit:\n'
            'Hint (1 wk = 168 , 2 wks = 336 , 3 wks = 504  , 4 wks= 672 )\n'))
            if outage_hours  <=0:
                print('Outage hours must be greater than 0.')
                continue
            break
        except ValueError:
            raise ValueError('Invalid Input.')
      
    
    case = []
    demand = []
    unit_capacity = []
    units_reqd = []
    units_installed = []
    unit_rel = []
    unit_schedule_outage_hours = []

    for i in range(2,6):
        for j in range(6):
            case.append(f'unit_size_{i}')
            demand.append(peak_demand)
            units_reqd.append(i)
            units_installed.append(i+j)
            unit_capacity.append(np.ceil(peak_demand/ i))
            unit_rel.append(unit_reliability)
            unit_schedule_outage_hours.append(outage_hours)

    project_basis = {
    'unit_sizing_case': case,
    'demand_kW': demand,
    'unit_capacity_kW': unit_capacity,
    'units_reqd': units_reqd,
    'units_installed': units_installed,
    'unit_reliability_pct': unit_rel,
    'unit_schedule_outage_hrs': unit_schedule_outage_hours,
    }
    df_cases = pd.DataFrame(project_basis)
    df_cases['system_capacity_kW'] = np.round(df_cases['unit_capacity_kW'] * df_cases['units_installed'],-2)
    df_cases['redundant_units'] = df_cases['units_installed'] - df_cases['units_reqd']
    return df_cases


def calc_system_reliability(row):
    '''
    Calculates the reliability of a system

    Args:
    row[0] = k
    row[1] = n
    row[2] = unit_rel
    row[3] = outage_hours

    Returns:
    pct_system_avail(float): annual percentage availability for the system
    '''
    k = int(row.iloc[0])
    n = int(row.iloc[1])
    unit_rel = row.iloc[2]
    outage_hours = row.iloc[3]
    pct = unit_rel/100
    time_outage = outage_hours * n
    time_no_outage = 8760 - time_outage
    reliability_no_outage = 0
    reliability_outage = 0

    for i in range(k, n+1):
        reliability_no_outage += comb(n, i)*(pct)**(i) * (1-pct)**(n-i) # calculate per-state reliability for periods where no units in scheduled outage

    for j in range(k, n):
        reliability_outage += comb(n-1, j)*(pct)**(j) * (1-pct)**(n-1-j) #  calculate per-state reliabiltiy for periods where 1 unit is in scheduled outage

    pct_system_avail = (reliability_no_outage * time_no_outage + reliability_outage * time_outage)  / 8760    

    return pct_system_avail *100


def get_tier_level(row):
    '''
    Defines a tier level from Uptime Institute tier levels
    reliability > 99.671:  Tier 1
    reliability > 99.741:  Tier 2
    reliability > 99.982:  Tier 3
    reliability > 99.995:  Tier 4

    returns Tier # in text format
    '''
    if row['system_availability'] >= 99.995:
        return 'Tier 4'
    elif row['system_availability'] >= 99.982:
        return 'Tier 3'
    elif row['system_availability'] >= 99.741:
        return 'Tier 2'
    elif row['system_availability'] >= 99.671:
        return 'Tier 1'
    else:
        return 'Tier NA'


def create_plots(df):
    '''
    Create plots for presenting the results

    args
    df: dataframe with results

    returns:  plots saved to outputs folder
    '''
    #  set plot formatting
    plt.style.use("ggplot")
    plt.rc("figure", autolayout=True)
    plt.rc(
    "axes",
    labelweight="bold",
    labelsize="large",
    titleweight="bold",
    titlesize=14,
    titlepad=10,)

    # Create scatterplot of availability vs. capacity.
    fig, axs = plt.subplots(figsize=(11,6))

    sns.scatterplot(data=df, x='system_capacity_kW', y='system_availability', 
                    hue='tier_level', hue_order=['Tier NA', 'Tier 1', 'Tier 2', 'Tier 3', 'Tier 4'], ax=axs, palette='Set1')
    axs.axvline(
        x=df.demand_kW.mean(),  # Use the mean or any representative value
        color='gray', 
        linewidth=3,  # Adjust line thickness
        alpha=1.0,
        linestyle='--',
        label='Peak Demand kW'
    )
    plt.xlabel('System Capacity kW')
    plt.ylabel('System Availability (%)')
    plt.title('Availability vs. Capacity and Uptime Institute Tier Levels')
    plt.legend(title='Tier Level', loc='center right' )
    plt.xlim(df.demand_kW.min()*0.9, df.system_capacity_kW.max()*1.1)  # Adjust based on your data
    plt.ylim(df.system_availability.min()*0.95, df.system_availability.max()*1.05)  # Optional: adjust y-axis if needed
    plt.grid()
    plt.savefig('outputs/avail_vs_sys_capacity_scatter.png')

    # Create boxplot of capacity vs. Tier Levels to show excess capacity range needed per Tier Level
    plt.subplots(figsize=(11,6))
    sns.boxplot(data=df, x='tier_level', y='system_capacity_kW', 
        hue='tier_level', order=['Tier NA', 'Tier 1', 'Tier 2', 'Tier 3', 'Tier 4'],
        hue_order=['Tier NA', 'Tier 1', 'Tier 2', 'Tier 3', 'Tier 4'], palette='Set1')
    sns.lineplot(data=df, x='tier_level', y='demand_kW', linestyle='--', label='Peak Demand Load', color='gray')
    plt.xlabel('Tier Level')
    plt.ylabel('System Capacity (kW)')
    plt.title('System Capacity (kW) BoxPlot for different tier levels')
    plt.legend(loc='upper left')
    plt.title('System Capacity Range for all Cases\nBy Tier Level')
    plt.grid()
    plt.savefig('outputs/boxplot_sys_capacity_tier_level.png')

    #  Create subplots for each Tier level showing system capacity, number of units required for each unit size.
    fig, axs = plt.subplots(2,2, figsize=(11,8), sharex=True, sharey=True)
    axs = axs.flatten()
    categories = df.unit_capacity_kW.unique()
    color_palette = sns.color_palette("Set1", len(categories)) 

    for i, tier in enumerate(['Tier 1','Tier 2', 'Tier 3', 'Tier 4']):
        filter = df.tier_level == tier
        sns.barplot(data=df[filter].sort_values('units_installed'), x='units_installed', y='system_capacity_kW', order= df.units_installed.unique(), 
                    hue='unit_capacity_kW', ax=axs[i], hue_order=categories, palette=dict(zip(categories, color_palette)), ) 
        axs[i].axhline(
        y=df.demand_kW.mean(),  # Use the mean or any representative value
        color='gray', 
        linewidth=3,  # Adjust line thickness
        alpha=0.5,
        linestyle='--',
        label='Peak Demand kW')
        axs[i].set_title(f'System Capacity vs. Number of units\n{tier}')
        axs[i].grid()
        axs[i].legend(loc='upper left', title='Unit Capacity (kW)')
        axs[i].set_xlabel('Units Required')
        axs[i].set_ylabel('System Capacity (kW)')
        axs[i].set_ylim(df.demand_kW.min()*0.7,df.system_capacity_kW.max() * 1.25)
    plt.suptitle('System Capacity and Number of Units Required by Tier Level\n', fontsize=14)
    plt.tight_layout()
    plt.savefig('outputs/subplot_sys_capacity_number_units.png')


def main():
    df = get_user_inputs()
    df['system_availability'] = df[['units_reqd', 'units_installed', 'unit_reliability_pct', 'unit_schedule_outage_hrs']].apply(calc_system_reliability, axis=1)
    df['tier_level'] = df.apply(get_tier_level, axis=1)
    create_plots(df)
    df.to_csv('outputs/results.csv', index=False)


if __name__ == "__main__":
    main()