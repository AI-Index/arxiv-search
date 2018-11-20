# arxiv-search
Scripts associated with the Arxiv search Jupyter Notebook

## Getting Started

This search tool is provided as a hosted Jupyter notebook.

The URL for the notebook and the password to access it will have been emailed to you.

Please click on the link in the email and enter the provided password.

Once you are viewing the notebook [ENTER NOTEBOOK NAME HERE], please follow the instructions
in the notebook to run a search or generate a graph.

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

### Slow queries

It is expected that some queries will take 30 seconds or more to return. If it is
taking longer than that the Python kernel may have died. Restarting the kernel
and re-running the Setup cells in the notebook before re-running the query cell
may clear the problem. 

If a query consistently fails to return results or hangs try a few modifications
of the query string and then reach out for help.
