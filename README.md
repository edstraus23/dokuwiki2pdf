# DokuWiki Content Conversion to PDF Using DITA-OT and Python

## Download the Code

1. Download zip file (`Code > Download Zip`).
2. Unzip file into a folder.
3. Move the `convert.py` file to the top-level of the dokuwiki folder structure (at the same level as the `html` folder).

## Using the Code
I rely heavily on DokuWiki for creating blog posts and taking notes for
coding and command line entries. It is very easy to use and offers many
extensions.

While DokuWiki extensions can generate PDFs, combining multiple posts
into a single document is difficult. This is where DITA Open Toolkit
(DITA OT) comes in. DITA excels at combining files and generating clean
tables of contents.

Since DITA OT requires Markdown, I use Pandoc to
convert the DokuWiki files into Markdown files. Below is the workflow
for using a DITA bookmap to combine and generate the final PDF. 

See the following Medium blog post for further details:

[DokuWiki Content Conversion to PDF Using DITA-OT and Python](https://medium.com/@cindyeric/dokuwiki-content-conversion-to-pdf-using-dita-ot-and-python-03eb291c8623?postPublishedType=repub)



### 1. Create a Bookmap File in DokuWiki

This page contains XML configuration and special comments that tell the
Python script how to process images and files. Create it in DokuWiki
inside ''code'' tags (e.g., at `ditamap:blogs`).

    <code>
    <?xml version='1.0' encoding='utf-8'?><!DOCTYPE bookmap PUBLIC "-//OASIS//DTD DITA BookMap//EN" "../dtd/bookmap/dtd/bookmap.dtd">
    <bookmap id="test1">
    <booktitle>
    <booklibrary>Blog Posts</booklibrary>
    <mainbooktitle>Compilation of Posts</mainbooktitle>
    <booktitlealt>By: Eric Strausbaugh</booktitlealt></booktitle>
    <frontmatter>
    <booklists><toc/></booklists>
    </frontmatter>

    <!-- :IMG:html/data/media/drupal:topics/drupal: -->
    <!-- :IMG:html/data/media/dita:topics/dita: -->
    <!-- :IMG:html/data/media/docker:topics/docker: -->

    <!-- :DW:html/data/pages/blogs:intro: -->
    <chapter href="topics/intro.md" format="markdown">
    <!-- :DW:html/data/pages/drupal:drupal_dita_pdf: -->
     <topicref href="topics/drupal_dita_pdf.md" format="markdown"></topicref>
    <!-- :DW:html/data/pages/dita:conref: -->
      <topicref href="topics/conref.md" format="markdown"></topicref>
    <!-- :DW:html/data/pages/docker:containers: -->
      <topicref href="topics/containers.md" format="markdown"></topicref>
    </chapter>
    </bookmap>
     </code > 

- Comment syntax to copy images from `html/data/media/drupal` to
  `topics/drupal`:

<!-- -->

    <!-- :IMG:html/data/media/drupal:topics/drupal: -->

- Comment syntax to convert a DokuWiki file
  (`html/data/pages/blogs/intro.txt`) to Markdown (`topics/intro.md`).
  **Note:** Omit the file extensions in the comment.

<!-- -->

    <!-- :DW:html/data/pages/blogs:intro: -->


### 2. Run the Python Conversion Script

Note: Activate your Python virtual environment first.

Run the conversion script by passing the source DokuWiki bookmap path
and the desired output `.ditamap` filename.

``` bash
sudo python3 convert.py  html/data/pages/ditamap/blogs.txt blogs.ditamap
```

- `html/data/pages/ditamap/blogs.txt` - Path to the source DokuWiki
  bookmap file.
- `blogs.ditamap` - Output `.ditamap` filename.

NOTE: Run from the top-level of the dokuwiki folder structure.

## 3. Run DITA OT Command to Create PDF File

    ~/dita-ot-4.4/bin/dita --input=blogs.ditamap --format=pdf --output=out
