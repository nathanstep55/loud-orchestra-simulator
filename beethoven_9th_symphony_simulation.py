# SPDX-License-Identifier: MIT-0

# Nathan Stephenson
# Calculate the peak decibels at a given xy point for Beethoven's 9th Symphony
# (This is just a thought experiment and isn't very accurate.)

# inspired by GMU Music Program discussion
# stemming from the meme https://twitter.com/LongmoorClaire/status/918014499071897600
# "When you keep in mind the fact that soundwaves are a form of air pressure, 
# 576,000 players can play the piece in half a second which would be loud enough
# to kill anyone in the immediate vicinity" - Rae

# apparently not, at least when everyone's outside (which is assumed in this demonstration), it's about 125dB dead in the center

# unfortunately you would need a LOT of hearing protection to not be affected by this
# 37dB is the best you can get I think, and that leaves it at 88dB, which is still above hearing loss threshold

from dataclasses import dataclass
import math

target_instrument_count = 576000  # total amount of instruments we want, at the least
instrument_spacing = 0.5  # how many meters apart per instrument? this includes the instrument/person size so make sure its large enough

@dataclass
class Instrument:
    name: str
    x: float  # in meters
    y: float  # in meters

# Note that watts to dBSPL and vice versa are dependent on the area of the sound producing object
def watts_to_dbspl(W, A):
    P0 = 20e-6  # 20 micro-pascals (minimum audible sound pressure)
    P = (W/A) ** 0.5
    return 20 * math.log10(P/P0)

def dbspl_to_watts(dB, A):
    P0 = 20e-6  # 20 micro-pascals (minimum audible sound pressure)
    return (((10.0 ** (dB / 20.0)) * P0) ** 2.0) * A

# https://www.wkcgroup.com/tools-room/inverse-square-law-sound-calculator/
def dbspl_loss(dbspl, distance):
    # assume the initial distance is about the distance of the performer's head to the body of the instrument
    # so...0.2m?
    if distance == 0.0: return dbspl
    return dbspl - max(20.0 * math.log10(distance / 0.3), 0.0)

# arrangement info taken from https://en.wikipedia.org/wiki/Symphony_No._9_(Beethoven)
# change the numbers depending on what instrument arrangement you'd like to have.
# it doesn't have to be for symphony no. 9, but if you use another instrument, make sure
# to add it to the decibel_chart dictionary
instrument_count = {
    'piccolo': 1,
    'flute': 2,
    'oboe': 2,
    'clarinet': 2,  
    'bassoon': 2,
    'horn': 4,
    'trumpet': 2,
    'trombone': 3,
    'timpani': 1,
    'bassdrum': 1,
    'triangle': 1,
    'cymbals': 1,
    'soprano': 1,
    'alto': 1,
    'tenor': 1,
    'bass': 1,
    'violin': 2,
    'viola': 1,
    'cello': 1,
    'double bass': 1
}

# watts, which are useful for determining dB given the area as well
# we only use this for the triangle, presently, since we have a watt value measured instead of dB
# sources found near decibel_chart dictionary
watts_chart = {
    'piccolo': 0.08,
    'flute': 0.06,
    'oboe': None,
    'clarinet': 0.05,  
    'bassoon': None,
    'horn': 0.15,
    'trumpet': 0.31,
    'trombone': None,
    'timpani': None,
    'bassdrum': 25.0,
    'triangle': 0.05,
    'cymbals': 9.5,
    'soprano': None,
    'alto': None,
    'tenor': None,
    'bass': 0.03,
    'violin': None,
    'viola': None,
    'cello': None,
    'double bass': 0.16
}

# area, in meters^2
# we only use this for the triangle, presently, since we have a watt value measured instead of dB
# https://www.pas.org/docs/default-source/pasic-archives/triangle
area_chart = {
    'piccolo': 0.08,
    'flute': 0.06,
    'oboe': None,
    'clarinet': 0.05,  
    'bassoon': None,
    'horn': 0.15,
    'trumpet': 0.31,
    'trombone': None,
    'timpani': None,
    'bassdrum': 25.0,
    'triangle': 0.1524 * 0.1524 / 2.0,
    'cymbals': 9.5,
    'soprano': None,
    'alto': None,
    'tenor': None,
    'bass': 0.03,
    'violin': None,
    'viola': None,
    'cello': None,
    'double bass': 0.16
}

# https://www.hearingconservation.org/assets/Decibel.pdf
# https://classicalcompass.org/woodwinds/bassoon/
# https://www.soundproofcow.com/what-are-the-loudest-musical-instruments/
# http://hyperphysics.phy-astr.gsu.edu/hbase/Music/orchins.html
# https://www.avatar.com.au/courses/PPofM/intensity/Intensity1.html
# https://acoustics.ippt.pan.pl/index.php/aa/article/viewFile/370/308
# https://www.trumpetherald.com/forum/viewtopic.php?p=1381728
decibel_chart = {
    'piccolo': 106.0,
    'flute': 103.0,
    'oboe': 112.0,
    'clarinet': 114.0,  
    'bassoon': 110.0,
    'horn': 106.0,
    'trumpet': 110.0,
    'trombone': 114.0,
    'timpani': 106.0,
    'bassdrum': 106.0,
    'triangle': watts_to_dbspl(watts_chart['triangle'], area_chart['triangle']),
    'cymbals': 119.5,
    'soprano': 90.0,
    'alto': 90.0,
    'tenor': 90.0,
    'bass': 90.0,
    'violin': 122.2,
    'viola': 119.6,
    'cello': 111.0,
    'double bass': 113.6 
}

instruments_per_symphony = sum(instrument_count[x] for x in instrument_count)

print(f"Instruments needed for one symphony: {instruments_per_symphony}")

# we are gonna copy paste all the instruments in a coordinate plane measured in meters
# each row is going to be as long as the nearest multiple of instruments_per_symphony to the square root of target_instrument_count
row_length = max(int((target_instrument_count ** 0.5 // instruments_per_symphony) * instruments_per_symphony), instruments_per_symphony)
print(f"Row length: {row_length}")
orchestra = []

# placing the instruments in rows and columns to be roughly equivalent to a square
i = 0
while i < target_instrument_count:
    for instrument in instrument_count:
        for _ in range(instrument_count[instrument]):
            row = i // row_length
            col = i % row_length
            orchestra.append(Instrument(name=instrument, x=col*instrument_spacing, y=row*instrument_spacing))
            i += 1

print(f"Total instrument count: {len(orchestra)}")

# let's say the target position is dead in the middle of the orchestra
target_pos = ((instrument_spacing*row_length) / 2, (instrument_spacing*len(orchestra)//row_length) / 2)
# target_pos = (1.0,1.0)

print(f"Target coordinates: {target_pos}")

# let's add up the power of all the instruments together
watts = 0  # watts at given point
for instrument in orchestra:
    # make sure to calculate the loss
    dbspl = dbspl_loss(decibel_chart[instrument.name], ((target_pos[0] - instrument.x)**2.0 + (target_pos[1] - instrument.y)**2.0)**0.5)
    watts += 10 ** (dbspl/10.0)

# finally, convert the watts to dB
final_decibels = 10 * math.log10(watts)

print(f"Total watts: {watts}")
print(f"Total decibels: {final_decibels}")