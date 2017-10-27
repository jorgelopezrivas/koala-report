# Security Levels
# Example of use
# df = load_security_levels('SecurityLevels-BBVA.txt')
# level = get_this_level(df, 'MH', 'L')

import pandas as pd
	
def load_security_levels(filename):
	df = pd.read_csv(filename,  delimiter=None, delim_whitespace=True)
	return df
	

def get_this_level(df, sisl, assl):
	query_str = "SID == '" + sisl + "' & AS == '" + assl + "'"
	row = df.query(query_str)
	# Always returns one row, so to allow easy access we do:
	return row.iloc[0]

	


	
	

