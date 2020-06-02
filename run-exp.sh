cfg=$1
cfgfile="config_environment-${cfg}.sh"

if [ "${cfg}x" == "x" ]; then
    echo "ERROR: you must provide a configuration name."
    echo "Usage: $0 configname"
    echo "There must exist a file configure_environment-configname.sh on the base directory"
    exit 1
fi

if [ ! -f "${cfgfile}" ]; then
    echo "ERROR: ${cfgfile} script is missing"
    exit 1
fi

cfglogdir="logs/${cfg}"
mkdir -p "${cfglogdir}"
DT=`date "+%Y-%m-%d-%H-%M-%S"`
cfglog="${cfglogdir}/run-${DT}"
echo "" > "${cfglog}" # Clean log file

echo "Redirecting all outputs to log file: ${cfglog}"


function report {
    echo "$@"
    echo "$@" >> "${cfglog}"
}

function fail {
    report "FAIL: $@"
    exit 1
}

source "${cfgfile}" &>> "${cfglog}" || fail "Error when sourcing configuration script \"${cfgfile}\""

# Build utils
report "1- Building utils..."
(cd utils && make || fail "Could not build utils") &>> "${cfglog}"

# Build sorting apps
report "2- Building sorting apps..."
(cd src && make || fail "Could not build utils")  &>> "${cfglog}"
(cd src/bbsegsort && make || fail "Could not build utils")  &>> "${cfglog}"

# Build sorting apps
report "3- Executing benchmark..."
mkdir -p "./times/equal/${cfg}" || fail "Could not create directory ./times/equal/${cfg}"
mkdir -p "./times/diff/${cfg}" || fail "Could not create directory ./times/diff/${cfg}"

(cd ./src && bash -x ../scripts/genexec.sh "../times/equal/${cfg}" ../utils/equal.exe 2>> "../${cfglog}") \
    || fail "Error when executing benchmarks: equal"

(cd ./src && ../scripts/genexec.sh "../times/diff/${cfg}" ../utils/diff.exe 2>> "../${cfglog}") \
    || fail "Error when executing benchmarks: diff"

report "4- Execution finished without errors"