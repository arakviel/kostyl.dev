#!/usr/bin/env bash
# usage: check.sh <project-id>  -> compact summary of lint/runtime/layout/contrast/craft findings
cd /Users/arakviel/Work/kostyl.dev/tools/hyperframes/${HF_MODULE:-cnn-image-classification}/$1
npx hyperframes check --json > /tmp/chk_$1.json 2>&1
python3 -I - "$1" <<'P'
import json,collections,sys
raw=open(f"/tmp/chk_{sys.argv[1]}.json").read(); d,_=json.JSONDecoder().raw_decode(raw[raw.index('{'):])
for k in('lint','runtime','layout','motion','contrast','craft'):
    print(k,dict(collections.Counter((f.get('code'),f.get('severity')) for f in d[k]['findings'])))
for k in('lint','runtime','layout','contrast','craft'):
    for f in d[k]['findings']:
        if f.get('severity')=='error' or f.get('code') in ('dead_stretch','first_frame_empty','text_below_floor'): print(' ',k,f.get('code'),f.get('time'),f.get('selector') or '',str(f.get('message'))[:110])
P
rm -f /tmp/chk_$1.json
