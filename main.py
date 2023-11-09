## Create a new Arelle controller
from datetime import datetime

from arelle import XbrlConst, Cntlr, ModelXbrl
from arelle.ModelValue import qname

## Init the controller
controller = Cntlr.Cntlr()
## Set to True to work offline
controller.webCache.workOffline = True
#
## Load a taxonomy (custom or predefined) for your XBRL instance
taxonomyFile = "HelloWorld.xsd"
instance = ModelXbrl.load(controller.modelManager, taxonomyFile)

## Create instance and fill up the instance
outputFile = "ysu_xbrl_generation_test.xbrl"
instance.createInstance(outputFile)

## Create context
periodStartStr = '09/19/22 13:55:26'
periodStart = datetime.strptime(periodStartStr, '%m/%d/%y %H:%M:%S')
periodEndStr = '09/19/22 13:59:26'
periodEnd = datetime.strptime(periodEndStr, '%m/%d/%y %H:%M:%S')

# Create context
newContext = instance.createContext("http://www.xbrl.org/2003/instance", "SAMPLE",
                                    "instant", periodStart, periodEnd,
                                    None, {}, [], [], afterSibling=ModelXbrl.AUTO_LOCATE_ELEMENT)

nonNumAttr = [("contextRef", newContext.id)]

monetaryUnit = qname(XbrlConst.iso17442, "iso17442:EUR")
newUnit = instance.createUnit([monetaryUnit], [], afterSibling=ModelXbrl.AUTO_LOCATE_ELEMENT)
print(f"Show the Units :  {instance.units}")

# Create fact
elements = [
    "Land",
    "BuildingsNet",
    "FurnitureAndFixturesNet",
    "ComputerEquipmentNet",
    "OtherPropertyPlantAndEquipmentNet",
    "PropertyPlantAndEquipmentNet",
]

for element_name in elements:
    monetaryAttr = [("contextRef", "I-2007"), ("unitRef", "U-Monetary"), ("decimals", "-3")]
    element_qname = qname("{http://xbrl.squarespace.com/HelloWorld}HelloWorld:"+element_name)
    instance.createFact(element_qname, attributes=monetaryAttr, text="9999")
print(f"Save instance to {instance.facts}")

# Create a new XBRL instance
instance.saveInstance()
print(f"Save instance to {outputFile}")
## Close the Arelle controller
controller.close()
print(f"XBRL instance saved to {outputFile}")
