import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
 
# Data


data = [(0, 0.46325241104090453), (1, 0.25224476222148323), (2, 0.08696375124709012), (3, 0.05320917858330562), (4, 0.032091785833056205), (5, 0.023112736947123378), (6, 0.014632524110409046), (7, 0.010142999667442634), (8, 0.008480212836714332), (9, 0.009810442301296974), (10, 0.007316262055204523), (11, 0.004323245759893582), (12, 0.004489524442966412), (13, 0.005487196541403392), (14, 0.0039906883937479215), (15, 0.002494180246092451), (16, 0.0013302294645826404), (17, 0.0016627868307283007), (18, 0.0016627868307283007), (19, 0.0011639507815098104), (20, 0.0013302294645826404), (21, 0.0013302294645826404), (22, 0.0008313934153641503), (23, 0.0011639507815098104), (24, 0.0014965081476554707), (25, 0.0006651147322913202), (26, 0.0011639507815098104), (27, 0.0003325573661456601), (28, 0.0006651147322913202), (29, 0.0006651147322913202), (30, 0.00016627868307283005), (31, 0.0003325573661456601), (33, 0.00016627868307283005), (34, 0.00016627868307283005), (35, 0.00016627868307283005), (38, 0.0004988360492184902), (39, 0.00016627868307283005), (42, 0.00016627868307283005), (54, 0.00016627868307283005), (55, 0.00016627868307283005), (64, 0.00016627868307283005), (72, 0.00016627868307283005)]
x = [elem[0] for elem in data]
#y = [elem[1]*100 for elem in data]

cum_percentage = 0
y = []
for elem in data: 
    freq = elem[1]
    cum_percentage += (freq*100)
    y.append(cum_percentage)


df=pd.DataFrame({'x': x, 'y': y })
 
# multiple line plot
plt.plot( 'x', 'y', data=df, marker='D', markerfacecolor='black', markersize=4, color='black', linewidth=1, rasterized=True)
plt.grid(b=True, axis='y')
#plt.ylim(ymax = 0.4, ymin = 0 )
#plt.yticks(np.arange(0, 100, step=5))
#plt.xticks(np.arange(0,max(x)+5, step=5))
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

