from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

class JqFullName(BrowserView):
    """ A simple class rendering the user's fullname.
    It is called by a JS
    """

    def __call__(self):
        mtool = getToolByName(self.context, "portal_membership")
        anonymous = mtool.isAnonymousUser()
        if anonymous:
            return

        userid = mtool.getAuthenticatedMember().getId()
        member_info = mtool.getMemberInfo(userid)
        # member_info is None if there's no Plone user object, as when
        # using OpenID.
        if member_info:
            fullname = member_info.get('fullname', '')
            plone_utils = getToolByName(self.context, 'plone_utils')
            charset = plone_utils.getSiteEncoding()
            decoded_fullname = fullname.decode(charset).strip()

            if decoded_fullname:
                return decoded_fullname

        return userid
