.a
resn 1
get 0
push 4
add
ret

push 0
ret
.b
resn 2
get 0
get 1
add
ret

push 0
ret
.main
resn 1
push 12
dup
set 0
drop 1
prep a
get 0
call 1
dbg
prep b
get 0
push 13
call 2
dbg
push 0
ret

push 0
ret
.start
prep main
call 0
halt
