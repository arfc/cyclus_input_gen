import numpy as np
import parser


def get_new_deployment(power_dict, inst_list, demand_eq, new_reactor_power,
                       new_reactor_lifetime, avail_timestep, new=False):
    """ Calculates the new deployment scheme to maintain power demand

    Parameters:
    -----------
    power_dict: dictionary
        key: institution
        value: capacity timeseries
    inst_list: list
        list of institution names to take into account
    demand_eq: str
        demand equation w.r.t time(t)
    new_reactor_power: int
        new reactor power capacity [GWe]
    new_reactor_lifetime: int
        lifetime of new reactor
    avail_timestep: int
        timestep when new reactor type is available
    new: bool
        if the reactor is new reactor type or not

    Returns:
    --------
    deploy_array: array
        timeseries for deploying new reactor
    """
    # get total power generated
    total_steps = len(power_dict[inst_list[0]])
    total_power = np.zeros(total_steps)
    for key, val in power_dict.items():
        if key in inst_list:
            total_power += np.array(val)

    # get lacking from power demand
    eq = parser.expr(demand_eq).compile()
    demand_timeseries = np.zeros(total_steps)
    for indx, value in enumerate(demand_timeseries):
        t = indx
        demand_timeseries[indx] = eval(eq)

    total_lack = demand_timeseries - total_power
    deploy_array = np.zeros(total_steps)
    deployed_power = np.zeros(total_steps)
    for indx in range(len(total_lack)):
        # skip index 0
        if indx == 0:
            continue
        if total_lack[indx] > new_reactor_power:
            num = total_lack[indx] // new_reactor_power
            if new and indx >= avail_timestep:
                deploy_array[indx] = num
                high_end = min([indx + new_reactor_lifetime, total_steps])
                for i in range(indx, high_end):
                    total_lack[i] -= num * new_reactor_power
                    deployed_power[i] += num * new_reactor_power
            elif not new and indx < avail_timestep:
                deploy_array[indx] = num
                high_end = min([indx + new_reactor_lifetime, total_steps])
                for i in range(indx, high_end):
                    total_lack[i] -= num * new_reactor_power
                    deployed_power[i] += num * new_reactor_power

    return deploy_array, deployed_power


def write_deployinst(deploy_array, reactor_name,
                     filename, lifetime):
    """ Writes the deployinst block of cyclus input file with
        the deploy array

    Parameters:
    -----------
    deploy_array: array
        deployment timeseries
    reactor_name: str
        name of reactor to be deployed
    filename: str
        name of output file
    lifetime: int
        lifetime of reactor

    Returns:
    --------
    null. creates xml file.
    """
    prototypes = '<prototypes>\n'
    build_times = '<build_times>\n'
    n_build = '<n_build>\n'
    lifetimes = '<lifetimes>\n'
    for time, build_num in enumerate(deploy_array):
        if build_num != 0:
            prototypes += '\t\t<val>%s</val>\n' % reactor_name
            build_times += '\t\t<val>%i</val>\n' % time
            n_build += '\t\t<val>%i</val>\n' % build_num
            lifetimes += '\t\t<val>%i</val>\n' % lifetime
    prototypes += '</prototypes>\n'
    build_times += '</build_times>\n'
    n_build += '</n_build>\n'
    lifetimes += '</lifetimes>\n'

    outstring = '<root>\n'
    outstring += prototypes + build_times + n_build + lifetimes
    outstring += '</root>\n'
    with open(filename, 'w') as f:
        f.write(outstring)
