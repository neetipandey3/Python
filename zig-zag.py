"""
Zig Zag Converter

Example 1:

Input: s = "PAYPALISHIRING", numRows = 3
Output: "PAHNAPLSIIGYIR"
"""

class ZigZag:

    def convert(self, s, numRows):
        """
        :type s: str
        :type numRows: int
        :rtype: str
        """
        row_num = 0
        row = [[] for idx in range(numRows)]
        if numRows == 1:
            return s
        next_row = True
        for c in s:
            row[row_num].append(c)
            if row_num == numRows - 1:
                next_row = False
            if row_num == 0:
                next_row = True

            if next_row:
                row_num += 1
            else:
                row_num -= 1

        zig_zag_str = ""
        for idx in range(numRows):
            zig_zag_str += "".join(row[idx])
            #print("".join(row[idx]), end = "")
        return zig_zag_str

def main():
    z = ZigZag()
    print(z.convert("QWERTYASDFG", 3))


if __name__ == "__main__":
    main()
