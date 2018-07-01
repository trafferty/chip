#!/usr/bin/env python3

import argparse
import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def parse_temp_data(temp_dat_file):

    '''
    timestamp, temp (C), temp (F)
    2018-06-30 18:41:30, 25.062000, 77.111600
    2018-06-30 18:41:40, 25.062000, 77.111600
    '''

    temp_dat = pd.read_csv(temp_dat_file)




def plot_disp_metrics(dispense_metrics):
    deltas = []
    dispensed = []
    targets = []
    dates = []
    for metric in dispense_metrics:
        try:
            delta = float(metric['delta'])
            dispensed_amount = float(metric['dispensed_amount'])
            target_amount = float(metric['target_amount'])
            date = metric['date'].split(' ')[0]
        except ValueError:
            continue
        deltas.append(delta)
        dispensed.append(dispensed_amount)
        targets.append(target_amount)
        dates.append(date)

    fig, ax = plt.subplots()
    if 1:
        t = range(0, len(deltas))
        plt.plot(t, dispensed, t, targets, t, deltas)
        plt.xlabel("Dispense Operations.  Max Delta: %d, Min Delta %d, Mean Delta: %1.1f" % (np.max(deltas), np.min(deltas), np.mean(deltas)))
        plt.ylabel('grams')
        plt.legend(['Dispensed amount', 'Target amount', 'Delta'], loc = 'upper right')
        ax.set_ylim(min(deltas) - 20, max(max(dispensed), max(targets)) + 20)
        #plt.annotate('Data gathering drinks', xy=(5,150))
        #plt.annotate('MC tweaks to parms', xy=(14,150))
        #plt.annotate('restart MC', xy=(31,150))
        #plt.annotate('restart MC', xy=(39,150))

        #for idx, delta in enumerate(deltas):
            #plt.annotate('%2.1fg' % delta, xy=(idx, delta))
    else:

        index = np.arange(len(deltas))
        bar_width = 0.25
        opacity = 0.4

        rects1 = plt.bar(index, dispensed, bar_width,
                         alpha=opacity,
                         color='r',
                         label='Actual Amount')

        rects2 = plt.bar(index + bar_width, targets, bar_width,
                         alpha=opacity,
                         color='b',
                         label='Target Amount')

        plt.xlabel('Dispense Operations')
        plt.ylabel('grams')
        plt.title('Dispense operations: Target vs Actual')
        #plt.xticks(index + bar_width, ('A', 'B', 'C', 'D', 'E'))
        plt.legend()
        #plt.tight_layout()
        yloc = max(max(targets), max(dispensed)) 
        for idx, delta in enumerate(deltas):
            plt.annotate('%2.1fg' % delta, xy=(idx, dispensed[idx]))

    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse out dispense metric data from an MC-produced log')
    parser.add_argument('-d', '--disp_log_file', type=str, default="", help='log file with raw disp data in it')
    parser.add_argument('-s', '--start_date', dest='start_date', type=str,
                        help='(optional) date to start parsing in the form of mm/dd/yyyy', default='')
    args = parser.parse_args()

    if len(args.disp_log_file):
        dispense_metrics = parse_disp_data(args.disp_log_file, args.start_date)
        plot_disp_metrics(dispense_metrics)
    else:  
        print "Must specify file name for disp log"
