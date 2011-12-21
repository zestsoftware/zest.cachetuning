  # -*- extra stuff goes here -*- 
from zope.i18nmessageid import MessageFactory
ZestCacheTuningMessageFactory = MessageFactory(u'zest.cachetuning')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
