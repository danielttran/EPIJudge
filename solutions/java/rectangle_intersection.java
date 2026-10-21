package epi;

import epi.test_framework.EpiTest;
import epi.test_framework.EpiUserType;
import epi.test_framework.GenericTest;
import java.util.Objects;

public class RectangleIntersection {
  @EpiUserType(ctorParams = {int.class, int.class, int.class, int.class})
  public static class Rect {
    int x, y, width, height;

    public Rect(int x, int y, int width, int height) {
      this.x = x;
      this.y = y;
      this.width = width;
      this.height = height;
    }

    @Override
    public boolean equals(Object other) {
      if (!(other instanceof Rect)) return false;
      Rect that = (Rect) other;
      return x == that.x && y == that.y && width == that.width && height == that.height;
    }

    @Override
    public int hashCode() { return Objects.hash(x, y, width, height); }

    @Override
    public String toString() {
      return "[" + x + ", " + y + ", " + width + ", " + height + "]";
    }
  }

  @EpiTest(testDataFile = "rectangle_intersection.tsv")
  public static Rect intersectRectangle(Rect r1, Rect r2) {
    long left = Math.max((long) r1.x, (long) r2.x);
    long bottom = Math.max((long) r1.y, (long) r2.y);
    long right = Math.min((long) r1.x + r1.width, (long) r2.x + r2.width);
    long top = Math.min((long) r1.y + r1.height, (long) r2.y + r2.height);
    if (right < left || top < bottom) return new Rect(0, 0, -1, -1);
    return new Rect(Math.toIntExact(left), Math.toIntExact(bottom),
                    Math.toIntExact(right - left), Math.toIntExact(top - bottom));
  }

  public static void main(String[] args) {
    System.exit(GenericTest.runFromAnnotations(args, "RectangleIntersection.java", RectangleIntersection.class).ordinal());
  }
}
