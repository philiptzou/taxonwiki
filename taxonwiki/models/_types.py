# -*- coding: utf-8 -*-
from __future__ import unicode_literals

ORGANISM_TYPE = [
    (None, 'Select one...'),
    ('invalid', '(Invalid)'),
    ('animal', 'Animal'),
    ('bacterial', 'Bacterial'),
    ('fungi', 'Fungi'),
    ('plant', 'Plant'),
    ('protist', 'Protist'),
    ('virus', 'Virus')
]

TAXON_STATUS_TYPE = [
    ('valid', 'Valid'),
    ('invalid', 'Invalid')
]

# TODO: use [All ranks](https://en.wikipedia.org/wiki/Taxonomic_rank#All_ranks)
# instead of main ranks.
RANK_TYPE = [
    (None, 'Select one...'),
    ('domain', 'Domain'),
    ('kingdom', 'Kingdom'),
    ('phylum', 'Phylum'),
    ('class', 'Class'),
    ('order', 'Order'),
    ('family', 'Family'),
    ('genus', 'Genus'),
    ('species', 'Species')
]

LANGUAGE_TYPE = [
    ('en', 'English'),
    ('zh-cn', '简体中文 (中国大陆)'),
    ('zh-tw', '正體中文 (台灣)'),
    ('zh-hk', '繁體中文 (香港)')
]
