'''
    Script to plot total force trend.
'''
import matplotlib.pyplot as plt
from vaspy.iter import OutCar

outcar = OutCar()
# plot
fig = plt.figure(figsize=(12, 7))
ax = fig.add_subplot(111)
ax.plot(outcar.total_forces, linewidth=5, color='#36648B')
ax.set_xlabel(r'$Step$')
ax.set_ylabel(r'$Total Force(eV/Angst)$')
plt.show()  # use plt to avoid window being closed
