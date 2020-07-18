main: 
movi v0 1 
snei v0 0 
jump afterthanid1 
imovi savelabelid3 
store vF 
jump savelabelid4 
savelabelid3: 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
savelabelid4: 
movi v0 0xB 
movr v1 v0 
movi v0 10 
movr v2 v0 
movi v0 10 
movr v3 v0 
call drawhex 
imovi savelabelid3 
load vF 
jump afterelseid2 
afterthanid1: 
imovi savelabelid5 
store vF 
jump savelabelid6 
savelabelid5: 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
savelabelid6: 
movi v0 0xA 
movr v1 v0 
movi v0 10 
movr v2 v0 
movi v0 10 
movr v3 v0 
call drawhex 
imovi savelabelid5 
load vF 
afterelseid2: 
movi v0 1 
snei v0 0 
jump afterthanid7 
imovi savelabelid9 
store vF 
jump savelabelid10 
savelabelid9: 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
savelabelid10: 
movi v0 0xC 
movr v1 v0 
movi v0 20 
movr v2 v0 
movi v0 10 
movr v3 v0 
call drawhex 
imovi savelabelid9 
load vF 
jump afterelseid8 
afterthanid7: 
afterelseid8: 
movi v0 0 
snei v0 0 
jump afterthanid11 
imovi savelabelid13 
store vF 
jump savelabelid14 
savelabelid13: 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
savelabelid14: 
movi v0 0xD 
movr v1 v0 
movi v0 30 
movr v2 v0 
movi v0 10 
movr v3 v0 
call drawhex 
imovi savelabelid13 
load vF 
jump afterelseid12 
afterthanid11: 
afterelseid12: 
 
drawhex: 
imovi savelabelid15 
store vF 
jump savelabelid16 
savelabelid15: 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
movr v0 v0 
savelabelid16: 
movr v0 v1 
movr v3 v0 
movr v0 v2 
movr v2 v0 
movr v0 v3 
movr v1 v0 
 
        digit v3 
        sprite v2 v1 5 
    imovi savelabelid15 
load vF 
movi v0 0 
return 
