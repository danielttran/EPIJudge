function shortestEquivalentPath(path) {
  const absolute = path.startsWith("/"),
    components = [];
  for (const part of path.split("/")) {
    if (!part || part === ".") continue;
    if (part === "..") {
      if (components.length && components.at(-1) !== "..") components.pop();
      else if (!absolute) components.push("..");
    } else components.push(part);
  }
  return (absolute ? "/" : "") + components.join("/");
}

module.exports = { shortestEquivalentPath };
