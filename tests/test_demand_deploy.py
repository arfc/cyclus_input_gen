import numpy as np
import collections
import os
import sys
import write_input.demand_deploy as dd



def test_get_new_deployment_prev():
    """Test get new deployment"""
    length = 10
    prev_power = {'instA': np.zeros(length)}
    deploy_array, power_array = dd.get_new_deployment(prev_power,
                                                      ['instA'],
                                                      '1*t',
                                                      1,
                                                      2,
                                                      100)

    assert sum(deploy_array) == 20
    assert max(power_array) == 8


def test_get_new_deployment_aft():
    """Test get new deployment"""
    length = 10
    prev_power = {'instA': np.zeros(length)}
    deploy_array, power_array = dd.get_new_deployment(prev_power,
                                                      ['instA'],
                                                      '1*t',
                                                      1,
                                                      2,
                                                      5,
                                                      new=True)
    # check if nothing is deployed before avail timestep
    assert sum(deploy_array[:5]) == 0
    assert max(power_array) == 9
