import json, base64, requests
from io import BytesIO
from PIL import Image, ImageDraw

skin = input("Enter Username:")
img = Image.open(BytesIO(requests.get(json.loads(base64.b64decode(requests.get("https://sessionserver.mojang.com/session/minecraft/profile/"+requests.get("https://api.mojang.com/users/profiles/minecraft/"+skin).json()["id"]).json()["properties"][0]["value"]))["textures"]["SKIN"]["url"]).content)).convert("RGBA")
layer = input("\nIs this skin Single-Layer or Multi-Layer? [y/n]")
if layer == str("y") or layer == str("Y"):
    print("Converting...")
    LowL = img.crop((0, 48, 16, 64))
    LowR = img.crop((48, 48, 64, 64))
    CenterR = img.crop((0, 32, 64, 48))
    HeadPat = img.crop((32, 0, 64, 16))
    export = Image.new("RGBA", (64, 64), color=0)
    export.paste(img, (0,0), img)
    export.paste(LowL, (16,48), LowL)
    export.paste(LowR, (32,48), LowR)
    export.paste(CenterR, (0,16), CenterR)
    export.paste(HeadPat, (0,0), HeadPat)
    for x in range(64):
        for y in range(64):
            R = pow(export.getpixel((x,y))[0]/255,(0.83))*191
            G = pow(export.getpixel((x,y))[1]/255,(0.83))*191
            B = pow(export.getpixel((x,y))[2]/255,(0.83))*191
            A = export.getpixel((x,y))[3]
            if R >= 191 :
                R = 191
            if G >= 191 :
                G = 191
            if B >= 191 :
                B = 191
            export.putpixel((x,y), (int(R), int(G), int(B), int(A)))
    print("Removing Transparency...")
    background = Image.new('RGBA', (64, 64), (106,106,106,255))
    export = Image.alpha_composite(background, export)
    print("Transparency Removed!")
    print("Cleaning up Images...")
    gray = ImageDraw.Draw(export)
    gray.rectangle([(0, 48), (15, 64)], fill=(106,106,106), outline=None, width=0)
    gray.rectangle([(48, 48), (63, 64)], fill=(106,106,106), outline=None, width=0)
    gray.rectangle([(0, 32), (64, 47)], fill=(106,106,106), outline=None, width=0)
    gray.rectangle([(32, 0), (64, 15)], fill=(106,106,106), outline=None, width=0)
    export = export.convert("RGB")
    export.save('out.png')
else:
    print("Removing Transparency...")
    for x in range(64):
        for y in range(64):
            R = pow(img.getpixel((x,y))[0]/255,(0.83))*191
            G = pow(img.getpixel((x,y))[1]/255,(0.83))*191
            B = pow(img.getpixel((x,y))[2]/255,(0.83))*191
            A = img.getpixel((x,y))[3]
            if R >= 191 :
                R = 191
            if G >= 191 :
                G = 191
            if B >= 191 :
                B = 191
            img.putpixel((x,y), (int(R), int(G), int(B), int(A)))
    background = Image.new('RGBA', img.size, (106,106,106))
    img = Image.alpha_composite(background, img)
    img = img.convert("RGB")
    img.save('out.png')
    print("Transparency Removed!")
