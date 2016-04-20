""" Nielsen, Louise makes recursive art.
"""

import random
import math
from PIL import Image


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)

        this function has no doctests because i did not want to do pseudorandom
        stuff.
    """
    # funcs is a list of the names of the functions
    funcs = ['x', 'y', 'prod', 'avg', 'cos_pi', 'sin_pi', 'square', 'cube']
    # chooses a random function from funcs
    random_func = random.choice(funcs)
    # following if/elif string describes the return for each of the functions
    # some of them return only themselves, some return another recursion
    if random_func in ['x', 'y']:
        return [random_func]
    elif random_func in ['prod', 'avg']:
        return [random_func, build_random_function(min_depth - 1, max_depth - 1), build_random_function(min_depth - 1, max_depth - 1)]
    elif random_func in ['cos_pi', 'sin_pi', 'square', 'cube']:
        return [random_func, build_random_function(min_depth - 1, max_depth - 1)]
    # this if/elif string has three cases
    # if it is almost at the maximum depth, return 'x' or 'y' to end recursion
    if max_depth == 0:
        return random.choice(funcs[:2])
    # if past minimum depth, return any function
    elif min_depth == 0:
        return random.choice(funcs)
    # otherwise, return only functions that allow another level of recursion
    else:
        return random.choice(funcs[2:])


def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        the long string of ifs and elifs that is this entire function defines
        what math happens for each of the functions. if the zero entry in the
        list is the name of the particular function, it returns the result of
        the appropriate math.

        the doctests test all of the possible functions and also test to two
        levels of recursion.

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
        >>> evaluate_random_function(['prod', ['sin_pi', ['x']], ['cos_pi', ['x']]], .1, -.2)
        0.2938926261462365
        >>> evaluate_random_function(['avg', ['square', ['x']], ['cube', ['y']]], .1, -.2)
        0.001
    """
    args = [evaluate_random_function(arg) for arg in f[1:]]
    if f[0] == 'x':
        return x
    elif f[0] == 'y':
        return y
    elif f[0] == 'prod':
        return args[0] * args[1]
    elif f[0] == 'avg':
        return .5 * (args[0] + args[1])
    elif f[0] == 'cos_pi':
        return math.cos(math.pi * args[0])
    elif f[0] == 'sin_pi':
        return math.sin(math.pi * args[0])
    elif f[0] == 'square':
        return args[0] ** 2
    elif f[0] == 'cube':
        return args[0] ** 3


def remap_interval(val,
                   input_interval_min,
                   input_interval_max,
                   output_interval_min,
                   output_interval_max):
    """ Given an input value in the interval [input_interval_min,
        input_interval_max], return an output value scaled to fall within
        the output interval [output_interval_min, output_interval_max].

        val: the value to remap
        input_interval_min: the start of the interval that contains all
                              possible values for val
        input_interval_max: the end of the interval that contains all possible
                            values for val
        output_interval_min: the start of the interval that contains all
                               possible output values
        output_inteval_max: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    # define the output and input intervals
    output_interval = float(output_interval_max - output_interval_min)
    input_interval = float(input_interval_max - input_interval_min)
    # if you treat the ratio as m in y=mx+b, returns mx+b
    ratio = output_interval / input_interval
    return (val - input_interval_min) * ratio + output_interval_min


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7, 12)
    green_function = build_random_function(7, 12)
    blue_function = build_random_function(7, 12)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    # import doctest
    # doctest.testmod()
    # doctest.run_docstring_examples(evaluate_random_function, globals())

    # Create some computational art!
    generate_art("myart3.png")
