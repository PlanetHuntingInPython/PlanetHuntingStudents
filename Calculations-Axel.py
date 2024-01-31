# Calculates Transit Impact Parameter, semi major axis through two methods
# and the orbital inclination of a planet using the Star Radius, Planet Radius, Orbital Period and Transit Duration

import math

# Calculates the transit impact parameter using the Star Radius, Planet Radius, Orbital Period and Transit Duration
def TransitImpactParameter(StarRadius,PlanetRadius, OrbitalPeriod, TransitDuration):
    return (((((StarRadius-PlanetRadius)**2)-((SemiMajorAxis2(OrbitalPeriod, TransitDuration)*math.sin((TransitDuration * math.pi)/(OrbitalPeriod)))**2))**0.5)/(StarRadius))

# Calculates the semi major axis using the Star Mass, Orbital Period and Orbital Radius
def SemiMajorAxis1(StarMass, OrbitalPeriod, OrbitalRadius):
    #returned in metres
    return round((6.67*(10**-11)*StarMass*(OrbitalPeriod**2))/((2*OrbitalRadius*math.pi)**2),2)

# Calculates the semi major axis using the Orbital Period and Transit Duration
def SemiMajorAxis2(OrbitalPeriod, TransitDuration):
    return round((2*math.pi*TransitDuration)/(OrbitalPeriod),2)

# Calculates the orbital inclination using the Star Radius, Planet Radius, Orbital Period and Transit Duration
def PlanetOrbitalInclination(StarRadius,PlanetRadius, OrbitalPeriod, TransitDuration):
    return math.acos((TransitImpactParameter(StarRadius,PlanetRadius, OrbitalPeriod, TransitDuration)*StarRadius)/(SemiMajorAxis2(OrbitalPeriod, TransitDuration)))