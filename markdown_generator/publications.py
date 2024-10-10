# coding: utf-8

# # Publications markdown generator for academicpages
# 
# Takes a TSV of publications with metadata and converts them for use with academicpages.github.io. This is an interactive Jupyter notebook, with the core python code in publications.py.

# ## Import pandas
import pandas as pd

# ## Import TSV
# Pandas makes this easy with the read_csv function. We are using a TSV, so we specify the separator as a tab, or `\t`.
publications = pd.read_csv("publications.tsv", sep="\t", header=0)

# ## Escape special characters
# YAML is very picky about how it takes a valid string, so we are replacing single and double quotes (and ampersands) with their HTML encoded equivalents. This makes them look not so readable in raw format, but they are parsed and rendered nicely.

html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;"
}

def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c,c) for c in text)

# ## Creating the markdown files
# This is where the heavy lifting is done. This loops through all the rows in the TSV dataframe, then starts to concatenate a big string (```md```) that contains the markdown for each type. It does the YAML metadata first, then does the description for the individual page.

import os
for row, item in publications.iterrows():
    
    md_filename = str(item.pub_date) + "-" + item.url_slug + ".md"
    html_filename = str(item.pub_date) + "-" + item.url_slug
    year = item.pub_date[:4]
    
    ## YAML variables
    md = "---\ntitle: \""   + item.title + "\"\n"
    
    md += """collection: publications"""
    
    md += """\npermalink: /publication/""" + html_filename
    
    if len(str(item.excerpt)) > 5:
        md += "\nexcerpt: '" + html_escape(item.excerpt) + "'"
    
    md += "\ndate: " + str(item.pub_date) 
    
    md += "\nvenue: '" + html_escape(item.venue) + "'"
    
    if len(str(item.slides_url)) > 5:
        md += "\nslidesurl: '<small><a href=\"" + item.slides_url + "\">Download slides here</a></small>'"
    
    if len(str(item.paper_url)) > 5:
        md += "\npaperurl: '<small><a href=\"" + item.paper_url + "\">Download paper here</a></small>'"
    
    md += "\ncitation: '<small>" + html_escape(item.citation) + "</small>'"
    
    md += "\n---"
    
    ## Markdown description for individual page
    if len(str(item.excerpt)) > 5:
        md += "\n" + html_escape(item.excerpt) + "\n"
    
    if len(str(item.slides_url)) > 5:
        md += "\n<small><a href='" + item.slides_url + "'>Download slides here</a></small>\n"
    
    if len(str(item.paper_url)) > 5:
        md += "\n<small><a href='" + item.paper_url + "'>Download paper here</a></small>\n"
    
    md += "\n<small>Recommended citation: " + item.citation + "</small>\n"
    
    # Save the markdown file
    md_filename = os.path.basename(md_filename)
    
    with open("../_publications/" + md_filename, 'w') as f:
        f.write(md)
