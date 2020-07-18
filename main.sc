
void drawhex(num, x ,y) {
    inline_asm(v3=num, v2=x, v1=y) #
        digit v3
        sprite v2 v1 5
    #
    return()
}

void main() {
    if (1) {
        drawhex(0xB, 10, 10)
    } else {
        drawhex(0xA, 10, 10)
    }
    if (1) {
        drawhex(0xC, 20, 10)
    }
    if (0) {
        drawhex(0xD, 30, 10)
    }
}

