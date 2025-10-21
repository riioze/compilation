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
.free
resn 1
push 0
ret

push 0
ret
.print
resn 4
get 0
push 10
mod
dup
set 1
drop 1
get 0
push 10
div
dup
set 2
drop 1
push 0
dup
set 3
drop 1
get 2
push 0
cmpne
jumpf l1a
prep print
get 2
call 1
push 1
add
dup
set 3
drop 1
jump l1b
.l1a
.l1b
push 48
get 1
add
send
get 3
ret

push 0
ret
.println
resn 2
prep print
get 0
call 1
dup
set 1
drop 1
push 10
send
get 1
ret

push 0
ret
.main
resn 3
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
.l2a
get 2
push 5
cmplt
jumpf l3a
push 3
dup
get 1
get 2
add
write
drop 1

.l2c
get 2
push 1
add
dup
set 2
drop 1

jump l3b
.l3a
jump l2b
.l3b
jump l2a
.l2b

prep println
get 1
read
call 1
drop 1
push 0
ret

push 0
ret
.start
prep main
call 0
halt
