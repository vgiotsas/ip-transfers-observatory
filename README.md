# ip-transfers-observatory

Observatory to monitor abuse and misuse of the IPv4 transfer market

# Datasets

## Cummulative port capacities

The cummulative IXP port capacities in [`cummulative-ixp-capacity/`](https://github.com/vgiotsas/ip-transfers-observatory/tree/master/cummulative-ixp-capacity) are used to infer hypergiant ASes that due to the size of their network may have a disproportionate number of IPs blacklisted.
Each line of the files with total IXP port capacities has the format `<asn> <total_port_capacity>`.

Inference of hypergiants based on IXP data is inspired by the following paper:

> Böttger, Timm, Felix Cuadrado, and Steve Uhlig. "Looking for hypergiants in peeringDB." ACM SIGCOMM Computer Communication Review 48, no. 3 (2018): 13-19.

## ASN Population

ASN population is another attribute used in filtering ASes that may have a disproportionate number of blacklisted IPs due to their very large user base.
The number of users per ASN is in the file [autsys_population.txt](https://github.com/vgiotsas/ip-transfers-observatory/blob/master/autsys_population.txt). To compile the ASN population we use data from APNIC's aspop project which is documented below:

> Geoff Huston. "How Big is that Network?" APNIC blog, October 2014. https://labs.apnic.net/?p=526

The format of each line of the [autsys_population.txt](https://github.com/vgiotsas/ip-transfers-observatory/blob/master/autsys_population.txt) file is as follows:

```
<ASN> <Number of Users> <ASN Country> <Percentage of Users in ASN country>
```

Each space separator is a TAB.

## Resolved Organization names to ASNs

RIRs report transfers between organizations and not ASNs. To analyze the routing behaviour of transferred IP prefixes it's useful to map the organization names to the corresponding ASNs. The file [`resolved_orgnames2asn.txt`](https://github.com/vgiotsas/ip-transfers-observatory/blob/master/resolved_orgnames2asn.txt) includes the mapping of between organization names and ASNs, for these organizations that we successfully mapped to an ASN. In many cases an organization is mapped to multiple ASNs if the organization owns multiple ASNs. 

Each line of the file has the following format: `<org_name>TAB<asn1,asn2,...>`

## Sibling ASNs

The directory `sinblings` includes pairs of ASNs that are considered to be siblings, namely they belong to the same organization.
Sibling inference is useful when analyzing IP transfers in order to understand the type of the transfer, namely if it's a transfer/acquisition or if it's a transaction between two unrelated organizations. The name of each file denotes the date of the sibling inference, for instance the file `siblings-20161001.txt` lists the siblings collected in 2016-10-01.  Each line of siblings file has the format `ASN1 ASN2` where the two ASNs are siblings. 

## Prefix-ASN origin shifts

The [`prefix_transfer_routing_shift.txt.gz`](https://github.com/vgiotsas/ip-transfers-observatory/blob/master/prefix_transfer_routing_shift.txt.gz) file includes the dates where the origin ASN of a prefix according to the RouteViews BGP data. Each line of the file includes the data for each prefix:

```
<IP_prefix> <ASN1,Date 1> <ASN2,Date 2>, ...
```

The date is in format YYYY-MM-DD. Multi-origin prefixes would have the origin ASNs separated by an underscore `_`.

For example consider the following sample:

```
1.0.0.0/24      15169,20120510  47872,20160209  13335,20180320
1.0.11.0/24     18046,20141012  18046_133741,20141021   133741_18046,20141031
1.0.12.0/24     18046,20141017  18046_133741,20141021   133741_18046,20141031
1.0.128.0/17    9737,20120101   23969,20180330
1.0.128.0/18    9737,20120101   23969_9737,20180504     23969,20180506
1.0.128.0/19    9737,20120101   23969_9737,20180504     23969,20180506
1.0.13.0/24     18046,20141007  18046_133741,20141021   133741_18046,20141031
1.0.160.0/19    9737,20120101   23969_9737,20180504     23969,20180506
1.0.192.0/18    9737,20120101   23969_9737,20180504     23969,20180506
```

Prefix `1.0.0.0/24` has been advertised by `AS15169` since 2012-05-10, then by `AS47872` since 2016-02-09, and finally the origin ASN became `AS13335` since 2018-03-20
