#
# Created by Andreas Ryde 22.11.2017
#

from PIL import Image
from PIL import ImageDraw
import random
import math
import sys

# Generation parameters:

# raw_input the user's desired values
# Background color of the created PNG
PNGBGCOLOR = (0, 0, 0)

# Quick Filename
RAND = random.randrange(0, 240000000000)

# ---------------------------------------------------------------------------
NAME = input('Galaxy Name:')

NUMC = int(input('Number of Extra Globular Clusters <Default:1>:') or "1")

NUMHUB = int(input('Number of Core Stars <Default:2000>:') or "2000")

NUMDISK = int(input('Number of Disk Stars <Default:4000>:') or "4000")

NUMCLUSA = NUMHUB / 70

NUMCLUS = int(input('Number of Stars in each Cluster <Default:Hub / 70>:') or str(NUMCLUSA))

DISCLUSA = NUMCLUS / 4

DISCLUS = int(input('Distribution of Star Number in each Cluster <Default: Avg/ 4>:') or str(DISCLUSA))

HUBRAD = float(input('Radius of Core <Default:90.0>:') or "90.0")

DISKRAD = float(input('Radius of Disk <Default:45.0>:') or "45.0")

CLUSRADA = NUMCLUS / 5

CLUSRAD = float(input('Radius of each cluster <Default:Star Number / 2>:') or str(CLUSRADA))

DISCLRADA = CLUSRAD / 5

DISCLRAD = float(input('Distribution of Cluster Radius <Default:Avg / 5>:') or str(DISCLRADA))

NUMARMS = int(input('Number of Galactic Arms <Default:3>:') or "3")

ARMROTS = float(input('Tightness of Arm Winding <Default:0.5>:') or "0.5")

ARMWIDTH = float(input('Arm Width in Degrees <Default:65>:') or "65")

MAXHUBZ = float(input('Maximum Depth of Core <Default:16.0>:') or "16.0")

MAXDISKZ = float(input('Maximum Depth of Arms <Default:2.0>:') or "2.0")

FUZZ = float(input('Maximum Outlier Distance from Arms <Default:25.0>:') or "25.0")

PNGSIZE = float(input('X and Y Size of PNG <Default:1200>:') or "1200")

PNGFRAME = float(input('PNG Frame Size <Default:50>:') or "50")

stars = []
clusters = []

disstar_color_dict = {
    0: (229, 30, 30),
    1: (203, 30, 26),
    2: (181, 18, 6),
    3: (200, 39, 13),
    4: (200, 63, 21),
    5: (222, 137, 10),
    6: (212, 178, 42),
    7: (210, 188, 38),
    8: (217, 207, 66),
    9: (222, 226, 125),
    10: (222, 226, 160),
    11: (255, 255, 253),
    12: (255, 255, 255),
    13: (253, 255, 255),
    14: (250, 255, 255),
    15: (222, 243, 255),
    16: (222, 243, 255),
    17: (230, 243, 255),
    18: (140, 176, 255),
    19: (140, 176, 225)
}

censtar_color_dict = {
    0: (229, 30, 30),
    1: (203, 30, 26),
    2: (181, 18, 6),
    3: (200, 39, 13),
    4: (200, 63, 21),
    5: (222, 75, 10),
    6: (222, 102, 10),
    7: (222, 137, 10),
    8: (212, 178, 42),
    9: (210, 188, 38),
    10: (217, 207, 66),
    11: (217, 207, 66),
    12: (222, 226, 125),
    13: (222, 226, 125),
    14: (255, 255, 253),
    15: (255, 255, 255),
    16: (253, 255, 255),
    17: (222, 243, 255),
    18: (222, 243, 255),
    19: (140, 176, 225)
}

SHRAD = HUBRAD * 0.1
SCRAD = CLUSRAD * 0.06
SDRAD = DISKRAD * 0.1
NUMCLUSA = NUMCLUS - DISCLUS
NUMCLUSB = NUMCLUS + DISCLUS
CLUSRADA = CLUSRAD - DISCLRAD
CLUSRADB = CLUSRAD + DISCLRAD
NUMCB = NUMC + 1

def generateClusters():
    c = 0
    cx = 0
    cy = 0
    cz = 0
    rad = random.uniform(CLUSRADA, CLUSRADB)
    num = random.uniform(NUMCLUSA, NUMCLUSB)
    clusters.append((cx, cy, cz, rad, num))
    c = 1
    while c < NUMCB:
        # random distance from centre
        dist = random.uniform(CLUSRAD, (HUBRAD+DISKRAD))
        # any rotation- clusters can be anywhere
        theta = random.random() * 360
        cx = math.cos(theta * math.pi / 180.0) * dist
        cy = math.sin(theta * math.pi / 180.0) * dist
        cz = random.random() * MAXHUBZ * 2.0 - MAXHUBZ
        rad = random.uniform(CLUSRADA, CLUSRADB)
        num = random.uniform(NUMCLUSA, NUMCLUSB)
        # add cluster to clusters array
        clusters.append((cx, cy, cz, rad, num))
        # process next
        c = c+1
        sran = 0
        cran = 0

def generateStars():
    # omega is the separation (in degrees) between each arm
    # Prevent div by zero error:
    if NUMARMS:
        omega = 360.0 / NUMARMS
    else:
        omega = 0.0
    i = 0
    while i < NUMDISK:

        # Choose a random distance from center
        dist = HUBRAD + random.random() * DISKRAD
        distb = dist + random.uniform(0,SDRAD)

        # This is the 'clever' bit, that puts a star at a given distance
        # into an arm: First, it wraps the star round by the number of
        # rotations specified.  By multiplying the distance by the number of
        # rotations the rotation is proportional to the distance from the
        # center, to give curvature
        theta = ((360.0 * ARMROTS * (distb / DISKRAD))

                 # Then move the point further around by a random factor up to
                 # ARMWIDTH
                 + random.random() * ARMWIDTH

                 # Then multiply the angle by a factor of omega, putting the
                 # point into one of the arms
                 # + (omega * random.random() * NUMARMS )
                 + omega * random.randrange(0, NUMARMS)

                 # Then add a further random factor, 'fuzzin' the edge of the arms
                 + random.random() * FUZZ * 2.0 - FUZZ
                 # + random.randrange( -FUZZ, FUZZ )
                 )

        # Convert to cartesian
        #def cartesian_convert
        x = math.cos(theta * math.pi / 180.0) * distb
        y = math.sin(theta * math.pi / 180.0) * distb
        z = random.random() * MAXDISKZ * 2.0 - MAXDISKZ
        
        # Replaces the if/elif logic with a simple lookup. Faster and
        # and easier to read.
        scol = disstar_color_dict[random.randrange(0,19)]

        # Add star to the stars array
        stars.append((x, y, z, scol))

        # Process next star
        i = i + 1
        sran = 0

    # Now generate the Hub. This places a point on or under the curve
    # maxHubZ - s d^2 where s is a scale factor calculated so that z = 0 is
    # at maxHubR (s = maxHubZ / maxHubR^2) AND so that minimum hub Z is at
    # maximum disk Z. (Avoids edge of hub being below edge of disk)

    scale = MAXHUBZ / (HUBRAD * HUBRAD)
    i = 0
    while i < NUMHUB:
        
        # Choose a random distance from center
        dist = random.random() * HUBRAD
        distb = dist + random.uniform(0,SHRAD)
        
        # Any rotation (points are not on arms)
        theta = random.random() * 360

        # Convert to cartesian
        x = math.cos(theta * math.pi / 180.0) * distb
        y = math.sin(theta * math.pi / 180.0) * distb
        z = (random.random() * 2 - 1) * (MAXHUBZ - scale * distb * distb)
        
        # Replaces the if/elif logic with a simple lookup. Faster and
        # and easier to read.
        scol = censtar_color_dict[random.randrange(0,19)]

        # Add star to the stars array
        stars.append((x, y, z, scol))

        # Process next star
        i = i + 1
        sran = 0
        
    # Generate clusters and their stars.
    
    c = 0
    while c < NUMCB:
        for (cx, cy, cz, rad, num) in clusters:    
            scale = rad / (rad * rad)
            i = 0
            while i < num:
                dist = random.uniform(-rad,rad)
                distb = dist + random.uniform(0,SCRAD)
                theta = random.random() * 360
                # Cartesian!
                x = cx + (math.cos(theta * math.pi / 180) * distb)
                y = cy + (math.sin(theta * math.pi / 180) * distb)
                z = (random.random() * 2 - 1) * ((cz + rad) - scale * distb * distb)
                scol = censtar_color_dict[random.randrange(0,19)]
                stars.append((x, y, z, scol))
                i = i + 1
                sran = 0
        c = c+1

    


def drawToPNG(filename):
    image = Image.new("RGB", (int(PNGSIZE), int(PNGSIZE)), PNGBGCOLOR)
    draw = ImageDraw.Draw(image)

    # Find maximal star distance
    max = 0
    for (x, y, z, scol) in stars:
        if abs(x) > max: max = x
        if abs(y) > max: max = y
        if abs(z) > max: max = z
        
    # Calculate zoom factor to fit the galaxy to the PNG size
    factor = float(PNGSIZE - PNGFRAME * 2) / (max * 2)
    for (x, y, z, scol) in stars:
        sx = factor * x + PNGSIZE / 2
        sy = factor * y + PNGSIZE / 2
        draw.point((sx, sy), fill=scol)

    # Save the PNG
    image.save(filename)
    print(filename)


# Generate the galaxy
generateClusters()
generateStars()

# Save the galaxy as PNG to galaxy.png
drawToPNG("spiralgalaxy" + str(RAND) + "-" + str(NAME) + ".png")

# Create the galaxy's data galaxy.txt
with open("spiralgalaxy" + str(RAND) + "-" + str(NAME) + ".txt", "w") as text_file:
    text_file.write("Galaxy Number: {}".format(RAND)
                   )
    text_file.write("Galaxy Name: {}".format(NAME)
                   )
    text_file.write("Number of Clusters: {}".format(NUMC)
                   )
    text_file.write("Hub Stars: {}".format(NUMHUB)
                   )
    text_file.write("Number of Stars per Cluster: {}".format(NUMCLUS)
                   )
    text_file.write("Star Number Distribution per Cluster: {}".format(DISCLUS)
                   )
    text_file.write("Disk Stars: {}".format(NUMDISK)
                   )
    text_file.write("Hub Radius: {}".format(HUBRAD)
                   )
    text_file.write("Cluster Radius: {}".format(CLUSRAD)
                   )
    text_file.write("Cluster Radius Distribution: {}".format(DISCLRAD)
                   )
    text_file.write("Disk Radius: {}".format(DISKRAD)
                   )
    text_file.write("Arm Number: {}".format(NUMARMS)
                   )
    text_file.write("Arm Rotation: {}".format(ARMROTS)
                   )
    text_file.write("Arm Width: {}".format(ARMWIDTH)
                   )
    text_file.write("Hub Maximum Depth: {}".format(MAXHUBZ))
    
    text_file.write("Disk Maximum Depth: {}".format(MAXDISKZ)
                   )
    text_file.write("Maximum Outlier Distance: {}".format(FUZZ)
                   )
    text_file.write("Image Size: {}".format(PNGSIZE)
                   )
    text_file.write("Frame Size: {}".format(PNGFRAME)
                   )