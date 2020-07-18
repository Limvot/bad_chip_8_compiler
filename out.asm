main: 
movi v0 0 
movr v3 v0 
movi v0 0 
movr v4 v0 
movi v0 1 
movr v5 v0 
movi v0 1 
movr v6 v0 
whiletopid1: 
movi v0 1 
snei v0 0 
jump whileendid2 
imovi savelabelid3 
store vF 
jump afterlabelid4 
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
afterlabelid4: 
movi v0 0xA 
movr v1 v0 
movr v0 v3 
movr v2 v0 
movr v0 v4 
movr v3 v0 
call drawhex 
imovi savelabelid3 
load vF 
movr v0 v5 
addr v3 v0 
movr v0 v6 
addr v4 v0 
movr v0 v3 
movr v1 v0 
movi v0 40 
movr v2 v0 
movi v0 0 
sner v1 v2 
movi v0 1 
snei v0 0 
jump afterthanid5 
movi v0 0 
movr v7 v0 
movr v0 v5 
subr v7 v0 
movr v0 v7 
movr v5 v0 
jump afterelseid6 
afterthanid5: 
afterelseid6: 
movr v0 v4 
movr v1 v0 
movi v0 20 
movr v2 v0 
movi v0 0 
sner v1 v2 
movi v0 1 
snei v0 0 
jump afterthanid7 
movi v0 0 
movr v7 v0 
movr v0 v6 
subr v7 v0 
movr v0 v7 
movr v6 v0 
jump afterelseid8 
afterthanid7: 
afterelseid8: 
jump whiletopid1 
whileendid2: 
 
drawhex: 
imovi savelabelid9 
store vF 
jump afterlabelid10 
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
afterlabelid10: 
movr v0 v3 
movr v3 v0 
movr v0 v4 
movr v2 v0 
movr v0 v5 
movr v1 v0 
 
        digit v3 
        sprite v2 v1 5 
    imovi savelabelid9 
load vF 
movi v0 0 
return 
