import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('company_sales_data.csv')
monthList = df['month_number'].tolist()
profitList = df['total_profit'].tolist()

plt.plot(monthList, profitList, label='Total profit over months')
plt.xlabel('Month number')
plt.ylabel('Total profit')

plt.xticks(monthList, rotation=70)
ytick = []
step = (max(profitList) - min(profitList))/10
ytick = [min(profitList) + i * step for i in range(10)]
plt.yticks(ytick, rotation=30)
plt.legend()
plt.title('Company profit in 2019')
plt.show()