from CooperVicon import CooperVicon
import matplotlib.pyplot as plt
import time
import numpy as np
import scipy.stats as stats

test = CooperVicon()
# test.getObjectsData()
# test.printObjects()
test.getObjectNames()

#Setup a figure
# plt.figure(1)
dts=[]
i=0
while i < 100:
    t1 = time.time()
    test.getFrame()
    state = test.getObjectGlobalState('pencil')
    # state.pretty_print()

    t2 = time.time()
    dt = t2-t1
    dts.append(dt)
    # plt.plot(t, state.translation[2], 'r*', markersize=2)
    # plt.show(block=False)
    # plt.pause(0.0001)
    if((t2-t1 < 0.01)):
        time.sleep(0.01 - (t2-t1))
    i += 1

plt.figure(1)
plt.plot(dts, stats.norm.pdf(dts))
std = np.var(dts)
mean = np.mean(dts)
print("mean: ", mean, " | stddev: ", std)

plt.show()
