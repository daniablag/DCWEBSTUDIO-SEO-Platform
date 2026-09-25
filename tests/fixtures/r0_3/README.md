# R0.3 synthetic acceptance fixtures

Every hostname uses the reserved `.test` suffix, every identifier is invented,
and no row contains production content, credentials, personal identifiers or a
live provider response.

- `url-list.txt` and the two CSV files are the accepted manual input shapes.
- `offline-serp-response.json` simulates a provider response without network
  access.
- `expected-*.json` files are normalized contract outputs.
- `manifest.json` pins SHA-256 checksums for every data fixture except itself.

Russian and Ukrainian keyword inputs are deliberately separate. They express
related business intent but are not translations generated from one another.
