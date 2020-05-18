import matplotlib.pyplot as plt
import pandas as pd
from CommonHelper.GVar import *
import numpy as np


def DataFrameToBarChart(df, ouputFileName, typeCode=0):
    # plt.savefig(ouputFileName, bbox_inches='tight')
    # libraries
    # Make a fake dataset
    listColumn = list(df.columns.values)
    listOccurent = []
    listDuration = []
    for col in listColumn:
        listOccurent.append(df[col][0])
        listDuration.append(df[col][1])

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.set_xlabel('Name')
    ax1.set_ylabel('Number of occurence')

    ax2.set_ylabel('Duration (hours)')

    x_pos = np.arange(len(listColumn))
    dataAx1 = listOccurent
    dataAx2 = listDuration

    ax1.bar([a - 0.1 for a in x_pos], dataAx1, width=0.1, color='green', label='Occurence')
    ax1.legend(loc='upper left')

    ax2.bar([a + 0.1 for a in x_pos], dataAx2, width=0.1, color='blue', label='Duration')
    ax2.legend(loc='upper right')
    plt.xticks(x_pos, listColumn)
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=90)

    plt.savefig(ouputFileName, bbox_inches='tight')


def TraceInfoToBarChart(df, ouputFileName, showact=True, showper=True, showduration=True):
    listColumn = list(df.columns.values)
    traceIdList, activityOccurenceList, performerOccurenceList, duractionList = [], [], [], []

    traceIdList = list(df.iloc[:, 0])  # first column of data frame (first_name)
    activityOccurenceList = list(df.iloc[:, 1])  # second column of data frame
    performerOccurenceList = list(df.iloc[:, 2])  # third column of data frame
    duractionList = list(df.iloc[:, 3])  # fourth column of data frame

    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Trace Id')
    ax1.set_ylabel('Number of occurence')

    ax2 = ax1.twinx()
    if showact or showper:
        if showper:
            ax1.bar([int(a) + 0.1 for a in traceIdList], [int(a) for a in performerOccurenceList], width=0.1,
                    label="Performer", align="center", color='y')
        if showact:
            ax1.bar([int(a) - 0.1 for a in traceIdList], [int(a) for a in activityOccurenceList], width=0.1,
                    label="Activity", align="center", color='g')
        ax1.legend(loc='upper left')

    if showduration:
        ax2.plot([int(a) for a in traceIdList], [int(a) for a in duractionList], 'r-', label="Duration")
        ax2.set_ylabel('Duration (Hours)')
        ax2.legend(loc='upper right')

    plt.savefig(ouputFileName, bbox_inches='tight')
    print("Finished!")
