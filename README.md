# SATChromaticPlane
# Dependancies
Numpy <br/>
`$ pip install numpy`

Pysat <br/>
Python package integrating modern SAT solvers
Install from: 
https://pysathq.github.io or use pip. <br/>
`$ pip install python-sat`

graphics <br/>
Included in the file graphics.py

# Usage
The program can be run by simplely calling python on allInOne.py, or by adding all the needed parameters in the terminal. If no paremeters 
are given then the program will use the defaults in the file. Alternatively you can run function.py and when it waits for user input run 
your own SAT solver on cnf_file and output to sat_output_file befoer continueing <br/> <br/>
Formate<br/>
python3 allInOne.py k_colors polygon edge_length scale_factor plane_width plane_height cnf_file sat_output_file

k_colors: integer specifieing the number of colors<br/>
polygon: integer specifing how many sides on the polygon (supports 4 and 6)<br/>
edge_length: float specifing the length of the polygon's edge<br/>
scale_factor: float 0 to 1 describing how small of an internal polygon is drawn<br/>
plane_width: float of the length of the plane's width being colored<br/>
plane_height: float of the length of the plane's height being colored<br/>
cnf_file: file name where the cnf formula will be printed to<br/>
sat_output_file: file where cadical will sent it's output to<br/>

Example
python3 allInOne.py 6 6 0.1 0.74 4 4 tile.cnf cadicalOut.txt
This colors a 4x4 plane with hexagons of six colors. The plane is tiled with 0.1 edge length hexagons,
but hexagons of 0.074 edge length are drawn at the center of these and colored.
