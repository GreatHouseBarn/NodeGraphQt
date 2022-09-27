#!/usr/bin/python

# Customisted nodes for network mapping. 2022 Idox Group PLC

from Qt import QtCore, QtGui

from NodeGraphQt import BaseNode
from NodeGraphQt.constants import NODE_LAYOUT_HORIZONTAL

__default_colours__ = [ "#0070C0", "#FFC000", "#00B050", "#C65911",
                        "#BFBFBF", "#FFFFFF", "#FF0000", "#002060",
                        "#FFFF00", "#7030A0", "#FF66CC", "#BDD7EE" ]


def draw_triangle_port(painter, rect, info):
    """
    Custom paint function for drawing a Triangle shaped port.

    Args:
        painter (QtGui.QPainter): painter object.
        rect (QtCore.QRectF): port rect used to describe parameters
                              needed to draw.
        info (dict): information describing the ports current state.
            {
                'port_type': 'in',
                'color': (0, 0, 0),
                'border_color': (255, 255, 255),
                'multi_connection': False,
                'connected': False,
                'hovered': False,
            }
    """
    painter.save()

    size = int(rect.height() / 2)
    triangle = QtGui.QPolygonF()
    triangle.append(QtCore.QPointF(-size, size))
    triangle.append(QtCore.QPointF(0.0, -size))
    triangle.append(QtCore.QPointF(size, size))

    transform = QtGui.QTransform()
    transform.translate(rect.center().x(), rect.center().y())
    port_poly = transform.map(triangle)

    # mouse over port color.
    if info['hovered']:
        color = QtGui.QColor(14, 45, 59)
        border_color = QtGui.QColor(136, 255, 35)
    # port connected color.
    elif info['connected']:
        color = QtGui.QColor(195, 60, 60)
        border_color = QtGui.QColor(200, 130, 70)
    # default port color
    else:
        color = QtGui.QColor(*info['color'])
        border_color = QtGui.QColor(*info['border_color'])

    pen = QtGui.QPen(border_color, 1.8)
    pen.setJoinStyle(QtCore.Qt.MiterJoin)

    painter.setPen(pen)
    painter.setBrush(color)
    painter.drawPolygon(port_poly)

    painter.restore()


def draw_square_port(painter, rect, info):
    """
    Custom paint function for drawing a Square shaped port.

    Args:
        painter (QtGui.QPainter): painter object.
        rect (QtCore.QRectF): port rect used to describe parameters
                              needed to draw.
        info (dict): information describing the ports current state.
            {
                'port_type': 'in',
                'color': (0, 0, 0),
                'border_color': (255, 255, 255),
                'multi_connection': False,
                'connected': False,
                'hovered': False,
            }
    """
    painter.save()

    # mouse over port color.
    if info['hovered']:
        color = QtGui.QColor(14, 45, 59)
        border_color = QtGui.QColor(136, 255, 35, 255)
    # port connected color.
    elif info['connected']:
        color = QtGui.QColor(*info['color'])
        border_color = QtGui.QColor(200, 130, 70)
    # default port color
    else:
        color = QtGui.QColor(*info['color'])
        border_color = QtGui.QColor(*info['border_color'])

    pen = QtGui.QPen(border_color, 1.8)
    pen.setJoinStyle(QtCore.Qt.MiterJoin)

    painter.setPen(pen)
    painter.setBrush(color)
    painter.drawRect(rect)

    painter.restore()

def HTMLColorToRGB(colorstring):
    """ convert #RRGGBB to an (R, G, B) tuple """
    colorstring = colorstring.strip()
    if colorstring[0] == '#': colorstring = colorstring[1:]
    if len(colorstring) != 6:
        raise ValueError("input #%s is not in #RRGGBB format" % colorstring)
    r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
    r, g, b = [int(n, 16) for n in (r, g, b)]
    return (r, g, b)

class TrunkOutNode(BaseNode):
    # set a unique node identifier.
    __identifier__ = 'nodes.network'

    # set the initial default node name.
    NODE_NAME = 'Trunk Cable (out)'

    def __init__(self):
        super(TrunkOutNode, self).__init__()

        # create input and output ports.
        self.add_output('out', color=(200, 10, 0), painter_func=draw_square_port)

        for i in range(12):
            colour = HTMLColorToRGB(__default_colours__[i])
            self.add_input(str(i+1), False, True, colour, False, draw_square_port)

        self.add_label('label', '', tab='Data')

class TrunkInNode(BaseNode):
    # set a unique node identifier.
    __identifier__ = 'nodes.network'

    # set the initial default node name.
    NODE_NAME = 'Trunk Cable (in)'

    def __init__(self):
        super(TrunkInNode, self).__init__()

        # create input and output ports.
        for i in range(12):
            colour = HTMLColorToRGB(__default_colours__[i])
            self.add_output(str(i+1), False, True, colour, False, draw_square_port)

        self.add_input('in', color=(200, 10, 0), painter_func=draw_square_port)

        self.add_label('label', '', tab='Data')

class Splitter1x4Node(BaseNode):
    # set a unique node identifier.
    __identifier__ = 'nodes.network'

    # set the initial default node name.
    NODE_NAME = 'Splitter 1x4'

    def __init__(self):
        super(Splitter1x4Node, self).__init__()

        # create input and output ports.
        self.add_input('in', color=(200, 10, 0), painter_func=draw_square_port)

        for i in range(4):
            self.add_output(str(i+1), False, True, (200, 10, 0), False, draw_square_port)

        self.add_label('label', '', tab='Data')


class Splitter1x8Node(BaseNode):
    # set a unique node identifier.
    __identifier__ = 'nodes.network'

    # set the initial default node name.
    NODE_NAME = 'Splitter 1x8'

    def __init__(self):
        super(Splitter1x8Node, self).__init__()

        # create input and output ports.
        self.add_input('in', color=(200, 10, 0), painter_func=draw_square_port)

        for i in range(8):
            self.add_output(str(i+1), False, True, (200, 10, 0), False, draw_square_port)

        self.add_label('label', '', tab='Data')

class Splitter1x16Node(BaseNode):
    # set a unique node identifier.
    __identifier__ = 'nodes.network'

    # set the initial default node name.
    NODE_NAME = 'Splitter 1x16'

    def __init__(self):
        super(Splitter1x16Node, self).__init__()

        # create input and output ports.
        self.add_input('in', color=(200, 10, 0), painter_func=draw_square_port)

        for i in range(16):
            self.add_output(str(i+1), False, True, (200, 10, 0), False, draw_square_port)

        self.add_label('label', '', tab='Data')

class Splitter1x32Node(BaseNode):
    # set a unique node identifier.
    __identifier__ = 'nodes.network'

    # set the initial default node name.
    NODE_NAME = 'Splitter 1x32'

    def __init__(self):
        super(Splitter1x32Node, self).__init__()

        # create input and output ports.
        self.add_input('in', color=(200, 10, 0), painter_func=draw_square_port)

        for i in range(32):
            self.add_output(str(i+1), False, True, (200, 10, 0), False, draw_square_port)

        self.add_label('label', '', tab='Data')

class DPInNode(BaseNode):
    # set a unique node identifier.
    __identifier__ = 'nodes.network'

    # set the initial default node name.
    NODE_NAME = 'D.P. (in)'

    def __init__(self):
        super(DPInNode, self).__init__()

        # create input and output ports.
        self.add_output('out', color=(200, 10, 0), painter_func=draw_square_port)
        self.add_label('label', '', tab='Data')

class DPOutNode(BaseNode):
    # set a unique node identifier.
    __identifier__ = 'nodes.network'

    # set the initial default node name.
    NODE_NAME = 'D.P. (out)'

    def __init__(self):
        super(DPOutNode, self).__init__()

        # create input and output ports.
        self.add_input('in', color=(200, 10, 0), painter_func=draw_square_port)
        self.add_label('label', '', tab='Data')

class MDUNode(BaseNode):
    # set a unique node identifier.
    __identifier__ = 'nodes.network'

    # set the initial default node name.
    NODE_NAME = 'MDU'

    def __init__(self):
        super(MDUNode, self).__init__()

        # create input and output ports.
        self.add_input('in', color=(200, 10, 0), painter_func=draw_square_port, multi_input=True)
        self.add_label('label', '', tab='Data')