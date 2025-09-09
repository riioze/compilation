.start
resn 1
push 1
dup
set 0
drop 1
get 0
push 0
cmpeq
jumpf l1a
push 0
dbg

jump l1b
.l1a
get 0
push 1
cmpeq
jumpf l2a
push 5
dbg

jump l2b
.l2a
push 10
dbg

.l2b
.l1b

drop 1
halt
