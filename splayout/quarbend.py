from splayout.utils import *
from splayout.waveguide import Waveguide
from splayout.bend import Bend
from splayout.fdtdapi import FDTDSimulation
from splayout.modeapi import MODESimulation

## anticlockwise
class AQuarBend:
    """
    Anticlockwise Connector Definition in SPLayout with an anticlockwise bend and two waveguides.

    Parameters
    ----------
    start_point : Point
        Start point of the connector.
    end point : Point
        End point of the connector.
    width : float
        Width of the waveguides (μm).
    radius : float
        Radius of the bend (μm).
    z_start : Float
        The start point for the structure in z axis (unit: μm, default: None, only useful when draw on CAD).
    z_end : Float
        The end point for the structure in z axis (unit: μm, default: None, only useful when draw on CAD).
    material : str or float
        Material setting for the structure in Lumerical FDTD (SiO2 = "SiO2 (Glass) - Palik", SiO2 = "SiO2 (Glass) - Palik"). When it is a float, the material in FDTD will be
        <Object defined dielectric>, and index will be defined. (default: None, only useful when draw on CAD)
    """

    def __init__(self,start_point,end_point,width,radius=5, z_start = None, z_end = None, material = None):
        self.start_point = tuple_to_point(start_point)
        self.end_point = tuple_to_point(end_point)
        self.radius = radius
        self.width = width
        self.z_start = z_start
        self.z_end = z_end
        self.material = material

        if (start_point.x < end_point.x and start_point.y > end_point.y): ## left down type
            if (end_point.x - start_point.x < self.radius) or (start_point.y - end_point.y < self.radius):
                raise Exception("Distance between two point is too short!")
            self.first_waveguide = Waveguide(start_point,Point(start_point.x,end_point.y + self.radius),self.width, self.z_start, self.z_end, self.material)
            self.center_bend = Bend(Point(start_point.x + self.radius, end_point.y + self.radius), math.pi, math.pi*3/2, self.width , self.radius, self.z_start, self.z_end, self.material)
            self.second_waveguide = Waveguide(Point(start_point.x + self.radius,end_point.y),end_point ,self.width, self.z_start, self.z_end, self.material)

        if (start_point.x < end_point.x and start_point.y < end_point.y): ## right down type
            if (end_point.x - start_point.x < self.radius) or (end_point.y - start_point.y < self.radius):
                raise Exception("Distance between two point is too short!")
            self.first_waveguide = Waveguide(start_point,Point(end_point.x - self.radius,start_point.y),self.width, self.z_start, self.z_end, self.material)
            self.center_bend = Bend(Point(end_point.x - self.radius, start_point.y + self.radius), -math.pi/2, 0 , self.width , self.radius, self.z_start, self.z_end, self.material)
            self.second_waveguide = Waveguide(Point(end_point.x,start_point.y + self.radius),end_point ,self.width, self.z_start, self.z_end, self.material)

        if (start_point.x > end_point.x and start_point.y < end_point.y):  ## right up type
            if (start_point.x - end_point.x < self.radius) or (
                    end_point.y - start_point.y < self.radius):
                raise Exception("Distance between two point is too short!")
            self.first_waveguide = Waveguide(start_point, Point(start_point.x, end_point.y - self.radius), self.width, self.z_start, self.z_end, self.material)
            self.center_bend = Bend(Point(start_point.x - self.radius, end_point.y - self.radius), 0 , math.pi / 2,
                                    self.width, self.radius, self.z_start, self.z_end, self.material)
            self.second_waveguide = Waveguide(Point(start_point.x - self.radius, end_point.y), end_point, self.width, self.z_start, self.z_end, self.material)


        if (start_point.x > end_point.x and start_point.y > end_point.y): ## left up type
            if (start_point.x - end_point.x < self.radius) or (start_point.y - end_point.y < self.radius):
                raise Exception("Distance between two point is too short!")
            self.first_waveguide = Waveguide(start_point,Point(end_point.x + self.radius,start_point.y),self.width, self.z_start, self.z_end, self.material)
            self.center_bend = Bend(Point(end_point.x + self.radius, start_point.y - self.radius), math.pi/2, math.pi, self.width , self.radius, self.z_start, self.z_end, self.material)
            self.second_waveguide = Waveguide(Point(end_point.x,start_point.y - self.radius),end_point ,self.width, self.z_start, self.z_end, self.material)

    def draw(self,cell,layer):
        """
        Draw the Component on the layout.

        Parameters
        ----------
        cell : Cell
            Cell to draw the component.
        layer : Layer
            Layer to draw.

        Returns
        -------
        out : Point,Point
            Start point and end point.
        """
        self.first_waveguide.draw(cell,layer)
        self.center_bend.draw(cell,layer)
        self.second_waveguide.draw(cell,layer)
        return self.start_point, self.end_point

    def draw_on_lumerical_CAD(self, engine):
        """
        Draw the Component on the lumerical CAD (FDTD or MODE).

        Parameters
        ----------
        engine : FDTDSimulation or MODESimulation
            CAD to draw the component.
        """
        if ((type(engine) == FDTDSimulation) or (type(engine) == MODESimulation)):
            if (type(self.z_start) != type(None) and type(self.z_end) != type(None) and type(self.material) != type(None) ):
                self.first_waveguide.draw_on_lumerical_CAD(engine)
                self.center_bend.draw_on_lumerical_CAD(engine)
                self.second_waveguide.draw_on_lumerical_CAD(engine)
            else:
                raise Exception("Z-axis specification or material specification is missing!")
        else:
            raise Exception("Wrong CAD engine!")

    def get_start_point(self):
        """
        Derive the start point of the connector.

        Returns
        -------
        out : Point
            Start point.
        """
        return  self.start_point

    def get_end_point(self):
        """
        Derive the end point of the connector.

        Returns
        -------
        out : Point
            End point.
        """
        return  self.end_point


class QuarBend:
    """
    Clockwise Connector Definition in SPLayout with an anticlockwise bend and two waveguides.

    Parameters
    ----------
    start_point : Point
        Start point of the connector.
    end point : Point
        End point of the connector.
    width : float
        Width of the waveguides (μm).
    radius : float
        Radius of the bend (μm).
    z_start : Float
        The start point for the structure in z axis (unit: μm, default: None, only useful when draw on CAD).
    z_end : Float
        The end point for the structure in z axis (unit: μm, default: None, only useful when draw on CAD).
    material : str or float
        Material setting for the structure in Lumerical FDTD (SiO2 = "SiO2 (Glass) - Palik", SiO2 = "SiO2 (Glass) - Palik"). When it is a float, the material in FDTD will be
        <Object defined dielectric>, and index will be defined. (default: None, only useful when draw on CAD)
    """
    def __init__(self,start_point,end_point,width,radius=5, z_start = None, z_end = None, material = None):
        self.start_point = tuple_to_point(start_point)
        self.end_point = tuple_to_point(end_point)
        self.radius = radius
        self.width = width
        self.z_start = z_start
        self.z_end = z_end
        self.material = material

        if (start_point.x < end_point.x and start_point.y > end_point.y): ## right up type
            if (end_point.x - start_point.x < self.radius) or (start_point.y - end_point.y < self.radius):
                raise Exception("Distance between two point is too short!")
            self.first_waveguide = Waveguide(start_point,Point(end_point.x - self.radius,start_point.y),self.width, self.z_start, self.z_end, self.material)
            self.center_bend = Bend(Point(end_point.x - self.radius, start_point.y - self.radius), 0, math.pi/2, self.width , self.radius, self.z_start, self.z_end, self.material)
            self.second_waveguide = Waveguide(Point(end_point.x,start_point.y - self.radius),end_point ,self.width, self.z_start, self.z_end, self.material)

        if (start_point.x < end_point.x and start_point.y < end_point.y): ## left up type
            if (end_point.x - start_point.x < self.radius) or (end_point.y - start_point.y < self.radius):
                raise Exception("Distance between two point is too short!")
            self.first_waveguide = Waveguide(start_point,Point(start_point.x,end_point.y - self.radius),self.width, self.z_start, self.z_end, self.material)
            self.center_bend = Bend(Point(start_point.x + self.radius, end_point.y - self.radius), math.pi/2, math.pi , self.width , self.radius, self.z_start, self.z_end, self.material)
            self.second_waveguide = Waveguide(Point(start_point.x + self.radius,end_point.y),end_point ,self.width, self.z_start, self.z_end, self.material)

        if (start_point.x > end_point.x and start_point.y < end_point.y):  ## down left type
            if (start_point.x - end_point.x < self.radius) or (
                    end_point.y - start_point.y < self.radius):
                raise Exception("Distance between two point is too short!")
            self.first_waveguide = Waveguide(start_point, Point(end_point.x + self.radius, start_point.y), self.width, self.z_start, self.z_end, self.material)
            self.center_bend = Bend(Point(end_point.x + self.radius, start_point.y + self.radius), math.pi , math.pi*3 / 2,
                                    self.width, self.radius, self.z_start, self.z_end, self.material)
            self.second_waveguide = Waveguide(Point(end_point.x, start_point.y + self.radius), end_point, self.width, self.z_start, self.z_end, self.material)


        if (start_point.x > end_point.x and start_point.y > end_point.y): ## right down type
            if (start_point.x - end_point.x < self.radius) or (start_point.y - end_point.y < self.radius):
                raise Exception("Distance between two point is too short!")
            self.first_waveguide = Waveguide(start_point,Point(start_point.x,end_point.y + self.radius),self.width, self.z_start, self.z_end, self.material)
            self.center_bend = Bend(Point(start_point.x - self.radius, end_point.y + self.radius),  - math.pi/2, 0 , self.width , self.radius, self.z_start, self.z_end, self.material)
            self.second_waveguide = Waveguide(Point(start_point.x - self.radius,end_point.y),end_point ,self.width, self.z_start, self.z_end, self.material)

    def draw(self,cell,layer):
        """
        Draw the Component on the layout.

        Parameters
        ----------
        cell : Cell
            Cell to draw the component.
        layer : Layer
            Layer to draw.

        Returns
        -------
        out : Point,Point
            Start point and end point.
        """
        self.first_waveguide.draw(cell,layer)
        self.center_bend.draw(cell,layer)
        self.second_waveguide.draw(cell,layer)
        return self.start_point, self.end_point

    def draw_on_lumerical_CAD(self, engine):
        """
        Draw the Component on the lumerical CAD (FDTD or MODE).

        Parameters
        ----------
        engine : FDTDSimulation or MODESimulation
            CAD to draw the component.
        """
        if ((type(engine) == FDTDSimulation) or (type(engine) == MODESimulation)):
            if (type(self.z_start) != type(None) and type(self.z_end) != type(None) and type(self.material) != type(None) ):
                self.first_waveguide.draw_on_lumerical_CAD(engine)
                self.center_bend.draw_on_lumerical_CAD(engine)
                self.second_waveguide.draw_on_lumerical_CAD(engine)
            else:
                raise Exception("Z-axis specification or material specification is missing!")
        else:
            raise Exception("Wrong CAD engine!")

    def get_start_point(self):
        """
        Derive the start point of the connector.

        Returns
        -------
        out : Point
            Start point.
        """
        return  self.start_point

    def get_end_point(self):
        """
        Derive the end point of the connector.

        Returns
        -------
        out : Point
            End point.
        """
        return  self.end_point