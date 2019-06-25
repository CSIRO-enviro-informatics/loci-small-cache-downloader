import requests
import rdflib
from rdflib import RDF, URIRef

# all the registers from all the datasets we want to download from
DS_REG_CLS = [
    ('asgs2011', 'http://linked.data.gov.au/dataset/asgs2011/australia/', 'http://linked.data.gov.au/def/asgs#Australia'),
    ('asgs2011', 'http://linked.data.gov.au/dataset/asgs2011/meshblock/', 'http://linked.data.gov.au/def/asgs#MeshBlock'),
    ('asgs2011', 'http://linked.data.gov.au/dataset/asgs2011/stateorterritory/', 'http://linked.data.gov.au/def/asgs#StateOrTerritory'),
    ('asgs2011', 'http://linked.data.gov.au/dataset/asgs2011/statisticalarealevel1/', 'http://linked.data.gov.au/def/asgs#StatisticalAreaLevel1'),
    ('asgs2011', 'http://linked.data.gov.au/dataset/asgs2011/statisticalarealevel2/', 'http://linked.data.gov.au/def/asgs#StatisticalAreaLevel2'),
    ('asgs2011', 'http://linked.data.gov.au/dataset/asgs2011/statisticalarealevel3/', 'http://linked.data.gov.au/def/asgs#StatisticalAreaLevel3'),
    ('asgs2011', 'http://linked.data.gov.au/dataset/asgs2011/statisticalarealevel4/', 'http://linked.data.gov.au/def/asgs#StatisticalAreaLevel4'),

    ('asgs2016', 'http://linked.data.gov.au/dataset/asgs2016/australia/', 'http://linked.data.gov.au/def/asgs#Australia'),
    ('asgs2016', 'http://linked.data.gov.au/dataset/asgs2016/meshblock/', 'http://linked.data.gov.au/def/asgs#MeshBlock'),
    ('asgs2016', 'http://linked.data.gov.au/dataset/asgs2016/stateorterritory/', 'http://linked.data.gov.au/def/asgs#StateOrTerritory'),
    ('asgs2016', 'http://linked.data.gov.au/dataset/asgs2016/statisticalarealevel1/', 'http://linked.data.gov.au/def/asgs#StatisticalAreaLevel1'),
    ('asgs2016', 'http://linked.data.gov.au/dataset/asgs2016/statisticalarealevel2/', 'http://linked.data.gov.au/def/asgs#StatisticalAreaLevel2'),
    ('asgs2016', 'http://linked.data.gov.au/dataset/asgs2016/statisticalarealevel3/', 'http://linked.data.gov.au/def/asgs#StatisticalAreaLevel3'),
    ('asgs2016', 'http://linked.data.gov.au/dataset/asgs2016/statisticalarealevel4/', 'http://linked.data.gov.au/def/asgs#StatisticalAreaLevel4'),

    ('geofabric', 'http://linked.data.gov.au/dataset/geofabric/contractedcatchment/', 'http://linked.data.gov.au/def/geofabric#ContractedCatchment'),
    ('geofabric', 'http://linked.data.gov.au/dataset/geofabric/riverregion/', 'http://linked.data.gov.au/def/geofabric#RiverRegion'),
    ('geofabric', 'http://linked.data.gov.au/dataset/geofabric/drainagedivision/', 'http://linked.data.gov.au/def/geofabric#DrainageDivision'),

    ('gnaf-2016-05', 'http://linked.data.gov.au/dataset/gnaf-2016-05/address/', 'http://linked.data.gov.au/def/gnaf#Address'),
    ('gnaf-2016-05', 'http://linked.data.gov.au/dataset/gnaf-2016-05/addressSite/', 'http://linked.data.gov.au/def/gnaf#AddressSite'),
    ('gnaf-2016-05', 'http://linked.data.gov.au/dataset/gnaf-2016-05/streetLocality/', 'http://linked.data.gov.au/def/gnaf#StreetLocality'),
    ('gnaf-2016-05', 'http://linked.data.gov.au/dataset/gnaf-2016-05/locality/', 'http://linked.data.gov.au/def/gnaf#Locality'),

    ('gnaf', 'http://linked.data.gov.au/dataset/gnaf/address/', 'http://linked.data.gov.au/def/gnaf#Address'),
    ('gnaf', 'http://linked.data.gov.au/dataset/gnaf/addressSite/', 'http://linked.data.gov.au/def/gnaf#AddressSite'),
    ('gnaf', 'http://linked.data.gov.au/dataset/gnaf/streetLocality/', 'http://linked.data.gov.au/def/gnaf#StreetLocality'),
    ('gnaf', 'http://linked.data.gov.au/dataset/gnaf/locality/', 'http://linked.data.gov.au/def/gnaf#Locality'),
]


def get_registers():
    last_dataset = None

    # for each register, get a single page of 1000 items
    for (dataset, reg, cls) in DS_REG_CLS:
        if dataset != last_dataset:
            print('getting {}'.format(reg))
            if last_dataset is not None:
                with open(last_dataset + '.nt', 'w') as f:
                    f.write(g.serialize(format='nt').decode('utf-8'))
            g = rdflib.Graph()
        last_dataset = dataset

        r = requests.get(reg + '?per_page=100&_format=text/turtle')
        if r.status_code == 200:
            g.parse(data=r.text, format='turtle')
        else:
            print('reg {} failed'.format(reg))
            print(r.status_code)
            print(r.text)
        print('done {}'.format(reg))

    # last one
    with open(last_dataset + '.nt', 'w') as f:
        f.write(g.serialize(format='nt').decode('utf-8'))


def get_instances():
    for (dataset, reg, cls) in DS_REG_CLS:
        reg_name = reg.split('/')[-2]
        cls_name = cls.split('#')[1]
        print('dataset: {}'.format(dataset))
        print('register: {}'.format(reg_name))
        i = 0
        g = rdflib.Graph().parse(dataset + '.nt', format='nt')
        g2 = rdflib.Graph()
        print('instance:')
        for s in g.subjects(predicate=RDF.type, object=URIRef(cls)):
            r = requests.get(s + '?_format=text/turtle')
            g2.parse(data=r.text, format='turtle')
            i += 1
            print('  ' + str(i))
        print(str(len(g2)) + ' triples in total')

        with open('{}_{}s.nt'.format(dataset, cls_name), 'w') as f:
            f.write(g2.serialize(format='nt').decode('utf-8'))


if __name__ == '__main__':
    get_registers()
    print()
    print('now instances')
    print()
    get_instances()
