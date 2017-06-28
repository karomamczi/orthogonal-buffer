# -*- coding: utf-8 -*-

############################
# Nazwa pliku: OrthogonalBuffer.py
# Autor: Karolina Mamczarz
# Nr albumu: 260692
# Data ostaniej aktualizacji: 2017-02-15
# Wersja: 1.0.0
# Opis: Stworzenie obiektu poligonowego bedącego buforem ortogonalnym wokół obiektów punktowych.
# Klasa: OrtoBuff
# Metody: __init__, CreateNewFeature, NewGeom_d_az, NewGeom_d, NewGeom_az, NewGeom
# Parametry: warstwa wejściowa,
#            wybór stałej lub zmiennej wartości bufora,
#            wielkość bufora (w jednostkach projektu),
#            pole atrybutowe dla wielkości bufora,
#            wybór stałego lub zmiennego kąta,
#            wartość azymutu skręcenia (w stopniach dziesiętnych),
#            pole atrybutowe dla wartość azymutu skręcenia,
#            warstwa wynikowa.
# Wynik: Bufor ortogonalny - klasa obiektów typu poligon zapisana w folderze wskazanym przez użytkownika.
############################

import arcpy
import os
from math import pi,cos,sin,sqrt


class OrthoBuff(object):

    def __init__(self,feature,choose_d,d,d_attr,choose_az,az,az_attr,new_feature):
        try:
            self.feature = feature
            self.choose_d = choose_d
            self.d = d
            self.d_attr = d_attr
            self.choose_az = choose_az
            self.az = az
            self.az_attr = az_attr
            self.out_file = new_feature
        except:
            arcpy.AddMessage("Błąd przy uruchamianiu Python Toolbox.")

    def CreateNewFeature(self):
        path, file = os.path.split(self.out_file)
        filename, fileext = os.path.splitext(file)
        arcpy.CreateFeatureclass_management(path, filename, "POLYGON","","","",self.feature)
        container, containerext = os.path.splitext(path)
        if containerext == ".gdb" or containerext == ".mdb" or containerext == ".sde":
            file = filename
        self.fullpathname = path + "\\" + file
        return self.fullpathname

    def NewGeom_d_az(self):
        l = [45, 135, 225, 315]
        cursor = arcpy.da.SearchCursor(self.feature,["SHAPE@XY",self.d_attr,self.az_attr])
        cursor_new = arcpy.da.InsertCursor(self.fullpathname, ["SHAPE@"])
        for row in cursor:
            p = row[0]
            d = row[1]
            az = row[2]
            array = arcpy.Array()
            for i in l:
                x = p[0] + (d*sqrt(2.0))*cos(((i+(90-az))*pi)/180)
                y = p[1] + (d*sqrt(2.0))*sin(((i+(90-az))*pi)/180)
                array.add(arcpy.Point(x,y))
            cursor_new.insertRow([arcpy.Polygon(array)])
            array.removeAll()
        return

    def NewGeom_d(self):
        l = [45, 135, 225, 315]
        cursor = arcpy.da.SearchCursor(self.feature,["SHAPE@XY",self.d_attr])
        cursor_new = arcpy.da.InsertCursor(self.fullpathname, ["SHAPE@"])
        for row in cursor:
            p = row[0]
            d = row[1]
            az = float(self.az)
            array = arcpy.Array()
            for i in l:
                x = p[0] + (d*sqrt(2.0))*cos(((i+(90-az))*pi)/180)
                y = p[1] + (d*sqrt(2.0))*sin(((i+(90-az))*pi)/180)
                array.add(arcpy.Point(x,y))
            cursor_new.insertRow([arcpy.Polygon(array)])
            array.removeAll()
        return

    def NewGeom_az(self):
        l = [45, 135, 225, 315]
        cursor = arcpy.da.SearchCursor(self.feature,["SHAPE@XY",self.az_attr])
        cursor_new = arcpy.da.InsertCursor(self.fullpathname, ["SHAPE@"])
        for row in cursor:
            p = row[0]
            d = float(self.d)
            az = row[1]
            array = arcpy.Array()
            for i in l:
                x = p[0] + (d*sqrt(2.0))*cos(((i+(90-az))*pi)/180)
                y = p[1] + (d*sqrt(2.0))*sin(((i+(90-az))*pi)/180)
                array.add(arcpy.Point(x,y))
            cursor_new.insertRow([arcpy.Polygon(array)])
            array.removeAll()
        return

    def NewGeom(self):
        l = [45, 135, 225, 315]
        cursor = arcpy.da.SearchCursor(self.feature,["SHAPE@XY"])
        cursor_new = arcpy.da.InsertCursor(self.fullpathname, ["SHAPE@"])
        for row in cursor:
            p = row[0]
            d = float(self.d)
            az = float(self.az)
            array = arcpy.Array()
            for i in l:
                x = p[0] + (d*sqrt(2.0))*cos(((i+(90-az))*pi)/180)
                y = p[1] + (d*sqrt(2.0))*sin(((i+(90-az))*pi)/180)
                array.add(arcpy.Point(x,y))
            cursor_new.insertRow([arcpy.Polygon(array)])
            array.removeAll()
        return

    def Choice(self):
        if self.choose_d == "Pole atrybutowe" and self.choose_az == "Pole atrybutowe":
            self.NewGeom_d_az()
        elif self.choose_d == "Stala" and self.choose_az == "Pole atrybutowe":
            self.NewGeom_az()
        elif self.choose_d == "Pole atrybutowe" and self.choose_az == "Stala":
            self.NewGeom_d()
        elif self.choose_d == "Stala" and self.choose_az == "Stala":
            self.NewGeom()


if __name__ == '__main__':
    poi = OrthoBuff(arcpy.GetParameterAsText(0),arcpy.GetParameterAsText(1),arcpy.GetParameterAsText(2),
                   arcpy.GetParameterAsText(3),arcpy.GetParameterAsText(4),arcpy.GetParameterAsText(5),
                   arcpy.GetParameterAsText(6),arcpy.GetParameterAsText(7))
    poi.CreateNewFeature()
    poi.Choice()