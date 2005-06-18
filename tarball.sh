#!/bin/bash
# $Header: /var/cvsroot/gentoo-src/java-config/python/tarball.sh,v 1.10 2004/02/18 01:40:36 aether Exp $
 
if [ -z "$1" ]; then
        echo
        echo "you need to have the version specified."
        echo "e.g.: $0 1.1.0-r3"
        echo
        exit 0
fi
 
export PKG="java-config"
export TMP="/tmp"
export V="$1"
export DEST="${TMP}/${PKG}-${V}"


die () {
	echo "!!! $1"
	exit $2
}

LOG="/tmp/tarball.log"
!(test -e ${LOG}) || test -w ${LOG} || die "Error creating log files!" $?
rm -rf ${LOG}
touch ${LOG}

pod () {
	echo "popd" >> ${LOG}
	popd  >/dev/null
}

pud () {
	echo "pushd, $@" >> ${LOG}
	pushd "$@" >/dev/null
}

sed -i -e "s:__portage_version__.*=.*:__portage_version__ = \"$V\":" java-config

tabnanny_output=`python -c "import tabnanny; tabnanny.check('.')"`

if [[ -z ${tabnanny_output} ]]; then
	echo ">>> Tabnanny said everything was ok!"
else
	echo ">>> Tabnanny failed !!"
	echo ${tabnanny_output}
	exit 1
fi

test -e ${DEST} && (
	echo ">>> Removing any existing package directory"
	rm -rf ${DEST} 1>>${LOG} 2>>${LOG} || \
	  die "Removing existing package directory failed" $?
)

echo ">>> Creating new package directory (${DEST})"
install -d -m0755 ${DEST} || die "Error creating package dir" $?

echo ">>> Normalizing ChangeLog"
sed -i -e "s:\t:  :g" ChangeLog


echo ">>> Copying package contents to package directory"

test -w ${DEST} || die "Copying package contents failed" $?
(
	cp ChangeLog ${DEST}
	cp -a java_config ${DEST}
	cp setup.py ${DEST}
	cp 30java-finalclasspath ${DEST}
	cp java-config ${DEST}
	cp java-config.1 ${DEST}

) 1>>${LOG} 2>>${LOG} 
 
echo ">>> Cleaning package directory"
pud ${DEST}
echo ">>> ${PWD}" && sleep 2

(
	find -name CVS -exec rm -rf {} \;
	find -name '*~' -exec rm -rf {} \;
	find -name '*.pyc' -exec rm -rf {} \;
	find -name '.cvsignore' -exec rm -rf {} \;
	find -name '.*swp' -exec rm -rf {} \;

) 1>>${LOG} 2>>${LOG}

echo ">>> Changing ownership of package directory to root.root"
chown -R root.root 1>&2 2>/dev/null ${DEST} \
  || echo "*** Changing package directory to root.root failed!"

TARBALL="${TMP}/${PKG}-${V}.tar.bz2"
echo ">>> Creating tarball ($TARBALL)"
pud ${TMP}
tar cjf $TARBALL ${PKG}-${V}

for C in `seq 2`; do pod; done
