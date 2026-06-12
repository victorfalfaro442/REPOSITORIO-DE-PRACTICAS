from PIL import Image
import numpy as np

i = Image.open('imagenes/dot.png')
iar = np.asarray(i)
print(iar)

i = Image.open('imagenes/dotndot.png')

iar = np.asarray(i)

print(iar)
	  
####
import matplotlib.pyplot as plt
###
i = Image.open('imagenes/dotndot.png')

iar = np.asarray(i)


plt.imshow(iar)
print(iar)
plt.show()

i = Image.open('imagenes/numbers/y0.4.png')

iar = np.asarray(i)


plt.imshow(iar)
print(iar)
plt.show()	  
