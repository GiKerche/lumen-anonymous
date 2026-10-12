# Lumen-bench anonymous explorer

The static explorer contains all 194,400 recorded trials, their outcomes and evidence, 108 parallel scenarios, 607 cross-judge cases, 83 human calibration cases, and 3,300 benign controls. The Results view displays the released harmful-action, language, and benign-control analyses. Filters and record dialogs link these results to their source evidence. The explorer makes no model API calls.

## Interactive exploration

- **Playground:** choose a prompt language on the world map, then compare two recorded responses while changing language, model, social pressure, or system instruction. The other displayed settings and scenario stay matched. Open the exact requests, proposed calls, and original evidence. Map locations are navigation anchors for languages; the benchmark does not measure country-level outcomes.
- **Condition matrix:** click any of the five-language by six-pressure cells to inspect the recorded outcome for the selected model, scenario, and instruction. There is one response per cell.
- **Model × language atlas:** explore all 150 model-language cells. Filter scenarios and pressure, switch between harmful-action and say–do rates, and compare ethical and neutral instructions. Each selection exposes its numerator, denominator, and output errors. Counts are descriptive; no inferential test is recalculated.
- **Predict the action:** read a model's prose before revealing its proposed tool calls and stored outcome. Examples are selected for exploration and do not form a representative sample.

Every view can be shared through its URL fragment. Guided examples are selected from the released observations. Neither responses nor labels are generated in the browser.

## Build and preview

```bash
python scripts/build_anonymous_site.py
python -m http.server 8768 --bind 127.0.0.1 --directory docs
```

Use a current browser with `DecompressionStream` support. The generator packages the existing data and copies the site into `docs/`. The main JSON/gzip files are retained beside byte-preserving `.js` companions; the latter let the browser load data under anonymous hosting restrictions. This packaging changes no scientific results. `site/core.js`, `site/lab.js`, `site/world.js`, and `site/app.js` are the readable sources; `site/browser.js` is generated from them. The world geometry is included locally and requires no map service.

To regenerate the numerical explorer from the deposited records, first run `python scripts/build_explorer.py --dataset-revision SNAPSHOT_SHA`, using the 40-character snapshot identifier in `site/data/manifest.json`, then run the anonymous-site builder. The snapshot identifier and content hashes describe provenance; links stay within the anonymous repository.

```bash
python -m unittest test_explorer test_dataset_metadata
node site/test-core.mjs
node site/test-lab.mjs
```

## Anonymous publication

GitHub Pages uses **main** and **/docs**. Mirror the **main** branch in Anonymous GitHub and enable **GitHub Pages**, PDFs, and images. The repository view and its **Website** button then use the same anonymous snapshot. After a source update, refresh that snapshot with **Force update** in the owner's dashboard.

Paper links use the locally included anonymous PDF. Source-record and download links resolve to the same anonymous repository when viewed through its website. No repository owner or organization is hardcoded into the site. On hosts that block browser downloads, Export opens the data for copying. Author metadata, organization artwork, and the original Git history are omitted from this review copy; bibliographic references to published work remain intact.

All responses and generated tool effects are synthetic. Filters are descriptive and do not recalculate the paper's inferential analyses. Missing/error cases are not interpreted as safe behavior.
