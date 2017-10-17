import csv
import re
from sp_app.models import SPKeyword

def my_import():
    EditorTag.objects.all().delete()

    with open('spip_mots.csv', 'r') as csvfile:
        val = {}
        r = csv.reader(csvfile, delimiter=";", quotechar='"')
        for line in r:
            if line[5] == 'Regroupements thématiques':
                val.clear()
                if line[1].startswith('<multi>'):
                    result = re.findall(r'\[(.{2})\]([^\[<]+)', line[1])
                    for code, value in result:
                        val['name_' + code] = value
                else:
                    val['name_fr'] = line[1]

                print(line[0], line[1])
                print(val)
                tag = SPKeyword(id_spip=line[0], **val)
                tag.save()


# 444, Sociabilité, , , 1, Regroupements thématiques, NULL, 2016-12-22 12:46:40
