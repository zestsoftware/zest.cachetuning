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

    def register_user(self, data):
        self.browser.open('http://nohost/plone/')
        self.browser.getLink('Register').click()
        data['password_confirm'] = data['password']

        for key, value in data.items():
            try:
                self.browser.getControl(name=key).value = value
            except LookupError:
                if key == 'password_confirm':
                    # In Plone 4, password confirm is called password_ctl
                    self.browser.getControl(name='form.password_ctl').value = value
                else:
                    # Plone 4, inputs are called 'form.xxx'
                    self.browser.getControl(name='form.%s' % key).value = value

        try:
            self.browser.getControl(name='form.button.Register').click()
        except LookupError:
            self.browser.getControl(name='form.actions.register').click()           

    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            ztc.installPackage(zest.cachetuning)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass
