.start
resn 2
push 0
dup
set 0
drop 1
.l1a
get 0
push 5
cmplt
jumpf l2a
push 0
dup
set 1
drop 1
.l3a
get 1
get 0
cmplt
jumpf l4a
get 1
dbg

.l3c
get 1
push 1
add
dup
set 1
drop 1

jump l4b
.l4a
jump l3b
.l4b
jump l3a
.l3b


.l1c
get 0
push 1
add
dup
set 0
drop 1

jump l2b
.l2a
jump l1b
.l2b
jump l1a
.l1b


drop 2
halt
