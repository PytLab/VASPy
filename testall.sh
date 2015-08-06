#!/usr/bin/env bash

# 测试XyzFile和PosCar
python ./scripts/continue.py ./testdata/ts.xyz

# 测试OsziCar
python ./unittest/oszicar_test.py 
