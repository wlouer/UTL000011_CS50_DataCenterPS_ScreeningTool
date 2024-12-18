
#  Data Center Power System - Availability Analysis of Redundancy Alternatives
## CS50P Final Project
### Bill Louer
###  New Jersey, USA
###  Date: 


#### Video Demo:  <URL HERE>

##  Background:
Data centers are expanding in number and in size at a rapid pace.  Data centers require a significant amount of electrical power at high availability.  Availability metrics for data centers are defined by Uptime Institute according to a Tier Level.  Uptime Institute's categorization of Tier level includes an availability metric as follows:
- Tier 1: Reliability >= 99.671
- Tier 2: Reliability >= 99.741
- Tier 3: Reliability >= 99.982
- Tier 4: Reliability >= 99.995

This metric refers to the data center availability which as a consequence dictates the power system availability being equal to or even greater than this value.  For simplicity, I have assumed that the power system must equal these availabiltiy levels to be classified according to the respective tier.

Reliability is defined as the measure of unplanned (forced) outage time divided by period hours.  Reliability is therefore a probabablistic measure.
Availability accounts for unplanned and planned or scheduled outages.  

##  Program Objective:  
- The objective of the program is to calculate the availability of a power system, given a demand load, individual unit reliability and annual scheduled outage hours per unit.
- Following user input, the program calculates the system availability for different unit size and unit redundancy cases (n+0, n+1, n+2, n+3, n+4, n+5).
-  For each case, the program calculates the system reliability under two conditions:
    - Condition 1:  no units in scheduled outage
    - Condition 2:  1 unit in scheduled outage
-  An average annual system reliability is calculated based on a period weighting average of the two conditions. 

##  Program Structure:  
The program consists of the following features and modules:

    1. Input function get_user_inputs():  
    -  Solicits user input via. the terminal prompt for 
        - demand_load 
        - unit_reliability 
        - annual scheduled outage duration per unit
    - Returns a dataframe with all cases and case definitions
        - Demand load as supplied by the user 
        - 2-5 units required and sized to meet the demand load without redundancy
        - 0-5 redundant units of the same size
        - Individual unit reliability as supplied by the user
        - Individual unit scheduled outage hours as supplied by the user
        - Calculated system capacity based on unit sizes and total units (reqd + redundant)

    2. System Reliability Calculation function calc_system_reliability():
    - Calculates the system availability for periods when there are no scheduled outages (no units out of service) and when a scheduled outage is planned (1 unit out of service).
    - Uses the summed 'per-state' reliability for all states where the system capacity equals or exceeds the demand load.  These per state reliability numbers are calculated using binomial probability.
    - Creates a weighted average of these two periods and returns system availability.
    
    3. Tier Level Categorization function get_tier_level():
    -  Based on the system availability, a Tier level is determined based on the above criteria.  
    
    4. Plotting function create_plots()
    -  Results plots are created using seaborn and matplotlib and saved to an outputs folder:
        - Availability vs. System Capacity Scatter Plotting.
        - BoxPlot of System Capacity by Tier Level.
        - Subplots of System Capacity vs. Number of Units shown for each Tier level.

    5. Results in tabular format are saved to a csv file for further analysis (if needed)

## Authors

- [@wlouer](https://www.github.com/wlouer)

## About Me
I'm Bill—a power industry professional with 20+ years of experience in power generation. My background as a mechanical engineer led to me a role as project manager where I led the development and execution of power generation projects. These days, I'm practicing, python, data science, visualization, and machine learning skills with the intention of using them as a tool to uncover insights and improve decision making in power project development, design, procurement, construction and operations.