export function getYiJiData(date) {
  // Simulate data
  const data = {
  yi: [
    "Sacrifice", "Prayer for Blessing", "Marriage", "Wealth Acquisition",
    "Housewarming", "Starting a Business", "Signing a Contract", "Travel",
    "Building a House", "Relocation", "Seeking Medical Treatment", "Education",
    "Litigation", "Planting", "Purchasing Property", "Making Offerings",
    "Engagement", "Construction", "Hiring Employees", "Starting a New Job"
  ],
  ji: [
    "Groundbreaking", "Excavation", "Funeral", "Travel",
    "Starting a Business", "Signing a Contract", "Marriage", "Moving",
    "Litigation", "Climbing", "Visiting Friends", "Purchasing Property",
    "Making Offerings", "Engagement", "Construction", "Planting",
    "Hiring Employees", "Starting a New Job", "Education", "Seeking Medical Treatment"
  ]
};

  //
  // random choose!!!!!!
  function seededRandom(seed) {
    let x = Math.sin(seed) * 10000;
    return x - Math.floor(x);
  }
  const seed = date.getFullYear() * 10000 + (date.getMonth() + 1) * 100 + date.getDate();
  function shuffleArray(arr, seed) {
    let shuffled = [...arr];
    for (let i = shuffled.length - 1; i > 0; i--) {
      let j = Math.floor(seededRandom(seed + i) * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
  }
  const minCount = 1;
  const maxCount = 1;
  const yiCount = Math.floor(seededRandom(seed) * (maxCount - minCount + 1)) + minCount;
  const jiCount = Math.floor(seededRandom(seed + 1) * (maxCount - minCount + 1)) + minCount;

  const yi = shuffleArray(data.yi, seed).slice(0, yiCount);
  const ji = shuffleArray(data.ji, seed + 1).slice(0, jiCount);

  return { yi, ji };
}
//
//
//