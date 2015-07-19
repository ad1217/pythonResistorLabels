#!/usr/bin/env python3
import math
import re

colors = {0 : "black",
          1 : "brown",
          2 : "red",
          3 : "orange",
          4 : "yellow",
          5 : "green",
          6 : "blue",
          7 : "violet",
          8 : "grey",
          9 : "white",
          -1: "gold",
          -2: "silver"}

htmlColors = {"black" : "black",
              "brown" : "brown",
              "red"   : "red",
              "orange": "orange",
              "yellow": "yellow",
              "green" : "green",
              "blue"  : "blue",
              "violet": "violet",
              "grey"  : "grey",
              "white" : "white",
              "silver": "silver",
              "gold"  : "gold"}

suffixes = {1: "K",
            2: "M",
            3: "G"}

def getName (val):
    pThousand = int(math.log(val, 1000))
    if pThousand in suffixes:
        return str(val/pow(1000, pThousand)).replace(".0", "") + suffixes[pThousand]
    else:
        return str(val).replace(".0", "")

def getColor (firstDigit, secondDigit, val):
    pTen = int(math.log10(val/(firstDigit*10+secondDigit)))
    return [colors[firstDigit], colors[secondDigit], colors[pTen]]

def parse (inp):
    value = 0
    name = ""
    color = []
    if re.match("\d\d?0*$", inp):
        value = int(inp)
        name  = getName(value)
        color = getColor(int(inp[0]), int(inp[1]) if len(inp) > 1 else 0, value)

    elif re.match("\d\.\d?0*$", inp):
        value = float(inp)
        name  = getName(value)
        color = getColor(int(inp[0]), int(inp[2]), value)

    elif re.match("\d\.?\d?0?[KMG]", inp):
        invsuffixes = dict((v, k) for k, v in suffixes.items())
        pTen  = invsuffixes[inp[-1]] * 3
        value = int(inp[:-1]) * pow(10, pTen)
        name  = getName(value)
        color = getColors(int(inp[0]), int(inp[1]), value)

    elif re.match("[a-z]+ [a-z]+ [a-z]+$", inp):
        invcolors = dict((v, k) for k, v in colors.items())
        color = inp.split(" ")
        value = int((invcolors[color[0]] * 10 + invcolors[color[1]]) * pow(10, invcolors[color[2]]))
        name  = getName(value)
    else:
        print("Invalid input: " + inp)

    return {"value": value,
            "name" : name,
            "color": color}

def svgWrite(resistors):
    width   = 5
    height  = 5
    spacing = 5

    xInitialOffset = 10
    yInitialOffset = 10

    xOffset = xInitialOffset
    yOffset = yInitialOffset

    resPerLine = math.floor((215.9 - (xInitialOffset * 2)) / (width * 3 + spacing))

    f=open("out.svg", "w")
    f.write('<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="8.5in" height="11in">\n')
    f.write('"  <rect x="0mm" y="0mm" width="8.5in" height="11in" fill="white"/>\n"')
    #f.write('<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="%imm" height="%imm">\n' %(width * 3 * len(resistors) + spacing * (len(resistors) - 1), height * 2))
    #f.write('"  <rect x="0mm" y="0mm" width="%imm" height="%imm" fill="white"/>\n"' %(width * 3 * len(resistors) + spacing * (len(resistors) - 1), height * 2))

    count = 0
    line = 0
    for res in resistors:
        blockOffset = 0
        for color in res["color"]:
            f.write('  <rect x="%imm" y="%imm" width="%imm" height="%imm" fill="%s"/>\n'
                    %(xOffset + blockOffset, yOffset, width, height, htmlColors[color]))
            blockOffset += width
        f.write('  <text x="%fmm" y="%imm" text-anchor="middle" font-size="%fmm" font-family="sans">%s</text>\n\n' %(xOffset + width * 3 / 2, yOffset + height * 2, height/1.2, "R" + res["name"]))
        xOffset += width * 3 + spacing
        count += 1
        if (count % resPerLine == 0):
            line +=1
            xOffset = xInitialOffset

        yOffset = yInitialOffset + line * (width * 2 + spacing)

    f.write("</svg>\n")

resistors = [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82]
resistors += [x / 10   for x in resistors]
resistors += [int(x * 10)   for x in resistors]
resistors += [int(round(x * 100, -1))  for x in resistors]
resistors += [int(x * 1000) for x in resistors]
svgWrite([parse(str(x)) for x in resistors])
