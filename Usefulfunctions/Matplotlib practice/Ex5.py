import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('company_sales_data.csv')
monthList = df['month_number'].tolist()
faceCremSalesData = df['facecream'].tolist()
faceWashSalesData = df['facewash'].tolist()
shampooSalesData = df['shampoo'].tolist()

plt.bar([a - 0.2 for a in monthList], faceCremSalesData, width=0.2, label='Face Cream sales data', align='edge')
plt.bar([a for a in monthList], faceWashSalesData, width=0.2, label='Face Wash sales data', align='edge')
plt.bar([a + 0.2 for a in monthList], shampooSalesData, width=0.2, label='Shampoo sales data', align='edge')
plt.xlabel('Month Number')
plt.ylabel('Sales units in number')
plt.legend(loc='upper left')
plt.title(' Sales data')

plt.xticks(monthList)
# plt.grid(True)
plt.title('Facewash and facecream sales data')
plt.show()
