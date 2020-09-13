# ip-transfers-observatory

Observatory to monitor abuse and misuse of the IPv4 transfer market

# Datasets

## Cummulative port capacities

The cummulative IXP port capacities in [`cummulative-ixp-capacity/`](https://github.com/vgiotsas/ip-transfers-observatory/tree/master/cummulative-ixp-capacity) are used to infer hypergiant ASes that due to the size of their network may have a disproportionate number of IPs blacklisted.
Each line of the files with total IXP port capacities has the format `<asn> <total_port_capacity>`.

Inference of hypergiants based on IXP data is inspired by the following paper:

> Böttger, Timm, Felix Cuadrado, and Steve Uhlig. "Looking for hypergiants in peeringDB." ACM SIGCOMM Computer Communication Review 48, no. 3 (2018): 13-19.
