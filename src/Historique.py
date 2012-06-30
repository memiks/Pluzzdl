#!/usr/bin/env python2
# -*- coding:Utf-8 -*-

#
# Modules
#

import cPickle as pickle
import datetime
import os

import logging
logger = logging.getLogger( "pluzzdl" )

#
# Constantes
#

FICHIER_CACHE = os.path.join( os.path.expanduser( "~" ), ".cache", "pluzzdl" )

#
# Classes
#

class Video( object ):
	
	def __init__( self, lien, fragments, finie, date = datetime.datetime.now() ):
		self.lien      = lien
		self.fragments = fragments
		self.finie     = finie
		self.date      = date
		
	def __eq__( self, other ):
		if not isinstance( other, Video ):
			return False
		else:
			return ( self.lien == other.lien )
	
	def __ne__( self, other ):
		return not self.__eq__( other )

class Historique( object ):
	
	def __init__( self ):
		self.charger()
	
	def __del__( self ):
		self.sauver()
	
	def charger( self ):
		if( os.path.exists( FICHIER_CACHE ) ):
			try:
				with open( FICHIER_CACHE, "r" ) as fichier:
					self.historique = pickle.load( fichier )
					logger.info( "Historique chargé" )
			except:
				self.historique = []
				logger.warning( "Impossible de lire le fichier d'historique %s, création d'un nouveau fichier" %( FICHIER_CACHE ) )
		else:
			self.historique = []
			logger.info( "Fichier d'historique indisponible, création d'un nouveau fichier" )

	def sauver( self ):
		self.nettoyer()
		try:
			with open( FICHIER_CACHE, "w" ) as fichier:
				pickle.dump( self.historique, fichier )
				logger.info( "Historique sauvé" )
		except:
			logger.warning( "Impossible d'écrire le fichier d'historique %s" %( FICHIER_CACHE ) )

	def nettoyer( self ):
		# Supprimer les videos de plus de 10 jours de l'historique
		for i in range( len( self.historique ) - 1, 0, -1 ):
			if( ( datetime.datetime.now() - self.historique[ i ].date ) > datetime.timedelta( days = 10 ) ):
				del self.historique[ i ]

	def ajouter( self, video ):
		if( isinstance( video, Video ) ):
			if( video in self.historique ):
				self.historique[ self.historique.index( video ) ] = video
			else:
				self.historique.append( video )

	def getVideo( self, lienVideo ):
		video = None
		for v in self.historique:
			if( v.lien == lienVideo ):
				video = v
				break
		return video


