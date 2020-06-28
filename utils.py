import cv2
import numpy as np 
import scipy.interpolate

def createCurveFunc(points):

    if points is None:
        return None
    num_points = len(points)

    if num_points < 2:
        return None

    xs, ys = zip(*points)
    if num_points < 4:
        kind = 'linear'
    else:
        kind = 'cubic'
    return scipy.interpolate.interp1d(xs, ys, kind, bounds_error = False)


def createLookupArray(func, length = 256):
    if func is None:
        return None
    lookup_array = np.empty(length)
    i = 0
    while i < length:
        func_i = func(i)
        lookup_array[i] = min(max(0, func_i), length - 1)
        i += 1
    return lookup_array


def applyLookupArray(lookup_array, src, dst):
    if lookup_array is None:
        return None
    dst[:] = lookup_array[src]


def createCompositeFunc(func0, func1):
    if func0 is None:
        return func1
    if func1 is None:
        return func0
    return lambda x : func0(func1(x))


def createFlatView(array):
    flat_view = array.view()
    flat_view.shape = array.size
    return flat_view