from AccessControl import ClassSecurityInfo
from zope.interface import implements
from Products.Archetypes import atapi
from Products.CMFCore.utils import ImmutableId
from Products.CMFCore.permissions import ModifyPortalContent
from Products.ATContentTypes.content.document import ATDocument
from Products.ATContentTypes.content.document import ATDocumentSchema
from zope.interface import Interface, implements
from Products.CMFCore.utils import getToolByName

from zest.cachetuning import config
from zest.cachetuning import ZestCacheTuningMessageFactory as _


class ICacheTuningTool(Interface):
    """marker interface"""

cacheTuningToolSchema = ATDocumentSchema.copy() + atapi.Schema((
    atapi.BooleanField(
        name = 'jq_replace_username',
        default=True,
        widget = atapi.BooleanWidget(
            label=_(u'label_jq_replace_username',
                    default=u'Replace username using Javascript'),
            description=_(u'help_jq_replace_username',
                          default=u'Enable caching the pages ' + \
                          'and keeping username displayed.')
            ),
        schemata='username',
        ),

    atapi.StringField(
        name='jq_replace_username_selector',
        default_method = 'default_js_query',
        widget = atapi.StringWidget(
            label=_(u'label_jq_replace_username_selector',
                    default=u'CSS query to select username'),
            description=_(u'help_jq_replace_username_selector',
                          default=u'You can here specify a custom query ' + \
                          'to find the element containing the username.')
            ),
        schemata='username',
        ),
    ))

# Hides the default fields.
for field in ['title', 'description', 'text']:
    if field in cacheTuningToolSchema:
        cacheTuningToolSchema[field].widget.visible={'edit': 'invisible',
                                               'view': 'invisible'}

# Hides the fields other than the ones we defined.
allowed_schematas = ['username']
for key in cacheTuningToolSchema.keys():
    if cacheTuningToolSchema[key].schemata not in allowed_schematas:
        cacheTuningToolSchema[key].widget.visible={'edit': 'invisible',
                                                   'view': 'invisible'}

class CacheTuningTool(ImmutableId, ATDocument):
    """ Tool for zest.cachetuning product.
    Allows to set various options.
    """
    security = ClassSecurityInfo()
    __implements__ = ()
    implements(ICacheTuningTool)
    
    id = 'portal_zestcachetuning'
    typeDescription = "Configure Zest cache tuning"
    typeDescMsgId = 'description_edit_zestcachetuning_tool'
    schema = cacheTuningToolSchema

    def __init__(self, *args, **kwargs):
        self.setTitle('Zest Cache tuning configuration')

    security.declareProtected(ModifyPortalContent, 'indexObject')
    def indexObject(self):
        pass

    security.declareProtected(ModifyPortalContent, 'reindexObject')
    def reindexObject(self, idxs=[]):
        pass

    security.declareProtected(ModifyPortalContent, 'reindexObjectSecurity')
    def reindexObjectSecurity(self, skip_self=False):
        pass

    def default_js_query(self):
        migration = getToolByName(self, 'portal_migration')
        versions = migration.coreVersions()

        plone_major_version = versions.get('Plone', '').split('.')[0]
        if plone_major_version == '4':
            return 'a#user-name'

        return 'a#user-name span'


atapi.registerType(CacheTuningTool, config.PROJECTNAME)
