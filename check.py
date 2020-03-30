import codecs
from lingpy import *
from lingpy import basictypes as bt
import networkx as nx
from tabulate import tabulate
from clldutils.misc import slug
from sys import argv
from collections import defaultdict
from lingpy.sequence.sound_classes import token2class

def strip_accent(sound):
    return sound.replace('ˈ', '')

# load the data
wl = Wordlist(argv[1])

# check for missing concepts
for idx, concept, language in wl.iter_rows('concept', 'doculect'):
    if not concept.strip():
        print('Missing concept {0} / {1}'.format(idx, language))
        wl[idx, 'concept'] = '?'
wl = Wordlist(wl)

# make network
G = nx.DiGraph()
wl = Wordlist(argv[1])
colors = [
        "#a6cee3",
        "#1f78b4",
        "#b2df8a",
        "#33a02c",
        "#fb9a99",
        "#e31a1c",
        "#fdbf6f",
        "#ff7f00",
        "#cab2d6",
        "#6a3d9a",
        "#ffff99",
        "#b15928",
        ]

cmap = {d: c for d, c in zip(wl.cols, colors)}

for idx in wl:
    G.add_node(
            idx,
            name=wl[idx, 'form'],
            doculect=wl[idx, 'doculect'],
            concept=wl[idx, 'concept'],
            cogid=wl[idx, 'cogid'],
            root=wl[idx, 'root'],
            color = cmap.get(wl[idx, 'doculect'], 'white')
            )
for idx, ancestor, relation, process in wl.iter_rows('ancestor', 'relation', 'process'):
    if ancestor.strip():
        G.add_edge(int(ancestor), idx, relation=relation, label=relation,
                process=process)

# check for contatenation
if "concatenation" in argv:
    table = []
    for nA, nB, data in G.edges(data=True):
        tkA, tkB = str(wl[nA, 'tokens']), str(wl[nB, 'tokens'])
        if 'no-accent' in argv:
            tkA = tkA.replace('ˈ', '')
            tkB = tkB.replace('ˈ', '')

        if data['relation'] == 'prefixation':
            prefix = data['process'].split(':')[1].strip()
            if 'no-accent' in argv:
                prefix = prefix.replace('ˈ', '')
            if prefix+' '+tkA != tkB:

                table += [[nA, nB, tkA, tkB,
                data['process'], edit_dist(
                    str(prefix+' '+tkA).split(), tkB.split(), normalized=True)]]
        elif data['relation'] == 'suffixation':
            suffix = data['process'].split(':')[1].strip()
            if 'no-accent' in argv:
                suffix = suffix.replace('ˈ', '')
            if tkA+' '+suffix != tkB:
                table += [[nA, nB, tkA, tkB,
                data['process'], edit_dist(
                    str(tkA+' '+suffix).split(), tkB.split(), normalized=True)]]
    if table:
        print('[i] found {0} cases where automated concatenation does not work'.format(
            len(table)))
        print(tabulate(
            table,
            headers=['IdA', 'IdB', 'TokensA', 'TokensB', 'Process', 'Distance'],
            tablefmt='pipe',
            floatfmt='.2f'))
    else:
        print('[i] no cases found where automated concatenation does not work')

if "alignments" in argv:
    table = []
    alms = Alignments(wl, ref='cogid', transcription='form')
    for cogid, msa in alms.msa['cogid'].items():
        lengths = [len(alm) for alm in msa['alignment']]
        if len(set(lengths)) != 1:
            table += [[cogid, ', '.join(msa['taxa'])]]
    if table:
        print('[i] found {0} alignments where the strings are of unequal length'.format(
            len(table)))
    else:
        print('[i] no problematic alignments found')
    
    all_changes = defaultdict(lambda : defaultdict(list))
    # retrieve ancestor descendant relations from graph
    ancestry = defaultdict(list)
    for nA, nB, data in G.edges(data=True):
        if data['relation'] == 'inheritance':
            ancestry[wl[nB, 'doculect']] += [wl[nA, 'doculect']]
    for a, b in ancestry.items():
        if len(set(b)) > 1:
            print('[i] {0} has {1} ancestors: {2}'.format(
                a, len(set(b)), 
                ', '.join(['{0} ({1})'.format(x, b.count(x)) for x in set(b)])
                ))
        ancestry[a] = sorted(b, key=lambda x: b.count(x), reverse=True)[0]
    for cogid, msa in alms.msa['cogid'].items():
        for i, idx in enumerate(msa['ID']):
            doculect = msa['taxa'][i]
            if ancestry[doculect] in msa['taxa']:
                for sA, sB in zip(
                        msa['alignment'][msa['taxa'].index(ancestry[doculect])],
                        msa['alignment'][i]
                        ):
                    all_changes[strip_accent(sA)][strip_accent(sB)] += [
                            (ancestry[doculect], doculect)]
    table = []
    for sA, dictB in sorted(all_changes.items(), key=lambda x: len(x[1]),
            reverse=True):
        for sB, items in dictB.items():
            table += [[
                sA, 
                sB,
                len(items),
                len(set(items)),
                ', '.join([
                    '{0} > {1} ({2})'.format(a, b, items.count(
                        (a,b))) for a, b in set(items)])]]
    table = sorted(
            table,
            key=lambda x: (
                x[2],
                x[3],
                token2class(x[0], 'cv'),
                token2class(x[1], 'cv'),
                token2class(x[0], 'dolgo'),
                token2class(x[1], 'dolgo'),
                token2class(x[0], 'sca'),
                token2class(x[1], 'sca')),
            reverse=True)
    print('[i] found {0} distinct changes in the data'.format(len(table)))
    with codecs.open("sound-change-frequencies.tsv", 'w', 'utf-8') as f:
        f.write('\t'.join(['Source', 'Target', 'Frequency', 'RelFreq',
            'Pairs'])+'\n')
        for line in table:
            f.write('\t'.join([
                str(x) for x in line])+'\n')
    print('[i] most frequent 10 changes')
    print(tabulate([line[:-1] for line in table][:10],
        tablefmt='pipe',
        headers=['Source', 'Target', 'Frequency', 'Relative Frequency']))
    print('[i] most rare 10 changes')
    print(tabulate([line[:-1] for line in table[::-1]][:10],
        tablefmt='pipe',
        headers=['Source', 'Target', 'Frequency', 'Relative Frequency']))


if "network" in argv:
    nx.write_graphml_lxml(G, argv[1][:-4]+'.graphml')


#if 'suffixes' in argv:
#    data = defaultdict(list)
#    for idx, doculect, tokens, relation, process in wl.iter_rows(
#            'doculect', 'tokens', 'relation', 'process'):
#        if doculect == "Indo-European" and relation == 'derivation':
#            if ',' in process:
#                grade, suffix = process.split(', ')
#                if suffix in ['suffix', 'prefix']:
#                    affix_type, affix_form = suffix.split(': ')
#                else:
#                    grade = ''
#            else:
#                grade, affix_type, affix_form = process, '', ''
#            if grade:
#                data[grade, affix_type, affix_form] += [idx]
#    print(data)
