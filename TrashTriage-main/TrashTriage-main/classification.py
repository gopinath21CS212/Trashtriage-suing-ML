import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import logging
logging.getLogger('tensorflow').setLevel(logging.FATAL)
import cv2 as cv
from cvzone.ClassificationModule import Classifier
import time

class classification:

    def __init__(self, model_path, labels_path):
        self.model_path = model_path
        self.labels_path = labels_path
        self.mydata = Classifier(self.model_path, self.labels_path)

    def classify_image(self, img_data):

        if img_data is None:
            return("Error: Unable to read the image.")

        predict, index = self.mydata.getPrediction(img_data, color=(0, 0, 255))

        if index == 0:
            msg = """1) Recycling: This recycling process involves breaking down the paper fibers and removing
any contaminants before manufacturing new paper items.
2) Composting: In this process, paper breaks down into organic matter that enriches soil
and supports plant growth.
3) Incineration: Controlled incineration of paper waste in waste-to-energy facilities can
generate heat and electricity.
4) Pulping for Energy: Paper waste can be turned into pulp and used as a biomass source
for energy production, including generating heat or electricity.
5) Source Reduction: This approach focuses on reducing paper waste generation. Practices
include using digital documents, printing double-sided, and minimizing unnecessary
printing.
6) Upcycling: Innovative initiatives involve transforming paper waste into higher-value
products, such as paper art, crafts, or functional items.
7) Papercrete: Paper waste can be mixed with cement to create a lightweight construction
material known as papercrete.
8) Anaerobic Digestion: In specific settings, paper waste can be subjected to anaerobic
digestion, which produces biogas and nutrient-rich digestate."""
            return("Material# Paper$Type# Biodegradable$Recyclable# Yes$Treatment methods#"+msg)
        elif index == 1:
            msg = """1) Recycling: Plastics can be sorted, cleaned, and processed into new products.It mainly
comprises of chemical recycling and mechanical recycling.
2) Incineration: Controlled incineration of plastic waste at high temperatures can help
convert it into energy. Modern incineration facilities are equipped with pollution control
technologies to minimize harmful emissions.
3) Pyrolysis: This is a type of chemical recycling where plastic waste is heated in the
absence of oxygen to break it down into its constituent components, such as oil, gas, and
char. These components can be used as fuel or raw materials.
4) Biodegradation: Research is ongoing to develop plastics that are more easily
biodegradable, breaking down into harmless components over time. However, proper
conditions are often needed for effective biodegradation.
5) Mechanical Treatment: Mechanical treatment involves sorting, shredding, and
granulating plastic waste for various uses, including making plastic lumber, textiles, and
more.
6) Waste-to-Energy Plants: These facilities use non-recyclable plastics as fuel to generate
electricity or heat. They can contribute to reducing the reliance on fossil fuels.
7) Upcycling: Some creative initiatives involve upcycling, where plastic waste is
transformed into higher-value products through artistic or innovative processes."""
            return("Material# Plastics$Type# Non-biodegradable$Recyclable# Yes$Treatment methods#"
                  +msg)
        elif index == 2:
            msg = """1) Recycling: Recycling metals conserves resources, reduces energy consumption, and
lowers greenhouse gas emissions compared to producing metals from raw materials.
2) Scrap Yards: Scrap yards and recycling centers play a crucial role in collecting, sorting,
and processing various types of metal waste for recycling.
3) Precious Metal Recovery: Precious metals like gold, silver, and platinum can be
recovered from electronic waste, jewelry, and industrial waste through specialized
processes.
4) Smelting: Metal smelting involves melting metals to separate them from impurities and
create new alloys or metal products.
5) Electroplating: In some cases, metals can be recovered from solutions used in
electroplating processes."""
            return("Material# Metal$Type# Non-biodegradable$Recyclable# Yes$Treatment methods#"
                  +msg)
        elif index == 3:
            msg="""1) Recycling: Collected glass containers and products are cleaned, sorted by color, crushed
into cullet (small glass fragments), and then melted to produce new glass items.
2) Reusing: Glass containers, such as bottles and jars, can be sanitized and reused for their
original purpose or repurposed for other uses.
3) Glassphalt: Crushed glass, or glass cullet, can be used as an aggregate in asphalt
mixtures, which is known as "glassphalt." This application can reduce the demand for
virgin aggregate and extend the life of road surfaces.
4) Landscaping and Construction: Crushed glass can be used in landscaping projects,
such as in decorative pathways, as well as in construction for various purposes.
5) Glass-to-Glass Recycling: Glass can be recycled into new glass containers (closed-loop
recycling) or into other glass products (open-loop recycling), depending on the quality
and color of the glass."""
            return("Material# Glass$Type# Non-biodegradable$Recyclable# Yes$Treatment methods#"
                  +msg)
        elif index == 4:
            msg="""1) E-Waste Recycling: E-waste recycling involves dismantling gadgets to recover valuable
materials such as metals (gold, silver, copper), plastics, glass, and circuit boards. These
materials can then be processed and reused in the production of new electronic devices
and other products.
2) Dismantling and Sorting: Gadgets are disassembled to separate different components
and materials.
3) Material Recovery: Components like circuit boards are processed to extract valuable
metals using methods such as shredding, mechanical separation, and chemical processes.
4) Secure Data Destruction: Before recycling, gadgets need to undergo secure data
destruction to ensure that any personal or sensitive information is properly erased.
5) Refurbishment and Reuse: Functional gadgets that are no longer needed can be
refurbished and sold as second-hand devices. This helps extend the life of the product and
reduces the demand for new manufacturing.
6) Extended Producer Responsibility (EPR): Many regions have EPR programs that
require manufacturers to take responsibility for the end-of-life management of their
products, including proper disposal and recycling.
7) Collection and Drop-off Centers: E-waste collection centers and drop-off points
facilitate the proper collection of gadgets for recycling and safe disposal"""
            return("Material# Gadget$Type# Non-biodegradable$Recyclable# Yes$Treatment methods#"
                  +msg)