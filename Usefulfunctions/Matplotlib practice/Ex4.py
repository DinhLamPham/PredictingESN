import numpy as np
import matplotlib.pyplot as plt

# Fixing random state for reproducibility
# np.random.seed(19680801)

def Scatter1():
    N = 50
    x = np.random.rand(N)
    x = [a*50 for a in x]
    y = np.random.rand(N)
    colors = np.random.rand(N)
    area = (50 * np.random.rand(N))**2.2  # 0 to 15 point radii

    plt.scatter(x, y, s=area, c=colors, alpha=0.3)
    plt.grid(True)
    plt.show()

def Scatter2():
    N = 45
    x, y = np.random.rand(2, N)
    c = np.random.randint(1, 5, size=N)
    s = np.random.randint(10, 220, size=N)

    fig, ax = plt.subplots()

    scatter = ax.scatter(x, y, c=c, s=s)

    # produce a legend with the unique colors from the scatter
    legend1 = ax.legend(*scatter.legend_elements(),
                        loc="lower left", title="Classes")
    ax.add_artist(legend1)

    # produce a legend with a cross section of sizes from the scatter
    handles, labels = scatter.legend_elements(prop="sizes", alpha=0.6)
    legend2 = ax.legend(handles, labels, loc="upper right", title="Sizes")

    plt.show()

def Scatter3():
    volume = np.random.rayleigh(27, size=40)
    amount = np.random.poisson(10, size=40)
    ranking = np.random.normal(size=40)
    price = np.random.uniform(1, 10, size=40)

    fig, ax = plt.subplots()

    # Because the price is much too small when being provided as size for ``s``,
    # we normalize it to some useful point sizes, s=0.3*(price*3)**2
    scatter = ax.scatter(volume, amount, c=ranking, s=0.3 * (price * 3) ** 2,
                         vmin=-3, vmax=3, cmap="Spectral")

    # Produce a legend for the ranking (colors). Even though there are 40 different
    # rankings, we only want to show 5 of them in the legend.
    legend1 = ax.legend(*scatter.legend_elements(num=5),
                        loc="upper left", title="Ranking")
    ax.add_artist(legend1)

    # Produce a legend for the price (sizes). Because we want to show the prices
    # in dollars, we use the *func* argument to supply the inverse of the function
    # used to calculate the sizes from above. The *fmt* ensures to show the price
    # in dollars. Note how we target at 5 elements here, but obtain only 4 in the
    # created legend due to the automatic round prices that are chosen for us.
    kw = dict(prop="sizes", num=5, color=scatter.cmap(0.7), fmt="$ {x:.2f}",
              func=lambda s: np.sqrt(s / .3) / 3)
    legend2 = ax.legend(*scatter.legend_elements(**kw),
                        loc="lower right", title="Price")

    plt.show()


Scatter2()
Scatter3()