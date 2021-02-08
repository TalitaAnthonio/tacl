# libraries
import numpy as np
import matplotlib.pyplot as plt
 
# set width of bar
barWidth = 0.25
 
# set height of bar
bars1 = [2599, 1137, 120] # unigrams 
bars2 = [0,700,1372] # bigrams 
bars3 = [0,0,90] # trigrams 
 
# Set position of bar on X axis
r1 = np.arange(len(bars1))

r2 = [x + barWidth for x in r1]

#print(r2)
r3 = [x + barWidth for x in r2]
 
# Make the plot
plt.bar(r1, bars1, color='#FFC300', width=barWidth, edgecolor='white', label='unigram-reference')
plt.bar(r2, bars2, color='#FF5733', width=barWidth, edgecolor='white', label='bigram-reference')
plt.bar(r3, bars3, color='#C70039', width=barWidth, edgecolor='white', label='trigram-reference')


for x,y in zip(r1,bars1):


    label = y 

    plt.annotate(label, # this is the text
                (x,y), # this is the point to label
                textcoords="offset points", # how to position the text
                xytext=(0,1), # distance from text to points (x,y)
                ha='center') # horizontal alignment can be left, right or center

for x,y in zip(r2,bars2):

    label = y 
    if label != 0: 

        plt.annotate(label, # this is the text
                    (x,y), # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(0,1), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center

for x,y in zip(r3,bars3):

    label = y 
    if label != 0: 

        plt.annotate(label, # this is the text
                    (x,y), # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(0,1), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center


# Add xticks on the middle of the group bars
plt.xlabel('insertion type', fontweight='bold')
plt.ylabel('Frequency', fontweight='bold')
print([r + barWidth for r in range(len(bars1))])
plt.xticks([r + barWidth for r in range(len(bars1))], ['unigram', 'bigram', 'trigram'])


# Create legend & Show graphic
plt.legend()
plt.show()
plt.savefig('reference-frequency.jpg', format='jpg', dpi=1200)
