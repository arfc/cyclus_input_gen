import sys
import jinja2
import numpy as np
import os
from datetime import datetime
from cyclus_input_gen.templates import template_collections

# tells command format if input is invalid

if len(sys.argv) < 4:
    print('Usage: from_pris.main([csv],' +
          '[init_date], [duration], [country_list], [output_file_name])')


def delete_file(file):
    """Deletes a file if it exists.

    Parameters
    ----------
    file: str
        filename to delete, if it exists

    Returns
    -------
    null

    """
    if os.path.exists('./' + file) is True:
        os.system('rm ' + file)


def read_csv(csv_file, country_list):
    """This function reads the csv file and returns the list.

    Parameters
    ---------
    csv_file: str
        csv file that lists country, reactor name, net_elec_capacity etc.

    Returns
    -------
    reactor_array:  list
        array with the data from csv file
    """
    reactor_array = np.genfromtxt(csv_file,
                                  skip_header=2,
                                  delimiter=',',
                                  dtype=('S128', 'S128',
                                         'S128', 'int',
                                         'S128', 'S128', 'S128',
                                         'int', 'S128',
                                         
                                         'S128', 'S128',
                                         'S128', 'float',
                                         'float', 'float',
                                         'int', 'int'),
                                  names=('country', 'reactor_name',
                                         'type', 'net_elec_capacity',
                                         'status', 'operator', 'const_date',
                                         'cons_year', 'first_crit',

                                         'first_grid', 'commercial',
                                         'shutdown_date', 'ucf',
                                         'lat', 'long',
                                         'entry_time', 'lifetime'))
    indx_list = []
    for indx, reactor in enumerate(reactor_array):
        if reactor['country'].decode('utf-8') not in country_list:
            indx_list.append(indx)
    reactor_array = np.delete(reactor_array, indx_list, axis=0)

    for indx, reactor in enumerate(reactor_array):
        reactor_array[indx]['const_date'] = std_date_format(
            reactor['const_date'])
        reactor_array[indx]['first_crit'] = std_date_format(reactor['first_crit'])
        reactor_array[indx]['first_grid'] = std_date_format(
            reactor['first_grid'])
        reactor_array[indx]['commercial'] = std_date_format(
            reactor['commercial'])
        reactor_array[indx]['shutdown_date'] = std_date_format(
            reactor['shutdown_date'])
        
    return filter_test_reactors(reactor_array)



def std_date_format(date_string):
    """ This function converts date format MM/DD/YYYY to YYYYMMDD

    Parameters:
    -----------
    date_string: str
        string with date
    
    Returns:
    --------
    date: int
        integer date with format YYYYMMDD
    """
    date_string = date_string.decode('utf-8')

    if date_string.count('/') == 2:
        obj = datetime.strptime(date_string, '%m/%d/%Y')
        return int(obj.strftime('%Y%m%d'))
    if len(date_string) == 4:
        # default first of the year if only year is given
        return int(date_string + '0101')
    if date_string == '':
        return int(-1)
        

def filter_test_reactors(reactor_array):
    """This function filters experimental reactors that have a
       net electricity capacity less than 100 MWe

    Parameters
    ---------
    reactor_array: list
        array with reactor data.

    Returns
    -------
    array
        array with the filtered data
    """
    hitlist = []
    count = 0
    for data in reactor_array:
        if data['net_elec_capacity'] < 100:
            hitlist.append(count)
        count += 1
    return np.delete(reactor_array, hitlist)


def get_ymd(yyyymmdd):
    """This function extracts year and month value from yyyymmdd format

        The month value is rounded up if the day is above 16

    Parameters
    ---------
    yyyymmdd: int
        date in yyyymmdd format

    Returns
    -------
    year: int
        year
    month: int
        month
    """
    yyyymmdd = int(yyyymmdd)
    year = yyyymmdd // 10000
    month = (yyyymmdd // 100) % 100
    day = yyyymmdd % 100
    if day > 16:
        month += 1
    return (year, month)


def get_lifetime(start_date, end_date):
    """This function gets the lifetime for a prototype given the
       start and end date.

    Parameters
    ---------
    start_date: int
        start date of reactor - first criticality.
    end_date: int
        end date of reactor - null if not listed or unknown

    Returns
    -------
    lifetime: int
        lifetime of the prototype in months

    """

    if end_date != -1:
        end_year, end_month = get_ymd(end_date)
        start_year, start_month = get_ymd(start_date)
        year_difference = end_year - start_year
        month_difference = end_month - start_month
        if month_difference < 0:
            year_difference -= 1
            start_month += 12
        month_difference = end_month - start_month

        return (12 * year_difference + month_difference)
    else:
        return 720


def get_entrytime(init_date, start_date):
    """This function converts the date format and saves it in variables.

        All dates are in format - yyyymmdd

    Parameters
    ---------
    init_date: int
        start date of simulation
    start_date: int
        start date of reactor - first criticality.

    Returns
    -------
    entry_time: int
        timestep of the prototype to enter

    """
    init_year, init_month = get_ymd(init_date)
    start_date = int(start_date)
    start_year, start_month = get_ymd(start_date)

    year_difference = start_year - init_year
    month_difference = start_month - init_month
    if month_difference < 0:
        year_difference -= 1
        start_month += 12
    month_difference = start_month - init_month

    entry_time = 12 * year_difference + month_difference

    return entry_time


def read_template(template):
    """ Returns a jinja template

    Parameters
    ---------
    template: str
        template file that is to be stored as variable.

    Returns
    -------
    output_template: jinja template object
        output template that can be 'jinja.render' -ed.

    """

    # takes second argument file as reactor template
    output_template = jinja2.Template(template)

    return output_template


def refine_name(name_data):
    """ Takes the name data and decodes and refines it.

    Parameters
    ----------
    name_data: str
        reactor name data from csv file

    Returns
    -------
    name: str
        refined and decoded name of reactor
    """
    name = name_data.decode('utf-8')
    start = name.find('(')
    end = name.find(')')
    if start != -1 and end != -1:
        name = name[:start]
    return name


def reactor_render(reactor_data, output_file, is_cyborg=False):
    """Takes the list and template and writes a reactor file

    Parameters
    ----------
    reactor_data: list
        list of data on reactors
    template: jinja.template
        jinja template for reactor file
    mox_template: jinja.template
        jinja template for mox reactor file
    output_file: str
        name of output file
    is_cyborg: bool
        if True, uses Cyborg templates

    Returns
    -------
    The reactor section of cyclus input file

    """

    pwr_template = read_template(template_collections.pwr_template)
    mox_reactor_template = read_template(template_collections.mox_template)
    candu_template = read_template(template_collections.candu_template)

    if is_cyborg:
        pwr_template = read_template(template_collections.pwr_template_cyborg)
        mox_reactor_template = read_template(template_collections.mox_template_cyborg)
        candu_template = read_template(template_collections.candu_template_cyborg)


    ap1000_spec = {'template': pwr_template,
                   'kg_per_assembly': 446.0,
                   'assemblies_per_core': 157 / 1110.0,
                   'assemblies_per_batch': 52 / 3330.0}
    bwr_spec = {'template': pwr_template,
                'kg_per_assembly': 180,
                'assemblies_per_core': 764 / 1000.0,
                'assemblies_per_batch': 764 / 3000.0}
    phwr_spec = {'template': candu_template,
                 'kg_per_assembly': 8000 / 473,
                 'assemblies_per_core': 473 / 500.0,
                 'assemblies_per_batch': 60}
    candu_spec = {'template': candu_template,
                  'kg_per_assembly': 8000 / 473,
                  'assemblies_per_core': 473 / 500.0,
                  'assemblies_per_batch': 60}
    pwr_spec = {'template': pwr_template,
                'kg_per_assembly': 446.0,
                'assemblies_per_core': 193 / 1000.0,
                'assemblies_per_batch': 193 / 3000.0}
    epr_spec = {'template': pwr_template,
                'kg_per_assembly': 467.0,
                'assemblies_per_core': 216,
                'assemblies_per_batch': 72}

    reactor_specs = {'AP1000': ap1000_spec,
                     'PHWR': phwr_spec,
                     'BWR': bwr_spec,
                     'CANDU': candu_spec,
                     'PWR': pwr_spec,
                     'EPR': epr_spec}

    for data in reactor_data:
        # refine name string
        name = refine_name(data['reactor_name'])
        reactor_type = data['type'].decode('utf-8')
        if reactor_type in reactor_specs.keys():
            # if the reactor type matches with the pre-defined dictionary,
            # use the specifications in the dictionary.
            spec_dict = reactor_specs[reactor_type]
            reactor_body = spec_dict['template'].render(
                country=data['country'].decode('utf-8'),
                type=reactor_type,
                reactor_name=name,
                assem_size=round(spec_dict['kg_per_assembly'], 3),
                n_assem_core=int((spec_dict['assemblies_per_core']
                                       * data['net_elec_capacity'])),
                n_assem_batch=int((spec_dict['assemblies_per_batch']
                                        * data['net_elec_capacity'])),
                capacity=data['net_elec_capacity'])
        else:
            # assume 1000MWe pwr linear core size model if no match
            reactor_body = pwr_template.render(
                country=data['country'].decode('utf-8'),
                reactor_name=name,
                type=reactor_type,
                assem_size=523.4,
                n_assem_core=int(
                    round(data['net_elec_capacity'] / 1000 * 193)),
                n_assem_batch=int(
                    round(data['net_elec_capacity'] / 3000 * 193)),
                capacity=data['net_elec_capacity'])

        with open(output_file, 'a') as output:
            output.write(reactor_body)


def input_render(init_date, duration, reactor_file,
                 region_file, output_file, reprocessing):
    """Creates total input file from region and reactor file

    Parameters
    ---------
    init_date: int
        date of desired start of simulation (format yyyymmdd)
    reactor_file: str
        jinja rendered reactor section of cyclus input file
    region_file: str
        jinja rendered region section of cylcus input file
    output_file: str
        name of output file
    reprocessing: bool
        True if reprocessing is done, false if ignored

    Returns
    -------
    A complete cylus input file.

    """
    template = read_template(template_collections.input_template)
    with open(reactor_file, 'r') as fp:
        reactor = fp.read()
    with open(region_file, 'r') as bae:
        region = bae.read()

    startyear, startmonth = get_ymd(init_date)

    # has reprocessing chunk if reprocessing boolean is true.
    if reprocessing is True:
        reprocessing_chunk = ('<entry>\n'
                              + '  <number>1</number>\n'
                              + '  <prototype>reprocessing</prototype>\n'
                              + '</entry>')
    else:
        reprocessing_chunk = ''
    # renders template
    rendered_template = template.render(duration=duration,
                                        startmonth=startmonth,
                                        startyear=startyear,
                                        reprocessing=reprocessing_chunk,
                                        reactor_input=reactor,
                                        region_input=region)

    with open(output_file, 'w') as output:
        output.write(rendered_template)

    os.system('rm reactor_output.xml.in region_output.xml.in')


def region_render(reactor_data, output_file):
    """Takes the list and template and writes a region file

    Parameters
    ---------
    reactor_data: list
        list of data on reactors
    output_file: str
        name of output file

    Returns
    -------
    The region section of cyclus input file

    """
    # template only has prototype, buildtime, n_build and lifetime
    template = read_template(template_collections.deployinst_template)
    # full template is the bigger template for the `region block'.
    full_template = read_template(template_collections.region_output_template)
    country_list = []
    empty_country = []

    valhead = '<val>'
    valtail = '</val>'

    # creates list of countries and turns it into a set
    for data in reactor_data:
        country_list.append(data['country'].decode('utf-8'))
    country_set = set(country_list)

    for country in country_set:
        prototype = ''
        entry_time = ''
        n_build = ''
        lifetime = ''

        # for every reactor data corresponding to a country, create a
        # file with its `region block`
        for data in reactor_data:
            if data['country'].decode('utf-8') == country:
                if data['lifetime'] == 0:
                    continue
                prototype += (valhead
                              + refine_name(data['reactor_name'])
                              + valtail + '\n')
                entry_time += (valhead
                               + str(data['entry_time']) + valtail + '\n')
                n_build += valhead + '1' + valtail + '\n'
                lifetime += valhead + str(data['lifetime']) + valtail + '\n'

        render_temp = template.render(prototype=prototype,
                                      start_time=entry_time,
                                      number=n_build,
                                      lifetime=lifetime)
        # if nothing is rendered the length will be less than 100:
        if len(render_temp) > 100:
            with open(country, 'a') as output:
                output.write(render_temp)
        else:
            empty_country.append(country)

    # remove the countries with no values
    for country in empty_country:
        country_set.remove(country)

    for country in country_set:
        # jinja render region template for different countries
        with open(country, 'r') as ab:
            country_input = ab.read()
            country_body = full_template.render(
                country=country,
                country_gov=(country
                             + '_government'),
                deployinst=country_input)

        # write rendered template as 'country'_region
        with open(country + '_region', 'a') as output:
            output.write(country_body)

        # concatenate the made file to the final output file and remove temp
        os.system('cat ' + country + '_region >> ' + output_file)
        os.system('rm ' + country)
        os.system('rm ' + country + '_region')


def main(csv_file, init_date, duration, country_list, output_file='complete_input.xml', reprocessing=True):
    """ Generates cyclus input file from csv files and jinja templates.

    Parameters
    ---------
    csv_file : str
        csv file containing reactor data (country, name, net_elec_capacity)
    init_date: int
        yyyymmdd format of initial date of simulation
    input_template: str
        template file for entire complete cyclus input file
    country_list: list of str
        list of countries to take into account
    output_file: str
        directory and name of complete cyclus input file
    reprocessing: bool
        True if reprocessing is done, False if not

    Returns
    -------
    File with reactor section of cyclus input file
    File with region section of cyclus input file
    File with complete cyclus input file

    """

    # deletes previously existing files
    delete_file(output_file)
    reactor_output_filename = 'reactor_output.xml.in'
    region_output_filename = 'region_output.xml.in'
    # read csv and templates
    csv_database = read_csv(csv_file, country_list)

    for data in csv_database:
        entry_time = get_entrytime(init_date, data['first_crit'])
        lifetime = get_lifetime(data['first_crit'], data['shutdown_date'])
        if entry_time <= 0:
            lifetime = lifetime + entry_time
            if lifetime < 0:
                lifetime = 0
            entry_time = 1
        data['entry_time'] = entry_time
        data['lifetime'] = lifetime
    # renders reactor / region / input file.
    reactor_render(csv_database, reactor_output_filename)
    region_render(csv_database, region_output_filename)
    input_render(init_date, duration, reactor_output_filename,
                 region_output_filename, output_file, reprocessing)

