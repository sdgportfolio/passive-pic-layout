"""
SRR-Flake: Split-Ring Resonator with Dielectric Flake Layout Generator
========================================================================
Parametric GDSFactory layout of a square split-ring resonator (SRR) with
a dielectric flake (e.g. NbOI2) bridging the gap.
The ring is built as a boolean subtraction of two concentric squares with
a parametric gap cut through the top wall; 
the flake sits on a separate material layer directly over the gap, 
allowing gap capacitance to be tuned independently of the ring.
This code supplements a COMSOL simulation of gold SRR + NbOI2 flake.

Author: Shroyon Dasgupta
GitHub: github.com/sdgportfolio/passive-pic-layout
"""


#Importing libraries
import gdsfactory as gf
import matplotlib.pyplot as plt
gf.gpdk.PDK.activate()


#--- FUNCTIONS ---
#GDSFactory function to create a split ring resonator with a flake
@gf.cell
def srr_with_flake(
    srr_length: float = 7.0,
    srr_arm_width: float = 1.0,
    srr_gap: float = 1.0,
    flake_size: float = 2.0,
    srr_layer: tuple = (1,0),
    flake_layer: tuple = (2,0),
) -> gf.Component:
    
    """
    Args:
        srr_length: side length of the square split ring resonator.
        srr_arm_width: arm width of the split ring resonator.
        srr_gap: air gap in the split ring resonator.
        flake_size: side length of the square flake.
        srr_layer: layer for the split ring resonator.
        flake_layer: layer for the flake.

    Returns:
        Component with a split ring resonator and a flake.
    """

    violations = srr_drc(srr_length, srr_arm_width, srr_gap, flake_size, srr_layer, flake_layer) #Calling the design rule check function to check for violations
    if violations:
        message = "DRC violation(s) found:\n" #Creating a message string to display the violations
        for v in violations:
            message += f"  - {v}\n" #Adding each violation to the message string
        raise ValueError(message) #Raising a ValueError with the message string if any violations are found
    else:
        print("No DRC violations found.") #Printing a message if no violations are found

    c = gf.Component() #Creating a new GDSFactory component to hold the split ring resonator and flake

    # Create split ring resonator
    outer_square = gf.components.rectangle(size = (srr_length, srr_length), layer = srr_layer, centered = True) #Creating the outer square of the SRR
    inner_square = gf.components.rectangle(size = (srr_length - 2 * srr_arm_width, srr_length - 2 * srr_arm_width), layer = srr_layer, centered = True) #Creating the inner square of the SRR
    srr_wo_gap = gf.boolean(outer_square, inner_square, operation = "A-B", layer = srr_layer) #Creating the SRR without the air gap using boolean subtraction operation
    air_gap = gf.components.rectangle(size = (srr_gap, srr_arm_width*1.2), layer = srr_layer, centered = True).copy().move((0, (srr_length/2 - srr_arm_width/2))) #Creating the air gap and moving it to the top of the SRR
    srr = gf.boolean(srr_wo_gap, air_gap, operation = "A-B", layer = srr_layer) #Creating the final SRR with the air gap using boolean subtraction operation
    srr_ref = c.add_ref(srr) #Adding the SRR to the component as first layer

    #Add flake
    flake = gf.components.rectangle(size = (flake_size, flake_size), layer = flake_layer, centered = True).copy().move((0, (srr_length/2 - srr_arm_width/2))) #Creating the flake and moving it to the top of the SRR
    flake_ref = c.add_ref(flake) #Adding the flake to the component as second layer

    return c #Returning the component with the SRR and flake

#Design Rule Check (DRC) function for the split ring resonator with flake
def srr_drc(srr_length, srr_arm_width, srr_gap, flake_size, srr_layer, flake_layer):
    """
    Design rule check for the split ring resonator with flake.

    Args:
        srr_length: side length of the square split ring resonator.
        srr_arm_width: arm width of the split ring resonator.
        srr_gap: air gap in the split ring resonator.
        flake_size: side length of the square flake.
        srr_layer: layer for the split ring resonator.
        flake_layer: layer for the flake.

    Returns:
        Violations of design rules  as a list of strings.
    """

    violations = [] #Creating an empty list to hold any design rule violations

    if srr_length <= 0.5 or srr_arm_width <= 0.5 or srr_gap <= 0.5 or flake_size <= 0.5:
        violations.append("Minimum feature size of 0.5 um is not met.")
    if srr_arm_width >= srr_length/4:
        violations.append("Arm width of the SRR cannot be larger than a quarter of the SRR side length.")
    if srr_gap >= srr_length/4:
        violations.append("Air gap is too large.")
    if flake_size >= srr_length - 2*srr_arm_width:
        violations.append("Flake size is too large.")
    if srr_layer == flake_layer:
        violations.append("SRR and flake cannot be on the same layer.")
    return violations #Returning the list of design rule violations


#--- OUTPUTS ---
if __name__ == "__main__": #Running the following code only if the script is run directly and not imported as a module
    c_srr = srr_with_flake(
    srr_length = 7.0,
    srr_arm_width = 1.0,
    srr_gap = 1.0,
    flake_size = 2.0,
    srr_layer = (1,0),
    flake_layer = (2,0)) #Calling the function to create a component with a split ring resonator and a flake

    c_srr.write_gds("srr_with_flake.gds") #Writing the component to a GDS file
    print(c_srr) #Printing the component object to the console

    c_srr.plot() #Plotting the component
    plt.show() #Displaying the plot