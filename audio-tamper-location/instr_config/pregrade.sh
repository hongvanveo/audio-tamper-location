#!/bin/bash
: <<'END'
Pregrade script for the fragile tamper-location audio lab.
It rebuilds grading state from the learner's current files.
END

homedir=$1
destdir=$2
dbg=/tmp/audio-tamper-location-pregrade.log

workdir="$homedir/$destdir/stego"
resultdir="$homedir/$destdir/.local/result"
result="$resultdir/tamper_location_check.txt"

mkdir -p "$resultdir"
: > "$result"
echo "pregrade for $homedir/$destdir" > "$dbg"

pass() { echo "PASS_$1" >> "$result"; }
fail() { echo "FAIL_$1: $2" >> "$result"; }

if [ -s "$workdir/cover.wav" ]; then
    pass "COVER_CREATED"
else
    fail "COVER_CREATED" "cover.wav missing"
fi

if [ -s "$workdir/marked.wav" ]; then
    pass "MARKED_CREATED"
else
    fail "MARKED_CREATED" "marked.wav missing"
fi

if [ -s "$workdir/.signature_found_done" ]; then
    pass "SIGNATURE_FOUND"
else
    fail "SIGNATURE_FOUND" "signature verification not completed"
fi

if [ -s "$workdir/.clean_audio_ok_done" ]; then
    pass "CLEAN_AUDIO_OK"
else
    fail "CLEAN_AUDIO_OK" "clean verification not completed"
fi

if [ -s "$workdir/tampered.wav" ]; then
    pass "TAMPERED_CREATED"
else
    fail "TAMPERED_CREATED" "tampered.wav missing"
fi

if [ -s "$workdir/.tamper_localized_done" ]; then
    pass "TAMPER_LOCALIZED"
else
    fail "TAMPER_LOCALIZED" "tamper localization not completed"
fi

