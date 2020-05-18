import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('company_sales_data.csv')
monthList = df['month_number']
totalUnitList = df['total_units']

plt.plot(monthList, totalUnitList, color='red', linestyle=':',
         label='Profit data of last year', marker='x', markerfacecolor='b')
plt.title('Company sales data of last year')
plt.xlabel('Month Number')
plt.ylabel('Total unit')

plt.xticks(monthList)
plt.yticks([min(totalUnitList), max(totalUnitList), (max(totalUnitList) - min(totalUnitList))/2])
plt.legend(loc=4)
plt.show()