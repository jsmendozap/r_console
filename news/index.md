# Changelog

## rqgis 0.4.0

- Support for QGIS 4.
  - Introduce the `rqgis` package to wrap the public API for QGIS
    interaction from R.
  - Added `qgis_draw_bbox` and `qgis_draw_points` functions
  - Automatic configuration of qgis_process path during `qgisprocess`
    package load
  - Dedicated API documentation website published via pkgdown
  - Implement a log viewer in the settings panel
  - Added option in settings to display the plugin title in the main
    panel
  - Bug fixes
