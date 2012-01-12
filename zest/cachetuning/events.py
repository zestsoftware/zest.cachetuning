from Products.CMFCore.utils import getToolByName

def rebuild_js(context, event):
    """ When saving the tool, the JS compressed files are rebuilded.
    """
    portal_js = getToolByName(context, 'portal_javascripts')

    if not portal_js.getDebugMode():
        portal_js.setDebugMode(True)
        portal_js.cookResources()
        portal_js.setDebugMode(False)

    
