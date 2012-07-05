#!/usr/bin/env python2
# -*- coding:Utf-8 -*-

#
# Infos
#

__author__  = "Chaoswizard"
__license__ = "GPL 2"
__version__ = "0.8.5"
__url__     = "http://code.google.com/p/tvdownloader/"

#
# Modules
#

import argparse
import logging
import platform
import os
import re
import sys

from ColorFormatter import ColorFormatter
from PluzzDL        import PluzzDL

#
# Main
#

if( __name__ == "__main__" ) :
	
	# Arguments de la ligne de commande
	usage   = "pluzzdl [options] urlEmission"
	parser  = argparse.ArgumentParser( usage = usage, description = "Télécharge les émissions de Pluzz" )
	parser.add_argument( "-f", "--fragments",   action = "store_true", default = False, help = 'télécharge la vidéo via ses fragments même si un lien direct existe' )
	parser.add_argument( "-r", "--resume",      action = "store_true", default = False, help = 'essaye de reprendre un téléchargement interrompu' )
	parser.add_argument( "-b", "--progressbar", action = "store_true", default = False, help = 'affiche la progression du téléchargement' )
	parser.add_argument( "-p", "--proxy", dest = "proxy", metavar = "PROXY",            help = 'utilise un proxy HTTP au format suivant http://URL:PORT' )	
	parser.add_argument( "-v", "--verbose",     action = "store_true", default = False, help = 'affiche les informations de debugage' )
	parser.add_argument( "--nocolor",           action = 'store_true', default = False, help = 'désactive la couleur dans le terminal' )
	parser.add_argument( "--version",           action = 'version', version = "pluzzdl %s" %( __version__ ) )
	parser.add_argument( "urlEmission", action = "store", help = "URL de l'émission Pluzz a charger" )
	args = parser.parse_args()
	
	# Mise en place du logger
	logger  = logging.getLogger( "pluzzdl" )
	console = logging.StreamHandler( sys.stdout )
	if( args.verbose ):
		logger.setLevel( logging.DEBUG )
		console.setLevel( logging.DEBUG )
	else:
		logger.setLevel( logging.INFO )
		console.setLevel( logging.INFO )
	console.setFormatter( ColorFormatter( not args.nocolor ) )
	logger.addHandler( console )
	
	# Affiche la version de pluzzdl et de python
	logger.debug( "pluzzdl %s avec Python %s" %( __version__, platform.python_version() ) )
	
	# Verification de l'URL
	if( re.match( "http://www.pluzz.fr/[^\.]+?\.html", args.urlEmission ) is None 
	and re.match( "http://www.francetv.fr/[^\.]+?", args.urlEmission ) is None ):
		logger.error( "L'URL \"%s\" n'est pas valide" %( args.urlEmission ) )
		sys.exit( -1 )
	
	# Verification du proxy
	if( args.proxy is not None and re.match( "http://[^:]+?:\d+", args.proxy ) is None ):
		logger.error( "Le proxy \"%s\" n'est pas valide" %( args.proxy ) )
		sys.exit( -1 )

	# Fonction d'affichage de l'avancement du téléchargement
	if( args.progressbar ):
		progressFnct = lambda x : logger.info( "Avancement : %3d %%" %( x ) )
	else:
		progressFnct = lambda x : None
	
	# Telechargement de la video
	PluzzDL( url          = args.urlEmission,
			 useFragments = args.fragments,
			 proxy        = args.proxy,
			 resume       = args.resume,
			 progressFnct = progressFnct )
