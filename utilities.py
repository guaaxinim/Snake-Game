from collections import namedtuple

#region Classes utilities/namespaces/PODs
class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

MouseInfo = namedtuple("MouseInfo", ("left", "middle", "right", "x", "y"))
Point = namedtuple("Point", ("x", "y"))
#endregion