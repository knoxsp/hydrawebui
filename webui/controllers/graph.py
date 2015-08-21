# -*- coding: utf-8 -*-
"""Sample controller with all its actions protected."""
from tg import expose, flash
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.predicates import has_permission
from io import StringIO
import cherrypy

import pandas as pd
from webui.lib.base import BaseController

import logging
log = logging.getLogger(__name__)

__all__ = ['GraphController']

class GraphController(BaseController):
    """Sample controller-wide authorization"""
    
    # The predicate that must be met for all the actions in this controller:
#    allow_only = has_permission('edit_perm',
#                                msg=l_('Only for people with the "edit_perm" permission'))
    
    @expose('webui.templates.vis.index')
    def index(self):
        """Let the user know that's visiting a protected controller."""
        #flash(_("Graph Controller here"))
        return dict(page='index')

    @expose('json')
    def upload_csv(self, csv_file):
        """Let the user know that's visiting a protected controller."""
        df = pd.read_csv(csv_file.file)
        df = df.rename(columns=lambda x: x.strip())

        all_data = df.to_csv(index=False),

        return dict(
            data = all_data,    
            columns = list(df.columns),#Convert from a dataframe column object to a list.
        )

    @expose('webui.templates.vis.index')
    def view_dataset(self, dataset_id):
        """Let the user know that's visiting a protected controller."""
        #flash(_("Graph Controller here"))
        return dict(page='index')

    @expose('json')
    def get_data(self, csv_text, x, y, z, size, color, filter):
        
        #There must be x, y and z options
        columns = [x, y, z]
        if color is not None and color != "":
            columns.append(color)
        if size is not None and size != "":
            columns.append(size)
        if filter is not None and filter != "":
            columns.append(filter)

        str_io = StringIO(csv_text)

        df = pd.read_csv(str_io)
        df = df.rename(columns=lambda x: x.strip())

        d = df.to_csv(columns=columns, index=False),

        return dict(
                    data = d
                )
