"""Virtual pond module to generate virtual sensor reading, aka expected value for current water level"""

import math

#Values from offline example in paper
surfaceReactionFactor = 0.25
urbanCatchmentArea = 0.59 #unit: Ha

#Discharge coeficent
dischargeCoeficent = 0.6

#Pond area from offline exmple in paper
pondArea = 5572 #unit: m^2

#Minimum and maximum water level in cm
maxWaterLevel = 300
minWaterLevel = 100


def getPreviousReading():
    "Get the previous pond reading"


    #Palceholder
    waterLevel = 200 #unit: cm

    #Orifice diameter in cm
    orificeMax = 17.5 
    orificeMed = orificeMax*(4/7)
    orificeMin = orificeMax*(1/7)
   

    orifice = orificeMax

    return waterLevel,orifice


def getWeatherforcast():
    "Get weather forcast from DMI api"

    #Peters code

    #placeholder
    rainMm = 20

    return rainMm


def generateVirtualSensorReading(pondArea):
    "Genereate the virtual value of expected water level"

    #Get weather forcast from DMI API
    forcast = getWeatherforcast()

    #Get values from previous stradegy
    waterLevel, orifice = getPreviousReading()

    #Water volume in cm^3
    volumeIn = waterIn(surfaceReactionFactor,forcast,urbanCatchmentArea)
    volumeOut = waterOut(dischargeCoeficent,orifice,waterLevel)

    print("Voulme in", volumeIn)
    print("Voulme out", volumeOut)

    #Volume = Q_in - Q_out
    if volumeIn >= volumeOut:
        waterVolume = volumeIn - volumeOut
    elif volumeOut > volumeIn:
        waterVolume = 0
    
    heightCm = (waterVolume/pondArea)*100 

    return heightCm




def waterIn(k, S, A_uc):
    """Water going into the pond
    Q_in = kSA_(uc)
    k: Urban surface reaction factor, in paper 0.25 (offline example)
    S: Difference between the rain falling into the urban area and the storm water leaving it
    A_uc : Urban catchment surface area, in paper 0.59 ha (offline example)
    Returns m^3
    """

    #Convert mm to m
    S = S / 1000

    #Conver ha to m^2
    A_uc = A_uc * 10000

    Q_in = k * S * A_uc

    
    return Q_in 


def waterOut(C, d, w):
    """Water going out of the pond
    Q_out = C(Pi/4)d^2 *sqrt(2gw)
    C: Discharge coefficient
    d: Chosen diameter of the orifice in cm
    w: Water level in cm
    g: gravitational acceleration (only valid if the orifice is fully submarged ie w >= d)
    Returns m^3
    """
    
    g = 9.81
    
    # Convert from cm to m
    w = w/100
    d = d/100
    
    Q_out = C*(math.pi/4)*(math.pow(d,2)) * math.sqrt(2*g*w)

    return Q_out




def main():


    heightCm = generateVirtualSensorReading(pondArea)

    print(f"Water level: {heightCm} cm.")




   

if __name__ == "__main__":
    main()
