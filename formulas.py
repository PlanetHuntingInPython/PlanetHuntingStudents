# Calculates Transit Impact Parameter, semi major axis through two methods
# and the orbital inclination of a planet using the Star Radius, Planet Radius, Orbital Period and Transit Duration

import math
# Calculates the transit impact parameter using the Star Radius, Planet Radius, Orbital Period and Transit Duration
def transitImpactParameter(stellarRadius, planetaryRadius, orbitalPeriod, transitDuration):
    return (((((stellarRadius - planetaryRadius)**2)-((semiMajorAxis2(orbitalPeriod, transitDuration)*math.sin((transitDuration * math.pi)/(orbitalPeriod)))**2))**0.5)/(stellarRadius))

# Calculates the semi major axis using the Star Mass, Orbital Period and Orbital Radius
def SemiMajorAxis1(stellarMass, orbitalPeriod, orbitalRadius):
    #returned in metres
    return round((6.67*(10**-11)*stellarMass*(orbitalPeriod**2))/((2*orbitalRadius*math.pi)**2),2)

# Calculates the semi major axis using the Orbital Period and Transit Duration
def semiMajorAxis2(orbitalPeriod, transitDuration):
    return round((2*math.pi*transitDuration)/(orbitalPeriod),2)

# Calculates the orbital inclination using the Star Radius, Planet Radius, Orbital Period and Transit Duration
def PlanetOrbitalInclination(starRadius, planetRadius, orbitalPeriod, transitDuration):
    return math.acos((transitImpactParameter(starRadius,planetRadius, orbitalPeriod, transitDuration)*starRadius)/(semiMajorAxis2(orbitalPeriod, transitDuration)))