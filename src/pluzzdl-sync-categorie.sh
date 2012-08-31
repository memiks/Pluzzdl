#!/bin/sh

ALLOWED="info documentaire serie--fiction magazine culture jeunesse divertissement sport jeu autre videos-en-regions tous-publics"
CAT=$1
BASE="http://www.pluzz.fr"

if [ -z "${CAT}" ]; then
	echo "Pas de catégorie. Sortie."
	exit 1
fi

echo ${ALLOWED} | grep -q -w "${CAT}"
if [ $? -ne 0 ]; then
	echo "Catégorie '${CAT}' inconnue."
	echo "Catégories connues : ${ALLOWED}"
	exit 2
fi

if [ ! -d ${CAT} ]; then
	mkdir ${CAT} || exit 3
fi

cd ${CAT}

PAGES=$(curl -s ${BASE}/${CAT} | grep "<li " | egrep 'class="current"|<li >' | grep '<\/li>' | sed -e 's/\t//g' | sed -e 's/<\/.*>//g' | sed -e 's/<li .*>//g')
for page in ${PAGES};
do
	VIDEOS=$(curl -s ${BASE}/${CAT}/${page} | grep "<a class=\"\" href=\"${BASE}" | sed -e 's/\t//g' | cut -d'"' -f4 | sort)
	for video in ${VIDEOS};
	do
		pluzzdl --resume --playlist $video
	done;
done;

cd ..
