import mingus.containers
import mingus.containers.note
import mingus.extra.lilypond as lp
import mingus
from mingus.containers import Note
import cv2
import numpy as np



n = Note()

print(n)

n.set_note("A", 5)

lilyString = lp.from_Note(n)

lp.to_png(lilyString, "test")

img = cv2.imread("test.png")

### 100x20 - 180x80

img = img[20:80, 100:180, :]

cv2.imwrite("test2.png", img)


l = [("E", 2), 
     ("F", 2), 
     ("G", 2), 
     ("A", 2), 
     ("B", 2), 
     ("C", 3), 
     ("D", 3), 
     ("E", 3), 
     ("F", 3), 
     ("G", 3), 
     ("A", 3), 
     ("B", 3), 
     ("C", 4), 
     ("D", 4), 
     ]


for i in range(14):
    #letter = chr((((i)%7)+65))
    #octave = (i//7) + 2
    #print(letter, octave)
    letter = l[i][0]
    octave = l[i][1]
    n.set_note(*l[i])

    lilyString = lp.from_Note(n, clef="bass")
    print(lilyString)
    lp.to_png(lilyString, f"{letter}{octave}")

    img = cv2.imread(f"{letter}{octave}.png")
    img = img[20:80, 100:180, :]

    cv2.imwrite(f"{letter}{octave}.png", img)
