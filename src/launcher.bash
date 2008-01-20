#!/bin/bash
# Not-so-elegant? patches more then welcome

abort() {
	echo ${@} >&2
	exit 1
}

# Source package env
# ---------------------
gjl_user_env="${HOME}/.gentoo/java-config-2/launcher.d/${gjl_package}"
gjl_system_env="/etc/java-config-2/launcher.d/${gjl_package}"
if [[ -f "${gjl_user_env}" ]]; then
	source "${gjl_user_env}"
elif [[ -f "${gjl_system_env}" ]]; then
	source "${gjl_system_env}"
fi

# Build gjl arguments
# ---------------------
request="--package ${gjl_package} --get-args"

if [[ -n ${gjl_main} ]]; then
	gjl_starte=${gjl_main}
elif [[ -n ${gjl_jar} ]]; then
	request="${request} --get-jar ${gjl_jar}"
else
	# Check if the installed package has only one jar and use that
	jars=$(java-config --classpath=${gjl_package})
	if [[ "${jars/:}" = "${jars}" ]]; then
		request="${request} --get-jar ${jars}"
	else
		abort "Need main or jar to start"
	fi
fi

if [[ -z ${GENTOO_VM} ]]; then
	request="${request} --get-vm"
elif [[ -n ${GJL_DEBUG} ]]; then
	echo "Detected \$GENTOO_VM is set, not trying to change vm" >&2
fi

# Get the information we need
# ----------------------------
[[ "${GJL_DEBUG}" ]] && echo "Calling: gjl ${request}"
results=$(gjl ${request}) || abort "Couldn't get needed information"
eval $results

if [[ -n ${gjl_vm} ]]; then
	export GENTOO_VM="${gjl_vm}"
fi

if [[ -z ${gjl_starte} ]]; then
	abort "Dont know what to run :(("
fi

# Run it
# --------

if [[ -n ${gjl_pwd} ]]; then
	cd ${gjl_pwd}
fi

if [[ -n ${GJL_DEBUG} ]]; then
	echo "Using: ${GENTOO_VM}" >&2
	echo "Running: exec ${gjl_args} ${gjl_java_args} ${gjl_starte} ${gjl_pkg_args} ${@}" >&2
fi

exec java ${gjl_args} ${gjl_java_args} ${gjl_starte} ${gjl_pkg_args} "${@}"
