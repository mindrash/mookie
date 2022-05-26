#!/usr/bin/env python3

import random
from random import randrange
import pyfiglet
import logging
import datetime
import PIL
from PIL import Image, ImageDraw, ImageColor, ImageChops, ImageFont
import torchvision.transforms.functional as F
import random
import json
from colorthief import ColorThief

def main():
    print(pyfiglet.figlet_format("metadevil"))
    print("Starting: " + str(datetime.datetime.now()))
    logging.basicConfig(level=logging.INFO, filename='logs/app-ipfs-pin.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    logging.info(pyfiglet.figlet_format("metadevil"))
    console_line = "*" * 80
    print(console_line)
    logging.info(console_line)
    logging.info("Starting: " + str(datetime.datetime.now()))

    mookie()

    logging.info(console_line)
    logging.info("Finished: " + str(datetime.datetime.now()))

def mookie():
    total_supply = 10
    mookie_count = 1
    width = 1024
    height = 1024
    description = "It's Mookie. Mookie isn't pretty. It's Mookie baby. Now go."
    background_layovers = [Image.open('pieces/bg_layover-1.png'), Image.open('pieces/bg_layover-2.png'),Image.open('pieces/bg_layover-3.png'),Image.open('pieces/bg_layover-4.png'),Image.open('pieces/bg_layover-5.png'),Image.open('pieces/bg_layover-6.png'),Image.open('pieces/bg_layover-7.png'),Image.open('pieces/bg_layover-8.png'),Image.open('pieces/bg_layover-9.png'),]
    bodies = [Image.open('pieces/body-1.png'), Image.open('pieces/body-2.png')]
    body_type = ""
    antennas = [Image.open('pieces/antenna-1.png'), Image.open('pieces/antenna-2.png'), Image.open('pieces/antenna-3.png')] 
    antenna_type = ""
    eye = Image.open('pieces/eye-1.png')
    neck = Image.open('pieces/neck-1.png')
    heads = [Image.open('pieces/head-1.png'), Image.open('pieces/head-2.png'), Image.open('pieces/head-3.png')] 
    head_type = ""
    mouths = [Image.open('pieces/mouth-1.png'), Image.open('pieces/mouth-2.png'), Image.open('pieces/mouth-3.png'), Image.open('pieces/mouth-4.png')] 
    mouth_type = ""
    shoe = Image.open('pieces/shoe-1.png')
    has_shoes = False
    skateboard = Image.open('pieces/skateboard-1.png')
    has_skateboard = False
    skateboard_wheel = Image.open('pieces/skateboard-wheel-1.png')
    coffee = Image.open('pieces/coffee-1.png')
    has_coffee = False
    has_freak_ellipse = False

    while mookie_count <= total_supply:
        print("Processing: " + str(mookie_count))
        logging.info("Processing: " + str(mookie_count))
        background_color = tuple(random.choices(range(200, 256), k=3))
        background_layover = background_layovers[randrange(0, len(background_layovers))]
        
        im = Image.new('RGBA', (width, height), background_color)
        im = ImageChops.blend(background_layover, im, .8)

        if (mookie_count > 1 and 1 == randrange(0, 20)):
            colors = ColorThief("out_png/1.png")
            palette = colors.get_palette(color_count=10)
            freak_ellipse(im, palette)
            has_freak_ellipse = True

        mookie = Image.new('RGBA', (width, height), (255, 0, 0, 0))
        head_type = randrange(0, len(heads))
        head = heads[head_type]
        mookie.paste(head, (352, 96), head)

        mookie.paste(neck, (32, 416), neck)

        body_type = randrange(0, len(bodies))
        body = bodies[body_type]
        mookie.paste(body, (32, 512), body)

        mouth_type = randrange(0, len(mouths))
        mouth = mouths[mouth_type]
        mookie.paste(mouth, (384, 416), mouth)

        ant_rand1 = randrange(0, len(antennas))
        antenna1 = antennas[ant_rand1]
        mookie.paste(antenna1, (128, 32), antenna1)
        ant_rand2 = randrange(0, len(antennas))
        while ant_rand1 == ant_rand2:
            ant_rand2 = randrange(0, len(antennas))
        antenna2 = antennas[ant_rand2].transpose(PIL.Image.FLIP_LEFT_RIGHT)
        mookie.paste(antenna2, (350, 32), antenna2)
        antenna_type = str({ant_rand1, ant_rand2})

        mookie_hue = F.adjust_hue(mookie, random.uniform(-.5, .5))
        im.paste(mookie_hue, (0, 0), mookie)

        eye1 = eye.rotate(90 * randrange(1, 5))
        eye2 = eye.rotate(90 * randrange(1, 5))
        im.paste(eye1, (384, 288), eye1)
        im.paste(eye2, (512, 288), eye2)

        if (1 == randrange(0, 5)):
            shoe2 = shoe.transpose(PIL.Image.FLIP_LEFT_RIGHT)
            shoe_hue = F.adjust_hue(shoe, random.uniform(-.5, .5))
            shoe_hue2 = shoe_hue.transpose(PIL.Image.FLIP_LEFT_RIGHT)
            im.paste(shoe_hue, (32, 832), shoe)
            im.paste(shoe_hue2, (832, 832), shoe2)
            has_shoes = True

        if (1 == randrange(0, 10)):
            im.paste(skateboard, (64, 832), skateboard)
            skateboard_wheel1 = skateboard_wheel.rotate(90 * randrange(1, 5))
            skateboard_wheel2 = skateboard_wheel.rotate(90 * randrange(1, 5))
            im.paste(skateboard_wheel1, (224, 928), skateboard_wheel)
            im.paste(skateboard_wheel2, (736, 928), skateboard_wheel)
            has_skateboard = True

        if (1 == randrange(0, 10)):
            im.paste(coffee, (96, 640), coffee)
            has_coffee = True

        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype("Paskowy.ttf", 70)
        label = str(bin(mookie_count))
        w, h = draw.textsize(label, font=font)
        draw.text(((width - w)/2, 930),label,(100,100,100),font=font)

        im.save("out_png/" + str(mookie_count) + ".png")

        data_name = str(mookie_count) + ".json"
        ipfs_url = "ipfs://[[IPFS_URL]]"
        nft_json = {
            "description" : description,
            "external_url" : "https://itsmookie.com",
            "image" : ipfs_url,
            "name" : "Mookie: " + label,
            "attributes" : [
                {
                    "trait_type" : "antenna_type",
                    "value" : antenna_type
                },
                {
                    "trait_type" : "head_type",
                    "value" : str(head_type)
                },
                {
                    "trait_type" : "mouth_type",
                    "value" : str(mouth_type)
                },
                {
                    "trait_type" : "body_type",
                    "value" : str(body_type)
                },
                {
                    "trait_type" : "has_shoes",
                    "value" : str(has_shoes)
                },
                {
                    "trait_type" : "has_coffee",
                    "value" : str(has_coffee)
                },
                {
                    "trait_type" : "has_skateboard",
                    "value" : str(has_skateboard)
                },
                {
                    "trait_type" : "has_freak_ellipse",
                    "value" : str(has_freak_ellipse)
                },
            ],
        }

        with open("out_meta/" + data_name, "w") as data_file:
            json.dump(nft_json, data_file)

        mookie_count += 1

def freak_ellipse(img, palette):
    dctx = ImageDraw.Draw(img)
    bmsz = (img.width // 16 - 10, img.height // 16 - 10)

    if randrange(0, 5) == 1:
        colors = palette
    else:
        colors = list(ImageColor.colormap.keys())

    if randrange(1, 3) % 2 == 0:
        colors.sort()

    if 1 == randrange(1, 10):
        colors.sort(reverse=True)

    for y in range(16):
        for x in range(16):
            bm = Image.new("L", bmsz)
            dctx_inner = ImageDraw.Draw(bm)
            dctx_inner.ellipse(
                [(0, 0), bm.size],
                fill=y * 16 + x
                )
            del dctx_inner

            pos = [
                ((bmsz[0] + 10) * x + 10,
                (bmsz[1] + 10) * y + 10)]
            dctx.bitmap(
                pos,
                bm,
                fill=colors[(y * 16 + x) % len(colors)])
    del dctx


if __name__ == "__main__":
    main()