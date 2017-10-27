import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np

def readAndCleanData(filename):
	excel = pd.read_excel(filename, 'Report')
	# quitar columnas no utilizadas para el reporte y asignar nombres
	data = excel[[1,2,4,5,6,7,8,9]]
	data.columns = ['folio','identificacion','tipo','fecha','configuracion','resultado g','resultado v', 'detalles']
	# quitar renglones con basura
	data = data.drop(data.index[:3])
	return data

def getFloatField(field, src):
	regexp= '(' + field+ '=)(-*\d+\.\d+)'
	res = re.search(regexp, str(src))
	if res is not None:
		return float(res.group(2))
	else:
		return -1000.00
		
def parseDetails(df):
	columns = ['netSpeech', 'saturation', 'snr', 'speechRatio', 'confidence', \
		'ivrScore', 'mobileLQLSScore','mobileMQLSScore','sameRecAsScore','sidScore']
	for col in columns:
		newColumn = []
		for row in df['detalles']:
			newColumn.append(getFloatField(col, row))
		df[col] = newColumn
	return df
		
	#todo:sisl
	#todo:assl
	#todo: param	
	
def processWindowThreshold(df, th, column, invalid=-1000, inverted=False):
	total = df.shape[0]
	
	
def processSimpleThreshold(df, th, column, invalid=-1000, inverted=False):
	
	# Get rows without  invalid values
	total = df.shape[0]
	invalid_df = df.loc[df[column] == invalid]
	invalid_count = invalid_df.shape[0]
	valid_df = df.loc[df[column] != invalid]
	valid_count = valid_df.shape[0]
	accepted_df = valid_df.loc[valid_df[column] >= th]
	accepted_count = accepted_df.shape[0]
	rejected_df = valid_df.loc[valid_df[column] < th]
	rejected_count = rejected_df.shape[0]
	
	fig, ax = plt.subplots()

	# A represents accepted, B represents Rejected

	a_heights , a_bins = np.histogram(accepted_df[column])
	b_heights , b_bins = np.histogram(rejected_df[column], bins=a_bins.shape[0])
	if inverted:
		ax.bar(a_bins[:-1], a_heights, width=(a_bins[1] - a_bins[0]), facecolor='red')
		ax.bar(b_bins[:-1], b_heights, width=(b_bins[1] - b_bins[0]), facecolor='green')
	else:
		ax.bar(a_bins[:-1], a_heights, width=(a_bins[1] - a_bins[0]), facecolor='green')
		ax.bar(b_bins[:-1], b_heights, width=(b_bins[1] - b_bins[0]), facecolor='red')
	plt.axvline(th, color='blue', linestyle='dashed', linewidth=2, label='th=' + str(th))
	plt.xlabel("Score")
	plt.ylabel("Count")
	plt.title(column)
	plt.legend()
	plt.grid(True)
	if inverted:
		figtext = "total %d, invalidos %d, validos %d (100%%), rechazados %d (%.2f%%), aceptados %d (%.2f%%)" % (total, \
			invalid_count,  valid_count, \
			accepted_count, (float(accepted_count) / float(valid_count) * 100), \
			rejected_count, (float(rejected_count) / float(valid_count) * 100))	
	else:
		figtext = "total %d, invalidos %d, validos %d (100%%), aceptados %d (%.2f%%), rechazados %d (%.2f%%)" % (total, \
			invalid_count,  valid_count, \
			accepted_count, (float(accepted_count) / float(valid_count) * 100), \
			rejected_count, (float(rejected_count) / float(valid_count) * 100))
	plt.figtext(0.5, 0.003,figtext, horizontalalignment='center', fontsize=12)
	plt.show()
	

	
#####################################################################
# Main
#####################################################################
data = readAndCleanData('sample_report.xlsx')
data = parseDetails(data)

#processNetSpeech(data)
#processSimpleThreshold(data, 1.55, "netSpeech")
#processSimpleThreshold(data, 10, "saturation", inverted=True)
#processSimpleThreshold(data, 20, "snr")
#processSimpleThreshold(data, 0.17, "speechRatio")
#processSimpleThreshold(data, 0, "confidence")
processSimpleThreshold(data, 9, "ivrScore", inverted=True)
