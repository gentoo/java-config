#!/bin/bash

abort() {
	echo ${@} >> /dev/stderr
	exit 1
}
getjar() {
	local jar=${1}
	for x in $(java-config -p ${package} | tr ':' ' '); do
		if [ "$(basename ${x})" == "${jar}" ] ; then
			echo ${x}
			return 0
		fi
	done
	return 1
}

if [[ -n ${main} ]]; then
	starte=${main}
elif [[ -n ${jar} ]]; then
	fjar=$(getjar ${jar}) || fjar=${jar}
	starte="-jar ${fjar}"
else
	abort "Need main or jar to start" 
fi

if [[ -z ${GENTOO_VM} ]]; then
	export GENTOO_VM=$(gjl --get-vm ${package}) || abort "Couldn't get a vm"
else
	echo "found \$GENTOO_VM not trying to change vm" >> /dev/stderr
fi

args=$(gjl --get-args ${package}) || abort "Couldn't build classpath"

exec java ${args} ${java_args} ${starte} ${pkg_args} "${@}"
