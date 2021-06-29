from splayout.utils import *
from splayout.waveguide import Waveguide
from splayout.polygon import Polygon


def MAKE_AEMD_GRATING(port_width=0.45,waveguide_layer=Layer(1,0),etch_layer=Layer(2,0),grating_number=40,grating_period=0.63,grating_duty=0.3/0.63):
    port_waveguide_width = port_width
    grating_number = grating_number
    grating_period = grating_period
    grating_duty = grating_duty
    grating_width = 18

    grating_polygon = Polygon(
        [ (226.71000, -7.44000),  (186.71500, -6.36500),
          (146.72500, -4.91400),  (106.71500, -3.46200),
          (18.22500, -0.26900),   (8.22700, -0.26900),
          (4.16200, -0.25000),    (0.00000, -port_waveguide_width / 2),
          (0.00000, port_waveguide_width / 2),  (4.16200, 0.25000),
          (8.22700, 0.27000), (18.22500, 0.27000),
          (106.73400, 3.46200),  (186.71500, 6.36400),
          (226.71000, 7.43900),  (276.35500, 7.43900),
          (276.35500, -7.44000)])

    grating_etch_list = []
    for i in range(0, grating_number):
        grating_etch_list.append(Waveguide( Point(246.061, 0.207) - (grating_period *grating_duty/2, 0) + (
                grating_period * i, 0),
            Point(246.061, 0.207) + (grating_period * grating_duty/2, 0) + (
                grating_period * i, 0),
            width=grating_width))
    global AEMD_grating_cell
    AEMD_grating_cell = Cell("AEMD_GRATING" )
    grating_polygon.draw(AEMD_grating_cell, waveguide_layer)
    for item in grating_etch_list:
        item.draw(AEMD_grating_cell, etch_layer)

    class AEMDgrating():
        def __init__(self,start_point,relative_position):
            self.start_point = start_point
            self.rotate_angle = relative_position

        def draw(self, cell, *args):
            '''
            Put the Component on the layout
            :param cell:
            :param args:
            :return:
            '''
            global AEMD_grating_cell

            cell.cell.add(gdspy.CellReference(AEMD_grating_cell.cell, (self.start_point.x, self.start_point.y),rotation=self.rotate_angle))

            return self.start_point

    return AEMDgrating