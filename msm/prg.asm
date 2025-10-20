.malloc
resn 2
push 0
read
dup
set 1
drop 1
push 0
read
get 0
add
dup
push 0
write
drop 1
get 1
ret

push 0
ret
.main
resn 3
push 0
read
dbg
prep malloc
push 5
call 1
dup
get 1
write
drop 1
push 0
dup
set 2
drop 1
.l1a
get 2
push 5
cmplt
jumpf l2a
push 3
dup
get 1
get 2
add
write
drop 1

.l1c
get 2
push 1
add
dup
set 2
drop 1

jump l2b
.l2a
jump l1b
.l2b
jump l1a
.l1b

get 1
read
dbg
recv
dup
set 0
drop 1
get 0
push 1
add
send
push 10
send
push 0
ret

push 0
ret
.start
prep main
call 0
halt
