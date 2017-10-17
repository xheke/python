import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

%matplotlib inline

dti = pd.date_range('2016/01/01', freq='M', periods=12)
rnd = np.random.standard_normal(len(dti)).cumsum()**2
df = pd.DataFrame(rnd, columns=['data'], index=dti)
df.plot()
plt.show()



