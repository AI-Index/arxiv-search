import os
import csv
import pandas
from datetime import date
from dateutil.relativedelta import relativedelta
from datetime import datetime as odt
from time import mktime, time
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, ID, TEXT, DATETIME
from whoosh.qparser import QueryParser
from IPython.display import display, Markdown, Latex

pandas.options.display.max_columns = None
pandas.options.display.max_colwidth = 2000

def get_text_filename(path):
    return path.split('/')[-1]

def get_paper_id(text_filename):
    pid = text_filename.replace(".pdf.txt", "")
    pid = text_filename.split('v')[0]
    return pid

def clean_text(text):
    return text.replace("\n", " ").replace("  ", " ").strip()

def create_results_csv(db, query, results):
    csv_filename = "q-results-{}.csv".format(int(time()))
    outpath = os.path.join("results", csv_filename)
    with open(outpath, 'w') as fh:
        writer = csv.writer(fh)
        writer.writerow([query])
        writer.writerow(["Link", "Title", "Summary"])
        for result in results:
            path = result['path']
            text_filename = get_text_filename(path)
            pid = get_paper_id(text_filename)
            data = db[pid]
            title = clean_text(data['title'])
            summary = clean_text(data['summary'])
            link = data['link']
            writer.writerow([link, title, summary])
    
    return outpath

def run_query(db, ix, query_str):
    print("Running Query ...")
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(query_str)
        results = searcher.search(query, limit=None)
        print("Found {} results.".format(len(results)))
        results_filename = create_results_csv(db, query_str, results)
        
    link_tmpl = '[Right-click "Save Link as ..." to Download CSV]({})'
    display(Markdown(link_tmpl.format(results_filename)))
    display(pandas.read_csv(results_filename))

def get_counts_over_time(ix, query_str, start_year, start_month, end_year, end_month, verbose=True):
    
    target_date = date(start_year, start_month, 1)
    end_date = date(end_year, end_month, 1)
    dates = []
    counts = []
    with ix.searcher() as searcher:    
        while target_date <= end_date:
            dates.append(target_date)
            date_str = target_date.strftime("%Y%m")
            if verbose:
                print("Now working on {} ...".format(date_str))
            q_tmpl = "{} published:{}".format(query_str, date_str)
            query = QueryParser("content", ix.schema).parse(q_tmpl)
            results = searcher.search(query, limit=None)
            count = len(results)
            counts.append(count)
            target_date += relativedelta(months=1)

    return dates, counts