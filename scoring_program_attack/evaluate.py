#!/usr/bin/env python
import sys
import os.path
from lmark2 import lmark
import pandas as pd
from checkE import checkE

input_dir = sys.argv[1]
output_dir = sys.argv[2]

submission_dir = os.path.join(input_dir, 'res')
orig_dir = os.path.join(input_dir, 'ref')

num_of_team = 10

with open(os.path.join(submission_dir, "my_team_id.txt")) as my_team:
    my_team_id = int(my_team.read())

if not os.path.isdir(submission_dir):
    print("%s doesn't exist" % submission_dir)

if os.path.isdir(submission_dir) and os.path.isdir(orig_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    score = [0] * (num_of_team + 1) # Note: Team ID starts with 1
    
    for i in range(1, num_of_team + 1):
        if i == my_team_id:
            continue
            
        estimate_file = os.path.join(submission_dir, "estimated_team%02d.csv" % i)
        answer_file = os.path.join(orig_dir, "correct_team%02d.csv" % i)

        dfX = pd.read_csv(answer_file, header=None)
        if os.path.exists(estimate_file):
            dfE = pd.read_csv(estimate_file, header=None)
            checkE(dfE) # Format & value check
            score[i] = lmark(dfE, dfX)
        else:
            score[i] = 1.0 # No Estimate index submitted. Privacy score will be 1.0

    output_filename = os.path.join(output_dir, 'scores.txt')
    with open(output_filename, mode="w") as f:        
        f.writelines("attack_score:%.4f\n" % (1 - (sum(score)) / (num_of_team - 1)))
        for i in range(1, num_of_team + 1):
            if i == my_team_id:
                continue # Preventing suicideal attack
            f.writelines("privacy_score_%d:%.4f\n" % (i, score[i]))