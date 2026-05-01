# Draw a Rectangle on the QGIS Map Canvas

Interactively prompts the user to draw a rectangle on the QGIS map
canvas and returns its bounding box.

## Usage

``` r
qgis_draw_bbox()
```

## Value

A `bbox` object from the `sf` package representing the drawn extent.

## Examples

``` r
if (FALSE) { # \dontrun{
# Draw a bounding box and save the extent to a variable
my_bbox <- qgis_draw_bbox()
print(my_bbox)
} # }
```
