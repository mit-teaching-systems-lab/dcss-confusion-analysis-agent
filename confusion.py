import argparse, os, random, re, shutil, sys
import pickle
import parselmouth
import pandas as pd
from feature_extraction_utils import *

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="The local file name to process")

def extract_audio_features(filename):

	"""
	MIT License

	Copyright (c) 2019 Ongun Uzay Macar

	Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

	The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

	retrieved from https://github.com/uzaymacar/simple-speech-features/main.ipynb
	"""

	sound = parselmouth.Sound(filename)
	df = pd.DataFrame()
	attributes = {}

	intensity_attributes = get_intensity_attributes(sound)[0]
	pitch_attributes = get_pitch_attributes(sound)[0]
	attributes.update(intensity_attributes)
	attributes.update(pitch_attributes)

	hnr_attributes = get_harmonics_to_noise_ratio_attributes(sound)[0]
	gne_attributes = get_glottal_to_noise_ratio_attributes(sound)[0]
	attributes.update(hnr_attributes)
	attributes.update(gne_attributes)

	df['local_jitter'] = None
	df['local_shimmer'] = None
	df.at[0, 'local_jitter'] = get_local_jitter(sound)
	df.at[0, 'local_shimmer'] = get_local_shimmer(sound)

	spectrum_attributes = get_spectrum_attributes(sound)[0]
	attributes.update(spectrum_attributes)

	formant_attributes = get_formant_attributes(sound)[0]
	attributes.update(formant_attributes)

	#lfcc_matrix, mfcc_matrix = get_lfcc(sound), get_mfcc(sound)
	#df['lfcc'] = None
	#df['mfcc'] = None
	#df.at[0, 'lfcc'] = lfcc_matrix
	#df.at[0, 'mfcc'] = mfcc_matrix

	#delta_mfcc_matrix = get_delta(mfcc_matrix)
	#delta_delta_mfcc_matrix = get_delta(delta_mfcc_matrix)
	#df['delta_mfcc'] = None
	#df['delta_delta_mfcc'] = None
	#df.at[0, 'delta_mfcc'] = delta_mfcc_matrix
	#df.at[0, 'delta_delta_mfcc'] = delta_delta_mfcc_matrix

	for attribute in attributes:
		df.at[0, attribute] = attributes[attribute]

	df.at[0, 'wav_filename'] = filename
	rearranged_columns = df.columns.tolist()[-1:] + df.columns.tolist()[:-1]
	df = df[rearranged_columns]

	return df

def classify(filename):


	features = ['local_jitter', 'local_shimmer', 'min_intensity', 'relative_min_intensity_time',
		   'max_intensity', 'relative_max_intensity_time', 'mean_intensity',
		   'stddev_intensity', 'q1_intensity', 'median_intensity', 'q3_intensity',
		   'voiced_fraction', 'min_pitch', 'relative_min_pitch_time', 'max_pitch',
		   'relative_max_pitch_time', 'mean_pitch', 'stddev_pitch', 'q1_pitch',
		   'q3_pitch', 'mean_absolute_pitch_slope',
		   'pitch_slope_without_octave_jumps', 'min_hnr', 'relative_min_hnr_time',
		   'max_hnr', 'relative_max_hnr_time', 'mean_hnr', 'stddev_hnr', 'min_gne',
		   'max_gne', 'mean_gne', 'stddev_gne', 'sum_gne', 'band_energy',
		   'band_density', 'band_energy_difference', 'band_density_difference',
		   'center_of_gravity_spectrum', 'stddev_spectrum', 'skewness_spectrum',
		   'kurtosis_spectrum', 'central_moment_spectrum', 'f1_mean', 'f2_mean',
		   'f3_mean', 'f4_mean', 'f1_median', 'f2_median', 'f3_median',
		   'f4_median', 'formant_dispersion', 'average_formant', 'mff',
		   'fitch_vtl', 'delta_f', 'vtl_delta_f']

	# Just some non-sense to make this do "something"
	loaded_clf = pickle.load(open('./confusion_mp3.pickle', 'rb'))
	audio_feaures = extract_audio_features(filename)
	return loaded_clf.predict(audio_feaures[features])

def main():
	args = parser.parse_args()

	if args.file == '':
		sys.exit('--file is empty')

	result = classify(args.file)
	sys.stdout.write(str(result[0]))


if __name__ == "__main__":
	main()
