# LocI Small Cache Downloader
Downloads nominated LocI Datasets' registers and a max specified number of contained items from their Linked Data APIs via HTTP to build a small LocI test cache.

Takes about 45min to run if doing 100s.

Sores everything as local n-triples RDF files for ease of command line concatenation.

n-triples -> trig like this:

`-$ { printf "<http://linked.data.gov.au/dataset/asgs2011> {\n\n"; cat asgs2011_dataset.nt; printf "\n}"; } > asgs2011_dataset.trig`


## Author
Nicholas Car
<nicholas.car@csiro.au>
