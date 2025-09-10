.start
resn 1
push 0
dup
set 0
drop 1
.l1a
.l1c
get 0
dbg
get 0
push 1
add
dup
set 0
drop 1

get 0
push 10
cmple
jumpf l2a
jump l1c
jump l2b
.l2a
jump l1b
.l2b
jump l1a
.l1b

drop 1
halt
