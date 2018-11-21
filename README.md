# arxiv-search
Scripts associated with the Arxiv search Jupyter Notebook

## Getting Started

This search tool is provided as a hosted Jupyter notebook.

The URL for the notebook and the password to access it will have been emailed to you.

Please click on the link in the email and enter the provided password.

Once you are viewing the notebook `Arxiv Search`, please follow the instructions
in the notebook to run a search or generate a chart.

## Sharing and Extended Use

The notebook is designed as a workspace for one researcher at a time. Making this a
more generally available tool will require additional engineering time.*

When starting a new piece of research it is best to make a copy of the top level search
notebook and have only one notebook running at a time. You can then save the notebook
as you go to preserve the research process without losing the orignal tested version.

* The notebook loads the search index directly which takes a ton of RAM. Running
multiple notebooks in this manner would use up all the RAM on the virtual machine.
Normally a search service is created and API requests are made to that service but
this level of complexity was postponned until the tool is validated.

## Troubleshooting

### No Results

##### Malformed Queries

A search which returns no results might be due to a malformed query.

```python
query_str = "bad publish:2018"
```

This query is trying to search on a field `publish` but no such field exists.

```python
query_str = "good published:2018"
```

This version should work.

##### Difficult Characters

The text corpus that is being searched was extracted from PDF documents. This
extraction process is not foolproof and has many strange characters as artifacts.
If you are searching for a person's name which contains a special character
or for a word which does not appear in English you may get zero results.

Searching for Math is not generally expected to work.

### Slow queries

It is expected that some queries will take 30 seconds or more to return. If it is
taking longer than that the Python kernel may have died. Restarting the kernel
and re-running the Setup cells in the notebook before re-running the query cell
may clear the problem. 

If a query consistently fails to return results or hangs try a few modifications
of the query string and then reach out for help.


### 'Notebook changed on disk'

Notebooks are not good at being used in multiple tabs or by multiple people. If you
save a change to your notebook in one tab it may cause a warning or error to
show up in any other tab that has the notebook open.

Try to only have the notebook open in only one tab at a time or you risk losing
work.

## System Administration

### Sessions

The jupyter notebook is run under a screen session names `jupyter`.

After login re-attach to this session with `screen -r jupyter`

Detach from this session by either closing the terminal window or typing `screen -d`.

If you need to create a new named screen session type `screen -S <session name>`

### Starting Jupyter

To start jupyter run `jupyter notebook --ip=0.0.0.0`. Note that the default IP address is 
`localhost` which is not world accessible.

### Configuring the Password

The initial and subsequent configuration of a password is done by running 
`jupyter notebook password`.
