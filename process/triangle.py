def triangle_type(a, b, c):
    if a + b <= c or a + c <= b or b + c <= a:
        return "不能构成三角形"
    else:
        if a == b or a == c or b == c:
            if a == c:
                return "等边三角形"
            else:
                return "等腰三角形"
        else:
            return "一般三角形"
def main():
    a = int(input("请输入第一条边的长度："))
    b = int(input("请输入第二条边的长度："))
    c = int(input("请输入第三条边的长度："))


    triangle = triangle_type(a, b, c)
    print(triangle)

if __name__ == "__main__":
    main()
