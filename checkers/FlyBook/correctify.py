#!/usr/bin/env python2
from PIL import Image
import random
import sys

def setbit(n, bit):
  if bit == 0:
    return n & 0b11111110
  return n | 1

if len(sys.argv) != 3:
  print "USAGE: ./correctify.py <image> <host>"
  sys.exit(1)

filename = sys.argv[1]
image = Image.open(filename)
s = ''
w, h = image.size

true = '100011010010111000010111010011110101000110001011'
host = sys.argv[2]
binhost = bin(int(host))[2:]

for i in range(len(binhost)):
  true = true[:i] + str((int(true[i]) + int(binhost[i])) % 2) + true[i + 1:]

pixels = w * h
t = 0
while 2 * len(true) <= 3 * pixels:
  r = ''
  i, j, k = 0, 0, 0
  while i < 2 * len(true):
    if j & 4 > 0:
      r += true[k]
      k += 1
    else:
      r += str(random.randint(0, 1))
    if j & 2 > 0:
      r += true[k]
      k += 1
    else:
      r += str(random.randint(0, 1))
    if j & 1 > 0:
      r += true[k]
      k += 1
    else:
      r += str(random.randint(0, 1))

    i += 3
    j += 1
    j %= 8
  true = r

image = image.convert("RGB")

result = Image.new("RGB", (w, h), (0, 0, 0, 0))

for i in xrange(w):
  for j in xrange(h):
    pos = h * i + j
    if 3 * pos < len(true):
      pixel = image.getpixel((i, j))
      if len(pixel) > 3:
        pixel = pixel[:3]
      r, g, b = pixel
      result.putpixel((i, j), (setbit(r, int(true[3 * pos])) , setbit(g, int(true[3 * pos + 2])), setbit(b, int(true[3 * pos + 1]))))
    else:
      result.putpixel((i, j), image.getpixel((i, j)))

result.save(filename + "." + host + ".png")

