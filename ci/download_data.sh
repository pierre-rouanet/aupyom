#!/usr/bin/env bash

pushd aupyom/example_data
    for f in *.wav; do
        echo "Downloading $f..."
        wget https://media.githubusercontent.com/media/pierre-rouanet/aupyom/$TRAVIS_BRANCH/aupyom/example_data/$f -O $f
    done
popd
