#!/usr/bin/env bash

[[ "${1}" == "" ]] && echo "usage: $0 (release|dev)" && exit 1
[[ "${1}" == "release" ]] && echo "creating release wheel..."
[[ "${1}" == "dev" ]] && export DEV="str(d.hour), str(d.minute)," && echo "creating dev wheel..."

git checkout exoedge_mqttsubscriber/__version__.py

BUILD_NUMBER=$(python -c "
import datetime
d = datetime.datetime.today()
print('.'.join(
    [
        str(d.year)[2:],
        str(d.month),
        str(d.day), ${DEV}
    ])
)
")
echo "__version__ = '$BUILD_NUMBER'" >> exoedge_mqttsubscriber/__version__.py

rm -rf dist build
python setup.py sdist bdist_wheel
git checkout exoedge_mqttsubscriber/__version__.py

