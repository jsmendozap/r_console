# R Console

An R console integrated into QGIS as a dock widget. Write and execute R code directly inside QGIS while having full access to the active project's layers, CRS, extent, and other properties from R.

## Features

- Interactive R console with command history
- Script editor with syntax highlighting, autocompletion, and calltips
- Bidirectional interoperability between R and QGIS:
  - Read project metadata (title, path, CRS, map units)
  - Load vector and raster layers from QGIS into R as `sf` or `SpatRaster` objects
  - Insert R spatial objects back into the QGIS project
  - Access the current map canvas extent
  - Load selected features from the active layer
- Automatic project state synchronization when layers or project properties change
- Dynamic autocompletion: function signatures are loaded automatically when new packages are attached

## Requirements

- QGIS 3.30 or later
- R 4.1.0 or later 
- R packages: `R6`, `jsonlite`, `evaluate`, `sf`, `terra`

Install the required R packages before using the plugin:

```r
install.packages(c("R6", "jsonlite", "evaluate", "sf", "terra"))
```

## Installation

Install from the QGIS Plugin Repository: **Plugins → Manage and Install Plugins → Search "R Console"**.

Or install manually by downloading the repository and copying it to your QGIS plugins directory:

- Linux/macOS: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
- Windows: `%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\`

## Usage

The dock widget contains two panels: an interactive console and a script editor.

### Console

Type R expressions and press **Enter** to execute. Use the **Up/Down** arrow keys to navigate command history. 

### Editor

Write R scripts in the editor. Execute the current expression with **Ctrl+Enter**, or run the entire script with the **Run** button. 

### QGIS project access

Connect to the active QGIS project using `qgis_project()`. This creates a `R6` object in your R environment. You can assign it any name:

```r
qgis <- qgis_project()
```

The object is automatically updated when project properties or layers change.

### QgisProject methods

#### Project metadata

```r
qgis$title    # project title
qgis$path     # project file path
qgis$crs      # CRS identifier (e.g. "EPSG:4326")
qgis$units    # map units (e.g. "degrees")
```

#### Interacting with Layers

**List all layers in the project:**

```r
# List all layers
layers_df <- qgis$list_layers()
print(layers_df)

# List only vector layers
vector_layers <- qgis$list_layers(type = 0)
print(vector_layers)
```

**Process data in R and insert it back into QGIS:**

Perform any analysis in R and push the results back to QGIS as a new layer.

```r
library(sf)
library(rnaturalearth)

world <- ne_countries()

# Insert the new layer into QGIS
qgis$insert_layer(world, name = "world")
```

**Get a layer from QGIS into R:**

You can load a layer by its name or its ID. Vector layers are loaded as `sf` objects and rasters as `SpatRaster` objects.

```r
# Load the vector layer back into R
world_new <- qgis$get_layer("world")

# Load a raster layer
dem <- qgis$get_layer("dem_raster")
```

#### Layer information

```r
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
#     featurecla
#     scalerank
#     labelrank
#     sovereignt
#     sov_a3
#     adm0_dif
#     level
#     ...
```

#### Canvas extent

```r
# returns the current map canvas extent as an bbox object
qgis$get_canvas_extent()
```

#### Selected features

```r
# returns selected features from the active layer as an sf object
qgis$get_selected_features()
```

## License

GNU General Public License v2 or later. See [LICENSE](LICENSE) for details.