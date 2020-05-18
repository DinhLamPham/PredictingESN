import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('company_sales_data.csv')
columnName = list(df.columns)[1:len(df.columns)-2]

monthList = df.iloc[:, 0].tolist()

for col in columnName:
    plt.scatter(monthList, df[col], label=col, alpha=1)

plt.legend()
plt.title('Sales data over year 2019')
plt.xlabel('Month number')
plt.ylabel('Sale data')
plt.show()
