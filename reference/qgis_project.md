# Connect to the Active QGIS Project

Establishes a connection to the currently active QGIS project. This
function is the main entry point for the `rqgis` package, returning an
R6 object that allows you to interact with QGIS layers, extent, and
project metadata directly from the R console.

## Usage

``` r
qgis_project(data = NULL)
```

## Arguments

- data:

  Optional list containing updates about the project state. Intended for
  internal plugin use only.

## Value

An R6 object of class
[`QgisProject`](https://jsmendozap.github.io/rqgis/reference/QgisProject.md)
containing the project's metadata and methods for bidirectional data
transfer.

## Examples

``` r
if (FALSE) { # \dontrun{
# Connect to the active QGIS project
qgis <- qgis_project()

# Inspect project properties
qgis$title
qgis$crs

# List available layers and retrieve one as an sf object
qgis$list_layers()
my_layer <- qgis$get_layer("world_borders")
} # }
```
