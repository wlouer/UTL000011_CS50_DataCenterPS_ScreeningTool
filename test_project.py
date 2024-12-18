import pytest
import pandas as pd  # Need to import pandas so that I can compare dataframes are equal
import numpy as np
from unittest.mock import patch #  the module patch will respond to input calls with my mock inputs
from project import get_user_inputs, calc_system_reliability, get_tier_level, create_plots
######################################################################################################
## Test the get_user_inputs function.

def test_get_user_inputs_good():
    mock_inputs_good = ['2500', '95', '335']
    
    case = ['unit_size_2','unit_size_2','unit_size_2','unit_size_2','unit_size_2','unit_size_2', 'unit_size_3', 'unit_size_3','unit_size_3','unit_size_3','unit_size_3','unit_size_3',
            'unit_size_4', 'unit_size_4','unit_size_4','unit_size_4','unit_size_4','unit_size_4', 'unit_size_5', 'unit_size_5','unit_size_5','unit_size_5','unit_size_5','unit_size_5']
    demand = list(np.ones(24) * float(mock_inputs_good[0]))
    unit_capacity = list(np.ceil(float(mock_inputs_good[0])/ np.array([2,2,2,2,2,2,3,3,3,3,3,3,4,4,4,4,4,4,5,5,5,5,5,5])))
    units_reqd = list(np.array([2,2,2,2,2,2,3,3,3,3,3,3,4,4,4,4,4,4,5,5,5,5,5,5],dtype=np.int64 ))
    units_installed = list(units_reqd + np.array([0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5], dtype=np.int64))
    unit_rel = list(np.ones(24) * float(mock_inputs_good[1]))
    unit_schedule_outage_hours = list(np.ones(24) * float(mock_inputs_good[2]))

    expected_result = pd.DataFrame({
    'unit_sizing_case': case,
    'demand_kW': demand,
    'unit_capacity_kW': unit_capacity,
    'units_reqd': units_reqd,
    'units_installed': units_installed,
    'unit_reliability_pct': unit_rel,
    'unit_schedule_outage_hrs': unit_schedule_outage_hours,
    })
    expected_result['system_capacity_kW'] = np.round(expected_result['unit_capacity_kW'] * expected_result['units_installed'],-2)
    expected_result['redundant_units'] = expected_result['units_installed'] - expected_result['units_reqd']


    # Use patch to mock input calls
    with patch('builtins.input', side_effect=mock_inputs_good):
        result = get_user_inputs()
    
    # Assert that the returned DataFrame matches the expected DataFrame
    pd.testing.assert_frame_equal(result, expected_result)


def test_get_user_inputs_invalid_then_valid():
    # Simulate invalid inputs first, then valid inputs
    mock_inputs_invalid_then_valid = ['abc', 'five', 'ninety', '2500', '95', '335']
    
    
    case = ['unit_size_2','unit_size_2','unit_size_2','unit_size_2','unit_size_2','unit_size_2', 'unit_size_3', 'unit_size_3','unit_size_3','unit_size_3','unit_size_3','unit_size_3',
            'unit_size_4', 'unit_size_4','unit_size_4','unit_size_4','unit_size_4','unit_size_4', 'unit_size_5', 'unit_size_5','unit_size_5','unit_size_5','unit_size_5','unit_size_5']
    demand = list(np.ones(24) * float(mock_inputs_invalid_then_valid[3]))
    unit_capacity = list(np.ceil((float(mock_inputs_invalid_then_valid[3])/ np.array([2,2,2,2,2,2,3,3,3,3,3,3,4,4,4,4,4,4,5,5,5,5,5,5]))))
    units_reqd = list(np.array([2,2,2,2,2,2,3,3,3,3,3,3,4,4,4,4,4,4,5,5,5,5,5,5],dtype=np.int64 ))
    units_installed = list(units_reqd + np.array([0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5], dtype=np.int64))
    unit_rel = list(np.ones(24) * float(mock_inputs_invalid_then_valid[4]))
    unit_schedule_outage_hours = list(np.ones(24) * float(mock_inputs_invalid_then_valid[5]))

    expected_result = pd.DataFrame({
    'unit_sizing_case': case,
    'demand_kW': demand,
    'unit_capacity_kW': unit_capacity,
    'units_reqd': units_reqd,
    'units_installed': units_installed,
    'unit_reliability_pct': unit_rel,
    'unit_schedule_outage_hrs': unit_schedule_outage_hours,
    })
    expected_result['system_capacity_kW'] = np.round(expected_result['unit_capacity_kW'] * expected_result['units_installed'],-2)
    expected_result['redundant_units'] = expected_result['units_installed'] - expected_result['units_reqd']

    #  patch to mock input calls
    with patch('builtins.input', side_effect=mock_inputs_invalid_then_valid):
        result = get_user_inputs()
    
    # Check if the function returns a DataFrame matching the expected result
    pd.testing.assert_frame_equal(result, expected_result)

#
############################################################################################################

def test_calc_system_reliability_valid():
    k = 4
    n = 9
    unit_rel = 95
    outage_hours = 335 
    row = pd.Series(np.array([k, n, unit_rel, outage_hours]))
    result = calc_system_reliability(row)
    expected_result = 99.999394
    np.testing.assert_allclose(result, expected_result)

###############################################################################################################
def test_calc_system_reliability_valid():
    k = 4
    n = 9
    unit_rel = 95
    outage_hours = 335 
    row = pd.Series(np.array([k, n, unit_rel, outage_hours]))
    result = calc_system_reliability(row)
    expected_result = 99.999394
    np.testing.assert_allclose(result, expected_result)

##############################################################################################
def test_get_tier_level_valid():
    row = pd.Series()
    row['system_availability'] = 99.95
    result = get_tier_level(row)
    assert result == 'Tier 2'

############################################################################################
def test_create_plots():
    df_sample = pd.DataFrame({
        'system_capacity_kW': [1000, 2000, 1500, 2500],
        'system_availability': [95, 90, 85, 92],
        'tier_level': ['Tier 1', 'Tier 2', 'Tier 3', 'Tier 4'],
        'unit_capacity_kW': [500, 500, 500, 500],
        'units_installed': [2, 4, 3, 5],
        'demand_kW': [1500, 2500, 2000, 2800]
    })
    with patch('matplotlib.pyplot.savefig') as mock_savefig: # patch directs the code to replace the .savefig() method with a mock object and tracks the 
        create_plots(df_sample)

        # Assert that savefig was called the correct number of times (should be 3 plot files saved)
        assert mock_savefig.call_count == 3
