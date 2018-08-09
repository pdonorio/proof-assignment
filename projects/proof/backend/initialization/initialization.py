# -*- coding: utf-8 -*-
from utilities.logs import get_logger

log = get_logger(__name__)


class Initializer(object):

    def __init__(self, services):

        # # FIXME: should it avoided when TESTING?
        # handler = services.get('mongo')
        # print("TEST PAOLO\n\n", handler)

        # push users
        # set roles
        # push questions
        # push quizzes

        # self.neo4j = services['neo4j']
        # Provider = self.neo4j.Provider
        # try:
        #     Provider.nodes.get(identifier='MNC')
        #     log.debug("Provider MNC already exists")
        # except Provider.DoesNotExist:
        #     mnc = Provider()
        #     mnc.identifier = 'MNC'
        #     mnc.scheme = 'ACRO'
        #     mnc.name = 'Museo Nazionale del Cinema'
        #     mnc.address = 'Via Montebello, 20 10124 Torino, Italia'
        #     mnc.phone = '+39 011.8138.580'
        #     mnc.fax = '+39 011 8138 585'
        #     mnc.email = 'cineteca@museocinema.it'
        #     mnc.website = 'http://www.museocinema.it'
        #     mnc.save()
        #     log.info("Provider MNC successfully created")
        pass


"""
class Customizer(object):

    def custom_user_properties(self, properties):

        log.pp(properties)
        # properties["irods_cert"] = get_random_name(len=12)
        return properties

    def custom_post_handle_user_input(self, auth, user_node, properties):

        print("TEST", auth, user_node, properties)
        return True

        try:
            group = auth.db.Group.nodes.get(shortname="default")
        except auth.db.Group.DoesNotExist:
            log.warning("Unable to find default group, creating")
            group = auth.db.Group()
            group.fullname = "Default user group"
            group.shortname = "default"
            group.save()

        log.info("Link %s to group %s", user_node.email, group.shortname)
        user_node.belongs_to.connect(group)

        return True


"""
