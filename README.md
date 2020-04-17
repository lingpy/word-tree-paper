# Code and data accompanying the study "Modeling word trees in historical linguistics"

When using the code or data in this repository, please cite the following (forthcoming) paper:

> Schweikhard, N. and J. List (forthcoming): Modeling word trees in historical linguistics. Preliminary ideas for the reconciliation of word trees and language trees. In: Sprach(en)forschung: Disziplinen und Interdisziplinarität. Akten der 27. Fachtagung der Gesellschaft für Sprache und Sprachen. Draft: https://doi.org/10.17613/8h49-rp11

```
@InProceedings{Schweikhard2020,
  author     = {Nathanael E. Schweikhard and Johann-Mattis List},
  booktitle  = {Sprach(en)forschung: Disziplinen und Interdisziplinarität. Akten der 27. Fachtagung der Gesellschaft für Sprache und Sprachen},
  title      = {Modeling word trees in historical linguistics. Preliminary ideas for the reconciliation of word trees and language trees},
  editor     = {Brogyanyi, Bela and Lipp, Reiner},
  eventdate  = {2019-05-30/2019-06-01},
  eventtitle = {27. Fachtagung der Gesellschaft für Sprache und Sprachen},
  publisher  = {Dr. Kovač},
  venue      = {Warschau},
  url        = {https://doi.org/10.17613/8h49-rp11},
  address    = {Hamburg},
  year       = {forthcoming},
}
```

To inspect the results of this annotation study directl, you can just visit the interactive web application at [https://lingpy.github.io/word-tree-paper/index.html](https://lingpy.github.io/word-tree-paper/index.html).


## Installation

Assuming you have Python and `pip` installed on your system, just type:

```
pip install -r requirements.txt
```

## Checking for concatenative derivation

Simply run:

```
$ python check.py NIL.tsv concatenation
```

And the code will output all those cases where the automated concatenation did not yield the expected results.

If accents are not consistently provided for the data, this test will also output the cases in which the results differs from the expected ones due to a missing accent. If you want to check the concatenative derivation for accuracy while disregarding the accent, run:

```
$ python check.py NIL.tsv concatenation no-accent
```

## Deriving sound change statistics

In order to check the alignments and calculate statistics on the sound changes in the dataset, run:

```
$ python check.py NIL.tsv alignments
```

This will output the following information:
* whether any mistakes where found with the alignments, i.e. whether any aligned strings contain different amounts of tokens
* whether any doculect seems to have more than one ancestor (this can occur if only some forms of its direct ancestor are reconstructed so that the doculect inherits forms both its direct ancestor and the general ancestor)
* statistics on how many distinct sound changes were found
* the 10 most frequent and the 10 least frequent sound changes in the dataset

## Instructions on using Cytoscape

In order to visualize the data we provide here in Cytoscape, please follow these steps:

* Install Cytoscape: https://cytoscape.org/.
* Open NIL.tsv in a spreadsheet editor and copy the columns ID, ANCESTOR and RELATION into a new file.
* Sort this new file by the column ANCESTOR and remove all rows where ANCESTOR is empty. (The supplementary material includes this file as Relations.tsv).
* Start Cytoscape and import this new file as a network (File -> Import -> Network from File...).
* Set ID as the Target Node, ANCESTOR as the Source Node, and PROCESS as the Interaction Type.
* Import NIL.tsv as a table (File -> Import -> Table from File...), keeping ID as the Key column.
* Use the Controle Panel to adjust the visualizations. For the tree-like visualization we use in the paper, you need to install the plugin yFiles Layout Algorithms in Cytoscape (Apps -> App Manager...) and then choose yFiles Tree Layout from the Layout menu.

The supplementary material also includes the Cytoscape-file we created this way as NIL.cys.
You can import new data into this file in order to visualize them with the same settings (you will need to choose the layout from the Layout menu again).

You can export the data, which makes it possible to view them in any browser (File -> Export -> Network to Web Page). The supplementary material includes this as index.html in the folder application.
