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
          -1: "silver",
          -2: "gold"}

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
        return str(int(val/pow(1000, pThousand))) + suffixes[pThousand]
    else:
        return str(val)

def parse (inp):
    value = 0
    name = ""
    color = []
    if re.match("\d\d?0*$", inp):
        value = int(inp)
        name  = getName(value)
        color = [colors[int(inp[0])], colors[int(inp[1])], colors[int(math.log(value, 10))-1]]
    elif re.match("\d\.?\d?0?[KMG]", inp):
        invsuffixes = dict((v, k) for k, v in suffixes.items())
        pTen  = invsuffixes[inp[-1]] * 3
        value = int(inp[:-1]) * pow(10, pTen)
        name  = getName(value)
        color = [colors[int(inp[0])], colors[int(inp[1])], colors[int(math.log(value, 10))-1]]
    elif re.match("[a-z]+ [a-z]+ [a-z]+$", inp):
        invcolors = dict((v, k) for k, v in colors.items())
        color = inp.split(" ")
        value = int((invcolors[color[0]] * 10 + invcolors[color[1]]) * pow(10, invcolors[color[2]]))
        name  = getName(value)
    else:
        print("Invalid input")

    return {"value": value,
            "name" : name,
            "color": color}

def svgWrite(resistors):
    width   = 5
    height  = 5
    spacing = 1
    f=open("out.svg", "w")
    f.write('<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="%imm" height="%imm">\n' %(width * 3 * len(resistors) + spacing * (len(resistors) - 1), height * 2))
    f.write('"  <rect x="0mm" y="0mm" width="%imm" height="%imm" fill="white"/>\n"' %(width * 3 * len(resistors) + spacing * (len(resistors) - 1), height * 2))

    xOffset = 0
    yOffset = 0
    for res in resistors:
        blockOffset = 0
        for color in res["color"]:
            f.write('  <rect x="%imm" y="%imm" width="%imm" height="%imm" fill="%s"/>\n'
                    %(xOffset + blockOffset, yOffset, width, height, htmlColors[color]))
            blockOffset += width
        f.write('  <text x="%fmm" y="%imm" text-anchor="middle" font-size="%fmm" font-family="sans">%s</text>\n\n' %(xOffset + width * 3 / 2, yOffset + height * 2, height/1.2, "R" + res["name"]))
        xOffset = width * 3 + spacing

    f.write("</svg>\n")

test = "10K" #input("input :")
resistor = parse(test)
print(resistor)
resistors = ["10K", "100K"]
svgWrite([parse(x) for x in resistors])
