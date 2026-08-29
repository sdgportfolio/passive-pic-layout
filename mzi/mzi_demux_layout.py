#Importing GDSFactory libraries
import gdsfactory as gf
from functools import partial
import matplotlib.pyplot as plt
gf.gpdk.PDK.activate()
print("PDK activated") #Confirming all necessary libraries and PDK have been activated


#--- GEOMETRIES ---
xs = gf.cross_section.strip(width = 0.5) #Defining the cross-section for the waveguides

mmi_splitter = gf.components.mmi1x2(
    width_mmi = 6.0,
    length_mmi = 31.0,
    gap_mmi = 0.5,
    cross_section = xs,
) #Defining the geometry of the 1x2 multi-mode interference (MMI) splitter

mmi_combiner = gf.components.mmi2x2(
    width_mmi = 6.0,
    length_mmi = 31.0,
    gap_mmi = 0.5,
    cross_section = xs,
) #Defining the geometry of the 2x2 multi-mode interference (MMI) coupler

mzi = gf.components.mzi1x2_2x2(
    delta_length = 140.27,
    length_x = 500.0,
    length_y = 20.0,
    bend = partial(gf.components.bend_euler, radius = 10.0, cross_section = xs),
    straight = partial(gf.components.straight, cross_section = xs),
    splitter = mmi_splitter,
    combiner = mmi_combiner,
    with_splitter = True,
    cross_section = xs,
) #Defining the geometry of an MZI


#--- COMPONENTS ---
c = gf.Component("MZI_demux_top") #Creating the component
mzi_ref = c.add_ref(mzi) #Adding the MZI reference
c.add_ports(mzi_ref.ports) #Adding ports

gc = gf.components.grating_coupler_elliptical_te(cross_section = xs) #Defining the geometry of the grating coupler
c = gf.routing.add_fiber_array(component = c, grating_coupler = gc, cross_section = xs, with_loopback = False, 
    #Layout-cleanup parameters
    pitch = 150.0,
    fanout_length = 100.0,
    straight_separation = 25.0,
    radius = 20.0,
    start_straight_length = 20.0,
    end_straight_length = 20.0) #Adding fiber array


#--- OUTPUTS ---
if __name__ == "__main__": #Main execution block
    c.write_gds(r"C:\Users\shroy\VSCode Files\mzi_demux_layout.gds") #Writing the GDS file
    c.plot() #Plotting the component
    plt.show() #Displaying the plot
    print(c) #Printing the component information