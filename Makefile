.PHONY : build install clean

# Repertoires
PREFIX ?= /usr
BINDIR ?= $(PREFIX)/bin
DATADIR ?= $(PREFIX)/share

# Commande pour l'installation
INSTALL = install -m 755

# Version de Python a utiliser
PYTHON_VERSION ?= python

# Version de pluzzdl
PLUZZDL_VERSION = $(shell grep '__version__ = ".*"' src/main.py | cut -d '"' -f 2)

# Nom du repertoire
PLUZZDL_REPERTOIRE = pluzzdl-$(PLUZZDL_VERSION)


# Compilation
build :
	# ByteCode
	@$(PYTHON_VERSION) -c "import compileall ; compileall.compile_dir( 'src' )"
	# Modifie le lanceur
	sed -i 's|__DATADIR__|$(DESTDIR)$(DATADIR)|g' pluzzdl.sh

# Installation
install :
	# Met en place le lanceur
	mkdir -p $(DESTDIR)$(BINDIR)
	$(INSTALL) pluzzdl.sh $(DESTDIR)$(BINDIR)/pluzzdl
	# Change les droits du fichier (il doit etre executable)
	chmod a+x $(DESTDIR)$(BINDIR)/pluzzdl
	
	# Met en place le code
	mkdir -p $(DESTDIR)$(DATADIR)/pluzzdl
	$(INSTALL) src/* $(DESTDIR)$(DATADIR)/pluzzdl/

# Nettoyage
clean : 
	@echo "Nothing"

# Creation tar.gz
tar :
	@mkdir -p $(PLUZZDL_REPERTOIRE)
	@cp Makefile pluzzdl.sh $(PLUZZDL_REPERTOIRE)
	@mkdir -p $(PLUZZDL_REPERTOIRE)/src
	@cp src/*.py $(PLUZZDL_REPERTOIRE)/src/
	@tar czf pluzzdl_$(PLUZZDL_VERSION).orig.tar.gz $(PLUZZDL_REPERTOIRE)
	@rm -rf $(PLUZZDL_REPERTOIRE)
