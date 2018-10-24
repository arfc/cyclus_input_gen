# pris-input-gen
Python package for automatic generation of Cyclus input files of nuclear operation history using the International Atomic Energy Agency (IAEA) Power Reactor Information System (PRIS) database.

The IAEA PRIS database is collected and curated (in `database/reactors_pris_2016.csv`),
but there are still missing values, mostly of future planned reactors.

The assumptions for the parameters are as follows:

	Cycle 		= 18 months (timesteps) for all
	Refueling 	= 2 months (timesteps) for all
	assembly mass 	= 180 UO2 / assembly for BWRs
			  		  446 UO2 / assembly for rest [PWR]
	#of assemblies 	= 157 for 1110MWe (PWR)
                      764 for 1098MWe (BWR),
                      linearly adjusted for other capacities

This script allows generation of CYCLUS input file types from csv files.

Input : csv file, initial_time, duration, country_list, [optional: output_file, reprocessing]
	    
    csv_file: the csv file containing country, reactor name and capacity
    
    initial_time: initial time of the simulation in yyyymmdd

    duration: duration of the simulation in months

	country_list: list of countries to extract

	output_file: string for output file path

	reprocessing: adds a reprocessing template if True (1)
    
    
Output : A complete input file ready for simulation. (default: complete_input.xml)
    
To install:
``` python setup.py install ```

Then run:
```
python
import write_input.write_input as wi
wi.main([csv_file], [init_date],[duration], [list_of_countries], [output_file], [reprocessing_bool])
```
