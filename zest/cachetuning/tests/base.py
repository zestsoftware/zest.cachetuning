import unittest

#from zope.testing import doctestunit
#from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
ptc.setupPloneSite()

try:
    from Testing.testbrowser import Browser
except ImportError:
    # Plone 3
    from Products.Five.testbrowser import Browser

import zest.cachetuning

class TestCase(ptc.PloneTestCase):
    browser = Browser()

    def login_as_user(self, username, password):
        self.browser.open('http://nohost/plone/logout')
        self.browser.open('http://nohost/plone/login_form')
        self.browser.getControl(name='__ac_name').value = username
        self.browser.getControl(name='__ac_password').value = password
        self.browser.getControl(name='submit').click()

    def login_as_manager(self):
        self.login_as_user(
            ptc.portal_owner,
            ptc.default_password)

    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            ztc.installPackage(zest.cachetuning)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass
