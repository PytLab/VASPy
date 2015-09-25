import sys
import numpy as np
import matplotlib.pyplot as plt
from vaspy.plotter import DataPlotter

# get filename
if len(sys.argv) <= 1:
    print "Usage: plot_cohp.py filename."
    sys.exit(1)
else:
    filename = sys.argv[1]
# get data
cohp = DataPlotter(filename=filename)
npt = cohp.data.shape[0]
E = cohp.data[:, 0]
x1 = cohp.data[:, 1]
x2 = cohp.data[:, 2]
maxnum = np.max(cohp.data)
minnum = np.min(cohp.data)
maxE = np.max(cohp.data[:, 0])
minE = np.min(cohp.data[:, 0])
hori_line = np.linspace(minnum, maxnum, 100)
vert_line = np.linspace(minE, maxE, 100)

# plot
fig = plt.figure(figsize=(7, 14))
ax = fig.add_subplot(111)
ax.plot(x1, E, linewidth=5, color='#4A708B')
ax.plot(x2, E, linewidth=5, color='#CD5C5C')
# add zero dashed line
ax.plot(hori_line, np.array([0.0]*100), linestyle='dashed', color='#000000')
ax.plot(np.array([0.0]*100), vert_line, linestyle='dashed', color='#000000')
ax.set_ylabel(r'$\bf{E - E_F(eV)}$', fontdict={'fontsize': 15})
fig.show()
