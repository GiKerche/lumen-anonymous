# Lumen-bench review artwork

The small L icon is an SVG included in this repository. The interface uses system fonts and loads no external artwork, analytics, or scripts.

World map: Natural Earth, public domain. Geography is a language-selection aid, not country-level benchmark data.

Source: https://github.com/nvkelso/natural-earth-vector/blob/master/geojson/ne_110m_admin_0_countries.geojson

License: https://www.naturalearthdata.com/about/terms-of-use/

Source SHA-256: `6866c877d39cba9c357620878839b336d569f8c662d3cfab4cb1dbe2d39c977f`. The static geometry is packaged in `site/world.js`; no map service is contacted at runtime.
