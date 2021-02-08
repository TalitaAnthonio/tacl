import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
 
# Data


data = [(0, 0.4632768361581921), (1, 0.2520771020272516), (2, 0.08707211698238618), (3, 0.053173811897640415), (4, 0.032070455300764376), (5, 0.02326354270521768), (6, 0.014622798271851114), (7, 0.010136257892987704), (8, 0.00847457627118644), (9, 0.00980392156862745), (10, 0.007311399135925557), (11, 0.004320372216683284), (12, 0.00448654037886341), (13, 0.005483549351944167), (14, 0.003988035892323031), (15, 0.0024925224327018943), (16, 0.0013293452974410102), (17, 0.001661681621801263), (18, 0.001661681621801263), (19, 0.001163177135260884), (20, 0.0013293452974410102), (21, 0.0013293452974410102), (22, 0.0008308408109006315), (23, 0.001163177135260884), (24, 0.0014955134596211367), (25, 0.0006646726487205051), (26, 0.001163177135260884), (27, 0.00033233632436025255), (28, 0.0006646726487205051), (29, 0.0006646726487205051), (30, 0.00016616816218012627), (31, 0.00033233632436025255), (33, 0.00016616816218012627), (34, 0.00016616816218012627), (35, 0.00016616816218012627), (38, 0.0004985044865403788), (39, 0.00016616816218012627), (42, 0.00016616816218012627), (54, 0.00016616816218012627), (55, 0.00016616816218012627), (64, 0.00016616816218012627), (72, 0.00016616816218012627)]
x = [elem[0] for elem in data]
y = [elem[1]*100 for elem in data]

df=pd.DataFrame({'x': x, 'y': y })
 
# multiple line plot
plt.plot( 'x', 'y', data=df, marker='D', markerfacecolor='black', markersize=4, color='black', linewidth=1, rasterized=True)
plt.grid(b=True, axis='y')
#plt.ylim(ymax = 0.4, ymin = 0 )
plt.yticks(np.arange(0, 55, step=5))
plt.xticks(np.arange(0,max(x)+5, step=5))
plt.xlabel('sentences prior', fontweight='bold')
plt.ylabel('percentage reference resolved', fontweight='bold')

for xpoint,ypoint in zip(x[0:5],y[0:5]):
    label = ypoint
    ypoint_rounded = "{0} % ".format(round(label, 2))

    plt.annotate(ypoint_rounded, # this is the text
                (xpoint,ypoint), # this is the point to label
                textcoords="offset points", # how to position the text
                xytext=(2,1), # distance from text to points (x,y)
                ha='left') # horizontal alignment can be left, right or center

print(x[:4])

for xpoint,ypoint in zip(x,y):
    label = ypoint
    
    if xpoint == 55: 
        ypoint_rounded = "{0} % ".format(round(label, 2))

        plt.annotate(ypoint_rounded, # this is the text
                    (xpoint,ypoint), # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(2,1), # distance from text to points (x,y)
                    ha='left') # horizontal alignment can be left, right or center

#plt.show()
plt.savefig('sentences-prior-distr.jpg', format='jpg', dpi=1200)

