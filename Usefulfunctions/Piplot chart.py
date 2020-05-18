import matplotlib.pyplot as plt
import numpy as np


def Piplot1():
    plt.clf()

    # using some dummy data for this example
    xs = np.arange(0, 20, 1)
    ys = np.random.normal(loc=10, scale=2.3, size=20)
    plt.plot(xs, ys)

    # text is left-aligned
    # plt.text(2, 4, 'This text starts at point (2,4)')
    # # text is right-aligned
    # plt.text(8, 3, 'This text ends at point (8,3)', horizontalalignment='right')
    # plt.xticks(np.arange(0, 100, 5))

    plt.xticks(np.arange(0, 20, 2), ['two', 'four', 'six', 'eight', 'ten'])
    plt.yticks(np.arange(0, 20, 2))

    plt.show()


def Piplot2():
    plt.clf()
    # using some dummy data for this example
    xs = np.arange(0, 10, 1)
    ys = np.random.normal(loc=2, scale=0.4, size=10)

    # ------------Bar type ----------------
    plt.bar(xs, ys, label='summary')

    # zip joins x and y coordinates in pairs
    for x, y in zip(xs, ys):
        label = "{:.2f}".format(y)
        plt.annotate(label,  # this is the text
                     (x, y),  # this is the point to label
                     textcoords="offset points",  # how to position the text
                     xytext=(0, 10),  # distance from text to points (x,y)
                     ha='center')  # horizontal alignment can be left, right or center

        # zip joins x and y coordinates in pairs

    # Line type --- Plot --------:
    # using some dummy data for this example
    xs = np.arange(0, 10, 1)
    ys = np.random.normal(loc=4, scale=0.5, size=10)
    # 'bo-' means blue color, round points, solid lines
    plt.plot(xs, ys, 'ro-', label='New Trend')
    for x, y in zip(xs, ys):
        label = "{:.2f}".format(y)

        plt.annotate(label,  # this is the text
                     (x, y),  # this is the point to label
                     textcoords="offset points",  # how to position the text
                     xytext=(0, 10),  # distance from text to points (x,y)
                     ha='center')  # horizontal alignment can be left, right or center

    plt.legend()
    plt.xticks(np.arange(0, 10, 2), ['two', 'four', 'six', 'eight', 'ten'])
    plt.yticks(np.arange(0, 5, 0.5))
    degrees = 70
    plt.xticks(rotation=degrees)

    plt.show()




def Piplot4():
    # using some dummy data for this example
    xs = np.random.normal(loc=4, scale=2.0, size=10)
    ys = np.random.normal(loc=2.0, scale=0.8, size=10)

    plt.scatter(xs, ys)

    # zip joins x and y coordinates in pairs
    for x, y in zip(xs, ys):
        label = "{:.2f}".format(y)

        plt.annotate(label,  # this is the text
                     (x, y),  # this is the point to label
                     textcoords="offset points",  # how to position the text
                     xytext=(0, 10),  # distance from text to points (x,y)
                     ha='center')  # horizontal alignment can be left, right or center

    plt.xticks(np.arange(0, 10, 1))
    plt.yticks(np.arange(0, 5, 0.5))

    plt.show()

def Piplot5():
    fig1 = plt.figure()

    # and the first axes using subplot populated with data
    ax1 = fig1.add_subplot(111)
    line1 = ax1.plot([1, 3, 4, 5, 2], 'o-')
    plt.ylabel("Left Y-Axis Data")

    # now, the second axes that shares the x-axis with the ax1
    ax2 = fig1.add_subplot(111, sharex=ax1, frameon=False)
    line2 = ax2.plot([10, 40, 20, 30, 50], 'xr-')
    ax2.yaxis.tick_right()
    ax2.yaxis.set_label_position("right")
    plt.ylabel("Right Y-Axis Data")

    # for the legend, remember that we used two different axes so, we need
    # to build the legend manually
    plt.legend([line1, line2], ["1", "2"])
    plt.show()

Piplot1()
Piplot2()
Piplot4()
Piplot5()