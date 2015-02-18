# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, lurl, request, redirect, tmpl_context
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg import predicates
from webui import model
from webui.controllers.secure import SecureController
from webui.model import DBSession
from tgext.admin.tgadminconfig import BootstrapTGAdminConfig as TGAdminConfig
from tgext.admin.controller import AdminController


from webui.lib.base import BaseController
from webui.controllers.error import ErrorController
from webui.model.page import Page
from docutils.core import publish_parts
import re
import HydraServer
from HydraServer.lib import project, network, attributes
from tg.predicates import in_group
from osgeo import osr, ogr
import json

import logging
log = logging.getLogger(__name__)

__all__ = ['RootController']

wikiwords = re.compile(r"\b([A-Z]\w+[A-Z]+\w+)")



class HydraAdminController(AdminController):
    allow_only = in_group('admin')

class RootController(BaseController):
    """
    The root controller for the webui application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """
    secc = SecureController()
    admin = HydraAdminController([model.User, model.Role, model.Perm], DBSession, config_type=TGAdminConfig)

    error = ErrorController()

    all_attributes = {}

    def _get_attributes(self):
        if self.all_attributes == {}:
            attrs = attributes.get_attributes() 
            self.all_attributes = {}
            for a in attrs:
                attr_details = {}
                attr_details['name'] = a.attr_name
                attr_details['dimension'] = a.attr_dimension
                self.all_attributes['id'] = attr_details 
    
    def _before(self, *args, **kw):
        tmpl_context.project_name = "Hydra Viewer"

    @expose('webui.templates.project')
    def _default(self, pagename="FrontPage"):
        """Handle the front-page."""
        from sqlalchemy.exc import InvalidRequestError

        if request.identity is not None:
            username = request.identity['repoze.who.userid']
            user_id = request.identity['user'].user_id
            display_name = request.identity['user'].display_name
            try:
                projects = project.get_projects(user_id, **{'user_id':user_id})
            except InvalidRequestError:
                raise redirect("notfound", pagename=pagename)

            return dict(display_name=display_name, projects=projects)
        else:
            redirect('/login',
                params=dict(came_from="", __logins=0))

    @expose('webui.templates.projects')
    def _default(self, pagename="FrontPage"):
        """Handle the front-page."""
        from sqlalchemy.exc import InvalidRequestError

        if request.identity is not None:
            username = request.identity['repoze.who.userid']
            user_id = request.identity['user'].user_id
            display_name = request.identity['user'].display_name
            try:
                projects = project.get_projects(user_id, **{'user_id':user_id})
            except InvalidRequestError:
                raise redirect("notfound", pagename=pagename)

            return dict(display_name=display_name, projects=projects)
        else:
            return dict(display_name="Please Log In", projects=[])

    @expose('webui.templates.error')
    def notfound(self, pagename):
        content = "Not found"
        return dict(content=c)

    #@expose('webui.templates.edit')
    #def edit(self, pagename):
    #    page = DBSession.query(Page).filter_by(pagename=pagename).one()
    #    return dict(wikipage=page)

    @expose('webui.templates.about')
    def about(self):
        """Handle the 'about' page."""
        return dict(page='about')

    # @expose()
    # def save(self, pagename, data, submit):
    #     page = DBSession.query(Page).filter_by(pagename=pagename).one()
    #     page.data = data
    #     redirect("/" + pagename)

    # @expose("webui.templates.pagelist")
    # def pagelist(self):
    #     pages = [page.pagename for page in DBSession.query(Page).order_by(Page.pagename)]
    #     return dict(pages=pages)

    @expose('webui.templates.project')
    def project(self, project_id):
        """This method returns a project page, with a list of networks."""
        user_id = request.identity['user'].user_id
        proj = HydraServer.lib.project.get_project(project_id, **{'user_id':user_id})
        return dict(project=proj, environment=request.environ)

    @expose('webui.templates.network')
    def network(self, network_id, scenario_id):
        """This method returns a network page, with a list of networks."""
        user_id = request.identity['user'].user_id
        net = HydraServer.lib.network.get_network(network_id, scenario_ids=[scenario_id], **{'user_id':user_id})
        
        if net.projection is not None:
            net_proj = net.projection.split(':')[1]
            source_proj = osr.SpatialReference()
            source_proj.ImportFromEPSG(int(net_proj))
            target_proj = osr.SpatialReference()
            target_proj.ImportFromEPSG(4326)
            transform = osr.CoordinateTransformation(source_proj, target_proj)
            for n in net.nodes:
                x = n.node_x
                y = n.node_y
                source_point = ogr.CreateGeometryFromWkt("POINT (%s %s)" % (x, y))
                source_point.Transform(transform)
                n.node_x = source_point.GetX()
                n.node_y = source_point.GetY()


        json_net = {'nodes':[], 'edges':[]}
        for node in net.nodes:
            node_dict = {
                'id' : str(node.node_id),
                'label': node.node_name,
                'x'    : float(node.node_x),
                'y'    : float(node.node_y),
                'size' : 2,
            }
            json_net['nodes'].append(node_dict)
        for link in net.links:
            link_dict = {
                'id' : str(link.link_id),
                'source': str(link.node_1_id),
                'target' : str(link.node_2_id),
            }
            json_net['edges'].append(link_dict)

        node_coords = {}
        node_name_map = {}
        for node in net.nodes:
            node_coords[node.node_id] = [node.node_x, node.node_y];
            node_name_map[node.node_id] = node.node_name
        link_coords = {}
        for link in net.links:
            link_coords[link.link_id] = [node_coords[link.node_1_id], node_coords[link.node_2_id]]

        DBSession.expunge_all() 
        
        return dict(network=net,
                    scenario_id=scenario_id,
                    environment=request.environ,
                    link_coords=link_coords,
                    node_coords=node_coords,
                    node_name_map=node_name_map,
                    json_net = json.dumps(json_net),
                    projection = net.projection)

    @expose('json')
    @expose('webui.templates.attributes')
    def attributes(self):
        attrs = self._get_attributes() 
        return dict(attributes=attrs)


    @expose('webui.templates.node')
    @expose('json')
    def node(self, node_id, scenario_id=None):
        user_id = request.identity['user'].user_id
        node_i = network.get_node(node_id, **{'user_id':user_id})
        attributes = []
        rs_dict = {}
        
        if scenario_id is not None:
            node_data = HydraServer.lib.scenario.get_resource_data('NODE', node_id, scenario_id, None, **{'user_id':user_id})
            for rs in node_data:
                rs_dict[rs.resource_attr_id] = rs.dataset

        for a in node_i.attributes:
            attr = {}
            attr['attr_id'] = a.attr_id
            attr['resource_attr_id']   = a.resource_attr_id
            attr['is_var'] = a.attr_is_var
            attr['name']   = a.attr.attr_name
            attr['value'] = rs_dict.get(a.resource_attr_id)
            attributes.append(attr)

        return dict(node_id=node_id, scenario_id=scenario_id, attributes=attributes)


    @expose('webui.templates.environ')
    def environ(self):
        """This method showcases TG's access to the wsgi environment."""
        return dict(page='environ', environment=request.environ)

    @expose('webui.templates.data')
    @expose('json')
    def data(self, **kw):
        """This method showcases how you can use the same controller for a data page and a display page"""
        return dict(page='data', params=kw)

    @expose('webui.templates.index')
    @require(predicates.has_permission('admin', msg=l_('Only for admin')))
    def manage_permission_only(self, **kw):
        """Illustrate how a page for admin only works."""
        return dict(page='admin stuff')

    @expose('webui.templates.index')
    @require(predicates.is_user('editor', msg=l_('Only for the editor')))
    def editor_user_only(self, **kw):
        """Illustrate how a page exclusive for the editor works."""
        return dict(page='editor stuff')

    @expose('webui.templates.login')
    def login(self, came_from=lurl('/')):
        """Start the user login."""
        login_counter = request.environ.get('repoze.who.logins', 0)
        if login_counter > 0:
            flash(_('Wrong credentials'), 'warning')
        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from)

    @expose()
    def post_login(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ.get('repoze.who.logins', 0) + 1
            redirect('/login',
                params=dict(came_from=came_from, __logins=login_counter))
        userid = request.identity['repoze.who.userid']
        flash(_('Welcome back, %s!') % userid)
        redirect(came_from)

    @expose()
    def post_logout(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('We hope to see you soon!'))
        redirect(came_from)
