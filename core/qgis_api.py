from qgis.PyQt.QtCore import QObject, pyqtSlot
from qgis.core import (
    QgsProject, QgsUnitTypes, QgsMapLayer, QgsRasterLayer,
    QgsVectorLayer, QgsWkbTypes, QgsProcessingFeatureSourceDefinition
)

import processing
import uuid
import tempfile
import os

class QGISApi(QObject):
    def __init__(self, iface):
        super().__init__()
        self.result = None
        self.needs_update = False
        self._temp_files = []
        self.iface = iface

    @pyqtSlot('PyQt_PyObject', result='PyQt_PyObject')
    def dispatch(self, msg):
        method = msg.get('method')
        match method:
            case "list_layers":
                self.result = self.list_layers(msg.get("args", {}))
            case "get_layer":
                self.result = self.get_layer(msg.get("args", {}))
            case "insert_layer":
                self.result = self.insert_layer(msg.get("args", {}))
            case "layer_info":
                self.result = self.get_layer_info(msg.get("args", {}))
            case "project_state":
                self.result = self.project_state()
            case "canvas_extent":
                self.result = self.get_canvas_extent()
            case "selected_features":
                self.result = self.get_selected_features()
            case _:
                self.result = {"type": "response", "error": f"Unknown method: {method}"}
        
        return self.result
    
    @pyqtSlot(result='PyQt_PyObject')
    def project_state(self):
        project = QgsProject.instance()
        result = {
            "type": "response",
            "title": project.title(),
            "path": project.homePath(),
            "crs": project.crs().userFriendlyIdentifier(),
            "units": QgsUnitTypes.toString(project.crs().mapUnits())
        }
        return result

    def list_layers(self, args):
        type = args.get("type")
        
        if type is not None:
            type = int(type)

        layers = QgsProject.instance().mapLayers().values()
        return {
            "type": "response",
            "layers": [{"name": l.name(), "id": l.id(), "type": l.type()} 
                       for l in layers 
                       if type is None or l.type() == type]
        }

    def get_layer(self, args):
        column = args.get("col")
        field = args.get("value")
        
        if column == "name":
            layer = QgsProject.instance().mapLayersByName(field)
            if not layer:
                return {"type": "error", "error": f"Layer not found: {field}"}
            layer = layer[0]
        elif column == "id":
            layer = QgsProject.instance().mapLayer(field)
            if layer is None:
                return {"type": "error", "error": f"Layer not found: {field}"}
        else: 
            result = {"type": "error", "error": f"Unknown layer: {column}"}
            return result

        if layer.providerType() in ("wms", "bing", "xyz"):
            return {"type": "response", "error": f"Layer '{field}' is a base map and cannot be exported"}

        type = layer.type()
        if type == QgsMapLayer.VectorLayer:
            path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4().hex}.fgb")
            processing.run("native:savefeatures", {'INPUT': layer, 'OUTPUT': path})
        elif type == QgsMapLayer.RasterLayer:
            path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4().hex}.tif")
            processing.run("gdal:translate", {'INPUT': layer, 'OUTPUT': path, 'OPTIONS': ''})
        else:
            return {"type": "error", "error": f"Unsupported layer type: {type}"}

        self._temp_files.append(path)
        return {"type": "response", "path": path}
    
    def insert_layer(self, args):
        path = args.get("path")
        if not os.path.exists(path):
            return {"type": "error", "error": f"Layer not found: {path}"}
        
        name = args.get("name")
        if not name:
            name = os.path.splitext(os.path.basename(path))[0]

        existing = QgsProject.instance().mapLayersByName(name)
        if existing:
            name = f"{name}_{len(existing)}"

        ext = os.path.splitext(path)[1].lower()
        if ext == ".tif":
            layer = QgsRasterLayer(path, name)
        else:
            layer = QgsVectorLayer(path, name, "ogr")

        if not layer.isValid():
            return {"type": "error", "error": f"Invalid layer: {path}"}
        
        QgsProject.instance().addMapLayer(layer)
        self._temp_files.append(path)
        return {"type": "response", "id": layer.id()}
    
    def get_canvas_extent(self):
        response = {
            "type": "response",
            "wkt": self.iface.mapCanvas().extent().asWktPolygon(), 
            "crs": self.iface.mapCanvas().mapSettings().destinationCrs().authid()
            }
        return response

    def get_selected_features(self):
        layer = self.iface.activeLayer()
        
        if layer is None:
            self.result = {"type": "response", "error": "No active layer"}
            return
        
        if not hasattr(layer, 'selectedFeatureCount'):
            self.result = {"type": "response", "error": "Active layer is not a vector layer"}
            return
        
        if layer.selectedFeatureCount() == 0:
            self.result = {"type": "response", "error": "No features selected"}
            return

        path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4().hex}.fgb")        
        processing.run("native:savefeatures", {
            'INPUT': QgsProcessingFeatureSourceDefinition(layer.id(), selectedFeaturesOnly=True),
            'OUTPUT': path
        })
        
        self._temp_files.append(path)

        return {"type": "response", "path": path}

    @pyqtSlot(result='PyQt_PyObject')
    def get_layer_info(self, args):
        column = args.get("column")
        field = args.get("value")
        
        if column == "name":
            layer = QgsProject.instance().mapLayersByName(field)
            if not layer:
                return {"type": "response", "error": "Layer not found"}
            layer = layer[0]
        else:
            layer = QgsProject.instance().mapLayer(field)
            if layer is None:
                return {"type": "response", "error": "Layer not found"}
        
        info = {
            "type": "response",
            "name": layer.name(),
            "crs": layer.crs().authid(),
            "units": QgsUnitTypes.toString(layer.crs().mapUnits()),
            "extent": {
                "xmin": layer.extent().xMinimum(),
                "xmax": layer.extent().xMaximum(),
                "ymin": layer.extent().yMinimum(),
                "ymax": layer.extent().yMaximum(),
            }
        }

        type = layer.type()
        if type == QgsMapLayer.VectorLayer:
            info["layer_type"] = "vector"
            info["geometry"] = QgsWkbTypes.displayString(layer.wkbType())
            info["features"] = layer.featureCount()
            info["fields"] = [f.name() for f in layer.fields()]

        elif type == QgsMapLayer.RasterLayer:
            info["layer_type"] = "raster"
            info["bands"] = layer.bandCount()
            info["width"] = layer.width()
            info["height"] = layer.height()
            info["res_x"] = layer.rasterUnitsPerPixelX()
            info["res_y"] = layer.rasterUnitsPerPixelY()

        return info

    def update_state(self):
        self.needs_update = True

    @pyqtSlot(result='PyQt_PyObject')
    def check_update(self):
        if not self.needs_update:
            self.result = None
            return None
        self.needs_update = False
        self.dispatch({"method": "project_state", "args": None})
    
    def remove_temp_files(self):
        for path in self._temp_files:
            if os.path.exists(path):
                os.remove(path)
        self._temp_files = []