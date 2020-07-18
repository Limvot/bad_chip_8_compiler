main: 
imovi savelabelid1 
store vF 
jump savelabelid2 
savelabelid1: 
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
savelabelid2: 
movi v0 0xA 
movr v1 v0 
movi v0 10 
movr v2 v0 
movi v0 10 
movr v3 v0 
call drawhex 
imovi savelabelid1 
load vF 
 
drawhex: 
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
movr v0 v1 
movr v3 v0 
movr v0 v2 
movr v2 v0 
movr v0 v3 
movr v1 v0 
 
        digit v3 
        sprite v2 v1 5 
    imovi savelabelid3 
load vF 
movi v0 0 
return 
