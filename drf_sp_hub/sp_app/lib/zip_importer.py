from zipfile import ZipFile
import tempfile
import shutil
import os
import re

from sp_app.models import Article

class ZipImporter():
    def __init__(self, zipf):
        with ZipFile(zipf, 'r') as my_zip:
            # Get current working dir
            self.cwd = os.getcwd()
            # Create temp space
            self.tmpdir = tempfile.mkdtemp()
            # Move to temp space
            os.chdir(self.tmpdir)
            # Extract zip file in temp space
            my_zip.extractall()

            # Iterate through uncompressed archive
            self.files = []

            with os.scandir(self.tmpdir) as my_root:
                for subdir in my_root:
                    # Iterate over subdirs only
                    if not subdir.is_dir():
                        continue

                    # Open subdir and look for files (not dirs)
                    with os.scandir(subdir.path) as my_d:
                        for f in my_d:
                            # Skip directories and check for media dir
                            if f.is_file() and f.startswith('SP') and f.endswith('.html'):
                                if os.path.isdir(os.path.join(subdir.path, 'media')):
                                    self.files.append(f)

            # Return to original directory
            os.chdir(self.cwd)

    def process_files(self):
        output = []
        for f in self.files:
            output.append(f.path)
            id_senspublic = re.findall(r'SP(\d+).html', f.filename)
            if len(id_senspublic) == 1:
                id_sp = id_senspublic[0]
                output.append('Found existing article ' + id_sp)
            else:
                continue

            try:
                # Try to load object
                obj = Article.objects.get(id_senspublic=id_sp)
            except Article.DoesNotExist:
                # Does not exist: create it
                obj = Article.objects.create(title=f.filename)

            with open(f, 'rb') as fp:
                obj.html_file.save(f, File(fp))

        return '\n'.join(output)

    def clean_files(self):
        shutil.rmtree(self.tmpdir)
