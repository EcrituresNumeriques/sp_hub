import re

from spkeyword.models import SPKeyword

import logging
logger = logging.getLogger(__name__)

def create_update_keywords_from_multi_string(label, kw_data=None):
    # Do nothing if the string is empty
    if not label:
        return False

    created_keywords = []
    label_dict = split_multi_spstring(label)

    # Some keywords are multilingual but don't have French versions
    # So we check that first
    if 'fr' in label_dict:
        # Remove the french item from the dict
        kw_label = label_dict.pop('fr')
        # And create/update the corresponding keyword
        kw_fr = create_update_editor_kw(kw_label, kw_data=kw_data, lang='fr')
        created_keywords.append(kw_fr)

        # Then, look at other languages
        for lang in label_dict:
           new_kw = create_update_editor_kw(
            label_dict[lang],
            # We only have an alignemnt for the french version, so pass None here
            kw_data=None,
            lang=lang,
            translation_of=kw_fr,
           )
           created_keywords.append(new_kw)

        return created_keywords
    else:
        print("Cannot find 'fr' language for " + next(iter(label_dict.values())))
        return False

def create_update_editor_kw(label, kw_data=None, lang='fr', translation_of=None):
    # Look for an existing keyword by the same name
    existing_kw = SPKeyword.objects.filter(name=label, language=lang, is_editor=True)

    my_args = { 'is_editor': True,
                'language': lang,
                'is_translation': translation_of,
    }

    # If we have alignment info, then the keyword is aligned
    if kw_data:
        my_args['data'] = kw_data
        my_args['aligned'] = True

    # Update
    if existing_kw:
        logger.info('Update existing keyword: ' + label + ' (' + lang + ')')
        existing_kw.update(**my_args)
        return existing_kw.get()
    # Create
    else:
        logger.info('Create editor keyword ' + label + ' (' + lang + ')')
        my_kw = SPKeyword.objects.create(name=label, **my_args)
        my_kw.save()
        return my_kw

def split_multi_spstring(s):
    # Look for multilingual patterns
    matches = re.findall('\[(..)\]([^\[<]+)', s)
    # Looks like it's not multilingual
    if not matches:
        return { 'fr': s }
    else:
        return { m[0]: m[1] for m in matches }
