# rqgis

The `rqgis` package provides the R API for the **R Console** QGIS
plugin. It allows you to interact with the active QGIS project, read
project properties, list layers, transfer spatial data between R and
QGIS, and use interactive map tools directly from the R console.

> **Note:** This package is designed to be run exclusively inside the
> QGIS R Console plugin. It relies on a custom communication protocol
> established by the plugin and will not work in a standalone RStudio
> session.

## Usage

### Connect to the QGIS Project

Connect to the active QGIS project using
[`qgis_project()`](https://jsmendozap.github.io/rqgis/reference/qgis_project.md).
This returns an `R6` object that serves as your main interface.

``` r

qgis <- qgis_project()

# Project metadata
qgis$title    # project title
qgis$path     # project file path
qgis$crs      # CRS identifier (e.g. "EPSG:4326")
qgis$units    # map units (e.g. "meters")
```

#### Interacting with Layers

**List all layers in the project:**

``` r

# List all layers
layers_df <- qgis$list_layers()
print(layers_df)

# List only vector layers
vector_layers <- qgis$list_layers(type = 0)
print(vector_layers)
```

**Process data in R and insert it back into QGIS:**

Perform any analysis in R and push the results back to QGIS as a new
layer.

``` r

library(sf)
library(rnaturalearth)
library(dplyr)

world <- ne_countries() %>% select(name, continent)

# Insert the new layer into QGIS
qgis$insert_layer(world, name = "world")
```

**Get a layer from QGIS into R:**

You can load a layer by its name or its ID. Vector layers are loaded as
`sf` objects and rasters as `SpatRaster` objects.

``` r

# Load the vector layer back into R
world_new <- qgis$get_layer("world")

# Load a raster layer
dem <- qgis$get_layer("dem_raster")
```

#### Layer information

``` r

qgis$layer_info("world")
# Layer: world> 
# @ Type: vector 
# @ CRS:  EPSG:4326 
# @ Extent: 
#     xmin = -180 
#     xmax = 180 
#     ymin = -90 
#     ymax = 83.64513 
# @ Geometry: MultiPolygon 
# @ Features: 177 
# @ Fields:
#     name
#     continent
```

#### Canvas extent

``` r

# returns the current map canvas extent as an bbox object
qgis$get_canvas_extent()
```

#### Selected features

``` r

# returns selected features from the active layer as an sf object
qgis$get_selected_features()
```

#### Interactive Map Tools

Prompt the user to draw geometries on the QGIS map canvas and receive
the coordinates instantly in R:

``` r

# Draw a rectangle and get its bounding box (sf bbox)
my_bbox <- qgis_draw_rectangle()

# Draw a specific number of points (sf sfc)
my_points <- qgis_draw_points(n = 3)
```

For full details on all available methods, explore the **Reference**
section.
