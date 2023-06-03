#!/usr/bin/env python
import sys
import os
import os.path
import pandas as pd
import numpy as np
import umark2
from checkC import checkC

input_dir = sys.argv[1]
output_dir = sys.argv[2]

submission_dir = os.path.join(input_dir, 'res')
orig_dir = os.path.join(input_dir, 'ref')

if not os.path.isdir(submission_dir):
    print("%s doesn't exist" % submission_dir)

if os.path.isdir(submission_dir) and os.path.isdir(orig_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_filename = os.path.join(output_dir, 'scores.txt')
    output_file = open(output_filename, 'w')

    data_id_file = os.path.join(submission_dir, "data_id.txt")
    data_id = open(data_id_file).read()

    orig_file = os.path.join(orig_dir, "orig_data_final_"+str(data_id)+".csv")

    submission_file = os.path.join(submission_dir, "anonymized.csv")

    orig_df = pd.read_csv(orig_file, header=None)
    submission_df = pd.read_csv(submission_file, header=None)
    
    checkC(orig_df, submission_df)

    df = umark2.umark(orig_df, submission_df)
    cnt, rate, coef, OR, pvalue, cor, iloss_age, iloss_bmi, iloss_cat, max, utility = df.loc["max"]

    output_file.write("utility_score:%.4f\n" % utility )
    output_file.write("rate:%.4f\n" % rate)
    output_file.write("cor:%.4f\n" % cor)
    output_file.write("OR:%.4f\n" % OR)
    output_file.write("il_age:%.4f\n" % iloss_age)
    output_file.write("il_bmi:%.4f\n" % iloss_bmi)
    output_file.write("il_cat:%.4f\n" % iloss_cat)
    output_file.close()   
    