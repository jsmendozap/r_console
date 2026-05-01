# Interface to the QGIS Project

The `QgisProject` class provides an R6 interface to interact with the
currently active QGIS project. It allows reading project properties,
listing layers, and transferring spatial data between R and QGIS.

## Details

Please note that you should not instantiate this class manually using
`QgisProject$new()`. Instead, use the public wrapper function
[`qgis_project()`](https://jsmendozap.github.io/rqgis/reference/qgis_project.md)
to safely establish the connection.

## Active bindings

- `title`:

  (character) The title of the QGIS project (read-only).

- `path`:

  (character) The absolute path to the QGIS project file (read-only).

- `crs`:

  (character) The authority ID of the project's CRS (e.g., "EPSG:4326")
  (read-only).

- `units`:

  (character) The map units of the project (e.g., "meters") (read-only).

## Methods

### Public methods

- [`QgisProject$new()`](#method-QgisProject-new)

- [`QgisProject$list_layers()`](#method-QgisProject-list_layers)

- [`QgisProject$get_layer()`](#method-QgisProject-get_layer)

- [`QgisProject$insert_layer()`](#method-QgisProject-insert_layer)

- [`QgisProject$layer_info()`](#method-QgisProject-layer_info)

- [`QgisProject$get_canvas_extent()`](#method-QgisProject-get_canvas_extent)

- [`QgisProject$get_selected_features()`](#method-QgisProject-get_selected_features)

- [`QgisProject$print()`](#method-QgisProject-print)

- [`QgisProject$clone()`](#method-QgisProject-clone)

------------------------------------------------------------------------

### Method [`new()`](https://rdrr.io/r/methods/new.html)

Create a new `QgisProject` object. This is typically instantiated via
qgis_project().

#### Usage

    QgisProject$new(data = NULL)

#### Arguments

- `data`:

  A list containing the initial project state. If `NULL`, it will be
  requested from QGIS. For internal use.

#### Returns

A new `QgisProject` object.

------------------------------------------------------------------------

### Method `list_layers()`

Lists layers available in the current QGIS project.

#### Usage

    QgisProject$list_layers(type = NULL)

#### Arguments

- `type`:

  (integer) An optional filter for layer type. Corresponds to
  `QgsMapLayerType`: `0` for vector, `1` for raster. Use `NULL` to list
  all layers.

#### Returns

A data frame with the `name` and `id` of the layers.

------------------------------------------------------------------------

### Method `get_layer()`

Reads a QGIS layer and loads it into R as a spatial object.

#### Usage

    QgisProject$get_layer(x, ...)

#### Arguments

- `x`:

  (character) The name or ID of the layer to get.

- `...`:

  Additional arguments passed to
  [`sf::st_read()`](https://r-spatial.github.io/sf/reference/st_read.html)
  for vector layers.

#### Returns

An `sf` object for vector layers or a `SpatRaster` object from the
`terra` package for raster layers.

------------------------------------------------------------------------

### Method `insert_layer()`

Inserts an R spatial object into the QGIS project as a new layer.

#### Usage

    QgisProject$insert_layer(layer, name = NULL, ...)

#### Arguments

- `layer`:

  The spatial object to insert. Must be an `sf` object or a `SpatRaster`
  from the `terra` package.

- `name`:

  (character) The desired name for the new layer in QGIS. If `NULL`, a
  name will be generated from the object's variable name.

- `...`:

  Additional arguments passed to
  [`sf::st_write()`](https://r-spatial.github.io/sf/reference/st_write.html)
  for vector layers.

#### Returns

The `QgisProject` object, invisibly.

------------------------------------------------------------------------

### Method `layer_info()`

Prints detailed information about a specific layer.

#### Usage

    QgisProject$layer_info(x)

#### Arguments

- `x`:

  (character) The name or ID of the layer.

#### Returns

The `QgisProject` object, invisibly.

------------------------------------------------------------------------

### Method `get_canvas_extent()`

Gets the extent of the current map canvas.

#### Usage

    QgisProject$get_canvas_extent()

#### Returns

A `bbox` object from the `sf` package representing the current view
extent.

------------------------------------------------------------------------

### Method `get_selected_features()`

Gets the selected features from the currently active vector layer in
QGIS.

#### Usage

    QgisProject$get_selected_features()

#### Returns

An `sf` object containing the selected features. Returns an error if the
active layer is not a vector layer or has no selection.

------------------------------------------------------------------------

### Method [`print()`](https://rdrr.io/r/base/print.html)

Prints a summary of the QGIS project information.

#### Usage

    QgisProject$print(...)

#### Arguments

- `...`:

  Ignored.

------------------------------------------------------------------------

### Method `clone()`

The objects of this class are cloneable with this method.

#### Usage

    QgisProject$clone(deep = FALSE)

#### Arguments

- `deep`:

  Whether to make a deep clone.
