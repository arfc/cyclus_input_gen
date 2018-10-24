# pris-input-gen
Python package for automatic generation of Cyclus input files of nuclear operation history using the International Atomic Energy Agency (IAEA) Power Reactor Information System (PRIS) database

The assumptions for the parameters are as follows:

	Cycle 		= 18 months (timesteps) for all
	Refueling 	= 2 months (timesteps) for all
	assembly mass 	= 180 UO2 / assembly for BWRs
			  		  523.4 UO2 / assembly for rest [PWR]
	#of assemblies 	= 193 for 1110MWe (PWR)
                      830 for 1098MWe (BWR),
                      linearly adjusted for other capacities

This script allows generation of CYCLUS input file types from csv files.

Input : csv file, initial_time, duration, reprocessing 


	    
    csv_file: the csv file containing country, reactor name and capacity
    
    initial_time: initial time of the simulation in yyyymmdd

    duration: duration of the simulation in months
    
    
Output : A complete input file ready for simulation. (default: complete_input.xml)
    
To run:

	python write_reactors.py [csv_file] [init_time] [duration]