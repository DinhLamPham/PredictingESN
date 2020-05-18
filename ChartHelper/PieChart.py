import numpy as np
import matplotlib.pyplot as plt


def DataFrameToPieChart(df, ouputFileName, typeCode=0):
    listColumn = list(df.columns.values)
    listOccurent = []
    listDuration = []
    for col in listColumn:
        listOccurent.append(df[col][0])
        listDuration.append(df[col][1])

    fig, ax = plt.subplots(subplot_kw=dict(aspect="equal"))
    data = (listOccurent)
    if typeCode == 1:
        data = listDuration

    def func(pct, allvals):
        absolute = int(pct/100.*np.sum(allvals))
        # return "{:.1f}%\n({:d} times)".format(pct, absolute)
        return "{:.1f}%".format(pct, absolute)

    wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                      textprops=dict(color="w"))
    ax.legend(wedges, listColumn,
              title="Name",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=8, weight="bold")
    # ax.set_title("Percentage of ouccrence times")
    plt.savefig(ouputFileName, bbox_inches='tight')
