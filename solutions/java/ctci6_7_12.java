import java.util.*;
class HashTable<K, V> {
  private static class Node<K, V> {
    final K key;
    V value;
    Node<K, V> next;
    Node(K key, V value, Node<K, V> next) {
      this.key = key;
      this.value = value;
      this.next = next;
    }
  }
  private final ArrayList<Node<K, V>> buckets;
  public HashTable(int capacity) {
    buckets = new ArrayList<>(Collections.nCopies(capacity, null));
  }
  private int index(K key) {
    return Math.floorMod(key.hashCode(), buckets.size());
  }
  private Node<K, V> find(K key) {
    for (var node = buckets.get(index(key)); node != null; node = node.next)
      if (Objects.equals(node.key, key))
        return node;
    return null;
  }
  public void Put(K key, V value) {
    var node = find(key);
    if (node != null) {
      node.value = value;
      return;
    }
    int slot = index(key);
    buckets.set(slot, new Node<>(key, value, buckets.get(slot)));
  }
  public V Get(K key) {
    var node = find(key);
    if (node == null)
      throw new NoSuchElementException();
    return node.value;
  }
  public boolean Contains(K key) {
    return find(key) != null;
  }
  public boolean Remove(K key) {
    int slot = index(key);
    Node<K, V> previous = null;
    var node = buckets.get(slot);
    while (node != null) {
      if (Objects.equals(node.key, key)) {
        if (previous == null)
          buckets.set(slot, node.next);
        else
          previous.next = node.next;
        return true;
      }
      previous = node;
      node = node.next;
    }
    return false;
  }
}
