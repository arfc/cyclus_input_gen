# cyclus-input-gen
Python package for automatic generation of Cyclus input files.


To install:
``` python setup.py install ```

Then import it anywhere using:
``` import cyclus_input_gen.[module_name] ```

## from_pris
Generates Cyclus input file of nuclear operation history using the International Atomic Energy Agency (IAEA) Power Reactor Information System (PRIS) database.

The IAEA PRIS database is collected and curated (in `database/world_reactors.csv`),
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
    
Then run:
```
python
import cyclus_input_gen.from_pris as fp
fp.main([csv_file], [init_date],[duration], [list_of_countries], [output_file], [reprocessing_bool])
```

## templates
Contains templates to be used in `from_pris`


## demand_deploy
Calculates deploy array to meet a power demand equation.
Also generates Cycamore::DeployInst xml block from the calculated deploy array


## Misc.

### CANDU calculation for `from_pris.py`
Galeriu and Melintescu - Technical characteristics of the CANDU reactor
CANDU 6 ( 700 MWe)
19.36 kg per bundle
4560 bundles in core
12 bundle per channel
average of six fuel bundles in channel exchanged
10 fuel channels per week
-> 6*10 = 60 bundles refueling per week
-> 6*10*4 = 240 bundles refueling per month