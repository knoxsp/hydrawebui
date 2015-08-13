# -*- coding: utf-8 -*-
"""Sample controller with all its actions protected."""
from tg import expose, flash
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.predicates import has_permission

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

        file_name = '/tmp/export.csv'
        
        df = pd.read_csv(file_name)
        df = df.rename(columns=lambda x: x.strip())

        selected_columns = df.columns[0:3]
        log.critical(selected_columns)

        d = df.to_csv(columns=[x for x in selected_columns], index=False),


        return dict(
            all_columns = [x for x in df.columns],
            selected_columns = [x for x in selected_columns],
            data = d,
            page='index')

    @expose('webui.templates.vis.index')
    def view_dataset(self, dataset_id):
        """Let the user know that's visiting a protected controller."""
        #flash(_("Graph Controller here"))
        return dict(page='index')

    @expose('json')
    def get_data(self, **kwargs):

        #total hack. TODO fix so that it's a specific parameter.
        columns = kwargs['columns[]']

        file_name = '/tmp/export.csv'
        
        df = pd.read_csv(file_name)
        df = df.rename(columns=lambda x: x.strip())

        d = df.to_csv(columns=columns, index=False),


        return dict(data = d)
