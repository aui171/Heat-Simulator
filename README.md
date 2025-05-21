# Heat-Simulator

This is a Simulation of a Naive model for Temperature distribution in an electrical component.

The model is based on the 2D PDE (d^2T/dx^2 + d^2T/dy^2) * alpha = dT/dt.

The heat source represents the components that generate heat, and the whole system is cooled down at a constant rate of 3 [K/s] uniformly. The sides are assumed to be perfect Insulator's and remain at 0K.

The Simulator allows to define the material each part of the system is made of, given the choice of 4 materials with the following thermal diffusivity constants:
 
Copper - 1.17 [cm^2/s] - This is the Default material, any part that isn't designated a specific material is made of Copper.
Silver - 1.65 [cm^2/s] 
Rubber - 0.0035 [cm^2/s] - The rubber is used as a very good Insulator.
Silicon - 0.88 [cm^2/s]

These values can be found on the Wikipedia page for Thermal diffusivity.

To use the Simulator after running main.py, you have a white board on which you can select red points, after that if you click Insert material component the Polygon defined by your red points will change material to the one specified. If you click Create heat source the red points will turn into heat sources with the heat rate specified. after you're done selecting click Simulate. 
