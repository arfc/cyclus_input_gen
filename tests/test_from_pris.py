import numpy as np
import collections
import os
import sys
import cyclus_input_gen.from_pris as fp

dir = os.path.dirname(__file__)
test_database_path = os.path.join(dir, 'test_database.csv')


def test_read_csv():
    """Test if read_csv returns the correct list with key"""
    reactor_array = fp.read_csv(test_database_path,
                                ['France', 'Czech_Republic'])
    print(type(reactor_array))
    test_dict = {}
    test_dict['country1'] = reactor_array[0]['country'].decode('utf-8')
    test_dict['country3'] = reactor_array[2]['country'].decode('utf-8')
    # makes sure the test reactor is filtered out
    test_dict['capacity1'] = reactor_array[0]['net_elec_capacity']
    test_dict['capacity3'] = reactor_array[2]['net_elec_capacity']

    answer_dict = {}
    answer_dict['country1'] = 'France'
    answer_dict['country3'] = 'Czech_Republic'
    answer_dict['capacity1'] = 1495
    answer_dict['capacity3'] = 1200
    assert test_dict == answer_dict


def test_filter_test_reactors():
    """Test if filter__reactors filters reactors with
       net electricity capacity less than 100Mwe"""
    test = np.array([('foo', 85), ('bar', 1200)],
                    dtype=[('name', 'S10'), ('net_elec_capacity', 'i4')])
    answer = np.array([('bar', 1200)],
                      dtype=[('name', 'S10'), ('net_elec_capacity', 'i4')])
    assert fp.filter_test_reactors(test) == answer


def test_ymd_ceiling():
    """Test if get_ymd gets the correct year, month, and day"""
    ceil = fp.get_ymd(20180225)
    answer = (2018, 3)
    assert ceil == answer


def test_ymd_floor():
    """Test if get_ymd gets the correct year, month, and day"""
    floor = fp.get_ymd(20180301)
    answer = (2018, 3)
    assert floor == answer


def test_lifetime():
    """Test if get_lifetime calculates the right lifetime"""
    start_date = 19700101
    end_date = 20070225
    lifetime = 446
    assert fp.get_lifetime(start_date, end_date) == lifetime


def test_lifetime_no_endtime():
    """Test if get_lifetime calculates the right lifetime
       given no endtime"""
    assert fp.get_lifetime(19700101, -1) == 720


def test_entrytime():
    """Test if get_entrytime calculates the correct entrytime"""
    init_date = 19700101
    start_date = 20070225
    assert fp.get_entrytime(init_date, start_date) == 446


def test_refine_name():
    """Test if name is refined correctly"""
    string = 'Charles(Bukowski)'
    string = string.encode('utf-8')
    assert fp.refine_name(string) == 'Charles'
