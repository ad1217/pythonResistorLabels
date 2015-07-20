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
              "brown" : "#862800",
              "red"   : "red",
              "orange": "orange",
              "yellow": "yellow",
              "green" : "green",
              "blue"  : "blue",
              "violet": "#8461A7",
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
    if re.match("\d\.?\d?0*$", inp):
        value = float(inp)
        name  = getName(value)
        color = getColor(int(inp[0]), 0 if len(inp) < 2 else int(inp[1]) if inp[1] != "." else int(inp[2]), value)

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
    width        = 5
    height       = 5
    spacing      = 5

    pageX        = 215.9
    pageY        = 279.4

    xMargin      = 20
    yMargin      = 0


    xOffset      = xMargin
    yOffset      = yMargin

    resPerLine   = math.floor((pageX - (xMargin * 2)) / (width * 3 + spacing))

    f=open("out.svg", "w")
    f.write('<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="%fmm" height="%fmm">\n' %(pageX, pageY))
    f.write('  <rect x="0" y="0" width="%fmm" height="%fmm" fill="white"/>\n' %(pageX, pageY))

    for ii, res in enumerate(resistors):
        xOffset = xMargin + (ii % resPerLine) * (width * 3 + spacing)
        yOffset = yMargin + math.floor(ii / resPerLine) * (width * 2 + spacing)

        blockOffset = 0
        for color in res["color"]:
            f.write('  <rect x="%imm" y="%imm" width="%imm" height="%imm" fill="%s"/>\n'
                    %(xOffset + blockOffset, yOffset, width, height, htmlColors[color]))
            blockOffset += width
        f.write('  <text x="%fmm" y="%imm" text-anchor="middle" font-size="%fmm" font-family="sans">%s</text>\n\n'
                %(xOffset + width * 3 / 2, yOffset + height * 2, height/1.2, "R" + res["name"]))

    f.write("</svg>\n")

e12 = [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82]
resistors = e12.copy()
resistors += [x / 10  for x in e12]
resistors += [int(x * 10) for x in e12]
resistors += [int(round(x * 100, -1)) for x in e12]
resistors += [int(x * 1000) for x in e12]
svgWrite([parse(str(x)) for x in resistors])
