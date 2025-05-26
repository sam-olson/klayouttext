import math
import pya

WIDTH = 15000
HEIGHT = 2000
LETTER_SPACE = WIDTH * 2
LINE_SPACE = HEIGHT * 4 + 2*WIDTH

ENCODING = {"0": 0xC3F,
            "1": 0x406,
            "2": 0xDB,
            "3": 0x8F,
            "4": 0xE6,
            "5": 0xED,
            "6": 0xFD,
            "7": 0x1401,
            "8": 0xFF,
            "9": 0xE7,
            "A": 0xF7,
            "B": 0x128F,
            "C": 0x39,
            "D": 0x120F,
            "E": 0xF9,
            "F": 0xF1,
            "G": 0xBD,
            "H": 0xF6,
            "I": 0x1209,
            "J": 0x1E,
            "K": 0x2470,
            "L": 0x38,
            "M": 0x536,
            "N": 0x2136,
            "O": 0x3F,
            "P": 0xF3,
            "Q": 0x203F,
            "R": 0x20F3,
            "S": 0x18D,
            "T": 0x1201,
            "U": 0x3E,
            "V": 0xC30,
            "W": 0x2836,
            "X": 0x2D00,
            "Y": 0x1500,
            "Z": 0xC09}

def segments(encoding, scale=1):
  """
  Function for creating determining coordinates of segment corners based on given encoding (per 14 segment protocol)

  Parameters
  ----------
  encoding: hex value encoding which segments to include for a given character (see ENCODING table above)
  scale: relative scale of segment size (default 1 for a 15 x 2 um segment)

  Returns
  ----------
  list of segment definition coordinates
  """

  w = WIDTH*scale
  h = HEIGHT*scale
  seg = []
  
  # segment A
  if encoding & 1:
    seg.append(((0,2*w+h), (2*h+w,2*w+2*h)))
  
  # segment B
  if encoding >> 1 & 1:
    seg.append(((w+h,w+h), (w+2*h,2*w+h)))
  
  # segment C
  if encoding >> 2 & 1:
    seg.append(((w+h,h), (w+2*h,w+h)))
  
  # segment D
  if encoding >> 3 & 1:
    seg.append(((0,0), (w+2*h,h)))
  
  # segment E
  if encoding >> 4 & 1:
    seg.append(((0,h), (h,h+w)))
  
  # segment F
  if encoding >> 5 & 1:
    seg.append(((0,h+w), (h, h+2*w)))
    
  # segment G1
  if encoding >> 6 & 1:
    seg.append(((h, h/2+w), (h+w/2, 3*h/2+w)))
  
  # segment G2
  if encoding >> 7 & 1:
    seg.append(((h+w/2, h/2+w), (h+w, 3*h/2+w)))
  
  # segment H
  if encoding >> 8 & 1:
    seg.append(((h, (2*w+h)-(h*math.sqrt(2)/2)),
                (h,2*w+h),
                (h+h*math.sqrt(2)/2,2*w+h),
                ((2*h+w)/2-h/2,(3*h/2+w)+(h*math.sqrt(2)/2)),
                ((2*h+w)/2-h/2,3*h/2+w),
                ((2*h+w)/2-h/2-(h*math.sqrt(2)/2),3*h/2+w)
                ))
  
  # segment I
  if encoding >> 9 & 1:
    seg.append((((2*h+w)/2-h/2,3*h/2+w), ((2*h+w)/2+h/2,2*w+h)))
  
  # segment J
  if encoding >> 10 & 1:
    seg.append(((w+h-h*math.sqrt(2)/2,2*w+h),
                (w+h,2*w+h),
                (w+h,2*w+h-h*math.sqrt(2)/2),
                ((2*h+w)/2+h/2+h*math.sqrt(2)/2,3*h/2+w),
                ((2*h+w)/2+h/2,3*h/2+w),
                ((2*h+w)/2+h/2,3*h/2+w+h*math.sqrt(2)/2)
                ))
  
  # segment K
  if encoding >> 11 & 1:
    seg.append(((h,h),
                (h,h+h*math.sqrt(2)/2),
                ((2*h+w)/2-h/2-h*math.sqrt(2)/2,h/2+w),
                ((2*h+w)/2-h/2,h/2+w),
                ((2*h+w)/2-h/2,h/2+w-h*math.sqrt(2)/2),
                (h+h*math.sqrt(2)/2,h)
                ))
  
  # segment L
  if encoding >> 12 & 1:
    seg.append((((2*h+w)/2-h/2,h), ((2*h+w)/2+h/2,h/2+w)))
  
  # segment M
  if encoding >> 13 & 1:
    seg.append(((w+h-h*math.sqrt(2)/2,h),
                ((2*h+w)/2+h/2,h/2+w-h*math.sqrt(2)/2),
                ((2*h+w)/2+h/2,h/2+w),
                ((2*h+w)/2+h/2+h*math.sqrt(2)/2,h/2+w),
                (w+h,h+h*math.sqrt(2)/2),
                (w+h,h)
                ))
  
  return seg

def create_text(string, loc, cell, layer, scale=1):
  """
  Function for creating text in layout based on 14-segment display
  
  Parameters
  ----------
  string: text string to place in layout
  loc: location (x,y) of string in layout (in microns)
  cell: cell in which to place text
  layer: layer in which text is written
  scale: relative scale of font (default segment size is 10 µm by 1 µm, scale of 2 will 
         increase this to 20 µm by 2 µm)
  
  Returns
  ----------
  None (draws segments on given layer)
  """
  
  string = string.upper()
  
  x = loc[0]
  y = loc[1]
  line_space = LINE_SPACE * scale
  letter_space = LETTER_SPACE * scale
  
  for s in string:
    if s == "\n":
      x = loc[0]
      y -= line_space
    else:
      if s in ENCODING.keys():
        coords = segments(ENCODING[s], scale)
        for i in coords:
          if len(i) == 2:
            cell.shapes(layer).insert(pya.Box(pya.Point(int(i[0][0]+x),int(i[0][1]+y)), 
                                      pya.Point(int(i[1][0]+x),int(i[1][1]+y))))
          else:
            cell.shapes(layer).insert(pya.Polygon([pya.Point(int(j[0]+x),int(j[1]+y)) for j in i]))
      x += letter_space
