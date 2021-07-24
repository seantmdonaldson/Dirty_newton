import sympy as sy
import matplotlib.pyplot as plt


# functions
def parabola_function(x_val, focus):
    parabola_function = (x_val**2) / (4 * focus)
    return parabola_function


def calc_parabola(x_domain, focus):
    y_domain = []
    for x_val in x_domain:
        y_domain.append(parabola_function(x_val, focus))
    return y_domain


def parab_derivative(focus):
    p = focus
    x = sy.symbols('x') # the x value
    parab_function = ((x**2) / (4 * p))
    parab_derivative = sy.diff(parab_function, x)
    print(f"Derivative: \n\n{parab_derivative}\n")
    return parab_derivative
    

def parab_linelength(derivative):
    x, r = sy.symbols('x r') # r is the radius of the aperture
    distance = sy.sqrt((1+(derivative)**2))
    integral = sy.integrate(distance, (x, 0, r)) 
    print(f"Definite integral: \n\n{integral}\n")
    return integral
    

def focus_lines(x_domain, focus, aperture):
    # build domain to graph intersecting lines to the focus
    y_domain = []
    x2 = half_aperture = aperture / 2
    y2 = parabola_function(half_aperture, focus)
    slope = (y2 - focus) / (x2)
    for x_val in x_domain:
        y_val = slope * (x_val - x2) + y2
        y_domain.append(y_val)
    return y_domain


def inverse_xdomain(x_domain):
    new_domain = []
    for x_val in x_domain:
        new_domain.append(-x_val)
    return new_domain


def find_aperture(indef_integral, arc_length):
    r = sy.symbols('r')
    f = indef_integral - (arc_length/2)
    radius = sy.nsolve(f, (r), arc_length) #arc_length provides an initial guess, in this case.
    diameter = radius * 2
    print("Aperture diameter: {:.6} mm".format(str(diameter)))
    print("Aperture radius: {:.6} mm".format(str(radius)))
    return diameter


def calc_focalratio(aperture, focal_len):
    fN = focal_len / aperture
    print("Focal Ratio (f/N): {:.3}".format(str(fN)))
    
    
def inch_or_milli():
    focal_len = int(input('Enter desired focal length (EX: "900"):\n'))
    sheet_wid = int(input('Enter width of material to be formed(EX: "127")\n'))
    inch_len = focal_len/(25.4)
    inch_wid = sheet_wid/(25.4)
    print('\nmm to inches conversion:\nfocal length {:.4}"\nsheet width {:.3}"\n'.format(inch_len, inch_wid))
    return focal_len, sheet_wid


# attributes & operations
sy.init_printing()
print("Dimensions in mm")
focal_length, sheet_width = inch_or_milli()         
x_axis = list(range(int(-(sheet_width/2)), int(((sheet_width+2)/2))))
parabola = calc_parabola(x_axis, focal_length)
x_axis_inverse = inverse_xdomain(x_axis) # create inverse x axis for focal line
deriv = parab_derivative(focal_length)
parab_int = parab_linelength(deriv)
aperture = find_aperture(parab_int, sheet_width)
calc_focalratio(aperture, focal_length)
focus_y = focus_lines(x_axis, focal_length, aperture)
mirror_depth = parabola_function((aperture/2), focal_length)
print("Mirror depth: {:.5}".format(str(mirror_depth)) + " mm")



# 2D plotting
fig, axs = plt.subplots(1, 2)
axs[0].set_xlim(-(sheet_width/2) - 10, (sheet_width/2) + 10) # visual restriction of x axis
axs[0].set_ylim(0, focal_length + 50) # visual restriction of y axis
axs[0].plot(x_axis, parabola) # plot main parabola
axs[0].plot(focal_length, 'bo') # plot the focus, or end of the focal length
axs[0].plot(x_axis, focus_y)
axs[0].plot(x_axis_inverse, focus_y)
axs[1].set_xlim(-(sheet_width/2) - 10, (sheet_width/2) + 10) # visual restriction of x axis
axs[1].plot(x_axis, parabola) # plot main parabola

#
plt.show()

