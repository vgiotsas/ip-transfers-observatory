# ip-transfers-observatory

Observatory to monitor abuse and misuse of the IPv4 transfer market

# Datasets

## Cummulative port capacities

The cummulative IXP port capacities in [`cummulative-ixp-capacity/`](https://github.com/vgiotsas/ip-transfers-observatory/tree/master/cummulative-ixp-capacity) are used to infer hypergiant ASes that due to the size of their network may have a disproportionate number of IPs blacklisted.
Each line of the files with total IXP port capacities has the format `<asn> <total_port_capacity>`.

Inference of hypergiants based on IXP data is inspired by the following paper:

> Böttger, Timm, Felix Cuadrado, and Steve Uhlig. "Looking for hypergiants in peeringDB." ACM SIGCOMM Computer Communication Review 48, no. 3 (2018): 13-19.

## Resolved Organization names to ASNs

RIRs report transfers between organizations and not ASNs. To analyze the routing behaviour of transferred IP prefixes it's useful to map the organization names to the corresponding ASNs. The file [`resolved_orgnames2asn.txt`](https://github.com/vgiotsas/ip-transfers-observatory/blob/master/resolved_orgnames2asn.txt) includes the mapping of between organization names and ASNs, for these organizations that we successfully mapped to an ASN. In many cases an organization is mapped to multiple ASNs if the organization owns multiple ASNs. 

Each line of the file has the following format: `<org_name>TAB<asn1,asn2,...>`
