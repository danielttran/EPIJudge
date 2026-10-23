'use strict';
function EncodeXml(
  elementNames,
  elementTexts,
  children,
  attributeOwners,
  attributeNames,
  attributeValues,
  codeNames,
  codes,
) {
  if (elementNames.length === 0) return [];
  const lookup = new Map(codeNames.map((name, i) => [name, String(codes[i])])),
    attributes = Array.from({ length: elementNames.length }, () => []),
    result = [],
    events = [[0, false]];
  for (let i = 0; i < attributeOwners.length; ++i) attributes[attributeOwners[i]].push(i);
  while (events.length) {
    const [node, exiting] = events.pop();
    if (exiting) {
      result.push("0");
      continue;
    }
    result.push(lookup.get(elementNames[node]));
    for (const attribute of attributes[node])
      result.push(lookup.get(attributeNames[attribute]), attributeValues[attribute]);
    result.push("0");
    events.push([node, true]);
    if (elementTexts[node].length) result.push(elementTexts[node]);
    else
      for (let i = children[node].length - 1; i >= 0; --i) events.push([children[node][i], false]);
  }
  return result;
}
