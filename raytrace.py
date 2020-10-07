# -*- coding: utf-8 -*-
import argparse
from glob import glob
import os
from os.path import join as pjoin
import shutil
import json
import yaml
from copy import copy
import xml.etree.ElementTree as ET
from textwrap import dedent

from jinja2 import Environment, FileSystemLoader, select_autoescape

# For running nbconvert programmatically
from traitlets import Unicode, List
from traitlets.config import Config
from nbconvert.preprocessors import Preprocessor, ExtractOutputPreprocessor
from nbconvert.preprocessors.extractoutput import platform_utf_8_encode
from nbconvert import HTMLExporter
from nbconvert.writers import FilesWriter

class Navbar(Preprocessor):
    pages = List(help='dict from toc.yaml').tag(config=True)
    active_page = Unicode(help='name of active page').tag(config=True)

    def preprocess(self, nb, resources):
        resources['navbar'] = {'pages': self.pages,
                               'active_page': self.active_page}
        return nb, resources

class ExtractX3DPreprocessor(Preprocessor):
    '''Extract embedded X3D into separate file and fix some things.

    This largely follows the ExtractOutputPreprocessor, but in the
    current form mayavi writes output that's not quite right to process.
    This is some quick-and-dirty around that, because a real fix
    requires changes to IPython and mayavi themselves.

    Problems:
      - <?xml ...> tag not in first line and has leading white space
      - js code with requirejs included (so more than one tag)
    '''

    output_filename_template = Unicode(
        "{unique_key}_{cell_index}_{index}{extension}"
    ).tag(config=True)

    def preprocess_cell(self, cell, resources, cell_index):
        """
        Apply a transformation on each cell,
        Parameters
        ----------
        cell : NotebookNode cell
            Notebook cell being processed
        resources : dictionary
            Additional resources used in the conversion process.  Allows
            preprocessors to pass variables into the Jinja engine.
        cell_index : int
            Index of the cell being processed (see base.py)
        """
        #Get the unique key from the resource dict if it exists.  If it does not
        #exist, use 'output' as the default.  Also, get files directory if it
        #has been specified
        unique_key = resources.get('unique_key', 'output')
        output_files_dir = resources.get('output_files_dir', None)

        #Make sure outputs key exists
        if not isinstance(resources['outputs'], dict):
            resources['outputs'] = {}

        #Loop through all of the outputs in the cell
        for index, out in enumerate(cell.get('outputs', [])):
            if out.output_type not in {'display_data', 'execute_result'}:
                continue
            if 'text/html' in out.data:
                if not '<X3D' in out['data']['text/html']:
                    continue

                # change label to model/x3d+xml


                out['data']['text/html'] = dedent(out['data']['text/html'])

                # invent a root tag. Othersiwe <X3D> and <script>
                # are on the same level and ET require a single root
                # and insert that after the <?xml ...?>
                fixedtext =  out['data']['text/html'].replace('?>', '?><temp>')
                fixedtext = fixedtext + '</temp>'
                # <?xml=...  cannot be preceeded by emtpy lines
                fixedtext = fixedtext.lstrip()
                root = ET.fromstring(fixedtext)
                # Only use XML specs, not javascript that comes after it
                xml = root.find('X3D')
                data = ET.tostring(xml)
                data = platform_utf_8_encode(data)

                ext = '.x3d'
                if out.metadata.get('filename', ''):
                    filename = out.metadata['filename']
                    if not filename.endswith(ext):
                        filename+=ext
                else:
                    filename = self.output_filename_template.format(
                        unique_key=unique_key,
                        cell_index=cell_index,
                        index=index,
                        extension=ext)

                    # On the cell, make the figure available via
                    #   cell.outputs[i].metadata.filenames['mime/type']
                    # where
                    #   cell.outputs[i].data['mime/type'] contains the data
                    if output_files_dir is not None:
                        filename = os.path.join(output_files_dir, filename)
                    out.metadata.setdefault('filenames', {})
                    out.metadata['filenames']['text/html'] = filename

                    if filename in resources['outputs']:
                        raise ValueError(
                            "Your outputs have filename metadata associated "
                            "with them. Nbconvert saves these outputs to "
                            "external files using this filename metadata. "
                            "Filenames need to be unique across the notebook, "
                            "or images will be overwritten. The filename {} is "
                            "associated with more than one output. The second "
                            "output associated with this filename is in cell "
                            "{}.".format(filename, cell_index)
                            )
                    #In the resources, make the figure available via
                    #   resources['outputs']['filename'] = data
                    resources['outputs'][filename] = data

        return cell, resources



default_htmlexporter = HTMLExporter()



parser = argparse.ArgumentParser(description='Generate website to bundle ray-trace simulations in one place with both Jupiter notebooks rendered to html and x3d output. If notebook and/or x3d path are set, those files will be copied to the correct location. If not, only the "skeleton" around it will be build, e.g. to reuse notebook files already on the server with a different ordering or layout.')
parser.add_argument('project',
                    help='ray-trace project to build websites for')
parser.add_argument('outpath',
                    help='base directory for output')
parser.add_argument('--x3dpath',
                    help='directory where x3d files are found')
parser.add_argument('--notebookpath',
                    help='directory where html rendered notebooks are found')


args = parser.parse_args()

# Generate html
env = Environment(loader=FileSystemLoader(['templates',
                                           args.project]),
                  autoescape=select_autoescape(['html']))

outpath = os.path.join(args.outpath, args.project)
os.makedirs(outpath, exist_ok=True)

with open(os.path.join(args.project, 'toc.yaml'), 'r') as f:
    conf = yaml.safe_load(f)


# The page list is nested to represent the structure of the menu.
# Make a flattened copy that can be iterated over:
def add_children(flatlist, page):
    flatlist.append(page)
    if 'children' in page:
        for p in page['children']:
            add_children(flatlist, p)

flatlist = []
#add_children(flatlist, conf)

for c in conf['children']:
    if 'children' in c:
        flatlist.extend(c['children'])
    else:
        flatlist.append(c)

for page in flatlist:
    kwargs = copy(page)
    if page['type'] == 'included':
        template = env.get_template(page['href'] + '.html')

        with open(pjoin(args.outpath, args.project,
                        page['href'] + '.html'), "w") as f:
            f.write(template.render(pages=conf['children'],
                                    active_page=page['href'],
                                    mission=page.get('mission', conf['mission']),
                                    description=page.get('description',
                                                         conf['description']),
                                    **kwargs))
        print("Wrote {0}".format(page['title']))


    # else:
    #     template = env.get_template(page['type'] + '.html')
    #     if (page['type'] == 'x3d') and args.x3dpath:
    #         with open(pjoin(args.x3dpath, page['href'] + '.json'), 'r') as f:
    #             kwargs['x3d'] = json.load(f)
    #         kwargs['x3d']['path'] = pjoin('x3d', page['href'])
    #         outdir = pjoin(outpath, 'x3d')
    #         os.makedirs(outdir, exist_ok=True)
    #         shutil.copy(pjoin(args.x3dpath, page['href'] + '.x3d'),
    #                     pjoin(outdir, page['href'] + '.x3d'))

    elif (page['type'] == 'notebook'):
        c = Config()
        c.HTMLExporter.template_file = 'index.html.j2'
        c.HTMLExporter.template_paths = ['./nbconverttemplates/notebook/', './templates/'] + default_htmlexporter.template_paths
        c.Navbar.pages = conf['children']
        c.Navbar.active_page = page['href']
        c.HTMLExporter.preprocessors = [Navbar,
                                        ExtractOutputPreprocessor,
                                        ExtractX3DPreprocessor
        ]
        c.FilesWriter.build_directory = outpath
        c.FilesWriter.relpath = outpath
#        c.ExtractOutputPreprocessor.extract_output_types = (
#        'image/png', 'image/jpeg', 'image/svg+xml', 'application/pdf',
#         'text/html'
#    )

        # create the new exporter using the custom config
        # Cannot reuse the old one, because Navbar active page
        # is different every time
        html_exporter = HTMLExporter(config=c)
        ipyfile = pjoin(args.notebookpath, page['href'] + '.ipynb')
        resources = {'output_files_dir': page['href']}
        (body, resources) = html_exporter.from_filename(ipyfile,
                                                        resources=resources
                                                        )

        fileswriter = FilesWriter(config=c)
        written = fileswriter.write(body, resources, notebook_name=page['href'])
        print(f'wrote {written}')


# copy several directories verbatim
for d in ['css', 'images']:
    outdir = pjoin(args.outpath, d)
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    filelist = glob(pjoin(d, '*'))
    for f in filelist:
        shutil.copy(f, outdir)

print("Done. Website is in directory: {}.".format(args.outpath))
print("If this version is meant for publication, take the following steps:")
print(" cd {}".format(args.outpath))
print(" git add any_new_files")
print(" git commit -am'My message here'")
print(" scp -r * space:/space/web/home/guenther/{}".format(args.project))

'''
converting norebooks and inserting footer and nav bar

- footer is easy because it's static: Use custom Jinja template, which inherits from standard html: https://nbconvert.readthedocs.io/en/latest/customizing.html#the-content-of-nbconvert-templates
- my navbar uses bootstrap 4, while notebook uses bootstrap 3, so that need a few changes
  - js: bootstrap4 uses newer version of jquery: https://nbconvert.readthedocs.io/en/latest/config_options.html, use: HTMLExporter.jquery_url='https://code.jquery.com/jquery-3.5.1.slim.min.js' That way, I replace the old jquery. Could also overwrite js block in template with hardcoded new path.

  - in template add links to bootstrap css, popper js and bootstrap js
  - override a few styles for notebook which otherwise expands ot fill page even for short notebooks:

div#notebook {
  padding-bottom: 20px;
  min-height: unset;
}
</style>

  - remove embedded bootstrap3. I think the easiest might be to change template to not inline css at all and manually stick all required css (bootstrap 4 + jupyter sepecific stuff) into separate files (or just one file) and load that. Could be done using the "resoures" in the converter, but seems like a pain (also, how would I know that all notebook really use the sae files?). Risk: When notebook updates, I manually have ot update the style. I think I can live with that or look where jupyter keeps the style files and copy from there.

  - navbar: programatically create template: https://nbconvert.readthedocs.io/en/latest/nbconvert_library.html#Programmatically-creating-templates
    Simply make template with navbar filled in and pass that to html exporter.

  - Bonus: Do not embed, but have images (and x3d) separately in a different directory.  https://nbconvert.readthedocs.io/en/latest/nbconvert_library.html


'''
