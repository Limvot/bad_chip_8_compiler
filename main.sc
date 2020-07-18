
void drawhex(num, x ,y) {
    inline_asm(v3=num, v2=x, v1=y) #
        digit v3
        sprite v2 v1 5
    #
    return()
}

void main() {
    byte x
    byte y
    byte dx
    byte dy
    x = 0
    y = 0
    dx = 1
    dy = 1
    while (1) {
        drawhex(0xA, x, y)
        x += dx
        y += dy
        if (x == 40) {
            byte tmp
            tmp = 0
            tmp -= dx
            dx = tmp
        }
        if (y == 20) {
            byte tmp
            tmp = 0
            tmp -= dy
            dy = tmp
        }
    }
}

