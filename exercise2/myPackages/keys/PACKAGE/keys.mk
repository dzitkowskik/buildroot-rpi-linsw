LEDKEYS_VERSION = 1.0
LEDKEYS_SITE = $(TOPDIR)/myPackages/keys
LEDKEYS_SITE_METHOD = local

define LEDKEYS_BUILD_CMDS
	$(MAKE) $(TARGET_CONFIGURE_OPTS) keys -C $(@D)
endef
define LEDKEYS_INSTALL_TARGET_CMDS
	$(INSTALL) -D -m 0755 $(@D)/keys $(TARGET_DIR)/usr/bin
endef
LEDKEYS_LICENSE = MIT

$(eval $(generic-package))
