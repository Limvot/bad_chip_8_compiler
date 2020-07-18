
void drawhex(num, x ,y) {
    inline_asm(v3=num, v2=x, v1=y) #
        digit v3
        sprite v2 v1 5
    #
    return()
}

void main() {
    drawhex(0xA, 10, 10)
}

