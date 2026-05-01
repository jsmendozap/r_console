# Draw Points on the QGIS Map Canvas

Interactively prompts the user to draw a specified number of points on
the QGIS map canvas and returns them as an `sfc` object.

## Usage

``` r
qgis_draw_points(n = 1)
```

## Arguments

- n:

  (integer) The number of points to draw. Defaults to 1.

## Value

An `sfc` object (geometry column) from the `sf` package containing the
drawn points.

## Examples

``` r
if (FALSE) { # \dontrun{
# Draw a single point
pt <- qgis_draw_points()

# Draw 3 points
pts <- qgis_draw_points(n = 3)
print(pts)
} # }
```
