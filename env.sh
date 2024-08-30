SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
export PYTHONPATH=$SCRIPT_DIR
export STC_LOG_LEVEL=DEBUG
# export RISCV=/usr/local/hpe
# export LD_LIBRARY_PATH=/usr/local/hpe/lib:$LD_LIBRARY_PATH
export GIT_LFS_SKIP_SMUDGE=1

