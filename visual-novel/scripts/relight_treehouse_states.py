#!/usr/bin/env python3
"""Explicit day/weather lighting states over fixed treehouse geometry.

The input can be an early or later furniture composition. Lighting affects the
whole room; weather remains outdoors. This is not a frozen-furniture contract.
"""
from pathlib import Path
import argparse
import json
import random

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from repair_treehouse_environments import PROJECT, SIZE, OPENINGS, EARLY_PAPERS, source_images, mask, rgba, compose


def exterior_mask(image):
    pixels = np.asarray(image, dtype=float)
    # The original hand masks define clear open air; the hue extension reaches
    # cool foliage edges beside warm posts/curtains without tinting those timbers.
    region = mask([
        [[556,232],[605,206],[672,226],[716,181],[840,164],[874,443],[682,478],[565,446]],
        [[916,221],[955,171],[1115,139],[1351,107],[1333,513],[1265,512],[930,475]],
        [[1400,213],[1454,149],[1563,83],[1671,58],[1671,565],[1420,515],[1395,499]],
    ], 1.0)
    cool = np.clip((np.minimum(pixels[:,:,1], pixels[:,:,2])-pixels[:,:,0]-3)/10,0,1)
    known = np.asarray(mask(OPENINGS, .75), dtype=float)/255
    extension = np.asarray(region, dtype=float)/255*cool
    return np.maximum(known, extension).clip(0,1)


def lighting_field():
    yy,xx = np.mgrid[:SIZE[1],:SIZE[0]]
    window = np.exp(-((xx-1170)/740)**2-((yy-495)/520)**2)
    floor = np.exp(-((xx-855)/680)**2-((yy-643)/290)**2)
    return xx,yy,window,floor


def rain_weather(base, outside, remembrance=False):
    pixels = np.asarray(base,dtype=np.float32)
    x,y,window,floor = lighting_field()
    lum = pixels@np.array([.2126,.7152,.0722])
    # Mist lifts distant air and suppresses its contrast; close branch ridges
    # retain stronger texture and carry narrow wet highlights.
    mist = (.13+.16*np.exp(-((x-1220)/500)**2-((y-240)/230)**2))*outside
    fog_color = np.array([112,133,137])
    pixels = pixels*(1-mist[:,:,None])+fog_color*mist[:,:,None]
    ridges = np.maximum(lum-cv2.GaussianBlur(lum.astype(np.float32),(0,0),2.4),0)
    pixels += np.minimum(ridges*.65,16)[:,:,None]*outside[:,:,None]*np.array([.70,.91,1.0])
    rain = Image.new('RGBA',(SIZE[0]*3,SIZE[1]*3))
    draw = ImageDraw.Draw(rain); rng = random.Random(9131 if remembrance else 8117)
    for i in range(4200):
        rx,ry=rng.uniform(530,1680),rng.uniform(40,580)
        depth=rng.random(); length=10+depth*29; drift=2+depth*5
        a=int(13+depth*42)
        draw.line((int(rx*3),int(ry*3),int((rx-drift)*3),int((ry+length)*3)),fill=(174,194,198,a),width=2 if depth<.55 else 3)
    rain=rain.resize(SIZE,Image.Resampling.LANCZOS)
    rain.putalpha(Image.fromarray((np.asarray(rain.getchannel('A'),dtype=float)*outside).astype(np.uint8)))
    return Image.alpha_composite(Image.fromarray(np.clip(pixels,0,255).astype(np.uint8)).convert('RGBA'),rain).convert('RGB')


def forest_light(image, rainy=False):
    a=np.asarray(image.convert("RGB"),dtype=float)/255
    x,y,window,floor=lighting_field()
    # Convert the deep blue shaded source to dimensional green afternoon leaves.
    # Rain has a neutral overcast canopy, not the same night-blue room with lines.
    if rainy:
        matrix=np.array([[.54,.59,.16],[.16,.83,.17],[.10,.34,.60]])
        forest=np.power(np.clip(a@matrix.T,0,1),.78)*np.array([.99,1.02,1.04])
    else:
        matrix=np.array([[.55,.91,.10],[.13,.98,.10],[.06,.36,.44]])
        forest=np.power(np.clip(a@matrix.T,0,1),.68)
        broad=np.exp(-((x-1240)/460)**2-((y-240)/310)**2)
        forest *= (1.08+.15*broad)[:,:,None]
        # Existing green leaf pigmentation, plus dark canopy masses, receives
        # restrained olive/forest chroma while lighter bark remains neutral.
        lum=a@np.array([.2126,.7152,.0722])
        leaf=np.clip((a[:,:,1]-a[:,:,2]+.045)/.10,0,1)
        dark=np.clip((.31-lum)/.23,0,1)
        leaf=np.maximum(leaf*.90,dark*.68)
        forest *= (1-leaf[:,:,None])+leaf[:,:,None]*np.array([.79,1.09,.72])
    return forest


def relight_room(image, state, protected_furniture=None):
    """Return early_day, early_rain, later_day or memory_rain state pixels."""
    image=image.convert('RGB'); assert image.size==SIZE
    outside=exterior_mask(image)
    if protected_furniture is not None:
        outside *= 1-np.asarray(protected_furniture,dtype=float)/255
    a=np.asarray(image,dtype=float)/255
    x,y,window,floor=lighting_field()
    rainy=state.endswith('rain')
    gamma=.91 if rainy else .77
    room=np.power(a,gamma)*np.array([.98,1.015,1.05])
    room *= (1+.10*window+.06*floor)[:,:,None] if not rainy else (.94+.045*window)[:,:,None]
    forest=forest_light(image,rainy)
    result=room*(1-outside[:,:,None])+forest*outside[:,:,None]
    # Rainy air cools broad interior fill while the painted local amber lamps
    # remain warm. Sunlit dry afternoons have more visible midtone wood detail.
    if rainy:
        room_cool=(.06*window*(1-outside))[:,:,None]
        result=result*(1-room_cool)+np.array([.22,.28,.30])*room_cool
    result=Image.fromarray(np.clip(result*255,0,255).astype(np.uint8))
    if rainy:
        result=rain_weather(result,outside,state=='memory_rain')
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--state',choices=['early_day','early_rain','later_day','memory_rain'])
    args=parser.parse_args()
    if args.input:
        assert args.output and args.state
        image=Image.open(args.input)
        args.output.parent.mkdir(parents=True,exist_ok=True)
        relight_room(image,args.state).save(args.output)
        return
    src=source_images()
    early=compose(src['room'],rgba(src['papers'],mask(EARLY_PAPERS,.7)))
    out=PROJECT/'build/graphics/environments/states';out.mkdir(parents=True,exist_ok=True)
    for state in ['early_day','early_rain']:
        relight_room(early,state).save(out/(state+'.png'))
    print(out)


if __name__=='__main__':main()
