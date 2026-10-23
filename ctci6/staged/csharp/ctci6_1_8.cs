using System;
using System.Collections.Generic;
using System.Text;
public class Solution {
    public void ZeroMatrix(int[][] matrix) {
        int rows = matrix.Length;
        if (rows == 0) return;
        int cols = matrix[0].Length;
        bool[] zeroRows = new bool[rows];
        bool[] zeroCols = new bool[cols];
        for (int r = 0; r < rows; ++r) {
            for (int c = 0; c < cols; ++c) {
                if (matrix[r][c] == 0) { zeroRows[r] = true; zeroCols[c] = true; }
            }
        }
        for (int r = 0; r < rows; ++r) {
            for (int c = 0; c < cols; ++c) {
                if (zeroRows[r] || zeroCols[c]) matrix[r][c] = 0;
            }
        }
    }
}
