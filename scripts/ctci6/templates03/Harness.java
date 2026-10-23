public class Harness {
  static final JsonObject CONFIG = Json.parse(CONFIG_VALUE).asObject();
  static Throwable unwrap(Throwable error) {
    while (error instanceof java.lang.reflect.InvocationTargetException && error.getCause() != null) error = error.getCause();
    return error;
  }
  static JsonValue execute(JsonObject row) throws Exception {
    String ref = row.get("ref").asString(); var args = row.get("arguments").asArray();
SORT_BRANCH_START
    if (ref.equals("3.5")) {
      var stack = new IntStack();
      for (var value : args.get(0).asArray()) stack.Push(value.asInt());
      new Solution().SortStack(stack); var output = new JsonArray();
      while (!stack.IsEmpty()) {
        output.add(stack.Pop());
        if (output.size() > args.get(0).asArray().size()) return new JsonObject().add("actual", output).add("mutationOk", false);
      }
      return new JsonObject().add("actual", output).add("mutationOk", true);
    }
SORT_BRANCH_END
    var operations = args.get(0).asArray(); var arguments = args.get(1).asArray(); var config = CONFIG.get(ref).asObject();
    var type = Class.forName(config.get("cls").asString()); Object instance = null;
    var output = new JsonArray(); boolean valid = true;
    var animals = new IdentityHashMap<Animal, String>();
    for (int i = 0; i < operations.size(); i++) {
      String op = operations.get(i).asString();
      try {
        var raw = arguments.get(i).asArray(); Object[] parameters = new Object[raw.size()];
        if (op.equals("Enqueue")) {
          var animal = new Animal(raw.get(0).asInt(), raw.get(1).asString());
          animals.put(animal, animal.Id + ":" + animal.Species); parameters = new Object[] {animal};
        } else for (int j = 0; j < raw.size(); j++) parameters[j] = raw.get(j).asInt();
        if (i == 0) {
          instance = parameters.length == 0 ? type.getDeclaredConstructor().newInstance() : type.getDeclaredConstructor(int.class).newInstance(parameters);
          output.add(Json.NULL); continue;
        }
        var method = Arrays.stream(type.getMethods()).filter(m -> m.getName().equals(op)).findFirst().orElseThrow();
        Object value = method.invoke(instance, parameters); String kind = config.get("methods").asObject().get(op).asString();
        JsonValue observed = Json.NULL;
        if (kind.equals("animal") && value != null) {
          if (!(value instanceof Animal) || !animals.containsKey((Animal) value)) { valid = false; observed = new JsonObject().add("invalidIdentity", true); }
          else observed = Json.value(((Animal) value).Id);
        } else if (kind.equals("i")) {
          if (!(value instanceof Integer)) { valid = false; observed = new JsonObject().add("invalidReturn", "integer"); }
          else observed = Json.value((int) value);
        } else if (kind.equals("b")) {
          if (!(value instanceof Boolean)) { valid = false; observed = new JsonObject().add("invalidReturn", "boolean"); }
          else observed = Json.value((boolean) value);
        } else if (kind.equals("void") && value != null) valid = false;
        output.add(observed);
      } catch (Throwable error) {
        var actual = unwrap(error);
        if (actual instanceof BankError bank) output.add(new JsonObject().add("error", bank.Code));
        else throw new RuntimeException(actual);
      }
    }
    for (var pair : animals.entrySet()) valid &= pair.getValue().equals(pair.getKey().Id + ":" + pair.getKey().Species);
    return new JsonObject().add("actual", output).add("mutationOk", valid);
  }
  public static void main(String[] ignored) throws Exception {
    var results = new JsonArray();
    for (var row : Json.parse(Files.readString(Path.of("cases.json"))).asArray()) {
      try { results.add(execute(row.asObject())); }
      catch (Throwable error) { results.add(new JsonObject().add("error", unwrap(error).toString())); }
    }
    Files.writeString(Path.of("results.json"), results.toString());
  }
}
