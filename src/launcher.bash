#!/bin/bash

abort() {
	echo ${@} >&2
	exit 1
}
getjar() {
	local jar=${1}
	for x in $(java-config -p ${gjl_package} | tr ':' ' '); do
		if [ "$(basename ${x})" == "${jar}" ] ; then
			echo ${x}
			return 0
		fi
	done
	return 1
}

gjl_user_env=${HOME}/.gentoo/env.d/22${gjl_package}
gjl_system_env=/etc/env.d/java/22${gjl_package}
if [[ -f ${gjl_user_env} ]]; then
	source ${gjl_user_env}
elif [[ -f ${gjl_system_env} ]]; then
	source ${gjl_system_env}
fi


if [[ -n ${gjl_main} ]]; then
	gjl_starte=${gjl_main}
elif [[ -n ${gjl_jar} ]]; then
	gjl_fjar=$(getjar ${gjl_jar}) || gjl_fjar=${gjl_jar}
	gjl_starte="-jar ${gjl_fjar}"
else
	abort "Need main or jar to start" 
fi

if [[ -z ${GENTOO_VM} ]]; then
	export GENTOO_VM=$(gjl --get-vm ${gjl_package}) || abort "Couldn't get a vm"
else
	echo "found \$GENTOO_VM not trying to change vm" >> /dev/stderr
fi

gjl_args=$(gjl --get-args ${gjl_package}) || abort "Couldn't build classpath"

exec java ${gjl_args} ${gjl_java_args} ${gjl_starte} ${gjl_pkg_args} "${@}"
