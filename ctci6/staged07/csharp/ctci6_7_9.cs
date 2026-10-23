using System;
using System.Collections.Generic;
using System.Text;
public class CircularArray<T> : IEnumerable<T>
{
    private readonly T[] items;
    private int head;
    public CircularArray(T[] initialValues)
    {
        items = initialValues.ToArray();
    }
    private void CheckIndex(int index)
    {
        if (index < 0 || index >= items.Length)
            throw new ArgumentOutOfRangeException(nameof(index));
    }
    public T Get(int index)
    {
        CheckIndex(index);
        return items[(head + index) % items.Length];
    }
    public void Set(int index, T value)
    {
        CheckIndex(index);
        items[(head + index) % items.Length] = value;
    }
    public void Rotate(int shift)
    {
        if (items.Length == 0)
            return;
        int step = shift % items.Length;
        if (step < 0)
            step += items.Length;
        head = (head + step) % items.Length;
    }
    public IEnumerator<T> GetEnumerator()
    {
        for (int index = 0; index < items.Length; ++index)
            yield return items[(head + index) % items.Length];
    }
    System.Collections.IEnumerator System.Collections.IEnumerable.GetEnumerator() =>
        GetEnumerator();
}
