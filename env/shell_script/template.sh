#! /bin/bash

# --- show usage ---
function usage {
    cat <<EOF
$(basename ${0}) is a test tool for ...

Usage:
    $(basename ${0}) [command] [<options>]

Options:
    --version, -v     print version
    --help, -h        print this
EOF
}

# --- show version ---
function version {
    echo "$(basename ${0}) version 0.0.1 "
}

# --- argument processing ---
if [ $# -eq 0 ];
    usage
    exit 1

while [ $# -gt 0 ];
do
    case ${1} in

        --version|-v)
            version
            exit 1
        ;;
        
        --help|-h)
            usage
            exit 1
        ;;
        
        *)
            echo "[ERROR] Invalid option '${1}'"
            usage
            exit 1
        ;;
    esac
    shift
done

