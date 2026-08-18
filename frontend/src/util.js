export function orderedShares(shares) {
    const items = Object.keys(shares).map((key) => [key, shares[key]]);
    items.sort((first, second) => second[1].count - first[1].count);
    return items;
}
